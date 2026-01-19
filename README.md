# thrashr888-agent-kit

A Claude Code plugin marketplace with development workflows, Rust tooling, and best practices.

## Installation

```bash
# Install via Claude Code
claude plugins install thrashr888/thrashr888-agent-kit
```

Or add to your project's `.claude/settings.local.json`:

```json
{
  "plugins": ["thrashr888/thrashr888-agent-kit"]
}
```

## Skills

### style-docs

Generate standardized project documentation using the 5-style system.

**Use when:** Creating plans, specs, skills, RFCs, ADRs, or other project documentation.

**Templates included:**
- Plan template (for Plan Mode exploration)
- Spec template (for evergreen architecture docs)
- Skill template (for agent implementation guides)
- RFC template (for formal proposals)
- ADR template (for architecture decisions)
- Bug report template
- Feature request template
- Pull request template

### github-releases

Create GitHub releases with proper versioning, changelogs, and artifacts.

**Use when:** Creating a release, tagging a version, publishing, or generating release notes.

**Features:**
- Semantic versioning guidance
- Changelog generation from git history
- Pre-release/beta workflow
- Artifact upload
- Rollback procedures

## Project Structure

```
thrashr888-agent-kit/
├── .claude-plugin/
│   └── plugin.json          # Plugin configuration
├── skills/
│   ├── style-docs/
│   │   ├── SKILL.md         # 5-style documentation system
│   │   └── references/      # 8 document templates
│   └── github-releases/
│       ├── SKILL.md         # Release workflow guide
│       └── scripts/         # Automation scripts
├── CLAUDE.md                # Agent instructions
├── AGENTS.md                # Compiled agent instructions
└── README.md                # This file
```

## The 5-Style Documentation System

| Style            | Purpose                           | Location          |
| ---------------- | --------------------------------- | ----------------- |
| 1. Plan Mode     | Deep exploration before coding    | `plans/`          |
| 2. Issues        | Track work across sessions        | `.beads/` or GH   |
| 3. Evergreen Specs | System truth ("how it works")   | `specs/`          |
| 4. Skills        | Agent guides ("how to implement") | `.claude/skills/` |
| 5. User Docs     | Human communication               | README, CLAUDE.md |

## Contributing

Skills are designed to be focused and reusable. When adding new skills:

1. Create a directory under `skills/`
2. Add `SKILL.md` with frontmatter (name, description)
3. Add `references/` for supporting docs
4. Add `scripts/` for automation helpers
5. Update this README

## License

MIT
