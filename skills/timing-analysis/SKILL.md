---
name: timing-analysis
description: Analyze time tracking data from Timing App. Use when the user asks about how they spent their time, wants a time report, or mentions Timing app data for periods like "today", "yesterday", "this week", "last week", "this month", or custom date ranges.
---

# Timing App Time Analysis

Analyze how you spent your time using data from the Timing App.

## Trigger Phrases

- "How did I spend my time today/yesterday/this week?"
- "Show me my Timing report for [period]"
- "What projects did I work on [period]?"
- "Time analysis for [date range]"
- "How much time did I spend on [project]?"

## Prerequisites

1. **Timing App Account**: Active Timing App subscription with web access
2. **API Token**: Generate at https://web.timingapp.com/integrations under "API & Integrations"
3. **1Password Storage**: Store the API token in 1Password:
   - Item name: `Timingapp`
   - Field: `API Key`

## Workflow

### 1. Retrieve API Token

```bash
# Get API token from 1Password
op item get "Timingapp" --fields "API Key" --reveal
```

### 2. Calculate Date Range

Convert natural language periods to ISO 8601 dates:

| Period | start_date_min | start_date_max |
|--------|----------------|----------------|
| today | Current date | Current date |
| yesterday | Current date - 1 day | Current date - 1 day |
| this week | Monday of current week | Current date |
| last week | Monday of previous week | Sunday of previous week |
| this month | 1st of current month | Current date |
| last month | 1st of previous month | Last day of previous month |
| past 7 days | Current date - 6 days | Current date |
| past 30 days | Current date - 29 days | Current date |

Use `date` command for calculations:
```bash
# Today
date +%Y-%m-%d

# Yesterday
date -v-1d +%Y-%m-%d

# Monday of this week (macOS)
date -v-monday +%Y-%m-%d

# First of this month
date +%Y-%m-01
```

### 3. Fetch Time Report (Aggregated by Project)

```bash
API_TOKEN="<token>"
START_DATE="2024-01-01"
END_DATE="2024-01-07"

curl -s "https://web.timingapp.com/api/v1/report?start_date_min=${START_DATE}&start_date_max=${END_DATE}&columns[]=project&project_grouping_level=1" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Accept: application/json"
```

**Key Parameters:**
- `project_grouping_level=1`: Group by top-level projects
- `project_grouping_level=2`: Include one level of sub-projects
- `columns[]=project`: Include project information
- `columns[]=title`: Include entry titles (for detailed breakdown)
- `timespan_grouping_mode=day`: Group by day (options: exact, day, week, month, year)

### 4. Fetch Detailed Time Entries (Optional)

For more detail on specific entries:

```bash
curl -s "https://web.timingapp.com/api/v1/time-entries?start_date_min=${START_DATE}&start_date_max=${END_DATE}" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Accept: application/json"
```

### 5. Fetch Project Hierarchy (Optional)

To understand project structure:

```bash
curl -s "https://web.timingapp.com/api/v1/projects/hierarchy" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Accept: application/json"
```

### 6. Format and Present Results

Present the analysis with:

1. **Summary Statistics**
   - Total time tracked
   - Number of distinct projects
   - Average daily hours (if multi-day period)

2. **Time by Project** (sorted by duration)
   - Project name
   - Duration (hours:minutes)
   - Percentage of total

3. **Daily Breakdown** (if multi-day period)
   - Date
   - Total hours
   - Top project(s)

4. **Insights**
   - Busiest day
   - Most-worked project
   - Comparison to typical workday (8 hours)

### Example Output Format

```
## Time Analysis: January 1-7, 2024

### Summary
- **Total Time Tracked**: 42h 15m
- **Daily Average**: 6h 2m
- **Projects Worked**: 5

### Time by Project

| Project | Duration | % of Total |
|---------|----------|------------|
| Client Work | 18h 30m | 43.8% |
| Internal | 12h 45m | 30.2% |
| Learning | 6h 00m | 14.2% |
| Admin | 3h 30m | 8.3% |
| Other | 1h 30m | 3.5% |

### Daily Breakdown

| Day | Hours | Top Project |
|-----|-------|-------------|
| Mon | 8h 15m | Client Work |
| Tue | 7h 30m | Internal |
| Wed | 6h 45m | Client Work |
| Thu | 8h 00m | Client Work |
| Fri | 5h 45m | Learning |
| Sat | 3h 00m | Learning |
| Sun | 3h 00m | Internal |

### Insights
- Busiest day: Monday (8h 15m)
- Most time on: Client Work (43.8%)
- 3 days exceeded 8-hour workday
```

## Duration Formatting

The API returns duration in seconds. Convert to human-readable format:

```bash
# Convert seconds to hours:minutes
seconds=15300
hours=$((seconds / 3600))
minutes=$(((seconds % 3600) / 60))
echo "${hours}h ${minutes}m"  # Output: 4h 15m
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired token | Regenerate API token at web.timingapp.com/integrations |
| 404 Not Found | Invalid endpoint | Check API endpoint URL |
| Empty results | No data for period | Verify date range has tracked time |
| 1Password error | Item not found | Ensure "Timingapp" item exists in 1Password |

## API Reference

- **Base URL**: `https://web.timingapp.com/api/v1`
- **Authentication**: Bearer token in Authorization header
- **Documentation**: https://web.timingapp.com/docs/
- **Rate Limits**: Standard API rate limits apply

## Notes

- All times are in the user's configured timezone
- The API returns a maximum of 30 days if no date range is specified
- For team accounts, add `include_team_members=true` to see all team data
- Productivity scores range from -2 (very unproductive) to 2 (very productive)
