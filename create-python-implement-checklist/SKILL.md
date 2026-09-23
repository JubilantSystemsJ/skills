---
name: create-python-implement-checklist
description: Create a phased, agent-executable implementation checklist from Python project requirements, architecture documents, ADRs, and contracts. Use when the user wants an implementation plan or markdown work queue, not code execution, issue creation, or a PRD.
---

# Create Python Implement Checklist

Create one implementation checklist that a coding agent can execute in a Python
repository. The checklist is a planning artifact: do not implement code,
create issues, commit, or push while using this skill.

This skill is intentionally Python-specific. It borrows the useful checklist
shape of generic planning tools, but it does not assume .NET, TypeScript,
React, a particular package manager, or a database.

## Workflow

### 1. Discover the repository contract

Before drafting the checklist, inspect only the relevant sources:

- repository instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
  and directory-specific instructions;
- the primary roadmap/requirements document;
- relevant PRD/specification, ADRs, data models, API/view contracts, and UX
  documents;
- `pyproject.toml`, `requirements*.txt`, lockfiles, packaging metadata,
  Makefile/task runner scripts, CI configuration, and existing test config;
- the nearest implementation and committed tests when the checklist targets an
  existing module.

Use `rg --files` and `rg` first. Do not read unrelated documentation merely to
make the source list look comprehensive.

Record the detected facts before writing:

- supported Python version and package layout (`src/`, flat package, or other);
- framework and integration boundaries;
- formatter, linter, type checker, test runner, coverage threshold,
  dependency/security scanners, and secret scanner;
- canonical application entrypoint and a safe terminating runtime command;
- browser/E2E tooling if a web surface exists;
- required documentation and generated-artifact locations.

If a command or runtime entrypoint cannot be verified, mark it as an explicit
assumption or prerequisite instead of presenting it as a confirmed command.

### 2. Reconcile requirements into execution boundaries

Extract the actual product outcome, decisions, invariants, dependencies,
non-goals, and future/deferred capabilities. Group work by cohesive boundary,
not by screen or file list alone.

For each requirement, identify:

- owning domain/application/infrastructure/client boundary;
- public interface or data contract;
- observable behavior and failure modes;
- test seam and realistic validation;
- documentation that must change;
- dependency on a previous phase.

Keep the checklist aligned with existing architecture. If a web surface exists,
routes are transport adapters over application services; they do not read
runtime files, call provider SDKs, launch subprocesses, or own workflow state.
If the project uses another architecture, preserve its documented boundaries
instead of imposing this example.

### 3. Produce the checklist

Use the canonical format below. Keep each item small enough for one focused
agent pass, but large enough to produce a behaviorally meaningful result.
Every item receives a sequential `P-###` identifier and maps to tests, docs,
and validation evidence. Each phase begins with a tracer-bullet slice: the
smallest path that proves the phase's architecture is wired end to end.

Do not mark anything complete in the generated checklist. It is handed to the
implementation workflow.

### Preserve the handoff contract

If the source is a settled PRD, specification, or work description, retain its
provenance in the checklist. Record the source reference, agreed public test
seams, implementation prerequisites, and the distinction between current
scope, future plumbing, and out-of-scope work. Do not reopen product decisions
inside a checklist item; surface a real contradiction as a prerequisite gate.

Every phase begins with a tracer bullet that proves one meaningful path through
the relevant Python layers. Prefer vertical behavior over separate domain,
adapter, and UI batches. A wide mechanical refactor is an exception: model it
as expand, migrate, and contract work with a green validation boundary between
each part.

Each item should expose a small execution contract:

- behavior delivered and observable failure behavior;
- dependencies and blocking edge, if any;
- public seam and test evidence;
- documentation or contract updates;
- exact discovered validation command and success condition;
- execution role (`implement`, `research`, `tdd`, or another configured role)
  when the repository's local workflow uses one.

## Canonical output format

The output is normally one Markdown file named according to the repository's
existing convention. If no convention exists, use:

```text
docs/implementation/<feature-name>-implementation-checklist.md
```

The file must contain these sections:

1. **Status** — date, primary source, supporting sources, detected Python
   stack, and explicit "ready for execution" or prerequisite status.
2. **Problem statement** — the outcome in product and engineering terms.
3. **Locked implementation rules** — Python/project-specific rules below,
   merged with repository instructions without weakening them.
4. **Scope boundary** — in scope and out of scope.
5. **Prerequisite contract gates** — dependencies that must exist before
   integration work can be considered complete.
6. **Runtime budgets and timeout contract** — command, budget, and success
   meaning.
7. **Closed-loop verifiable outputs** — numbered outputs with proof methods.
8. **Phases** — each phase must include:
   - Goal;
   - tracer-bullet item followed by sequential `P-###` checklist items;
   - Verifiable outputs;
   - exact local validation tasks and budgets;
   - invalid implementations to reject;
   - Phase complete when.
9. **Final gate** — cross-phase completion, quality, security, runtime, and
   documentation checks.

## Python locked rules

Adapt these rules to the repository's real configuration. A stricter existing
rule wins; do not invent a weaker fallback.

### Code and architecture

- Target the configured Python version. Type every new public and meaningful
  internal function boundary; use the repository's configured type checker,
  commonly Pyright or mypy.
- Preserve the repository's package/dependency direction. Use a composition
  root for concrete adapters and keep external SDKs, HTTP, subprocess, and
  filesystem effects behind narrow typed interfaces where the architecture
  requires it.
- Prefer standard-library types, `pathlib`, dataclasses, Pydantic only at
  declared input/output boundaries, context managers, explicit subprocess
  argument lists, and structured logging where appropriate.
