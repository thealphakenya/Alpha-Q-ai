Startup and preflight notes

- The `scripts/qmoi-start.py` script performs a lightweight preflight check for commonly required runtime
  Python packages (requests, aiohttp, schedule, PyYAML, GitPython, watchdog). If any are missing the script
  will attempt to install them into the active Python interpreter using `sys.executable -m pip install`.

- Heavy, system-dependent packages (for example `torch` and some compiled C extensions) are not auto-installed
  by the preflight because they often require platform-specific wheels or system headers. Install those in CI
  or on the target host using platform-appropriate wheels.

- For reproducible local checks, use the provided `requirements-minimal.txt` which now includes the small runtime
  packages required to run the start sequence in a dev container:

  requests
  aiohttp
  boto3
  numpy
  pandas
  GitPython
  watchdog
  schedule
  PyYAML

- CI: the workflow at `.github/workflows/install-requirements.yml` installs `requirements-minimal.txt` and then
  optionally attempts to install heavier requirements with a CPU-friendly PyTorch wheel using the official
  PyTorch wheel index. Adjust that workflow to match your target runner (GPU vs CPU) and pin versions where
  necessary for reproducible installs.

If you'd like, I can:

- open a PR from `autosync-links-20251107` with the changes I pushed, including a short PR description and testing notes; or
- create a separate focused branch to only contain the preflight/start changes and the requirements update; or
- continue by creating a CI job that runs the full start flow on an `ubuntu-latest` runner with CPU PyTorch wheels to validate end-to-end.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10428`; directories: `1268`; Markdown: `2416`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2109, orchestration=2061, qteam_accountability=2049, release_tag_publish=2088, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2221`; needs review: `187`; metric candidate lines: `52705`; percentage occurrences: `22237`.
- Markdown word count: `3550281`; heuristic sentence count: `673664`; sentence records indexed: `673664`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29834` metric claims; `10658` completion claims; `29737` metric and `10529` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13328`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `39967` lines in `3666` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `286`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
