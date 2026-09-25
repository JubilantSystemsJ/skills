---
name: verify-checklist-python
description: Skeptically re-audit a completed local Python implementation checklist, including child checklists and their parent overview when present, then fix and prove real gaps in code, tests, documentation, and runtime wiring.
---

# Verify Checklist (Python)

Re-audit a completed local Python implementation checklist without trusting its
checkmarks. The goal is runtime truth: identify misleading claims, missing
behavior, weak tests, stale documentation, dead paths, and broken wiring;
correct what can be corrected; and leave a precise evidence trail for anything
genuinely blocked.

## Build the audit map

Read the entire executable checklist, optional validation/test records, linked
product requirements, architecture documents, ADRs, repository instructions,
relevant implementation and tests, and project tooling configuration. When the
checklist belongs to a set, read the parent overview first, then audit one
completed child at a time. Parse every checked and unchecked executable item
into a live audit table:

| Item | Claimed state | Intended behavior | Proof required | Finding | Evidence |
| --- | --- | --- | --- | --- | --- |

Treat a checkmark as a claim to test, not as evidence. Include cross-cutting
audit targets for package boundaries, runtime wiring, documentation drift,
quality policy, secrets, and replaced paths. Discover Python versions, package
layout, actual validation commands, startup method, and browser tooling from
the repository.

Also verify the handoff chain: the implementation still matches the originating
PRD/specification or description, declared prerequisites were respected, agreed
test seams were used, and the evidence can be consumed by the next local
execution phase.

## Audit Parent Overviews as Coordination Records

The parent overview has no implementation checkboxes to audit. Instead, verify
that each source requirement maps to one child, each completed child has an
evidence record and rereview result, declared local prerequisites match the
implementation order, and the parent has not claimed completion before its
cross-checklist integration and final gates pass.

Do not let a completed child imply completion of another child or the parent.
If a child invalidates shared assumptions, mark the affected overview and
children blocked, record the evidence, and route the plan back to
`plan-checklist-python` for an explicit revision. Local artifacts
and recorded proof remain the sole basis for that decision.

## Pre-phase inventory

Before auditing each phase's items, including the first, pause and take
inventory of that phase as an audit boundary. Check whether the original
implementation missed something in this phase's scope, whether there is an
oversight in the phase's stated behavior or assumptions, or whether extra
verification work is required before this phase's items can be audited
meaningfully. List each finding as a lettered pre-phase item (`a`, `b`, `c`,
... `z`) scoped to this phase; do not fold these into `RG-###` or the phase's
existing item numbering.

For every lettered item, decide and record one of two outcomes: it blocks
auditing this phase and must be resolved here first, or it - or the phase's
audit itself - is independent enough to hand to another agent or session to
progress in parallel. Apply the same skeptical discipline as the rest of this
audit: investigate, verify the result against real evidence rather than a
claim, record that evidence, and only then tick the lettered item off before
moving to the next one or into the phase's per-item audit. When the inventory
finds nothing, record that explicitly and proceed.

## Any added step follows the checklist pattern

This discipline is not limited to pre-phase inventory items. Any step added
to a phase during the audit - a pre-phase finding, a newly discovered
`RG-###` gap, an edge case surfaced while auditing an item, or a correction
the parent overview requires - is verified the same way as every other item
on the list: name it, investigate or fix it, confirm the result against real
evidence rather than a claim, record that evidence, and only then tick it off
before moving to the next item. Never batch several added steps into one
unverified block, and never treat a phase's audit as complete while an added
step is still open.

## Per-item skeptical loop

For each item, compare the promised product behavior with the code path,
public contract, tests, documentation, and live runtime result. Label findings
precisely: `verified`, `missing`, `incomplete`, `scaffolded`, `weakly-tested`,
`runtime-failing`, `doc-drift`, `dead-path`, `parallel-path`, `risky`, or
`blocked`.

Correct the most valuable evidence-backed problem first:

```text
reproduce -> write or strengthen a public-behavior test -> fix the root cause ->
run focused proof -> run broader proof -> update evidence and docs
```

Every discovered regression gets a dedicated behavior-first regression test.
Tests should exercise public Python interfaces—CLI commands, routes, services,
persisted outputs, or documented APIs—not merely inspect private structure.
Use fakes only at external boundaries that cannot safely or deterministically
run in the test.

## Python-specific audit lenses

Verify the repository's chosen architecture is real in imports and runtime
wiring. In layered projects, domain code remains free of framework and I/O
imports; application code coordinates use cases; infrastructure implements
ports; the composition root selects concrete adapters. Identify and resolve
upward dependencies, broad exception swallowing, type suppressions masking
errors, untyped public boundaries, generic dumping-ground modules, unsafe
subprocess construction, and unredacted secret paths.

For package and operational behavior, inspect actual entrypoints, configuration
loading, persistence/recovery behavior, logging/error paths, and external
adapter seams. Confirm an implementation is reachable through its advertised
command, API, or UI—not merely present in the source tree.

For web work, boot the real service where feasible and verify the changed route
and critical interaction, loading/empty/error states, keyboard behavior where
relevant, responsive layout, and server/browser error output. In
FastAPI/Jinja/HTMX applications, verify route-to-use-case boundaries, escaped
templates, mutation safety, and that browser state is not a second authority.

Run the final review on two separate axes: product/specification fidelity and
Python standards/architecture. Report each independently, including scope creep
and missing behavior on the first axis and typing, dependency direction,
quality, and maintainability issues on the second. A passing test suite does
not erase a specification failure, and a correct feature does not erase an
architecture failure.

## Resolve drift, not just symptoms

Scan for duplicate or obsolete code, stale compatibility layers, unreachable
implementations, test fixtures no longer used, and documentation that claims
behavior the system does not provide. Establish the one live path, remove
replaced paths where safe, and update docs/contracts to the verified runtime
truth. Record an intentional migration boundary only when a safe deletion is
not yet possible.

Update checklist items only with clear audit notes. Preserve an incomplete
checkbox for a real blocker. Add newly found gaps as a distinct `RG-###` item
with the discovery reason and required proof. For a checklist set, update the
parent overview with the child audit result and any changed next action. Keep
transient execution detail in the checklist or validation record rather than
architecture documents.

## Final proof and report

After every corrected area, run focused validation. Before closing the audit,
run all applicable project-wide formatter, lint, type, test, coverage,
dependency, security, secret-scan, build, and browser/E2E gates. Then run the
canonical safe application entrypoint and confirm usable success. A passing
import, filtered test, or documentation assertion is not operational proof.

If the repository has an execution-control boundary, verify it explicitly:
validation may update local evidence records, while human approval, merge, or
deployment actions remain separate. A display or status indicator is not
execution evidence.

Finish with a PR-style rereview summary:

- verified items and their strongest evidence;
- corrections made and regression tests added;
- removed dead or parallel paths;
- documentation and contract repairs;
- commands and runtime/browser proof run;
- remaining blockers, risks, and unverified external boundaries.

The rereview is complete only when every checklist item has an audit finding
and all remediated work has passing evidence. For a checklist set, report each
child result separately and state whether the parent completion criteria pass;
otherwise report the unresolved state without implying completion.
