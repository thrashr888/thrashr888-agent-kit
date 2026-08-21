# Plan: <Task>

## Acceptance Criteria

- [ ] When <condition>, the system shall <observable behavior>.
- [ ] <Constraint or invariant> remains true.

## Non-Goals

- <Deliberately excluded scope>

## Risks and Decisions

- <Open decision, owner, and why it matters>

## Steps

### 1. <Named change>

- **Location:** `path/to/file.ext:line` or symbol
- **Change:** Behavior and interface change; add a concise exact snippet only
  when it removes ambiguity.
- **Reason:** Requirement or research finding this satisfies.
- **Verify:** Exact command or manual path, including expected result.
- **Risk / rollback:** Likely failure and safe recovery if relevant.

Repeat for each material change.

## Final Verification

- [ ] Targeted behavior check passes.
- [ ] Relevant tests, lint, type, build, contract, or rendering checks pass.
- [ ] Acceptance criteria were exercised directly.
- [ ] Deviations from the plan are documented.

The plan must be reviewable before code is written and executable without
reconstructing intent from a conversation transcript.
