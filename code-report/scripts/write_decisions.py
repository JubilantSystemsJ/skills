#!/usr/bin/env python3
"""Write a readable decision and evidence log from a report manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def write(manifest: dict) -> str:
    report = manifest["report"]
    lines = [
        f"# {report['title']} decisions and evidence",
        "",
        f"Target: `{report['target']}`",
        f"Scope: `{report['scope']}`",
        f"Written: {report['written_at']}",
        "",
        "## Product purpose",
        "",
        manifest["product"]["purpose"],
        "",
        "## Decisions",
        "",
    ]
    for decision in manifest.get("decisions", []):
        lines.append(f"- **{decision.get('topic', 'Decision')}** — {decision.get('selected', '')}: {decision.get('rationale', '')}")
    lines += ["", "## Research choices", ""]
    for choice in manifest.get("research", []):
        lines.append(f"- **{choice.get('topic', 'Research')}** — selected `{choice.get('selected_pattern', '')}`: {choice.get('rationale', '')}")
    lines += ["", "## Sources", ""]
    for source in manifest.get("sources", []):
        stale = " (stale)" if source.get("stale") else ""
        lines.append(f"- `{source.get('kind', 'unknown')}` **{source.get('label', '')}** — {source.get('location', 'unresolved')}{stale}")
    lines += ["", "## Validation", ""]
    validation = manifest.get("validation", {})
    if validation:
        for key, value in validation.items():
            lines.append(f"- `{key}`: {value}")
    else:
        lines.append("- No validation results recorded yet.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(write(manifest), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
