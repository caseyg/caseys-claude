# Changelog

## January 13, 2026

### Repository Restructure

Simplified repo structure following the [Agent Skills Specification](https://agentskills.io/specification).

**Structure changes:**
- Flattened `plugins/<name>/.claude-plugin/skills/<name>/` → `skills/<name>/`
- Moved plugin metadata from JSON files to YAML frontmatter in SKILL.md
- Added `assets/` directory for supplementary files per spec
- Single `.claude-plugin/` for marketplace compatibility

**New skill:**
- **not-ai** - Rewrites AI-sounding text into clear, natural plain language

**Development:**
- Added pre-commit hook with skills-ref validation via `uvx`
- Updated all Python install instructions to use `uv pip`

**Documentation:**
- Added spec references to CLAUDE.md
- Updated README with marketplace install commands

---

## January 8, 2026

### Security & Privacy

Scrubbed PII from repo and git history before public release. Demo data now uses placeholder names, IDs, and paths.

### New Features

**Todoist Triage Skill**
- SQLite-backed sync for local queries
- Duplicate detection (exact + fuzzy via `thefuzz`)
- Stale task finder (60+ days, no due date)
- Missing metadata alerts
- Project suggestions based on keywords
- Learns from decisions via `TRIAGE_MEMORY.md`

**Temporal Clustering & Pattern Discovery**
- Groups tasks created within 10-minute windows
- Extracts people names, concepts, action verbs
- Learns work/personal context from user answers
- Detects action patterns (e.g., "Call X" → `@phone` label)
- Persists learned rules for future sessions

**EF/ADHD Coaching**
- Task sizing: quick wins, large tasks, automation candidates
- SMART criteria scoring
- Task breakdown coaching with subtask creation
- Automation suggestions for repetitive tasks

### Documentation

Updated `CLAUDE.md` with plugin table, dependencies, and API patterns.

---

## January 1, 2026

### New Features

**Three new automation skills shipped today!**

- **reorder-basics** - Amazon Buy Again automation using browser automation + 1Password. Never manually reorder toilet paper again.

- **book-fitness** - Chelsea Piers class booking via direct API. JWT token caching, 24h advance booking logic, all 3 NYC locations supported.

- **coop-shift** - Park Slope Food Coop shift finder. Browser automation for the server-rendered Django site. Filter by job type, auto-fill initials, credit shifts to housemates.

### Other Improvements

- **Repo infrastructure** - Added `marketplace.json` plugin registry, `.gitignore`, and `CLAUDE.md` documentation.
