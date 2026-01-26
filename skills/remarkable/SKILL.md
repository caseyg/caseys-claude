---
name: remarkable
version: 1.1.0
description: Manage reMarkable tablet documents - upload PDFs/EPUBs, download with annotations, backup notebooks, and list/search documents. Use when the user mentions reMarkable, wants to send files to their tablet, download annotated PDFs, or backup their notebooks.
---

# reMarkable Document Management

Upload, download, and manage documents on your reMarkable tablet via the cloud API.

## Trigger Phrases

- "upload [file] to remarkable"
- "send this PDF to my remarkable"
- "download [name] from remarkable"
- "get my annotated [document]"
- "backup my remarkable notebooks"
- "list my remarkable documents"
- "find [name] on remarkable"
- "register remarkable" (first-time setup)
- "sync morning pages to obsidian"
- "sync remarkable to obsidian"

## Prerequisites

1. **reMarkable Account**: Active reMarkable cloud sync (Connect subscription not required for basic sync)
2. **1Password CLI**: For secure token storage
3. **Node.js 18+**: For running TypeScript scripts with rmapi-js
4. **Python 3.9+** (optional): For annotation rendering

### First-Time Setup

Before using this skill, register the device:

1. Go to https://my.remarkable.com/device/browser/connect
2. Get the 8-character code displayed
3. Run the registration workflow (see Register Device section)
4. The device token is stored in 1Password item `Remarkable`, field `device_token`

## Dependencies

```bash
# Install rmapi-js for API access
npm install rmapi-js

# Install Python dependencies for annotation rendering (optional)
uv pip install rmscene PyMuPDF svgwrite
```

## Authentication

The reMarkable API uses a two-tier token system:

| Token Type | Lifetime | Storage |
|------------|----------|---------|
| Device Token | Permanent | 1Password `Remarkable.device_token` |
| User Token | 24 hours | Auto-refreshed by rmapi-js |

### Get Device Token from 1Password

```bash
op item get "Remarkable" --fields "device_token" --reveal
```

### Initialize API

```typescript
import { remarkable } from "rmapi-js";

// Get token from 1Password
const deviceToken = await $`op item get "Remarkable" --fields "device_token" --reveal`.text();

// Initialize API (handles user token refresh automatically)
const api = await remarkable(deviceToken.trim());
```

## Workflows

### 1. Register Device (First-Time Setup)

```typescript
import { register } from "rmapi-js";

// User provides 8-char code from my.remarkable.com/device/browser/connect
const code = "abcd1234"; // Get from user via AskUserQuestion

// Exchange code for permanent device token
const deviceToken = await register(code);

// Store in 1Password
await $`op item edit "Remarkable" "device_token=${deviceToken}"`;
// Or create if doesn't exist:
// await $`op item create --category="API Credential" --title="Remarkable" "device_token=${deviceToken}"`;

console.log("Registration complete! Device token stored in 1Password.");
```

### 2. List Documents

```typescript
import { remarkable } from "rmapi-js";

const deviceToken = await $`op item get "Remarkable" --fields "device_token" --reveal`.text();
const api = await remarkable(deviceToken.trim());

// Fetch all documents and folders
const items = await api.listItems();

// Build hierarchy
const folders = new Map();
const documents = [];

for (const item of items) {
  if (item.type === "CollectionType") {
    folders.set(item.id, { ...item, children: [] });
  } else {
    documents.push(item);
  }
}

// Organize documents into folders
for (const doc of documents) {
  const parent = doc.parent || "";
  if (parent && folders.has(parent)) {
    folders.get(parent).children.push(doc);
  }
}

// Display hierarchy
console.log("=== Root ===");
for (const doc of documents.filter(d => !d.parent || d.parent === "")) {
  console.log(`  📄 ${doc.visibleName} (${doc.hash.slice(0, 8)})`);
}

for (const [id, folder] of folders) {
  if (!folder.parent || folder.parent === "") {
    console.log(`\n📁 ${folder.visibleName}/`);
    for (const child of folder.children) {
      console.log(`  📄 ${child.visibleName}`);
    }
  }
}
```

### 3. Search Documents

```typescript
// Fuzzy search by name
function findDocuments(items, query) {
  const queryLower = query.toLowerCase();
  return items
    .filter(item => item.type !== "CollectionType")
    .filter(item => item.visibleName.toLowerCase().includes(queryLower))
    .sort((a, b) => {
      // Exact match first, then prefix match, then contains
      const aName = a.visibleName.toLowerCase();
      const bName = b.visibleName.toLowerCase();
      if (aName === queryLower) return -1;
      if (bName === queryLower) return 1;
      if (aName.startsWith(queryLower)) return -1;
      if (bName.startsWith(queryLower)) return 1;
      return aName.localeCompare(bName);
    });
}

const matches = findDocuments(items, "meeting notes");
if (matches.length === 0) {
  console.log("No documents found matching query");
} else if (matches.length === 1) {
  console.log(`Found: ${matches[0].visibleName}`);
} else {
  // Use AskUserQuestion to let user select
  console.log("Multiple matches found:");
  matches.forEach((m, i) => console.log(`${i + 1}. ${m.visibleName}`));
}
```

