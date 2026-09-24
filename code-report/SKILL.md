---
name: code-report
description: Explain a repository, change, branch, commit range, or focused area through a product-aware, evidence-grounded, self-contained offline HTML report. Use when readers need to understand how a codebase serves a live product; not for code review or implementation planning.
---

# Code Report

Create a durable explanation of how a product purpose is implemented by a codebase.
The report is explanatory, not a review: describe what the evidence shows, distinguish
inference from fact, and record unknowns instead of inventing intent.

## Target routing

Use an explicit target whenever the request supplies one:

- `repo [focus]` — the current checkout as a whole, optionally focused on an area.
- `branch [name]` — the named or current branch versus the repository default branch.
- `commit <source-id> <target-id>` — compare the source tree with the target tree.
- `change <target>` — explain a supplied diff or change target.
- `focus <area>` — explain one product or subsystem area at the current checkout.

Bare invocation means the current checkout as a repository report. If a request mixes
whole-repository and change scope, ask which scope is intended. Resolve the default branch
and exact target commit before citing source lines.

Write artifacts outside the repository to:

```text
$HOME/code-reports/YYYY-MM-DD-<target-slug>-code-report.html
$HOME/code-reports/YYYY-MM-DD-<target-slug>-code-report.json
$HOME/code-reports/YYYY-MM-DD-<target-slug>-code-report-decisions.md
```

## Discovery and decision capture

For material preferences that cannot be discovered from the repository, use the native
selectable-question interface when available. Ask no more than three meaningful questions
per round, include a recommended option, and continue until scope, audience, product goal,
depth, visualization, and validation choices are settled. Record answers in the decision
Markdown and JSON manifest.

Do not ask the user for facts available in the repository. First inspect the README,
manifests, architecture records, entrypoints, tests, UI or API surfaces, supported
commands, and runtime instructions. Establish:

- product purpose, users, inputs, process, outputs, and boundaries;
- active entrypoints proven by wiring or runtime evidence;
- key components and their responsibilities;
- one representative real product flow;
- available tests, smoke commands, and external dependencies;
- confirmed facts, inferences, unknowns, and evidence gaps.

## Product-to-code evidence chain

Build one traceable thread through the report:

```text
product outcome -> user/system flow -> architecture responsibility -> implementation evidence
```

Use these evidence labels consistently:

- **Code-confirmed** — read directly in the target source.
- **Runtime-confirmed** — observed by running a supported command or flow.
- **Documented** — stated in project documentation or durable records.
- **Inferred** — reasoning supplied by the report author; label it as inference.
- **Unknown** — relevant but unverified; state the missing proof.

Use section-level source references in the reader-facing page. Keep detailed anchors,
commands, research provenance, and evidence records in the source bundle. Never claim that
a filename or registration alone proves an active entrypoint.

## Report contract

Use one responsive page with these sections, in order:

1. **Catch-up** — product purpose, boundaries, vocabulary, and only the background needed.
2. **The Gist** — the core mechanism in plain language, with a small representative example.
3. **How It Fits Together** — product architecture, responsibilities, and boundaries.
4. **Follow the Data** — one real product flow with actual code-relevant data.
5. **In the Code** — the implementation path in logical flow order, not filename order.
6. **Prove It** — a short learning check with reasoning-focused quiz questions.

Adapt depth to reader friction and codebase complexity. The minimum useful report covers
purpose, boundaries, one real flow, evidence, and a learning check. Omit material that does
not support the reader task, selected flow, architecture understanding, or quiz concept.

Write layered explanations: answer first, define names before using them, then expose
technical depth through disclosure controls. Prefer one idea per sentence, active voice,
plain terms, and concrete examples. Mark motivations and design reasons as **Inferred**
unless the durable record states them.

## Visual and interaction policy

Use one purposeful visual for each major section when a visual improves understanding.
Choose the smallest useful inline HTML/CSS/SVG diagram for the relationship: product flow,
component boundary, data flow, state, hierarchy, or ordered steps. Omit a visual when prose
is clearer; do not decorate the page or repeat the same relationship twice.

The final HTML must be self-contained and offline. Inline CSS, JavaScript, and SVG. Do not
load fonts, scripts, images, or analytics from a network. Keep the narrative and answer
explanations readable with JavaScript disabled.

The page must provide semantic headings, keyboard-operable controls, visible focus states,
usable contrast, responsive layout, and reduced-motion support. Include table-of-contents
navigation, progressive disclosure, and quiz feedback.

Quiz questions may be single-correct or multi-select. Multi-select uses all-or-nothing
scoring. Shuffle options at runtime by answer identity, not by authored position. Explain
the reasoning immediately and avoid position, length, or copied-source clues.

## Research and pattern decisions

For each material design choice, inspect relevant local skills/templates, project evidence,
and—when available—primary, license-aware external sources. Network failure must degrade
gracefully to local evidence. Do not copy incompatible prose or assets.

For every major section, record in the source bundle:

- candidate patterns considered;
- selected pattern;
- rejected alternatives;
- why the selected pattern fits this product, audience, and evidence;
- any unknown or unavailable research input.

Keep the main page digestible. Show a concise design-decision appendix and keep full
comparison data in the Markdown and JSON artifacts.

## Source bundle and incremental refresh

Use `schema/report-manifest.schema.json` as the source contract. The manifest stores
provenance, decisions, product compass, section content, sources, diagrams, quiz metadata,
research comparisons, and validation results.

When a later run targets a changed revision, refresh affected evidence, claims, diagrams,
and quiz items. Preserve unaffected decisions and mark stale evidence explicitly. Do not
silently carry a source anchor across revisions.

Use the helpers when deterministic transformation or validation is useful:

```bash
python3 code-report/scripts/render_report.py --manifest report.json --output report.html
python3 code-report/scripts/validate_report.py report.html --manifest report.json
```

The helpers are portable Python standard-library tools. Browser smoke checks are optional;
if unavailable, record the skipped check in the manifest rather than treating it as proof.

## Completion checks

Before delivery, confirm:

- the target, commit, date, and provenance agree;
- all six sections and their table-of-contents links exist;
- every source reference resolves or is explicitly marked unknown;
- HTML, CSS, JavaScript, diagrams, and quiz logic are self-contained;
- code and user-controlled text are escaped;
- the page has no external requests and remains readable without JavaScript;
- quiz choices shuffle without changing correctness;
- keyboard interaction and narrow layouts work;
- all stated numbers came from recorded commands;
- validation results and skipped checks are recorded;
- no irrelevant module inventory or unsupported motivation remains.

The final report is an artifact, not a conversational lesson. Keep explanations and
decisions in the files so another reader can understand and regenerate the result without
the original chat.
