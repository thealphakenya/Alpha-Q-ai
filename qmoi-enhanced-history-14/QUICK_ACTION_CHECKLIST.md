# QUICK ACTION CHECKLIST — This Week

**Start Date**: November 14, 2025  
**Target Completion**: November 21, 2025

---

## ✅ Phase 1: Validate Workflows (Priority: CRITICAL)

### Day 1 — Monday, Nov 18

- [ ] Push test tag: `git tag test-v1.2.5 && git push origin test-v1.2.5`
- [ ] Monitor GitHub Actions workflow execution
- [ ] Verify draft release created: https://github.com/thealphakenya/qmoi-enhanced/releases
- [ ] Check all 16 assets uploaded to draft

**Command to Check Status**:

```bash
gh release view test-v1.2.5 --json assets --jq '.assets | length'
# Expected output: 16
```

### Day 2 — Tuesday, Nov 19

- [ ] Download one asset and verify SHA256
- [ ] Publish draft release: `python3 scripts/sync_to_draft_release.py --tag test-v1.2.5 --publish`
- [ ] Verify published release on GitHub
- [ ] Test compliance check: `python3 scripts/generate_release_compliance_report.py`
- [ ] Check report: `cat reports/release_compliance_report.json | jq '.status'`
  - Expected: `"OK"`

---

## ✅ Phase 2: Fix Critical Issues (Priority: HIGH)

### Day 3 — Wednesday, Nov 20

- [ ] Review Dependabot vulnerabilities: https://github.com/thealphakenya/qmoi-enhanced/security/dependabot
- [ ] Create issue for each critical vulnerability
- [ ] Assign to team members if applicable

### Day 4 — Thursday, Nov 21

- [ ] Merge or create Dependabot PRs
- [ ] Verify no critical/high issues remain
- [ ] Commit fixes: `git add -A && git commit -m "fix: resolve dependabot vulnerabilities"`

---

## ✅ Phase 3: Documentation Updates (Priority: MEDIUM)

### Day 5 — Friday, Nov 22

- [ ] Update `GITHUB_RELEASES_RECENT.md` with real v1.2.3 & v1.2.4 data
- [ ] Create `RELEASES_USER_GUIDE.md` (quick-start for users)
- [ ] Review all links in README point to correct URLs
- [ ] Test all download links work

**Files to Update**:

1. `/workspaces/qmoi-enhanced/GITHUB_RELEASES_RECENT.md` — Replace [AUTOFIXED by Ollama at 2026-07-26T18:54:39.550205Z]s
2. `/workspaces/qmoi-enhanced/RELEASES_USER_GUIDE.md` — NEW FILE
3. `/workspaces/qmoi-enhanced/DOWNLOADQMOIAIAPPALLDEVICES.md` — Update links
4. `/workspaces/qmoi-enhanced/README.md` — Audit & verify

---

## 🎯 Parallel Tasks (Can Start Anytime)

### Planning & Preparation

- [ ] Schedule meeting: "Release Pipeline Review" (30 min, all teams)
- [ ] Draft requirements: "Missing Platforms Build Pipeline" (Raspberry Pi, Wear OS, Docker)
- [ ] Design: "Interactive Release Browser" UI mockups
- [ ] Inventory: Current build infrastructure (CI/CD, cross-compilation tools)

---

## 📊 Daily Standup Template

**When**: Each morning  
**Duration**: 5 minutes  
**Format**: Completed, In Progress, Blockers

### Example:

```
Monday, Nov 18:
✅ Completed: Pushed test-v1.2.5 tag, workflow triggered
🔄 In Progress: Monitoring GitHub Actions (10 min in)
⚠️ Blockers: None

Tuesday, Nov 19:
✅ Completed: All 16 assets in draft release, SHA256 verified
🔄 In Progress: Publishing draft release
⚠️ Blockers: None

[Continue through Friday...]
```

---

## 🚨 BLOCKERS & ESCALATION

If you encounter any of these, escalate immediately:

1. **Workflow doesn't trigger** → Check GitHub Actions logs → Post in #devops
2. **PAT token expired** → Extract fresh token from playbook → Update secrets
3. **Assets missing from release** → Run `python3 scripts/sync_all_releases.py` → Verify backups created
4. **SHA256 mismatch** → Regenerate manifest → Re-upload assets
5. **Dependabot dep conflicts** → Check compatibility → Create detailed GitHub issue

---

## ✨ Success Metrics

By end of week (Nov 21):

| Metric                                           | Target      | Status |
| ------------------------------------------------ | ----------- | ------ |
| Workflows executing without errors               | 100%        | ⏳     |
| Draft release created successfully               | Yes         | ⏳     |
| All 16 assets present in release                 | Yes         | ⏳     |
| SHA256 verification working                      | Yes         | ⏳     |
| Compliance check running (auto-issue on failure) | Yes         | ⏳     |
| Critical vulnerabilities resolved                | 0 remaining | ⏳     |
| User-facing docs updated                         | 100%        | ⏳     |
| Download links all functional                    | 100%        | ⏳     |

---

## 📞 Quick Links

- **GitHub Repo**: https://github.com/thealphakenya/qmoi-enhanced
- **GitHub Actions**: https://github.com/thealphakenya/qmoi-enhanced/actions
- **Releases Page**: https://github.com/thealphakenya/qmoi-enhanced/releases
- **Security Alerts**: https://github.com/thealphakenya/qmoi-enhanced/security/dependabot
- **Local Docs**: `/workspaces/qmoi-enhanced/RELEASE_MAINTENANCE.md`

---

**Accountability**: Track daily progress in this file. Update status after each phase.  
**Review**: Friday EOD all-hands to review completion & plan week 2.

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
