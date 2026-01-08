# Todoist Triage

Interactive triage and cleanup for your Todoist task list. Syncs data to a local SQLite database for efficient analysis, detects duplicates and stale tasks, suggests organizational improvements, and learns from your decisions over time.

## Trigger Phrases

- `/todoist-triage`
- "triage my todoist"
- "clean up my todoist"
- "find duplicate tasks in todoist"
- "organize my todoist inbox"

## Prerequisites

- **Todoist MCP**: Must be configured for write operations
- **1Password CLI**: API token stored in item "Todoist", field "API Token"
- **Python 3**: With `thefuzz` library for fuzzy matching (`pip install thefuzz`)

## Overview

This skill operates in 5 phases:

1. **SYNC** - Fetch data from Todoist Sync API into local SQLite
2. **ANALYZE** - Run queries to detect issues (duplicates, stale, missing metadata)
3. **TRIAGE** - Interactive decision-making with AskUserQuestion
4. **CONFIRM** - Review summary of all planned changes
5. **APPLY** - Execute changes via MCP tools, update memory

## File Locations

```
plugins/todoist-triage/
├── TRIAGE_MEMORY.md          # User preferences & session history (git-tracked)
└── data/                      # Runtime data (gitignored)
    ├── todoist.db            # SQLite database
    └── sync_state.json       # Sync token & timestamps
```

---

## Phase 1: SYNC

### Step 1.1: Initialize Database

Create the SQLite database if it doesn't exist:

```bash
PLUGIN_DIR="$PLUGIN_ROOT"
DB_PATH="$PLUGIN_DIR/data/todoist.db"

# Create data directory if needed
mkdir -p "$PLUGIN_DIR/data"

# Initialize database with schema
sqlite3 "$DB_PATH" << 'EOF'
-- Sync state tracking
CREATE TABLE IF NOT EXISTS sync_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    sync_token TEXT NOT NULL DEFAULT '*',
    last_full_sync DATETIME,
    last_incremental_sync DATETIME
);
INSERT OR IGNORE INTO sync_state (id, sync_token) VALUES (1, '*');

-- Projects
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT,
    color TEXT,
    is_inbox BOOLEAN DEFAULT 0,
    is_archived BOOLEAN DEFAULT 0,
    is_favorite BOOLEAN DEFAULT 0,
    view_style TEXT,
    child_order INTEGER,
    synced_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Sections
CREATE TABLE IF NOT EXISTS sections (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    section_order INTEGER,
    synced_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Labels
CREATE TABLE IF NOT EXISTS labels (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    color TEXT,
    is_favorite BOOLEAN DEFAULT 0,
    synced_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Items (tasks)
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    description TEXT,
    project_id TEXT,
    section_id TEXT,
    parent_id TEXT,
    labels TEXT,                          -- JSON array
    priority INTEGER DEFAULT 1,           -- 1=p4, 2=p3, 3=p2, 4=p1
    due_date TEXT,
    due_datetime TEXT,
    due_string TEXT,
    due_is_recurring BOOLEAN DEFAULT 0,
    deadline_date TEXT,
    is_completed BOOLEAN DEFAULT 0,
    completed_at DATETIME,
    added_at DATETIME,
    child_order INTEGER,
    synced_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Computed fields for analysis
    content_normalized TEXT,
    content_hash TEXT
);

-- Completed items archive
CREATE TABLE IF NOT EXISTS completed_items (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    project_id TEXT,
    completed_at DATETIME,
    synced_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Triage findings (per session)
CREATE TABLE IF NOT EXISTS triage_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    finding_type TEXT NOT NULL,           -- duplicate_exact, duplicate_fuzzy, stale, missing_due, inbox_old, etc.
    item_id TEXT,
    related_item_id TEXT,
    similarity_score REAL,
    details TEXT,                         -- JSON
    suggested_action TEXT,
    user_decision TEXT,
    decided_at DATETIME,
    applied_at DATETIME
);

-- Learned rules
CREATE TABLE IF NOT EXISTS triage_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_type TEXT NOT NULL,
    pattern TEXT,
    action TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_applied DATETIME,
    apply_count INTEGER DEFAULT 0
);

-- Indices
CREATE INDEX IF NOT EXISTS idx_items_project ON items(project_id);
CREATE INDEX IF NOT EXISTS idx_items_content_hash ON items(content_hash);
CREATE INDEX IF NOT EXISTS idx_items_added ON items(added_at);
CREATE INDEX IF NOT EXISTS idx_items_due ON items(due_date);
CREATE INDEX IF NOT EXISTS idx_items_completed ON items(is_completed);
CREATE INDEX IF NOT EXISTS idx_findings_session ON triage_findings(session_id);
CREATE INDEX IF NOT EXISTS idx_findings_type ON triage_findings(finding_type);
EOF

echo "Database initialized at $DB_PATH"
```

