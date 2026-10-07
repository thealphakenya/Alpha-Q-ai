---
title: "Issue draft for qmoi-enhanced/local-release-verify.ps1"
generated: 2025-11-08T16:06:38.799895Z
---

# Review needed: qmoi-enhanced/local-release-verify.ps1

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.040269Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.040269Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.040269Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
# Verify local platform artifacts

param(
    [string]$Out = "local_release_verification.json"
)

$ErrorActionPreference = 'Stop'

function Write-Info($m){ Write-Host $m -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host $m -ForegroundColor Yellow }
function Write-Ok($m){ Write-Host $m -ForegroundColor Green }
function Write-Err($m){ Write-Host $m -ForegroundColor Red }

Write-Info "Checking local platform artifacts..."

$expected = @(
    @{ namePattern = "qmoi ai.exe"; platform = "windows"; path = "Qmoi_apps" },
    @{ namePattern = "qmoi ai.apk"; platform = "android"; path = "Qmoi_apps" },
    @{ namePattern = "qmoi ai.deb"; platform = "linux/chromebook"; path = "Qmoi_apps" },
    @{ namePattern = "qmoi_ai_all_apps.zip"; platform = "all"; path = "Qmoi_apps" },
    @{ namePattern = "qmoiexe.exe"; platform = "windows"; path = "dist" }
)

$report = [ordered]@{
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    local_artifacts_found = @()
    missing = @()
    total_size = 0
}

foreach ($exp in $expected) {
    $searchPath = if ($exp.path) { $exp.path } else { "." }
    $found = Get-ChildItem -Path $searchPath -Recurse -Name | Where-Object { $_ -like "*$($exp.namePattern)*" -or $_ -like "*$($exp.namePattern.Replace(' ', '*'))*" }

    if ($found) {
        $fullPath = Join-Path $searchPath $found[0]
        if (Test-Path $fullPath) {
            $fileInfo = Get-Item $fullPath
            $report.local_artifacts_found += @{
                platform = $exp.platform
                name = $found[0]
                path = $fullPath
                size = $fileInfo.Length
                lastModified = $fileInfo.LastWriteTime
            }
            $report.total_size += $fileInfo.Length
        }
    } else {
        $report.missing += @{ platform = $exp.platform; pattern = $exp.namePattern; searchPath = $searchPath }
    }
}

$json = $report | ConvertTo-Json -Depth 5
Set-Content -LiteralPath $Out -Value $json -Encoding UTF8

Write-Info "Found $($report.local_artifacts_found.Count) artifacts, t
```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.

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
