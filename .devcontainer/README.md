# Low-bandwidth Codespaces mode

This configuration keeps container creation small and avoids work that requires
network access. It uses the Python 3.12 devcontainer image, adds no VS Code
extensions or Android SDK, and does not install Python packages, start QMOI
services, run tests, install Ollama, or download models during startup.

The post-create script only ensures the pip cache directory exists and reports
the Python version. It is safe to rerun after an interrupted create because it
does not overwrite project files or make network requests. There is deliberately
no post-start command, so reconnecting does not repeat setup work.

## Optional tools and dependencies

Install only what the current task needs. For Python development, create the
ignored virtual environment and install dependencies explicitly:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Pip uses `/home/vscode/.cache/pip` to reuse downloaded packages while that
Codespace filesystem and cache remain available. A deleted or rebuilt
Codespace may not retain this cache. The repository's `requirements-minimal.txt`
still includes large data/scientific packages, so it is not installed
automatically. Android SDK, Gradle, Ollama, and model downloads are also
opt-in; install them only for a task that needs them. VS Code extension updates
are not automatic in this mode; review and apply them manually when appropriate.

The root has no Dockerfile. Existing app startup/build scripts and the Ollama
autonomous runner are not Codespaces lifecycle hooks and are intentionally not
called here: some install dependencies, start background services, mutate
files, or fetch Ollama models. Root GitHub Actions workflows remain independent
of Codespaces startup and were not changed by this configuration.

## Saving work and recovering a connection

Editor buffers autosave after one second and VS Code persistent terminals are
enabled. Git autofetch is disabled to avoid background network traffic; review
`git status` and create small commits for durable checkpoints. Stage only the
files intended for a checkpoint, and push explicitly when network access and
repository authorization are available. There is no automatic add, commit, or
push, so reconnects cannot capture unrelated files or publish work
unexpectedly. Local commits are not a backup if a Codespace is deleted; push
important checkpoints when authorized.

After reconnecting, inspect the source-control view and `git status` before
continuing. Do not blindly rerun service-startup scripts: first check whether
their processes are already running. Terminal revival and autosave improve
recovery from a dropped browser connection, but cannot recover unsaved data
after Codespace deletion or repair a failed remote connection.

## Browser sign-in and WebSocket failures

Devcontainer settings do not authenticate the browser and do not repair
GitHub/Codespaces sessions, captive portals, proxies, or WebSocket tunnels.
Diagnose those on the client device separately:

1. Complete any Wi-Fi captive-portal sign-in in the browser before opening
   Codespaces. Confirm GitHub and Codespaces are signed in within the same
   browser profile and that any organization SSO requirement is satisfied.
2. Reload the Codespace page after network access is available. If it still
   fails, inspect browser developer tools for the Codespaces WebSocket request,
   its HTTP status/close reason, and timing. A successful WebSocket upgrade
   normally reports `101`; failures can indicate blocked `wss` traffic or an
   expired browser session. Do not share request headers, cookies, tokens, or
   sensitive URL query values.
3. Compare on a second trusted network or hotspot. If only one network fails,
   ask its network administrator whether TLS WebSocket traffic to the
   GitHub/Codespaces services is filtered. Do not weaken account security or
   paste credentials into a terminal to work around browser sign-in.
4. Record the browser/device, network type, approximate time, Codespace region,
   WebSocket status/close reason, and whether a second network changes the
   result. Redact identifiers and all authentication material before sharing
   diagnostics.

`GIT_TERMINAL_PROMPT=0` prevents a stalled command-line credential prompt; it
does not change browser sign-in or WebSocket behavior. Use the normal VS Code
or GitHub authentication flow rather than entering passwords or tokens in a
terminal.

No browser logs, client-side network captures, or captive-portal details were
available during this repository change, so no specific authentication or
tunnel root cause is claimed.

## Prebuilds, region, and measurements

Codespaces prebuilds and region selection are managed in GitHub, not by this
repository file. They were not enabled or changed; prebuilds can incur
additional compute and storage charges and require repository-owner approval.
This configuration has no dependency-install startup step to precompute, so
evaluate prebuilds only if repeated measurements show the image preparation
time is a material bottleneck.

Record create/rebuild duration, reconnect duration, approximate transferred
bytes, selected region, and client network type across comparable runs before
and after adopting a prebuild or changing region. Separate image-pull time from
post-create time, and compare browser-to-Codespaces tunnel behavior separately
from Codespaces-to-package-host latency. A server-side ping or a fast package
download does not establish that an Android browser's WebSocket path is
healthy.

## Audit evidence

- Correlation ID: `620c3f3f-219d-46c1-9af4-172a01050092`
- Baseline branch: `codespace-sturdy-fishstick-69wxr9jjgw5pfrq65`
- Baseline commit: `34e8588c6bd0f3a7c23b0d3daf992449e94235f3`
- Baseline tree: `83d496a3d29a26d47c477da39f098f9b45dd3928`
- Baseline worktree: clean.
- Baseline root `.devcontainer/` and `Dockerfile`: absent.
- Local checks: both JSON files parsed; devcontainer settings matched workspace
  settings; `bash -n` passed; post-create succeeded twice using a temporary
  cache directory.
- Post-create script wall time: `0.0075s` and `0.0066s` on this workspace's
  Python 3.14.2 runtime. These are script-only measurements, not Codespace
  creation/startup times or measurements of the configured Python 3.12 image.
- SHA-256:
  - `.devcontainer/devcontainer.json`:
    `7229e1faa2e1f0d59c4196f3c5432ad385b4088ccd4db597bd85626bf5314107`
  - `.devcontainer/post-create.sh`:
    `4cde8c604fb8f911ed3ea6b1df9c92fe89bbccd0b197e25c12034251f75d227f`
  - `.vscode/settings.json`:
    `86cb8a387aa2f4e59aed8336cb3b4e8cb299871679e60b757e8052a45c6ef7bf`
  - `.gitignore`:
    `061409f50e052dd40207d7efd6f0a91320a7e27f9d709edb1147710adcbffea3`
- Network-byte count: `NOT_MEASURED`; the tested post-create script has no
  network operation. No actual Codespace rebuild was performed.
- Devcontainer CLI and Codespaces startup logs: unavailable in this workspace.
- Browser authentication/WebSocket outcome, Codespaces region, prebuild status,
  startup duration before this change, and bandwidth: `NOT_MEASURED`.
- Remote workflow, prebuild, and billing settings were not inspected or
  changed.

The local validation results and final file hashes are reported in the change
handoff; they are not evidence of remote Codespaces creation, browser
authentication, or remote workflow success.
