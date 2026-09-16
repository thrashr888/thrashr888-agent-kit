---
name: verify-running-app
description: Verify which build, checkout, and data store a running app uses before testing it. Use for live app QA, reproducing a reported UI bug, or resolving ambiguity between installed apps and development worktrees.
allowed-tools: Read, Bash, Grep, Glob
---

# Verify the Running App

Tie a live test to the actual process and build that handled it. A matching app
name, open window, successful build, or healthy development server is not enough
when several checkouts or installed versions exist.

## Establish the target

Start from the user's requested app, behavior, and checkout or release. Inspect
the current environment before assuming a path or port. If several candidates
remain and the intended one cannot be inferred, report the candidates and ask
which to test; continue independent inspection meanwhile.

Use the available app, browser, or debug tooling to connect the visible window
or URL to its owning process. Prefer targeted inspection over dumping all
process arguments or environment variables, which may contain secrets.

For a known process and checkout on macOS, useful read-only probes include:

```bash
# Set app_pid and app_repo from observed evidence first.
ps -p "$app_pid" -o pid=,ppid=,comm=
lsof -a -p "$app_pid" -d txt,cwd -Fn
lsof -a -p "$app_pid" -iTCP -sTCP:LISTEN -nP
git -C "$app_repo" status --short --branch
git -C "$app_repo" rev-parse HEAD
git -C "$app_repo" worktree list --porcelain
```

Check parent/child processes when a browser, launcher, or helper owns the visible
surface. An executable's directory and its working directory are different
evidence; neither alone identifies a separately served frontend.

## Connect runtime, source, and data

Record only the identity needed for this test:

- **Runtime:** process ID, executable or app bundle, and selected window, URL,
  port, or debug endpoint. Bundle identifiers may be shared across builds.
- **Source:** checkout, branch or detached state, commit, and relevant uncommitted
  changes. For an installed app, use its version/build identifier and available
  release metadata; a source checkout need not exist.
- **Build provenance:** use an embedded revision or build record when available.
  Current repository HEAD and binary modification time do not prove the running
  binary was built from that revision. Label missing provenance as unknown.
- **Data:** profile, database, configuration directory, account, or environment
  only where it can change the outcome. Confirm from app diagnostics,
  configuration, or targeted open-file inspection; do not infer isolation from
  separate worktree paths. Two debug builds may share the same production data.

For hot-reloaded apps, verify both the native process and the frontend server's
checkout. A fresh frontend does not prove native code was rebuilt. Select the
exact endpoint when a debug tool can discover multiple instances; record its
identity without copying authentication tokens into the report.

If the runtime differs from the intended target, fix it within the existing
authorization and recheck identity. Preserve unsaved state and unrelated
processes. Launching another copy is not evidence that the test reached it.
Do not stop arbitrary matching processes, reset shared data, or migrate a real
database merely to establish which app is running.

## Exercise the behavior and attach the evidence

Run the requested interaction against the verified target. Check the observable
result and relevant persistence or backend effect. A direct backend call can
support diagnosis but does not prove that a UI interaction works. For visual
claims, inspect the resulting screen using the available authorized UI tools.

After a restart, rebuild, or endpoint change, recheck identity before carrying
forward test results. If only a different build is available, describe exactly
what was tested and leave the requested build's result unverified.

Keep the final record short, for example:

> Tested the sidebar action in PID 4123, feature checkout at revision abc1234,
> with uncommitted sidebar changes and the isolated QA profile. Runtime revision
> is confirmed by the build endpoint. Clicking Save persisted the item after
> reopening. Screenshot and query output are attached to the task.

Use real observations in the record. Distinguish confirmed identity, inferred
identity, and unknown provenance; do not turn missing evidence into a pass.