### 4. Upload PDF/EPUB

```typescript
import { remarkable } from "rmapi-js";
import { readFile } from "fs/promises";

const deviceToken = await $`op item get "Remarkable" --fields "device_token" --reveal`.text();
const api = await remarkable(deviceToken.trim());

// Read file from disk
const filePath = "/path/to/document.pdf";
const buffer = await readFile(filePath);
const fileName = filePath.split("/").pop().replace(/\.(pdf|epub)$/i, "");

// Detect file type from extension
const isPdf = filePath.toLowerCase().endsWith(".pdf");

// Upload to root (simple API - works with all schema versions)
let entry;
if (isPdf) {
  entry = await api.uploadPdf(fileName, new Uint8Array(buffer));
} else {
  entry = await api.uploadEpub(fileName, new Uint8Array(buffer));
}

console.log(`Uploaded: ${entry.visibleName} (hash: ${entry.hash})`);

// Alternative: Upload to specific folder using low-level API
// const folderId = "folder-uuid-here";
// entry = await api.putPdf(fileName, new Uint8Array(buffer), { parent: folderId });
```

### 5. Download Document (Raw ZIP)

```typescript
import { remarkable } from "rmapi-js";
import { writeFile, mkdir } from "fs/promises";

const deviceToken = await $`op item get "Remarkable" --fields "device_token" --reveal`.text();
const api = await remarkable(deviceToken.trim());

// Find document by name (use search workflow above)
const items = await api.listItems();
const doc = items.find(i => i.visibleName === "Target Document");

if (!doc) {
  throw new Error("Document not found");
}

// Download as ZIP archive (contains all .rm files, metadata, original PDF if applicable)
const zipData = await api.getDocument(doc.hash);

// Save to downloads directory
const today = new Date().toISOString().split("T")[0];
const downloadDir = `data/downloads/${today}`;
await mkdir(downloadDir, { recursive: true });

const safeName = doc.visibleName.replace(/[^a-zA-Z0-9-_]/g, "_");
const zipPath = `${downloadDir}/${safeName}.zip`;
await writeFile(zipPath, zipData);

console.log(`Downloaded: ${zipPath}`);

// Also get original PDF if it was a PDF document
try {
  const pdfData = await api.getPdf(doc.hash);
  const pdfPath = `${downloadDir}/${safeName}-original.pdf`;
  await writeFile(pdfPath, pdfData);
  console.log(`Original PDF: ${pdfPath}`);
} catch (e) {
  // Not a PDF document or no original available
  console.log("No original PDF available (may be a notebook)");
}
```

### 6. Download with Annotation Rendering

After downloading the raw ZIP:

```bash
# Extract ZIP
DOWNLOAD_DIR="data/downloads/2024-01-15"
DOC_NAME="Meeting_Notes"
unzip "${DOWNLOAD_DIR}/${DOC_NAME}.zip" -d "${DOWNLOAD_DIR}/${DOC_NAME}_extracted"

# Run annotation renderer (if .rm files exist)
python skills/remarkable/assets/scripts/render-annotations.py \
  "${DOWNLOAD_DIR}/${DOC_NAME}_extracted" \
  "${DOWNLOAD_DIR}/${DOC_NAME}-annotated.pdf"
```

**Python Annotation Rendering** (`render-annotations.py`):

