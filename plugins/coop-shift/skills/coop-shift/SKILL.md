# Coop Shift

A skill for finding and booking Park Slope Food Coop shifts using browser automation.

## Description

This skill should be used when the user asks to "book a coop shift", "find available shifts", "check my coop schedule", or wants to manage their PSFC work assignments. It uses browser automation since PSFC is a server-rendered Django app without a REST API.

## Trigger Phrases

- "book a coop shift"
- "find available shifts at the coop"
- "check my coop schedule"
- "cancel my coop shift"
- "what shifts are available this week"
- "/coop-shift [shift type]"

## Prerequisites

1. **dev-browser plugin** must be installed
2. **1Password CLI** must be installed and configured (`op` command available)
3. PSFC credentials stored in 1Password with title "Coop Member Services"

### Installing 1Password CLI

If `op` command is not found:

```bash
brew install --cask 1password-cli
```

Then enable CLI integration in the 1Password app:
1. Open 1Password → Settings → Developer
2. Enable "Integrate with 1Password CLI"

## Member Info

| Field | Value |
|-------|-------|
| Member ID | `12345` |
| Name | Casey Gollan |
| Work Assignment | Freelance |
| Initials | `CG` |

## Site Architecture

PSFC Member Services is a **server-rendered Django app** with no REST API. All actions are form submissions via standard page navigation.

**Base URL:** `https://members.foodcoop.com/services/`

### Key URLs

| Page | URL Pattern |
|------|-------------|
| Home | `/services/` |
| Shift Calendar | `/services/shifts/{page}/{job_id}/{time_slot}/{date}/` |
| Shift Details | `/services/shift_claim/{shift_id}/` |
| Job Descriptions | `/services/jobs/` |

### URL Parameters

**Shift Calendar:**
- `page`: Week offset (0 = current, 1 = next, etc.)
- `job_id`: Filter by job type (0 = all)
- `time_slot`: Filter by time (0 = entire day)
- `date`: Reference date (YYYY-MM-DD)

**Time Slots:**
| Slot | ID |
|------|-----|
| Entire day | `0` |
| Early Morning (4-7am) | `1` |
| Morning (7-10am) | `2` |
| Mid-day (10am-2pm) | `3` |
| Afternoon (2-6pm) | `4` |
| Evening (6-11pm) | `5` |

## Job Types

Common job types available in the dropdown:

| Job | Notes |
|-----|-------|
| Checkout 💳 | Register operation |
| Receiving: Lifting 🚚 | Heavy lifting required |
| Receiving: Stocking 📦 | Shelf stocking |
| Flex Worker 🥫 | Flexible assignments |
| Cleaning 🏝 | End of day cleaning |
| Inventory 📋 | Stock counting |
| 🥕 Carrot 🥕 | Bonus shift (earn carrots) |

Shifts marked with 🥕 are "carrot shifts" - completing 5 earns a bonus.

## Constraints

| Rule | Details |
|------|---------|
| Max scheduled shifts | 2 within 6 weeks |
| Cancellation deadline | 8 PM the night before |
| Late cancellation | Requires a cancel ticket |

## Workflow

### Step 1: Navigate to Member Services

```
browser_navigate: https://members.foodcoop.com/services/
```

Take a snapshot to verify logged in status. If redirected to login page, proceed to Step 1a.

### Step 1a: Authenticate via 1Password (if needed)

If the page shows a login form, get credentials from 1Password:

```bash
op item get "Coop Member Services" --fields username,password --format json
```

Then fill the login form:

```javascript
// Fill member number
browser_type: element="Member Number field", ref="<ref>", text="<member_number>"

// Fill password
browser_type: element="Password field", ref="<ref>", text="<password>"

// Click login
browser_click: element="Log In button", ref="<ref>"
```

**Handling 2FA (if prompted):**

If PSFC prompts for a one-time password:

```bash
op item get "Coop Member Services" --otp
```

Enter the OTP code in the verification field.

### Step 2: Check Current Status

From the home page, extract:
- Current shift credit balance
- Scheduled shifts (dates, times, types)
- Household status (Alert/Active)
- Cancel tickets available

