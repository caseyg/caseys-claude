---
name: analyze-spending
description: Analyze finances using LunchMoney API. Use when the user asks about spending
  patterns, budget analysis, subscription audit, recurring expenses, or financial
  overview for periods like "this month", "last month", "this year", or custom date ranges.
---

# Analyze Spending with LunchMoney

Analyze your finances, identify spending patterns, review budgets, and find subscriptions you might want to cancel using data from LunchMoney.

## Trigger Phrases

- `/analyze-spending`
- "analyze my spending"
- "review my finances"
- "find subscriptions to cancel"
- "audit my recurring expenses"
- "how much did I spend on [category]?"
- "budget review for [period]"
- "where is my money going?"

## Prerequisites

1. **LunchMoney Account**: Active subscription with API access
2. **API Key**: Generate at https://my.lunchmoney.app/developers
3. **1Password Storage**: Store the API key in 1Password:
   - Item name: `Lunchmoney`
   - Field: `API Key`

## File Structure

```
skills/analyze-spending/
├── SKILL.md                      # This file
├── assets/
│   ├── MEMORY.md                 # Template for user preferences
│   └── subscription-audit-template.md  # Template for categorized report
└── data/                         # Runtime data (gitignored)
    ├── MEMORY.md                 # User preferences & decisions (copy from assets/)
    ├── cache/                    # Cached API responses
    │   ├── user.json             # User info (refreshed weekly)
    │   ├── categories.json       # Categories (refreshed weekly)
    │   ├── recurring_items.json  # Subscriptions (refreshed daily)
    │   └── transactions/         # Transaction data by month
    │       ├── 2025-12.json
    │       └── 2026-01.json
    ├── cache_meta.json           # Cache timestamps
    └── reports/                  # Generated markdown reports
        ├── 2026-01-19_spending-overview.md
        └── 2026-01-19_subscription-audit.md
```

---

## Memory & Preferences

The `MEMORY.md` file stores user preferences, decisions, and learned patterns across sessions.

### Initialize Memory

```bash
SKILL_DIR="skills/analyze-spending"
MEMORY_FILE="${SKILL_DIR}/data/MEMORY.md"
MEMORY_TEMPLATE="${SKILL_DIR}/assets/MEMORY.md"

# Create data directory and copy template if MEMORY.md doesn't exist
mkdir -p "${SKILL_DIR}/data"
if [ ! -f "$MEMORY_FILE" ]; then
  cp "$MEMORY_TEMPLATE" "$MEMORY_FILE"
  echo "Created MEMORY.md from template"
fi
```

### Reading Preferences from Memory

Extract YAML configuration blocks from MEMORY.md:

```bash
# Extract essential subscriptions (won't flag for cancellation)
ESSENTIAL_SUBS=$(sed -n '/^essential_subscriptions:/,/^[a-z]/p' "$MEMORY_FILE" | \
  grep -E '^\s+-\s+payee:' | sed 's/.*payee:\s*"\(.*\)"/\1/')

# Extract excluded categories
EXCLUDED_CATS=$(sed -n '/^excluded_categories:/,/^[a-z]/p' "$MEMORY_FILE" | \
  grep -E '^\s+-\s+"' | sed 's/.*"\(.*\)"/\1/')

# Extract watchlist
WATCHLIST=$(sed -n '/^watchlist:/,/^[a-z]/p' "$MEMORY_FILE" | \
  grep -E '^\s+-\s+payee:' | sed 's/.*payee:\s*"\(.*\)"/\1/')
```

### Updating Memory After Decisions

When the user makes a decision about a subscription, append to the Session History:

```bash
# Add a decision to memory
add_decision() {
  local date="$1"
  local subscription="$2"
  local decision="$3"
  local reason="$4"
  local savings="$5"

  cat >> "$MEMORY_FILE" << EOF

#### ${date}
- **${subscription}**: ${decision}
  - Reason: ${reason}
  - Annual savings: \$${savings}
EOF
}

# Example: User decided to cancel a subscription
add_decision "2026-01-19" "Crunch Gym" "cancel" "Keeping Chelsea Piers instead" "1053"
```

### Adding to Watchlist

