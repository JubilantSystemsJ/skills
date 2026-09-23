---
name: plan-checklist-csharp
description: Turn supplied C# and .NET requirements, PRDs, specifications, issues, and repository documentation into one local implementation checklist or a coordinated set of bounded local checklists. Use for planning only, before code execution.
---

# Plan Checklist (C#)

Create the local implementation artifact that a later C# coding agent will
execute. This skill plans only: it does not edit application code, run
implementation validation, create tracker work, commit, or push.

The source may be a PRD, specification, issue, work description, conversation,
bug report, roadmap section, or supplied documentation. The deliverable is one
implementation checklist or a parent overview with bounded child checklists.

## 1. Gather Decision-Bearing Context

Read the supplied sources and only the repository material needed to interpret
them:

- repository and directory instructions;
- the primary request plus linked PRDs, specifications, ADRs, and contracts;
- relevant architecture, data, API, and UX documents;
- solution, project, package, analyzer, test, startup, CI, and browser
  configuration;
- the nearest implementation and committed tests for an existing behavior.

Inspect `*.sln`, `*.slnx`, `*.csproj`, `Directory.Build.*`, `global.json`,
`NuGet.config`, `.editorconfig`, test projects, and CI scripts as applicable.
Record verified facts: target frameworks, solution and project layout,
architecture boundaries, test frameworks, analyzers, formatters, `dotnet`
commands, safe runtime proof, browser tooling, documentation locations, and
unknowns. An unverified command or requirement is an explicit assumption or
prerequisite, never a fabricated checklist task.

## 2. Decide the Artifact Shape

Write **one standalone checklist** when the requested outcome has one cohesive
implementation boundary and can be completed, quality-gated, and proven through
one safe runtime path in a focused execution context.

Write a **checklist set** only when work has independently verifiable outcomes,
one outcome depends on evidence or a contract from another, separate solution,
project, migration, or runtime boundaries require isolated validation and
rollback, or the full work cannot be safely executed and reviewed in one
focused context.

Do not split merely because the plan has multiple phases or files. Keep every
artifact file-backed and local. A parent overview coordinates evidence and
declared local prerequisites; it is not executable work.

For a checklist set, create one parent overview and child checklists. Each
child has one observable outcome, scope, prerequisite set, public test seam,
validation, and completion gate. When architecture, integration, persistence,
or UI uncertainty needs proof, make the first child a **tracer bullet**: the
smallest end-to-end vertical path that proves the approach before dependent
children start. A tracer bullet is a local child checklist, not a separate
delivery type.

## 3. Reconcile Sources Into Bounded Work

For each source requirement, identify the owning domain, application,
presentation, infrastructure, or integration boundary; observable behavior and
failure behavior; public contract; test seam; documentation impact; and
prerequisite. Preserve the documented architecture rather than imposing a new
one.

For Clean Architecture repositories, preserve inward dependencies:

```text
Domain <- Application <- Interfaces / Presentation
                     <- Infrastructure
```

The composition root selects concrete adapters. Do not put persistence, HTTP,
or framework concerns into Domain or application rules merely because a
checklist is being authored.

Map each requirement to one standalone checklist or one child. Shared rules and
cross-checklist constraints live in the parent overview; duplicate them in a
child only when execution needs them locally. Surface a real contradiction or
missing product decision as a prerequisite gate instead of silently deciding it.

## 4. Write Local Artifacts

Follow the repository convention. If none exists, write either:

```text
docs/implementation/<work-name>-csharp-implementation-checklist.md
```

or, for a checklist set:

```text
docs/implementation/<work-name>/overview.md
docs/implementation/<work-name>/01-<tracer-or-slice>-csharp-checklist.md
docs/implementation/<work-name>/02-<slice>-csharp-checklist.md
```

### Parent Overview Format

The parent overview contains:

