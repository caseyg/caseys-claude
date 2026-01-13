---
name: tripit-export
description: Export TripIt travel data (trips, flights, hotels) to JSON using browser
  automation. Use when the user asks to export, download, or backup their TripIt data.
---

# TripIt Export

Export all TripIt travel data (trips, flights, lodging, activities) to JSON format using TripIt's undocumented API v2.

## Trigger Phrases

- "export tripit data"
- "export my trips from tripit"
- "download tripit trips"
- `/tripit-export`

## Prerequisites

- **dev-browser plugin**: Browser automation with persistent state
- **TripIt account**: User must be able to log in to tripit.com

## API Reference

### Discovered Endpoints

```
# List upcoming trips (paginated)
GET /api/v2/list/trip?exclude_types=weather&page_size=50&past=false&traveler=true&page_num=1

# List past trips (paginated)
GET /api/v2/list/trip?exclude_types=weather&page_size=50&past=true&traveler=all&page_num=1

# Get full trip details (includes flights, lodging, activities)
GET /api/v2/get/trip/uuid/{trip-uuid}/include_objects/true?exclude_types=weather

# User profile
GET /api/v2/get/profile
```

### Response Structure

**Trip List Response:**
```json
{
  "timestamp": "...",
  "page_num": "1",
  "page_size": "50",
  "max_page": "1",
  "Trip": [...]
}
```

**Trip Details Response:**
```json
{
  "Trip": {...},
  "AirObject": [...],
  "LodgingObject": [...],
  "ActivityObject": [...],
  "CarObject": [...],
  "RestaurantObject": [...],
  "NoteObject": [...],
  "TransportObject": [...],
  "RailObject": [...],
  "CruiseObject": [...]
}
```

## Workflow

### Step 1: Launch Browser and Authenticate

Navigate to TripIt and have the user log in:

```typescript
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect("http://127.0.0.1:9222");
const page = await client.page("tripit");
await page.goto("https://www.tripit.com/app/trips");
await waitForPageLoad(page);

console.log("Please log in to TripIt...");
```

**Tell user to log in manually, then confirm when done.**

### Step 2: Fetch All Trips

After authentication, fetch upcoming and past trips with pagination:

```typescript
async function fetchAllTrips(page, past: boolean): Promise<any[]> {
  const allTrips: any[] = [];
  let pageNum = 1;
  let maxPage = 1;

  do {
    const params = new URLSearchParams({
      exclude_types: "weather",
      page_size: "50",
      past: String(past),
      traveler: past ? "all" : "true",
      page_num: String(pageNum)
    });

    const response = await page.evaluate(async (url) => {
      const res = await fetch(url, {
        headers: { "Accept": "application/json" }
      });
      return res.json();
    }, `/api/v2/list/trip?${params}`);

    if (response.Trip) {
      const trips = Array.isArray(response.Trip) ? response.Trip : [response.Trip];
      allTrips.push(...trips);
    }

    maxPage = parseInt(response.max_page || "1");
    pageNum++;
  } while (pageNum <= maxPage);

  return allTrips;
}

const upcomingTrips = await fetchAllTrips(page, false);
const pastTrips = await fetchAllTrips(page, true);
```

### Step 3: Fetch Full Trip Details

For each trip, fetch complete details:

```typescript
const tripDetails = {};

for (const trip of [...upcomingTrips, ...pastTrips]) {
  const details = await page.evaluate(async (uuid) => {
    const res = await fetch(
      `/api/v2/get/trip/uuid/${uuid}/include_objects/true?exclude_types=weather`,
      { headers: { "Accept": "application/json" } }
    );
    return res.json();
  }, trip.uuid);

  tripDetails[trip.uuid] = {
    trip: details.Trip,
    flights: details.AirObject || [],
    lodging: details.LodgingObject || [],
    activities: details.ActivityObject || [],
    cars: details.CarObject || [],
    restaurants: details.RestaurantObject || [],
    notes: details.NoteObject || [],
    transport: details.TransportObject || [],
    rail: details.RailObject || [],
    cruise: details.CruiseObject || []
  };

  // Rate limiting
  await page.waitForTimeout(500);
}
```

### Step 4: Generate Final Export

```typescript
const exportData = {
  exportDate: new Date().toISOString(),
  summary: {
    upcomingTrips: upcomingTrips.length,
    pastTrips: pastTrips.length,
    totalTrips: upcomingTrips.length + pastTrips.length
  },
  trips: Object.entries(tripDetails).map(([uuid, details]) => ({
    uuid,
    name: details.trip?.display_name,
    startDate: details.trip?.start_date,
    endDate: details.trip?.end_date,
    primaryLocation: details.trip?.primary_location,
    ...details
  }))
};

const outputPath = `tripit-export-${new Date().toISOString().split("T")[0]}.json`;
writeFileSync(outputPath, JSON.stringify(exportData, null, 2));
```

## Output Format

```json
{
  "exportDate": "2026-01-13T...",
  "summary": {
    "upcomingTrips": 2,
    "pastTrips": 45,
    "totalTrips": 47
  },
  "trips": [
    {
      "uuid": "...",
      "name": "Trip Name",
      "startDate": "2026-01-15",
      "endDate": "2026-01-20",
      "primaryLocation": "Tokyo, Japan",
      "trip": { /* full trip metadata */ },
      "flights": [ /* AirObject array */ ],
      "lodging": [ /* LodgingObject array */ ],
      "activities": [ /* ActivityObject array */ ],
      "cars": [],
      "restaurants": [],
      "notes": [],
      "transport": [],
      "rail": [],
      "cruise": []
    }
  ]
}
```

## Error Handling

- **401 Unauthorized**: Session expired. Re-authenticate by navigating to TripIt login.
- **Rate limiting**: Add delays between API calls if receiving 429 errors.
- **Empty responses**: Some trips may have no flights/lodging - this is normal.

## Notes

- TripIt API v2 is undocumented and may change without notice
- Authentication is session-based (cookies) - no API key required
- Large trip histories may take several minutes to export
- The `exclude_types=weather` param reduces response size
