#!/usr/bin/env python3
"""Merge fresh evidence into a prior manifest without losing recorded decisions."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


def refresh(previous: dict, current: dict) -> dict:
    result = copy.deepcopy(current)
    if not result.get("decisions"):
        result["decisions"] = copy.deepcopy(previous.get("decisions", []))
    if not result.get("research"):
        result["research"] = copy.deepcopy(previous.get("research", []))
    old_sources = {source.get("label"): source for source in previous.get("sources", [])}
    new_labels = {source.get("label") for source in result.get("sources", [])}
    for source in result.get("sources", []):
        old = old_sources.get(source.get("label"))
        if old and old.get("location") != source.get("location"):
            source["previous_location"] = old.get("location")
            source["stale"] = False
    for label, old in old_sources.items():
        if label not in new_labels:
            stale = copy.deepcopy(old)
            stale["stale"] = True
            stale["note"] = "Source was present in the previous revision but absent from the refreshed evidence."
            result.setdefault("sources", []).append(stale)
    result.setdefault("validation", {})["refresh"] = {
        "preserved_decisions": bool(previous.get("decisions")) and not bool(current.get("decisions")),
        "preserved_research": bool(previous.get("research")) and not bool(current.get("research")),
        "stale_source_count": sum(1 for source in result.get("sources", []) if source.get("stale")),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previous", required=True, type=Path)
    parser.add_argument("--current", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    previous = json.loads(args.previous.read_text(encoding="utf-8"))
    current = json.loads(args.current.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(refresh(previous, current), indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
