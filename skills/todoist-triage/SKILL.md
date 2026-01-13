---
name: todoist-triage
description: Triage and clean up Todoist with duplicate detection, stale task cleanup,
  and ADHD-friendly coaching. Use when the user asks to triage, organize, or clean
  up their Todoist inbox or tasks.
---

# Todoist Triage

Interactive triage and cleanup for your Todoist task list, designed with **Executive Function (EF) and ADHD support** in mind. Syncs data to a local SQLite database for efficient analysis, detects issues, suggests improvements, and coaches you toward better task management habits.

## Philosophy: EF and ADHD-Friendly Design

This skill acts as an **Executive Function coach**, not just a task cleaner. It's built around principles that help people who struggle with:

- **Task initiation**: Identifies "quick wins" (2-5 min tasks) to build momentum
- **Task sizing**: Breaks down overwhelming tasks into concrete next actions
- **Clarity**: Ensures tasks are SMART (Specific, Measurable, Attainable, Relevant, Timebound)
- **Decision fatigue**: Batches similar decisions, offers smart defaults
- **Motivation**: Celebrates progress, suggests dopamine-friendly task ordering
- **Overwhelm**: Never shows everything at once; works in focused chunks

**Core Principles:**
1. **One thing at a time** - Each question focuses on one decision
2. **Momentum first** - Start sessions by identifying quick wins
3. **Break it down** - Large vague tasks become concrete action steps
4. **Raise the bar gently** - Suggest improvements without judgment
5. **Learn patterns** - Remember what works for you specifically

## Trigger Phrases

- `/todoist-triage`
- "triage my todoist"
- "clean up my todoist"
- "find duplicate tasks in todoist"
- "organize my todoist inbox"
- "help me get unstuck" (EF-focused mode)
- "what can I do right now" (quick wins mode)

## Prerequisites

- **Todoist MCP**: Must be configured for write operations
- **1Password CLI**: API token stored in item "Todoist", field "API Token"
- **Python 3**: With `thefuzz` library for fuzzy matching (`uv pip install thefuzz`)

## Overview

This skill operates in 5 phases:

1. **SYNC** - Fetch data from Todoist Sync API into local SQLite
2. **ANALYZE** - Detect issues: duplicates, stale tasks, sizing problems, SMART gaps
3. **TRIAGE** - Interactive decision-making with EF-friendly coaching
4. **CONFIRM** - Review summary of all planned changes
5. **APPLY** - Execute changes via MCP tools, update memory

## File Locations

```
skills/todoist-triage/
├── SKILL.md                   # This file
├── assets/
│   └── TRIAGE_MEMORY.md       # Template for user preferences
└── data/                      # Runtime data (gitignored)
    ├── todoist.db             # SQLite database
    └── sync_state.json        # Sync token and timestamps
```

---

## Phase 1: SYNC

### Step 1.1: Initialize Database

Create the SQLite database if it doesn't exist:

```bash
DB_PATH="skills/todoist-triage/data/todoist.db"
mkdir -p "skills/todoist-triage/data"

sqlite3 "$DB_PATH" << 'EOF'
CREATE TABLE IF NOT EXISTS sync_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    sync_token TEXT NOT NULL DEFAULT '*',
    last_full_sync DATETIME,
    last_incremental_sync DATETIME
);
INSERT OR IGNORE INTO sync_state (id, sync_token) VALUES (1, '*');

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT,
    is_inbox BOOLEAN DEFAULT 0,
    is_archived BOOLEAN DEFAULT 0,
    synced_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    description TEXT,
    project_id TEXT,
    section_id TEXT,
    parent_id TEXT,
    labels TEXT,
    priority INTEGER DEFAULT 1,
    due_date TEXT,
    is_completed BOOLEAN DEFAULT 0,
    added_at DATETIME,
    content_normalized TEXT,
    content_hash TEXT,
    synced_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS triage_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    finding_type TEXT NOT NULL,
    item_id TEXT,
    related_item_id TEXT,
    similarity_score REAL,
    details TEXT,
    suggested_action TEXT,
    user_decision TEXT,
    decided_at DATETIME,
    applied_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_items_content_hash ON items(content_hash);
CREATE INDEX IF NOT EXISTS idx_items_added ON items(added_at);
CREATE INDEX IF NOT EXISTS idx_findings_session ON triage_findings(session_id);
EOF
```

### Step 1.2: Fetch Todoist API Token

```bash
TODOIST_TOKEN=$(op item get "Todoist" --fields "API Token" --reveal)
```

### Step 1.3: Call Todoist Sync API

```bash
SYNC_TOKEN=$(sqlite3 "$DB_PATH" "SELECT sync_token FROM sync_state WHERE id = 1;")

RESPONSE=$(curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -d "sync_token=$SYNC_TOKEN" \
  -d 'resource_types=["all"]')

echo "$RESPONSE" > "skills/todoist-triage/data/sync_response.json"
```

---

## Phase 2: ANALYZE

### Detect Exact Duplicates

```sql
SELECT i1.id, i2.id, i1.content
FROM items i1
JOIN items i2 ON i1.content_hash = i2.content_hash AND i1.id < i2.id
WHERE i1.is_completed = 0 AND i2.is_completed = 0;
```

