---
name: research-plan-implement
description: Run complex agent work through research, plans, and proof.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---

# Research, Plan, Implement, Verify

Use a phased workflow for non-trivial agent work in unfamiliar, high-risk, or
cross-cutting code. The point is not ceremony: each phase produces a compact,
reviewable artifact that lets the next phase start from verified truth rather
than a long, noisy conversation.

The workflow is **Research → Plan → Implement → Verify**, with deliberate
compaction between phases and a final **Codify** decision for durable learning.

## When to Use

Use when a task changes multiple files or systems, modifies an unfamiliar
codebase, has meaningful blast radius, needs a reviewable plan, or has failed
once because an agent reasoned from incomplete context.

Do not use full RPI for a reversible, obvious one-line change. Use a direct edit
and focused verification instead. Match process to the cost of being wrong.

## Decide the Depth First

| Task shape | Default approach | Example |
| --- | --- | --- |
| Trivial and reversible | Direct change + targeted check | Correct a label or typo |
| Simple and familiar | Short plan + check | Add an existing loading pattern |
| Medium or partially unfamiliar | Research + plan + implementation checks | Add a feature through known extension points |
| Complex, risky, or cross-service | Full RPI + explicit acceptance criteria + plan review | Change authorization or a shared data contract |
| High-impact and hard to reverse | Full RPI + design review + staged rollout plan | Replace a payment, identity, or persistence boundary |

If the task’s risk changes during research, change the workflow depth before
implementation rather than pretending the original estimate still applies.

## Artifacts and Lifetimes

| Artifact | Purpose | Lifetime |
| --- | --- | --- |
| Acceptance criteria | Define success and non-goals | Feature / task |
| Research note | Compressed snapshot of relevant code and constraints | Feature / task |
| Implementation plan | Reviewable sequence of changes and proof | Feature / task; attach to review when useful |
| Test and validation evidence | Prove outcomes independently | Retain with code or delivery record as appropriate |
| Codified learning | Prevent repeated rediscovery | Durable, only when stable and reusable |

Use `references/research-template.md` and `references/plan-template.md` as
starting points. Keep task artifacts out of root instructions unless they are
stable knowledge future work actually needs.

## Procedure

### 1. Define success before exploring solutions

Write the observable outcome, non-goals, constraints, and verification standard.
State requirements—not a guessed implementation. If a prompt says “use service
X” without an external constraint, treat X as a hypothesis to investigate.

For behavior that matters, express acceptance criteria in a condition/action
form such as: “When _condition_, the system shall _observable behavior_.”

**Completion criterion:** success has an external proof; a reviewer can tell
what is deliberately out of scope and what must not change.

### 2. Research the current system

Use `Glob`, `Grep`, and `Read` to locate entry points, trace input-to-output
flow, find analogous patterns, and identify constraints. Use a sub-agent for
broad exploration only when it can return a compact result with file paths and
line numbers.

Research must contain:

- exact file paths and line numbers;
- the relevant execution or data flow;
- existing patterns to follow;
- dependencies, contracts, and invariants to preserve; and
- open questions or evidence that is still missing.

Research must not contain implementation recommendations yet. That separation
prevents early guesses from disguising themselves as discovered facts.

**Completion criterion:** a different engineer can locate the affected code and
understand the constraints without reading the entire repository.

### 3. Compact and challenge the initial framing

Start planning from the acceptance criteria and the concise research artifact,
not the raw transcript, failed attempts, or tool dump. Ask one explicit question:
**Is the proposed direction idiomatic for this codebase and its constraints?**

If research contradicts the original framing, revise the problem statement and
acceptance criteria before planning. Do not force evidence to fit the first
prompt.

Treat context utilization as a warning signal, not a universal percentage. When
repeated corrections, unrelated history, or large tool output are steering the
conversation, compact, reset, or isolate the work in a new context.

**Completion criterion:** the plan’s premise is evidence-backed and does not
inherit an untested solution from the opening prompt.

### 4. Write an executable, reviewable plan

Create a plan with ordered steps. For each step, state:

1. **Location:** exact file path and symbol, line range, or insertion point.
2. **Change:** intended behavior and interface change; include a concise real
   snippet only where it removes ambiguity.
3. **Reason:** requirement or constraint it satisfies.
4. **Verification:** command, test, manual path, or contract check and expected
   evidence.
