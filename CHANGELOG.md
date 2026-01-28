# Changelog

## January 26, 2026

### remarkable - CRDT Protocol Documentation

- **Added CRDT protocol documentation** (`references/CRDT_PROTOCOL.md`) - Comprehensive documentation of reMarkable's CRDT text synchronization protocol including:
  - CrdtId structure (author ID + sequence number)
  - CrdtSequenceItem for text blocks with left/right ID ordering
  - LwwValue (Last-Write-Wins) for paragraph styles
  - Paragraph style codes (PLAIN=1, HEADING=2, BULLET=4, NUMBERED=10, etc.)
  - Binary file format v6 structure
  - Operations: insert, append, delete text via CRDT

- **Added write-text POC** (`assets/scripts/write-text-poc.py`) - Proof-of-concept script for writing text to reMarkable documents using CRDT operations. Features:
  - List documents and pages from desktop app storage
  - Dry-run mode for safe testing
  - Author ID tracking (uses ID 2 to avoid conflicts with tablet's ID 1)
  - CRDT state persistence for sequence number continuity
  - Automatic backup before writes

### remarkable v1.3.1

- **Fixed default Obsidian path** - Changed from `~/Obsidian/vault/Daily` to `~/Obsidian/cag/Daily`

### remarkable v1.3.0

- **Fixed date detection for retrospective writing** - Now parses dates from content headings (e.g., "# 2026-01-24") instead of relying only on page modification timestamps. This correctly handles writing paper notes days later - content is filed to the date in the heading, not the date you typed it.

### remarkable v1.2.0

- **Fixed numbered list support** - Discovered reMarkable uses paragraph style code 10 for numbered lists (not 8-9 as guessed). Implemented monkey-patching of rmscene's `ParagraphStyle` enum to recognize style 10 before modules are loaded.

### remarkable v1.1.0

- **Numbered list support** - Morning Pages sync now converts numbered lists to Markdown (`1. 2. 3.` and nested `a. b. c.`).
- Added `NumberedListState` class for stateful list tracking
- Documented all supported Markdown formats in SKILL.md

### Repository

- Added semantic versioning guidelines to CLAUDE.md
- Added deployment checklist to CLAUDE.md

---

## January 25, 2026

### New Skills

- **remarkable** - reMarkable tablet integration via rmapi-js. Upload PDFs/EPUBs, download documents with annotations, backup notebooks, and sync Morning Pages to Obsidian. Features:
  - Device registration with 1Password token storage
  - List/search documents with caching
  - Upload PDF/EPUB to folders
  - Download with annotation rendering (Python/rmscene)
  - **Morning Pages sync**: Extracts typed text from `.rm` v6 format, converts reMarkable formatting (headers, bullets, checkboxes, bold) to Markdown, syncs to Obsidian Daily notes with intelligent merging

- **analyze-spending** - Financial analysis using LunchMoney API. Includes subscription auditing with 12-month transaction cross-referencing, spending by category, and an interactive interview mode to validate recurring charges and make cancellation decisions. Caches data locally with smart refresh thresholds.

- **timing-analysis** - Analyze time tracking data from the Timing App. Query by natural language periods ("today", "this week", "last month"), see project breakdowns, and generate time reports.

---

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