- Keep modules cohesive. Do not create `utils`, `helpers`, `common`, or
  `misc` dumping grounds or add abstractions that do not simplify a real seam.
- Handle failures explicitly with narrow exceptions and preserved context. Do
  not use broad catches, silent fallbacks, unbounded retries, or broad type
  suppressions to make a gate pass.
- Never hard-code, log, render, or persist secrets. Use the repository's
  credential references and redaction rules.
- If the repository requires explanatory comments, use its exact convention.
  For AgentFabric-style repositories that means `# AI Suggests:`; never copy
  a language-inappropriate `//` convention into Python.

### Tests and evidence

- Test observable behavior, error handling, safety boundaries, public
  contracts, and recovery semantics. Prefer focused unit tests, then
  integration tests at real deterministic boundaries, then critical E2E tests.
- Use real implementations when safe and deterministic. Use fakes/mocks only
  for unavailable, unsafe, slow, nondeterministic, or prohibitively expensive
  boundaries, and keep them faithful to the production contract.
- Do not delete, weaken, skip, narrow, or rewrite tests merely to pass. Change
  a test only for a demonstrable defect, unsupported environment coupling, or
  intentional supported contract change.
- Add explicit timeouts to tests and subprocesses where the project supports
  them. A timeout is a defect signal, not permission to make the timeout
  unbounded.
- Require coverage to meet the configured threshold. Never lower the threshold
  or add exclusions as an implementation shortcut.

### Quality, runtime, and documentation

- Discover and use the repository's actual formatter, lint, type, test,
  coverage, dependency, security, secret-scan, and E2E commands.
- If a mandatory startup quality gate exists, include it before every
  operational runtime proof. For AgentFabric-style repositories this is
  `python quality_gate.py` or the configured equivalent.
- After every code change in the eventual implementation, run the canonical
  safe application entrypoint and prove exit code 0 with usable output. A
  module import, help text, quality-only command, or unit test is not runtime
  proof.
- Update affected documentation, contracts, examples, fixtures, migration
  notes, and user-facing commands in the same phase as the behavior change.
- Do not add dependencies unless direct use is justified and the repository's
  dependency audit passes.

### Web-specific rules when a web surface exists

- Use the repository's selected web stack. If it is FastAPI/Jinja/HTMX, keep
  routes thin, use typed Pydantic boundaries, preserve full-page fallback,
  return explicit HTMX fragments, and do not introduce an SPA or Node toolchain
  without a documented need.
- Apply semantic HTML, labels, keyboard access, visible focus, CSRF and
  authorization for browser mutations, autoescaping, safe CORS, and redacted
  errors.
- Validate responsive behavior in a running browser at representative mobile,
  tablet, desktop, and ultra-wide sizes. Assert no unintended overflow,
  clipping, layout shift, or hover-only required action.
- Browser UI state must not become a second workflow source of truth. Submit
  mutations through the same application/control-plane interface as CLI/TUI
  clients and test stale revisions, duplicate submissions, reconnects, and
  command receipts.

## Scope rules

Keep the generated checklist limited to the requested product slice. Include
prerequisite gates and explicit handoffs for dependencies, but do not silently
expand a UI checklist into provider implementation, deployment, database
migration, or issue creation.

Separate these categories visibly:

- **In scope:** behavior required for the current slice;
- **Prerequisite:** required contract or implementation owned elsewhere;
- **Future plumbing:** shape/projection reserved now but not executed;
- **Out of scope:** deliberately excluded capability.

When a future capability affects current layout or data contracts, add a
compatibility item and validation fixture without implementing the future
executor.

## Default runtime budgets

Use repository-specific budgets when they exist. Otherwise start with these
defaults and state that they are planning budgets:

| Operation | Budget |
| --- | ---: |
| Focused unit/route test | 10 seconds |
| Full non-browser test suite | 120 seconds |
| Formatter/linter/type gate | 60 seconds |
| Integration test group | 180 seconds |
| One browser journey | 30 seconds |
| Full browser/E2E suite | 300 seconds |
| Application startup | 15 seconds |
| Safe runtime smoke command | 30 seconds |

All budgets must have an observable success condition. Never use
`--exit-zero`, `continue-on-error`, hidden retries, or a command that discards
its exit status.

## Quality checks before finalizing the artifact

Before reporting the checklist complete:

- every primary requirement maps to at least one `P-###` item;
- every phase has a tracer-bullet path, hard validation gate, verifiable
  outputs, and invalid-implementation rejection criteria;
- every item maps to tests, documentation, and validation evidence;
- all item IDs are sequential and unique;
- all validation commands were discovered or are clearly marked assumptions;
- package manager and Python tooling match repository metadata;
- the checklist preserves existing domain vocabulary and ADR decisions;
- deferred capabilities are visibly separated from current scope;
- no scaffold-only, file-presence-only, or placeholder-only implementation can
  satisfy a phase gate;
- the generated Markdown has no unfinished TODO placeholders or secret-shaped
  fixture values.
- the checklist identifies the spec or work-item provenance and agreed test
  seams;
- phase items have observable vertical outcomes and prerequisites rather than
  only layer/file assignments;
- the implementation workflow can start from the local checklist without
  relying on this conversation being available.

## Output report

After creating the checklist, report:

- output path;
- phase and item counts;
- verifiable-output count;
- source documents consumed;
- detected Python version/package layout/tooling;
- exact validation commands included;
- whether runtime validation and browser validation are included;
- the next recommended skill, normally `implement-python-checklist`.
