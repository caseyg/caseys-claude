#!/usr/bin/env python3
"""
Proof-of-concept: Write text to a reMarkable document using CRDT operations.

This script demonstrates how to append text to an existing reMarkable page
by creating valid CRDT sequence items.

Usage:
    python write-text-poc.py <document_uuid> <page_uuid> "Text to append"
    python write-text-poc.py --list  # List available documents
    python write-text-poc.py --dry-run <doc> <page> "Text"  # Preview without writing

Requirements:
    - rmscene library: uv pip install rmscene
    - Access to reMarkable desktop app's local storage

WARNING: This is experimental. Always backup your documents first!
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# rmscene imports
try:
    from rmscene import read_blocks, write_blocks
    from rmscene.scene_stream import RootTextBlock
    from rmscene.scene_items import Text, ParagraphStyle
    from rmscene.crdt_sequence import CrdtSequence, CrdtSequenceItem
    from rmscene.tagged_block_common import CrdtId, LwwValue
except ImportError:
    print("Error: rmscene not installed. Run: uv pip install rmscene")
    sys.exit(1)


# Configuration
DESKTOP_DATA_DIR = Path.home() / "Library/Containers/com.remarkable.desktop/Data/Library/Application Support/remarkable/desktop"
STATE_FILE = Path(__file__).parent.parent.parent / "data" / "crdt_state.json"

# Use author ID 2 (tablet typically uses 1)
DEFAULT_AUTHOR_ID = 2


@dataclass
class CrdtState:
    """Track CRDT state for generating new IDs."""
    author_id: int
    last_sequence: int

    def next_id(self) -> CrdtId:
        """Generate the next CrdtId and increment counter."""
        self.last_sequence += 1
        return CrdtId(self.author_id, self.last_sequence)

    def save(self, path: Path):
        """Save state to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "author_id": self.author_id,
            "last_sequence": self.last_sequence,
            "updated": datetime.now().isoformat()
        }, indent=2))

    @classmethod
    def load(cls, path: Path, author_id: int = DEFAULT_AUTHOR_ID) -> "CrdtState":
        """Load state from JSON file or create new."""
        if path.exists():
            data = json.loads(path.read_text())
            return cls(
                author_id=data.get("author_id", author_id),
                last_sequence=data.get("last_sequence", 0)
            )
        return cls(author_id=author_id, last_sequence=0)


def list_documents() -> list[dict]:
    """List all documents in the desktop app's local storage."""
    documents = []

    if not DESKTOP_DATA_DIR.exists():
        print(f"Desktop data directory not found: {DESKTOP_DATA_DIR}")
        return documents

    for metadata_file in DESKTOP_DATA_DIR.glob("*.metadata"):
        doc_id = metadata_file.stem
        try:
            metadata = json.loads(metadata_file.read_text())
            doc_folder = DESKTOP_DATA_DIR / doc_id
            page_count = len(list(doc_folder.glob("*.rm"))) if doc_folder.exists() else 0

            documents.append({
                "id": doc_id,
                "name": metadata.get("visibleName", "Unknown"),
                "type": metadata.get("type", "Unknown"),
                "pages": page_count,
                "modified": metadata.get("lastModified", "")
            })
        except Exception as e:
            print(f"  Error reading {doc_id}: {e}")

    return sorted(documents, key=lambda d: d.get("modified", ""), reverse=True)


def list_pages(doc_id: str) -> list[dict]:
    """List pages in a document."""
    content_file = DESKTOP_DATA_DIR / f"{doc_id}.content"
    doc_folder = DESKTOP_DATA_DIR / doc_id

    if not content_file.exists():
        return []

    content = json.loads(content_file.read_text())
    pages = []

    for page in content.get("cPages", {}).get("pages", []):
        page_id = page.get("id", "")
        rm_file = doc_folder / f"{page_id}.rm"

        pages.append({
            "id": page_id,
            "exists": rm_file.exists(),
            "size": rm_file.stat().st_size if rm_file.exists() else 0,
            "template": page.get("template", {}).get("value", "Unknown")
        })

    return pages


def get_last_item_id(items: CrdtSequence) -> CrdtId:
    """Get the ID of the last character in the sequence."""
    sequence_items = items.sequence_items()
    if not sequence_items:
        return CrdtId(0, 0)  # END_MARKER

    # Find the last non-deleted item
    last_item = None
    for item in sequence_items:
        if item.deleted_length == 0 and item.value:
            last_item = item

    if last_item is None:
        return CrdtId(0, 0)

    # The last character's ID is item_id + len(value) - 1
    if isinstance(last_item.value, str) and len(last_item.value) > 0:
        return CrdtId(
            last_item.item_id.part1,
            last_item.item_id.part2 + len(last_item.value) - 1
        )
    return last_item.item_id


