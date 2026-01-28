# reMarkable CRDT Protocol Documentation

This document describes the CRDT (Conflict-free Replicated Data Type) protocol used by reMarkable tablets and the desktop app for real-time text synchronization.

## Overview

reMarkable uses a **sequence CRDT** for text storage, allowing offline editing on multiple devices (tablet, desktop app, mobile) that automatically merge without conflicts when synced.

## Core Data Structures

### CrdtId (Unique Identifier)

Every character and operation has a unique identifier:

```
CrdtId = (part1: uint8, part2: varuint)
```

| Field | Type | Description |
|-------|------|-------------|
| `part1` | uint8 (0-255) | **Author ID** - identifies the device/user |
| `part2` | varuint | **Sequence number** - monotonically increasing per author |

**Special values:**
- `CrdtId(0, 0)` = END_MARKER (marks sequence boundaries)
- Author ID `1` = typically the tablet
- Author ID `2+` = desktop/other devices

### CrdtSequenceItem (Text Block)

Each text block in the sequence:

```python
@dataclass
class CrdtSequenceItem:
    item_id: CrdtId      # Unique ID (first char's ID for multi-char blocks)
    left_id: CrdtId      # What this comes AFTER (or END_MARKER)
    right_id: CrdtId     # What this comes BEFORE (or END_MARKER)
    deleted_length: int  # If > 0, this is a tombstone (deleted text)
    value: str | int     # Text content OR formatting code
```

### LwwValue (Last-Write-Wins)

Used for values where only the most recent change matters:

```python
@dataclass
class LwwValue[T]:
    timestamp: CrdtId  # When this value was set
    value: T           # The actual value
```

## Text Storage Model

### Character ID Assignment

When storing multi-character strings, each character gets an implicit ID:

| String | item_id | Character IDs |
|--------|---------|---------------|
| "Hello" | CrdtId(1, 100) | H=100, e=101, l=102, l=103, o=104 |

### Ordering via left_id/right_id

The sequence is ordered using a doubly-linked list structure:

```
[START] <-> [char A] <-> [char B] <-> [char C] <-> [END]
              ^            ^            ^
          left=START   left=A       left=B
          right=B      right=C      right=END
```

**Real example from Morning Pages:**
```
CrdtId(1, 15)  value='2026-01-19\nWent to bed...'
    left=CrdtId(0, 0)   # START marker
    right=CrdtId(0, 0)  # END marker (this was the only item)

CrdtId(1, 95)  value='A Jude Law movie '
    left=CrdtId(1, 94)  # After character 94
    right=CrdtId(0, 0)  # Before END
```

### Tombstones (Deletions)

Deleted text is represented as tombstones:

```python
CrdtSequenceItem(
    item_id=CrdtId(1, 75),
    left_id=CrdtId(1, 74),
    right_id=CrdtId(0, 0),
    deleted_length=17,  # 17 characters were deleted
    value=""            # Empty for tombstones
)
```

## Paragraph Styles

Paragraph styles are stored as LWW values keyed by the newline character's ID:

```python
text.styles = {
    CrdtId(1, 5513): LwwValue(
        timestamp=CrdtId(1, 5514),
        value=ParagraphStyle.BULLET2
    ),
    CrdtId(1, 5558): LwwValue(
        timestamp=CrdtId(1, 5561),
        value=ParagraphStyle.PLAIN
    ),
}
```

### Style Values

| Value | Name | Markdown |
|-------|------|----------|
| 0 | BASIC | (default) |
| 1 | PLAIN | Normal text |
| 2 | HEADING | `# Heading` |
| 3 | BOLD | `**text**` |
| 4 | BULLET | `- item` |
| 5 | BULLET2 | `  - nested` |
| 6 | CHECKBOX | `- [ ] task` |
| 7 | CHECKBOX_CHECKED | `- [x] done` |
| 10 | NUMBERED | `1. item` |
| 11 | NUMBERED2 | `   a. nested` |

### Inline Formatting

Bold and italic are stored as integer format codes in the sequence:

| Code | Meaning |
|------|---------|
| 1 | Bold ON |
| 2 | Bold OFF |
| 3 | Italic ON |
| 4 | Italic OFF |

## Binary File Format (v6)

### Header

```
"reMarkable .lines file, version=6" (44 bytes, padded with spaces)
```

### Tagged Block Structure

Each data element is prefixed with a tag:

```
Tag = (index << 4) | tag_type
```

| Tag Type | Value | Description |
|----------|-------|-------------|
| ID | 0x0F | CrdtId value |
| Length4 | 0x0C | Subblock with 4-byte length prefix |
| Byte8 | 0x08 | 8-byte value |
| Byte4 | 0x04 | 4-byte value |
| Byte1 | 0x01 | 1-byte value |

### Text Item Block (type 0x06)

```
[tag:1] parent_id: CrdtId
[tag:2] item_id: CrdtId
[tag:3] left_id: CrdtId
[tag:4] right_id: CrdtId
[tag:5] deleted_length: varuint
[tag:6] value: subblock (optional)
    - If string: UTF-8 encoded text
    - If format: uint8 format code
```

### Variable-Length Integer (varuint)

