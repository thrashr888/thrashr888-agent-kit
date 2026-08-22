# Webview-app gotchas for the fix stage

Traps that recur when fixing Mac-formula findings in Tauri/Electron apps.
Each one cost a debugging session somewhere; check the list before
re-deriving.

## Menus and shortcuts

- **Native menu key equivalents beat the webview.** On macOS the menu's
  accelerator consumes the keystroke before JS sees the keydown. Two
  consequences: a shortcut bound in both the menu and a JS handler is a
  latent double-fire (fatal for toggles), and a menu accelerator fires even
  while the user is typing in a text field. Pick one owner per shortcut —
  menu in the app, JS handler only for browser dev builds (gate on
  `isTauri()` or equivalent).
- **Don't give text-editing keys to menu accelerators.** A menu accelerator
  on ⌘←/⌘→ breaks line-start/line-end in every input; ⇧⌘V shadows Paste and
  Match Style. Menu items can exist without accelerators — discoverability
  without capture.
- **The Edit menu's predefined items ARE the clipboard.** WKWebView routes
  ⌘C/V/X/Z through the native Edit menu; remove it and copy/paste dies in
  inputs.
- **Build the menu once.** AppKit only auto-populates the Window menu with
  windows created after the menu is assigned — rebuilding it empties the
  list. Mutate submenus in place instead.

## Events and windows

- **JS "Any" event listeners are NOT filtered by emit target** (Tauri).
  Every window receives every event; put the target window's label in the
  payload and self-filter in each listener.
- **Menu events addressed to the focused window die in reduced windows.**
  A pop-out (note reader, print shell) mounts a subset of the UI; a menu
  action routed there flips store state nothing renders — a silent no-op.
  Detect the reduced window in the frontend (a boot flag beats label
  matching when labels are shared) and forward the event to the main
  window, then `show()` + `setFocus()` it so the user sees the result.
- **Escape on `window` closes every stacked dialog at once.** Keep a
  module-level stack of open modals; only the topmost token answers
  Escape. Capture-phase `stopImmediatePropagation` handlers (fullscreen
  overlays) still win — leave them alone.

## Undo without a backend

- **A clickable toast is a complete undo affordance.** If the toast system
  takes an optional onClick: snapshot the object before deleting, delete
  immediately, recreate from the snapshot on click. Give clickable toasts
  a longer TTL than plain ones.
- **File-backed entities restore exactly** if the save command accepts an
  explicit id (upsert). Database-backed entities recreate with a new id —
  re-apply any non-default flags (enabled=false etc.) after recreation.
- **Snapshot the saved state, not the edit buffer.** Undoing a delete
  restores what was on disk, not unsaved edits that happened to be in the
  form.

## Verification

- **Grep can't confirm runtime behavior.** Double-bindings, focus behavior,
  and reduced-motion response need a live check in the running app (for
  Tauri, the driving-tauri-apps skill). Report unverified findings as
  static inferences, not confirmed bugs.
- **Stale webviews fake "code not applied."** Kill old dev processes before
  concluding a fix didn't take.
