# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code personal skills repository** - a collection of automation plugins that extend Claude Code's functionality. Skills are declarative (defined in markdown), not compiled code.

## Repository Structure

```
.claude-plugin/marketplace.json    # Plugin registry - lists all available plugins
plugins/
  <plugin-name>/
    .claude-plugin/plugin.json     # Plugin metadata (name, version, description)
    skills/
      <skill-name>/
        SKILL.md                   # Skill implementation guide
```

## Creating New Plugins

1. Create a new directory under `plugins/`
2. Add `.claude-plugin/plugin.json` with name, description, version
3. Add skills under `skills/<skill-name>/SKILL.md`
4. Register the plugin in `.claude-plugin/marketplace.json`

Use the `compound-engineering:create-agent-skill` skill for guided plugin creation.

## SKILL.md Structure

A skill file should include:
- **Description**: When to use this skill
- **Trigger Phrases**: Natural language or `/slash-command` invocations
- **Prerequisites**: Required tools (1Password CLI, dev-browser, etc.)
- **Workflow**: Step-by-step implementation guide with code examples
- **API Reference**: Endpoints, request/response formats (if applicable)
- **Error Handling**: Common failure cases and recovery strategies

## Current Plugins

| Plugin | Description | Dependencies |
|--------|-------------|--------------|
| `reorder-basics` | Amazon Buy Again automation | 1Password CLI, dev-browser |
| `book-fitness` | Chelsea Piers class booking via REST API | 1Password CLI |
| `coop-shift` | Park Slope Food Coop shift booking | dev-browser |
| `tripit-export` | Export TripIt travel data to JSON | dev-browser |
| `things-to-todoist` | Migrate Things 3 tasks to Todoist | Todoist MCP, Python (things.py, thefuzz) |

## Key Integration Points

- **1Password CLI**: Secure credential retrieval via `op item get`. Cache tokens in 1Password with `op item edit`.
- **dev-browser plugin**: Browser automation with persistent state. Start with `./server.sh`, connect via `@/client.js`.
- **Todoist MCP**: Use `mcp__todoist__*` tools for task management with built-in rate limiting.
- **AskUserQuestion**: User confirmation before purchases/destructive actions. Batch multiple questions in one call.
