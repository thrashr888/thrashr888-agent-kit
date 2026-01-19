---
name: github-releases
description: Create releases for Rust CLI tools, macOS apps, Python/uv projects, and Next.js apps. Use when asked to release, tag, ship, publish, or deploy any project.
allowed-tools: Read, Edit, Bash, Grep, Glob, WebFetch
---

# Release Workflows

Project-specific release workflows covering Rust CLI tools, macOS apps, Python/uv deployments, and Next.js apps.

## Quick Reference: Which Workflow?

| Project Type | Workflow | Trigger |
|-------------|----------|---------|
| Rust CLI (AllBeads, QDOS) | Tag-triggered CI | `git tag -a vX.Y.Z` → GitHub Actions builds binaries |
| macOS App (ethertext, AllBeadsApp) | Makefile-driven | `make archive` → notarize → `make release` |
| Python/uv (rookery) | CI Deploy | Push to main → tests pass → auto-deploy to EC2 |
| Next.js (AllBeadsWeb) | Vercel | Push to main → auto-deploy |

---

## Rust CLI Release (AllBeads, QDOS)

### Pre-Release Checklist

```bash
# Quality gates (ALL must pass)
cargo fmt -- --check && cargo clippy -- -D warnings && cargo test

# Check current version
grep '^version' Cargo.toml

# Verify clean working tree
git status
```

### Release Process

1. **Update version in Cargo.toml**
   ```toml
   version = "X.Y.Z"
   ```

2. **Commit version bump**
   ```bash
   git add Cargo.toml Cargo.lock
   git commit -m "Bump version to X.Y.Z"
   ```

3. **Create annotated tag** (triggers CI release)
   ```bash
   git tag -a vX.Y.Z -m "AllBeads X.Y.Z Release

   ## Highlights
   - Key feature 1

   ## Changes
   - Change 1

   ## Bug Fixes
   - Fix 1"
   ```

4. **Push to trigger release**
   ```bash
   git push && git push --tags
   ```

5. **Monitor release build**
   ```bash
   gh run list --limit 3
   gh run watch <run-id>
   ```

6. **Update release title/notes** (optional)
   ```bash
   gh release edit vX.Y.Z --title "vX.Y.Z - Feature 1, Feature 2"
   ```

7. **Update Homebrew tap** (manual)
   ```bash
   # Get SHA256 for macOS binary
   curl -sL https://github.com/USER/REPO/releases/download/vX.Y.Z/binary-macos-aarch64 | shasum -a 256

   # Update homebrew-REPO/Formula/binary.rb
   # - Update version "X.Y.Z"
   # - Update sha256 hash
   cd ~/Workspace/homebrew-REPO
   git add . && git commit -m "Update to vX.Y.Z" && git push
   ```

### GitHub Actions Workflow

The release workflow builds multi-platform binaries:
- Linux x86_64 (glibc + musl)
- Linux aarch64
- macOS x86_64 + aarch64
- Windows x86_64

Prerelease detection: tags containing `alpha`, `beta`, or `rc` are marked as prereleases.

---

## macOS App Release (ethertext, AllBeadsApp)

### Prerequisites

- Xcode with valid signing identity
- `create-dmg` installed: `brew install create-dmg`
- AWS CLI configured for S3 uploads
- Sparkle for auto-updates: `brew install --cask sparkle`

### Release Process

1. **Update version in Xcode**
   - Set `MARKETING_VERSION` in project settings

2. **Create Xcode archive**
   ```bash
   make archive
   ```

3. **Notarize in Xcode Organizer**
   - Distribute App → Developer ID → Upload
   - Wait for notarization
   - Export notarized app to `~/Downloads/`

4. **Run release**
   ```bash
   make release
   ```
   This:
   - Creates DMG from exported app
   - Uploads to S3 (versioned + latest)
   - Generates Sparkle appcast.xml
   - Updates Homebrew Cask

5. **Commit and push**
   ```bash
   git add -A && git commit -m "Release $(VERSION)" && git push
   make tag && git push --tags

   # Push homebrew tap
   cd ~/Workspace/homebrew-APPNAME
   git add -A && git commit -m "Update to $(VERSION)" && git push
   ```

### Makefile Targets

| Target | Description |
|--------|-------------|
| `make version` | Show current version |
| `make archive` | Create Xcode archive |
| `make dmg` | Create DMG from exported app |
| `make upload` | Upload DMG to S3 |
| `make appcast` | Generate Sparkle appcast.xml |
| `make brew-update` | Update Homebrew cask |
| `make release` | Full release (upload + appcast + brew) |
| `make tag` | Create git tag |

### Sparkle Setup (Auto-Updates)

```bash
make install-sparkle  # Install tools + generate keys
make sparkle-pubkey   # Show public key for Info.plist
make sparkle-sign     # Sign DMG for appcast
```

---

## Python/uv Deploy (rookery)

Continuous deployment triggered by successful tests.

### Deployment Flow

1. Push to main
2. GitHub Actions runs `pytest`
3. On success, triggers deploy workflow
4. SSH deploy to EC2:
   - Rsync files
   - `uv sync` dependencies
   - `alembic upgrade head` migrations
   - Restart systemd service
   - Health check (5 retries)

### Manual Deploy

```bash
# Trigger deploy workflow manually
gh workflow run deploy.yml
```

### Version Tracking

Deployments are stamped with build version:
```bash
printf "%s\n" "$(date -u +%Y%m%dT%H%M%SZ)_$(git rev-parse --short HEAD)" > VERSION
```

---

## Next.js/Vercel Deploy (AllBeadsWeb)

Auto-deploy on push to main. No manual release process.

### CI Workflow

```bash
bun install
bun run typecheck
bun run test
```

Vercel handles deployment automatically.

---

## Troubleshooting

### Stuck GitHub Actions workflow

```bash
gh run cancel <run-id>

# Delete and recreate tag
git push origin :refs/tags/vX.Y.Z
git tag -d vX.Y.Z
git tag -a vX.Y.Z -m "Release"
git push origin vX.Y.Z
```

### Rollback

```bash
# Delete tag
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z

# Delete release
gh release delete vX.Y.Z

# Revert if needed
git revert HEAD
```

### macOS app not notarized

Export from Xcode Organizer ensures stapling. Verify with:
```bash
xcrun stapler validate ~/Downloads/AppName.app
```

---

## Resources

- `scripts/create-release.sh`: Automated Rust release script
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Sparkle Documentation](https://sparkle-project.org/)
