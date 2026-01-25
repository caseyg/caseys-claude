#!/usr/bin/env python3
"""
Render reMarkable annotations onto PDF pages.

This script takes an extracted reMarkable document archive and overlays
the handwritten annotations (.rm files) onto the original PDF.

Usage:
    python render-annotations.py <extracted_dir> <output.pdf>

Example:
    unzip Document.zip -d Document_extracted
    python render-annotations.py Document_extracted Document-annotated.pdf

Requirements:
    uv pip install rmscene PyMuPDF svgwrite

The .rm file format (v6) is parsed using the rmscene library.
Strokes are rendered as vector paths and overlaid onto PDF pages.
"""

import sys
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

try:
    from rmscene import read_blocks
    from rmscene.scene_items import Line
except ImportError:
    print("Error: rmscene not installed. Run: uv pip install rmscene")
    sys.exit(1)

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: uv pip install PyMuPDF")
    sys.exit(1)


# reMarkable display dimensions (pixels)
RM_WIDTH = 1404
RM_HEIGHT = 1872

# Pen type to color mapping (simplified)
# 0=Black, 1=Gray, 2=White (eraser)
COLOR_MAP = {
    0: (0, 0, 0),        # Black
    1: (0.5, 0.5, 0.5),  # Gray
    2: (1, 1, 1),        # White (for eraser)
}

# Pen types
PEN_TYPES = {
    0: "brush",
    2: "ballpoint",
    4: "fineliner",
    5: "highlighter",
    6: "eraser",
    7: "mechanical_pencil",
    21: "calligraphy",
}


@dataclass
class Stroke:
    """A single stroke from the .rm file."""
    points: list[tuple[float, float, float]]  # (x, y, pressure)
    color: int
    thickness: float
    pen_type: int


def extract_strokes(rm_path: Path) -> list[Stroke]:
    """
    Extract strokes from a .rm file.

    The rmscene library parses the v6 binary format which uses
    a block-based structure with CRDT support.
    """
    strokes = []

    try:
        with open(rm_path, "rb") as f:
            for block in read_blocks(f):
                # Look for Line objects which contain stroke data
                if hasattr(block, "value") and isinstance(block.value, Line):
                    line = block.value
                    points = []

                    for p in line.points:
                        # Points have x, y, and various attributes
                        x = getattr(p, "x", 0)
                        y = getattr(p, "y", 0)
                        pressure = getattr(p, "pressure", 0.5)
                        points.append((x, y, pressure))

                    if points:
                        strokes.append(Stroke(
                            points=points,
                            color=getattr(line, "color", 0),
                            thickness=getattr(line, "thickness_scale", 1.0),
                            pen_type=getattr(line, "tool", 0),
                        ))
    except Exception as e:
        print(f"Warning: Failed to parse {rm_path}: {e}")

    return strokes


def load_content_mapping(extracted_dir: Path) -> dict[str, int]:
    """
    Load page UUID to page number mapping from .content file.

    The .content file maps page UUIDs (used in .rm filenames)
    to their position in the PDF.
    """
    mapping = {}

    content_files = list(extracted_dir.glob("*.content"))
    if not content_files:
        return mapping

    try:
        content = json.loads(content_files[0].read_text())

        # Handle different content file formats
        if "cPages" in content and "pages" in content["cPages"]:
            # Newer format with cPages structure
            for i, page in enumerate(content["cPages"]["pages"]):
                page_id = page.get("id", "")
                if page_id:
                    mapping[page_id] = i
        elif "pages" in content:
            # Older format with direct pages array
            for i, page_id in enumerate(content["pages"]):
                if page_id:
                    mapping[page_id] = i

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Warning: Failed to parse content file: {e}")

    return mapping


def find_original_pdf(extracted_dir: Path) -> Optional[Path]:
    """Find the original PDF in the extracted archive."""
    pdf_files = list(extracted_dir.glob("*.pdf"))
    if pdf_files:
        return pdf_files[0]
    return None


