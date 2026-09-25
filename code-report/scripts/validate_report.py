#!/usr/bin/env python3
"""Validate report manifest invariants and generated HTML without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_IDS = {"background", "intuition", "architecture", "dataflow", "code", "quiz"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.external: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        href = values.get("href") or values.get("src") or ""
        if href:
            self.hrefs.append(href)
            if re.match(r"^(https?:)?//", href):
                self.external.append(href)


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def validate_manifest(manifest: dict) -> None:
    for key in ("schema_version", "report", "product", "sections", "quiz", "validation"):
        if key not in manifest:
            fail(f"manifest missing {key}")
    if manifest["schema_version"] != "1.0":
        fail("unsupported schema version")
    report = manifest["report"]
    for key in ("title", "slug", "scope", "target", "written_at"):
        if not report.get(key):
            fail(f"report missing {key}")
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", report["slug"]):
        fail("report slug is not kebab case")
    product = manifest["product"]
    for key in ("purpose", "boundaries", "outcomes"):
        if not product.get(key):
            fail(f"product missing {key}")
    sections = manifest["sections"]
    if len(sections) < 6:
        fail("fewer than six sections")
    ids = {section.get("id") for section in sections}
    missing = REQUIRED_IDS - ids
    if missing:
        fail(f"missing sections: {', '.join(sorted(missing))}")
    architecture = next((section for section in sections if section.get("id") == "architecture"), {})
    component_ids = architecture.get("components", [])
    components = {component.get("id"): component for component in manifest.get("components", [])}
    if not component_ids:
        fail("architecture section has no component context packets")
    for component_id in component_ids:
        component = components.get(component_id)
        if not component:
            fail(f"architecture references missing component: {component_id}")
        for key in ("name", "kind", "role", "receives", "produces", "neighbors", "boundary", "why", "sources"):
            if not component.get(key):
                fail(f"component {component_id} missing context field: {key}")
    for question in manifest.get("quiz", {}).get("questions", []):
        options = question.get("options", [])
        correct = question.get("correct", [])
        if len(options) < 2 or not correct or any(not isinstance(value, int) or value >= len(options) for value in correct):
            fail(f"invalid quiz question {question.get('id', '<unknown>')}")
        if question.get("type") == "single" and len(correct) != 1:
            fail(f"single question has multiple answers: {question.get('id', '<unknown>')}")
        if question.get("type") == "multi" and len(correct) < 1:
            fail(f"multi question has no answer: {question.get('id', '<unknown>')}")


def validate_html(page: str, manifest: dict) -> None:
    parser = PageParser()
    parser.feed(page)
    missing = REQUIRED_IDS - parser.ids
    if missing:
        fail(f"HTML missing section ids: {', '.join(sorted(missing))}")
    if parser.external:
        fail(f"external resources found: {', '.join(parser.external)}")
    if "{{" in page or "}}" in page:
        fail("unresolved template marker")
    if "<script" in page.lower() and "data-quiz" not in page:
        fail("script exists without quiz wiring")
    for href in parser.hrefs:
        if href.startswith("#") and href[1:] not in parser.ids:
            fail(f"broken internal link: {href}")
    if "document.querySelectorAll('[data-quiz]')" not in page:
        fail("runtime quiz shuffle is missing")
    if "<noscript>" not in page:
        fail("no-JavaScript fallback is missing")
    if "<meta name=\"viewport\"" not in page:
        fail("responsive viewport metadata is missing")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    validate_html(args.html.read_text(encoding="utf-8"), manifest)
    print(f"valid: {args.html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
