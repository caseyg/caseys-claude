# Todoist Triage Memory

This file stores user preferences, learned rules, and session history for the Todoist triage skill.

## Configuration

```yaml
# Stale task thresholds
stale_thresholds:
  no_due_date_days: 60        # Tasks without due date older than this
  overdue_days: 14            # Tasks past due date by this many days
  inbox_days: 7               # Tasks in Inbox longer than this

# Projects to exclude from triage (never flag tasks in these)
excluded_projects: []
# Example:
# excluded_projects:
#   - "Someday/Maybe"
#   - "Reference"
#   - "Templates"

# Labels to exclude (never flag tasks with these labels)
excluded_labels: []
# Example:
# excluded_labels:
#   - "@waiting"
#   - "@recurring"
#   - "@reference"

# Duplicate handling default
duplicate_default: "review"    # review, keep_newest, keep_oldest, merge

# Fuzzy match similarity threshold (0-100)
similarity_threshold: 80

# Temporal cluster settings
temporal_cluster:
  window_minutes: 10            # Tasks created within this window are grouped
  min_cluster_size: 3           # Minimum tasks to form a cluster
```

## Known Patterns

Patterns learned from asking the user about people, concepts, and actions.

```yaml
# People - Names that appear in tasks with known context
known_people: {}
# Example:
# known_people:
#   Sarah:
#     context: work              # work, personal, client, multiple
#     action: move_to_project    # move_to_project, add_label, none
#     project: "Work"
#   Mom:
#     context: personal
#     action: add_label
#     label: "@family"

# Concepts - Keywords that should trigger organization
known_concepts: {}
# Example:
# known_concepts:
#   website:
#     action: add_label
#     label: "@website"
#   taxes:
#     action: move_to_project
#     project: "Finances"
#   quarterly:
#     action: add_label
#     label: "@quarterly-review"

# Action patterns - Verbs at start of tasks
action_rules: {}
# Example:
# action_rules:
#   call:
#     action: add_label
#     label: "@phone"
#   email:
#     action: none               # Too common to be useful
#   buy:
#     action: move_to_project
#     project: "Shopping"
```

## Triage Statistics

| Metric | Value |
|--------|-------|
| Total sessions | 0 |
| Tasks triaged | 0 |
| Duplicates removed | 0 |
| Stale tasks cleared | 0 |
| Projects created | 0 |

## Learned Rules

Rules automatically learned from user decisions. Higher confidence = more consistent decisions.

| Pattern | Action | Confidence | Times Applied |
|---------|--------|------------|---------------|
| _No rules yet_ | | | |

<!-- Example rules:
| `tax.*` | Move to Finances | 95% | 12 |
| `call.*` | Add @phone label | 88% | 8 |
| `buy.*\|shop.*` | Move to Shopping | 92% | 15 |
-->

## User Preferences

Preferences inferred from past decisions:

- **Duplicate handling**: _Not yet determined_
- **Preferred default priority**: _Not yet determined_
- **Someday equivalent project**: _Not yet determined_

## Session History

### No sessions yet

_Run `/todoist-triage` to start your first triage session._

<!--
### Session 20260108_143000 - January 8, 2026

**Changes applied:**
- Deleted 5 duplicates
- Completed 12 stale tasks
- Created "Q1 2026 Planning" project
- Moved 8 tasks from Inbox to appropriate projects

**User decisions:**
- "Keep both 'Review budget' tasks" (Work and Personal are separate)
- "Create section not project for taxes" → Added 'Taxes' section to Finances

**Patterns learned:**
- Tasks containing "tax" → Finances project
-->

## Excluded Items

Specific tasks or patterns to never flag (user explicitly said to keep):

| Item/Pattern | Reason | Added |
|--------------|--------|-------|
| _None yet_ | | |

## Notes

_Add any personal notes about your Todoist organization preferences here._
