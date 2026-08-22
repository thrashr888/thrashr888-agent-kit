# Official Apple sources for the Mac formula

The six clauses are a distillation, not an invention — each one compresses
specific Human Interface Guidelines pages. Cite these when an owner asks
"says who?", and consult them for edge calls the clause briefs don't cover.
All URLs verified live as of 2026-08.

Platform framing for the whole formula:

- Designing for macOS — <https://developer.apple.com/design/human-interface-guidelines/designing-for-macos>
  (what people expect from a Mac app: keyboard and pointer precision,
  resizable windows, the menu bar as a fixture)

## 1. System is law

- Dark Mode — <https://developer.apple.com/design/human-interface-guidelines/dark-mode>
  (follow the system appearance; never force a mode)
- Typography — <https://developer.apple.com/design/human-interface-guidelines/typography>
  (system fonts, text styles that track the user's text size)
- Motion — <https://developer.apple.com/design/human-interface-guidelines/motion>
  (purposeful, brief animation; honor Reduce Motion)
- Accessibility — <https://developer.apple.com/design/human-interface-guidelines/accessibility>
  (Reduce Motion, text size, and the other system settings apps must respect)
- Mac keyboard shortcuts — <https://support.apple.com/en-us/102650>
  (the canonical list of what ⌘C/V/X/Z/A/F and friends must keep meaning)

## 2. Menu is the index

- The menu bar — <https://developer.apple.com/design/human-interface-guidelines/the-menu-bar>
  (every app shows its commands in the menu bar; standard menu categories
  and what belongs in each)
- Menus — <https://developer.apple.com/design/human-interface-guidelines/menus>
  (item naming, key equivalents, enablement by context)

## 3. Keyboard is complete

- Keyboards — <https://developer.apple.com/design/human-interface-guidelines/keyboards>
  (Full Keyboard Access: every interaction operable from the keyboard)
- Accessibility — <https://developer.apple.com/design/human-interface-guidelines/accessibility>
  (labels for controls, focus visibility)

## 4. Undo beats confirm

- Undo and redo — <https://developer.apple.com/design/human-interface-guidelines/undo-and-redo>
  (people rely on undo to recover; don't make them confirm their way
  through routine actions)

## 5. Objects are direct

- Drag and drop — <https://developer.apple.com/design/human-interface-guidelines/drag-and-drop>
  (content moves in AND out of the app by direct manipulation)
- Context menus — <https://developer.apple.com/design/human-interface-guidelines/context-menus>
  (right-click reveals the actions relevant to the item under the pointer)

## 6. State survives

- Windows — <https://developer.apple.com/design/human-interface-guidelines/windows>
  (window behavior people expect on the Mac, including restoring where
  they left off)
- NSWindowRestoration — <https://developer.apple.com/documentation/appkit/nswindowrestoration>
  (the AppKit contract for restoring windows across relaunch — the level
  of fidelity native apps get for free and non-native stacks must
  reimplement)