```bash
add_to_watchlist() {
  local payee="$1"
  local reason="$2"
  local review_date=$(date -v+30d +%Y-%m-%d)

  # This would need more sophisticated YAML editing
  # For now, prompt user to manually add:
  echo "Add to watchlist section in MEMORY.md:"
  echo "  - payee: \"${payee}\""
  echo "    added: $(date +%Y-%m-%d)"
  echo "    review_date: ${review_date}"
  echo "    reason: \"${reason}\""
}
```

### Using Memory in Analysis

When analyzing, filter based on preferences:

```bash
# Filter out essential subscriptions from cancellation suggestions
filter_subscriptions() {
  jq --argjson essential "$(echo "$ESSENTIAL_SUBS" | jq -R . | jq -s .)" '
    map(select(.payee as $p | $essential | index($p) | not))
  '
}

# Exclude certain categories from spending totals
filter_transactions() {
  jq --argjson excluded "$(echo "$EXCLUDED_CATS" | jq -R . | jq -s .)" '
    .transactions | map(select(.category_name as $c | $excluded | index($c) | not))
  '
}
```

---

## Workflow

### 0. Interview Mode (Always On)

The skill includes an interactive interview to validate subscription data and make decisions. This is critical because:
- LunchMoney's `transactions_within_range` field is often unreliable
- Users forget what's cancelled vs still active
- Categorization may need user confirmation

**Interview Categories** (ask about each in order):
1. **Fitness** - Gym memberships, fitness apps
2. **Streaming** - Video, music, audiobooks
3. **AI/Dev Tools** - AI subscriptions, hosting, developer tools
4. **Reading/News** - RSS, read-later, newsletters
5. **Productivity** - Software subscriptions
6. **Memberships** - Patreon, donations, co-ops

**Interview Questions Pattern**:
```
Use AskUserQuestion tool with:
- Show actual charges found from 12 months of transactions
- Group by category with totals (monthly/annual)
- Include "Last Charged" date and status indicators (✅/⚠️/🔴/❌)
- Distinguish cancelled (❌) from irregular (🔴 Xd ago)
- Offer actionable choices: Keep all, Cancel all, Review each, etc.
```

**Key Learnings to Apply**:
- **Use 12-month window** to catch annual subscriptions and show real activity
- Always cross-check recurring_items with actual transactions using normalized payee matching
- Show "Last Charged: Dec 2025" not confusing "Missed 3" status
- Price variations are normal (e.g., Starlink $120 → $5) - match by name not amount
- Ask follow-up questions based on responses
- Record all decisions in MEMORY.md

**After Interview**:
- Update MEMORY.md with decisions
- Generate action items list
- Calculate estimated savings
- Set review dates for watchlist items

### 1. Initialize Data Directory

```bash
SKILL_DIR="skills/analyze-spending"
DATA_DIR="${SKILL_DIR}/data"
CACHE_DIR="${DATA_DIR}/cache"
REPORTS_DIR="${DATA_DIR}/reports"
TRANSACTIONS_DIR="${CACHE_DIR}/transactions"

mkdir -p "${CACHE_DIR}" "${REPORTS_DIR}" "${TRANSACTIONS_DIR}"

# Initialize MEMORY.md if needed
MEMORY_FILE="${DATA_DIR}/MEMORY.md"
if [ ! -f "$MEMORY_FILE" ]; then
  cp "${SKILL_DIR}/assets/MEMORY.md" "$MEMORY_FILE"
fi
```

### 2. Retrieve API Key

```bash
LUNCHMONEY_API_KEY=$(op item get "Lunchmoney" --fields "API Key" --reveal)
```

### 3. Check Cache Validity

Before fetching, check if cached data is still fresh:

```bash
CACHE_META="${CACHE_DIR}/cache_meta.json"

# Initialize cache meta if it doesn't exist
if [ ! -f "$CACHE_META" ]; then
  echo '{}' > "$CACHE_META"
fi

# Check if cache is fresh (returns "true" or "false")
is_cache_fresh() {
  local cache_key="$1"
  local max_age_hours="$2"

  local last_fetch=$(jq -r ".${cache_key} // 0" "$CACHE_META")
  local now=$(date +%s)
  local age_hours=$(( (now - last_fetch) / 3600 ))

  [ "$age_hours" -lt "$max_age_hours" ] && echo "true" || echo "false"
}

# Update cache timestamp
update_cache_meta() {
  local cache_key="$1"
  local now=$(date +%s)
  local tmp=$(mktemp)
  jq ".${cache_key} = ${now}" "$CACHE_META" > "$tmp" && mv "$tmp" "$CACHE_META"
}
```

