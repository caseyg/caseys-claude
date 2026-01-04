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
| **Active tasks per project** | **300** ← Most common migration blocker |
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
pip3 install things.py thefuzz python-Levenshtein
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

```python
#!/usr/bin/env python3
"""Analyze Things and Todoist data to detect duplicates and conflicts."""

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from thefuzz import fuzz

class ConflictType(Enum):
    EXACT_MATCH = "exact"           # Same title, same location
    FUZZY_MATCH = "fuzzy"           # Similar title (>80% match)
    THINGS_MORE_DETAILED = "things_richer"  # Things has more info
    TODOIST_MORE_DETAILED = "todoist_richer"  # Todoist has more info
    DIFFERENT_LOCATION = "location"  # Same task, different project/section

class MergeAction(Enum):
    SKIP = "skip"                   # Don't import, keep Todoist version
    UPDATE = "update"               # Update Todoist with Things data
    MARK_DONE_SKIP = "done_skip"    # Mark Things version as migrated, skip
    CREATE_NEW = "create"           # Create as new task (allows duplicates)
    MERGE = "merge"                 # Combine both (append notes, etc.)

@dataclass
class Conflict:
    things_item: dict
    todoist_item: Optional[dict]
    conflict_type: ConflictType
    similarity_score: int
    suggested_action: MergeAction
    reason: str
    user_action: Optional[MergeAction] = None

@dataclass
class MergeReport:
    # Exact matches - likely duplicates
    exact_matches: list = field(default_factory=list)
    # Fuzzy matches - probable duplicates
    fuzzy_matches: list = field(default_factory=list)
    # Things has more detail
    things_richer: list = field(default_factory=list)
    # Todoist has more detail
    todoist_richer: list = field(default_factory=list)
    # No conflict - safe to create
    no_conflict: list = field(default_factory=list)
    # Project/section conflicts
    structure_conflicts: list = field(default_factory=list)

def calculate_detail_score(item: dict, source: str) -> int:
    """Calculate how detailed an item is (higher = more detailed)."""
    score = 0

    if source == "things":
        if item.get("notes"):
            score += len(item["notes"]) // 10  # Points per 10 chars
        if item.get("checklist"):
            score += len(item["checklist"]) * 5  # 5 points per checklist item
        if item.get("deadline"):
            score += 10
        if item.get("tags"):
            score += len(item["tags"]) * 2
    else:  # todoist
        if item.get("description"):
            score += len(item["description"]) // 10
        if item.get("due"):
            score += 10
        if item.get("labels"):
            score += len(item["labels"]) * 2
        # Check for subtasks (would need separate query)

    return score

def find_matching_task(things_task: dict, todoist_tasks: list, threshold: int = 80):
    """Find matching Todoist task for a Things task."""
    things_title = things_task.get("title", "").lower().strip()

    best_match = None
    best_score = 0

    for todoist_task in todoist_tasks:
        todoist_title = todoist_task.get("content", "").lower().strip()

        # Exact match
        if things_title == todoist_title:
            return todoist_task, 100, ConflictType.EXACT_MATCH

        # Fuzzy match
        score = fuzz.ratio(things_title, todoist_title)
        if score > best_score and score >= threshold:
            best_match = todoist_task
            best_score = score

    if best_match:
        return best_match, best_score, ConflictType.FUZZY_MATCH

    return None, 0, None

def find_matching_project(things_name: str, todoist_projects: list, threshold: int = 80):
    """Find matching Todoist project for a Things area/project."""
    things_name_lower = things_name.lower().strip()

    for project in todoist_projects:
        todoist_name = project.get("name", "").lower().strip()

        if things_name_lower == todoist_name:
            return project, 100

        score = fuzz.ratio(things_name_lower, todoist_name)
        if score >= threshold:
            return project, score

    return None, 0

def analyze_conflicts(things_data: dict, todoist_data: dict) -> MergeReport:
    """Analyze both datasets and generate conflict report."""
    report = MergeReport()

    todoist_tasks = todoist_data.get("tasks", [])
    todoist_projects = todoist_data.get("projects", [])
    todoist_sections = todoist_data.get("sections", [])

    # Analyze standalone todos
    for todo in things_data.get("todos", []):
        match, score, conflict_type = find_matching_task(todo, todoist_tasks)

        if match:
            things_score = calculate_detail_score(todo, "things")
            todoist_score = calculate_detail_score(match, "todoist")

            if things_score > todoist_score + 5:  # Things significantly more detailed
                conflict = Conflict(
                    things_item=todo,
                    todoist_item=match,
                    conflict_type=ConflictType.THINGS_MORE_DETAILED,
                    similarity_score=score,
                    suggested_action=MergeAction.UPDATE,
                    reason=f"Things version has more detail (score: {things_score} vs {todoist_score})"
                )
                report.things_richer.append(conflict)
            elif todoist_score > things_score + 5:  # Todoist more detailed
                conflict = Conflict(
                    things_item=todo,
                    todoist_item=match,
                    conflict_type=ConflictType.TODOIST_MORE_DETAILED,
                    similarity_score=score,
                    suggested_action=MergeAction.SKIP,
                    reason=f"Todoist version has more detail (score: {todoist_score} vs {things_score})"
                )
                report.todoist_richer.append(conflict)
            elif conflict_type == ConflictType.EXACT_MATCH:
                conflict = Conflict(
                    things_item=todo,
                    todoist_item=match,
                    conflict_type=conflict_type,
                    similarity_score=score,
                    suggested_action=MergeAction.SKIP,
                    reason="Exact duplicate - already exists in Todoist"
                )
                report.exact_matches.append(conflict)
            else:
                conflict = Conflict(
                    things_item=todo,
                    todoist_item=match,
                    conflict_type=conflict_type,
                    similarity_score=score,
                    suggested_action=MergeAction.SKIP,
                    reason=f"Similar task found ({score}% match)"
                )
                report.fuzzy_matches.append(conflict)
        else:
            # No match - safe to create
            report.no_conflict.append(todo)

    # Analyze project tasks
    for project in things_data.get("projects", []):
        for item in project.get("items", []):
            if item.get("type") == "heading":
                continue

            match, score, conflict_type = find_matching_task(item, todoist_tasks)
            if match:
                things_score = calculate_detail_score(item, "things")
                todoist_score = calculate_detail_score(match, "todoist")

                if things_score > todoist_score + 5:
                    conflict = Conflict(
                        things_item=item,
                        todoist_item=match,
                        conflict_type=ConflictType.THINGS_MORE_DETAILED,
                        similarity_score=score,
                        suggested_action=MergeAction.UPDATE,
                        reason=f"Things version more detailed (in project: {project['title']})"
                    )
                    report.things_richer.append(conflict)
                else:
                    conflict = Conflict(
                        things_item=item,
                        todoist_item=match,
                        conflict_type=conflict_type,
                        similarity_score=score,
                        suggested_action=MergeAction.SKIP,
                        reason=f"Duplicate found (in project: {project['title']})"
                    )
                    if conflict_type == ConflictType.EXACT_MATCH:
                        report.exact_matches.append(conflict)
                    else:
                        report.fuzzy_matches.append(conflict)
            else:
                report.no_conflict.append(item)

    # Analyze structure (areas -> projects)
    for area in things_data.get("areas", []):
        match, score = find_matching_project(area["title"], todoist_projects)
        if match and score < 100:
            conflict = Conflict(
                things_item=area,
                todoist_item=match,
                conflict_type=ConflictType.FUZZY_MATCH,
                similarity_score=score,
                suggested_action=MergeAction.MERGE,
                reason=f"Similar project exists: '{match['name']}' ({score}% match)"
            )
            report.structure_conflicts.append(conflict)

    return report

def print_report(report: MergeReport):
    """Print human-readable conflict report."""
    print("\n" + "="*60)
    print("MIGRATION CONFLICT REPORT")
    print("="*60)

    print(f"\n✅ NO CONFLICTS: {len(report.no_conflict)} items ready to import")

    if report.exact_matches:
        print(f"\n⚠️  EXACT DUPLICATES: {len(report.exact_matches)} items")
        print("   Suggested: SKIP (already in Todoist)")
        for c in report.exact_matches[:5]:
            print(f"   - {c.things_item.get('title', '')[:50]}")
        if len(report.exact_matches) > 5:
            print(f"   ... and {len(report.exact_matches) - 5} more")

    if report.fuzzy_matches:
        print(f"\n🔍 FUZZY MATCHES: {len(report.fuzzy_matches)} items")
        print("   Suggested: Review and decide")
        for c in report.fuzzy_matches[:5]:
            print(f"   - Things: '{c.things_item.get('title', '')[:40]}'")
            print(f"     Todoist: '{c.todoist_item.get('content', '')[:40]}' ({c.similarity_score}%)")
        if len(report.fuzzy_matches) > 5:
            print(f"   ... and {len(report.fuzzy_matches) - 5} more")

    if report.things_richer:
        print(f"\n📝 THINGS MORE DETAILED: {len(report.things_richer)} items")
        print("   Suggested: UPDATE Todoist with Things data")
        for c in report.things_richer[:5]:
            print(f"   - {c.things_item.get('title', '')[:50]}")
            print(f"     Reason: {c.reason}")
        if len(report.things_richer) > 5:
            print(f"   ... and {len(report.things_richer) - 5} more")

    if report.todoist_richer:
        print(f"\n📋 TODOIST MORE DETAILED: {len(report.todoist_richer)} items")
        print("   Suggested: SKIP (keep Todoist version)")
        for c in report.todoist_richer[:5]:
            print(f"   - {c.things_item.get('title', '')[:50]}")
        if len(report.todoist_richer) > 5:
            print(f"   ... and {len(report.todoist_richer) - 5} more")

    if report.structure_conflicts:
        print(f"\n🏗️  STRUCTURE CONFLICTS: {len(report.structure_conflicts)} projects/areas")
        for c in report.structure_conflicts:
            print(f"   - Things: '{c.things_item.get('title')}'")
            print(f"     Todoist: '{c.todoist_item.get('name')}' ({c.similarity_score}%)")

    print("\n" + "="*60)

if __name__ == "__main__":
    with open("things_export.json") as f:
        things_data = json.load(f)
    with open("todoist_export.json") as f:
        todoist_data = json.load(f)

    report = analyze_conflicts(things_data, todoist_data)
    print_report(report)

    # Save report for next step
    # (Would need to serialize dataclasses)
```

