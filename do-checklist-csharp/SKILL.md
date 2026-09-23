---
name: do-checklist-csharp
description: Execute one approved local C# and .NET implementation checklist, including a child selected by a parent overview, with behavior-first tests, quality gates, and live runtime proof. Use after local checklist planning is approved.
---

# Do Checklist (C#)

Turn one approved local C# implementation checklist into working, evidenced
behavior. This skill executes one bounded checklist at a time; it does not
rewrite product scope, create planning artifacts, create external work, or
treat item checkmarks as proof.

## Establish the Execution Contract

Read the executable checklist in full, its source material, repository and
directory instructions, linked ADRs/contracts, nearest implementation and
committed tests, and .NET tooling configuration. When the checklist belongs to
a set, read the parent overview first for shared rules, prerequisites, tracer
evidence, child order, and parent completion criteria; execute only the selected
child.

Extract every phase, item, output, prerequisite, validation command, budget,
and completion condition. A parent overview coordinates evidence; it is not
authority to implement another child.

Discover target framework, solution/project layout, `dotnet` SDK selection,
formatter/analyzer, test/coverage tooling, application entrypoint, safe runtime
smoke command, and browser tooling from the repository. Unknown commands are
explicit prerequisites or assumptions, never evidence.

## Coordinate Checklist Sets Locally

For a standalone checklist, begin after its prerequisites pass. For a checklist
set, use the parent overview to select the next child whose declared local
prerequisites and evidence gates are satisfied. The tracer-bullet child proves
the relevant vertical path before dependent children begin; it does not grant
permission to silently expand into their scopes.

On child completion, update its evidence record with commands, results,
artifacts, and blockers. Update the parent overview only with child state,
evidence reference, and newly unblocked child. The parent is complete only when
every child has implementation and independent rereview evidence and its shared
integration and final gates pass.

If execution proves the split wrong, stop at the smallest safe decision point,
record the evidence, and return the artifacts to
`plan-checklist-csharp` for an explicit revision.

## Execute Incrementally

Work one `P-###` item at a time:

```text
understand observable contract -> make the smallest cohesive change ->
prove behavior -> update durable docs -> record evidence -> complete item
```

Use a tight red-green loop for public behavior, defects, safety boundaries, and
failure paths: add one focused failing test, implement only enough to pass it,
then refactor only while behavior remains green. Work vertically; do not batch
all tests first or split one outcome into disconnected Domain, infrastructure,
and UI batches.

Honor the documented architecture. Keep Domain independent of ASP.NET Core,
Blazor, EF Core, HTTP, filesystem, and transport dependencies where the
repository uses Clean Architecture. Application code coordinates use cases;
infrastructure implements ports; the composition root selects concrete
adapters. Use DI at real seams, explicit types, nullable-safe code, narrow
exceptions, structured logging, and explicit cancellation handling.

Use async correctly: avoid `.Result`, `.Wait()`, synchronous blocking over
async I/O, accidental fire-and-forget calls, and swallowed cancellation. Do not
hide failures behind empty catches or silent fallback values.

For Blazor work, preserve `.razor` markup, `.razor.cs` logic/state/handlers,
and `.razor.css` vanilla CSS. Use configured theme variables, accessible
semantic controls, responsive layout, visible focus, keyboard flow, and
representative browser viewport proof.

## Treat Gates as Behavior

Run discovered repository commands in their required order. As applicable, run
`dotnet restore`, focused tests after the first substantive edit, broader
project/solution tests, format/analyzer/build/coverage/security checks, browser
or E2E tests, and the canonical safe runtime entrypoint. A successful build or
unit test is not a substitute for runtime proof.

If a command fails, diagnose the root cause, repair the implementation, rerun
focused proof, then rerun the broader gate. Do not weaken analyzers, tests,
coverage, timeouts, or quality policy to pass. A slow or hung process is
evidence to investigate, not permission for unbounded waiting.

Update public contracts, developer setup, user-facing guidance, examples, and
durable documentation in the same checklist item as the behavior change.

## Keep Records True

Complete an item only when behavior, tests, documentation, and validation
evidence agree. Record command, result, artifacts, and blocker in the checklist
or linked validation record. If a prerequisite is unavailable, preserve the
incomplete state and state the precise proof gap.

If paused, persist current phase, revision, commands, evidence, next action,
and for a checklist set, the parent overview's next executable child. These
file-backed records are the handoff source; chat context is not a second
authority.

## Completion Report

Lead with implemented behavior. Include executed checklist path, completed
items, materially changed files/contracts, behavior-first tests, exact final
gates, live runtime/browser proof, recorded evidence, and blockers. For a
child checklist, name the parent overview and next local action. Hand the
completed checklist to `verify-checklist-csharp` for independent proof.