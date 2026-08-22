# Clause briefs — full audit prompts

Each brief below is a complete prompt for one read-only subagent. Replace
`<repo>` with the working directory and adjust file names to the stack
(examples assume a Tauri + React app; for AppKit/SwiftUI swap the search
targets, not the questions). Every brief ends the same way: report findings
with `file:line` evidence, worst first, findings only — no fixes.

## 1. System is law

Audit: "system appearance, accessibility text size, and reduced motion are
never overridden; standard edit shortcuts always mean the standard thing."

- Type: search `text-\[[0-9]+px\]` and px font sizes in components. Fixed-
  canvas artifacts (print sheets, slide surfaces) are legitimate exceptions;
  everything else should be rem/em tracking the system text size. Verify the
  wiring end-to-end: who reads the OS text size, how it reaches the root
  font-size, whether pop-out windows inherit it.
- Motion: search `duration-|transition|animate|keyframes`. Flag durations
  over the repo's cap, spring/bounce easing, and any animation not covered
  by the global `prefers-reduced-motion` guard. Two classes the CSS guard
  cannot reach: rAF/WebGL loops, and components that read
  `matchMedia("(prefers-reduced-motion)")` **once** without a change
  listener (toggling the OS setting then does nothing until remount).
- Colors: hex/rgb literals in components (not the token files). The tell for
  a real violation: a hardcoded color that needs a manual light/dark
  override next to it.
- Shortcuts: find keydown handlers matching metaKey + c/v/x/z/a/f. Flag any
  that preventDefault outside an editor context, and any global shortcut
  handler that skips the repo's focus/dialog guard (fires while typing or
  while a modal is open).

## 2. Menu is the index

Audit: "every user-facing command appears in the native menu bar with its
shortcut."

- Inventory the native menu source completely: every item, accelerator, and
  how it dispatches to the frontend.
- Inventory the app's real commands: primary buttons, command-palette
  entries, keyboard handlers, tray/dock menus.
- Diff four ways: (a) commands in the UI missing from the menu — rank
  keyboard-bound commands and primary verbs highest; (b) shortcuts in any
  in-app shortcuts list missing from the menu, and vice versa (parallel
  hand-maintained lists are the structural cause — name it); (c) menu items
  whose frontend handler is missing, or dead in secondary window types
  (test every window type the app can open — pop-outs often mount a subset
  of the UI); (d) accelerator collisions — the same key bound in both the
  menu and a JS handler (menu key equivalents beat the webview, so a
  double-bound *toggle* can open-and-close), and app accelerators that
  shadow system-wide conventions (⇧⌘V Paste and Match Style is the classic).
- Check menu-item enablement: items that should disable by context but rely
  on runtime error toasts instead.

## 3. Keyboard is complete

Audit: "anything clickable is reachable and operable by keyboard."

- Non-button click targets: `<div>/<tr>/<span>/<g>` with onClick and no
  role/tabIndex/key handler. Table rows duplicating a compliant card view
  are the classic miss — same object, two views, one inert.
- Hover-only reveals: `opacity-0` or `hidden` + `group-hover:` without the
  matching `focus-within`/`focus-visible` variant. Count the compliant
  sites too — the violations are usually forks of a correct shared pattern,
  and saying so points at the fix.
- Icon-only buttons without aria-label (a `title` gives a name but note it).
- Overlays: check the shared Modal/Menu primitives first (Escape, focus
  trap, focus restore, roles), then hunt one-off overlays that skip them.
  Also test the stacked case: if every dialog listens for Escape on
  `window`, one keypress closes the whole stack.
- Mouse-only affordances: toolbars raised only on `mouseup` (keyboard
  selection never shows them — listen to `selectionchange`), drag-only
  canvases with no key alternative, drag-to-resize without arrow keys.
- Nested interactive elements — parse, don't regex; `=>` inside JSX
  attributes produces false positives.

## 4. Undo beats confirm

Audit: "prefer an immediate, undoable action with a toast over a
confirmation modal; confirm only genuinely unrecoverable bulk loss."

- Enumerate every confirm-dialog call site and what it guards.
- Enumerate every destructive action (delete/remove/clear/archive in the
  API layer and components) and classify: confirms first / immediate with
  undo / immediate with nothing.
- Judge recoverability honestly: is the data re-importable, regenerable, or
  soft-deleted server-side? A confirm whose own copy says "nothing is
  touched" is self-convicting. The inverse shape is worse: user-authored
  config (schedules, custom prompts, hand-written entries) hard-deleted on
  one click with no recourse — especially when the delete also closes the
  view you would copy the content from.
- Check whether any undo mechanism exists outside text editors, and whether
  the toast system already has a click-action hook (if it does, undo is a
  snapshot + recreate away — say so).
- Note inconsistencies the app has with itself: the same data class guarded
  in one path and silently destroyed in another.

## 5. Objects are direct

Audit: "right-click any object for its actions; drag in; drag/copy out."

- Find the context-menu mechanism, then derive the coverage rule (e.g. "has
  a menu iff it renders RowMenu inside a .group"). List object types WITH
  and WITHOUT menus; objects with hover actions but no context menu; and
  the biggest on-screen object (the document/reader) specifically.
- Menu parity: the same object type rendered in different views (list,
  gallery, reader, table) should carry the same action set. Diff them item
  by item; comments claiming parity are often stale.
- Row actions with no menu equivalent and menu items with no visible
  equivalent (hover-gated ⋯ as the only path).
- Drag-in: file-drop handling, where it lands, failure paths, whether a
  browser dev build has an HTML5 fallback.
- Drag-out: search `draggable|onDragStart|dataTransfer`. Zero hits means
  nothing leaves the app by drag — a one-line, high-signal finding.
- Copy/export inventory per object type; flag agent/API capabilities with
  no UI equivalent (the agent can do it, the user cannot).

## 6. State survives

Audit: "window size, panel widths, selection, and in-progress text restore
on relaunch."

- Window geometry: is a window-state plugin registered (check the plugin
  manifest AND the dependency list AND the runtime registration — all
  three)? Any Resized/Moved persistence? Hard-coded default sizes? Note
  close-to-tray masking: geometry loss only shows on a real quit.
- Build the two tables: what persists (key by key) and what doesn't.
  Check specifically: scroll position (module-level Maps are in-memory
  only), navigation history stacks (persisting just the current entry
  kills back/forward across relaunch), draft text (a debounce with no
  pagehide/beforeunload flush loses the last N seconds), and draft
  *metadata* (attachments/mentions saved apart from the text silently
  drop).
- Multi-window: does the restore subscriber self-scope to the main window,
  or do pop-outs clobber it?