### Detect Fuzzy Duplicates

Use Python with thefuzz for similarity detection (threshold: 80%):

```python
from thefuzz import fuzz

for t1 in tasks:
    for t2 in tasks:
        score = fuzz.ratio(t1['content'].lower(), t2['content'].lower())
        if score >= 80:
            # Found fuzzy duplicate
```

### Detect Stale Tasks

- No due date + age > 60 days
- Overdue > 14 days
- In Inbox > 7 days

```sql
SELECT * FROM items
WHERE is_completed = 0
  AND due_date IS NULL
  AND julianday('now') - julianday(added_at) > 60;
```

### Task Sizing Analysis

Identify tasks that need breakdown:
- Vague verbs: plan, organize, figure out, deal with
- Multiple "and"s in task name
- Very long task names (>12 words)

Quick wins:
- Specific verbs: call, email, buy, schedule
- Short task names (<6 words)

---

## Phase 3: TRIAGE (Interactive)

### Present Summary

```
AskUserQuestion(
  questions=[{
    "question": "Analysis complete! Found:\n* Q quick wins\n* X duplicates\n* Z stale tasks\n\nWhat to tackle?",
    "header": "Summary",
    "options": [
      {"label": "Quick wins", "description": "Build momentum"},
      {"label": "Duplicates", "description": "Clean up duplicates"},
      {"label": "Stale tasks", "description": "Review old tasks"},
      {"label": "Full triage", "description": "All categories"}
    ]
  }]
)
```

### Handle Duplicates

```
AskUserQuestion(
  questions=[{
    "question": "Found X tasks with identical content. How to handle?",
    "header": "Duplicates",
    "options": [
      {"label": "Keep newest", "description": "Delete older duplicates"},
      {"label": "Keep oldest", "description": "Delete newer duplicates"},
      {"label": "Review each", "description": "Manual decision"}
    ]
  }]
)
```

### Quick Wins (Momentum Building)

```
AskUserQuestion(
  questions=[{
    "question": "Here are 5 tasks you could finish in 15 minutes:\n1. Call dentist\n2. Reply to email\n3. Order supplies\n\nKnock some out now?",
    "header": "Quick Wins",
    "options": [
      {"label": "Show all", "description": "See full list"},
      {"label": "Batch by type", "description": "Group calls, emails"},
      {"label": "Start with #1", "description": "Let's do it"},
      {"label": "Skip", "description": "Move to other triage"}
    ]
  }]
)
```

### Large Task Breakdown

```
AskUserQuestion(
  questions=[{
    "question": "'Plan vacation to Japan'\n\nThis looks like a project. What's the VERY NEXT physical action?",
    "header": "Break Down",
    "options": [
      {"label": "Research flights", "description": "Search dates/prices"},
      {"label": "Pick dates", "description": "Check calendar"},
      {"label": "Ask travel buddy", "description": "Coordinate"},
      {"label": "Help me think", "description": "Walk through it"}
    ]
  }]
)
```

---

## Phase 4: CONFIRM

```
AskUserQuestion(
  questions=[{
    "question": "Ready to apply:\n* Delete: 8 duplicates\n* Complete: 3 stale\n* Update: 6 with due dates\n\nProceed?",
    "header": "Confirm",
    "options": [
      {"label": "Apply all", "description": "Execute changes"},
      {"label": "Dry run", "description": "Show what would happen"},
      {"label": "Review again", "description": "Go back"},
      {"label": "Cancel", "description": "Discard all"}
    ]
  }]
)
```

---

## Phase 5: APPLY

### Execute via MCP

```
# Complete tasks
mcp__todoist__complete-tasks(ids: ["id1", "id2", ...])

# Update tasks
mcp__todoist__update-tasks(tasks: [
  {id: "x", dueString: "tomorrow"},
  {id: "y", projectId: "new_project"}
])

# Create projects
mcp__todoist__add-projects(projects: [{name: "New Project"}])
```

### Update TRIAGE_MEMORY.md

Record session results and learned patterns:

```markdown
### Session 20260113_143022

**Changes applied:**
- Deleted 8 duplicates
- Completed 3 stale tasks
- Updated 6 tasks with due dates

**Patterns learned:**
- Tasks mentioning 'Sarah' -> Work project
- Tasks starting with 'Call' -> Add @phone label
```

---

## Configuration (TRIAGE_MEMORY.md)

Copy `assets/TRIAGE_MEMORY.md` to `data/TRIAGE_MEMORY.md` and customize:

```yaml
stale_thresholds:
  no_due_date_days: 60
  overdue_days: 14
  inbox_days: 7

excluded_projects:
  - "Someday/Maybe"
  - "Reference"

duplicate_default: "keep_newest"
similarity_threshold: 80
```

---

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| 1Password 401 | Session expired | Run `op signin` |
| Todoist API 401 | Token invalid | Check 1Password item |
| Todoist API 429 | Rate limit | Wait 60s, retry |
| MCP 403 | Project limit (300) | Suggest sub-project |

---

## Tools Used

- **Bash**: Database init, API calls
- **Python**: Fuzzy matching, analysis
- **SQLite**: Local data storage
- **AskUserQuestion**: Interactive decisions
- **mcp__todoist__***: Task operations
