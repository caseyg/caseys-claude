# Casey's Claude Code Skills

Personal automation skills for [Claude Code](https://claude.ai/code). Skills are declarative markdown files that extend Claude's capabilities with domain-specific workflows.

## Installation

```bash
# Add marketplace
/plugin marketplace add caseyg/caseys-claude

# Install any skill (all skills install together)
/plugin install analyze-spending@caseys-claude
```

## Available skills

| Skill | Description |
|-------|-------------|
| **analyze-spending** | Financial analysis with LunchMoney API, subscription auditing |
| **book-fitness** | Chelsea Piers class booking via REST API with JWT caching |
| **coop-shift** | Park Slope Food Coop shift finder with browser automation |
| **not-ai** | Rewrite AI-sounding text into clear, natural plain language |
| **reorder-basics** | Amazon Buy Again automation with 1Password integration |
| **remarkable** | reMarkable tablet sync: upload/download docs, Morning Pages to Obsidian |
| **things-to-todoist** | Migrate tasks from Things 3 to Todoist |
| **timing-analysis** | Time tracking analysis from Timing App |
| **todoist-triage** | Inbox triage with duplicate detection and ADHD-friendly coaching |
| **tripit-export** | Export TripIt travel data to JSON |

## Dependencies

Different skills require different integrations:

- **1Password CLI** (`op`) - Secure credential storage for API keys and tokens
- **dev-browser** - Browser automation for sites without APIs
- **LunchMoney API** - Financial data for analyze-spending
- **rmapi-js** - reMarkable cloud API (TypeScript)
- **rmscene** - reMarkable `.rm` file parsing (Python: `uv pip install rmscene`)
- **Timing App API** - Time tracking data for timing-analysis
- **Todoist MCP** - Task management via `mcp__todoist__*` tools
- **Python** - For Things 3 export (`things.py`, `thefuzz`)

## Usage

Skills activate via natural language or slash commands:

- "Analyze my spending" or "Find subscriptions to cancel"
- "How did I spend my time this week?"
- "Reorder my Amazon basics"
- "Book yoga tomorrow at Chelsea Piers"
- "Find an available coop shift"
- "Sync my Morning Pages to Obsidian"
- "Upload this PDF to my reMarkable"
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