### Step 1.2: Fetch Todoist API Token

```bash
TODOIST_TOKEN=$(op item get "Todoist" --fields "API Token" --reveal)
```

### Step 1.3: Get Current Sync Token

```bash
SYNC_TOKEN=$(sqlite3 "$DB_PATH" "SELECT sync_token FROM sync_state WHERE id = 1;")
echo "Current sync token: ${SYNC_TOKEN:0:20}..."
```

### Step 1.4: Call Todoist Sync API

```bash
# Fetch all resources (full or incremental based on token)
RESPONSE=$(curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -d "sync_token=$SYNC_TOKEN" \
  -d 'resource_types=["all"]')

# Save response for parsing
echo "$RESPONSE" > "$PLUGIN_DIR/data/sync_response.json"

# Check if full sync
IS_FULL_SYNC=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('full_sync', False))")
echo "Full sync: $IS_FULL_SYNC"

# Extract new sync token
NEW_SYNC_TOKEN=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('sync_token', ''))")
```

### Step 1.5: Parse and Insert Data

Use this Python script to parse the sync response and populate SQLite:

```python
#!/usr/bin/env python3
"""Parse Todoist sync response and populate SQLite database."""

import json
import sqlite3
import hashlib
import re
from pathlib import Path
from datetime import datetime

PLUGIN_DIR = Path("$PLUGIN_ROOT")
DB_PATH = PLUGIN_DIR / "data" / "todoist.db"
SYNC_RESPONSE = PLUGIN_DIR / "data" / "sync_response.json"

def normalize_content(content: str) -> str:
    """Normalize task content for comparison."""
    # Lowercase, remove extra whitespace, strip punctuation
    text = content.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def hash_content(content: str) -> str:
    """Create hash of normalized content."""
    normalized = normalize_content(content)
    return hashlib.md5(normalized.encode()).hexdigest()

def main():
    with open(SYNC_RESPONSE) as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now = datetime.now().isoformat()

    # Update sync token
    new_token = data.get('sync_token', '*')
    is_full = data.get('full_sync', False)

    if is_full:
        cur.execute("""
            UPDATE sync_state SET sync_token = ?, last_full_sync = ? WHERE id = 1
        """, (new_token, now))
    else:
        cur.execute("""
            UPDATE sync_state SET sync_token = ?, last_incremental_sync = ? WHERE id = 1
        """, (new_token, now))

    # Upsert projects
    for proj in data.get('projects', []):
        cur.execute("""
            INSERT OR REPLACE INTO projects
            (id, name, parent_id, color, is_inbox, is_archived, is_favorite, view_style, child_order, synced_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proj['id'], proj['name'], proj.get('parent_id'),
            proj.get('color'), proj.get('inbox_project', False),
            proj.get('is_archived', False), proj.get('is_favorite', False),
            proj.get('view_style'), proj.get('child_order'), now
        ))

    # Upsert sections
    for sec in data.get('sections', []):
        cur.execute("""
            INSERT OR REPLACE INTO sections (id, project_id, name, section_order, synced_at)
            VALUES (?, ?, ?, ?, ?)
        """, (sec['id'], sec['project_id'], sec['name'], sec.get('section_order'), now))

    # Upsert labels
    for label in data.get('labels', []):
        cur.execute("""
            INSERT OR REPLACE INTO labels (id, name, color, is_favorite, synced_at)
            VALUES (?, ?, ?, ?, ?)
        """, (label['id'], label['name'], label.get('color'), label.get('is_favorite', False), now))

    # Upsert items (tasks)
    for item in data.get('items', []):
        due = item.get('due') or {}
        content = item.get('content', '')

        cur.execute("""
            INSERT OR REPLACE INTO items
            (id, content, description, project_id, section_id, parent_id, labels,
             priority, due_date, due_datetime, due_string, due_is_recurring, deadline_date,
             is_completed, added_at, child_order, synced_at, content_normalized, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item['id'], content, item.get('description'),
            item.get('project_id'), item.get('section_id'), item.get('parent_id'),
            json.dumps(item.get('labels', [])),
            item.get('priority', 1),
            due.get('date'), due.get('datetime'), due.get('string'),
            due.get('is_recurring', False),
            item.get('deadline', {}).get('date') if item.get('deadline') else None,
            item.get('checked', False) or item.get('is_completed', False),
            item.get('added_at'), item.get('child_order'), now,
            normalize_content(content), hash_content(content)
        ))

        # Handle deleted items
        if item.get('is_deleted'):
            cur.execute("DELETE FROM items WHERE id = ?", (item['id'],))

    # Handle completed items info
    for completed in data.get('completed_info', []):
        # This contains aggregates, not individual items
        pass

    conn.commit()

    # Print summary
    cur.execute("SELECT COUNT(*) FROM projects WHERE NOT is_archived")
    proj_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM items WHERE NOT is_completed")
    item_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM labels")
    label_count = cur.fetchone()[0]

    print(f"Sync complete: {proj_count} projects, {item_count} active tasks, {label_count} labels")

    conn.close()

if __name__ == "__main__":
    main()
```

