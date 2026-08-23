---
name: debugging-tauri-apps
description: Find out why a Tauri app crashed, froze, or failed silently — macOS crash reports, the unified log, the debug bridge's error history, panic hooks, and the capture a shipped app needs to have. Use when a Tauri app misbehaves and the terminal shows nothing, or when adding error/crash logging to one.
allowed-tools: Read, Bash, Grep, Glob, Edit, Write
---

# Debugging Tauri apps

Two halves. **Finding out what happened** in an app that is already
misbehaving, and **building the capture** so next time there is something to
find. Start with the first; the second is what you do once you discover there
was nothing to read.

For driving an app — clicks, fills, snapshots, screenshots — see
`driving-tauri-apps`. This skill is about failures.

## The thing that makes Tauri apps hard to debug

A Tauri app launched from Finder has **no stdout and no stderr**. Every
`println!` and `eprintln!` in the Rust backend goes to `/dev/null`, and the
webview console goes nowhere at all. Under `pnpm tauri dev` you see
everything; in the bundle the user actually runs, you see nothing. So an app
that logs perfectly in development can be a complete black box in production,
and the difference is invisible until you go looking.

That single fact drives everything below.

## Finding out what happened

Work outward from the app's own records to the system's.

```bash
# 1. The debug bridge's history — if the app has tauri-plugin-debug-bridge.
#    Prints recent records and exits; works even if the app has since died.
tauri-browser errors --limit 30
tauri-browser errors --origin rust        # panics and host-app records only
tauri-browser logs --level warn

# 2. The app's own log, if it writes one. The Mac convention:
ls -t ~/Library/Logs/<bundle-id>/
tail -50 ~/Library/Logs/<bundle-id>/*.log

# 3. Crash reports — only for hard crashes (SIGSEGV, SIGABRT, SIGILL).
ls -t ~/Library/Logs/DiagnosticReports/ | grep -i <app>
```

Read a crash report by parsing the JSON after the first line:

```bash
python3 -c "
import json,sys
raw=open('$REPORT').read()
d=json.loads(raw[raw.index(chr(10))+1:])
print(d['exception'], d['termination'])
t=d['threads'][d['faultingThread']]
for f in t['frames'][:15]: print(' ', f.get('symbol'))
"
```

```bash
# 4. The unified log — only if the app uses os_log. `log show` needs a
#    predicate; process name works, subsystem is better.
log show --last 1h --predicate 'subsystem == "com.example.app"' --style compact
log show --last 30m --predicate 'process == "MyApp"' --style compact
log stream --predicate 'subsystem == "com.example.app"'     # live
```

**An empty `log show` is a finding, not a dead end.** It means the app never
reaches the unified log — which is the normal state for a Tauri app that
hasn't been given os_log explicitly. Don't keep tuning the predicate.

## Reading the answer

| What you see | What it means |
| --- | --- |
| No crash report, app still running, feature dead | A panic in a command. `panic = unwind` turned it into an `Err` string the UI showed as a toast. Nothing else recorded it. |
| No crash report, app gone | A clean exit, or something killed it. Check the app's own log for the last thing it did. |
| `SIGABRT` with `rust_panic` → `abort` in the trace | A panic that couldn't unwind — usually across an FFI boundary (see below). |
| `SIGABRT` with `__eprint` in the trace | A print to a broken stderr. See "stderr can kill your app". |
| Repeated `PoisonError` panics | A panic poisoned a mutex. Every later lock of it panics forever. Restart is the only exit. |
| White window, no errors anywhere | A React render throw with no error boundary. The tree unmounted and nobody was told. |

## Three ways a Tauri app dies that aren't obvious

**Unwinding across an FFI boundary aborts.** A panic in a *synchronous*
`#[tauri::command]` invoked from the webview unwinds into an Objective-C frame
and the runtime gives up: `fatal runtime error: failed to initiate panic,
error 5, aborting`. The whole app goes down, hard, from a panic that would
have been survivable elsewhere. Async commands and background threads unwind
normally.

**stderr can kill your app.** `eprintln!` unwraps its write and panics with
"failed printing to stderr" if it fails. When a `tauri dev` parent terminal
exits, the app's stderr becomes a broken pipe, and the next print panics —
from inside whatever thread or completion block happened to run it. This is a
real, observed crash: a Spotlight indexing completion block printing its
result took an entire app down with SIGABRT. In a GUI app, print through a
macro that can't panic:

```rust
macro_rules! note {
    ($($arg:tt)*) => {{
        use std::io::Write as _;
        let _ = writeln!(std::io::stderr(), $($arg)*);
    }};
}
```

**A poisoned mutex is permanent.** `state.thing.lock().unwrap()` panics
forever once any panic has poisoned that mutex. The user sees one feature fail
over and over with the same message and no amount of retrying helps. Treat a
`PoisonError` panic as fatal and tell the user to restart — it is the only
thing that works.

## Building the capture

If the investigation above found nothing to read, this is the fix. Four
pieces, roughly in order of value per line of code.

**1. One log file, in the Mac place.** JSONL, one record per line, rotated,
at the path Tauri already gives you:

