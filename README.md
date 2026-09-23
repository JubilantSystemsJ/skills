# Skills

A small personal collection of Claude Code skills for shipping a change end to end:
plan it, do it, verify it actually happened, then explain it. Built to be small,
composable.

## The Plan → Do(Build) → Verify pattern

**The problem.** Ask an agent to "just implement this feature" and three things get
blurred into one pass: deciding what to build, actually building it, and judging whether
it's actually done. An agent grading its own homework in the same breath it wrote the
homework tends to mark everything correct. Bugs from stage one silently survive into
stage three because nothing forces a fresh, skeptical look.

**The fix.** Split the work into three skills that hand off a single shared artifact - a
local implementation checklist - so each stage gets undivided attention, and the last
stage is a genuinely independent, skeptical re-check rather than a self-review.

```
Plan  →  produces the checklist (docs/implementation/*.md)
Do    →  executes it top to bottom, item by item, with evidence
Verify → re-reads the real code fresh, not the checkboxes, and fixes real gaps
```

Each phase comes in a Python and a C#/.NET flavor:

- **`plan-checklist-python`** / **`plan-checklist-csharp`** - turn a spec, PRD, issue, or
  ticket into one local checklist, or a coordinated set of them for bigger work. Planning
  only - no code is touched.
- **`do-checklist-python`** / **`do-checklist-csharp`** - execute an approved checklist:
  tests written first, the repo's real quality gates run, live runtime proof captured,
  evidence recorded against each item as it's actually completed.
- **`verify-checklist-python`** / **`verify-checklist-csharp`** - come back later with no
  memory of writing the code, re-read what's actually there against what the checklist
  claimed, and fix any gap it finds rather than just reporting it.

### A practical walkthrough

Say you need to add rate limiting to a Python endpoint:

1. `/plan-checklist-python` reads the ticket and repo conventions, and writes
   `docs/implementation/rate-limiting-implementation-checklist.md` - a numbered list of
   concrete steps, each with its own test seam and a clear "done" condition.
2. `/do-checklist-python` works through that file top to bottom: writes the failing test,
   makes it pass, runs the project's actual lint/type/test commands, and records the
   evidence next to each item - not just a checked box.
3. `/verify-checklist-python` opens the same checklist cold, re-reads the real code and
   tests against every claim, and repairs anything that was marked done but wasn't -
   before you ever open a PR.
4. Once it's real, run **Code Tour** on the branch to get a proper explanation of what you
   just shipped (see below).

The C# flavor works the same way, just swap `python` for `csharp`.

## Code Tour: catching up on what actually changed

`/code-tour` has two scopes. A pull request, branch, diff, change, or commit range means
"explain one change" and produces a single self-contained HTML page: what changed, the
core idea behind it, how the touched pieces fit together, a visual trace of the data
flowing through the real change, a code walkthrough ordered by logical flow rather than
file order, and a short quiz to check it actually landed. Use `/code-tour branch` for the
current branch or `/code-tour branch feature/login` for a named branch. Use `/code-tour
commit abc123 def456` to compare an ordered source commit with a target commit. Use
`/code-tour repo` for an explicit whole-repository HTML report, or `/code-tour repo
authentication flow` to focus that report on one area. Every scope writes a self-contained
HTML file. With no further wording, `/code-tour` defaults to the current branch versus the
repository's default branch.

This is the natural last step after Plan → Do → Verify: the checklist cycle proves the
change is *correct*; Code Tour makes it *understandable* - to a teammate reviewing the PR,
to future-you re-opening a branch after a two-week gap, or to anyone who just needs to get
back up to speed on what actually moved in the codebase without re-reading the whole diff
by hand.

## Reference

| Skill | Language | Stage |
|---|---|---|
| [`plan-checklist-python`](./plan-checklist-python/SKILL.md) | Python | Plan |
| [`plan-checklist-csharp`](./plan-checklist-csharp/SKILL.md) | C# / .NET | Plan |
| [`do-checklist-python`](./do-checklist-python/SKILL.md) | Python | Do |
| [`do-checklist-csharp`](./do-checklist-csharp/SKILL.md) | C# / .NET | Do |
| [`verify-checklist-python`](./verify-checklist-python/SKILL.md) | Python | Verify |
| [`verify-checklist-csharp`](./verify-checklist-csharp/SKILL.md) | C# / .NET | Verify |
| [`code-tour`](./code-tour/SKILL.md) | Any | After - explain the result |

Full detail, triggers, and rules live in each skill's own `SKILL.md` - this file is a map,
not a replacement for reading them.