def append_text_to_page(
    rm_path: Path,
    text: str,
    state: CrdtState,
    dry_run: bool = False
) -> bool:
    """
    Append text to an existing reMarkable page.

    Args:
        rm_path: Path to the .rm file
        text: Text to append
        state: CRDT state for generating IDs
        dry_run: If True, don't actually write

    Returns:
        True if successful
    """
    if not rm_path.exists():
        print(f"Error: File not found: {rm_path}")
        return False

    # Backup the original file
    backup_path = rm_path.with_suffix(".rm.backup")
    if not dry_run:
        shutil.copy(rm_path, backup_path)
        print(f"  Backup created: {backup_path.name}")

    # Read all blocks from the file
    with open(rm_path, "rb") as f:
        blocks = list(read_blocks(f))

    # Find the RootTextBlock
    root_text_block = None
    for block in blocks:
        if isinstance(block, RootTextBlock):
            root_text_block = block
            break

    if root_text_block is None:
        print("Error: Page has no text block. Cannot append to drawing-only pages.")
        return False

    # Get the last character ID from the text items
    last_id = get_last_item_id(root_text_block.value.items)
    print(f"  Last character ID: {last_id}")

    # Create new CRDT item for the appended text
    new_item_id = state.next_id()

    # Prepend newlines if text doesn't start with one (to separate from existing)
    if not text.startswith("\n"):
        text = "\n\n" + text

    new_item = CrdtSequenceItem(
        item_id=new_item_id,
        left_id=last_id,
        right_id=CrdtId(0, 0),  # END_MARKER
        deleted_length=0,
        value=text
    )

    print(f"  New item ID: {new_item_id}")
    print(f"  Text to append: {repr(text[:50])}{'...' if len(text) > 50 else ''}")

    if dry_run:
        print("\n  [DRY RUN] Would append text but not writing.")
        return True

    # Add the new item to the text sequence
    root_text_block.value.items.add(new_item)

    # Write all blocks back to file
    with open(rm_path, "wb") as f:
        write_blocks(f, blocks)

    print(f"  Successfully wrote to: {rm_path.name}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Write text to a reMarkable document (proof-of-concept)"
    )
    parser.add_argument("--list", action="store_true", help="List available documents")
    parser.add_argument("--pages", metavar="DOC_ID", help="List pages in a document")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--author-id", type=int, default=DEFAULT_AUTHOR_ID,
                        help=f"CRDT author ID (default: {DEFAULT_AUTHOR_ID})")
    parser.add_argument("doc_id", nargs="?", help="Document UUID")
    parser.add_argument("page_id", nargs="?", help="Page UUID")
    parser.add_argument("text", nargs="?", help="Text to append")

    args = parser.parse_args()

    if args.list:
        print("=== Available Documents ===\n")
        documents = list_documents()
        for doc in documents[:20]:
            print(f"  {doc['name']}")
            print(f"    ID: {doc['id']}")
            print(f"    Pages: {doc['pages']}, Type: {doc['type']}")
            print()
        return

    if args.pages:
        print(f"=== Pages in Document ===\n")
        pages = list_pages(args.pages)
        for i, page in enumerate(pages):
            status = "OK" if page['exists'] else "MISSING"
            print(f"  [{i}] {page['id']}")
            print(f"      Status: {status}, Size: {page['size']} bytes")
            print(f"      Template: {page['template']}")
            print()
        return

    if not all([args.doc_id, args.page_id, args.text]):
        parser.print_help()
        print("\nExamples:")
        print("  python write-text-poc.py --list")
        print("  python write-text-poc.py --pages <doc-uuid>")
        print("  python write-text-poc.py --dry-run <doc-uuid> <page-uuid> 'Hello World'")
        return

    # Load CRDT state
    state = CrdtState.load(STATE_FILE, args.author_id)
    print(f"=== Writing Text to reMarkable ===")
    print(f"  Author ID: {state.author_id}")
    print(f"  Starting sequence: {state.last_sequence}")

    # Build path to .rm file
    rm_path = DESKTOP_DATA_DIR / args.doc_id / f"{args.page_id}.rm"

    # Append text
    success = append_text_to_page(rm_path, args.text, state, dry_run=args.dry_run)

    if success and not args.dry_run:
        state.save(STATE_FILE)
        print(f"\n  State saved. New sequence: {state.last_sequence}")
        print("\n  NOTE: Restart the reMarkable desktop app to see changes,")
        print("        or wait for automatic sync.")


if __name__ == "__main__":
    main()
