#!/bin/bash
set -euo pipefail

# GitHub Release Creation Script
# Usage: ./create-release.sh [major|minor|patch] [--prerelease]

VERSION_TYPE="${1:-patch}"
PRERELEASE="${2:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prerequisites() {
    if ! command -v gh &> /dev/null; then
        log_error "gh CLI not found. Install: https://cli.github.com/"
        exit 1
    fi

    if ! gh auth status &> /dev/null; then
        log_error "gh CLI not authenticated. Run: gh auth login"
        exit 1
    fi

    if ! git rev-parse --is-inside-work-tree &> /dev/null; then
        log_error "Not in a git repository"
        exit 1
    fi

    if [[ -n $(git status --porcelain) ]]; then
        log_error "Working tree is not clean. Commit or stash changes first."
        exit 1
    fi
}

# Get current version from latest tag
get_current_version() {
    local tag
    tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
    echo "${tag#v}"
}

# Increment version
increment_version() {
    local version="$1"
    local type="$2"

    IFS='.' read -r major minor patch <<< "$version"

    case "$type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            log_error "Invalid version type: $type (use major, minor, or patch)"
            exit 1
            ;;
    esac

    echo "${major}.${minor}.${patch}"
}

# Generate changelog
generate_changelog() {
    local last_tag="$1"

    echo "## What's Changed"
    echo ""

    if git rev-parse "$last_tag" &>/dev/null; then
        git log "${last_tag}..HEAD" --pretty=format:"- %s (%h)" --no-merges
    else
        git log --pretty=format:"- %s (%h)" --no-merges | head -20
    fi

    echo ""
    echo ""
    echo "**Full Changelog**: https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/compare/${last_tag}...v${NEW_VERSION}"
}

# Main
main() {
    check_prerequisites

    CURRENT_VERSION=$(get_current_version)
    NEW_VERSION=$(increment_version "$CURRENT_VERSION" "$VERSION_TYPE")

    log_info "Current version: v${CURRENT_VERSION}"
    log_info "New version: v${NEW_VERSION}"

    # Generate changelog
    CHANGELOG=$(generate_changelog "v${CURRENT_VERSION}")

    echo ""
    echo "=== Changelog Preview ==="
    echo "$CHANGELOG"
    echo "========================="
    echo ""

    # Confirm
    read -p "Create release v${NEW_VERSION}? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warn "Release cancelled"
        exit 0
    fi

    # Create release
    RELEASE_FLAGS=""
    if [[ "$PRERELEASE" == "--prerelease" ]]; then
        RELEASE_FLAGS="--prerelease"
    fi

    log_info "Creating release v${NEW_VERSION}..."

    gh release create "v${NEW_VERSION}" \
        --title "v${NEW_VERSION}" \
        --notes "$CHANGELOG" \
        $RELEASE_FLAGS

    log_info "Release v${NEW_VERSION} created successfully!"
    log_info "View at: $(gh release view "v${NEW_VERSION}" --json url -q .url)"
}

main
