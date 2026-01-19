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

### Development Skills

#### style-docs

Generate standardized project documentation using the 5-style system.

**Use when:** Creating plans, specs, skills, RFCs, ADRs, or other project documentation.

**Templates included:**
- Plan, Spec, Skill templates
- RFC, ADR templates
- Bug report, Feature request, Pull request templates

#### github-releases

Release workflows for multiple tech stacks.

**Use when:** Creating a release, tagging a version, publishing, or deploying.

**Supports:**
- Rust CLI (tag-triggered, multi-platform, Homebrew)
- macOS apps (Makefile, notarization, S3, Sparkle)
- Python/uv (EC2 deploy with health checks)
- Next.js (Vercel auto-deploy)

### Rust Skills

#### rust-development

Rust development workflow with quality gates and iteration patterns.

**Use when:** Developing Rust code, running tests, or iterating on Rust projects.

**Covers:**
- Quality gates: `cargo fmt`, `clippy`, `test`
- Error handling with `anyhow` and `thiserror`
- Common patterns (Builder, Newtype)
- IDE integration

#### rust-onboard

Set up new Rust projects with proper infrastructure.

**Use when:** Starting a new Rust project or adding CI/CD to an existing one.

**Includes:**
- GitHub Actions CI/CD workflows
- Release workflow with multi-platform builds
- Homebrew formula template
- Project structure and configuration

#### rust-release

Release Rust CLI tools with multi-platform binaries.

**Use when:** Releasing a new version of a Rust CLI tool.

**Features:**
- Multi-platform builds (Linux, macOS, Windows)
- GitHub Releases with checksums
- Homebrew tap updates
- Prerelease support (alpha, beta, rc)

#### rust-best-practices

Idiomatic Rust coding patterns and guidelines.

**Use when:** Writing Rust code, reviewing code, or learning Rust idioms.

**Covers:**
- Error handling patterns
- Ownership and borrowing
- API design (Builder, Newtype)
- Testing and documentation
- Performance considerations

## Project Structure

```
thrashr888-agent-kit/
├── .claude-plugin/
│   ├── plugin.json           # Plugin configuration
│   └── marketplace.json      # Marketplace catalog
├── skills/
│   ├── style-docs/           # Documentation templates
│   ├── github-releases/      # Release workflows
│   ├── rust-development/     # Rust dev workflow
│   ├── rust-onboard/         # Rust project setup
│   ├── rust-release/         # Rust release workflow
│   └── rust-best-practices/  # Rust coding guidelines
├── CLAUDE.md
├── AGENTS.md
└── README.md
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
2. Add `SKILL.md` with frontmatter (name, description, allowed-tools)
3. Add `references/` for supporting docs
4. Add `scripts/` for automation helpers
5. Update `marketplace.json` and this README

## License

MIT