```rust
let dir = app.path().app_log_dir()?;   // ~/Library/Logs/<bundle-id> on macOS
```

`~/Library/Logs` is right for three reasons: Console.app lists it under Log
Reports beside the crash reports, it survives an app-data reset, and users can
find it to send you. JSONL beats prose — it stays greppable *and* parseable.
Record `{ts, level, origin, kind, message, detail?, context?}`; `origin`
distinguishes backend from front-end, `kind` (`panic`, `ipc`, `render`,
`unhandled-rejection`, `startup`) makes the log greppable by failure shape
rather than by wording.

**2. A panic hook, installed first.** On the first line of `run()`, before the
Tauri builder exists — a panic during `setup` is the one that leaves no window
and no explanation:

```rust
pub fn install_panic_hook() {
    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(move |info| {
        // A panic raised inside a panic hook ABORTS. Guard the body.
        let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            record(payload_of(info), info.location(), Backtrace::force_capture());
        }));
        previous(info);
    }));
}
```

Trim the backtrace to the frame that actually failed — everything up to and
including `rust_begin_unwind` / `panic_fmt` is your own hook and the panic
runtime, and it pushes the real frame off the top of the record.

**3. The front-end, at its chokepoints.** Three places cover almost
everything:

- The single function every IPC call's failure passes through. Find it (an
  `invoke` wrapper, a `run()`, a query client's `onError`) and log there —
  one call covers every command, *with the command name*, which is the detail
  every user bug report lacks.
- `window.onerror` and `unhandledrejection`, installed before the app mounts.
  Rejections matter most: they are how a front-end bug stays invisible,
  because the UI just never updates and nothing is thrown at anyone.
- A root error boundary, logging `error.stack` **and**
  `info.componentStack` — neither is derivable from the other.

**4. Somewhere to see it without a file browser.** A `recent_errors` command
(and an MCP tool, if the app has an MCP server) so the UI, a support
conversation, and an agent asked to fix the bug can all read the same records.

### If the app has the debug bridge, most of this is free

`tauri-plugin-debug-bridge` captures JS console output, uncaught JS errors
with stacks, and Rust panics into a ring that is also mirrored to
`/tmp/tauri-debug-bridge/<identifier>.log`. Push the app's own failures in
alongside them:

```rust
tauri_plugin_debug_bridge::record(Level::Warn, "sweep", format!("failed: {err:#}"));
```

That is a dev-build capability though — the bridge is normally feature-gated
off in release. A shipped app still needs its own log.

### Reaching the unified log from Rust

Only worth it if you want Console.app and `log stream` to work. There is no
safe crate-free API; the FFI has two details that silently produce
`<compose failure>` instead of your message:

- The format string must live in `__TEXT`. A plain Rust `static` lands in
  `__DATA_CONST`, where the decoder can't find it by (image uuid, offset).
  Use `#[link_section = "__TEXT,__cstring"]`.
- The `dso` argument must be the mach header of the image owning that string.
  `__dso_handle` is **not** it in a Rust binary — dereferencing it segfaults.
  Use `dladdr` on the format string's address and take `dli_fbase`.

```rust
#[link_section = "__TEXT,__cstring"]
static FORMAT: [u8; 11] = *b"%{public}s\0";
// buffer for one public string arg: [0x02, 0x01, 0x22, 0x08, ptr_le_bytes…]
// then _os_log_impl(dso, log, type, FORMAT.as_ptr(), buf, len)
```

Keep the call fixed-shape — one format string, one argument, the same 12-byte
buffer every time — and write to disk *before* calling it. This runs on the
panic path, where an encoding bug is a crash inside a crash. Message text goes
through as data, so a message containing `%s` is inert.

## Not getting stuck in an unrecoverable state

Capture is half the job. The other half is that the user must never be left
with a dead window and no next step.

- **Startup failures**: `.expect()` in `setup` gives a Dock bounce and
  nothing else. Log the failure and show a native alert naming it and the log
  path (`osascript -e 'display alert …'` works before any window exists), then
  exit.
- **Render crashes**: a recovery screen with `Restart`, `Try again`, `Copy
  details`, and `Show log`. Render it *outside* the app's modal component — a
  modal renders inside the tree that just failed.
- **Backend wedging**: raise a fatal on the conditions that don't recover —
  a poisoned lock, or several panics in one session — and give the same
  screen. `tauri-plugin-process`'s `relaunch()` is the restart; fall back to a
  webview reload if it fails.
- **A menu item that reveals the log**, so "send me the log" is one click
  rather than a walk through a hidden directory.

## Two invariants for any of this code

**Recording must never fail loudly.** Swallow every error inside the logger. A
logger that can throw hands the caller a second error inside its error path,
which is how logging becomes a loop.

**A flood must not become the log.** Throttle by (kind, message) — a few per
minute, then every hundredth carrying the running count — plus a global
ceiling. A component that throws on every render will otherwise fill the disk
and bury the one error you needed. Throttle on both sides: the front-end's
copy exists so the flood never becomes an IPC storm.
