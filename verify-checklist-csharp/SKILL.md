---
name: verify-checklist-csharp
description: Skeptically re-audit a completed local C# and .NET implementation checklist, including child checklists and their parent overview when present, then fix and prove real gaps in code, tests, documentation, and runtime wiring.
---

# Verify Checklist (C#)

Re-audit a completed local C# implementation checklist without trusting its
checkmarks. Find missing behavior, weak tests, stale documentation, dead paths,
and broken runtime wiring; correct what can be corrected; and leave precise
evidence for anything genuinely blocked.

## Build the Audit Map

Read the executable checklist, its source material, validation/test records,
repository instructions, ADRs/contracts, implementation, tests, solution and
project configuration, and runtime tooling. When the checklist belongs to a
set, read the parent overview first, then audit one completed child at a time.

Parse every checked and unchecked executable item into a live audit table:

| Item | Claimed state | Intended behavior | Proof required | Finding | Evidence |
| --- | --- | --- | --- | --- |

Treat a checkmark as a claim to test, not evidence. Discover the actual SDK,
target frameworks, solution structure, analyzer/formatter/test commands,
startup method, browser tooling, and coverage/security policy from repository
configuration.

## Audit Parent Overviews as Coordination Records

The parent overview has no implementation checkboxes. Verify that each source
requirement maps to one child, every completed child has implementation evidence
and rereview results, declared local prerequisites match execution order, the
tracer bullet produced its promised end-to-end proof, and the parent has not
claimed completion before shared integration and final gates pass.

Do not let a completed child imply completion of another child or the parent.
If a child invalidates shared assumptions, mark affected children blocked,
record evidence, and route the artifacts to `plan-checklist-csharp`
for an explicit revision.

## Pre-Phase Inventory

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

## Any Added Step Follows the Checklist Pattern

This discipline is not limited to pre-phase inventory items. Any step added
to a phase during the audit - a pre-phase finding, a newly discovered
`RG-###` gap, an edge case surfaced while auditing an item, or a correction
the parent overview requires - is verified the same way as every other item
on the list: name it, investigate or fix it, confirm the result against real
evidence rather than a claim, record that evidence, and only then tick it off
before moving to the next item. Never batch several added steps into one
unverified block, and never treat a phase's audit as complete while an added
step is still open.

## Per-Item Skeptical Loop

For each item, compare promised behavior with the real code path, public
contract, tests, docs, and runtime result. Label findings precisely:
`verified`, `missing`, `incomplete`, `scaffolded`, `weakly-tested`,
`runtime-failing`, `doc-drift`, `dead-path`, `parallel-path`, `risky`, or
`blocked`.

Correct the most valuable evidence-backed problem first:

```text
reproduce -> add or strengthen a public-behavior test -> fix the root cause ->
run focused proof -> run broader proof -> update evidence and docs
```

Every discovered regression receives a dedicated behavior-first regression test.
Test public C# interfaces: endpoints, components, commands, services,
persistence results, or documented APIs, rather than private structure.

## C# and .NET Audit Lenses

Verify that the documented architecture exists in project references, imports,
and runtime wiring. In Clean Architecture solutions, Domain stays independent
of framework and I/O concerns; Application coordinates use cases; Infrastructure
implements ports; the composition root selects concrete adapters.

Inspect DI lifetimes, configuration binding, validation, cancellation,
`async`/`await` correctness, error handling, structured logging, secret
redaction, serialization, persistence/recovery, and public contracts. Resolve
sync-over-async, unobserved tasks, empty catches, swallowed exceptions,
disabled nullable/analyzer warnings, unsafe static state, framework leakage,
and unreachable registrations or endpoints.

For Blazor work, verify `.razor` markup, `.razor.cs` logic/state/handlers, and
`.razor.css` vanilla CSS remain separated according to repository convention.
Check configured theme tokens, semantic controls, keyboard flow, focus,
loading/empty/error/disabled states, responsive reflow, touch sizing, and no
unintended horizontal overflow. Boot the actual application where feasible and
verify changed flows at representative viewports with browser evidence.

## Resolve Drift, Not Symptoms

Scan for duplicate services, obsolete compatibility bridges, unused components,
dead endpoints, stale test fixtures, parallel state models, and documentation
that claims behavior the system does not provide. Establish one live path,
remove safely replaced paths, and update durable docs/contracts to runtime
truth. Preserve a migration boundary only when deletion is unsafe and document
why.

Update executable checklists with clear audit notes. Preserve incomplete state
for real blockers. Add newly found gaps as `RG-###` entries with discovery
reason and required proof. For a checklist set, update the parent overview with
child audit results and changed next action; keep detailed command output in
the child evidence record.

## Final Proof and Report

After each correction, run focused validation. Before closing the audit, run
all applicable solution/project formatter, analyzer, `dotnet build`, tests,
coverage, security, browser/E2E, and runtime smoke gates. A passing compilation
or filtered test is not operational proof.

Report product/specification fidelity and C# architecture/quality separately.
Finish with verified items and strongest evidence, corrections and regression
tests, removed dead/parallel paths, documentation repairs, commands and
runtime/browser proof, and remaining blockers. For a checklist set, report each
child result separately and state whether parent completion criteria pass.