Save and run:

```bash
python3 "$PLUGIN_DIR/data/sync_parser.py"
```

---

## Phase 2: ANALYZE

### Step 2.1: Generate Session ID

```bash
SESSION_ID=$(date +%Y%m%d_%H%M%S)
echo "Triage session: $SESSION_ID"
```

### Step 2.2: Detect Exact Duplicates

```sql
-- Find tasks with identical normalized content
INSERT INTO triage_findings (session_id, finding_type, item_id, related_item_id, details, suggested_action)
SELECT
    '{SESSION_ID}' as session_id,
    'duplicate_exact' as finding_type,
    i1.id as item_id,
    i2.id as related_item_id,
    json_object(
        'content', i1.content,
        'project1', p1.name,
        'project2', p2.name,
        'added1', i1.added_at,
        'added2', i2.added_at
    ) as details,
    'delete_older' as suggested_action
FROM items i1
JOIN items i2 ON i1.content_hash = i2.content_hash AND i1.id < i2.id
LEFT JOIN projects p1 ON i1.project_id = p1.id
LEFT JOIN projects p2 ON i2.project_id = p2.id
WHERE i1.is_completed = 0 AND i2.is_completed = 0
  AND i1.parent_id IS NULL AND i2.parent_id IS NULL;  -- Skip subtasks
```

### Step 2.3: Detect Fuzzy Duplicates

Use Python with thefuzz for similarity detection:

```python
#!/usr/bin/env python3
"""Detect fuzzy duplicate tasks using Levenshtein similarity."""

import sqlite3
import json
from pathlib import Path
from thefuzz import fuzz

PLUGIN_DIR = Path("$PLUGIN_ROOT")
DB_PATH = PLUGIN_DIR / "data" / "todoist.db"
SIMILARITY_THRESHOLD = 80  # Minimum similarity percentage

def find_fuzzy_duplicates(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all active non-subtasks
    cur.execute("""
        SELECT i.id, i.content, i.content_normalized, i.project_id, i.added_at,
               p.name as project_name
        FROM items i
        LEFT JOIN projects p ON i.project_id = p.id
        WHERE i.is_completed = 0 AND i.parent_id IS NULL
        ORDER BY i.added_at
    """)
    tasks = cur.fetchall()

    # Compare each pair (skip already found exact duplicates)
    found_pairs = set()
    cur.execute("""
        SELECT item_id, related_item_id FROM triage_findings
        WHERE session_id = ? AND finding_type = 'duplicate_exact'
    """, (session_id,))
    for row in cur.fetchall():
        found_pairs.add((row[0], row[1]))
        found_pairs.add((row[1], row[0]))

    duplicates = []
    for i, t1 in enumerate(tasks):
        for t2 in tasks[i+1:]:
            if (t1['id'], t2['id']) in found_pairs:
                continue

            # Calculate similarity
            ratio = fuzz.ratio(t1['content_normalized'], t2['content_normalized'])
            if ratio >= SIMILARITY_THRESHOLD:
                duplicates.append({
                    'item_id': t1['id'],
                    'related_item_id': t2['id'],
                    'similarity': ratio,
                    'content1': t1['content'],
                    'content2': t2['content'],
                    'project1': t1['project_name'],
                    'project2': t2['project_name']
                })

    # Insert findings
    for dup in duplicates:
        cur.execute("""
            INSERT INTO triage_findings
            (session_id, finding_type, item_id, related_item_id, similarity_score, details, suggested_action)
            VALUES (?, 'duplicate_fuzzy', ?, ?, ?, ?, 'review')
        """, (
            session_id, dup['item_id'], dup['related_item_id'], dup['similarity'],
            json.dumps({
                'content1': dup['content1'],
                'content2': dup['content2'],
                'project1': dup['project1'],
                'project2': dup['project2']
            })
        ))

    conn.commit()
    print(f"Found {len(duplicates)} fuzzy duplicates")
    conn.close()

if __name__ == "__main__":
    import sys
    session_id = sys.argv[1] if len(sys.argv) > 1 else "test"
    find_fuzzy_duplicates(session_id)
```

