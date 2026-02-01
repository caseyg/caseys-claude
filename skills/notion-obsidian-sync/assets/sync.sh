#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
NOTOMA_BIN="$DATA_DIR/notoma"
NOTOMA_SRC="$DATA_DIR/notoma-src"
CONFIG_TEMPLATE="$SKILL_DIR/assets/config.yaml"
RUNTIME_CONFIG="$DATA_DIR/config.yaml"

# Parse flags
FORCE=false
DRY_RUN=false
for arg in "$@"; do
  case "$arg" in
    --force)  FORCE=true ;;
    --dry-run) DRY_RUN=true ;;
    *) echo "Unknown flag: $arg"; exit 1 ;;
  esac
done

# Ensure data directory exists
mkdir -p "$DATA_DIR"

# 1. Retrieve Notion token from 1Password
echo "🔑 Retrieving Notion token from 1Password..."
NOTION_TOKEN="$(op item get "Notion" --fields "API Key" --reveal)"
if [[ -z "$NOTION_TOKEN" ]]; then
  echo "❌ Failed to retrieve Notion token. Verify 1Password item 'Notion' with field 'API Key'."
  exit 1
fi
export NOTION_TOKEN

# 2. Build notoma if not cached
if [[ ! -x "$NOTOMA_BIN" ]]; then
  echo "🔨 Building notoma..."
  if [[ ! -d "$NOTOMA_SRC" ]]; then
    git clone https://github.com/natikgadzhi/notoma.git "$NOTOMA_SRC"
  fi
  pushd "$NOTOMA_SRC" > /dev/null
  go build -o "$NOTOMA_BIN" .
  popd > /dev/null
  echo "✅ notoma built at $NOTOMA_BIN"
fi

# 3. Generate runtime config with absolute paths
VAULT_PATH="${HOME}/Obsidian/cag/Notion"
STATE_FILE="$DATA_DIR/notoma-state.json"
mkdir -p "$VAULT_PATH"

sed \
  -e "s|~/Obsidian/cag/Notion|${VAULT_PATH}|g" \
  -e "s|skills/notion-obsidian-sync/data/notoma-state.json|${STATE_FILE}|g" \
  "$CONFIG_TEMPLATE" > "$RUNTIME_CONFIG"

# 4. Handle --force (delete state to trigger full sync)
if $FORCE && [[ -f "$STATE_FILE" ]]; then
  echo "🔄 Force mode: removing state file for full re-sync"
  rm "$STATE_FILE"
fi

# 5. Run notoma sync
SYNC_ARGS=(sync --config "$RUNTIME_CONFIG")
if $DRY_RUN; then
  SYNC_ARGS+=(--dry-run)
fi

echo "📥 Running notoma sync..."
"$NOTOMA_BIN" "${SYNC_ARGS[@]}"

echo "✅ Sync complete. Output: $VAULT_PATH"
