---
name: orbital
description: Back up Orbital.nyc reflections (weekly logs, monthly logs, quarterly log reflections, and quarterly community updates with wins/lessons/intentions/talk) as Markdown to Obsidian. Use when the user asks to sync, back up, export, or archive Orbital reflections or logs.
metadata:
  version: 1.0.0
---

# Orbital Reflection Backup

Back up weekly, monthly, and quarterly reflections from Orbital.nyc to Obsidian as Markdown files. This covers two distinct Orbital features:

1. **Reflection Log Notes** — weekly, monthly, and quarterly private journal-style logs (`/log/weekly/`, `/log/monthly/`, `/log/quarterly/`)
2. **Quarterly Community Updates** — community-facing reflections with Wins, Lessons, Intentions, and Talk (`/member/updates/`)

**Important:** Only back up the authenticated user's own content. Never access other members' posts.

## Trigger Phrases

- "back up orbital"
- "sync orbital to obsidian"
- "export orbital reflections"
- "archive orbital logs"
- "download my orbital notes"

## Prerequisites

1. **Orbital.nyc Account**: Active membership with reflection log access
2. **1Password CLI**: Credentials stored in item `orbital.nyc` (ID: `y3bbe4uwhmgy4sha32vzdplqpa`, fields: `email`, `password`)
3. **Obsidian Vault**: At `~/Obsidian/cag/` (output goes to `Orbital/` subfolder)
4. **Python 3 + markdownify**: `pip install markdownify`

## Quick Run

```bash
# Incremental sync (skips unchanged notes)
python skills/orbital/assets/sync.py

# Full re-sync (ignore last_sync timestamp)
python skills/orbital/assets/sync.py --force
```

The script is idempotent — safe to run multiple times:

- **Log notes**: Skipped if `updatedAt` is before the last sync timestamp
- **Quarterly updates**: Skipped if file content hasn't changed
- **File writes**: Only write if content differs from existing file
- Sync timestamp stored in `~/Obsidian/cag/Orbital/.last_sync`

## Output

**Directory:** `~/Obsidian/cag/Orbital/`

| Type | Filename | Example |
|------|----------|---------|
| Weekly log | `{period}.md` | `2026-W03.md` |
| Monthly log | `{period}.md` | `2026-01.md` |
| Quarterly log | `{period}.md` | `2025-Q4.md` |
| Quarterly update | `{quarter}-update.md` | `2025-Q4-update.md` |

## Authentication

Orbital uses Supabase for authentication. The sync script handles this automatically:

1. Retrieves email/password from 1Password item `y3bbe4uwhmgy4sha32vzdplqpa`
2. POSTs to Supabase auth endpoint for a JWT access token (1-hour expiry)
3. Uses `Authorization: Bearer <token>` header on all API calls

### Supabase Auth Details

| Field | Value |
|-------|-------|
| Supabase URL | `https://avlgvxtubpfmwtyhvsis.supabase.co` |
| Anon Key | `sb_publishable_K-FozEyE7nhPRcNJ7Jjy3w_a7fVN0B6` |
| Auth Endpoint | `POST /auth/v1/token?grant_type=password` |
| Token Lifetime | 3600 seconds (1 hour) |

## API Reference

### 1. Reflection Log Notes

```
GET https://orbital.nyc/api/account/notes
Authorization: Bearer <supabase_jwt>
```

| Param | Required | Description |
|-------|----------|-------------|
| `span` | Yes | Number of days to look back (use `3650` for full archive) |
| `types` | Yes | Comma-separated: `weekly`, `monthly`, `quarterly` |
| `includeIncomplete` | No | `true`/`false` |
| `weekStartDay` | No | `1` = Monday |
| `timezone` | No | e.g. `America/New_York` |

Each note has a `noteContent` object:
- `default`: freeform HTML (used by weekly notes)
- `sections[]`: structured Q&A with `heading` and `content` HTML (used by monthly/quarterly)

### 2. Quarterly Community Updates

Three-step process: get member ID, get editions, get posts per edition.

**Get member ID:**
```
GET https://orbital.nyc/api/account/member → .member.id
```

**Get editions:**
```
GET https://orbital.nyc/api/networks/member/tasks/history
```
Editions stored as `1:Q4 2025` — strip `1:` prefix for queries.

**Get posts:**
```
GET https://orbital.nyc/api/networks/member/posts/user/{memberId}?type={type}&edition={edition}
```

Post types: `win`, `lesson`, `poll`

The `poll` type covers multiple sections, differentiated by `promptId`:

| promptId | Section | Description |
|----------|---------|-------------|
| (none) | Wins | `type=win` — separate type |
| `personal` | Lessons | Personal growth |
| `work` | Lessons | Work/project insights |
| `field` | Lessons | Industry observations |
| `change` | Intentions | Things to do differently |
| `sustain` | Intentions | Things to keep doing |
| `annual-reflection` | Intentions | Year-end reflection (Q4 only) |
| `rituals` | Intentions | Rituals and practices |
| `links` | Talk | Media recommendations |
| `questions` | Talk | Questions for community |
| `ask` | Talk | Asks/requests |
| `give` | Talk | Offers to community |
| `qol` | Talk | Quality of life tips |
| `feedback` | Talk | Meta feedback |

New promptIds may appear as Orbital evolves. The sync script handles unknown promptIds by title-casing them and placing them in an "Other" section.

Each post has: `id`, `type`, `authorId`, `lead` (headline), `body` (full text), `url` (optional link), `promptId`, `dateCreated`, `finalized`, `finalizedAt`.

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `401 Unauthorized` | Token expired or invalid | Script auto-authenticates each run |
| Empty notes array | No reflections in span | Increase `span` (default: 3650 days) |
| 1Password error | Missing credentials | Verify item `y3bbe4uwhmgy4sha32vzdplqpa` exists |
| `markdownify` missing | Python dependency | `pip install markdownify` |
| Unknown `promptId` | Orbital added new question | Captured in "Other" section automatically |

## Notes

- Only the authenticated user's own content is accessed — member ID comes from `/api/account/member`
- All API endpoints return redirects; the script follows them automatically
- Weekly notes use freeform `default` HTML; monthly/quarterly log notes use structured `sections`
- Quarterly community updates are a separate system from log notes
- Older editions (e.g., Q2 2025) may have `null` promptIds on lessons — handled as uncategorized
- Use 1Password item ID `y3bbe4uwhmgy4sha32vzdplqpa` (not name) to avoid ambiguity
- Supabase anon key is a publishable client key (safe to include)
