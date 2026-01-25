# reMarkable Skill Preferences

User preferences for reMarkable document management.

## Default Settings

```yaml
# Default download location (relative to skill directory)
download_dir: data/downloads

# Include original PDF when downloading annotated documents
include_original: true

# Auto-render annotations after download
auto_render_annotations: true

# Default backup behavior
backup:
  include_original: false
  create_dated_folder: true
```

## Folder Preferences

```yaml
# Default folder for uploads (empty = root)
default_upload_folder: ""

# Folders to exclude from backup
exclude_from_backup: []
```

## Display Preferences

```yaml
# Show document hashes in list output
show_hashes: false

# Show full folder paths
show_full_paths: true
```

## Notes

- This file can be customized per-project by copying to `.claude/remarkable.local.md`
- Settings are read by Claude during skill execution
- YAML frontmatter is parsed for configuration values