---

## Step 4: Present Conflicts to User (Interactive)

After running the analysis, use Claude's `AskUserQuestion` tool to get user decisions. Group similar conflicts for efficient decision-making.

### AskUserQuestion Examples

**Question 1: Exact Duplicates**

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

**Question 2: Fuzzy Matches**

```
AskUserQuestion(
  questions=[{
    "question": "Found 8 similar tasks:\n• Things 'Buy groceries' → Todoist 'Get groceries' (85%)\n• Things 'Call dentist' → Todoist 'Dentist call' (78%)\n• Things 'Q4 budget review' → Todoist 'Review Q4 budget' (90%)\n...and 5 more. How should I handle these?",
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

**Question 3: Things Has More Detail**

```
AskUserQuestion(
  questions=[{
    "question": "Found 12 tasks where Things has richer notes/checklists than Todoist. Update Todoist with the Things data?",
    "header": "Enrich",
    "multiSelect": false,
    "options": [
      {"label": "Update all (Recommended)", "description": "Enhance Todoist tasks with Things notes/checklists"},
      {"label": "Skip all", "description": "Keep Todoist as-is, don't import Things details"},
      {"label": "Review individually", "description": "I'll decide which tasks to enrich"}
    ]
  }]
)
```

**Question 4: Structure Conflicts (per area)**

```
AskUserQuestion(
  questions=[{
    "question": "Things area 'Work Projects' matches Todoist project 'Work' (82% similar). How should I handle this?",
    "header": "Structure",
    "multiSelect": false,
    "options": [
      {"label": "Merge into 'Work'", "description": "Add Things tasks to existing Todoist project"},
      {"label": "Create new project", "description": "Create 'Work Projects' as separate project"},
      {"label": "Create as section", "description": "Create 'Work Projects' as section inside 'Work'"},
      {"label": "Skip this area", "description": "Don't import tasks from this Things area"}
    ]
  }]
)
```

**Question 5: Final Confirmation**

```
AskUserQuestion(
  questions=[{
    "question": "Ready to migrate:\n• Create: 45 new tasks\n• Update: 12 tasks with richer data\n• Skip: 23 duplicates\n\nProceed with migration?",
    "header": "Confirm",
    "multiSelect": false,
    "options": [
      {"label": "Yes, migrate now", "description": "Execute the migration with these decisions"},
      {"label": "Dry run first", "description": "Show what would happen without making changes"},
      {"label": "Cancel", "description": "Abort migration, make no changes"}
    ]
  }]
)
```

### Multi-Question Batching

When there are multiple structure conflicts, batch them into one call:

```
AskUserQuestion(
  questions=[
    {
      "question": "'Work Projects' → 'Work' (82% match)?",
      "header": "Work",
      "multiSelect": false,
      "options": [
        {"label": "Merge", "description": "Add to existing 'Work' project"},
        {"label": "New project", "description": "Create as separate project"},
        {"label": "Skip", "description": "Don't import this area"}
      ]
    },
    {
      "question": "'Personal' → 'Personal Life' (75% match)?",
      "header": "Personal",
      "multiSelect": false,
      "options": [
        {"label": "Merge", "description": "Add to existing 'Personal Life' project"},
        {"label": "New project", "description": "Create as separate project"},
        {"label": "Skip", "description": "Don't import this area"}
      ]
    },
    {
      "question": "'Side Projects' → No match found",
      "header": "Side",
      "multiSelect": false,
      "options": [
        {"label": "Create new", "description": "Create 'Side Projects' in Todoist"},
        {"label": "Skip", "description": "Don't import this area"}
      ]
    }
  ]
)
```

---

## Step 5: Execute Migration with Todoist MCP

### Using MCP (Recommended)

The Todoist MCP provides `add-tasks` which handles batching and rate limiting:

```
# 1. Get project IDs
mcp__todoist__find-projects()  # Returns all projects with IDs