Used for sequence numbers and lengths:

```python
def read_varuint(stream):
    result = 0
    shift = 0
    while True:
        byte = stream.read(1)
        result |= (byte & 0x7F) << shift
        shift += 7
        if not (byte & 0x80):
            break
    return result
```

## Operations

### Insert Text

To insert "NEW" after character with ID `CrdtId(1, 50)`:

```python
new_item = CrdtSequenceItem(
    item_id=CrdtId(MY_AUTHOR, next_seq()),
    left_id=CrdtId(1, 50),      # Insert after this
    right_id=CrdtId(1, 51),     # Insert before this
    deleted_length=0,
    value="NEW"
)
tree.root_text.items.add(new_item)
```

### Append Text

To append to the end:

```python
last_id = get_last_character_id(tree.root_text.items)
new_item = CrdtSequenceItem(
    item_id=CrdtId(MY_AUTHOR, next_seq()),
    left_id=last_id,
    right_id=CrdtId(0, 0),  # END_MARKER
    deleted_length=0,
    value="\n\nAppended text here"
)
```

### Delete Text

Create a tombstone covering the deleted range:

```python
tombstone = CrdtSequenceItem(
    item_id=CrdtId(MY_AUTHOR, next_seq()),
    left_id=before_deleted_range,
    right_id=after_deleted_range,
    deleted_length=num_chars_to_delete,
    value=""
)
```

### Change Paragraph Style

Update the styles dictionary:

```python
newline_char_id = find_newline_before_paragraph(text)
text.styles[newline_char_id] = LwwValue(
    timestamp=CrdtId(MY_AUTHOR, next_seq()),
    value=ParagraphStyle.HEADING
)
```

## Conflict Resolution

The CRDT design ensures automatic conflict resolution:

1. **Unique IDs**: Each character has a globally unique (author, seq) ID
2. **Ordering**: `left_id`/`right_id` pointers establish relative position
3. **Timestamps**: LWW values use timestamps to resolve concurrent edits
4. **Tombstones**: Deletions are preserved, preventing "resurrection" bugs

### Example: Concurrent Edits

```
Initial: "Hello World"
         H(1,1) e(1,2) l(1,3) l(1,4) o(1,5) _(1,6) W(1,7)...

Tablet inserts "!" after "Hello":
  CrdtId(1, 20), left=(1,5), right=(1,6), value="!"

Desktop inserts "," after "Hello" simultaneously:
  CrdtId(2, 1), left=(1,5), right=(1,6), value=","

Result after merge: "Hello,! World" or "Hello!, World"
  (Deterministic based on author ID comparison)
```

## Desktop App Architecture

The reMarkable desktop app uses:

| Component | Technology |
|-----------|------------|
| UI Framework | Qt/QML |
| Real-time sync | MQTT (paho-mqtt) |
| Peer connection | WebRTC datachannel |
| Text operations | SceneController, SceneParticipant |

### Key Classes (from binary analysis)

- `SceneController::replaceText(QString, index, length, flags)`
- `SceneController::deleteText(MoveOperation)`
- `SceneParticipant::replaceComposeText(QString, index, ComposeState)`
- `CrdtTextItem` - CRDT-aware text item
- `SceneTextParagraphFormatAction` - paragraph formatting

## Local File Storage

Desktop app stores documents in:
```
~/Library/Containers/com.remarkable.desktop/Data/Library/Application Support/remarkable/desktop/
├── {UUID}/           # Document folder
│   └── {page-id}.rm  # Page data (binary, v6 format)
├── {UUID}.content    # Page list with CRDT timestamps
├── {UUID}.metadata   # Document name, dates
└── {UUID}.local      # Local sync state
```

## Implementation Notes

### Author ID Selection

- Avoid `0` (reserved for END_MARKER)
- Avoid `1` (typically used by tablet)
- Use `2-255` for custom implementations

### Sequence Number Tracking

Maintain a state file to track the last-used sequence number per author:

```json
{
  "author_id": 2,
  "last_sequence": 1547
}
```

### Triggering Sync

After modifying files:
1. Update `.content` file timestamps
2. The desktop app file watcher should detect changes
3. Or use the cloud API to push changes

## rmscene API Notes

The rmscene library provides these key functions:

```python
from rmscene import read_blocks, write_blocks
from rmscene.scene_stream import RootTextBlock

# Read all blocks from .rm file
with open("page.rm", "rb") as f:
    blocks = list(read_blocks(f))

# Find and modify the text block
for block in blocks:
    if isinstance(block, RootTextBlock):
        block.value.items.add(new_crdt_item)
        break

# Write all blocks back
with open("page.rm", "wb") as f:
    write_blocks(f, blocks)
```

**Note:** There is no `write_tree()` function. The library reads blocks into a SceneTree for convenience, but writing requires working with blocks directly.

## References

- [rmscene](https://github.com/ricklupton/rmscene) - Python library for reading/writing .rm files
- [rmapi-js](https://github.com/Ogdentrod/rmapi-js) - TypeScript API client
- [ddvk/remarkable-hacks](https://github.com/ddvk/remarkable-hacks) - Reverse engineering resources