```python
#!/usr/bin/env python3
"""Render reMarkable annotations onto PDF."""

import sys
import json
from pathlib import Path
from rmscene import read_blocks
from rmscene.scene_items import Line
import fitz  # PyMuPDF

# reMarkable display dimensions
RM_WIDTH = 1404
RM_HEIGHT = 1872

def extract_strokes(rm_path: Path) -> list:
    """Extract strokes from .rm file."""
    strokes = []
    with open(rm_path, "rb") as f:
        for block in read_blocks(f):
            if hasattr(block, "value") and isinstance(block.value, Line):
                line = block.value
                points = [(p.x, p.y, p.pressure) for p in line.points]
                strokes.append({
                    "points": points,
                    "color": getattr(line, "color", 0),
                    "thickness": getattr(line, "thickness_scale", 1.0),
                })
    return strokes

def render_to_pdf(extracted_dir: Path, output_pdf: Path):
    """Render annotations onto PDF pages."""
    extracted_dir = Path(extracted_dir)

    # Find original PDF
    pdf_files = list(extracted_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF found in archive - this may be a pure notebook")
        # For notebooks, create blank pages
        # ... (simplified for this example)
        return

    original_pdf = pdf_files[0]
    doc = fitz.open(original_pdf)

    # Find content file to map pages
    content_files = list(extracted_dir.glob("*.content"))
    page_mapping = {}
    if content_files:
        content = json.loads(content_files[0].read_text())
        # Map page UUIDs to PDF page numbers
        for i, page_id in enumerate(content.get("cPages", {}).get("pages", [])):
            page_uuid = page_id.get("id", "")
            page_mapping[page_uuid] = i

    # Find and render .rm files
    for rm_file in extracted_dir.rglob("*.rm"):
        page_uuid = rm_file.stem
        page_num = page_mapping.get(page_uuid, 0)

        if page_num >= len(doc):
            continue

        page = doc[page_num]
        rect = page.rect

        # Scale factors
        scale_x = rect.width / RM_WIDTH
        scale_y = rect.height / RM_HEIGHT

        strokes = extract_strokes(rm_file)
        for stroke in strokes:
            points = stroke["points"]
            if len(points) < 2:
                continue

            # Build path
            path_points = [(p[0] * scale_x, p[1] * scale_y) for p in points]

            # Draw stroke
            shape = page.new_shape()
            shape.draw_polyline(path_points)

            # Color mapping (simplified)
            color = (0, 0, 0)  # Black default
            if stroke["color"] == 1:
                color = (0.5, 0.5, 0.5)  # Gray
            elif stroke["color"] == 2:
                color = (1, 1, 1)  # White (eraser)

            shape.finish(color=color, width=stroke["thickness"])
            shape.commit()

    doc.save(output_pdf)
    doc.close()
    print(f"Rendered: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: render-annotations.py <extracted_dir> <output.pdf>")
        sys.exit(1)

    render_to_pdf(Path(sys.argv[1]), Path(sys.argv[2]))
```

### 7. Backup All Notebooks

```typescript
import { remarkable } from "rmapi-js";
import { writeFile, mkdir } from "fs/promises";

const deviceToken = await $`op item get "Remarkable" --fields "device_token" --reveal`.text();
const api = await remarkable(deviceToken.trim());

// Get all documents
const items = await api.listItems(true); // refresh to get latest
const documents = items.filter(i => i.type !== "CollectionType");

// Create backup directory
const today = new Date().toISOString().split("T")[0];
const backupDir = `data/downloads/${today}-backup`;
await mkdir(backupDir, { recursive: true });

console.log(`Backing up ${documents.length} documents to ${backupDir}`);

const manifest = {
  backupDate: new Date().toISOString(),
  documentCount: documents.length,
  documents: [],
};

for (const doc of documents) {
  try {
    const zipData = await api.getDocument(doc.hash);
    const safeName = doc.visibleName.replace(/[^a-zA-Z0-9-_]/g, "_");
    const filePath = `${backupDir}/${safeName}-${doc.hash.slice(0, 8)}.zip`;
    await writeFile(filePath, zipData);

    manifest.documents.push({
      name: doc.visibleName,
      hash: doc.hash,
      parent: doc.parent,
      file: filePath.split("/").pop(),
    });

    console.log(`  ✓ ${doc.visibleName}`);

    // Rate limiting
    await new Promise(r => setTimeout(r, 200));
  } catch (error) {
    console.error(`  ✗ ${doc.visibleName}: ${error.message}`);
    manifest.documents.push({
      name: doc.visibleName,
      hash: doc.hash,
      error: error.message,
    });
  }
}

// Save manifest
await writeFile(`${backupDir}/manifest.json`, JSON.stringify(manifest, null, 2));
console.log(`\nBackup complete: ${backupDir}/manifest.json`);
```

### 8. Sync Morning Pages to Obsidian

Automatically sync typed Morning Pages from reMarkable to Obsidian daily notes.

**Trigger phrases:**
- "sync morning pages to obsidian"
- "sync my morning pages"
- "update obsidian with remarkable notes"

**Features:**
- Automatically finds the latest "Morning Pages YYYY-MM" document
- Extracts typed text from each page with date detection
- Syncs to Obsidian Daily folder (configure via `OBSIDIAN_DAILY_PATH` env var)
- **Merge logic**: Appends `## Morning Pages` section to existing daily notes
- **Incremental sync**: Only processes new/changed content
- **Idempotent**: Safe to run multiple times

#### Quick Run