**Cache freshness thresholds:**
| Data Type | Max Age | Rationale |
|-----------|---------|-----------|
| user | 168 hours (7 days) | Rarely changes |
| categories | 168 hours (7 days) | Rarely changes |
| recurring_items | 24 hours | May change daily |
| transactions (current month) | 4 hours | Active updates |
| transactions (past months) | 168 hours | Historical, stable |

### 4. Fetch and Cache User Info

```bash
USER_CACHE="${CACHE_DIR}/user.json"

if [ "$(is_cache_fresh user 168)" = "false" ] || [ ! -f "$USER_CACHE" ]; then
  curl -s "https://dev.lunchmoney.app/v1/me" \
    -H "Authorization: Bearer ${LUNCHMONEY_API_KEY}" \
    > "$USER_CACHE"
  update_cache_meta "user"
  echo "Fetched fresh user data"
else
  echo "Using cached user data"
fi
```

### 5. Fetch and Cache Categories

```bash
CATEGORIES_CACHE="${CACHE_DIR}/categories.json"

if [ "$(is_cache_fresh categories 168)" = "false" ] || [ ! -f "$CATEGORIES_CACHE" ]; then
  curl -s "https://dev.lunchmoney.app/v1/categories" \
    -H "Authorization: Bearer ${LUNCHMONEY_API_KEY}" \
    > "$CATEGORIES_CACHE"
  update_cache_meta "categories"
  echo "Fetched fresh categories"
else
  echo "Using cached categories"
fi
```

### 6. Fetch and Cache Transactions

Transactions are cached per-month to enable efficient incremental updates:

```bash
fetch_transactions_for_month() {
  local year_month="$1"  # Format: YYYY-MM
  local start_date="${year_month}-01"
  local end_date=$(date -j -f "%Y-%m-%d" "${start_date}" -v+1m -v-1d +%Y-%m-%d 2>/dev/null || \
                   date -d "${start_date} +1 month -1 day" +%Y-%m-%d)

  local cache_file="${TRANSACTIONS_DIR}/${year_month}.json"
  local cache_key="transactions_${year_month//-/_}"

  # Current month: refresh every 4 hours; past months: refresh weekly
  local current_month=$(date +%Y-%m)
  local max_age=168
  [ "$year_month" = "$current_month" ] && max_age=4

  if [ "$(is_cache_fresh $cache_key $max_age)" = "false" ] || [ ! -f "$cache_file" ]; then
    curl -s "https://dev.lunchmoney.app/v1/transactions?start_date=${start_date}&end_date=${end_date}&debit_as_negative=true&limit=1000" \
      -H "Authorization: Bearer ${LUNCHMONEY_API_KEY}" \
      > "$cache_file"
    update_cache_meta "$cache_key"
    echo "Fetched transactions for ${year_month}"
  else
    echo "Using cached transactions for ${year_month}"
  fi
}

# Fetch for a date range (fetches all months in range)
START_DATE="2025-12-01"
END_DATE="2026-01-31"

# Generate list of months in range and fetch each
current="$START_DATE"
while [ "$current" \< "$END_DATE" ] || [ "$current" = "$END_DATE" ]; do
  month=$(echo "$current" | cut -d- -f1-2)
  fetch_transactions_for_month "$month"
  current=$(date -j -f "%Y-%m-%d" "${month}-01" -v+1m +%Y-%m-%d 2>/dev/null || \
            date -d "${month}-01 +1 month" +%Y-%m-%d)
done
```

### 7. Fetch and Cache Recurring Items

```bash
RECURRING_CACHE="${CACHE_DIR}/recurring_items.json"
START_DATE=$(date -v-60d +%Y-%m-%d)  # 60 days back for context
END_DATE=$(date +%Y-%m-%d)

if [ "$(is_cache_fresh recurring 24)" = "false" ] || [ ! -f "$RECURRING_CACHE" ]; then
  curl -s "https://dev.lunchmoney.app/v1/recurring_items?start_date=${START_DATE}&end_date=${END_DATE}&debit_as_negative=true" \
    -H "Authorization: Bearer ${LUNCHMONEY_API_KEY}" \
    > "$RECURRING_CACHE"
  update_cache_meta "recurring"
  echo "Fetched fresh recurring items"
else
  echo "Using cached recurring items"
fi
```

