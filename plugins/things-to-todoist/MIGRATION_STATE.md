# Things to Todoist Migration State

**Last updated:** 2026-01-04 15:40 EST

## Summary

Migration from Things 3 for Mac to Todoist is ~80% complete. Hit API rate limits on remaining tasks.

**SKILL.md updated to use Todoist MCP** - the MCP provides cleaner batching via `mcp__todoist__add-tasks`.

## What Was Accomplished

| Step | Status | Details |
|------|--------|---------|
| Export Things data | Done | 645 todos, 13 projects, 3 areas, 36 with checklists |
| Export Todoist data | Done | Pre-migration: 273 tasks, 15 projects |
| Analyze conflicts | Done | 44 exact dupes, 5 fuzzy matches identified |
| Create new projects | Done | Created "Career" and "Finances" in Todoist |
| Import tasks | Partial | 352 created, 206 checklist items added |
| Move misplaced tasks | Done | 6 tasks moved from Inbox to correct projects |

## Current Todoist State

- **927 tasks** total (was 273 before migration)
- **17 projects** (added Career, Finances)

## What's Left

### ~145 tasks failed due to rate limiting

These are mostly Work tasks. The Todoist API allows ~450 requests per 15 minutes.

**To retry:** Run this rate-limit-safe script:

```bash
cd /tmp && python3 -u << 'EOF'
import json
import time
import sys
from todoist_api_python.api import TodoistAPI
from itertools import chain

# === CONFIGURATION ===
API_TOKEN = "YOUR_TOKEN_HERE"  # Get from 1Password or user
DELAY_BETWEEN_REQUESTS = 2.5   # Seconds between API calls (safe: 30 req/min)
BATCH_SIZE = 25                # Pause after this many tasks
BATCH_PAUSE = 30               # Seconds to pause between batches

api = TodoistAPI(API_TOKEN)

print("Loading data...", flush=True)

# Load remaining tasks
with open('remaining_tasks.json', 'r') as f:
    data = json.load(f)
titles = data['titles']

with open('things_export_v2.json', 'r') as f:
    things = json.load(f)
lookup = {t.get('title', '').strip(): t for t in things['todos']}

PROJECT_MAP = {
    'Work 💼': 'Work', 'Career 📈': 'Career', 'Professional': 'Career',
    'Networking 🤝': 'Career', 'Finances 💸': 'Finances', 'Ideas': 'Projects',
    'Growth 🌱': 'Personal Growth', 'Love 💘': 'Love',
    'Organization and systems 🗂️': 'Organization + Systems', 'Maine 🌲': 'Maine',
    'Home and style 💅': 'Style', 'Projects + Fun 🕺': 'Fun',
    'Body and health 💪': 'Health', 'Social (friends and family) 🫶': 'Relationships',
    'Projects wiki reboot': 'Projects', None: 'Inbox',
}

print("Fetching Todoist projects...", flush=True)
projects = {p.name: p.id for p in chain.from_iterable(api.get_projects())}

total = len(titles)
created = 0
errors = []
eta_per_task = DELAY_BETWEEN_REQUESTS + 0.5  # Estimate

print(f"\n{'='*60}", flush=True)
print(f"IMPORTING {total} TASKS (ETA: ~{int(total * eta_per_task / 60)} minutes)", flush=True)
print(f"Rate: 1 request every {DELAY_BETWEEN_REQUESTS}s, batch pause every {BATCH_SIZE} tasks", flush=True)
print(f"{'='*60}\n", flush=True)

for i, title in enumerate(titles):
    todo = lookup.get(title)
    if not todo:
        print(f"⚠️  [{i+1}/{total}] Not found: {title[:40]}", flush=True)
        continue

    proj = todo.get('project_title') or todo.get('area_title')
    target = PROJECT_MAP.get(proj, 'Inbox')
    target_id = projects.get(target, projects.get('Inbox'))

    # Exponential backoff on failure
    for attempt in range(3):
        try:
            notes = todo.get('notes', '')
            desc = notes if isinstance(notes, str) else ''
            api.add_task(content=title, project_id=target_id,
                        description=desc[:16000] if desc else None)
            created += 1
            remaining = total - i - 1
            eta_mins = int(remaining * eta_per_task / 60)
            print(f"✅ [{i+1}/{total}] {title[:45]} → {target} (ETA: {eta_mins}m)", flush=True)
            break
        except Exception as e:
            if '403' in str(e) and attempt < 2:
                wait = 30 * (attempt + 1)  # 30s, then 60s
                print(f"⏳ Rate limited, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                errors.append(title)
                print(f"❌ [{i+1}/{total}] {title[:40]}: {str(e)[:30]}", flush=True)
                break

    # Rate limiting delay
    time.sleep(DELAY_BETWEEN_REQUESTS)

    # Batch pause
    if (i + 1) % BATCH_SIZE == 0 and i + 1 < total:
        print(f"\n⏸️  Batch pause ({BATCH_PAUSE}s) - {created} created so far\n", flush=True)
        time.sleep(BATCH_PAUSE)

print(f"\n{'='*60}", flush=True)
print(f"COMPLETE: {created}/{total} created, {len(errors)} errors", flush=True)
print(f"{'='*60}", flush=True)

if errors:
    print(f"\nFailed tasks saved to /tmp/still_remaining.json", flush=True)
    with open('still_remaining.json', 'w') as f:
        json.dump({'count': len(errors), 'titles': errors}, f, indent=2)
EOF
```

