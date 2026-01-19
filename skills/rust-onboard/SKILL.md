---
name: rust-onboard
description: Onboard a new Rust project with standard tooling, CI/CD, and best practices. Use when starting a new Rust project or setting up an existing one with proper infrastructure.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---

# Rust Project Onboarding

Set up a new Rust project with standard tooling, CI/CD, and release automation.

## Quick Start

### New Project

```bash
# Binary project
cargo new my-project
cd my-project

# Library project
cargo new --lib my-lib
```

### Existing Project

```bash
cd existing-project
cargo init  # Creates Cargo.toml if missing
```

## Essential Setup

### 1. Cargo.toml Configuration

```toml
[package]
name = "my-project"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
description = "Brief description"
license = "MIT"
repository = "https://github.com/user/repo"
readme = "README.md"
keywords = ["keyword1", "keyword2"]
categories = ["command-line-utilities"]

[dependencies]
# Add your dependencies

[dev-dependencies]
# Test dependencies

[profile.release]
lto = true
strip = true
```

### 2. Rust Toolchain

```bash
# Install stable toolchain
rustup default stable

# Add components
rustup component add rustfmt clippy

# For cross-compilation
rustup target add aarch64-apple-darwin
rustup target add x86_64-unknown-linux-gnu
```

### 3. Editor Config

Create `.editorconfig`:

```ini
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

### 4. Git Setup

Create `.gitignore`:

```gitignore
/target/
Cargo.lock  # Remove this line for binaries
*.swp
*.swo
.DS_Store
.env
```

**Note:** Commit `Cargo.lock` for binaries, ignore for libraries.

## CI/CD Setup

### GitHub Actions CI

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  CARGO_TERM_COLOR: always

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt, clippy

      - name: Format check
        run: cargo fmt -- --check

      - name: Clippy
        run: cargo clippy -- -D warnings

      - name: Test
        run: cargo test

      - name: Build
        run: cargo build --release
```

### GitHub Actions Release

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

env:
  CARGO_TERM_COLOR: always

jobs:
  build:
    name: Build ${{ matrix.target }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - target: x86_64-unknown-linux-gnu
            os: ubuntu-latest
            artifact_name: my-project
            asset_name: my-project-linux-x86_64

          - target: aarch64-apple-darwin
            os: macos-latest
            artifact_name: my-project
            asset_name: my-project-macos-aarch64

          - target: x86_64-pc-windows-msvc
            os: windows-latest
            artifact_name: my-project.exe
            asset_name: my-project-windows-x86_64.exe

    steps:
      - uses: actions/checkout@v4

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}

      - name: Build
        run: cargo build --release --target ${{ matrix.target }}

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.asset_name }}
          path: target/${{ matrix.target }}/release/${{ matrix.artifact_name }}

  release:
    name: Create Release
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts

      - name: Prepare assets
        run: |
          mkdir -p release
          for dir in artifacts/*/; do
            name=$(basename "$dir")
            cp "$dir"/* "release/$name"
            chmod +x "release/$name" 2>/dev/null || true
          done

      - name: Create checksums
        run: |
          cd release
          sha256sum * > checksums.txt

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: release/*
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Homebrew Distribution

### Create Formula

In a separate `homebrew-myproject` repo, create `Formula/myproject.rb`:

```ruby
class Myproject < Formula
  desc "Brief description"
  homepage "https://github.com/user/myproject"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/user/myproject/releases/download/v#{version}/myproject-macos-aarch64"
      sha256 "SHA256_HASH_HERE"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/user/myproject/releases/download/v#{version}/myproject-linux-x86_64"
      sha256 "SHA256_HASH_HERE"
    end
  end

  def install
    bin.install Dir["*"].first => "myproject"
  end

  test do
    system "#{bin}/myproject", "--version"
  end
end
```

## Documentation

### README.md Template

```markdown
# Project Name

Brief description.

## Installation

### Homebrew (macOS/Linux)

\`\`\`bash
brew install user/tap/myproject
\`\`\`

### From Source

\`\`\`bash
cargo install --git https://github.com/user/myproject
\`\`\`

## Usage

\`\`\`bash
myproject [OPTIONS] <ARGS>
\`\`\`

## Development

\`\`\`bash
# Run tests
cargo test

# Build release
cargo build --release
\`\`\`

## License

MIT
```

## Onboarding Checklist

- [ ] `Cargo.toml` with proper metadata
- [ ] `.gitignore` configured
- [ ] `.editorconfig` for consistency
- [ ] `README.md` with usage
- [ ] `.github/workflows/ci.yml` for CI
- [ ] `.github/workflows/release.yml` for releases
- [ ] Homebrew formula (for distribution)
- [ ] Initial tests written
- [ ] Quality gates pass (`cargo fmt && cargo clippy && cargo test`)

## Beads Integration

If using beads for issue tracking:

```bash
bd init
bd create --title="Initial release" --type=feature --priority=1
```