### 8. Load Cached Data for Analysis

```bash
# Read from cache files
USER_DATA=$(cat "$USER_CACHE")
CATEGORIES=$(cat "$CATEGORIES_CACHE")
RECURRING=$(cat "$RECURRING_CACHE")

# Merge transaction files for date range
TRANSACTIONS=$(jq -s '
  map(.transactions // []) |
  add |
  sort_by(.date) |
  reverse
' ${TRANSACTIONS_DIR}/*.json)
```

---

## Report Generation

### Generate Spending Overview Report

```bash
REPORT_DATE=$(date +%Y-%m-%d)
REPORT_FILE="${REPORTS_DIR}/${REPORT_DATE}_spending-overview.md"

generate_spending_report() {
  local start_date="$1"
  local end_date="$2"
  local period_name="$3"

  cat > "$REPORT_FILE" << EOF
# Spending Overview: ${period_name}

*Generated: $(date '+%Y-%m-%d %H:%M')*
*Period: ${start_date} to ${end_date}*

## Summary

| Metric | Amount |
|--------|--------|
| Income | \$${TOTAL_INCOME} |
| Expenses | \$${TOTAL_EXPENSES} |
| **Net** | **\$${NET}** |

## Spending by Category

| Category | Amount | % |
|----------|--------|---|
$(echo "$CATEGORY_BREAKDOWN")

## Top Merchants

| Merchant | Amount | # Txns |
|----------|--------|--------|
$(echo "$TOP_MERCHANTS")

---
*Data cached at: $(jq -r '.transactions_2026_01 // "N/A" | tonumber | strftime("%Y-%m-%d %H:%M")' "$CACHE_META" 2>/dev/null || echo "N/A")*
EOF

  echo "Report saved to: $REPORT_FILE"
}
```

### Generate Subscription Audit Report (Template-Based)

The subscription audit uses a fill-in-the-blanks template at `assets/subscription-audit-template.md`. This approach:
- Categorizes subscriptions into meaningful groups
- Provides actionable recommendations at the top
- **Analyzes 12 months of transaction data** (default) for comprehensive coverage
- Cross-references recurring_items with actual transactions
- Shows "Last Charged" date instead of unreliable "Missed N" status
- Detects duplicate services and truly inactive subscriptions

**Template placeholders**: `{{TOTAL_MONTHLY}}`, `{{CAT_STREAMING_ROWS}}`, etc.

**Subscription Categories**:
| Category | Keywords for Matching |
|----------|----------------------|
| 🏠 Housing & Utilities | rent, house fee, loan, verizon, starlink |
| 📺 Streaming | hulu, hbo, prime video, paramount, disney, spotify |
| 💪 Fitness | gym, fitness, crunch |
| 🧠 AI & Learning | chatgpt, jasper, execute program |
| 💻 Developer Tools | github, linode, digitalocean, ngrok |
| 📱 Productivity | obsidian, notion, adobe, zapier |
| 📰 News & Media | substack, readwise, feedbin, newsblur |
| 💾 Storage | backblaze, google storage, icloud |
| 🎁 Memberships | patreon, rei, open source |

**Python-based generation** (avoids jq `!=` escaping issues in bash):

```python
import json
from pathlib import Path

# Load data
with open("data/cache/recurring_items.json") as f:
    items = json.load(f)
with open("assets/subscription-audit-template.md") as f:
    template = f.read()

# Categorize and calculate
active_items = [i for i in items if not i.get("exclude_from_totals", False)]

def annual_cost(item):
    amount = float(item.get("amount", 0) or 0)
    cadence = item.get("cadence", "monthly")
    multipliers = {
        "yearly": 1, "monthly": 12, "weekly": 52,
        "biweekly": 26, "quarterly": 4
    }
    return amount * multipliers.get(cadence, 12)

# Generate recommendations based on:
# - Category overlap (multiple streaming, multiple gyms)
# - Inactive subscriptions (no transactions_within_range)
# - Duplicate payee names

# Fill template placeholders
output = template.replace("{{TOTAL_MONTHLY}}", f"{total:.2f}")
# ... fill all placeholders

Path("data/reports").mkdir(exist_ok=True)
with open(f"data/reports/{date}_subscription-audit.md", "w") as f:
    f.write(output)
```