### Step 2.4: Detect Stale Tasks

Read thresholds from TRIAGE_MEMORY.md, defaulting to:
- No due date + age > 60 days
- Overdue > 14 days
- In Inbox > 7 days

```sql
-- Stale: No due date and older than 60 days
INSERT INTO triage_findings (session_id, finding_type, item_id, details, suggested_action)
SELECT
    '{SESSION_ID}',
    'stale_no_due',
    i.id,
    json_object(
        'content', i.content,
        'project', p.name,
        'added_at', i.added_at,
        'age_days', CAST(julianday('now') - julianday(i.added_at) AS INTEGER)
    ),
    'review'
FROM items i
LEFT JOIN projects p ON i.project_id = p.id
WHERE i.is_completed = 0
  AND i.due_date IS NULL
  AND i.due_is_recurring = 0
  AND julianday('now') - julianday(i.added_at) > 60
  AND i.parent_id IS NULL;

-- Stale: Overdue by more than 14 days
INSERT INTO triage_findings (session_id, finding_type, item_id, details, suggested_action)
SELECT
    '{SESSION_ID}',
    'stale_overdue',
    i.id,
    json_object(
        'content', i.content,
        'project', p.name,
        'due_date', i.due_date,
        'days_overdue', CAST(julianday('now') - julianday(i.due_date) AS INTEGER)
    ),
    'review'
FROM items i
LEFT JOIN projects p ON i.project_id = p.id
WHERE i.is_completed = 0
  AND i.due_date IS NOT NULL
  AND i.due_is_recurring = 0
  AND julianday('now') - julianday(i.due_date) > 14;

-- Stale: In Inbox for more than 7 days
INSERT INTO triage_findings (session_id, finding_type, item_id, details, suggested_action)
SELECT
    '{SESSION_ID}',
    'inbox_old',
    i.id,
    json_object(
        'content', i.content,
        'added_at', i.added_at,
        'age_days', CAST(julianday('now') - julianday(i.added_at) AS INTEGER)
    ),
    'assign_project'
FROM items i
JOIN projects p ON i.project_id = p.id AND p.is_inbox = 1
WHERE i.is_completed = 0
  AND julianday('now') - julianday(i.added_at) > 7;
```

### Step 2.5: Detect Missing Metadata

```sql
-- High priority tasks without due dates
INSERT INTO triage_findings (session_id, finding_type, item_id, details, suggested_action)
SELECT
    '{SESSION_ID}',
    'missing_due_high_priority',
    i.id,
    json_object(
        'content', i.content,
        'project', p.name,
        'priority', i.priority
    ),
    'set_due_date'
FROM items i
LEFT JOIN projects p ON i.project_id = p.id
WHERE i.is_completed = 0
  AND i.priority >= 3  -- p1 or p2
  AND i.due_date IS NULL
  AND i.due_is_recurring = 0;
```

### Step 2.6: Project Health Analysis