### Step 3: Navigate to Shift Calendar

```
browser_navigate: https://members.foodcoop.com/services/shifts/
```

Or with filters:
```
browser_navigate: https://members.foodcoop.com/services/shifts/0/0/0/2026-01-01/
```

### Step 4: Filter Shifts (Optional)

Use the dropdowns to filter by:
- Job type (combobox)
- Time of day (combobox)

Or use URL parameters directly.

### Step 5: Find Available Shifts

Take a snapshot and parse the shift calendar. Available shifts appear as links:
- Format: `{time} {job_type} {emoji}`
- Example: `6:00pm Checkout 💳`
- Booked shifts show ✅: `6:00pm Checkout 💳 ✅`

### Step 6: Present Options to User

Show matching shifts with:
- Date and time
- Job type
- Whether it's a carrot shift (🥕)

Use `AskUserQuestion` to confirm which shift to book.

### Step 7: Book the Shift

1. Click on the shift link to go to shift details page
2. Select credit recipient (radio button - default to self)
3. Fill in initials in 3 agreement fields (`CG`)
4. Click "Work this shift" button
5. Handle "Are you sure?" confirmation dialog (accept)

```javascript
// Fill initials
browser_fill_form: [
  {name: "initials 1", type: "textbox", ref: "<ref>", value: "CG"},
  {name: "initials 2", type: "textbox", ref: "<ref>", value: "CG"},
  {name: "initials 3", type: "textbox", ref: "<ref>", value: "CG"}
]

// Click submit
browser_click: "Work this shift" button

// Handle confirmation
browser_handle_dialog: accept
```

### Step 8: Confirm Success

After booking, the page redirects to the shift calendar with message:
> "You are now scheduled to work this shift."

## Cancellation

### Cancel a Shift

1. Navigate to shift details: `/services/shift_claim/{shift_id}/`
2. Click "CANCEL SHIFT" button
3. Handle "Are you sure?" confirmation dialog (accept)
4. Redirects with message: "You have cancelled your shift."

**Note:** Cancellation is only available before 8 PM the night before the shift.

## Error Handling

| Situation | Response |
|-----------|----------|
| Not logged in | Authenticate via 1Password (Step 1a) |
| 1Password item not found | Item should be titled "Coop Member Services" |
| Login failed | Check credentials in 1Password, may need manual update |
| Max shifts reached | Inform user they have 2 shifts scheduled (max allowed) |
| Shift no longer available | Refresh calendar and show alternatives |
| Past cancellation deadline | Inform user they need a cancel ticket |

## Housemates

Shifts can be credited to housemates instead of self:

| Name | Member ID | Status |
|------|-----------|--------|
| Alex Johnson | 11111 | Active |
| Sam Williams | 22222 | Active |
| Jordan Lee | 33333 | Active |
| Taylor Brown | 44444 | Active |
| Morgan Davis | 55555 | Active |

When booking, a radio button allows selecting who receives shift credit.

## Example Session

**User:** "find me a checkout shift this weekend"

**Assistant:**
1. Navigate to shift calendar with Checkout filter
2. Filter to weekend dates
3. Present available shifts:
   ```
   Found 3 Checkout shifts this weekend:

   1. Saturday Jan 10, 6:00 PM - Checkout 💳
   2. Sunday Jan 11, 10:30 AM - Checkout 💳
   3. Sunday Jan 11, 3:30 PM - Checkout 💳

   Which would you like to book?
   ```
4. User picks #1
5. Book it → fill initials → confirm
6. "Booked! You're scheduled for Checkout at 6:00 PM on Saturday Jan 10."

## Tools Used

| Tool | Purpose |
|------|---------|
| `Bash` | Run 1Password CLI commands for auth |
| `browser_navigate` | Navigate to PSFC pages |
| `browser_snapshot` | Read page state |
| `browser_click` | Click buttons and links |
| `browser_type` | Fill login credentials |
| `browser_fill_form` | Fill initials fields |
| `browser_select_option` | Use dropdown filters |
| `browser_handle_dialog` | Accept confirmation dialogs |
| `AskUserQuestion` | Confirm shift selection |