**Fetch 12 months of data for analysis** (recommended default):

```bash
# Fetch 12 months of transactions for comprehensive analysis
# This catches annual subscriptions and provides accurate "Last Charged" dates
for i in {11..0}; do
  MONTH=$(date -v-${i}m +%Y-%m)
  fetch_transactions_for_month "$MONTH"
done

# Update recurring items with 90-day window (for LunchMoney's own tracking)
START_DATE=$(date -v-90d +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)
curl -s "https://dev.lunchmoney.app/v1/recurring_items?start_date=${START_DATE}&end_date=${END_DATE}" \
  -H "Authorization: Bearer ${LUNCHMONEY_API_KEY}" \
  > "$RECURRING_CACHE"
```

**Why 12 months?**
- Catches annual subscriptions (GitHub, Backblaze, etc.)
- Shows true "Last Charged" date instead of "Missed N"
- Identifies cancelled vs just-irregular subscriptions
- Price changes are visible (e.g., Starlink $120 → $5)

---

## Analysis Using Cached Data

### Find ACTUALLY Active Subscriptions (Cross-Reference Method)

**Important**: Don't rely solely on `recurring_items.transactions_within_range` - it's often empty even when charges exist. Cross-reference with actual transactions using **normalized payee matching**:

```python
import json
import re
from collections import defaultdict
from pathlib import Path

# Payee name normalization - critical for matching variations
def normalize(name):
    """Normalize payee name for matching (case-insensitive, strip suffixes)"""
    if not name:
        return ""
    name = name.lower().strip()
    # Remove common suffixes/prefixes
    name = re.sub(r'\s*(inc\.?|llc|ltd|co\.?|corp\.?|subscription|membership|payment|charge|premium)\s*', ' ', name)
    # Remove special characters
    name = re.sub(r'[^a-z0-9\s]', '', name)
    # Collapse whitespace
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def get_keywords(name):
    """Extract brand keywords for fuzzy matching"""
    # E.g., "STARLINK INTERNET LLC" → ["starlink", "internet"]
    normalized = normalize(name)
    return set(normalized.split())

# Load 12 months of transactions from cache
transactions = []
for month_file in Path("data/cache/transactions").glob("*.json"):
    with open(month_file) as f:
        transactions.extend(json.load(f).get("transactions", []))

# Find transactions matching a recurring item (flexible matching)
def find_transactions_for_payee(target_payee, original_name=None):
    """Match transactions by normalized name or keywords"""
    target_norm = normalize(target_payee)
    target_keywords = get_keywords(target_payee)
    matches = []

    for txn in transactions:
        payee = txn.get("payee", "")
        payee_norm = normalize(payee)

        # 1. Direct normalized match
        if target_norm and target_norm in payee_norm:
            matches.append(txn)
            continue

        # 2. Reverse containment
        if payee_norm and payee_norm in target_norm:
            matches.append(txn)
            continue

        # 3. Keyword overlap (for brand names)
        payee_keywords = get_keywords(payee)
        if target_keywords & payee_keywords:  # Set intersection
            matches.append(txn)
            continue

    return matches

# Build subscription report with "Last Charged" dates
for item in recurring_items:
    payee = item.get("payee", "Unknown")
    txns = find_transactions_for_payee(payee, item.get("original_name"))

    if txns:
        # Sort by date descending
        txns.sort(key=lambda t: t.get("date", ""), reverse=True)
        last_charge = txns[0].get("date")  # e.g., "2025-12-22"
        charge_count = len(txns)
        monthly_avg = sum(abs(float(t.get("amount", 0))) for t in txns) / 12
        print(f"{payee}: ${monthly_avg:.2f}/mo | Last: {last_charge} | {charge_count} charges")
    else:
        print(f"{payee}: ❌ No charges found in 12 months (likely cancelled)")
```

