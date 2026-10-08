Receiving GitHub Actions notifications through Discord is free and one of the easiest options.
Step 1: Create a Discord server (or use one you own)
If you don't already have one, create a Discord server.
Step 2: Create a webhook
Open your Discord server.
Click the server name → Server Settings.
Go to Integrations.
Select Webhooks.
Click New Webhook.
Give it a name (e.g., GitHub Actions).
Choose the channel where you want notifications (e.g., #github-notifications).
Click Copy Webhook URL.
Save the webhook.
Step 3: Add the webhook to GitHub
In your GitHub repository:
Go to Settings → Secrets and variables → Actions.
Click New repository secret.
Name it:
DISCORD_WEBHOOK
Paste the webhook URL.
Save the secret.
Step 4: Use it in your workflow
In your GitHub Actions workflow, add a step like this:
- name: Send Discord Notification
  if: always()
    env:
        WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          run: |
              STATUS="${{ job.status }}"
                  curl -H "Content-Type: application/json" \
                      -d "{\"content\":\"🚀 Workflow: ${{ github.workflow }}\nStatus: ${STATUS}\nRepository: ${{ github.repository }}\nBranch: ${{ github.ref_name }}\nRun: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}\"}" \
                          "$WEBHOOK"
                          The if: always() condition ensures the notification is sent whether the workflow succeeds, fails, or is cancelled.
                          What you'll receive
                          Every workflow run will post a message in your Discord channel with information such as:
                          Workflow name
                          Status (success, failure, or cancelled)
                          Repository
                          Branch
                          A direct link to the workflow run
                          You can then enable Discord notifications on your phone, and you'll receive push notifications whenever a new message appears in that channel.
                          If you want a more polished experience, I can also provide �⁠a workflow that sends **rich Discord embed messages** with colors (🟢 green for success, 🔴 red for failure, 🟡 yellow for running), execution time, commit message, author, and clickable buttons linking directly to the workflow run.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10435`; directories: `1269`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2110, orchestration=2061, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52722`; percentage occurrences: `22237`.
- Markdown word count: `3552546`; heuristic sentence count: `673863`; sentence records indexed: `673863`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29844` metric claims; `10662` completion claims; `29747` metric and `10533` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13340`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40017` lines in `3670` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `287`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
