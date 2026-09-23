---
name: implement-python-checklist
description: Execute an existing phased implementation checklist derived from a Python PRD, specification, or work description, with behavior-first tests, repository quality gates, and runtime proof. Use after a checklist is approved; use planning skills to create or reshape a checklist.
---

# Implement Python Checklist

Turn one approved Python implementation checklist into working, evidenced
behavior. This skill executes; it does not rewrite product scope, create a new
roadmap, or treat item checkmarks as proof.

## Establish the execution contract

Read the checklist in full, its originating PRD/specification or work
description, repository and local instructions, linked source documents,
relevant ADRs/contracts, the nearest code and committed tests, and
the project's Python/CI tooling configuration. Extract every phase, item,
output, prerequisite, validation command, budget, and completion condition.

Before the first change, report the intended phase order and build a short live
TODO. Discover these from repository evidence rather than assuming them:

- supported Python version and package layout;
- formatter, lint, type, test, coverage, dependency, security, and secret-scan
  commands;
- canonical application entrypoint and safe terminating smoke command;
- integration/E2E/browser tooling when relevant.

An unknown command is an explicit prerequisite or assumption, never evidence.

Confirm the public test seam for each item before writing tests. If the
PRD/specification names one, use it; if it does not, propose the highest useful
seam and record the decision before the first test. The implementation should
be understandable from the local checklist and source documents without
reconstructing the original conversation.

## Execute incrementally

Work one checklist item at a time within its phase:

```text
understand observable contract -> make the smallest cohesive change ->
prove behavior -> update durable docs -> record evidence -> complete item
```

Use test-first development when practical, especially for defects, public
behavior, safety boundaries, and failure paths. Run a focused test after the
first substantive edit, then broader phase gates once the item is integrated.
Tests should exercise real deterministic implementations where safe; use fakes
or mocks only at unavailable, unsafe, slow, nondeterministic, or prohibitively
costly external boundaries.

For each behavior, use a tight red-green loop: write one failing public-
behavior test, implement only enough to pass it, then move to the next
behavior. Work vertically through the smallest meaningful path. Do not batch
all tests first or split the work into disconnected domain, infrastructure, and
UI layers. Refactoring belongs after the behavior is green and must serve the
PRD/specification or the repository architecture.

Keep architecture honest. Follow documented dependency direction and compose
concrete infrastructure in the composition root. Keep Python domain rules and
application coordination independent of web frameworks, subprocesses,
filesystems, SDKs, and transport code where the repository architecture calls
for that separation. Use typed function boundaries, cohesive modules, narrow
exceptions with useful context, and explicit subprocess argument lists.

For an established web stack, preserve its boundaries. In FastAPI/Jinja/HTMX
projects, routes translate requests, application services own use cases,
templates receive view models, and UI mutations use the same application path
as other clients. Validate changed flows with accessible, responsive browser
proof at representative viewports.

## Treat gates as behavior

Run repository-defined quality gates in their required order. Preserve the
configured formatter, lint, type, test, coverage, dependency, security, and
secret-scan policy. Diagnose failing gates at their source, repair the actual
problem, and rerun focused then broad proof. A policy or test change is valid
only when it corrects a demonstrable defect or intentional supported contract
change and is documented for review.

After every code change, run the canonical safe application entrypoint and
confirm an exit code of zero with usable output. If a quality gate is mandatory
before startup, it precedes the smoke command. Imports, help output, isolated
unit tests, and quality-only commands do not replace runtime proof.

Use checklist or repository time budgets. A slow or hung command is evidence to
investigate; record the cause and return to the narrowest useful check before
re-running its full gate.

At completion, review the diff against two independent questions: does it meet
the originating PRD/specification, and does it meet the repository's Python
standards and architecture? Keep the reports separate. Resolve material
findings before the draft-PR handoff or record them as explicit blockers. Do
not automatically merge, approve, or close external work.

## Keep records true

Complete a checklist item only when its promised behavior, tests,
documentation, and validation evidence agree. Add concise evidence to the
checklist or its linked validation record: command, result, and artifact path
when useful. Update public contracts, developer setup, examples, and durable
documentation with the change; remove superseded code and stale documentation
when the new behavior replaces them.

When a prerequisite is unavailable, retain its incomplete state and report the
specific blocker, attempts, safe options, and remaining proof gap. Do not
simulate external success or replace live proof with a claim.

If work is paused or handed to another session, persist the current phase,
revision, commands, evidence, and next action in the local checklist or
validation record. That file-backed record is the handoff source; chat context
is not a second authority.

## Completion report

Lead with the implemented behavior. Include completed checklist items, files or
contracts materially changed, behavior-first tests added, exact final gates
run, runtime proof, and any explicit blockers or follow-ups. State partial
completion plainly.