**Key matching strategies**:
1. **Name normalization**: "STARLINK INTERNET LLC" → "starlink internet"
2. **Keyword extraction**: Matches "starlink" even if merchant name varies
3. **Price-agnostic**: Same vendor, different amounts still match
4. **Bidirectional containment**: "HBO Max" matches "HBO MAX SUBSCRIPTION"

**Status indicators** (in reports):
- **✅ Active**: Last charged within 45 days
- **⚠️ Stale**: Last charge 45-90 days ago
- **🔴 Xd ago**: Shows days since last charge (e.g., "🔴 136d ago")
- **❌ Cancelled**: No charges found in 12 months

### Analyze Spending by Category

```bash
jq -r '
  .transactions |
  group_by(.category_name) |
  map({
    category: (.[0].category_name // "Uncategorized"),
    total: (map(.amount | tonumber | if . < 0 then . * -1 else 0 end) | add),
    count: length
  }) |
  sort_by(-.total) |
  .[:15]
' "${TRANSACTIONS_DIR}/2026-01.json"
```

### Calculate Income vs Expenses

```bash
jq -r '
  .transactions |
  [
    (map(select(.amount | tonumber | . < 0) | .amount | tonumber | . * -1) | add),
    (map(select(.amount | tonumber | . > 0) | .amount | tonumber) | add)
  ] |
  {expenses: .[0], income: .[1], net: (.[1] - .[0])}
' "${TRANSACTIONS_DIR}/2026-01.json"
```

### Find Top Merchants

```bash
jq -r '
  .transactions |
  map(select(.amount | tonumber | . < 0)) |
  group_by(.payee) |
  map({
    payee: .[0].payee,
    total: (map(.amount | tonumber | . * -1) | add),
    count: length
  }) |
  sort_by(-.total) |
  .[:10]
' "${TRANSACTIONS_DIR}/2026-01.json"
```

### Subscription Annual Cost Analysis

```bash
jq '
  def annual_cost(amount; cadence):
    if cadence == "weekly" then amount * 52
    elif cadence == "biweekly" then amount * 26
    elif cadence == "twice a month" then amount * 24
    elif cadence == "monthly" then amount * 12
    elif cadence == "every 3 months" then amount * 4
    elif cadence == "every 4 months" then amount * 3
    elif cadence == "twice a year" then amount * 2
    elif cadence == "yearly" then amount
    else amount * 12
    end;

  map(select(.exclude_from_totals != true)) |
  {
    total_monthly: (map(if .cadence == "monthly" then (.amount | tonumber) else 0 end) | add),
    total_annual: (map(annual_cost((.amount | tonumber); .cadence)) | add),
    count: length
  }
' "$RECURRING_CACHE"
```

---

## Force Refresh Cache

To force a fresh fetch of all data:

```bash
# Clear all cache
rm -rf "${CACHE_DIR}"/*
echo '{}' > "${CACHE_DIR}/cache_meta.json"
mkdir -p "${TRANSACTIONS_DIR}"

# Or clear specific cache
rm "${CACHE_DIR}/recurring_items.json"
jq 'del(.recurring)' "$CACHE_META" > tmp && mv tmp "$CACHE_META"
```

---

## Viewing Past Reports

```bash
# List all generated reports
ls -la "${REPORTS_DIR}"

# View most recent spending report
cat "${REPORTS_DIR}/$(ls -t ${REPORTS_DIR}/*spending* | head -1)"

# View most recent subscription audit
cat "${REPORTS_DIR}/$(ls -t ${REPORTS_DIR}/*subscription* | head -1)"
```

---

## Cadence Calculation

Convert LunchMoney cadence to annual cost:

| Cadence | Multiplier |
|---------|------------|
| weekly | × 52 |
| biweekly | × 26 |
| twice a month | × 24 |
| monthly | × 12 |
| every 3 months | × 4 |
| every 4 months | × 3 |
| twice a year | × 2 |
| yearly | × 1 |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired API key | Generate new key at lunchmoney.app/developers |
| 404 Not Found | Invalid endpoint | Check API URL |
| Empty transactions | No data for period | Verify date range has transactions |
| 1Password error | Item not found | Ensure "Lunchmoney" item exists with "API Key" field |
| Stale cache | Data not refreshing | Check cache_meta.json timestamps, force refresh if needed |

---

## API Reference

