# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code personal skills repository** - a collection of automation skills that extend Claude Code's functionality. Skills are declarative markdown files with YAML frontmatter for metadata.

## Repository Structure

```
skills/
  <skill-name>/
    SKILL.md                   # Skill definition with YAML frontmatter
    assets/                    # Optional supplementary files (templates, configs)
```

## SKILL.md Format

Each skill has a SKILL.md with YAML frontmatter:

```yaml
---
name: skill-name
description: When to use this skill and what it does.
---

# Skill Title

## Trigger Phrases
## Prerequisites
## Workflow
## Error Handling
```

## Creating New Skills

1. Create a new directory under `skills/`
2. Add `SKILL.md` with YAML frontmatter containing `name` and `description`
3. Validate with `uvx --from skills-ref agentskills validate skills/<skill-name>`

Use the `compound-engineering:create-agent-skill` skill for guided skill creation.

## Key Integration Points

- **1Password CLI**: Credential retrieval via `op item get`, token caching via `op item edit`
- **dev-browser plugin**: Browser automation with persistent state for sites without APIs
- **Todoist MCP**: Task management via `mcp__todoist__*` tools with built-in rate limiting
- **AskUserQuestion**: User confirmation before purchases/destructive actions

## Development

```bash
# Validate all skills
uvx --from skills-ref agentskills validate skills/

# Validate single skill
uvx --from skills-ref agentskills validate skills/<skill-name>

# Package all skills as individual zips (for Claude desktop import)
./scripts/package-skills.sh

# Install pre-commit hooks
pre-commit install

# Install Python dependencies (for things-to-todoist, todoist-triage)
uv pip install things.py thefuzz python-Levenshtein
```

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Code Skills Documentation](https://docs.claude.com/en/skills)
