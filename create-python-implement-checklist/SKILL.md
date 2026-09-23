---
name: create-python-implement-checklist
description: Turn supplied Python requirements, PRDs, specifications, issues, and repository documentation into one local implementation checklist or a coordinated set of bounded local checklists. Use for planning only, before code execution.
---

# Create Python Implement Checklist

Create the local implementation artifact that a later coding agent will
execute. This skill plans only: it does not edit application code, run
implementation validation, create tracker work, commit, or push.

The source may be a PRD, specification, issue, work description, conversation,
bug report, roadmap section, or any combination of supplied documentation. A
source is input evidence, not a delivery unit. The deliverable is either one
implementation checklist or a parent overview with several bounded child
checklists.

## 1. Gather Only Decision-Bearing Context

Read the supplied sources and the repository material needed to interpret them:

- repository and directory instructions;
- the primary request plus linked PRDs, specifications, issues, ADRs, and
  contracts;
- relevant architecture, data, API, and UX documents;
- packaging, test, quality, startup, CI, and browser configuration;
- the nearest implementation and committed tests for an existing behavior.

Use the repository's fast search tools first. Do not inventory unrelated
documentation merely to make the source list look comprehensive.

Record verified facts before designing work: Python version and package layout;
architecture and integration boundaries; formatter, lint, type, test, coverage,
security, dependency, and secret-scan commands; canonical safe runtime proof;
browser tooling; documentation locations; and any unknowns. An unverified
command or requirement is an explicit assumption or prerequisite, never a
fabricated checklist task.

## 2. Decide the Artifact Shape

Write **one standalone checklist** when the requested outcome has one cohesive
implementation boundary and can be completed, quality-gated, and proven through
one safe runtime path in a focused execution context.

Write a **checklist set** only when one or more of these conditions holds:

- the work contains independently releasable or independently verifiable
  outcomes;
- one outcome depends on evidence or a contract produced by another;
- separate repository, package, migration, or runtime boundaries need isolated
  validation and rollback;
- the full work cannot be executed and reviewed safely in one focused context
  without losing traceability or conflating unrelated failure modes.

Do not split merely because the plan has several phases or files. Keep every
artifact file-backed and local; the plan records local prerequisites and
evidence, not a projection to another system.

For a checklist set, create one parent overview and child checklists. The
parent is coordination metadata, never executable work. Each child has one
observable outcome, its own scope, prerequisites, test seam, validation, and
completion gate. When architecture or integration uncertainty needs proof, make
the first vertical child prove the relevant path end to end before dependent
children begin.

## 3. Reconcile Source Material Into Bounded Work

For every source requirement, determine the owning boundary, observable
behavior, failure behavior, public contract, test seam, documentation impact,
and prerequisite. Preserve documented architecture rather than imposing a new
one. For a web surface, routes remain transport adapters over application
services and do not own runtime files, provider SDKs, subprocesses, or workflow
state.

Map every requirement to exactly one child checklist or standalone checklist.
Shared rules and cross-checklist constraints belong in the parent overview;
they are repeated in a child only when execution needs them locally. Surface a
real contradiction or missing product decision as a prerequisite gate instead
of silently deciding it.

## 4. Write Local Artifacts

Follow an existing repository convention. If none exists, write either:

```text
docs/implementation/<work-name>-implementation-checklist.md
```

or, for a checklist set:

```text
docs/implementation/<work-name>/overview.md
docs/implementation/<work-name>/01-<slice>-implementation-checklist.md
docs/implementation/<work-name>/02-<slice>-implementation-checklist.md
```

### Parent Overview Format

The parent overview contains:

1. status, primary source, supporting sources, and planning assumptions;
2. the requested outcome, scope boundary, and non-goals;
3. shared repository rules and discovered quality/runtime commands;
4. a requirement-to-checklist traceability table;
5. child order, explicit local prerequisites, and the next executable child;
6. shared integration, migration, rollback, or compatibility constraints;
7. parent completion criteria: every child complete and independently
   rereviewed, cross-checklist integration proven, and all required final gates
   recorded;
8. deferred work and unresolved blockers.

The overview never has implementation checkboxes. It coordinates child
evidence; it does not replace it.

### Standalone and Child Checklist Format

Each executable checklist contains:

1. **Status and provenance** - source documents, scope, assumptions, and
   relationship to the parent overview when present.
2. **Outcome and scope boundary** - observable result, non-goals, and
   prerequisites.
3. **Locked implementation rules** - repository-specific architecture,
   security, quality, and documentation rules.
4. **Closed-loop outputs** - numbered observable outputs and their proof.
5. **Phases** - sequential `P-###` items. Every item states behavior, failure
   behavior where relevant, test seam, documentation impact, discovered
   validation command, success condition, and local dependency.
6. **Completion gate** - focused and broad quality, runtime, browser/E2E, and
   documentation proof required for this checklist.
7. **Evidence record** - a place for the implementation skill to record
   command, result, artifact path, and remaining blocker without treating a
   checkbox as proof.

Keep each `P-###` item small enough for one focused execution pass but large
enough to produce a meaningful vertical behavior. A wide mechanical refactor
is the exception: model expand, migrate, and contract as separate green
validation boundaries.

## 5. Encode Python Implementation Constraints

Adapt rules to the repository's actual configuration; a stricter local rule
wins. Require typed public and meaningful internal boundaries, cohesive
modules, narrow failure handling, explicit subprocess arguments, safe secret
handling, architecture-respecting adapters, behavior-first tests, configured
coverage, and no weakened quality policy. Require the eventual implementation
to prove the canonical safe runtime entrypoint after code changes and to run
browser proof for changed web behavior.

When a repository has a mandatory startup quality gate, include it before the
runtime proof. Keep future plumbing, prerequisites, and out-of-scope work
visibly separate from executable behavior.

## 6. Check the Artifact Before Reporting It

Before reporting completion, confirm:

- every primary source requirement maps to one executable checklist item;
- the chosen shape is justified and every child is independently executable;
- parent and child paths, order, prerequisites, and completion criteria agree;
- item identifiers are unique within each checklist;
- validation commands are discovered or marked as assumptions;
- the artifact describes only local checklist scope, prerequisites, and
  evidence;
- no placeholder, file-presence-only, or unproven implementation can satisfy
  a completion gate;
- the next skill can execute directly from these files without relying on chat
  context.

## Output Report

Report the artifact paths, whether the result is standalone or coordinated,
the child count and next executable child when applicable, source documents
consumed, detected tooling, planned runtime/browser proof, assumptions, and
the next skill: `implement-python-checklist` for an executable checklist or
`plan-python-checklist` when a parent overview needs coordination first.