1. status, source documents, planning assumptions, and target solution;
2. requested outcome, scope boundary, and non-goals;
3. shared .NET architecture rules and discovered commands;
4. a requirement-to-checklist traceability table;
5. child order, local prerequisites, tracer-bullet rationale when used, and the
   next executable child;
6. shared migration, compatibility, rollback, and integration constraints;
7. completion criteria: every child implemented and independently rereviewed,
   cross-checklist integration proven, and all final gates recorded;
8. deferred work and unresolved blockers.

The overview has no implementation checkboxes. It coordinates child evidence;
it does not replace it.

### Standalone and Child Checklist Format

Each executable checklist contains:

1. **Status and provenance** - source documents, target projects, scope,
   assumptions, and parent relationship when present.
2. **Outcome and scope boundary** - observable result, non-goals, and
   prerequisites.
3. **Locked implementation rules** - discovered C#/.NET architecture,
   security, quality, and documentation rules.
4. **Closed-loop outputs** - numbered observable outputs and their proof.
5. **Phases** - sequential `P-###` items. Every item states behavior, failure
   behavior where relevant, public test seam, documentation impact, discovered
   validation command, success condition, and local dependency.
6. **Completion gate** - focused and broad quality, runtime, browser/E2E, and
   documentation proof required for this checklist.
7. **Evidence record** - command, result, artifact path, and remaining blocker
   recorded by the implementation skill.

Keep each `P-###` item small enough for one focused execution pass but large
enough to produce meaningful vertical behavior. A wide mechanical refactor is
the exception: model expand, migrate, and contract as separate green validation
boundaries.

## 5. Encode C# and .NET Constraints

Adapt every rule to repository evidence; stricter local rules win.

- Use the configured SDK and target frameworks. Keep nullable and analyzer
  policy intact; do not disable warnings or lower quality thresholds to pass.
- Keep Domain rules free of framework, transport, persistence, and UI imports.
  Use DI and explicit interfaces at real seams; do not add abstractions without
  an ownership or testing benefit.
- Use `async`/`await` correctly: no sync-over-async, accidental fire-and-forget,
  or swallowed cancellation. Propagate `CancellationToken` across meaningful
  asynchronous and I/O boundaries when the repository pattern requires it.
- Validate inputs and handle expected failures explicitly. Do not use empty
  catches, silent fallbacks, or unbounded retries. Log meaningful context and
  never log secrets.
- Use the repository's required comment convention. For repositories using the
  archived C# charter, new explanatory sections begin with `// AI Suggests:`;
  examples begin with `// Hypothetical:`.
- Test public behavior, errors, safety boundaries, persistence/recovery, and
  contracts. Prefer real deterministic components; fake only unavailable,
  unsafe, slow, nondeterministic, or prohibitively costly boundaries.
- Discover and use actual `dotnet restore`, `dotnet build`, `dotnet test`,
  formatter, analyzer, coverage, security, and browser/E2E commands. Include
  exact budgets and success conditions.

For Blazor work, preserve the repository component convention: `.razor` for
markup, `.razor.cs` for logic/state/handlers, and `.razor.css` for vanilla
component CSS. Use configured theme tokens such as `var(--color-*)`; preserve
semantic HTML, keyboard access, visible focus, responsive reflow, touch-sized
controls, and no unintended horizontal overflow. Include browser proof at
representative viewport sizes.

## 6. Check the Artifact Before Reporting It

Before reporting completion, confirm:

- every source requirement maps to one executable checklist item;
- the chosen shape is justified and every child is independently executable;
- parent and child paths, order, prerequisites, tracer rationale, and completion
  criteria agree;
- item identifiers are unique within each checklist;
- all `dotnet` and browser commands are discovered or marked as assumptions;
- no placeholder, file-presence-only, or unproven implementation can satisfy a
  completion gate;
- the next skill can execute directly from the files without chat history.

## Output Report

Report artifact paths, standalone or coordinated shape, child count and next
executable child when applicable, source documents consumed, target framework
and tooling detected, planned runtime/browser proof, assumptions, and the next
skill: `do-checklist-csharp`.