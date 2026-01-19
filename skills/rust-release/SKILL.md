---
name: rust-release
description: Release workflow for Rust CLI tools with multi-platform binaries, GitHub Releases, and Homebrew distribution. Use when releasing a new version of a Rust project.
allowed-tools: Read, Edit, Bash, Grep, Glob, WebFetch
---

# Rust Release Workflow

Release Rust CLI tools with multi-platform binaries, GitHub Releases, and Homebrew tap updates.

## Pre-Release Checklist

```bash
# 1. Quality gates (ALL must pass)
cargo fmt -- --check && cargo clippy -- -D warnings && cargo test

# 2. Check current version
grep '^version' Cargo.toml

# 3. Verify clean working tree
git status

# 4. Check beads for blockers (if using)
bd show <release-epic-id>
```

## Release Process

### Step 1: Update Version

Edit `Cargo.toml`:

```toml
version = "X.Y.Z"
```

Use semantic versioning:
- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes

### Step 2: Update Cargo.lock

```bash
cargo check  # Updates Cargo.lock
```

### Step 3: Commit Version Bump

```bash
git add Cargo.toml Cargo.lock
git commit -m "Bump version to X.Y.Z"
```

### Step 4: Create Annotated Tag

```bash
git tag -a vX.Y.Z -m "Project X.Y.Z Release

## Highlights
- Key feature 1
- Key feature 2

## Changes
- Change 1
- Change 2

## Bug Fixes
- Fix 1
- Fix 2"
```

### Step 5: Push to Trigger Release

```bash
git push && git push --tags
```

This triggers the GitHub Actions release workflow.

### Step 6: Monitor Build

```bash
gh run list --limit 3
gh run watch <run-id>
```

### Step 7: Update Release Notes (optional)

The workflow uses `generate_release_notes: true`, but you can customize:

```bash
gh release edit vX.Y.Z \
  --title "vX.Y.Z - Feature 1, Feature 2" \
  --notes "$(cat <<'EOF'
## Highlights
- Key feature 1

## Changes
- Change 1

## Bug Fixes
- Fix 1

## Full Changelog
https://github.com/USER/REPO/compare/vPREV...vX.Y.Z
EOF
)"
```

### Step 8: Update Homebrew Tap

After binaries are uploaded:

```bash
# Get SHA256 for macOS ARM binary
curl -sL https://github.com/USER/REPO/releases/download/vX.Y.Z/binary-macos-aarch64 | shasum -a 256

# Update formula
cd ~/Workspace/homebrew-REPO
# Edit Formula/binary.rb:
#   - Update version "X.Y.Z"
#   - Update sha256 hashes

git add Formula/binary.rb
git commit -m "Update binary to vX.Y.Z"
git push
```

### Step 9: Close Release Beads (if using)

```bash
bd close <release-epic-id> --reason="Released vX.Y.Z"
bd sync
```

## GitHub Actions Workflow

The release workflow builds for:

| Platform | Target | Notes |
|----------|--------|-------|
| Linux x86_64 | `x86_64-unknown-linux-gnu` | glibc |
| Linux x86_64 | `x86_64-unknown-linux-musl` | Static, Alpine-compatible |
| Linux ARM | `aarch64-unknown-linux-gnu` | Raspberry Pi, ARM servers |
| macOS Intel | `x86_64-apple-darwin` | Optional, runners unreliable |
| macOS ARM | `aarch64-apple-darwin` | M1/M2/M3 Macs |
| Windows | `x86_64-pc-windows-msvc` | .exe |

### Prerelease Tags

Tags containing `alpha`, `beta`, or `rc` are marked as prereleases:

```bash
git tag -a v1.0.0-beta.1 -m "Beta release"
```

## Homebrew Formula Template

```ruby
class MyTool < Formula
  desc "Tool description"
  homepage "https://github.com/USER/REPO"
  version "X.Y.Z"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/USER/REPO/releases/download/vX.Y.Z/mytool-macos-aarch64"
      sha256 "ARM_SHA256"
    end
    on_intel do
      url "https://github.com/USER/REPO/releases/download/vX.Y.Z/mytool-macos-x86_64"
      sha256 "INTEL_SHA256"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/USER/REPO/releases/download/vX.Y.Z/mytool-linux-x86_64"
      sha256 "LINUX_SHA256"
    end
    on_arm do
      url "https://github.com/USER/REPO/releases/download/vX.Y.Z/mytool-linux-aarch64"
      sha256 "LINUX_ARM_SHA256"
    end
  end

  def install
    bin.install Dir["*"].first => "mytool"
  end

  test do
    system "#{bin}/mytool", "--version"
  end
end
```

## Troubleshooting

### Stuck GitHub Actions

```bash
gh run cancel <run-id>

# Delete and recreate tag
git push origin :refs/tags/vX.Y.Z
git tag -d vX.Y.Z
git tag -a vX.Y.Z -m "Release"
git push origin vX.Y.Z
```

### macOS Runner Issues

macOS runners (especially Intel) can be unreliable. Options:
- Remove x86_64-apple-darwin from matrix
- Use `macos-14` for ARM builds
- Accept occasional failures and re-run

### Cross-Compilation Failures

For Linux ARM:
```yaml
- name: Install cross-compilation tools
  if: matrix.target == 'aarch64-unknown-linux-gnu'
  run: |
    sudo apt-get update
    sudo apt-get install -y gcc-aarch64-linux-gnu
```

For musl:
```yaml
- name: Install musl tools
  if: matrix.target == 'x86_64-unknown-linux-musl'
  run: |
    sudo apt-get update
    sudo apt-get install -y musl-tools
```

## Rollback

```bash
# Delete local tag
git tag -d vX.Y.Z

# Delete remote tag
git push origin :refs/tags/vX.Y.Z

# Delete release
gh release delete vX.Y.Z --yes

# Revert version bump
git revert HEAD
git push
```

## Release Checklist

- [ ] Quality gates pass
- [ ] Version updated in Cargo.toml
- [ ] Cargo.lock updated
- [ ] Version bump committed
- [ ] Annotated tag created with release notes
- [ ] Tag pushed, workflow triggered
- [ ] Release build succeeded
- [ ] Release notes finalized
- [ ] Homebrew formula updated
- [ ] Beads closed and synced
