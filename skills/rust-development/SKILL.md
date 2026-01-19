---
name: rust-development
description: Rust development workflow with quality gates, testing, and iteration patterns. Use when developing Rust code, running tests, or iterating on Rust projects.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---

# Rust Development Workflow

Development patterns for Rust CLI tools and libraries, based on AllBeads and QDOS workflows.

## Quality Gates

**ALL THREE must pass before commits:**

```bash
cargo fmt -- --check && cargo clippy -- -D warnings && cargo test
```

Run frequently during development, not just before commits.

## Development Loop

### 1. Check and Build

```bash
# Fast check (no codegen)
cargo check

# Full build
cargo build

# Release build
cargo build --release
```

### 2. Run Tests

```bash
# All tests
cargo test

# Specific test
cargo test test_name

# With output
cargo test -- --nocapture

# Single-threaded (for tests with shared state)
cargo test -- --test-threads=1
```

### 3. Format and Lint

```bash
# Format code
cargo fmt

# Check formatting without changing
cargo fmt -- --check

# Lint with warnings as errors
cargo clippy -- -D warnings

# Auto-fix clippy suggestions
cargo clippy --fix --allow-dirty
```

### 4. Run the Binary

```bash
# Debug build
cargo run -- [args]

# Release build
cargo run --release -- [args]

# With specific features
cargo run --features "feature1,feature2" -- [args]
```

## Project Structure

Standard Rust project layout:

```
project/
├── Cargo.toml          # Package manifest
├── Cargo.lock          # Dependency lock
├── src/
│   ├── main.rs         # Binary entry point
│   ├── lib.rs          # Library root (if both bin and lib)
│   └── module/
│       └── mod.rs
├── tests/              # Integration tests
├── benches/            # Benchmarks
└── examples/           # Example binaries
```

## Error Handling Patterns

### Application Errors (use `anyhow`)

```rust
use anyhow::{Context, Result};

fn main() -> Result<()> {
    let config = load_config()
        .context("Failed to load configuration")?;
    Ok(())
}
```

### Library Errors (use `thiserror`)

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    #[error("Invalid input: {0}")]
    InvalidInput(String),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}
```

## Dependency Management

```bash
# Add dependency
cargo add serde --features derive

# Add dev dependency
cargo add --dev tokio-test

# Update dependencies
cargo update

# Check for outdated
cargo outdated  # requires cargo-outdated
```

## Workspace Setup

For multi-crate projects:

```toml
# Cargo.toml (workspace root)
[workspace]
members = ["crate1", "crate2"]
resolver = "2"

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
```

## Performance Profiling

```bash
# Build with debug info for profiling
cargo build --release

# Time compilation
cargo build --timings

# Check binary size
cargo bloat --release  # requires cargo-bloat
```

## Build Performance

### Use mold linker (Linux)

Faster linking times:

```toml
# .cargo/config.toml
[target.'cfg(target_os = "linux")']
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
```

Install: `sudo apt install mold` or `brew install mold`

### Use sccache for caching

Cache compiler artifacts across builds:

```bash
cargo install --locked sccache
export RUSTC_WRAPPER=sccache

# Add to shell profile for persistence
echo 'export RUSTC_WRAPPER=sccache' >> ~/.zshrc
```

### Auto-derive macro

Reduce boilerplate for common derives:

```rust
macro_rules! auto_derived {
    ( $( $item:item )+ ) => {
        $(
            #[derive(Debug, Clone, PartialEq, Eq)]
            $item
        )+
    };
}

// Usage
auto_derived! {
    pub struct User {
        id: i64,
        name: String,
    }

    pub struct Config {
        host: String,
        port: u16,
    }
}
```

Add `Serialize, Deserialize` to the macro if using serde.

## Common Patterns

### Builder Pattern

```rust
pub struct Config {
    host: String,
    port: u16,
}

impl Config {
    pub fn builder() -> ConfigBuilder {
        ConfigBuilder::default()
    }
}

#[derive(Default)]
pub struct ConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
}

impl ConfigBuilder {
    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn build(self) -> Result<Config, &'static str> {
        Ok(Config {
            host: self.host.ok_or("host required")?,
            port: self.port.unwrap_or(8080),
        })
    }
}
```

### Newtype Pattern

```rust
pub struct UserId(pub i64);
pub struct Email(String);

impl Email {
    pub fn new(s: impl Into<String>) -> Result<Self, &'static str> {
        let s = s.into();
        if s.contains('@') {
            Ok(Self(s))
        } else {
            Err("invalid email")
        }
    }
}
```

## IDE Integration

For VS Code with rust-analyzer:

```json
// .vscode/settings.json
{
  "rust-analyzer.check.command": "clippy",
  "rust-analyzer.cargo.features": "all"
}
```

## Anti-Patterns

**DON'T:**
- Use `.unwrap()` in library code (use `?` instead)
- Ignore clippy warnings
- Skip `cargo fmt` before commits
- Write tests after the fact

**DO:**
- Write code that passes fmt/clippy on first write
- Use `Result<T, E>` for fallible operations
- Run tests frequently during development
- Use `#[must_use]` for important return values
