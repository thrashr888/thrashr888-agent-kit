---
name: agent-ready-engineering
description: Make codebases ready for reliable human and agent work.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---

# Agent-Ready Engineering

Improve the engineering conditions that let people and coding agents make safe,
fast, repeatable changes. Agents do not repair a weak delivery system: they
amplify its standards, feedback loops, documentation, and review practices.

This skill strengthens the system around a workflow. It does not prescribe a
specific model, IDE, language, or vendor.

## When to Use

Use when:

- an agent repeatedly struggles with a codebase, environment, or deployment
  workflow;
- local iteration is slow because validation only happens in CI or a GUI;
- a team is rolling out coding agents and needs no-regrets investments;
- generated pull requests are increasing review load or reducing confidence;
- an onboarding, testability, or developer-experience investment should also
  make future agent work more reliable.

Do not use for a single isolated feature unless its delivery path exposes a
repeatable system problem. Do not standardize a stack merely because an agent
prefers it; start from real friction and measurable feedback loops.

## The Six Foundations

| Foundation | What good looks like | Evidence |
| --- | --- | --- |
| Standard tooling | Community-supported language, package, build, and formatting conventions | A fresh checkout follows documented commands without bespoke setup |
| Development-time control | Builds, tests, lint, types, migrations, and safe dev actions have CLI or API paths | No critical task requires clicking through a GUI or waiting on CI |
| Deterministic validation | Same input produces the same result, quickly, with an actionable failure | A targeted check identifies the violated constraint and exits non-zero |
| Structure and testability | Explicit boundaries, dependencies, and small testable units | A change can be exercised without booting unrelated systems |
| Written intent | Requirements, external constraints, decisions, and invariants are discoverable | An agent can explain why a constraint exists, not only what the code does |
| Review capacity and quality | Specific owners, visible turn-taking, and a real rejection bar | Review load and first-response time are observable and distributed |

## Quick Reference

| Symptom | First move | Do not do |
| --- | --- | --- |
| Agent guesses at environment state | Expose a narrow CLI/API query with structured, actionable output | Paste a long manual runbook into every prompt |
| CI is the only feedback loop | Make the relevant check runnable locally and targetable | Tell the agent to wait through full CI after every edit |
| Tests assert only that a button was clicked | Introduce a lower-level seam and behavior-focused assertions | Add more brittle end-to-end clicks as the only proof |
| Requirements live in meetings or tickets | Capture intent, external constraints, and acceptance criteria near the code | Generate documentation that merely restates function signatures |
| One reviewer absorbs all PRs | Assign a named reviewer, backup, and first-response expectation | Send every review to an unowned team channel |
| Same setup or debugging lesson recurs | Codify the stable lesson in a script, skill, or scoped instruction | Preserve task history as permanent project guidance |

## Procedure

### 1. Choose one agent loop to improve

Start with a concrete loop, not a generic “AI readiness” initiative. State:

- the change an engineer or agent is trying to make;
- the command, API, or UI step that blocks it;
- the feedback currently available; and
- the cost of a wrong or slow result.

Use `Grep` and `Read` to trace the actual entry points and `Bash` to exercise
existing checks before proposing a fix.

**Completion criterion:** the work names one observable loop such as “change
configuration → validate → test → inspect result,” with evidence of the current
friction.

### 2. Audit the foundations around that loop

Use `references/agent-readiness-audit.md`. Mark each foundation as:

- **ready** — works reliably at development time;
- **weak** — works but is slow, opaque, or unnecessarily manual; or
- **blocked** — missing, GUI-only, CI-only, or nondeterministic.

Audit the narrow path first. A repository-wide scorecard is useful only after a
representative workflow has shown what the scores mean.

**Completion criterion:** every weak or blocked item has a concrete symptom and
an owner or next decision; no score is based on inference alone.

### 3. Create the shortest trustworthy feedback loop

Prioritize work in this order when the foundations are missing:

1. Replace custom or opaque setup with documented, conventional tooling where
   the replacement is justified.
2. Provide CLI/API access for development-time operations.
3. Make validation deterministic, targetable, and clear enough to guide a fix.
4. Add seams, boundaries, and fixtures that make the changed behavior testable.
5. Record the intent and constraints that a validator cannot infer.
6. Design review flow to absorb the new PR volume without lowering the bar.

