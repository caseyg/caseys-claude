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
version: 1.0.0
description: When to use this skill and what it does.
---

# Skill Title

## Trigger Phrases
## Prerequisites
## Workflow
## Error Handling
```

## Semantic Versioning

Skills use [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
  - Renamed/removed trigger phrases
  - Changed required prerequisites
  - Incompatible workflow changes
  - Removed features

- **MINOR** (1.0.0 → 1.1.0): New features, backwards compatible
  - New trigger phrases
  - New workflow steps
  - New optional parameters
  - Enhanced output formats

- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backwards compatible
  - Bug fixes
  - Documentation updates
  - Performance improvements
  - Dependency updates (non-breaking)

### Version Update Checklist

When modifying a skill:
1. Determine change type (breaking, feature, fix)
2. Update `version` in SKILL.md frontmatter
3. Document changes in commit message

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

## Deployment

When deploying changes to skills, follow this checklist:

### 1. Bump Version

For each modified skill, update the `version` field in `SKILL.md`:

```yaml
---
name: skill-name
version: 1.1.0  # Bump according to semantic versioning rules above
description: ...
---
```

### 2. Update README.md

If the change affects user-facing features:
- Update the skill description in the "Available skills" table
- Add new trigger phrases to the "Usage" section
- Document new dependencies if added

### 3. Update CHANGELOG.md

Add entry at the top with today's date:

```markdown
## Month Day, Year

### skill-name vX.Y.Z

- Brief description of changes
- New features added
- Bug fixes
```

Group multiple skill updates under the same date heading.

### 4. Validate

```bash
uvx --from skills-ref agentskills validate skills/<skill-name>
```

### 5. Commit and Push

```bash
git add -A
git commit -m "skill-name: Brief description of changes (vX.Y.Z)"
git push
```

### Quick Deploy Command

For simple changes, run all steps:

```bash
# After editing skill files, validate and deploy
uvx --from skills-ref agentskills validate skills/<skill-name> && \
git add -A && \
git commit -m "<skill-name>: <description> (vX.Y.Z)" && \
git push
```

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Code Skills Documentation](https://docs.claude.com/en/skills)
