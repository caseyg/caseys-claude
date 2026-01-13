# Casey's Claude Code Skills

A collection of personal automation plugins for [Claude Code](https://claude.ai/code). Skills are declarative (defined in markdown) and extend Claude's capabilities with domain-specific workflows.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| **reorder-basics** | Amazon Buy Again automation with 1Password integration |
| **book-fitness** | Chelsea Piers class booking via REST API with JWT caching |
| **coop-shift** | Park Slope Food Coop shift finder with browser automation |
| **tripit-export** | Export TripIt travel data to JSON |
| **things-to-todoist** | Migrate tasks from Things 3 to Todoist |
| **todoist-triage** | Inbox triage with duplicate detection, stale task cleanup, and ADHD-friendly coaching |
| **not-ai** | Rewrite AI-sounding text into clear, natural plain language |

## Dependencies

Different plugins require different integrations:

- **1Password CLI** (`op`) - Secure credential storage
- **dev-browser** - Browser automation for sites without APIs
- **Todoist MCP** - Task management via `mcp__todoist__*` tools
- **Python** - For Things 3 export (`things.py`, `thefuzz`)

## Usage

Skills activate via natural language or slash commands. Examples:

- "Reorder my Amazon basics"
- "Book yoga tomorrow at Chelsea Piers"
- "Find an available coop shift"
- "Triage my Todoist inbox"

## Repository Structure

```
.claude-plugin/marketplace.json    # Plugin registry
plugins/
  <plugin-name>/
    .claude-plugin/plugin.json     # Plugin metadata
    skills/
      <skill-name>/
        SKILL.md                   # Skill implementation
```

## Creating New Plugins

See [CLAUDE.md](./CLAUDE.md) for detailed guidance on creating plugins and writing SKILL.md files.

## License

Personal use. Skills contain hardcoded assumptions (locations, accounts, preferences) that you'd need to adapt for your own use.
