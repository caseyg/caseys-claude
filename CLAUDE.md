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
- **Workflow**: Step-by-step implementation guide
- **Error Handling**: Common failure cases and recovery strategies

## Current Plugins

### reorder-basics
Amazon Buy Again automation using 1Password + dev-browser.

**Dependencies:**
- `op` command (1Password CLI): `brew install --cask 1password-cli`
- dev-browser plugin for browser automation

**Trigger phrases:** "reorder [item]", "buy [item] again", "/reorder-basics [item]"

## Key Integration Points

- **1Password CLI**: Secure credential retrieval via `op item get`
- **dev-browser plugin**: Browser automation with persistent state
- **AskUserQuestion**: User confirmation before purchases/destructive actions
