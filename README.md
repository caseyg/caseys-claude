# Casey's Claude Code Skills

Personal automation skills for [Claude Code](https://claude.ai/code). Skills are declarative markdown files that extend Claude's capabilities with domain-specific workflows.

## Installation

```bash
# Add from marketplace
/plugin marketplace add caseyg/caseys-claude
/plugin install caseys-claude@caseys-claude
```

Or clone directly:

```bash
cd ~/.claude
git clone https://github.com/caseyg/caseys-claude.git
```

## Available skills

| Skill | Description |
|-------|-------------|
| **reorder-basics** | Amazon Buy Again automation with 1Password integration |
| **book-fitness** | Chelsea Piers class booking via REST API with JWT caching |
| **coop-shift** | Park Slope Food Coop shift finder with browser automation |
| **tripit-export** | Export TripIt travel data to JSON |
| **things-to-todoist** | Migrate tasks from Things 3 to Todoist |
| **todoist-triage** | Inbox triage with duplicate detection and ADHD-friendly coaching |
| **not-ai** | Rewrite AI-sounding text into clear, natural plain language |

## Dependencies

Different skills require different integrations:

- **1Password CLI** (`op`) - Secure credential storage
- **dev-browser** - Browser automation for sites without APIs
- **Todoist MCP** - Task management via `mcp__todoist__*` tools
- **Python** - For Things 3 export (`things.py`, `thefuzz`)

## Usage

Skills activate via natural language or slash commands:

- "Reorder my Amazon basics"
- "Book yoga tomorrow at Chelsea Piers"
- "Find an available coop shift"
- "Triage my Todoist inbox"
- `/not-ai` - Rewrite text in plain language

## Repository structure

```
skills/
  <skill-name>/
    SKILL.md                   # Skill definition with YAML frontmatter
    assets/                    # Optional supplementary files (templates, configs)
```

## SKILL.md format

Each skill has a SKILL.md with YAML frontmatter:

```yaml
---
name: skill-name
description: When to use this skill and what it does.
---

# Skill Title

Skill documentation, workflow steps, and code examples.
```

## License

Personal use. Skills contain hardcoded assumptions (locations, accounts, preferences) that you'd need to adapt for your own use.
