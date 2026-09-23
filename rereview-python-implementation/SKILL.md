---
name: rereview-python-implementation
description: Skeptically re-audit a Python implementation against its checklist, then fix and prove real gaps in code, tests, documentation, and runtime wiring. Use after implementation or when claimed completion needs independent verification.
---

# Rereview Python Implementation

Re-audit an implemented Python checklist without trusting its checkmarks. The
goal is runtime truth: identify misleading claims, missing behavior, weak
tests, stale documentation, dead paths, and broken wiring; correct what can be
corrected; and leave a precise evidence trail for anything genuinely blocked.

## Build the audit map

Read the entire checklist, optional validation/test records, linked product
requirements, architecture documents, ADRs, repository instructions, relevant
implementation and tests, and project tooling configuration. Parse every
checked and unchecked checklist item into a live audit table:

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
with the discovery reason and required proof. Keep transient execution detail
in the checklist or validation record rather than architecture documents.

## Final proof and report

After every corrected area, run focused validation. Before closing the audit,
run all applicable project-wide formatter, lint, type, test, coverage,
dependency, security, secret-scan, build, and browser/E2E gates. Then run the
canonical safe application entrypoint and confirm usable success. A passing
import, filtered test, or documentation assertion is not operational proof.

If the repository has an execution-control boundary, verify it explicitly:
validation may produce a report and update the local evidence record, but any
human approval, merge, or deployment actions remain separate. Where external
state is projected, verify that it is reconciled with internal execution state
rather than treating a board edit or UI projection as a second workflow
authority.

Finish with a PR-style rereview summary:

- verified items and their strongest evidence;
- corrections made and regression tests added;
- removed dead or parallel paths;
- documentation and contract repairs;
- commands and runtime/browser proof run;
- remaining blockers, risks, and unverified external boundaries.

The rereview is complete only when every checklist item has an audit finding
and all remediated work has passing evidence; otherwise report the unresolved
state without implying completion.
