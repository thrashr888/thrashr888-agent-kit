---
name: shipping-tauri-apps
description: Build, code-sign, notarize, and release Tauri 2 desktop apps on macOS (Rust backend + web frontend), including dev-loop gotchas (capabilities/ACL, watcher, cargo patches) and CI fallbacks. Use when working on a Tauri app's release pipeline, Apple signing/notarization, GitHub Actions for macOS builds, or debugging a Tauri dev loop. Distilled from shipping Alchemy (a local NotebookLM clone).
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Shipping Tauri desktop apps (macOS)

Hard-won playbook. Most of the pain is **Apple code-signing/notarization**, not Tauri —
it hits every desktop toolchain and you only pay it once, so nobody remembers the fixes.
This skill is that memory.

## TL;DR mental model

- **Notarization takes ~1–5 minutes.** If it's been 20+, it's *hung*, not slow — diagnose, don't wait.
- **Release locally, not in CI.** A modern Mac signs+notarizes first-try, every time; CI is where
  signing gets fragile (headless keychain). Keep CI as a *manual fallback*, primary = a local script.
- **Every signing bug is deterministic** once you read the actual error. Get the error, don't guess.

## 1. Local-first release (the primary path)

On Apple Silicon, a local build is faster than CI and avoids the whole class of CI signing bugs,
because the Developer ID cert + notary profile already live in your Keychain.

`scripts/release.sh <version>` skeleton (ASCII-only — see §6):

```bash
set -euo pipefail
VERSION="$1"; TAG="v$VERSION"; TARGET="aarch64-apple-darwin"
NOTARY_PROFILE="${NOTARY_PROFILE:-myapp-notary}"
# Auto-detect the identity so the script is generic for any contributor:
SIGNING_IDENTITY="${APPLE_SIGNING_IDENTITY:-$(security find-identity -v -p codesigning \
  | awk -F'"' '/Developer ID Application/{print $2; exit}')}"

# Preconditions: on main, clean tree, tag doesn't exist, notary profile works.
xcrun notarytool history --keychain-profile "$NOTARY_PROFILE" >/dev/null   # fails early if missing

# Bump version in package.json + tauri.conf.json (node) and Cargo.toml (perl, first match only).
# Quality gate. Sign the sideloaded dylib (see §4). Build:
APPLE_SIGNING_IDENTITY="$SIGNING_IDENTITY" pnpm tauri build --target "$TARGET"

DMG="src-tauri/target/$TARGET/release/bundle/dmg/App_${VERSION}_aarch64.dmg"
echo "==> notarize start: $(date -u +%FT%TZ)"
xcrun notarytool submit "$DMG" --keychain-profile "$NOTARY_PROFILE" --wait
xcrun stapler staple "$DMG"
echo "==> notarize done: $(date -u +%FT%TZ)"
spctl -a -t open --context context:primary-signature -vv "$DMG"   # expect: source=Notarized Developer ID

git add -A && git commit -m "$TAG" && git tag "$TAG" && git push origin main "$TAG"
gh release create "$TAG" "$DMG" --title "App $TAG" --generate-notes
```

**One-time setup** (document in a `RELEASE.md`):
1. A **Developer ID Application** cert in the login Keychain (`security find-identity -v -p codesigning`).
2. A notary profile (an app-specific password from account.apple.com → Sign-In and Security):
   `xcrun notarytool store-credentials myapp-notary --apple-id you@x.com --team-id TEAMID`
3. `gh` authenticated.

## 2. macOS signing & notarization gotchas (the whole list)

Each of these cost real time. When notarization fails, **always** pull the log — it names the file:
`xcrun notarytool log <submission-id> --keychain-profile <profile>`

| Symptom | Cause | Fix |
|---|---|---|
| `status: Invalid`, log: *"not signed with a valid Developer ID"* on a bundled `.dylib` | A sideloaded dylib in `Resources/` (not `Frameworks/`) ships ad-hoc-signed; tauri deep-signs `Frameworks/` only | `codesign --force --timestamp --options runtime --sign "$IDENTITY" the.dylib` **before** `tauri build` (§4) |
| `401 Invalid credentials … use the app-specific password` | Wrong/expired app-specific password, or Apple-ID password pasted instead | Regenerate an app-specific password; re-set the secret. `notarytool history` with the profile proves the account itself works |
| `403 A required agreement is missing or has expired` | Apple updated the Program License Agreement; all notarization frozen until re-accepted | Account Holder signs at developer.apple.com/account (gold banner) and appstoreconnect.apple.com → Agreements. Propagation can take minutes |
| Keychain `.p12` **Export greyed out** | Selected the cert under *Certificates* (no private key) | Use **My Certificates**, or skip the GUI: `security export -k login.keychain-db -t identities -f pkcs12 -P 'pw' -o out.p12` |
| Gatekeeper `rejected, source=Unnotarized Developer ID` | Signed but not yet notarized | Expected pre-notarization; notarize+staple flips it to `accepted, source=Notarized Developer ID` |

**Notarization ≠ signing.** Split them mentally. Verify the *published* artifact, not a local build:
`spctl -a -t open --context context:primary-signature -vv <dmg>`.

**Optional hardening:** swap Apple-ID/app-password for an **App Store Connect API key** (`.p8` + issuer +
key id) — kills the entire "password drifted" failure class for CI.

## 3. Diagnosing "hung" notarization / CI

The killer diagnostic: **`xcrun notarytool history --keychain-profile <profile>`** uses the same Apple
account as CI, so if a submission isn't listed, **the build never reached `notarytool submit`** — the
hang is *before* notarization (usually signing). This one query tells you hung-vs-slow instantly.

