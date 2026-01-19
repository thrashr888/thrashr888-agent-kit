---
name: homebrew-tap
description: Manage Homebrew taps for distributing CLI tools and macOS apps. Use when creating or updating Homebrew formulas and casks.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Homebrew Tap Management

Create and maintain Homebrew taps for distributing CLI tools (Formulas) and macOS apps (Casks).

## Tap Structure

```
homebrew-myproject/
├── Formula/
│   └── mytool.rb      # CLI tools (binaries)
├── Casks/
│   └── myapp.rb       # macOS apps (.app bundles)
└── README.md
```

## Creating a Tap

```bash
# Create tap repository
mkdir homebrew-myproject
cd homebrew-myproject
git init

# Create directories
mkdir -p Formula Casks

# Create README
cat > README.md << 'EOF'
# Homebrew Tap for MyProject

## Installation

```bash
brew tap username/myproject
brew install mytool
```
EOF

# Push to GitHub
git add .
git commit -m "Initial tap setup"
gh repo create homebrew-myproject --public --source=. --push
```

## Formula (CLI Tools)

### Basic Formula

```ruby
# Formula/mytool.rb
class Mytool < Formula
  desc "Brief description of the tool"
  homepage "https://github.com/username/mytool"
  version "1.0.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/username/mytool/releases/download/v#{version}/mytool-macos-aarch64"
      sha256 "SHA256_HASH_FOR_ARM"
    end
    on_intel do
      url "https://github.com/username/mytool/releases/download/v#{version}/mytool-macos-x86_64"
      sha256 "SHA256_HASH_FOR_INTEL"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/username/mytool/releases/download/v#{version}/mytool-linux-aarch64"
      sha256 "SHA256_HASH_FOR_LINUX_ARM"
    end
    on_intel do
      url "https://github.com/username/mytool/releases/download/v#{version}/mytool-linux-x86_64"
      sha256 "SHA256_HASH_FOR_LINUX_INTEL"
    end
  end

  def install
    bin.install Dir["mytool*"].first => "mytool"
  end

  def caveats
    <<~EOS
      MyTool has been installed!

      Quick start:
        mytool --help

      Documentation: https://github.com/username/mytool
    EOS
  end

  test do
    system "#{bin}/mytool", "--version"
  end
end
```

### Formula with Dependencies

```ruby
class Mytool < Formula
  desc "Tool with dependencies"
  homepage "https://github.com/username/mytool"
  version "1.0.0"
  license "MIT"

  depends_on "openssl@3"
  depends_on "sqlite"

  # ... rest of formula
end
```

## Cask (macOS Apps)

### Basic Cask

```ruby
# Casks/myapp.rb
cask "myapp" do
  version "1.0.0"
  sha256 "SHA256_HASH_FOR_DMG"

  url "https://myapp.example.com/downloads/#{version}/MyApp.dmg"
  name "MyApp"
  desc "Description of the app"
  homepage "https://myapp.example.com"

  depends_on macos: ">= :ventura"

  app "MyApp.app"

  zap trash: [
    "~/Library/Application Support/MyApp",
    "~/Library/Preferences/com.example.MyApp.plist",
    "~/Library/Caches/com.example.MyApp",
  ]
end
```

### Cask with Sparkle Auto-Update

```ruby
cask "myapp" do
  version "1.0.0"
  sha256 "SHA256_HASH"

  url "https://myapp.example.com/downloads/#{version}/MyApp.dmg"
  name "MyApp"
  desc "App with auto-updates"
  homepage "https://myapp.example.com"

  livecheck do
    url "https://myapp.example.com/downloads/appcast.xml"
    strategy :sparkle
  end

  auto_updates true
  depends_on macos: ">= :ventura"

  app "MyApp.app"
end
```

## Updating a Release

### Get SHA256 Hash

```bash
# For remote file
curl -sL https://example.com/download/file | shasum -a 256

# For local file
shasum -a 256 /path/to/file
```

### Update Formula

```bash
# Update version and SHA256
cd ~/Workspace/homebrew-mytool

# Edit Formula/mytool.rb
#   - Update version "X.Y.Z"
#   - Update sha256 hashes for each platform

# Commit and push
git add Formula/mytool.rb
git commit -m "Update mytool to X.Y.Z"
git push
```

### Makefile Target (from ethertext)

```makefile
HOMEBREW_TAP := $(HOME)/Workspace/homebrew-mytool
VERSION := 1.0.0
SHA256_FILE := $(BUILD_DIR)/MyApp.dmg.sha256

brew-update: sha256
	@test -d "$(HOMEBREW_TAP)" || \
		(echo "Error: Homebrew tap not found at $(HOMEBREW_TAP)" && exit 1)
	@SHA=$$(cat $(SHA256_FILE)) && \
	sed -i '' "s/version \".*\"/version \"$(VERSION)\"/" $(HOMEBREW_TAP)/Casks/myapp.rb && \
	sed -i '' "s/sha256 \".*\"/sha256 \"$$SHA\"/" $(HOMEBREW_TAP)/Casks/myapp.rb
	@echo "Updated $(HOMEBREW_TAP)/Casks/myapp.rb to version $(VERSION)"
	@echo "Don't forget to commit and push the homebrew tap!"
```

## Testing

### Test Formula Locally

```bash
# Install from local tap
brew install --build-from-source ./Formula/mytool.rb

# Or tap locally and install
brew tap username/mytool ~/Workspace/homebrew-mytool
brew install mytool
```

### Test Cask Locally

```bash
# Install from local cask
brew install --cask ./Casks/myapp.rb
```

### Audit Formula

```bash
brew audit --strict ./Formula/mytool.rb
```

## User Installation

```bash
# Tap the repository
brew tap username/myproject

# Install formula
brew install mytool

# Install cask
brew install --cask myapp

# Update
brew upgrade mytool
brew upgrade --cask myapp
```

## Multi-Binary Formula

For projects with multiple binaries:

```ruby
class Mytools < Formula
  desc "Collection of tools"
  homepage "https://github.com/username/mytools"
  version "1.0.0"
  license "MIT"

  # ... url and sha256 ...

  def install
    bin.install "tool1"
    bin.install "tool2"
    bin.install "tool3"
  end

  test do
    system "#{bin}/tool1", "--version"
    system "#{bin}/tool2", "--version"
  end
end
```

## Common Issues

### SHA256 Mismatch

Re-download and recalculate:
```bash
curl -sL <url> | shasum -a 256
```

### Quarantine Issues

For unsigned binaries:
```bash
xattr -d com.apple.quarantine /usr/local/bin/mytool
```

### Version Not Updating

```bash
brew update
brew upgrade mytool
```

## Checklist: New Release

- [ ] Build and upload release artifacts
- [ ] Get SHA256 for each platform binary
- [ ] Update Formula/Cask with new version and hashes
- [ ] Test installation locally
- [ ] Commit and push tap repository
- [ ] Verify `brew upgrade` works
