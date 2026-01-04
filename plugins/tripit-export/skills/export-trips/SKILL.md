# TripIt Export Skill

Export all TripIt travel data (trips, flights, lodging, activities) to JSON format using TripIt's undocumented API v2.

## Trigger Phrases

- "export tripit data"
- "export my trips from tripit"
- "download tripit trips"
- "/tripit-export"

## Prerequisites

- **dev-browser plugin**: Browser automation with persistent state
- **TripIt account**: User must be able to log in to tripit.com

## API Reference

### Discovered Endpoints

```
# List upcoming trips (paginated)
GET /api/v2/list/trip?exclude_types=weather&page_size=50&past=false&should_sort_trips_by_date=true&traveler=true&trip_permission_filter=all&page_num=1&isPast=false

# List past trips (paginated)
GET /api/v2/list/trip?exclude_types=weather&page_size=50&past=true&should_sort_trips_by_date=true&traveler=all&trip_permission_filter=all&page_num=1&isPast=true

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
  "num_bytes": "...",
  "page_num": "1",
  "page_size": "50",
  "max_page": "1",
  "Trip": [...],
  "Profile": {...}
}
```

**Trip Details Response:**
```json
{
  "timestamp": "...",
  "Trip": {...},
  "ActivityObject": [...],   // Tours, events, etc.
  "AirObject": [...],        // Flights
  "LodgingObject": [...],    // Hotels
  "Profile": {...}
}
```

## Workflow

### Step 1: Launch Browser and Authenticate

Start the dev-browser server:

```bash
cd ~/.claude/plugins/cache/dev-browser-marketplace/dev-browser/*/skills/dev-browser && ./server.sh &
```

Wait for "Ready" message, then navigate to TripIt:

```typescript
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect("http://127.0.0.1:9222");
const page = await client.page("tripit");
await page.setViewportSize({ width: 1280, height: 800 });
await page.goto("https://www.tripit.com/app/trips");
await waitForPageLoad(page);

console.log("Please log in to TripIt...");
await client.disconnect();
```

**Tell user to log in manually, then confirm when done.**

### Step 2: Fetch All Trips

After authentication, fetch upcoming and past trips with pagination:

```typescript
import { connect } from "@/client.js";
import { writeFileSync } from "fs";

const client = await connect("http://127.0.0.1:9222");
const page = await client.page("tripit");

// Helper to fetch paginated trips
async function fetchAllTrips(past: boolean): Promise<any[]> {
  const allTrips: any[] = [];
  let pageNum = 1;
  let maxPage = 1;

  do {
    const params = new URLSearchParams({
      exclude_types: "weather",
      page_size: "50",
      past: String(past),
      should_sort_trips_by_date: "true",
      traveler: past ? "all" : "true",
      trip_permission_filter: "all",
      page_num: String(pageNum),
      isPast: String(past)
    });

    const response = await page.evaluate(async (url) => {
      const res = await fetch(url, {
        headers: {
          "Accept": "application/json",
          "X-Requested-With": "XMLHttpRequest"
        }
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

const upcomingTrips = await fetchAllTrips(false);
const pastTrips = await fetchAllTrips(true);

console.log(`Found ${upcomingTrips.length} upcoming trips`);
console.log(`Found ${pastTrips.length} past trips`);

writeFileSync("tmp/all-trips.json", JSON.stringify({
  upcoming: upcomingTrips,
  past: pastTrips
}, null, 2));

await client.disconnect();
```

### Step 3: Fetch Full Trip Details

For each trip, fetch complete details including flights, lodging, and activities:

```typescript
import { connect } from "@/client.js";
import { readFileSync, writeFileSync } from "fs";

const client = await connect("http://127.0.0.1:9222");
const page = await client.page("tripit");

const allTrips = JSON.parse(readFileSync("tmp/all-trips.json", "utf-8"));
const allTripUuids = [...allTrips.upcoming, ...allTrips.past].map(t => t.uuid);

const tripDetails: Record<string, any> = {};

for (const uuid of allTripUuids) {
  console.log(`Fetching details for trip ${uuid}...`);

  const details = await page.evaluate(async (tripUuid) => {
    const res = await fetch(
      `/api/v2/get/trip/uuid/${tripUuid}/include_objects/true?exclude_types=weather`,
      {
        headers: {
          "Accept": "application/json",
          "X-Requested-With": "XMLHttpRequest"
        }
      }
    );
    return res.json();
  }, uuid);

  tripDetails[uuid] = {
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

  // Rate limiting - small delay between requests
  await page.waitForTimeout(500);
}

writeFileSync("tmp/trip-details.json", JSON.stringify(tripDetails, null, 2));
console.log(`Exported ${Object.keys(tripDetails).length} trips with full details`);

await client.disconnect();
```

### Step 4: Generate Final Export

Combine all data into a clean export format:

```typescript
import { readFileSync, writeFileSync } from "fs";

const allTrips = JSON.parse(readFileSync("tmp/all-trips.json", "utf-8"));
const tripDetails = JSON.parse(readFileSync("tmp/trip-details.json", "utf-8"));

const exportData = {
  exportDate: new Date().toISOString(),
  summary: {
    upcomingTrips: allTrips.upcoming.length,
    pastTrips: allTrips.past.length,
    totalTrips: allTrips.upcoming.length + allTrips.past.length
  },
  trips: Object.entries(tripDetails).map(([uuid, details]: [string, any]) => ({
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
console.log(`Export complete: ${outputPath}`);
```

## Output Format

The final JSON export includes:

```json
{
  "exportDate": "2025-01-02T...",
  "summary": {
    "upcomingTrips": 2,
    "pastTrips": 45,
    "totalTrips": 47
  },
  "trips": [
    {
      "uuid": "...",
      "name": "Trip Name",
      "startDate": "2025-01-15",
      "endDate": "2025-01-20",
      "primaryLocation": "Tokyo, Japan",
      "trip": { /* full trip metadata */ },
      "flights": [ /* AirObject array */ ],
      "lodging": [ /* LodgingObject array */ ],
      "activities": [ /* ActivityObject array */ ],
      "cars": [ /* CarObject array */ ],
      "restaurants": [ /* RestaurantObject array */ ],
      "notes": [ /* NoteObject array */ ],
      "transport": [ /* TransportObject array */ ],
      "rail": [ /* RailObject array */ ],
      "cruise": [ /* CruiseObject array */ ]
    }
  ]
}
```

## Error Handling

- **401 Unauthorized**: Session expired. Re-authenticate by navigating to TripIt login page.
- **Rate limiting**: Add delays between API calls if receiving 429 errors.
- **Empty responses**: Some trips may have no flights/lodging - this is normal.

## Notes

- TripIt API v2 is undocumented and may change without notice
- Authentication is session-based (cookies) - no API key required
- Large trip histories may take several minutes to export
- The `exclude_types=weather` param reduces response size by omitting weather forecasts
