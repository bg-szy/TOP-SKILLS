#!/usr/bin/env python
"""
Generate a detailed commit message for the skills update pipeline.
Compares current manifest.json with the committed version,
counts changes, and outputs a formatted message.
"""
import json
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "skills" / "manifest.json"


def get_previous_manifest() -> dict:
    """Read manifest.json from the last commit (HEAD)."""
    try:
        result = subprocess.run(
            ["git", "show", "HEAD:skills/manifest.json"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="replace",
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception:
        pass
    return {"skills": {}}


def get_current_manifest() -> dict:
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.loads(f.read())


def format_commit_message(old: dict, current: dict) -> str:
    old_skills = old.get("skills", {})
    cur_skills = current.get("skills", {})

    old_keys = set(old_skills.keys())
    cur_keys = set(cur_skills.keys())

    added_keys = cur_keys - old_keys
    removed_keys = old_keys - cur_keys
    common_keys = cur_keys & old_keys

    # Detect updated (sha changed)
    updated_keys = set()
    for k in common_keys:
        if old_skills[k].get("sha") != cur_skills[k].get("sha"):
            updated_keys.add(k)

    # Group by source
    def by_source(keys):
        groups = defaultdict(list)
        for k in keys:
            prefix = k.split("/", 1)[0]
            groups[prefix].append(k.split("/", 1)[1] if "/" in k else k)
        return groups

    added_src = by_source(added_keys)
    updated_src = by_source(updated_keys)
    removed_src = by_source(removed_keys)

    # Build message
    lines = []
    lines.append(f"Auto-update skills")

    total_new = len(added_keys)
    total_upd = len(updated_keys)
    total_del = len(removed_keys)
    summary_parts = []
    if total_new:
        summary_parts.append(f"+{total_new} new")
    if total_upd:
        summary_parts.append(f"~{total_upd} updated")
    if total_del:
        summary_parts.append(f"-{total_del} removed")
    if summary_parts:
        lines.append("")
        lines.append(f"Summary: {', '.join(summary_parts)}")
        lines.append(f"Total: {len(cur_keys)} skills")

    if total_new:
        lines.append("")
        lines.append("New skills by source:")
        for src in sorted(added_src):
            names = added_src[src]
            lines.append(f"  {src}: +{len(names)}")
            for n in names[:8]:
                lines.append(f"    - {n}")
            if len(names) > 8:
                lines.append(f"    ... and {len(names)-8} more")

    if total_upd:
        lines.append("")
        lines.append("Updated skills by source:")
        for src in sorted(updated_src):
            lines.append(f"  {src}: ~{len(updated_src[src])}")

    if total_del:
        lines.append("")
        lines.append("Removed skills by source:")
        for src in sorted(removed_src):
            lines.append(f"  {src}: -{len(removed_src[src])}")
            for n in removed_src[src]:
                lines.append(f"    - {n}")

    if not any([total_new, total_upd, total_del]):
        lines.append("")
        lines.append("No changes — all skills up to date.")

    return "\n".join(lines)


def main():
    old = get_previous_manifest()
    current = get_current_manifest()
    msg = format_commit_message(old, current)
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