# 2. Build project mapping
PROJECT_MAP = {
    'Work 💼': 'Work',           # → project_id from find-projects
    'Career 📈': 'Career',
    'Professional': 'Career',   # Things area → Todoist project
    'Networking 🤝': 'Career',
    'Finances 💸': 'Finances',
    'Ideas': 'Projects',
    'Growth 🌱': 'Personal Growth',
    'Love 💘': 'Love',
    'Organization and systems 🗂️': 'Organization + Systems',
    'Maine 🌲': 'Maine',
    'Home and style 💅': 'Style',
    'Projects + Fun 🕺': 'Fun',
    'Body and health 💪': 'Health',
    'Social (friends and family) 🫶': 'Relationships',
}

# 3. Batch add tasks (up to 100 at a time)
mcp__todoist__add-tasks({
  "tasks": [
    {"content": "Task title", "projectId": "xxx", "description": "notes"},
    {"content": "Another task", "projectId": "yyy"},
    // ... up to 100 tasks
  ]
})
```

### MCP Error Handling

**HTTP 403 ≠ Rate Limiting** — This is the most common mistake!

| Error | HTTP Status | Meaning |
|-------|-------------|---------|
| `MAX_ITEMS_LIMIT_REACHED` | 403 | Project has 300 tasks. Create sub-project. |
| Rate limit | 429 | Too many API calls. Wait 15 minutes. |

**When you hit 403 with `MAX_ITEMS_LIMIT_REACHED`:**
```
# 1. Create a sub-project
mcp__todoist__add-projects([{"name": "Work Backlog", "parentId": "WORK_ID"}])