**Estimated time:** ~6-8 minutes for 145 tasks (safe rate limiting)

### ~54 tasks need to be moved to correct projects

These were created in the first migration before project mapping was added. They're in Inbox but should be elsewhere.

**To fix:** The move script ran but only found 6 that matched Things titles. The rest may have been from original Todoist or have slightly different titles.

## Files in /tmp/

| File | Purpose |
|------|---------|
| `things_export.json` | Original export (incomplete) |
| `things_export_v2.json` | Full export with project_title and checklist |
| `todoist_export.json` | Pre-migration Todoist backup |
| `merge_report.json` | Conflict analysis results |
| `fix_migration_stats.json` | Stats from main migration run |
| `move_stats.json` | Stats from move operation |
| `remaining_tasks.json` | 145 task titles that need importing |
| `tasks_for_mcp.json` | Tasks grouped by project for MCP import |

## Project Mapping Used

| Things Project/Area | Todoist Project |
|---------------------|-----------------|
| Work 💼 | Work |
| Career 📈 | Career |
| Professional | Career |
| Networking 🤝 | Career |
| Finances 💸 | Finances |
| Ideas | Projects |
| Growth 🌱 | Personal Growth |
| Love 💘 | Love |
| Organization and systems 🗂️ | Organization + Systems |
| Maine 🌲 | Maine |
| Home and style 💅 | Style |
| Projects + Fun 🕺 | Fun |
| Body and health 💪 | Health |
| Social (friends and family) 🫶 | Relationships |
| Projects wiki reboot | Projects |
| (none) | Inbox |

## User Decisions Made

1. **Duplicates:** Update Todoist if Things has more info
2. **Fuzzy matches:**
   - "Archive projecfts wiki" → Update Todoist
   - "IBM.com marketing page generator" → Skip
   - "Fastmail MCP" → Skip
   - "Cursor PM" → Update Todoist
   - "Cancel DigitalOcean" → Skip
3. **Things areas mapping:**
   - "Areas" → Inbox
   - "Projects + Fun 🕺" → Projects
   - "Professional" → Work

## To Fully Complete Migration

### Option 1: Use Todoist MCP (Recommended)

After restarting Claude Code to reconnect the MCP:

```
# 1. Get project IDs
mcp__todoist__find-projects()

# 2. Work project ID: 6CrfHcmv4r99QPGR
#    Inbox project ID: 6CrfHcmv47hgjffx

# 3. Import in batches of 20-30 tasks
mcp__todoist__add-tasks({
  "tasks": [
    {"content": "Task title", "projectId": "6CrfHcmv4r99QPGR", "description": "notes"},
    // ...
  ]
})
```

The task data is prepared in `/tmp/tasks_for_mcp.json` with 135 Work tasks and 10 Inbox tasks.

### Option 2: Python script with rate limiting

1. Wait 5-10 minutes for rate limit to reset
2. Run the retry script above with valid API token
3. Optionally: Review Inbox tasks and move any that belong elsewhere
4. Delete `/tmp/` files when satisfied

## Skill Location

The migration skill is at:
`$PLUGIN_ROOT/skills/migrate/SKILL.md`
