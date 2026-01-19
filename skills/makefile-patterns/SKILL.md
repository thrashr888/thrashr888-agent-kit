---
name: makefile-patterns
description: Makefile patterns for development workflows. Use when creating or understanding Makefiles for build automation, release workflows, and development iteration.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Makefile Patterns

Common Makefile patterns for development, building, testing, and releasing.

## Basic Structure

```makefile
# Variables at top
PROJECT := myproject
VERSION := $(shell cat VERSION 2>/dev/null || echo "0.0.0")
BUILD_DIR := ./build

# Default target (first target)
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build    - Build the project"
	@echo "  test     - Run tests"
	@echo "  clean    - Clean build artifacts"

# Actual targets
.PHONY: build test clean
build:
	@echo "Building $(PROJECT) $(VERSION)..."

test:
	@echo "Running tests..."

clean:
	rm -rf $(BUILD_DIR)
```

## Variable Patterns

### Environment with Defaults

```makefile
# Use env var if set, otherwise default
CONFIG ?= Release
PORT ?= 8080

# Computed from shell
VERSION := $(shell git describe --tags --always 2>/dev/null || echo "dev")
GIT_SHA := $(shell git rev-parse --short HEAD)
BUILD_TIME := $(shell date -u +%Y%m%dT%H%M%SZ)
```

### Conditional Variables

```makefile
# Platform-specific
ifeq ($(shell uname),Darwin)
    OS := macos
    SED := sed -i ''
else
    OS := linux
    SED := sed -i
endif
```

## Help Target

### Self-Documenting Help

```makefile
.PHONY: help
help:
	@echo "Development:"
	@echo "  dev       - Start development server"
	@echo "  build     - Build for production"
	@echo "  test      - Run tests"
	@echo ""
	@echo "Release:"
	@echo "  release   - Full release workflow"
	@echo "  tag       - Create git tag"
	@echo ""
	@echo "Utilities:"
	@echo "  clean     - Clean build artifacts"
	@echo "  version   - Show current version"
```

### Grep-Based Help (auto-generates from comments)

```makefile
.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build the project
	...

test: ## Run tests
	...
```

## Development Patterns

### Dev Loop (Kill, Build, Run)

```makefile
APP_NAME := MyApp
APP := $(BUILD_DIR)/$(APP_NAME).app

.PHONY: dev kill run
dev: kill build run ## Quick dev iteration

kill: ## Stop running app
	@echo "Stopping $(APP_NAME)..."
	@pkill -x "$(APP_NAME)" 2>/dev/null || true
	@sleep 0.5

run: ## Run the app
	@echo "Starting $(APP_NAME)..."
	@open $(APP)
```

### Watch Mode

```makefile
.PHONY: watch
watch: ## Watch for changes and rebuild
	@echo "Watching for changes..."
	@fswatch -o src/ | xargs -n1 -I{} make build
```

## Build Patterns

### Rust Build

```makefile
.PHONY: build build-release
build: ## Debug build
	cargo build

build-release: ## Release build
	cargo build --release

check: ## Fast syntax check
	cargo check

fmt: ## Format code
	cargo fmt

lint: ## Lint with clippy
	cargo clippy -- -D warnings

test: ## Run tests
	cargo test

# Quality gate (run before commits)
.PHONY: qa
qa: fmt lint test ## Run all quality checks
```

### Xcode Build

```makefile
DEVELOPER_DIR ?= /Applications/Xcode.app/Contents/Developer
PROJECT := ./MyApp.xcodeproj
SCHEME := MyApp
CONFIG ?= Debug
BUILD_DIR := ./build
DEST := platform=macOS

.PHONY: build
build: deps ## Build the app
	DEVELOPER_DIR=$(DEVELOPER_DIR) xcodebuild -project $(PROJECT) \
	  -scheme $(SCHEME) -configuration $(CONFIG) \
	  -derivedDataPath $(BUILD_DIR) -destination '$(DEST)' \
	  build | cat

deps: ## Resolve dependencies
	DEVELOPER_DIR=$(DEVELOPER_DIR) xcodebuild -resolvePackageDependencies \
	  -project $(PROJECT) | cat

archive: ## Create release archive
	DEVELOPER_DIR=$(DEVELOPER_DIR) xcodebuild -project $(PROJECT) \
	  -scheme $(SCHEME) -configuration Release \
	  -archivePath $(BUILD_DIR)/$(SCHEME).xcarchive \
	  archive | cat
```

### Python/uv Build

```makefile
.PHONY: install test lint fmt
install: ## Install dependencies
	uv sync --dev

test: ## Run tests
	uv run pytest

lint: ## Run linter
	uv run ruff check .

fmt: ## Format code
	uv run black .
	uv run isort .
```

