# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**thrashr888-agent-kit** - A Claude Code plugin marketplace with development workflows, Rust tooling, and best practices.

## Project Structure

```
thrashr888-agent-kit/
├── .claude-plugin/
│   └── plugin.json          # Plugin configuration
├── skills/
│   ├── style-docs/          # 5-style documentation system
│   │   ├── SKILL.md
│   │   └── references/      # 8 document templates
│   └── github-releases/     # Release workflow
│       ├── SKILL.md
│       └── scripts/
├── CLAUDE.md                # This file
├── AGENTS.md                # Compiled agent instructions
└── README.md
```

## Adding Skills

Each skill needs:
1. Directory under `skills/`
2. `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: One-line description. Use when [triggers].
   allowed-tools: Read, Edit, Write, Bash, Grep, Glob
   ---
   ```
3. Optional `references/` for supporting docs
4. Optional `scripts/` for automation

## Skill Design Principles

- **Single purpose**: Each skill does one thing well
- **Clear triggers**: Description says when to use it
- **Prescriptive**: Step-by-step workflows, not abstract guidance
- **Code examples**: Show, don't just tell
- **Tool allowlists**: Limit scope with `allowed-tools`

## Beads Issue Tracking

This repository uses `bd` (beads) for issue tracking.

```bash
bd ready              # Show unblocked work
bd show <id>          # View issue details
bd update <id> --status=in_progress
bd close <id>
bd sync               # Sync with git
```

## Quality Guidelines

- Skills should be self-contained and testable
- Reference external resources in `references/`
- Automation scripts go in `scripts/`
- Update README when adding skills