5. **Risk / rollback:** likely failure mode and safe recovery when relevant.

Do not write vague instructions such as “update the handler.” Do not fill the
plan with speculative implementation detail that has not been justified by the
research.

**Completion criterion:** a capable engineer can follow the plan mechanically,
and every step has a way to prove it worked.

### 5. Review the plan before generating a large diff

Review the plan against the acceptance criteria, research findings, and risks.
Correct a bad plan before it becomes hundreds of bad lines. For high-risk work,
seek a human decision at this boundary rather than asking an agent to resolve a
product or security trade-off silently.

When a plan is approved, preserve it alongside the change if it adds value to
reviewers. Reviewers should compare the final diff to the plan, not reconstruct
intent from generated code alone.

**Completion criterion:** every requirement has a planned implementation and
verification path; unresolved decisions are explicitly blocked or escalated.

### 6. Implement in verified increments

Follow the reviewed plan. At each logical boundary, run the planned verification
before moving to the next step. If evidence shows the plan is wrong, stop and
return to research or planning; do not improvise a new design mid-implementation
without recording the decision.

Use sub-agents to isolate broad investigation or independent verification—not as
personality labels such as “frontend agent” or “QA agent.” The parent should
receive a short evidence summary, not the sub-agent’s exploration transcript.

**Completion criterion:** each completed plan step has its promised evidence,
and deviations are reflected in the plan or documented decision.

### 7. Verify independently

Use deterministic tools to prove the outcome: targeted tests, type checks,
linters, schema or contract tests, builds, integration paths, or render-based
inspection for visual changes. An agent’s “done” statement is not a result.

Test the acceptance criteria directly where practical, including failure and
boundary cases. Validate the final artifact, not only intermediate source files.

**Completion criterion:** the evidence demonstrates all acceptance criteria and
reports any deliberately deferred work honestly.

### 8. Assess and codify only durable learning

After the task, ask: **what did we learn that would prevent future rediscovery?**
Codify a lesson only when it is stable, specific, and likely to recur.

| Lesson | Durable home |
| --- | --- |
| Repeated agent procedure | A skill, command, or template |
| Project-wide convention or setup fact | Root `AGENTS.md` / `CLAUDE.md` |
| Domain convention | Closest scoped instruction file |
| Stable architecture decision | ADR or specification |
| Repeatable failure | Test, lint rule, validator, or script |

Do not promote raw research notes, task status, temporary workarounds, or one-off
errors into permanent instructions. The goal is compounding clarity, not an
ever-growing context dump.

**Completion criterion:** any durable lesson has a justified home and is
validated like code; ephemeral artifacts remain scoped to the task.

## Context Hygiene

- **Give tools, not a dump.** Provide search and reading capabilities so the
  agent can discover relevant context progressively.
- **Keep handoffs compressed.** Pass exact paths, constraints, decisions, and
  evidence—not transcripts and full files.
- **Isolate exploration.** A sub-agent can read fifty files; its return should
  contain the five facts the parent needs.
- **Reset a bad trajectory.** After two or three corrections that do not improve
  the result, reframe from acceptance criteria and verified research.
- **Keep instructions scoped.** Root guidance is orientation; deeper directories
  hold local conventions and details.

## Pitfalls

- **RPI as theater:** creating artifacts without using them during review or
  implementation merely adds paperwork.
- **A plan that becomes a fossil:** when evidence changes, update the plan or
  record why it changed; do not blindly execute it.
- **Context compaction that discards constraints:** compress failed attempts away,
  but preserve requirements, decisions, and open risks.
- **Agent self-verification:** probabilistic confidence cannot replace external,
  deterministic proof.
- **Sub-agents as job titles:** use them for a bounded context boundary and a
  defined output, not an ambiguous autonomous department.
- **Over-codification:** a task-specific workaround in durable instructions makes
  future work worse, not smarter.

## Verification

Before completing a non-trivial task, confirm:

1. Acceptance criteria and non-goals were written before implementation.
2. Research names exact paths, evidence, patterns, and constraints.
3. The plan names changes, proof, and risks for every material step.
4. The final diff matches the approved plan or has documented deviations.
5. Independent tools—not the agent’s confidence—prove the outcome.
6. Any codified learning is stable, scoped, and verified.
