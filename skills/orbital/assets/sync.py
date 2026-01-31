#!/usr/bin/env python3
"""Back up Orbital.nyc reflections to Obsidian as Markdown.

Covers both:
1. Reflection Log Notes (weekly, monthly, quarterly)
2. Quarterly Community Updates (wins, lessons, intentions, talk)

Only accesses the authenticated user's own content.

Usage:
    # Set credentials via environment or let the script use 1Password
    python sync.py

    # Force full re-sync (ignore last_sync timestamp)
    python sync.py --force
"""

import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SUPABASE_URL = "https://avlgvxtubpfmwtyhvsis.supabase.co"
SUPABASE_KEY = "sb_publishable_K-FozEyE7nhPRcNJ7Jjy3w_a7fVN0B6"
OP_ITEM_ID = "y3bbe4uwhmgy4sha32vzdplqpa"
ORBITAL_DIR = Path.home() / "Obsidian" / "cag" / "Orbital"

# Map known promptIds to readable section headers.
# Unknown promptIds get title-cased automatically.
PROMPT_LABELS = {
    # Lessons
    "personal": "Personal Lessons",
    "work": "Work Lessons",
    "field": "Field Lessons",
    # Intentions
    "change": "Do Differently",
    "sustain": "Keep Doing",
    "annual-reflection": "Annual Reflection",
    "rituals": "Rituals",
    # Talk
    "links": "Recommendations",
    "questions": "Questions",
    "ask": "Asks",
    "give": "Offers",
    "qol": "Quality of Life",
    "feedback": "Feedback",
}

# Which promptIds belong to which section
INTENTION_PROMPTS = {"change", "sustain", "annual-reflection", "rituals"}
TALK_PROMPTS = {"links", "questions", "ask", "give", "qol", "feedback"}


try:
    from markdownify import markdownify as _md

    def html_to_md(html: str) -> str:
        if not html or "<" not in html:
            return html or ""
        result = _md(html, heading_style="ATX", bullets="-")
        return re.sub(r"\n{3,}", "\n\n", result).strip()
except ImportError:

    def html_to_md(html: str) -> str:
        return html or ""


