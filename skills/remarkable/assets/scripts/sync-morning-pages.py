#!/usr/bin/env python3
"""
Sync Morning Pages from reMarkable to Obsidian.

This script:
1. Finds the latest "Morning Pages" document on reMarkable
2. Downloads it (or uses cached version if unchanged)
3. Extracts text from each page with date detection
4. Syncs to Obsidian Daily folder, merging with existing notes

Usage:
    python sync-morning-pages.py [--force] [--dry-run]

Options:
    --force    Re-download even if cached version exists
    --dry-run  Show what would be synced without making changes

Configuration:
    Set OBSIDIAN_DAILY_PATH environment variable or edit DEFAULT_OBSIDIAN_PATH below.
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Try to import rmscene - will fail gracefully if not installed
try:
    from rmscene import read_tree
    from rmscene.text import TextDocument
    from rmscene.scene_items import ParagraphStyle
    RMSCENE_AVAILABLE = True
except ImportError:
    RMSCENE_AVAILABLE = False
    print("Warning: rmscene not installed. Run: uv pip install rmscene")

# Configuration
# Override these with environment variables for your setup
DEFAULT_OBSIDIAN_PATH = Path(os.environ.get(
    "OBSIDIAN_DAILY_PATH",
    Path.home() / "Obsidian" / "vault" / "Daily"
))
CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "cache"
DOWNLOAD_DIR = Path(__file__).parent.parent.parent / "data" / "downloads"

# 1Password item name for reMarkable device token
# Override with OP_REMARKABLE_ITEM env var if you have naming conflicts
OP_ITEM_NAME = os.environ.get("OP_REMARKABLE_ITEM", "Remarkable")

# Default frontmatter for new daily notes
DEFAULT_FRONTMATTER = """---
tags:
  - 🏷️/note/daily
---
## Notes

![[Daily.base]]