def render_strokes_to_page(page: fitz.Page, strokes: list[Stroke]) -> None:
    """Render strokes onto a PDF page."""
    rect = page.rect

    # Calculate scale factors from reMarkable coordinates to PDF
    scale_x = rect.width / RM_WIDTH
    scale_y = rect.height / RM_HEIGHT

    for stroke in strokes:
        if len(stroke.points) < 2:
            continue

        # Skip eraser strokes (they should erase, not draw)
        if stroke.pen_type == 6:
            continue

        # Convert points to PDF coordinates
        pdf_points = [
            fitz.Point(p[0] * scale_x, p[1] * scale_y)
            for p in stroke.points
        ]

        # Get color
        color = COLOR_MAP.get(stroke.color, (0, 0, 0))

        # Calculate stroke width (pressure-sensitive would be complex)
        width = max(0.5, stroke.thickness * 1.5)

        # For highlighter, use transparency
        if stroke.pen_type == 5:
            color = (1, 1, 0)  # Yellow
            # PyMuPDF doesn't support transparency easily, so we'll just use yellow

        # Draw the stroke as a polyline
        shape = page.new_shape()
        shape.draw_polyline(pdf_points)
        shape.finish(
            color=color,
            width=width,
            lineCap=1,  # Round caps
            lineJoin=1,  # Round joins
        )
        shape.commit()


def create_blank_notebook(num_pages: int, output_path: Path) -> fitz.Document:
    """Create a blank PDF for pure notebooks (no original PDF)."""
    doc = fitz.open()

    # A4-ish dimensions matching reMarkable aspect ratio
    width = 595  # A4 width in points
    height = width * (RM_HEIGHT / RM_WIDTH)

    for _ in range(num_pages):
        doc.new_page(width=width, height=height)

    return doc


def render_to_pdf(extracted_dir: Path, output_path: Path) -> None:
    """
    Main rendering function.

    1. Find original PDF (or create blank pages for notebooks)
    2. Load page mapping from .content file
    3. Find all .rm files and extract strokes
    4. Render strokes onto corresponding PDF pages
    5. Save the result
    """
    extracted_dir = Path(extracted_dir)
    output_path = Path(output_path)

    # Find .rm files
    rm_files = list(extracted_dir.rglob("*.rm"))
    if not rm_files:
        print("No .rm files found - document has no annotations")
        # Just copy the original PDF if it exists
        original = find_original_pdf(extracted_dir)
        if original:
            import shutil
            shutil.copy(original, output_path)
            print(f"Copied original PDF to: {output_path}")
        return

    print(f"Found {len(rm_files)} page(s) with annotations")

    # Load page mapping
    page_mapping = load_content_mapping(extracted_dir)

    # Open or create PDF
    original = find_original_pdf(extracted_dir)
    if original:
        print(f"Original PDF: {original.name}")
        doc = fitz.open(original)
    else:
        print("No original PDF - creating blank notebook pages")
        doc = create_blank_notebook(len(rm_files), output_path)

    # Process each .rm file
    for rm_file in rm_files:
        page_uuid = rm_file.stem

        # Determine page number
        if page_uuid in page_mapping:
            page_num = page_mapping[page_uuid]
        else:
            # Try to extract number from filename or use 0
            try:
                page_num = int(page_uuid.split("-")[0])
            except (ValueError, IndexError):
                page_num = 0

        # Skip if page doesn't exist
        if page_num >= len(doc):
            print(f"Warning: Page {page_num} doesn't exist, skipping {rm_file.name}")
            continue

        # Extract and render strokes
        strokes = extract_strokes(rm_file)
        if strokes:
            print(f"  Page {page_num + 1}: {len(strokes)} strokes")
            page = doc[page_num]
            render_strokes_to_page(page, strokes)

    # Save result
    doc.save(output_path)
    doc.close()
    print(f"\nRendered PDF saved to: {output_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python render-annotations.py <extracted_dir> <output.pdf>")
        print("")
        print("Example:")
        print("  unzip Document.zip -d Document_extracted")
        print("  python render-annotations.py Document_extracted Document-annotated.pdf")
        sys.exit(1)

    extracted_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not extracted_dir.is_dir():
        print(f"Error: Directory not found: {extracted_dir}")
        sys.exit(1)

    render_to_pdf(extracted_dir, output_path)


if __name__ == "__main__":
    main()
