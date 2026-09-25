#!/usr/bin/env python3
"""Render a code-report JSON manifest into a self-contained HTML document."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "report-template.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_text(text: str) -> str:
    paragraphs = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        if all(line.startswith("- ") for line in lines):
            items = "".join(f"<li>{esc(line[2:])}</li>" for line in lines)
            paragraphs.append(f"<ul>{items}</ul>")
        else:
            paragraphs.append(f"<p>{esc(' '.join(lines))}</p>")
    return "\n".join(paragraphs)


def render_visual(visual: dict | None) -> str:
    if not visual:
        return ""
    title = esc(visual.get("title", "Visual explanation"))
    svg = visual.get("svg")
    if svg:
        if "<script" in svg.lower() or "http://" in svg.lower() or "https://" in svg.lower():
            raise ValueError("visual SVG must not contain scripts or external URLs")
        body = svg
    else:
        body = f"<p>{esc(visual.get('description', 'No visual description supplied.'))}</p>"
    return f'<figure class="visual"><figcaption><strong>{title}</strong></figcaption>{body}</figure>'


def render_sources(source_ids: list[str], sources: list[dict]) -> str:
    by_label = {str(source.get("label")): source for source in sources}
    items = []
    for source_id in source_ids:
        source = by_label.get(source_id, {"label": source_id, "kind": "unknown", "location": "unresolved"})
        items.append(
            f'<li><span class="evidence">{esc(source.get("kind", "unknown"))}</span> '
            f'{esc(source.get("label", source_id))} — {esc(source.get("location", "unresolved"))}</li>'
        )
    return f'<details><summary>Sources for this section</summary><ul>{"".join(items)}</ul></details>' if items else ""


def render_components(component_ids: list[str], components: list[dict], sources: list[dict]) -> str:
    by_id = {str(component.get("id")): component for component in components}
    cards = []
    for component_id in component_ids:
        component = by_id.get(component_id)
        if not component:
            cards.append(f'<article class="component"><h3>{esc(component_id)}</h3><p><span class="evidence">unknown</span> No component context packet was supplied.</p></article>')
            continue
        def items(values: list[str]) -> str:
            return "".join(f"<li>{esc(value)}</li>" for value in values)
        cards.append(
            '<article class="component">'
            f'<h3>{esc(component.get("name", component_id))}</h3>'
            f'<p><span class="evidence">{esc(component.get("kind", "component"))}</span> {esc(component.get("role", ""))}</p>'
            f'<dl><dt>Receives</dt><dd><ul>{items(component.get("receives", []))}</ul></dd>'
            f'<dt>Produces</dt><dd><ul>{items(component.get("produces", []))}</ul></dd>'
            f'<dt>Fits with</dt><dd><ul>{items(component.get("neighbors", []))}</ul></dd>'
            f'<dt>Boundary</dt><dd>{esc(component.get("boundary", "Unknown"))}</dd>'
            f'<dt>Why it exists</dt><dd>{esc(component.get("why", "Unknown"))}</dd></dl>'
            f'{render_sources(component.get("sources", []), sources)}'
            '</article>'
        )
    return f'<div class="component-grid">{"".join(cards)}</div>' if cards else ""


def render_sections(manifest: dict) -> tuple[str, str]:
    sections = manifest.get("sections", [])
    sources = manifest.get("sources", [])
    components = manifest.get("components", [])
    content = []
    toc = ["<strong>Contents</strong>"]
    clusters = [("Understand", sections[:3]), ("Trace", sections[3:5]), ("Check", sections[5:])]
    for cluster_name, cluster_sections in clusters:
        if not cluster_sections:
            continue
        toc.append(f'<div class="cluster">{esc(cluster_name)}</div>')
        for section in cluster_sections:
            if section.get("id") == "quiz":
                continue
            section_id = esc(section["id"])
            title = esc(section["title"])
            toc.append(f'<a href="#{section_id}">{title}</a>')
            content.append(
                f'<section id="{section_id}"><h2>{title}</h2>'
                f'<p class="lede">{esc(section.get("summary", ""))}</p>'
                f'{render_components(section.get("components", []), components, sources)}'
                f'{render_text(section.get("body", ""))}'
                f'{render_visual(section.get("visual"))}'
                f'{render_sources(section.get("sources", []), sources)}</section>'
            )
    return "\n".join(content), "\n".join(toc)


def render_quiz(manifest: dict) -> str:
    questions = manifest.get("quiz", {}).get("questions", [])
    if not questions:
        return ""
    quiz_section = next((section for section in manifest.get("sections", []) if section.get("id") == "quiz"), {})
    blocks = [
        '<section id="quiz"><h2>Prove It</h2>',
        f'<p class="lede">{esc(quiz_section.get("summary", "Check the reasoning in the report."))}</p>',
        render_text(quiz_section.get("body", "")),
        render_visual(quiz_section.get("visual")),
        render_sources(quiz_section.get("sources", []), manifest.get("sources", [])),
        '<p>Answer from the reasoning in the report. Choices change position when the page loads.</p>',
    ]
    answer_key = []
    for number, question in enumerate(questions, start=1):
        qid = esc(question["id"])
        qtype = "checkbox" if question.get("type") == "multi" else "radio"
        name = f"q-{qid}"
        options = []
        for index, option in enumerate(question.get("options", [])):
            options.append(
                f'<label class="quiz-option"><input type="{qtype}" name="{esc(name)}" value="{index}"> {esc(option)}</label>'
            )
        correct = [int(value) for value in question.get("correct", [])]
        feedback = esc(question.get("feedback", "Review the relevant section and evidence."))
        blocks.append(
            f'<article class="quiz" data-quiz data-correct="{esc(json.dumps(correct))}" data-feedback="{feedback}">'
            f'<h3>{number}. {esc(question["prompt"])}</h3>'
            f'<div class="quiz-options">{"".join(options)}</div>'
            f'<button type="button">Check answer</button><p class="quiz-feedback" hidden aria-live="polite"></p>'
            f'</article>'
        )
        answer_key.append(f"<li><strong>{number}:</strong> {esc(question.get('feedback', 'See the related section.'))}</li>")
    blocks.append(f'<noscript><details open><summary>Answer explanations</summary><ol>{"".join(answer_key)}</ol></details></noscript></section>')
    return "\n".join(blocks)


def render_decisions(manifest: dict) -> str:
    decisions = manifest.get("decisions", [])
    research = manifest.get("research", [])
    if not decisions and not research:
        return ""
    items = []
    for decision in decisions:
        items.append(f'<li><strong>{esc(decision.get("topic", "Decision"))}:</strong> {esc(decision.get("selected", ""))} — {esc(decision.get("rationale", ""))}</li>')
    for choice in research:
        items.append(f'<li><strong>Research — {esc(choice.get("topic", ""))}:</strong> selected {esc(choice.get("selected_pattern", ""))}; {esc(choice.get("rationale", ""))}</li>')
    return f'<section id="decisions"><h2>Design decisions</h2><div class="decision"><ul>{"".join(items)}</ul></div></section>'


def render(manifest: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    report = manifest["report"]
    sections, toc = render_sections(manifest)
    content = sections + render_quiz(manifest) + render_decisions(manifest)
    replacements = {
        "{{TITLE}}": esc(report["title"]),
        "{{PROVENANCE}}": esc(f'{report["target"]} · {report.get("commit", "commit unknown")} · written {report["written_at"]}'),
        "{{LEDE}}": esc(manifest["product"]["purpose"]),
        "{{CONTENT}}": content,
        "{{TOC}}": toc,
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    if "{{" in template or "}}" in template:
        raise ValueError("unresolved template marker")
    return template


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(manifest), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
