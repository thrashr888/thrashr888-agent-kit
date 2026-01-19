---
name: github-releases
description: Create GitHub releases with proper versioning, changelogs, and artifacts. Use when asked to create a release, tag a version, publish a release, or generate release notes from git history.
allowed-tools: Read, Edit, Bash, Grep, Glob, WebFetch
---

# GitHub Releases Workflow

Automate the release process including quality checks, version bumping, tagging, and optional package manager updates.

## Pre-Release Checklist

Before releasing, verify:

1. **Quality gates pass** (run your project's test suite):
   ```bash
   # Example for different project types
   npm test && npm run build           # Node.js
   cargo fmt -- --check && cargo clippy -- -D warnings && cargo test  # Rust
   go test ./... && go build           # Go
   pytest && python -m build           # Python
   ```

2. **All blockers closed**: Check issues/beads for the release
   ```bash
   bd show <epic-id>  # If using beads
   gh issue list --label "release-blocker"  # GitHub issues
   ```

3. **Changes committed**: `git status` shows clean working tree

## Release Process

### Step 1: Determine Version

Ask the user what version to release if not specified. Check current version:

```bash
# Get latest tag
git describe --tags --abbrev=0 2>/dev/null || echo "No tags found"

# List recent tags
git tag --sort=-v:refname | head -5
```

Determine next version using semantic versioning:
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backwards compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backwards compatible

### Step 2: Update Version (if applicable)

For projects with version files:

```bash
# Cargo.toml (Rust)
grep '^version' Cargo.toml
# Edit to: version = "X.Y.Z"

# package.json (Node.js)
npm version X.Y.Z --no-git-tag-version

# setup.py / pyproject.toml (Python)
# Edit version field
```

### Step 3: Commit Version Bump

```bash
git add .
git commit -m "Bump version to X.Y.Z"
```

### Step 4: Create Annotated Tag

Create a tag with release notes:

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z

## Highlights
- Key feature 1
- Key feature 2

## Changes
- Change 1
- Change 2

## Bug Fixes
- Fix 1"
```

### Step 5: Push to GitHub

```bash
git push && git push --tags
```

### Step 6: Create Release (if not using CI)

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z" \
  --notes "$(cat <<'EOF'
## Highlights
- Key feature 1
- Key feature 2

## Changes
- Change 1

## Bug Fixes
- Fix 1
EOF
)"
```

### Step 7: Monitor Release Build (if using CI)

```bash
gh run list --limit 3
gh run watch <run-id>
```

### Step 8: Attach Artifacts (if applicable)

```bash
# Upload release artifacts
gh release upload vX.Y.Z ./dist/artifact.tar.gz ./dist/artifact.zip

# Upload with custom names
gh release upload vX.Y.Z ./build/output.tar.gz#myproject-vX.Y.Z-linux.tar.gz
```

### Step 9: Update Release Title/Notes

```bash
gh release edit vX.Y.Z --title "vX.Y.Z - Feature 1, Feature 2" --notes "$(cat <<'EOF'
## Highlights
- Key feature 1

## Changes
- Change 1

## Bug Fixes
- Fix 1
EOF
)"
```

### Step 10: Close Release Epic (if using beads)

```bash
bd close <epic-id> --reason="Released vX.Y.Z"
bd sync
```

## Generate Changelog

Collect changes since last release:

```bash
# Changes since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# With more detail
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s (%h)"
```

Categorize changes:
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

## Release Notes Format

```markdown
## What's New

### Added
- Feature description (#PR)

### Changed
- Change description (#PR)

### Fixed
- Bug fix description (#PR)

## Breaking Changes

- Description of breaking change and migration path

## Contributors

@username, @username

## Full Changelog

https://github.com/owner/repo/compare/v1.1.0...v1.2.0
```

## Pre-release Workflow

For beta/alpha releases:

```bash
gh release create vX.Y.Z-beta.1 \
  --prerelease \
  --title "vX.Y.Z Beta 1" \
  --notes "Beta release for testing"
```

## Troubleshooting

### Workflow job stuck or cancelled

GitHub Actions runners can be unreliable. If a job is stuck:

1. Cancel the stuck workflow: `gh run cancel <run-id>`
2. Delete and recreate the tag:
   ```bash
   git push origin :refs/tags/vX.Y.Z  # Delete remote tag
   git tag -d vX.Y.Z                   # Delete local tag
   git tag -a vX.Y.Z -m "Release"      # Recreate tag
   git push origin vX.Y.Z              # Push new tag
   ```

### Test workflow changes safely

Before modifying release workflows, test with a test tag (e.g., `v0.0.0-test`).

## Rollback

If something goes wrong:

```bash
# Delete local tag
git tag -d vX.Y.Z

# Delete remote tag
git push origin :refs/tags/vX.Y.Z

# Delete release
gh release delete vX.Y.Z

# Revert commits if needed
git revert HEAD
```

## Automation Script

Use `scripts/create-release.sh` for automated releases:

```bash
./scripts/create-release.sh patch  # 1.0.0 → 1.0.1
./scripts/create-release.sh minor  # 1.0.0 → 1.1.0
./scripts/create-release.sh major  # 1.0.0 → 2.0.0
```

## Resources

- `scripts/create-release.sh`: Automated release script
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