For a check to belong in an agent loop, it should be runnable without a human
browser session, fast enough for deliberate iteration, and precise about what
failed. A useful target is seconds; if a check takes longer than a minute,
provide a focused variant unless the operation fundamentally cannot be reduced.

**Completion criterion:** a developer or agent can run a documented command or
API call that proves the most important property of the loop before CI.

### 4. Make validation explain the next action

A failed check must identify the condition, location, and expected state—not
merely report a generic internal error. Pair generated code with deterministic
checks such as tests, type checks, schema checks, linters, or contract tests.

Use LLMs to propose and implement; use external tools to verify. Do not accept
an agent’s self-assessment as proof.

**Completion criterion:** an intentionally invalid change fails locally with an
error a different engineer could use to make the next correction.

### 5. Preserve intent and remove hidden coupling

Use the repository's planning, specification, and ADR conventions for durable
requirements and decisions; use `style-docs` when that companion skill is
installed. Document why the behavior exists, external constraints, data
contracts, and non-obvious invariants. Do not add a prose tour of code the agent
can inspect.

Where a change is hard to test, make dependencies explicit, isolate side effects,
and introduce seams that preserve production behavior while enabling focused
verification.

**Completion criterion:** the relevant requirement or decision explains the
constraint behind the validation, and the changed behavior can be tested without
an unrelated production dependency.

### 6. Protect review quality as volume increases

Treat review as a first-class delivery system. Use named assignees, backups,
load visibility, and a clear first-response expectation. Reviewers should compare
a change with its acceptance criteria and implementation plan, not only inspect
a wall of generated diff.

Maintain the ability to reject a change. Faster review without a quality bar
creates a feedback loop that trains both humans and agents to ship avoidable
problems.

**Completion criterion:** each review has a specific owner and the team can tell
whether the review queue is balanced.

### 7. Run a representative agent exercise

Give an agent a bounded, real task in the improved loop. It must discover the
right context, make the change, run the defined verification, and report evidence
rather than a confidence statement. Capture only durable lessons from the run.

**Completion criterion:** the exercise reaches a real pass/fail outcome without
manual, undocumented rescue steps.

## Codify Durable Learning

After a meaningful task, ask: **what would prevent the next engineer or agent
from rediscovering this?** Put the answer in the narrowest durable artifact:

| Learning | Preferred home |
| --- | --- |
| A repeatable command or environment check | Script, Make target, or documented CLI task |
| A project-wide invariant | Root `AGENTS.md` / `CLAUDE.md` or specification |
| A domain-specific convention | Closest subdirectory instruction file |
| A reusable workflow | Skill, command, or template |
| A regression that can be detected mechanically | Test, lint rule, schema, or validator |

Do not codify one-off task status, temporary workarounds, credentials, or untested
opinions. Version-control durable instructions and review them like code.

## Pitfalls

- **Standardization theater:** replacing a working tool without evidence that it
  blocks the target loop wastes effort. Prefer conventional tools when choosing
  new paths or fixing demonstrated friction.
- **CI-only proof:** a green remote pipeline is too slow and too late to be the
  only feedback source for iterative agent work.
- **More tests, same weak seam:** broad end-to-end tests do not substitute for a
  focused, deterministic behavioral check.
- **Documentation as a code paraphrase:** code explains mechanics; documentation
  must explain intent, constraints, and decisions.
- **Adoption as a mandate:** broad agent use matters only when the surrounding
  practices make it safe. Remove blockers and measure actual workflow use.
- **A review SLO without load balancing:** speed targets simply burn out the
  most responsive reviewer unless ownership is distributed.

## Verification

Before calling an improvement complete:

1. Use `Bash` to run the documented development-time command on both a passing
   and an intentionally failing case.
2. Confirm the failure is deterministic, actionable, and scoped to the changed
   behavior.
3. Confirm the relevant intent or constraint is documented where a future agent
   can discover it.
4. Inspect review assignment and queue ownership for the representative change.
5. Use `Read` and `Grep` to confirm the new command, test, or instruction is
   discoverable from the workflow’s entry point.
