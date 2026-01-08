# Book Fitness

A skill for checking and booking fitness classes at Chelsea Piers via direct API calls.

## Description

This skill should be used when the user asks to "book a class", "check yoga schedule", "sign up for fitness", or wants to book a class exactly 24 hours before it starts. It uses the Chelsea Piers REST API directly - no browser automation needed.

## Trigger Phrases

- "book yoga" / "book a yoga class"
- "check yoga schedule"
- "book [class type] at Chelsea Piers"
- "what classes are available tomorrow"
- "sign me up for [class name]"
- "cancel my [class] booking"
- "/book-fitness [class type]"
- "/book-fitness" (defaults to yoga)

## Prerequisites

1. **1Password CLI** must be installed and configured (`op` command available)
2. Chelsea Piers credentials stored in 1Password with title "Chelseapiers"

## API Reference

**Base URL:** `https://mymembership.chelseapiers.com/api`

### Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/user/authenticate` | POST | Login, get JWT token |
| `/user/account` | GET | Get/refresh user info |
| `/classes/search-booking-participations` | POST | Search classes |
| `/booking/create-booking` | POST | Book a class |
| `/booking/cancel-booking` | POST | Cancel a booking |

### Known IDs

| Entity | ID |
|--------|-----|
| User ID | `12345` |
| Downtown Brooklyn | `14` |
| Prospect Heights | `15` |
| Flatiron | `16` |

### Location Context

| Location | ID |
|----------|-----|
| Downtown Brooklyn | `14` |
| Prospect Heights | `15` |
| Flatiron | `16` |

Default to searching all locations unless user specifies.

### Activity Group IDs

| Activity | ID |
|----------|-----|
| Yoga (all types) | `1001` |

*Other activity IDs TBD - discover by removing filter and inspecting responses.*

## Workflow

### Step 1: Check for Cached Token

First, try to get a cached token from 1Password:

```bash
op item get "Chelseapiers" --fields token,token_expiry --format json
```

If token exists and `token_expiry` > now, skip to Step 3.

### Step 2: Authenticate (if needed)

Get credentials and authenticate:

```bash
op item get "Chelseapiers" --fields username,password --format json
```

```bash
curl -s -X POST https://mymembership.chelseapiers.com/api/user/authenticate -H "Content-Type: application/json" -d '{"email":"<username>","password":"<password>","sessionTimeoutOneMonth":false}'
```

**Response:**
```json
{
  "user": {"userId": 12345, "centerId": 14, "firstName": "Demo", ...},
  "token": "eyJ...",
  "expiry": "2026-01-02T19:37:58.202Z"
}
```

**Cache the token in 1Password:**

```bash
op item edit "Chelseapiers" token="<jwt_token>" token_expiry="<expiry_timestamp>"
```

This avoids re-authenticating on every request.

**Notes:**
- Use single-line curl commands. Multi-line commands with `\` continuations can fail.
- Avoid complex `$()` command substitution chains. Run commands separately and use the output directly.
- Store the token in a variable or substitute it directly into the curl command.

### Step 3: Search for Classes

```bash
curl -s -X POST "https://mymembership.chelseapiers.com/api/classes/search-booking-participations?selectedUserId=12345&selectedUserCenterId=14" -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"activityGroupIds":[1001],"activityIds":[],"centers":[14,15,16],"dateFrom":"<date>","dateTo":"<date>"}'
```

**Response:** Array of class objects:
```json
{
  "centerId": 14,
  "centerName": "Downtown Brooklyn",
  "personId": 12345,
  "participationListIndex": -1,
  "waitingListIndex": -1,
  "booking": {
    "id": 151433,
    "name": "Yoga Restorative",
    "date": "2026-01-02",
    "startTime": "18:30",
    "endTime": "19:30",
    "durationMinutes": 60,
    "instructorNames": ["Jane Doe"],
    "roomNames": ["Yoga Studio"],
    "bookedCount": 0,
    "classCapacity": 20,
    "waitingListCount": 0
  }
}
```

**Key fields:**
- `booking.id` → The `bookingId` for create-booking
- `participationListIndex` → `-1` = not booked, else your position
- `waitingListIndex` → `-1` = not on waitlist
- `bookedCount` vs `classCapacity` → availability

### Step 4: Present Options to User

Parse the response and show matching classes:

```
Found 3 yoga classes on Jan 2:

1. Hot Yoga Flow - 9:30 AM @ Downtown Brooklyn
   Instructor: Alex Smith | 38/38 (FULL, 7 waitlist)

2. Hot Yoga Athletic - 12:30 PM @ Downtown Brooklyn
   Instructor: Sam Johnson | 17/40 spots

3. Yoga Restorative - 6:30 PM @ Downtown Brooklyn
   Instructor: Jane Doe | 0/20 spots
```

Use `AskUserQuestion` to confirm which class to book.

### Step 5: Book the Class

```bash
curl -s -X POST https://mymembership.chelseapiers.com/api/booking/create-booking -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"selectedUserId":12345,"selectedUserCenterId":14,"bookingCenterId":<centerId>,"bookingId":<bookingId>}'
```

**Success:** Returns updated booking info.

**Too Early Error:**
```json
{
  "errorI18NMessage": "booking.tooEarlyToBookParticipant",
  "httpCode": 400
}
```

### Step 6: Report Result

Confirm to user:
- Class name, time, location
- Instructor
- Whether booked or added to waitlist

## Cancellation

### Cancel a Booking

```bash
curl -s -X POST https://mymembership.chelseapiers.com/api/booking/cancel-booking -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"bookingId":<bookingId>}'
```

To find bookings to cancel, search classes and look for `participationListIndex >= 0`.

## 24-Hour Advance Booking

Classes open for booking exactly 24 hours before start time.

### Logic

```
class_start = "2026-01-02T18:30:00"
booking_opens = class_start - 24h = "2026-01-01T18:30:00"
current_time = now()

if current_time >= booking_opens:
    → Book immediately
elif booking_opens - current_time < 5 minutes:
    → Wait and retry
else:
    → Tell user when booking opens
```

### Handling "Too Early" Error

If `create-booking` returns `booking.tooEarlyToBookParticipant`:
1. Calculate when booking opens (class time - 24h)
2. If within 5 minutes, wait and retry
3. Otherwise, inform user of opening time

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `booking.tooEarlyToBookParticipant` | 24h window not open | Wait or inform user |
| `401 Unauthorized` | Token expired | Re-authenticate |
| Class full | `bookedCount >= classCapacity` | Offer waitlist |

## Example Session

**User:** "book yoga tomorrow morning"

**Assistant:**
1. Check for cached token in 1Password
2. Search yoga classes for tomorrow across all locations
3. Present options:
   ```
   Found 3 morning yoga classes for Jan 2:

   1. Hot Yoga Flow - 9:30 AM @ Downtown Brooklyn
      Instructor: Alex Smith | 38/38 (FULL)

   2. Yoga Flow - 8:30 AM @ Prospect Heights
      Instructor: Jordan Lee | 25/40 spots

   3. Hot Yoga Flow - 7:15 AM @ Flatiron
      Instructor: Morgan Chen | 10/48 spots

   Which would you like to book?
   ```
4. User picks #2
5. Book it → success
6. "Booked Yoga Flow at 8:30 AM tomorrow at Prospect Heights"

## Tools Used

| Tool | Purpose |
|------|---------|
| `Bash` | 1Password CLI + curl requests |
| `AskUserQuestion` | Confirm class selection |
