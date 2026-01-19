---
name: style-docs
description: Generate standardized project documentation using the 5-style system. Use when asked to create plans, specs, skills, RFCs, ADRs, or other project documentation. Ensures consistent, high-quality documentation across the codebase.
---

# 5-Style Documentation System

Use this skill when creating project documentation, planning features, or organizing technical decisions.

## The 5 Documentation Styles

| Style              | Purpose                           | Location          | Update Trigger       |
| ------------------ | --------------------------------- | ----------------- | -------------------- |
| 1. Plan Mode       | Deep exploration before coding    | `plans/`          | Per feature          |
| 2. Issues          | Track work across sessions        | `.beads/` or GH   | Throughout feature   |
| 3. Evergreen Specs | System truth ("how it works")     | `specs/`          | Architecture changes |
| 4. Skills          | Agent guides ("how to implement") | `.claude/skills/` | Pattern changes      |
| 5. User Docs       | Human communication               | README, CLAUDE.md | Major features       |

## When to Use Each Style

### Style 1: Plan Mode (plans/)

**Purpose:** Explore and design before coding

**When to use:**
- Starting a non-trivial feature
- Making architectural decisions
- Complex refactoring

**File naming:** `plans/YYYY-MM-DD-feature-name.md`

**Template:** See `references/plan-template.md`

### Style 2: Issues (.beads/ or GitHub)

**Purpose:** Track work items and dependencies

**When to use:**
- Work spans multiple sessions
- Feature has dependencies
- Need to track blockers

**Commands:**
```bash
bd create --title="..." --type=task|bug|feature --priority=2
bd update <id> --status=in_progress
bd close <id>
```

### Style 3: Specs (specs/)

**Purpose:** Document architectural truth - WHAT the system does

**When to use:**
- Architecture changes
- New subsystems added
- Core patterns established

**Characteristics:**
- Declarative, not prescriptive
- Evergreen (rarely becomes stale)
- Describes constraints and invariants

**Template:** See `references/spec-template.md`

### Style 4: Skills (.claude/skills/)

**Purpose:** Guide agents on HOW to implement

**When to use:**
- New implementation patterns
- Workflow documentation
- Agent guidance needed

**Characteristics:**
- Prescriptive (step-by-step)
- Code examples
- Tool allowlists

**Template:** See `references/skill-template.md`

### Style 5: User Docs (README, CLAUDE.md)

**Purpose:** Human-facing communication

**When to use:**
- Public-facing changes
- Getting started guides
- API documentation

**Files:**
- `README.md`: Project overview, installation
- `CLAUDE.md`: Agent instructions
- `AGENTS.md`: Compiled agent instructions

## Decision Framework

| Situation                  | Action                            |
| -------------------------- | --------------------------------- |
| Starting new feature       | Enter plan mode → write to plans/ |
| Feature spans sessions     | Create beads issue                |
| New architectural pattern  | Update spec in `specs/`           |
| New implementation pattern | Update skill in `.claude/skills/` |
| Public-facing change       | Update README.md                  |
| Agent guidance needed      | Update CLAUDE.md                  |

## Additional Templates

For specific use cases:

- **RFC** (`references/rfc-template.md`): Formal proposals needing team input
- **ADR** (`references/adr-template.md`): Architecture decision records
- **Bug Report** (`references/bug-report-template.md`): Bug documentation
- **Feature Request** (`references/feature-request-template.md`): Feature proposals
- **Pull Request** (`references/pull-request-template.md`): PR descriptions

## Anti-Patterns

**DON'T:**
- Write RFC-style docs that get stale ("We plan to add X")
- Document temporary decisions in specs (use issues)
- Put implementation details in specs (use skills)
- Put architectural constraints in skills (use specs)

**DO:**
- Keep specs declarative and evergreen
- Keep skills prescriptive and code-focused
- Track multi-session work in issues
- Update docs when patterns change

## Resources

All templates available in `references/`:
- `plan-template.md` - Plan mode template
- `spec-template.md` - Evergreen spec template
- `skill-template.md` - Skill document template
- `rfc-template.md` - RFC template
- `adr-template.md` - ADR template
- `bug-report-template.md` - Bug report template
- `feature-request-template.md` - Feature request template
- `pull-request-template.md` - PR description template