```bash
# From the skill directory
cd skills/remarkable

# Run sync (uses cached data if available)
python assets/scripts/sync-morning-pages.py

# Force re-download from reMarkable
python assets/scripts/sync-morning-pages.py --force

# Preview changes without writing
python assets/scripts/sync-morning-pages.py --dry-run
```

#### How It Works

1. **Find latest document**: Searches for documents matching "Morning Pages *"
2. **Download if needed**: Uses hash comparison to skip unchanged documents
3. **Extract text**: Parses .rm files using rmscene to get typed text
4. **Detect dates**: Uses page modification timestamps to determine dates
5. **Sync to Obsidian**:
   - If daily note exists with `## Morning Pages`: Update if content changed
   - If daily note exists without `## Morning Pages`: Append section
   - If no daily note: Create with default frontmatter

#### Obsidian Daily Note Format

New notes are created with this template:

```markdown
---
tags:
  - 🏷️/note/daily
---
## Notes

![[Daily.base]]

## Morning Pages

[Your typed text from reMarkable]
```

#### Configuration

Set custom Obsidian path via environment variable:

```bash
export OBSIDIAN_DAILY_PATH="/path/to/your/Obsidian/vault/Daily"
python assets/scripts/sync-morning-pages.py
```

Or edit `DEFAULT_OBSIDIAN_PATH` in the script.

#### Text Extraction Details

The reMarkable v6 format stores typed text in CRDT (Conflict-free Replicated Data Type) sequences. The sync script:

1. Reads `.content` file to get page metadata and modification timestamps
2. For each `.rm` file, parses the `SceneTree` structure
3. Extracts text from `root_text.items._items` which contains `CrdtSequenceItem` objects
4. Converts paragraph styles to Markdown formatting
5. Joins text fragments and organizes by date

**Supported Markdown Formatting:**
| reMarkable Style | Markdown Output |
|------------------|-----------------|
| Heading | `# Heading` |
| Bold | `**Bold text**` |
| Bullet list | `- Item` |
| Nested bullet | `  - Nested item` |
| Checkbox | `- [ ] Task` |
| Checked checkbox | `- [x] Done` |
| Numbered list | `1. First`, `2. Second` |
| Nested numbered | `   a. Sub-item`, `   b. Sub-item` |

**Note**: Handwritten content is NOT extracted (would require OCR). Only typed text from the reMarkable keyboard is synced. Numbered list support is future-proofed for when rmscene adds ParagraphStyle support (expected style values 8-9).

#### Caching

Downloaded documents are cached in `data/cache/` with hash-based validation:
- Cache hit: Skips download if hash matches
- `--force` flag: Bypasses cache and re-downloads

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `401 Unauthorized` | Device token invalid or revoked | Re-register device |
| `HashNotFoundError` | Document deleted/moved on device | Refresh document list with `listItems(true)` |
| `GenerationError` | Concurrent edit detected | Retry operation (rmapi-js usually auto-retries) |
| 1Password item not found | No device token stored | Run registration workflow |
| No .rm files in ZIP | Document has no annotations | Return original PDF only |
| rmscene parse error | Unsupported .rm format version | Return raw ZIP, warn user |

## Data Storage

```
skills/remarkable/data/           # Gitignored runtime data
├── cache/
│   └── documents.json            # Cached document list (5 min freshness)
└── downloads/
    └── YYYY-MM-DD/
        ├── Document_Name.zip      # Raw remarkable archive
        ├── Document_Name-original.pdf
        └── Document_Name-annotated.pdf
```

## API Quick Reference

| Method | Purpose |
|--------|---------|
| `register(code)` | Exchange 8-char code for device token |
| `remarkable(deviceToken)` | Create API instance (handles auth) |
| `api.listItems(refresh?)` | List all documents and folders |
| `api.uploadPdf(name, buffer)` | Upload PDF to root |
| `api.uploadEpub(name, buffer)` | Upload EPUB to root |
| `api.putPdf(name, buffer, opts)` | Upload PDF with options (folder target) |
| `api.getDocument(hash)` | Download full document as ZIP |
| `api.getPdf(hash)` | Get original PDF only |
| `api.getEpub(hash)` | Get original EPUB only |
| `api.getContent(hash)` | Get document content metadata |
| `api.getMetadata(hash)` | Get document metadata |

## Notes

- Device tokens never expire - store securely in 1Password
- User tokens expire in 24 hours but rmapi-js refreshes automatically
- The `uploadPdf`/`uploadEpub` methods use a simpler API that works with all schema versions
- For folder uploads, use `putPdf`/`putEpub` with `{ parent: folderId }` option
- Annotation rendering requires Python with rmscene - the .rm v6 format is complex
- reMarkable display resolution is 1404x1872 pixels