## Release Patterns

### DMG Creation (macOS)

```makefile
DMG_NAME := MyApp
DMG_DIR := $(BUILD_DIR)/dmg
DMG_FILE := $(BUILD_DIR)/$(DMG_NAME).dmg
EXPORTED_APP := $(HOME)/Downloads/MyApp.app

.PHONY: dmg
dmg: ## Create DMG installer
	@test -d "$(EXPORTED_APP)" || \
		(echo "Error: Export app from Xcode first" && exit 1)
	rm -rf $(DMG_DIR) $(DMG_FILE)
	mkdir -p $(DMG_DIR)
	cp -R $(EXPORTED_APP) $(DMG_DIR)/
	create-dmg \
	  --volname "$(DMG_NAME)" \
	  --window-pos 200 120 \
	  --window-size 600 400 \
	  --icon-size 100 \
	  --icon "MyApp.app" 150 190 \
	  --app-drop-link 450 190 \
	  $(DMG_FILE) $(DMG_DIR)
```

### SHA256 and Upload

```makefile
SHA256_FILE := $(BUILD_DIR)/MyApp.dmg.sha256
S3_BUCKET := my-bucket

.PHONY: sha256 upload
sha256: dmg ## Generate SHA256
	shasum -a 256 $(DMG_FILE) | awk '{print $$1}' > $(SHA256_FILE)
	@echo "SHA256: $$(cat $(SHA256_FILE))"

upload: sha256 ## Upload to S3
	aws s3 cp $(DMG_FILE) s3://$(S3_BUCKET)/downloads/$(VERSION)/MyApp.dmg --acl public-read
	aws s3 cp $(SHA256_FILE) s3://$(S3_BUCKET)/downloads/$(VERSION)/MyApp.dmg.sha256 --acl public-read
```

### Homebrew Update

```makefile
HOMEBREW_TAP := $(HOME)/Workspace/homebrew-myapp

.PHONY: brew-update
brew-update: sha256 ## Update Homebrew tap
	@test -d "$(HOMEBREW_TAP)" || (echo "Error: Tap not found" && exit 1)
	@SHA=$$(cat $(SHA256_FILE)) && \
	$(SED) "s/version \".*\"/version \"$(VERSION)\"/" $(HOMEBREW_TAP)/Casks/myapp.rb && \
	$(SED) "s/sha256 \".*\"/sha256 \"$$SHA\"/" $(HOMEBREW_TAP)/Casks/myapp.rb
	@echo "Updated tap to $(VERSION)"
```

### Git Tag

```makefile
.PHONY: tag
tag: ## Create git tag
	@if git rev-parse "v$(VERSION)" >/dev/null 2>&1; then \
		echo "Tag v$(VERSION) already exists"; \
	else \
		git tag -a "v$(VERSION)" -m "Release $(VERSION)" && \
		echo "Created tag v$(VERSION)"; \
	fi
```

### Full Release

```makefile
.PHONY: release
release: upload brew-update ## Full release workflow
	@echo ""
	@echo "=== Release $(VERSION) complete ==="
	@echo "Next steps:"
	@echo "  1. git commit -m 'Release $(VERSION)' && git push"
	@echo "  2. make tag && git push --tags"
	@echo "  3. cd $(HOMEBREW_TAP) && git commit -m 'Update to $(VERSION)' && git push"
```

## Utility Patterns

### Check Prerequisites

```makefile
.PHONY: check-aws
check-aws: ## Verify AWS credentials
	@aws sts get-caller-identity > /dev/null 2>&1 || \
		(echo "Error: AWS not configured. Run 'aws configure'" && exit 1)
	@echo "AWS credentials OK"
```

### Version Display

```makefile
.PHONY: version
version: ## Show current version
	@echo "Version: $(VERSION)"
	@echo "Git SHA: $(GIT_SHA)"
	@echo "Build:   $(BUILD_TIME)"
```

### Clean

```makefile
.PHONY: clean clean-all
clean: ## Clean build artifacts
	rm -rf $(BUILD_DIR)

clean-all: clean ## Clean everything including dependencies
	rm -rf node_modules .venv __pycache__
```

## Anti-Patterns

**DON'T:**
- Use tabs inconsistently (Makefiles require tabs for recipes)
- Forget `.PHONY` for non-file targets
- Use `cd` without `&&` (each line runs in new shell)
- Hardcode paths that vary by machine

**DO:**
- Use `?=` for overridable defaults
- Add `| cat` to Xcode commands (prevents xcpretty issues)
- Quote variables that might have spaces
- Use `@` prefix to hide command echo when appropriate