def op_get(field: str) -> str:
    result = subprocess.run(
        ["op", "item", "get", OP_ITEM_ID, "--fields", field, "--reveal"],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def get_token() -> str:
    """Authenticate with Supabase via 1Password credentials."""
    email = op_get("email")
    password = op_get("password")

    data = json.dumps({"email": email, "password": password}).encode()
    req = urllib.request.Request(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        data=data,
        headers={
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
        },
    )
    resp = urllib.request.urlopen(req)
    body = json.loads(resp.read())
    token = body.get("access_token")
    if not token:
        print("Authentication failed:", body, file=sys.stderr)
        sys.exit(1)
    return token


def api_get(token: str, path: str) -> dict:
    url = f"https://orbital.nyc{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def write_file(filepath: Path, content: str) -> bool:
    """Write file only if content changed. Returns True if written."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    if filepath.exists() and filepath.read_text() == content:
        return False
    filepath.write_text(content)
    return True


def render_post(post: dict) -> list[str]:
    """Render a single post (win/lesson/poll) to markdown lines."""
    lines = []
    lead = post.get("lead") or ""
    body = post.get("body") or ""
    url = post.get("url") or ""
    if lead:
        lines.append(f"**{lead}**")
        lines.append("")
    if body:
        lines.append(body)
        lines.append("")
    if url:
        lines.append(f"[Link]({url})")
        lines.append("")
    return lines


def build_log_note(note: dict) -> str:
    """Build markdown for a reflection log note."""
    ntype = note["type"]
    period = note["period"]
    updated = note.get("updatedAt", "")
    prompt = note.get("promptTextSnapshot") or ""
    default_content = (note.get("noteContent") or {}).get("default") or ""
    sections = (note.get("noteContent") or {}).get("sections") or []

    lines = [
        "---",
        f"type: orbital-{ntype}",
        f'period: "{period}"',
        f'updated: "{updated}"',
        "tags:",
        "  - orbital",
        f"  - orbital/{ntype}",
        "---",
        "",
    ]

    if ntype == "weekly":
        lines.append(f"# Week {period.split('-', 1)[1]}")
    else:
        lines.append(f"# {period}")
    lines.append("")

    if prompt:
        lines.append(f"> [!question] {prompt}")
        lines.append("")

    if default_content:
        lines.append(html_to_md(default_content))
        lines.append("")

    for section in sections:
        heading = section.get("heading", "")
        content = section.get("content", "")
        if heading:
            lines.append(f"## {heading}")
            lines.append("")
        if content:
            lines.append(html_to_md(content))
            lines.append("")

    return "\n".join(lines)


def build_quarterly_update(
    edition: str,
    quarter: str,
    win_posts: list,
    lesson_posts: list,
    poll_posts: list,
) -> str:
    """Build markdown for a quarterly community update."""
    lines = [
        "---",
        "type: orbital-quarterly-update",
        f'edition: "{edition}"',
        f'quarter: "{quarter}"',
        "tags:",
        "  - orbital",
        "  - orbital/quarterly-update",
        "---",
        "",
        f"# {quarter} Quarterly Update",
        "",
    ]

    # Wins
    if win_posts:
        lines.append("## Wins")
        lines.append("")
        for p in win_posts:
            lead = p.get("lead") or ""
            if lead:
                lines.append(f"### {lead}")
                lines.append("")
            body = p.get("body") or ""
            if body:
                lines.append(body)
                lines.append("")
            url = p.get("url") or ""
            if url:
                lines.append(f"[Link]({url})")
                lines.append("")

    # Lessons — group by known promptIds, then catch uncategorized
    if lesson_posts:
        lines.append("## Lessons")
        lines.append("")
        seen = set()
        for pid in ["personal", "work", "field"]:
            matching = [p for p in lesson_posts if p.get("promptId") == pid]
            if matching:
                seen.update(p["id"] for p in matching)
                lines.append(f"### {PROMPT_LABELS[pid]}")
                lines.append("")
                for p in matching:
                    lines.extend(render_post(p))
        uncategorized = [p for p in lesson_posts if p["id"] not in seen]
        if uncategorized:
            for p in uncategorized:
                lines.extend(render_post(p))

    # Intentions
    intention_posts = [p for p in poll_posts if p.get("promptId") in INTENTION_PROMPTS]
    if intention_posts:
        lines.append("## Intentions")
        lines.append("")
        seen = set()
        for pid in sorted(INTENTION_PROMPTS):
            matching = [p for p in intention_posts if p.get("promptId") == pid]
            if matching:
                seen.update(p["id"] for p in matching)
                lines.append(f"### {PROMPT_LABELS.get(pid, pid.replace('-', ' ').title())}")
                lines.append("")
                for p in matching:
                    lines.extend(render_post(p))

    # Talk
    talk_posts = [p for p in poll_posts if p.get("promptId") in TALK_PROMPTS]
    if talk_posts:
        lines.append("## Talk")
        lines.append("")
        seen = set()
        for pid in sorted(TALK_PROMPTS):
            matching = [p for p in talk_posts if p.get("promptId") == pid]
            if matching:
                seen.update(p["id"] for p in matching)
                lines.append(f"### {PROMPT_LABELS.get(pid, pid.replace('-', ' ').title())}")
                lines.append("")
                for p in matching:
                    lines.extend(render_post(p))

    # Catch any poll posts with unknown promptIds
    known_poll_ids = INTENTION_PROMPTS | TALK_PROMPTS
    other = [p for p in poll_posts if p.get("promptId") not in known_poll_ids]
    if other:
        lines.append("## Other")
        lines.append("")
        for p in other:
            pid = p.get("promptId") or "uncategorized"
            label = PROMPT_LABELS.get(pid, pid.replace("-", " ").title())
            lines.append(f"### {label}")
            lines.append("")
            lines.extend(render_post(p))

    return "\n".join(lines)


def main():
    force = "--force" in sys.argv
    ORBITAL_DIR.mkdir(parents=True, exist_ok=True)

    last_sync_file = ORBITAL_DIR / ".last_sync"
    if not force and last_sync_file.exists():
        last_sync = last_sync_file.read_text().strip()
    else:
        last_sync = None

    print("Authenticating...")
    token = get_token()

    # Get member ID (for quarterly updates)
    member = api_get(token, "/api/account/member")
    member_id = member["member"]["id"]
    print(f"Member: {member['member'].get('name', member_id)}")

    # === Log Notes ===
    print("\nFetching log notes...")
    notes_data = api_get(
        token,
        "/api/account/notes?span=3650&includeIncomplete=false"
        "&weekStartDay=1&workweekLength=5&timezone=America/New_York"
        "&types=weekly,monthly,quarterly",
    )
    notes = notes_data.get("notes", [])
    print(f"Found {len(notes)} log notes")

    written = 0
    skipped = 0
    for note in notes:
        period = note["period"]
        updated = note.get("updatedAt", "")

        # Skip unchanged notes (compare updatedAt to last sync)
        if last_sync and updated and updated <= last_sync:
            skipped += 1
            continue

        filepath = ORBITAL_DIR / f"{period}.md"
        content = build_log_note(note)
        if write_file(filepath, content):
            print(f"  Wrote: {filepath.name}")
            written += 1
        else:
            print(f"  Unchanged: {filepath.name}")
            skipped += 1

    print(f"Log notes: {written} written, {skipped} skipped")

    # === Quarterly Updates ===
    print("\nFetching quarterly updates...")
    history = api_get(token, "/api/networks/member/tasks/history")
    editions = sorted(
        set(t["networkEdition"].removeprefix("1:") for t in history.get("tasks", []))
    )
    print(f"Found {len(editions)} editions: {editions}")

    written_updates = 0
    for edition in editions:
        parts = edition.split()
        if len(parts) == 2:
            quarter = f"{parts[1]}-{parts[0]}"
        else:
            quarter = edition

        enc = urllib.parse.quote(edition)
        wins = api_get(token, f"/api/networks/member/posts/user/{member_id}?type=win&edition={enc}")
        lessons = api_get(token, f"/api/networks/member/posts/user/{member_id}?type=lesson&edition={enc}")
        polls = api_get(token, f"/api/networks/member/posts/user/{member_id}?type=poll&edition={enc}")

        win_posts = wins.get("posts", [])
        lesson_posts = lessons.get("posts", [])
        poll_posts = polls.get("posts", [])

        if not win_posts and not lesson_posts and not poll_posts:
            print(f"  Skipping {edition} (no content)")
            continue

        filepath = ORBITAL_DIR / f"{quarter}-update.md"
        content = build_quarterly_update(edition, quarter, win_posts, lesson_posts, poll_posts)
        if write_file(filepath, content):
            print(f"  Wrote: {filepath.name} ({len(win_posts)}W {len(lesson_posts)}L {len(poll_posts)}P)")
            written_updates += 1
        else:
            print(f"  Unchanged: {filepath.name}")

    print(f"Quarterly updates: {written_updates} written")

    # Update last sync timestamp
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    last_sync_file.write_text(now)
    print(f"\nSync complete. Timestamp: {now}")


if __name__ == "__main__":
    main()
