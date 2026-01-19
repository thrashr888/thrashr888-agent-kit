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

## Skills (10 total)

### Development

| Skill | Description |
|-------|-------------|
| **style-docs** | 5-style documentation system (plans, specs, skills, RFCs, ADRs) |
| **github-releases** | Release workflows for Rust, macOS apps, Python/uv, Next.js |
| **makefile-patterns** | Makefile patterns for dev, build, test, and release automation |

### Rust

| Skill | Description |
|-------|-------------|
| **rust-development** | Quality gates, testing, iteration patterns |
| **rust-onboard** | Project setup with CI/CD and Homebrew |
| **rust-release** | Multi-platform builds, GitHub Releases, Homebrew taps |
| **rust-best-practices** | Idiomatic patterns, error handling, API design |

### Python

| Skill | Description |
|-------|-------------|
| **python-uv** | Modern Python with uv, pytest, FastAPI, Django, EC2 deploy |

### Infrastructure

| Skill | Description |
|-------|-------------|
| **hcp-terraform** | HCP Terraform (Terraform Cloud) remote plan/apply workflow |
| **homebrew-tap** | Manage Homebrew formulas and casks for distribution |

## Skill Details

### style-docs

Generate standardized project documentation using the 5-style system.

**Use when:** Creating plans, specs, skills, RFCs, ADRs, or other project documentation.

### github-releases

Release workflows for multiple tech stacks.

**Supports:**
- Rust CLI (tag-triggered, multi-platform, Homebrew)
- macOS apps (Makefile, notarization, S3, Sparkle)
- Python/uv (EC2 deploy with health checks)
- Next.js (Vercel auto-deploy)

### python-uv

Modern Python development with uv package manager.

**Use when:** Working on Python projects using uv, pytest, FastAPI, or Django.

**Covers:**
- uv sync, add, run commands
- pytest testing patterns
- FastAPI/Django development
- EC2 deployment with health checks
- GitHub Actions CI

### hcp-terraform

HCP Terraform (Terraform Cloud) workflow.

**Use when:** Working with Terraform that runs remotely in HCP Terraform.

**Key constraint:** Cannot apply locally - all plans/applies run in HCP Terraform.

### homebrew-tap

Manage Homebrew taps for distributing software.

**Use when:** Creating or updating Homebrew formulas (CLI tools) or casks (macOS apps).

### makefile-patterns

Common Makefile patterns for automation.

**Use when:** Creating or understanding Makefiles for build, test, and release workflows.

**Includes:**
- Dev loop (kill, build, run)
- Rust, Xcode, Python build patterns
- DMG creation, S3 upload
- Homebrew tap updates
- Git tagging

## Project Structure

```
thrashr888-agent-kit/
├── .claude-plugin/
│   ├── plugin.json           # Plugin configuration
│   └── marketplace.json      # Marketplace catalog (10 plugins)
├── skills/
│   ├── style-docs/           # Documentation templates
│   ├── github-releases/      # Release workflows
│   ├── makefile-patterns/    # Makefile automation
│   ├── rust-development/     # Rust dev workflow
│   ├── rust-onboard/         # Rust project setup
│   ├── rust-release/         # Rust release workflow
│   ├── rust-best-practices/  # Rust coding guidelines
│   ├── python-uv/            # Python/uv development
│   ├── hcp-terraform/        # Terraform Cloud workflow
│   └── homebrew-tap/         # Homebrew distribution
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