```sql
-- Projects near 300-task limit
SELECT p.name, COUNT(i.id) as task_count
FROM projects p
LEFT JOIN items i ON p.id = i.project_id AND i.is_completed = 0
WHERE p.is_archived = 0
GROUP BY p.id
HAVING task_count > 250
ORDER BY task_count DESC;

-- Empty projects (candidates for deletion)
SELECT p.name, p.id
FROM projects p
LEFT JOIN items i ON p.id = i.project_id AND i.is_completed = 0
WHERE p.is_archived = 0 AND p.is_inbox = 0
GROUP BY p.id
HAVING COUNT(i.id) = 0;
```

### Step 2.7: Generate Summary

```sql
-- Count findings by type
SELECT finding_type, COUNT(*) as count
FROM triage_findings
WHERE session_id = '{SESSION_ID}'
GROUP BY finding_type
ORDER BY count DESC;
```

---

## Phase 3: TRIAGE (Interactive)

### Step 3.1: Present Summary

After analysis, present findings to user:

```
Use AskUserQuestion with:
- Header: "Triage Summary"
- Question: "Analysis complete! Found:\n• X exact duplicates\n• Y fuzzy duplicates\n• Z stale tasks\n• W tasks missing due dates\n\nWhat would you like to tackle?"
- Options:
  - "Duplicates (X+Y)" - Handle duplicate tasks first
  - "Stale tasks (Z)" - Review old/overdue tasks
  - "Missing dates (W)" - Add due dates to priority tasks
  - "Full triage" - Work through all categories
  - "Skip" - Exit without changes
```

### Step 3.2: Handle Exact Duplicates

For exact duplicates, offer batch handling:

```
Use AskUserQuestion with:
- Header: "Exact Duplicates"
- Question: "Found X tasks with identical content:\n• 'Task A' (Project1, Project2)\n• 'Task B' (Inbox, Work)\n...\n\nHow should I handle these?"
- Options:
  - "Keep newest, delete old" - Automatic resolution
  - "Keep oldest, delete new" - Preserve original
  - "Merge (combine notes)" - Keep one, merge descriptions
  - "Review each" - Manual decision per duplicate
```

### Step 3.3: Handle Fuzzy Duplicates

Present fuzzy matches individually or in small batches:

```
Use AskUserQuestion with (batch up to 4 questions):
- Question 1:
  - Header: "Similar 1/N"
  - Question: "'Buy groceries' vs 'Get groceries'\n85% similar | Both in Personal"
  - Options: "Keep first", "Keep second", "Keep both", "Merge"
- Question 2: ...
```

### Step 3.4: Handle Stale Tasks

Group stale tasks by category and offer batch actions:

```
Use AskUserQuestion with:
- Header: "Stale Tasks"
- Question: "Found 15 tasks older than 60 days with no due date:\n• 'Learn Spanish' (145 days)\n• 'Organize photos' (89 days)\n...\n\nQuick action?"
- Options:
  - "Review list" - See all and decide individually
  - "Move to Someday" - Defer all to backlog
  - "Complete all" - Mark as done (they're probably done)
  - "Delete all" - Remove from system
  - "Skip" - Leave as-is
```

### Step 3.5: Handle Missing Due Dates

```
Use AskUserQuestion with:
- Header: "Missing Dates"
- Question: "'Finish quarterly report'\nPriority: P1 | Project: Work\n\nWhen should this be due?"
- Options:
  - "Today"
  - "Tomorrow"
  - "This week"
  - "Next week"
  - "Custom..." (user types date)
  - "Skip"
```

### Step 3.6: Suggest Groupings

Identify tasks with common keywords and suggest organization:

```
Use AskUserQuestion with:
- Header: "Grouping"
- Question: "Found 6 tasks about 'taxes' scattered across projects:\n• 'Gather tax documents' (Finances)\n• 'File state taxes' (Inbox)\n...\n\nCreate a 'Taxes' project?"
- Options:
  - "Create project" - New project, move all
  - "Create section" - Add section in existing project
  - "Add label" - Tag with #taxes
  - "Skip" - Leave scattered
```

---

## Phase 4: CONFIRM

### Step 4.1: Generate Change Summary

Query all findings with user decisions:

