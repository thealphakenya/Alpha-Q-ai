---
title: "Workflow fix proposals"
qmoi_validation_frontmatter: true
---

# Workflow fix proposals

_generated at 2025-10-28T23:48:19.067214Z_

Repository detected: thealphakenya/qmoi-enhanced

## .github/workflows/auto_release_variations.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 18
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 21
- Pin `docker/build-push-action` to `docker/build-push-action@v4`. Locations: 64
- Review `docker/setup-buildx-action` and consider pinning or templating. Locations: 26
- Pin `softprops/action-gh-release` to `softprops/action-gh-release@v1`. Locations: 48, 55

**Secret bootstrap commands (dry-run):**

```
# gh secret set GITHUB_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set PYPI_API_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set json --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

## .github/workflows/build.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 14
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 20
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 16
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

## .github/workflows/ci.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 15, 48
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 50
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 17

**Secret bootstrap commands (dry-run):**

```
# gh secret set GITHUB_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

## .github/workflows/github-actions-qmoi-build.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 20
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 22
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 26

**Secret bootstrap commands (dry-run):**

```
# gh secret set GITHUB_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

## .github/workflows/nightly.yml

- Review `workflows/build-and-publish.yml` and consider pinning or templating. Locations: 7
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

## .github/workflows/npm.yml

- Review `actions/cache` and consider pinning or templating. Locations: 19
- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 11
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 13
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

## .github/workflows/publish-q-alpha.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 19
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 22
- Review `peaceiris/actions-gh-pages` and consider pinning or templating. Locations: 33

**Secret bootstrap commands (dry-run):**

```
# gh secret set GITHUB_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

## .github/workflows/q.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 9
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 11
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

## .github/workflows/qmoi-app-build.yml

**Secret bootstrap commands (dry-run):**

```
# gh secret set QMOI_DISCORD_WEBHOOK --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_EMAIL_PASS --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_EMAIL_RECIPIENT --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_EMAIL_USER --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_SLACK_WEBHOOK --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_TELEGRAM_CHAT --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_TELEGRAM_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_TWILIO_SID --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_TWILIO_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set QMOI_TWILIO_WHATSAPP --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

## .github/workflows/qmoi-autodev.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 13
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 15
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

## .github/workflows/qmoi-ci.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 23
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 26
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 30
- Review `actions/upload-artifact` and consider pinning or templating. Locations: 40
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

## .github/workflows/release.yml

- Review `actions/cache` and consider pinning or templating. Locations: 21
- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 17, 57
- Pin `actions/setup-node` to `actions/setup-node@v4`. Locations: 59
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 26, 63
- Review `actions/upload-artifact` and consider pinning or templating. Locations: 40
- Review `docker/setup-buildx-action` and consider pinning or templating. Locations: 19
- Pin `softprops/action-gh-release` to `softprops/action-gh-release@v1`. Locations: 81, 89

**Secret bootstrap commands (dry-run):**

```
# gh secret set GH_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

```
# gh secret set GITHUB_TOKEN --repo thealphakenya/qmoi-enhanced  # run interactively to enter value
```

## .github/workflows/sync-notify.yml

## .github/workflows/update-readme-cli.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 18
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 20
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

## .github/workflows/validate-and-tag-md.yml

- Pin `actions/checkout` to `actions/checkout@v4`. Locations: 13
- Pin `actions/setup-python` to `actions/setup-python@v4`. Locations: 15
- Review `actions/upload-artifact` and consider pinning or templating. Locations: 27
- Consider gating workflow steps when run from forks or other repos, e.g. use `if: github.repository == "owner/repo"` on sensitive steps.

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