# 2. Import remaining tasks to the new sub-project
mcp__todoist__add-tasks([{..., "projectId": "NEW_SUBPROJECT_ID"}])
```

The MCP uses the same Todoist API limits (~450 requests per 15 minutes). For large batches, it's more efficient to use fewer calls with more tasks per call (up to 50).

### Fallback: Python Script with Rate Limiting

```python
#!/usr/bin/env python3
"""Execute migration based on user decisions - fallback script."""

import json
import time
from todoist_api_python.api import TodoistAPI
from typing import Dict, List

RATE_LIMIT_DELAY = 2.5  # Safe: ~24 req/min, well under 30/min limit

def execute_migration(
    api_token: str,
    things_data: dict,
    todoist_data: dict,
    decisions: dict,
    dry_run: bool = True
):
    """
    Execute migration with user-specified merge decisions.

    Args:
        api_token: Todoist API token
        things_data: Exported Things data
        todoist_data: Exported Todoist data
        decisions: Dict mapping conflict categories to actions:
            {
                "exact_matches": "skip",
                "fuzzy_matches": "skip",
                "things_richer": "update",
                "todoist_richer": "skip",
                "structure_mapping": {
                    "Work Projects": {"action": "merge", "target_id": "123456"},
                    "Personal": {"action": "create"}
                },
                "individual_overrides": {
                    "uuid-123": "create",  # Override for specific item
                    "uuid-456": "skip"
                }
            }
        dry_run: If True, only print what would happen
    """
    api = TodoistAPI(api_token)

    stats = {
        "skipped": 0,
        "updated": 0,
        "created": 0,
        "marked_done": 0,
        "errors": 0
    }

    # Build lookup tables
    todoist_tasks_by_title = {
        t["content"].lower().strip(): t
        for t in todoist_data.get("tasks", [])
    }
    todoist_projects_by_name = {
        p["name"].lower().strip(): p
        for p in todoist_data.get("projects", [])
    }

    # Process areas -> projects
    area_to_project = {}
    print("\n=== Processing Areas/Projects ===")

    for area in things_data.get("areas", []):
        area_title = area["title"]
        struct_decision = decisions.get("structure_mapping", {}).get(area_title, {})
        action = struct_decision.get("action", "create")

        if action == "merge":
            target_id = struct_decision.get("target_id")
            area_to_project[area["uuid"]] = target_id
            print(f"  Merging '{area_title}' into existing project (ID: {target_id})")
        elif action == "skip":
            print(f"  Skipping area: {area_title}")
            stats["skipped"] += 1
        else:  # create
            if dry_run:
                print(f"  Would create project: {area_title}")
                area_to_project[area["uuid"]] = f"new_{area['uuid']}"
            else:
                project = api.add_project(name=area_title)
                area_to_project[area["uuid"]] = project.id
                print(f"  Created project: {area_title}")
                stats["created"] += 1
                time.sleep(RATE_LIMIT_DELAY)

    # Process tasks
    print("\n=== Processing Tasks ===")

    def process_task(todo: dict, project_id=None, section_id=None):
        """Process a single task based on decisions."""
        title = todo.get("title", "")
        uuid = todo.get("uuid")

        # Check for individual override
        if uuid in decisions.get("individual_overrides", {}):
            action = decisions["individual_overrides"][uuid]
        else:
            # Check if this is a duplicate
            title_lower = title.lower().strip()
            existing = todoist_tasks_by_title.get(title_lower)

            if existing:
                # Determine which category this falls into
                things_score = len(todo.get("notes", "")) + len(todo.get("checklist", [])) * 10
                todoist_score = len(existing.get("description", ""))

                if things_score > todoist_score + 5:
                    action = decisions.get("things_richer", "update")
                elif todoist_score > things_score + 5:
                    action = decisions.get("todoist_richer", "skip")
                else:
                    action = decisions.get("exact_matches", "skip")
            else:
                action = "create"

        # Execute action
        if action == "skip":
            print(f"    Skipped: {title[:50]}")
            stats["skipped"] += 1
            return None

        elif action == "done_skip":
            print(f"    Marked done & skipped: {title[:50]}")
            stats["marked_done"] += 1
            return None

        elif action == "update":
            existing = todoist_tasks_by_title.get(title.lower().strip())
            if existing and not dry_run:
                try:
                    # Update with Things data
                    update_data = {}
                    if todo.get("notes") and len(todo["notes"]) > len(existing.get("description", "")):
                        update_data["description"] = todo["notes"]
                    if todo.get("deadline") and not existing.get("due"):
                        update_data["due_string"] = todo["deadline"]

                    if update_data:
                        api.update_task(task_id=existing["id"], **update_data)
                        print(f"    Updated: {title[:50]}")
                        stats["updated"] += 1
                        time.sleep(RATE_LIMIT_DELAY)
                except Exception as e:
                    print(f"    Error updating {title[:50]}: {e}")
                    stats["errors"] += 1
            elif dry_run:
                print(f"    Would update: {title[:50]}")
            return None

        else:  # create
            if dry_run:
                print(f"    Would create: {title[:50]}")
                stats["created"] += 1
                return None

            try:
                task_data = {
                    "content": title,
                    "description": todo.get("notes", ""),
                }
                if project_id:
                    task_data["project_id"] = project_id
                if section_id:
                    task_data["section_id"] = section_id
                if todo.get("deadline"):
                    task_data["due_string"] = todo["deadline"]

                task = api.add_task(**task_data)
                print(f"    Created: {title[:50]}")
                stats["created"] += 1
                time.sleep(RATE_LIMIT_DELAY)

                # Create subtasks from checklist
                for item in todo.get("checklist", []):
                    api.add_task(
                        content=item.get("title", ""),
                        parent_id=task.id
                    )
                    time.sleep(RATE_LIMIT_DELAY)

                return task
            except Exception as e:
                print(f"    Error creating {title[:50]}: {e}")
                stats["errors"] += 1
                return None

    # Process standalone todos
    for todo in things_data.get("todos", []):
        project_id = area_to_project.get(todo.get("area_uuid"))
        process_task(todo, project_id)

    # Process project tasks
    for project in things_data.get("projects", []):
        parent_project_id = area_to_project.get(project.get("area_uuid"))

        for item in project.get("items", []):
            if item.get("type") != "heading":
                process_task(item, parent_project_id)

    # Summary
    print("\n" + "="*60)
    print("MIGRATION SUMMARY")
    print("="*60)
    print(f"  Created: {stats['created']}")
    print(f"  Updated: {stats['updated']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Marked done: {stats['marked_done']}")
    print(f"  Errors: {stats['errors']}")

    return stats