- **Base URL**: `https://dev.lunchmoney.app/v1`
- **Authentication**: Bearer token in Authorization header
- **Documentation**: https://lunchmoney.dev/
- **Rate Limits**: Standard API rate limits apply

---

## Example Session

```
User: /analyze-spending

Claude: I'll analyze your spending. Let me check the cache and cross-reference
actual transactions (12-month window for comprehensive coverage)...

[Fetching 12 months of transactions: Feb 2025 - Jan 2026]
[Cross-referencing recurring_items with actual transaction data]
[Using normalized payee matching for accuracy]

Found 34 subscriptions with charges in the past year. Starting interview...

─────────────────────────────────────────────
📺 STREAMING & ENTERTAINMENT
   Active Monthly: $85.93 | Annual: $1,031.17

| Service      | Monthly | Last Charged | Status    |
|--------------|---------|--------------|-----------|
| HBO Max      | $15.82  | 2025-12-27   | ✅ Active |
| Paramount+   | $8.66   | 2025-12-24   | ✅ Active |
| Crunchyroll  | $5.33   | 2025-12-26   | ✅ Active |
| Hulu         | $3.16   | 2025-12-25   | ✅ Active |
| Audible      | $11.21  | 2026-01-04   | ✅ Active |
| Spotify      | $9.99   | Never (12mo) | ❌ Cancelled |
| Disney+      | $7.99   | Never (12mo) | ❌ Cancelled |

Which do you want to keep?
[ ] Keep 2-3 favorites
[ ] Rotate quarterly
[x] Cancel all

User: Cancel all
─────────────────────────────────────────────

─────────────────────────────────────────────
💻 DEVELOPER TOOLS & HOSTING
   Active Monthly: $48.54 | Annual: $582.43

| Service             | Monthly | Last Charged | Status      |
|---------------------|---------|--------------|-------------|
| GitHub              | $15.33  | 2025-09-05   | 🔴 136d ago |
| Google Cloud Storage| $14.61  | 2026-01-07   | ✅ Active   |
| Ngrok               | $10.50  | 2026-01-19   | ✅ Active   |
| DigitalOcean        | $8.10   | 2025-12-31   | ✅ Active   |

User: Cancel DO and Ngrok
─────────────────────────────────────────────

[Continues through all categories...]

## Summary of Decisions

| Action | Services | Monthly Savings |
|--------|----------|-----------------|
| Cancel | Streaming (5 active) | $44 |
| Cancel | Dev tools (2 services) | $19 |
| Cancel | Productivity (4 services) | $80 |
| Downgrade | Claude.ai ($218→$100) | $118 |
| **Total** | | **$261/mo ($3,132/yr)** |

Action items saved to: data/MEMORY.md
Report saved to: data/reports/2026-01-19_subscription-audit-12mo.md

Next steps:
- [ ] Cancel streaming services (HBO, Paramount+, Crunchyroll, Hulu, Audible)
- [ ] Cancel DigitalOcean and Ngrok
- [ ] Downgrade Claude.ai to $100 tier
- [ ] Review Patreon creators by 2026-02-01
```

---

## Notes

- All amounts are in the user's primary currency unless specified
- Debit transactions should be treated as negative (expenses)
- Credit transactions are positive (income/refunds)
- **Don't trust `recurring_items.transactions_within_range`** - always cross-reference with actual transactions
- **Default analysis window is 12 months** to catch annual subscriptions and show accurate "Last Charged" dates
- The API returns a maximum of 1000 transactions per request; use pagination for larger date ranges
- Cache is stored in `data/` which should be gitignored
- Reports are timestamped for historical comparison

### Status Legend (in reports)

| Status | Meaning |
|--------|---------|
| ✅ Active | Last charged within 45 days |
| ⚠️ Stale | Last charge 45-90 days ago (may be cancelled or annual) |
| 🔴 Xd ago | Shows days since last charge (e.g., "🔴 136d ago" for GitHub) |
| ❌ Cancelled | No charges found in 12 months |

### Payee Matching Notes

- Names are normalized: "STARLINK INTERNET LLC" → "starlink internet"
- Matching is price-agnostic (same vendor, different amounts still match)
- Keyword extraction catches brand name variations
- Apple charges are mixed (TV, iCloud, App Store) - hard to separate by merchant name alone