"""


def get_device_token() -> str:
    """Get reMarkable device token from 1Password."""
    try:
        result = subprocess.run(
            ["op", "item", "get", OP_ITEM_NAME, "--fields", "device_token", "--reveal"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Could not get device token from 1Password")
        print("Run the registration script first.")
        sys.exit(1)


def extract_date_from_name(name: str) -> str:
    """Extract YYYY-MM date from Morning Pages name for sorting."""
    import re
    # Match patterns like "Morning Pages 2026-01" or "Morning pages 2025-11"
    match = re.search(r'(\d{4}-\d{2})', name)
    if match:
        return match.group(1)
    return "0000-00"  # Sort unknown dates first


def find_morning_pages_document(device_token: str) -> dict | None:
    """Find the latest Morning Pages document on reMarkable."""
    # Use the TypeScript list script to get documents
    result = subprocess.run(
        ["npx", "tsx", str(Path(__file__).parent / "list.ts"), "--json"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )

    if result.returncode != 0:
        print(f"Error listing documents: {result.stderr}")
        return None

    documents = json.loads(result.stdout)

    # Find documents matching "Morning Pages YYYY-MM" pattern (case-insensitive)
    morning_pages = []
    for doc in documents:
        name = doc.get("name", "")
        if name.lower().startswith("morning pages"):
            morning_pages.append(doc)

    if not morning_pages:
        print("No Morning Pages documents found")
        return None

    # Sort by extracted date (YYYY-MM) to get the latest month
    morning_pages.sort(key=lambda d: extract_date_from_name(d["name"]))
    latest = morning_pages[-1]

    print(f"Found: {latest['name']} (hash: {latest['hash'][:8]})")
    return latest


def download_document(doc: dict, force: bool = False) -> Path | None:
    """Download document if not already cached or if forced."""
    cache_file = CACHE_DIR / f"morning_pages_{doc['hash'][:16]}.json"
    download_path = DOWNLOAD_DIR / "morning_pages_latest"
    zip_path = download_path / f"{doc['hash'][:16]}.zip"
    extracted_path = download_path / "extracted"

    # Check if already downloaded
    if not force and cache_file.exists() and extracted_path.exists():
        cache_data = json.loads(cache_file.read_text())
        if cache_data.get("hash") == doc["hash"]:
            print(f"Using cached version (hash matches)")
            return extracted_path

    # Download fresh
    print(f"Downloading {doc['name']}...")
    download_path.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["npx", "tsx", str(Path(__file__).parent / "download.ts"),
         "--hash", doc["hash"], "--output", str(download_path)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )

    if result.returncode != 0:
        print(f"Error downloading: {result.stderr}")
        return None

    # Find and extract ZIP
    zip_files = list(download_path.glob("*.zip"))
    if not zip_files:
        print("Error: No ZIP file found after download")
        return None

    # Extract
    import zipfile
    if extracted_path.exists():
        import shutil
        shutil.rmtree(extracted_path)

    with zipfile.ZipFile(zip_files[0], 'r') as zf:
        zf.extractall(extracted_path)

    # Save cache metadata
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps({
        "hash": doc["hash"],
        "name": doc["name"],
        "downloaded": datetime.now().isoformat(),
    }))

    print(f"Extracted to {extracted_path}")
    return extracted_path


def style_to_markdown_prefix(style) -> tuple[str, str]:
    """
    Convert ParagraphStyle to Markdown prefix and suffix.

    Returns (prefix, suffix) tuple for wrapping the paragraph text.
    """
    if style == ParagraphStyle.HEADING:
        return "# ", ""
    elif style == ParagraphStyle.BOLD:
        return "**", "**"
    elif style == ParagraphStyle.BULLET:
        return "- ", ""
    elif style == ParagraphStyle.BULLET2:
        return "  - ", ""  # Nested bullet (indented)
    elif style == ParagraphStyle.CHECKBOX:
        return "- [ ] ", ""
    elif style == ParagraphStyle.CHECKBOX_CHECKED:
        return "- [x] ", ""
    else:
        # PLAIN, BASIC, or unknown - no prefix
        return "", ""


def is_list_style(style) -> bool:
    """Check if a paragraph style is a list item (bullet, checkbox)."""
    return style in (
        ParagraphStyle.BULLET,
        ParagraphStyle.BULLET2,
        ParagraphStyle.CHECKBOX,
        ParagraphStyle.CHECKBOX_CHECKED,
    )


def extract_text_from_rm(rm_file: Path) -> str:
    """
    Extract text content from a .rm file with proper Markdown formatting.

    Uses TextDocument.from_scene_item() to parse paragraph styles and
    converts them to Markdown syntax (headers, bullets, checkboxes, bold).

    Handles line spacing correctly:
    - Single newline between consecutive list items
    - Double newline between paragraphs
    - Double newline when transitioning between list and non-list content
    """
    if not RMSCENE_AVAILABLE:
        return ""

    try:
        with open(rm_file, 'rb') as f:
            tree = read_tree(f)

            if not tree.root_text:
                return ""

            # Use TextDocument for proper paragraph parsing with styles
            try:
                doc = TextDocument.from_scene_item(tree.root_text)

                result_lines = []
                prev_was_list = False

                for para in doc.contents:
                    text = str(para).strip()
                    if not text:
                        continue

                    # Get the paragraph style
                    style = para.style.value if para.style else ParagraphStyle.PLAIN
                    prefix, suffix = style_to_markdown_prefix(style)
                    curr_is_list = is_list_style(style)

                    # Apply Markdown formatting
                    formatted_line = f"{prefix}{text}{suffix}"

                    # Determine spacing
                    if result_lines:
                        if curr_is_list and prev_was_list:
                            # Consecutive list items: single newline
                            result_lines.append(formatted_line)
                        else:
                            # Transition or regular paragraphs: double newline
                            result_lines.append("")
                            result_lines.append(formatted_line)
                    else:
                        result_lines.append(formatted_line)

                    prev_was_list = curr_is_list

                return '\n'.join(result_lines)

            except Exception:
                # Fallback to raw CRDT extraction if TextDocument fails
                texts = []
                seq = tree.root_text.items
                if hasattr(seq, '_items'):
                    for item in seq._items.values():
                        if hasattr(item, 'value') and isinstance(item.value, str):
                            texts.append(item.value)
                return ''.join(texts)

    except Exception:
        # Silently fail on parse errors (common with newer format)
        return ""


def normalize_for_markdown(text: str) -> str:
    """
    Clean up Markdown text spacing.

    The new extraction code already handles proper spacing between
    list items and paragraphs, so this just cleans up edge cases.
    """
    import re

    # Remove excessive blank lines (3+ newlines → 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def extract_pages_with_dates(extracted_path: Path) -> dict[str, list[str]]:
    """Extract text from all pages, organized by date."""
    # Load content file to get page dates
    content_files = list(extracted_path.glob("*.content"))
    if not content_files:
        print("Error: No .content file found")
        return {}

    content = json.loads(content_files[0].read_text())

    # Build page -> date mapping
    page_dates = {}
    for page in content.get('cPages', {}).get('pages', []):
        page_id = page.get('id', '')
        modified_ms = int(page.get('modifed', 0))  # Note: reMarkable typo
        if modified_ms and page_id:
            date = datetime.fromtimestamp(modified_ms / 1000).strftime('%Y-%m-%d')
            page_dates[page_id] = date

    # Extract text from each .rm file
    day_texts = defaultdict(list)

    for rm_file in sorted(extracted_path.rglob('*.rm')):
        page_id = rm_file.stem
        date = page_dates.get(page_id, 'unknown')

        text = extract_text_from_rm(rm_file)
        if text.strip():
            # Normalize line breaks for Markdown
            text = normalize_for_markdown(text)
            day_texts[date].append(text)

    return dict(day_texts)


def sync_to_obsidian(day_texts: dict[str, list[str]], obsidian_path: Path, dry_run: bool = False) -> dict:
    """Sync extracted text to Obsidian daily notes."""
    stats = {"created": 0, "merged": 0, "skipped": 0}

    obsidian_path.mkdir(parents=True, exist_ok=True)

    for date in sorted(day_texts.keys()):
        if date == 'unknown':
            continue

        texts = day_texts[date]
        combined_text = '\n\n'.join(texts)

        obsidian_file = obsidian_path / f'{date}.md'

        if obsidian_file.exists():
            existing = obsidian_file.read_text()

            # Check if Morning Pages section already exists
            if '## Morning Pages' in existing:
                # Check if content is different (update detection)
                existing_mp_start = existing.find('## Morning Pages')
                existing_mp_section = existing[existing_mp_start:]

                # Simple hash comparison for changes
                existing_hash = hashlib.md5(existing_mp_section.encode()).hexdigest()[:8]
                new_hash = hashlib.md5(combined_text.encode()).hexdigest()[:8]

                if existing_hash == new_hash:
                    stats["skipped"] += 1
                    continue

                # Content changed - replace the entire Morning Pages section
                # Morning Pages is always the last section, so replace to end of file
                new_content = existing[:existing_mp_start] + '## Morning Pages\n\n' + combined_text + '\n'

                if not dry_run:
                    obsidian_file.write_text(new_content)
                print(f"  UPDATE {date} - Morning Pages content changed")
                stats["merged"] += 1
            else:
                # Append Morning Pages section
                new_content = existing.rstrip() + '\n\n## Morning Pages\n\n' + combined_text + '\n'
                if not dry_run:
                    obsidian_file.write_text(new_content)
                print(f"  MERGE {date} - Added Morning Pages section")
                stats["merged"] += 1
        else:
            # Create new daily note
            new_content = DEFAULT_FRONTMATTER + '## Morning Pages\n\n' + combined_text + '\n'
            if not dry_run:
                obsidian_file.write_text(new_content)
            print(f"  CREATE {date} - New daily note")
            stats["created"] += 1

    return stats


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sync Morning Pages from reMarkable to Obsidian")
    parser.add_argument("--force", action="store_true", help="Force re-download")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    args = parser.parse_args()

    # Get Obsidian path from env or default
    obsidian_path = Path(os.environ.get("OBSIDIAN_DAILY_PATH", DEFAULT_OBSIDIAN_PATH))

    if not RMSCENE_AVAILABLE:
        print("Error: rmscene required. Install with: uv pip install rmscene")
        sys.exit(1)

    print("=== Sync Morning Pages to Obsidian ===\n")

    # Step 1: Get device token
    print("1. Authenticating...")
    device_token = get_device_token()

    # Step 2: Find latest Morning Pages
    print("\n2. Finding latest Morning Pages...")
    doc = find_morning_pages_document(device_token)
    if not doc:
        sys.exit(1)

    # Step 3: Download if needed
    print("\n3. Downloading...")
    extracted_path = download_document(doc, force=args.force)
    if not extracted_path:
        sys.exit(1)

    # Step 4: Extract text
    print("\n4. Extracting text...")
    day_texts = extract_pages_with_dates(extracted_path)
    print(f"   Found {len(day_texts)} days with content")

    # Step 5: Sync to Obsidian
    print(f"\n5. Syncing to {obsidian_path}...")
    if args.dry_run:
        print("   (DRY RUN - no changes will be made)")

    stats = sync_to_obsidian(day_texts, obsidian_path, dry_run=args.dry_run)

    # Summary
    print(f"\n=== Summary ===")
    print(f"Created: {stats['created']}")
    print(f"Merged/Updated: {stats['merged']}")
    print(f"Skipped (unchanged): {stats['skipped']}")

    if args.dry_run:
        print("\n(Dry run - no changes were made)")


if __name__ == "__main__":
    main()
