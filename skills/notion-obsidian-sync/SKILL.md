---
name: notion-obsidian-sync
description: Sync Notion workspace to Obsidian vault using notoma. Use when the user asks to sync notion, import notion pages, export notion to obsidian, or back up notion to markdown.
metadata:
  version: 1.0.0
---

# Notion → Obsidian Sync

Incremental sync of your Notion workspace to Obsidian as Markdown, using [notoma](https://github.com/natikgadzhi/notoma) for conversion with .base files, attachments, and state tracking.

## Trigger Phrases

- "sync notion to obsidian"
- "import notion"
- "notion sync"
- "back up notion"
- "export notion to obsidian"
- "download my notion pages"

## Prerequisites

1. **Go 1.24+**: For building notoma from source
2. **1Password CLI**: Notion API token stored in item `Notion`, field `API Key`
3. **Obsidian Vault**: At `~/Obsidian/cag/` (output goes to `Notion/` subfolder)

### First-Time Setup

1. Create a Notion integration at https://www.notion.so/profile/integrations
2. Copy the Internal Integration Secret
3. Store it in 1Password: item `Notion`, field `API Key`
4. Share desired Notion pages/databases with the integration

## Quick Run

```bash
# Incremental sync (uses saved state)
bash skills/notion-obsidian-sync/assets/sync.sh

# Full re-sync (ignore state, re-download everything)
bash skills/notion-obsidian-sync/assets/sync.sh --force

# Preview without writing files
bash skills/notion-obsidian-sync/assets/sync.sh --dry-run
```

## Workflow

1. Retrieve Notion API token from 1Password (`op item get "Notion" --fields "API Key" --reveal`)
2. Build notoma if binary not cached in `data/notoma` (clone repo + `go build`)
3. Generate runtime config from `assets/config.yaml` with absolute paths
4. Run `data/notoma sync --config <runtime-config>`
5. Report results (pages synced, attachments downloaded, errors)

## Output

**Directory:** `~/Obsidian/cag/Notion/`

- Markdown files for each Notion page
- `_attachments/` subfolder for images and files
- State tracked in `data/notoma-state.json` for incremental sync

## Configuration

The config template lives at `assets/config.yaml`. The sync script copies it at runtime and resolves relative paths to absolute ones. Key settings:

| Setting | Value | Purpose |
|---------|-------|---------|
| `discover_workspace_roots` | `true` | Auto-discover all shared pages |
| `vault_path` | `~/Obsidian/cag/Notion` | Obsidian output directory |
| `attachment_folder` | `_attachments` | Subfolder for downloaded files |
| `download_attachments` | `true` | Fetch images and file blocks |

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `NOTION_TOKEN not set` | 1Password retrieval failed | Verify item `Notion` exists with field `API Key` |
| `go: command not found` | Go not installed | Install Go 1.24+ via `brew install go` |
| Build failure | Network or Go module issue | Delete `data/notoma-src/` and retry |
| `401 Unauthorized` | Token invalid or integration not shared | Re-check integration token and page sharing |
| State corruption | Interrupted sync | Delete `data/notoma-state.json` and run `--force` |

## Notes

- Binary and state files live in `data/` (gitignored via `**/data/` pattern)
- notoma is built from source once and cached; delete `data/notoma` to force rebuild
- The `--force` flag deletes the state file before syncing, triggering a full re-download
- Safe to run repeatedly — notoma's state tracking makes syncs incremental