```sql
SELECT
    CASE user_decision
        WHEN 'delete' THEN 'Delete'
        WHEN 'complete' THEN 'Complete'
        WHEN 'update' THEN 'Update'
        WHEN 'move' THEN 'Move'
        WHEN 'create' THEN 'Create'
    END as action,
    COUNT(*) as count
FROM triage_findings
WHERE session_id = '{SESSION_ID}' AND user_decision IS NOT NULL
GROUP BY user_decision;
```

### Step 4.2: Request Confirmation

```
Use AskUserQuestion with:
- Header: "Confirm"
- Question: "Ready to apply changes:\n• Delete: 8 duplicate tasks\n• Complete: 3 stale tasks\n• Move: 12 tasks to Someday\n• Update: 6 tasks with due dates\n• Create: 'Taxes' project\n\nProceed?"
- Options:
  - "Apply all" - Execute changes
  - "Dry run" - Show what would happen
  - "Review again" - Go back to triage
  - "Cancel" - Discard all
```

---

## Phase 5: APPLY

### Step 5.1: Execute Changes via MCP

Group changes by operation type and execute in batches:

**Complete tasks:**
```
Use mcp__todoist__complete-tasks with ids array (up to 50 per call)
```

**Update tasks (due dates, projects, priorities):**
```
Use mcp__todoist__update-tasks with tasks array containing:
- id: task ID
- dueString: "tomorrow", "next week", etc.
- projectId: new project ID
- priority: "p1", "p2", "p3", "p4"
```

**Create projects:**
```
Use mcp__todoist__add-projects with projects array
```

**Delete tasks (with caution):**
```
Use mcp__todoist__delete-object with type="task" and id
Only after explicit user confirmation
```

### Step 5.2: Handle Errors

| Error | Recovery |
|-------|----------|
| 403 Forbidden | Project at 300-task limit - suggest sub-project |
| 429 Too Many Requests | Wait 60 seconds, retry |
| Task not found | Skip, already deleted |

### Step 5.3: Update Local Database

After successful MCP operations, update SQLite to reflect changes:

```sql
-- Mark applied findings
UPDATE triage_findings
SET applied_at = datetime('now')
WHERE session_id = '{SESSION_ID}' AND user_decision IS NOT NULL;

-- Update or delete items based on actions
-- (handled per-operation in the apply loop)
```

### Step 5.4: Update TRIAGE_MEMORY.md

Append session results to memory file:

```markdown
### Session {SESSION_ID} - {DATE}

**Changes applied:**
- Deleted N duplicates
- Completed N stale tasks
- Updated N tasks with due dates
- Created "Project Name" project

**User decisions:**
- "Keep both 'Review budget' tasks" (Work and Personal separate)
- Preferred threshold for stale: 60 days

**Patterns learned:**
- Tasks matching `tax.*` → move to Finances
```

---

## Configuration (TRIAGE_MEMORY.md)

The skill reads configuration from `TRIAGE_MEMORY.md`:

```yaml
# Thresholds
stale_thresholds:
  no_due_date_days: 60
  overdue_days: 14
  inbox_days: 7

# Exclusions - never flag these
excluded_projects:
  - "Someday/Maybe"
  - "Reference"

excluded_labels:
  - "@waiting"
  - "@recurring"

# Duplicate handling default
duplicate_default: "keep_newest"  # keep_newest, keep_oldest, merge, review

# Fuzzy match threshold (0-100)
similarity_threshold: 80
```

---

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| 1Password 401 | Session expired | Run `op signin` |
| Todoist API 401 | Token invalid | Check 1Password item |
| Todoist API 429 | Rate limit | Wait 60s, retry |
| SQLite locked | Concurrent access | Retry with backoff |
| Empty sync response | No changes | Normal for incremental |
| MCP 403 | Project limit (300) | Suggest sub-project |

---

## Tools Used

- **Bash**: Database init, API calls, file operations
- **Python**: Sync parsing, fuzzy matching, analysis
- **SQLite**: Local data storage and querying
- **AskUserQuestion**: All interactive decisions
- **mcp__todoist__complete-tasks**: Mark tasks done
- **mcp__todoist__update-tasks**: Modify task properties
- **mcp__todoist__add-projects**: Create new projects
- **mcp__todoist__add-sections**: Create new sections
- **mcp__todoist__delete-object**: Remove items (with confirmation)
- **mcp__todoist__find-projects**: Look up project IDs
- **mcp__todoist__get-overview**: Verify final state
