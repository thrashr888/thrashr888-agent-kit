---
name: driving-tauri-apps
description: Automate, inspect, and verify a running Tauri app with tauri-browser — DOM snapshots, ref-based clicks, React-safe fills, screenshots, direct Tauri command invokes, and demo-data seeding. Use when driving a Tauri app for testing, screenshots, demo setup, or end-to-end verification of app changes.
allowed-tools: Read, Bash, Grep, Glob
---

# Driving Tauri apps with tauri-browser

[tauri-browser](https://github.com/thrashr888/tauri-browser) is a CLI + in-app plugin
(`tauri-plugin-debug-bridge`) that lets an agent drive a running Tauri app: snapshot the DOM with
element refs, click/fill, run JS, take screenshots, and call Tauri commands directly. Use plugin +
CLI **0.4.1 or newer** — it fixed four foundational bugs (see "Old versions" below).

## Setup (consuming app)

```toml
# src-tauri/Cargo.toml
[dependencies]
tauri-plugin-debug-bridge = { version = "0.4.1", optional = true }
[features]
debug = ["dep:tauri-plugin-debug-bridge"]
```

```rust
// lib.rs
#[cfg(feature = "debug")]
let builder = builder.plugin(tauri_plugin_debug_bridge::init());
```

Run with `pnpm tauri dev --features debug`. **No capability configuration needed** (≥0.4.1
self-grants its ACL permission). The CLI auto-discovers port + token from
`/tmp/tauri-debug-bridge/`; with several live apps, pass `--app com.example.id`.

## Core loop

```bash
tauri-browser connect                          # health check; proves the bridge is up
tauri-browser snapshot -i                      # interactive elements with @refs
tauri-browser click @e3                        # by ref, or CSS: click '[title="Send"]'
tauri-browser fill 'textarea' "hello"          # React-safe as of 0.4.1
tauri-browser run-js "return document.title"   # escape hatch for anything else
tauri-browser screenshot out.png               # native WKWebView capture
tauri-browser invoke list_things '{"id":"x"}'  # call a Tauri command directly
```

## The gotchas that actually bite

1. **Snapshot refs go stale on re-render.** `@refs` are `data-debug-ref` attributes assigned at
   snapshot time; any framework re-render can drop them. Re-`snapshot` immediately before clicking,
   or click by CSS selector / `run-js` element search instead.

2. **`invoke` bypasses the frontend.** Data created via `invoke` lands in the backend, but the app's
   store (Zustand/Redux/etc.) doesn't know. Either `run-js "location.reload()"` to re-init, or drive
   the UI to refetch. Corollary: verify backend effects with another `invoke` (e.g. `list_*`), verify
   UI effects with `run-js`/screenshot.

3. **Verify framework *state*, not DOM values.** After `fill`, the DOM value can look right while app
   state didn't update. Probe a state-driven signal instead — e.g. is the submit button enabled:
   `run-js "return !document.querySelector('[title=\"Send\"]').disabled"`.

4. **Waiting on async app work:** poll a completion signal in a shell loop rather than sleeping blind:

   ```bash
   for i in $(seq 1 40); do
     done=$(tauri-browser run-js "return document.body.innerText.includes('Suggested follow-ups')" | grep -c true)
     [ "$done" = "1" ] && break; sleep 5
   done
   ```

5. **After changing the plugin or Cargo deps, the dev watcher won't rebuild** — it only watches `.rs`
   files. `touch src-tauri/src/main.rs`, then confirm the running binary actually has the change
   (`strings target/debug/app | grep <marker>`) before re-testing.

6. **Multi-line `run-js` needs explicit `return`;** single-line expressions are auto-returned.
   `await` works (the wrapper is async). Avoid triggering `alert`/`confirm` — they block the bridge.

## Recipes

**Seed demo data through the backend, then drive the UI:**

```bash
tauri-browser invoke create_notebook '{"title":"Demo"}'          # returns the id
tauri-browser invoke add_source_file '{"notebookId":"...","path":"/abs/file.md"}'
tauri-browser run-js "location.reload()"                          # store refetch
tauri-browser click '[title="Demo"]'                              # navigate to it
```

**Fill a React composer and submit:**

```bash
tauri-browser fill 'textarea' 'What is blocking our enterprise deals?'
tauri-browser click '[title="Send"]'
```

**Screenshot a specific UI state:** drive to the state, confirm it exists
(`run-js "return !!document.querySelector('[role=dialog]')"`), then `screenshot`. Screenshots are
correct even when the window is occluded (≥0.4.1 forces a render pass).

## Old versions (pre-0.4.1) — symptoms and workarounds

| Symptom | Cause | ≥0.4.1 | Workaround on old versions |
|---|---|---|---|
| `eval`/`snapshot`/`invoke` time out; `connect`/`screenshot` fine | Tauri ACL silently denies the plugin's `eval_callback` | plugin self-grants at runtime | add `"debug-bridge:default"` to a capability file (breaks release builds if plugin is feature-gated) |
| Screenshots miss changes you just made (modal absent) | occluded window returns last composited frame | `afterScreenUpdates` forces fresh render | focus the app first via osascript, wait ~2s |
| `fill` sets the DOM but app state never updates | React's value tracker dedupes the input event | prototype value setter | `run-js` with `Object.getOwnPropertyDescriptor(proto,'value').set.call(el, text)` + dispatch `input` |
| "Multiple apps detected" with one app running | stale discovery files from exited apps | liveness probe + cleanup | delete dead files in `/tmp/tauri-debug-bridge/` |

## Guidelines

- Always `connect` first; if the bridge is down, nothing else will work and errors mislead.
- Prefer `invoke` for data setup (fast, deterministic) and real UI interaction for anything you're
  screenshotting or verifying — the point of driving the UI is exercising the real code path.
- Screenshot verification beats DOM assertions for visual work; read the image, don't trust selectors.