- Then check GH step timings: `gh api repos/O/R/actions/runs/<id>/jobs -q '.jobs[0].steps[]'`.
  A step stuck for 20+ min with a later step still `pending` = the stuck step is the culprit.
- **Make notarization its own workflow step** (not tauri's inline notarize, which swallows
  `notarytool` output). Print `date -u` before/after so the log answers "how long did it take?".

## 4. Tauri-specific build & packaging

- **Sideloaded native libs** (e.g. `libpdfium.dylib` for PDF work) declared as tauri `resources` must
  exist at bundle time AND be Developer-ID-signed for notarization. Sign them before `tauri build`.
- **Don't fetch assets during `cargo` compile** (a `build.rs` network fetch). It's fragile — a transient
  failure leaves a declared resource missing and hard-fails `tauri_build`. Fetch at **install time**
  instead: a `postinstall` npm hook + an explicit CI step, all calling one idempotent `scripts/fetch-*.sh`.
  Don't track large binaries in git; gitignore + fetch keeps the repo lean.
- **Feature flags for dev vs release.** A `debug` feature exposes dev-only plugins (debug bridge etc.).
  Run tests with the dev feature set to match `tauri dev` and avoid recompiling the heavy dep tree
  (e.g. lance/arrow): `cargo test --no-default-features --features debug`.
- **Custom overlay title bar**: `data-tauri-drag-region` + `core:window:allow-start-dragging`.
- macOS release compile of x86_64 AVX-512 kernels (lance) can fail cross-compiling; build native per-arch.

## 5. Tauri dev-loop gotchas

- **Webview→plugin command invokes are ACL-gated and fail *silently*.** If a plugin's JS calls
  `invoke('plugin:name|command')` and no capability grants it, the promise rejects with no server-side
  trace — everything built on the callback just times out. Two fixes: grant `name:default` in a
  capability file, or (for dev-only plugins) have the plugin **self-grant at runtime** in its `setup()`:
  `app.add_capability(r#"{"identifier":"x","windows":["*"],"permissions":["name:default"]}"#)`.
  Prefer self-grant for dev tooling — a capability *file* referencing a feature-gated plugin **breaks
  release builds** that don't compile the plugin (unknown permission at build time).
- **`tauri dev` only watches `.rs` sources.** It does not rebuild on `Cargo.toml` / `Cargo.lock`
  changes — after editing deps, `touch src-tauri/src/main.rs` to nudge the watcher.
- **`[patch.crates-io]` needs a lockfile refresh.** Adding the patch alone yields
  `warning: patch ... was not used in the crate graph`; run `cargo update -p <crate>` to re-resolve.
  Verify with the lockfile `source =` line (path vs registry). Remember to remove the patch and re-update
  once the fixed version is published.
- **Verify what's actually running:** `strings target/debug/app | grep <new-marker>` proves whether the
  rebuilt binary contains your change before you debug "the fix didn't work".
- **Driving/inspecting the running app:** use tauri-browser — see the `driving-tauri-apps` skill.

## 6. GitHub Actions (the CI fallback)

- **Keychain auto-lock hangs `codesign` forever.** The temp build keychain auto-locks after the
  5-minute default, but a Rust/Tauri compile is ~20 min — so signing at minute 22 blocks on a locked
  keychain with no error. Fix: `security set-keychain-settings build.keychain` (no timeout) at import,
  and re-`unlock-keychain` right before the build.
- **`secrets` context is forbidden in step-level `if:`** — `if: ${{ secrets.X != '' }}` fails *workflow
  validation* (0s, no jobs, workflow shown by file path not name). Guard inside the shell instead:
  `env: { X: ${{ secrets.X }} }` then `if [ -z "$X" ]; then ... fi`.
- Tauri only skips notarization when `APPLE_ID`/`APPLE_PASSWORD`/`APPLE_TEAM_ID` are **absent** — empty
  strings still trigger a (failing) attempt. Export them to `$GITHUB_ENV` only when all are set.
- Demote `release.yml` to `workflow_dispatch`-only when local is primary, so `git push origin vX` doesn't
  trigger a redundant 25-min build. **Validate the fallback once** — a backup you've never seen pass isn't one.

## 7. Cross-cutting engineering lessons

- **Shell scripts: ASCII only.** A Unicode char right after `$VAR` (e.g. `"downloading $PKG…"`) folds
  into the variable name under some locales, so `set -u` aborts with `PKG: unbound variable`. Bites only
  on the non-early-exit path — test scripts by exercising the *actual work* path under `sh` + `LC_ALL=C`.
  Check: `grep -rlP '[^\x00-\x7F]' scripts/`.
- **Quality gate before commit/push.** `cargo fmt -- --check && cargo clippy -- -D warnings && cargo test`.
  Newline-separated statements don't stop on failure — `&&`-chain them, and read a green result before
  pushing. In pipelines, `set -o pipefail` or the tail of a `cmd | tail` chain will lie about failures.
- **Cancellation without threading through every layer:** store per-request
  `tokio_util::sync::CancellationToken`s in app state, keyed by **scope** (`"chat"`, `"artifact"`) in a
  `HashMap` so stopping one activity doesn't kill another; race work with
  `tokio::select! { r = work => …, _ = token.cancelled() => … }`.
- **pnpm 11**: approve dependency native build scripts in `pnpm-workspace.yaml` `allowBuilds`;
  `verifyDepsBeforeRun` can break tauri/vite.

## Related skills

- `driving-tauri-apps` — automate/inspect the running app with tauri-browser.
- `building-local-ai-apps` — provider abstraction, RAG, and UX patterns for local-AI desktop apps.
- `github-releases`, `homebrew-tap` — general release + tap workflows.
