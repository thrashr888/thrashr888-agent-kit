# Live Page Review

Use this pass when the requested Mac review includes page presentation or
release QA. Choose pages and states relevant to the change; a focused layout
fix does not require every fixture below. Apply the repo's existing design
rules and established sibling-page patterns.

## Establish a repeatable pass

Identify the running build and data profile before testing. Prefer disposable
fixtures for state changes, and confirm isolation before introducing malformed
data or cancelling a write. Use an existing test seam when available; do not
corrupt real user data to manufacture an error state.

For each selected page, check the entry path, visible result, primary action,
and return path. Inspect the real window at its normal size and a supported
narrow size where wrapping or clipping could change the result.

| Check | What to exercise |
| --- | --- |
| Alignment and density | Compare list/detail edges, labels, controls, and action rows with sibling pages. Check wrapping and long values against the existing design. |
| Descriptions and labels | Enter a description through the UI, then verify it appears in the intended list or detail surface and survives reopening. Distinguish missing data from missing presentation. |
| Empty and partial data | Verify useful navigation and actions with zero items and with only one supported data category populated; counts and placeholders should agree. |
| Loading and failure | Exercise a relevant slow, validation-failure, or malformed-data fixture. Diagnostics should be readable and navigation should remain usable. |
| Cancellation and recovery | Where supported, cancel a disposable operation and inspect its final state, diagnostics, and next usable action. Reopen or retry only within the authorized test scope. |
| Hidden values | Use synthetic marked values, including nested data. Check list, detail, search, and any affected output surface against the product's actual visibility policy; do not assume input and derived-output marking are identical. |
| Keyboard and focus | Reach the affected controls with the keyboard, dismiss overlays, and confirm focus returns to a useful place. |

## Record enough to reproduce

Keep a compact record: page, fixture or precondition, steps, expected behavior,
observed behavior, build identity, and evidence reference. Use screenshots for
visual findings and logs or state reads for persistence claims. Omit real
secrets from captures; prefer synthetic fixtures over redacting after exposure.

A screenshot of a page is not evidence that its action worked. Conversely, a
successful backend call does not establish that the visible control worked.
Verify each claim through its relevant interaction and result.

After a fix, repeat the failing steps against the updated build and compare
the same state. Mark untested states explicitly. If a defect remains, carry
its reproduction and evidence into the existing issue tracker rather than
calling the page verified because unrelated tests passed.
