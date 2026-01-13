---
name: things-to-todoist
description: Migrate tasks from Things 3 to Todoist with duplicate detection and merge
  support. Use when the user asks to migrate, export, sync, or move tasks from Things
  to Todoist.
---

# Things to Todoist Migration

Migrate tasks, projects, areas, and tags from Things 3 for Mac to Todoist with intelligent duplicate detection and merge support.

## Trigger Phrases

- `/things-to-todoist`
- "migrate things to todoist"
- "export things to todoist"
- "merge things with todoist"

## Prerequisites

### 1. Todoist MCP (Recommended)

The Todoist MCP handles rate limiting, batching, and provides a cleaner interface:
- Batch task creation with `mcp__todoist__add-tasks` (up to 50 tasks per call)
- Project/sub-project creation with `mcp__todoist__add-projects`
- Project lookup with `mcp__todoist__find-projects`
- Task search with `mcp__todoist__find-tasks`

---

## Todoist Usage Limits

Understanding these limits is critical for large migrations. Source: [Todoist Help](https://www.todoist.com/help/articles/usage-limits-in-todoist-e5rcSY)

### Per-Project Limits (All Plans)
| Resource | Limit |
|----------|-------|
| **Active tasks per project** | **300** <- Most common migration blocker |
| Sections per project | 20 |
| Task name | 500 characters |
| Task description | 16,383 characters |
| Task comment | 15,000 characters |
| Labels per task | 100 |

### Account Limits
| Resource | Beginner | Pro |
|----------|----------|-----|
| Active personal projects | 5 | 300 |
| Total active projects | 500 | 500 |
| Labels per account | 500 | 500 |
| Filters | 3 | 150 |

### API Limits
| Limit | Value |
|-------|-------|
| Sync API commands per request | 100 |
| Rate limit | ~450 requests per 15 minutes |
| Rate limit response | HTTP 429 |
| Project limit response | HTTP 403 with `MAX_ITEMS_LIMIT_REACHED` |

### Workaround: Sub-Projects

When a project hits the 300-task limit, create sub-projects:

```
mcp__todoist__add-projects({
  "projects": [{"name": "Work Backlog", "parentId": "WORK_PROJECT_ID"}]
})
```

Sub-projects have their own separate 300-task limit, effectively extending capacity.

### 2. Python Libraries (for Things export)

```bash
uv pip install things.py thefuzz python-Levenshtein
```

### 3. Things 3 Must Be Installed

The `things.py` library reads directly from the Things SQLite database at:
```
~/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/Things Database.thingsdatabase/main.sqlite
```

## Concept Mapping

| Things 3 | Todoist | Notes |
|----------|---------|-------|
| Area | Project | Top-level organizational container |
| Project | Section or Sub-project | Can be nested under Area's project |
| Heading | Section | Dividers within projects |
| To-Do | Task | Individual actionable items |
| Checklist Item | Subtask | Nested under parent task |
| Tag | Label | Applied to tasks |
| Notes | Description | Task description field |
| When (Today/Evening/Anytime/Someday) | Priority + Due Date | Map scheduling to Todoist equivalents |
| Deadline | Due Date | Direct mapping |

## Workflow Overview

This is an **interactive migration** with user decision points:

1. **Export** - Extract data from Things
2. **Fetch** - Get current Todoist state
3. **Analyze** - Detect duplicates and conflicts
4. **Present** - Show merge report to user
5. **Decide** - User chooses merge strategy per conflict
6. **Execute** - Apply decisions
7. **Verify** - Confirm results

---

## Step 1: Retrieve Todoist API Token

```bash
# If using 1Password
op item get "Todoist" --fields "API Token"

# Or use environment variable
echo $TODOIST_API_TOKEN
```

---

## Step 2: Export Both Systems

### Export Things Data

```python
#!/usr/bin/env python3
"""Extract all data from Things 3 for migration."""

import things
import json
from datetime import datetime

def export_things_data():
    """Export complete Things database to structured dict."""

    data = {
        "exported_at": datetime.now().isoformat(),
        "source": "things",
        "areas": [],
        "projects": [],
        "todos": [],
        "tags": []
    }

    # Export areas
    for area in things.areas():
        data["areas"].append({
            "uuid": area.get("uuid"),
            "title": area.get("title"),
            "tags": area.get("tags", [])
        })

    # Export projects (including area association)
    for project in things.projects(include_items=True):
        data["projects"].append({
            "uuid": project.get("uuid"),
            "title": project.get("title"),
            "area_uuid": project.get("area"),
            "notes": project.get("notes", ""),
            "tags": project.get("tags", []),
            "status": project.get("status"),
            "deadline": project.get("deadline"),
            "items": project.get("items", [])  # Headings and todos
        })

    # Export standalone todos (not in projects)
    for todo in things.todos():
        if not todo.get("project"):
            data["todos"].append({
                "uuid": todo.get("uuid"),
                "title": todo.get("title"),
                "area_uuid": todo.get("area"),
                "notes": todo.get("notes", ""),
                "tags": todo.get("tags", []),
                "status": todo.get("status"),
                "when": todo.get("when"),
                "deadline": todo.get("deadline"),
                "checklist": todo.get("checklist", [])
            })

    # Export tags
    for tag in things.tags():
        data["tags"].append({
            "uuid": tag.get("uuid"),
            "title": tag.get("title"),
            "parent_uuid": tag.get("parent")
        })

    return data

if __name__ == "__main__":
    data = export_things_data()
    with open("things_export.json", "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Exported: {len(data['areas'])} areas, {len(data['projects'])} projects, "
          f"{len(data['todos'])} standalone todos, {len(data['tags'])} tags")
```

### Export Todoist Data

```python
#!/usr/bin/env python3
"""Export current Todoist state for comparison."""

import json
import os
from todoist_api_python.api import TodoistAPI

def export_todoist_data(api_token: str):
    """Export complete Todoist state to structured dict."""
    api = TodoistAPI(api_token)

    data = {
        "source": "todoist",
        "projects": [],
        "sections": [],
        "tasks": [],
        "labels": []
    }

    # Export projects
    for project in api.get_projects():
        data["projects"].append({
            "id": project.id,
            "name": project.name,
            "parent_id": project.parent_id,
            "color": project.color,
            "is_favorite": project.is_favorite
        })

    # Export sections
    for section in api.get_sections():
        data["sections"].append({
            "id": section.id,
            "name": section.name,
            "project_id": section.project_id,
            "order": section.order
        })

    # Export tasks (active only)
    for task in api.get_tasks():
        data["tasks"].append({
            "id": task.id,
            "content": task.content,
            "description": task.description or "",
            "project_id": task.project_id,
            "section_id": task.section_id,
            "parent_id": task.parent_id,
            "labels": task.labels,
            "priority": task.priority,
            "due": task.due.string if task.due else None,
            "is_completed": task.is_completed
        })

    # Export labels
    for label in api.get_labels():
        data["labels"].append({
            "id": label.id,
            "name": label.name,
            "color": label.color
        })

    return data

if __name__ == "__main__":
    token = os.environ.get("TODOIST_API_TOKEN")
    data = export_todoist_data(token)
    with open("todoist_export.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Exported: {len(data['projects'])} projects, {len(data['sections'])} sections, "
          f"{len(data['tasks'])} tasks, {len(data['labels'])} labels")
```

---

## Step 3: Analyze and Detect Conflicts

Use fuzzy matching to detect duplicates:

```python
#!/usr/bin/env python3
"""Analyze Things and Todoist data to detect duplicates and conflicts."""

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from thefuzz import fuzz

class ConflictType(Enum):
    EXACT_MATCH = "exact"
    FUZZY_MATCH = "fuzzy"
    THINGS_MORE_DETAILED = "things_richer"
    TODOIST_MORE_DETAILED = "todoist_richer"
    DIFFERENT_LOCATION = "location"

class MergeAction(Enum):
    SKIP = "skip"
    UPDATE = "update"
    MARK_DONE_SKIP = "done_skip"
    CREATE_NEW = "create"
    MERGE = "merge"

@dataclass
class Conflict:
    things_item: dict
    todoist_item: Optional[dict]
    conflict_type: ConflictType
    similarity_score: int
    suggested_action: MergeAction
    reason: str
    user_action: Optional[MergeAction] = None

def find_matching_task(things_task: dict, todoist_tasks: list, threshold: int = 80):
    """Find matching Todoist task for a Things task."""
    things_title = things_task.get("title", "").lower().strip()

    best_match = None
    best_score = 0

    for todoist_task in todoist_tasks:
        todoist_title = todoist_task.get("content", "").lower().strip()

        if things_title == todoist_title:
            return todoist_task, 100, ConflictType.EXACT_MATCH

        score = fuzz.ratio(things_title, todoist_title)
        if score > best_score and score >= threshold:
            best_match = todoist_task
            best_score = score

    if best_match:
        return best_match, best_score, ConflictType.FUZZY_MATCH

    return None, 0, None
```

---

## Step 4: Present Conflicts to User (Interactive)

Use `AskUserQuestion` to get user decisions on conflicts:

**Exact Duplicates:**
```
AskUserQuestion(
  questions=[{
    "question": "Found 15 exact duplicate tasks already in Todoist. How should I handle them?",
    "header": "Duplicates",
    "multiSelect": false,
    "options": [
      {"label": "Skip all (Recommended)", "description": "Keep Todoist versions, don't import from Things"},
      {"label": "Mark done & skip", "description": "Consider these migrated, skip import"},
      {"label": "Review individually", "description": "I'll decide for each of the 15 tasks"}
    ]
  }]
)
```

**Fuzzy Matches:**
```
AskUserQuestion(
  questions=[{
    "question": "Found 8 similar tasks. How should I handle these?",
    "header": "Similar",
    "multiSelect": false,
    "options": [
      {"label": "Skip all matches", "description": "Treat as duplicates, keep Todoist versions"},
      {"label": "Update if Things richer", "description": "Update Todoist when Things has more detail"},
      {"label": "Create as new", "description": "Import all as new tasks (allows duplicates)"},
      {"label": "Review individually", "description": "I'll decide for each similar pair"}
    ]
  }]
)
```

---

## Step 5: Execute Migration with Todoist MCP

```
# 1. Get project IDs
mcp__todoist__find-projects()

# 2. Build project mapping
PROJECT_MAP = {
    'Work': 'project_id_from_find',
    'Personal': 'another_project_id',
}

# 3. Batch add tasks (up to 50 at a time)
mcp__todoist__add-tasks({
  "tasks": [
    {"content": "Task title", "projectId": "xxx", "description": "notes"},
    {"content": "Another task", "projectId": "yyy"},
  ]
})
```

### MCP Error Handling

| Error | HTTP Status | Meaning |
|-------|-------------|---------|
| `MAX_ITEMS_LIMIT_REACHED` | 403 | Project has 300 tasks. Create sub-project. |
| Rate limit | 429 | Too many API calls. Wait 15 minutes. |

---

## Merge Actions Reference

| Action | Effect | When to Use |
|--------|--------|-------------|
| `skip` | Keep Todoist version, don't import | Exact duplicates, Todoist is source of truth |
| `update` | Update Todoist task with Things data | Things has richer notes/checklists |
| `done_skip` | Mark as migrated, skip import | Task is done conceptually |
| `create` | Create new task in Todoist | No duplicate exists |
| `merge` | Combine data from both | Preserve info from both systems |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `MAX_ITEMS_LIMIT_REACHED` | Project has 300 active tasks | Create sub-project |
| `Database is locked` | Things is running | Quit Things 3 before export |
| `Rate limit exceeded` | Too many API calls | Wait 15 minutes |
| `Task not found` | ID changed | Re-export Todoist data |

---

## Sources

- [things.py library](https://github.com/thingsapi/things.py)
- [todoist-api-python](https://github.com/Doist/todoist-api-python)
- [Todoist API Documentation](https://developer.todoist.com/api/v1/)
- [Todoist Usage Limits](https://www.todoist.com/help/articles/usage-limits-in-todoist-e5rcSY)
- [thefuzz](https://github.com/seatgeek/thefuzz)
