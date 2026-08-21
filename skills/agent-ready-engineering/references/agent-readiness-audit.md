# Agent-Readiness Audit

Use this checklist for one real engineering loop. Record evidence—command
output, path, screenshot, or named owner—not a subjective score.

## Scope

- **Workflow:** What change is the engineer or agent trying to make?
- **Risk:** What happens if the workflow is wrong, slow, or unreproducible?
- **Entry point:** Where does the workflow begin?
- **Current loop time:** How long does the first useful feedback take?

## Foundation Checklist

### Standard tooling

- [ ] The language, package manager, build tool, and formatter follow an
  ecosystem convention or document a justified deviation.
- [ ] A fresh checkout can bootstrap from repo instructions.
- [ ] Lockfiles and versions are explicit where they affect reproducibility.

### Development-time control

- [ ] Build, targeted test, lint, and type check have terminal commands.
- [ ] Critical dev actions expose a CLI or API instead of a GUI-only path.
- [ ] The command supports a focused scope for the workflow being changed.

### Deterministic validation

- [ ] A passing run is repeatable with the same inputs.
- [ ] An invalid input or change fails predictably.
- [ ] Failure output names the violated condition and likely location.
- [ ] The focused check returns quickly enough to drive iteration.

### Structure and testability

- [ ] Dependencies are explicit at the point of use.
- [ ] The behavior can be exercised without unrelated infrastructure.
- [ ] Tests assert observable behavior or a stated invariant.
- [ ] The module boundary and side effects are clear.

### Written intent

- [ ] Acceptance criteria are written before implementation begins.
- [ ] External contracts, policy, regulatory, or business constraints are
  discoverable.
- [ ] A non-obvious decision has rationale, not merely an outcome.

### Review capacity and quality

- [ ] A specific reviewer and fallback are assigned.
- [ ] The team can see queue ownership and first-response time.
- [ ] The review checks evidence against requirements and plan.
- [ ] The process can reject changes that do not meet the bar.

## Prioritization

| Finding | Prioritize when | First intervention |
| --- | --- | --- |
| GUI-only or CI-only critical action | Agents must repeat it while iterating | Expose a bounded CLI/API operation |
| Slow or opaque validation | Failure diagnosis dominates edit time | Add a focused local check with actionable output |
| Untestable behavior | Agent output cannot be trusted | Introduce a seam and behavior-level test |
| Missing rationale or contract | Agent is technically correct but contextually wrong | Capture requirement, constraint, or ADR |
| Review overload | Generated PR volume grows faster than review | Name owners, balance work, and set a response expectation |