if __name__ == "__main__":
    import os

    with open("things_export.json") as f:
        things_data = json.load(f)
    with open("todoist_export.json") as f:
        todoist_data = json.load(f)

    token = os.environ.get("TODOIST_API_TOKEN")

    # Example decisions (would come from user interaction)
    decisions = {
        "exact_matches": "skip",
        "fuzzy_matches": "skip",
        "things_richer": "update",
        "todoist_richer": "skip",
        "structure_mapping": {
            # "Work Projects": {"action": "merge", "target_id": "existing_project_id"},
        },
        "individual_overrides": {
            # "specific-uuid": "create"
        }
    }

    print("=== DRY RUN ===")
    execute_migration(token, things_data, todoist_data, decisions, dry_run=True)

    # Uncomment to execute:
    # print("\n=== EXECUTING ===")
    # execute_migration(token, things_data, todoist_data, decisions, dry_run=False)
```

---

## Merge Actions Reference

| Action | Effect | When to Use |
|--------|--------|-------------|
| `skip` | Keep Todoist version, don't import | Exact duplicates, Todoist is source of truth |
| `update` | Update Todoist task with Things data | Things has richer notes/checklists |
| `done_skip` | Mark as migrated, skip import | Task is done conceptually, just cleaning up |
| `create` | Create new task in Todoist | No duplicate exists, or want both versions |
| `merge` | Combine data from both | Preserve info from both systems |

---

## Interactive Workflow Summary

When running `/things-to-todoist`, Claude will:

1. **Export both systems** automatically
2. **Analyze conflicts** and generate report
3. **Ask user** about each conflict category:
   - "Found 15 exact duplicates. Skip all?" → User: "Yes"
   - "Found 8 fuzzy matches. Review individually?" → User: "Show me the first 5"
   - "Things has more detail for 12 tasks. Update Todoist?" → User: "Yes, update all"
   - "'Work Projects' matches 'Work' (82%). Merge or create new?" → User: "Merge into Work"
4. **Execute** with confirmed decisions
5. **Report** results

---

## Error Handling

### HTTP Status Codes

| Status | Meaning | Solution |
|--------|---------|----------|
| **403** | **Forbidden** - Project item limit (300) reached | Create a sub-project and import there |
| **429** | **Rate Limit** - Too many API calls | Wait 15 minutes, then retry with delays |
| 400 | Bad request | Check task content format |
| 401 | Unauthorized | Verify API token |

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `MAX_ITEMS_LIMIT_REACHED` | Project has 300 active tasks | Create sub-project: `add-projects({parentId: "..."})` |
| `Database is locked` | Things is running | Quit Things 3 before running export |
| `Rate limit exceeded` | Too many API calls | Increase delay or wait 15 minutes |
| `Task not found` | ID changed | Re-export Todoist data and retry |
| `Invalid project_id` | Structure changed | Re-run structure mapping step |

### Large Migration Strategy

For migrations with 300+ tasks per project:

1. **Pre-check task counts**: Count tasks per Things area/project before migrating
2. **Create sub-projects proactively**: If an area has >250 tasks, create sub-projects first
3. **Batch by sub-project**: Split tasks across sub-projects to stay under 300 each

```python
# Example: Split large project into sub-projects
if len(tasks) > 250:
    # Create "Work Backlog" sub-project
    backlog = mcp__todoist__add-projects([{"name": "Backlog", "parentId": project_id}])
    # Import older/lower-priority tasks to backlog
```

---

## Sources

- [things.py library](https://github.com/thingsapi/things.py) - Python library for Things 3 database access
- [todoist-api-python](https://github.com/Doist/todoist-api-python) - Official Todoist Python SDK
- [Todoist API Documentation](https://developer.todoist.com/api/v1/)
- [Todoist Usage Limits](https://www.todoist.com/help/articles/usage-limits-in-todoist-e5rcSY) - Official limits (300 tasks/project)
- [thefuzz](https://github.com/seatgeek/thefuzz) - Fuzzy string matching
- [Things Data Export Support](https://culturedcode.com/things/support/articles/2982272/)
