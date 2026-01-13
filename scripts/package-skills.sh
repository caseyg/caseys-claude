#!/usr/bin/env bash
# Package each skill into individual zip files in the repo root

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
DIST_DIR="$REPO_ROOT/dist"

# Ensure dist directory exists and is clean
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Package each skill directory (SKILL.md must be at top level of zip)
for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name="$(basename "$skill_dir")"
  (cd "$SKILLS_DIR" && zip -r "$DIST_DIR/${skill_name}.zip" "${skill_name}")
  echo "Created dist/${skill_name}.zip"
done

echo "Done. Packaged $(ls -1 "$DIST_DIR"/*.zip 2>/dev/null | wc -l | tr -d ' ') skills."
