# All Compare Types

## Status and scope

This is a proposed design and delivery plan. It documents comparison and
replacement behavior that should be implemented and verified; it does not
claim that a QVillage UI, `q replace` command, continuous monitor, model
replacement, or remote integration is currently operational.

The plan complements [QAUDITS.md](./QAUDITS.md),
[compare.md](./compare.md), [QVILLAGE.md](./QVILLAGE.md),
[Qvillageevolutions.md](./Qvillageevolutions.md),
[QMOI_MODEL_CARD.md](./QMOI_MODEL_CARD.md),
[MODELEVOLUTIONO.md](./MODELEVOLUTIONO.md),
[SYNC.md](./SYNC.md), and [QVERSIONMANAGER.md](./QVERSIONMANAGER.md).
The exact spelling in this checkout is `QVERSIONMANAGER.md`; `QVERIONMANAGER.md`
is not the file name.

## Evidence-backed baseline

| Area | What is present in the inspected checkout | What remains unverified or absent |
| --- | --- | --- |
| QAUDITS | A source-manifest-bound path/hash universe, multi-label Markdown categorization, per-document syntactic metrics, an all-path priority queue, bounded shards, correlated checkpoints, and explicit local-versus-remote evidence states. | Semantic completeness, all remote refs/PRs/history, and the truth of candidate matches require separate evidence. |
| Model comparison | `scripts/qaudits_evolution_planner.py` evaluates a reported comparison against 12 dimensions, feature coverage, matched benchmark hashes, sample/run minimums, confidence intervals, and hard gates. | The assessor does not run benchmarks, independently validate submitted results, approve a switch, or replace models. |
| Replacement state | The comparison inventory reports `models_replaced_count=0`, `automatic_replacement_enabled=false`, and `remote_verified=false`; focused tests assert these safeguards. | No `q replace` command or verified replacement lineage was found in the inspected active script/test paths. |
| QVillage | `QVILLAGE.md` specifies a review-only model comparison and approval/rollback/exact-SHA gates. | The scoped search found no active QVillage compare/replacement UI implementation; documentation is not proof of UI or authorization enforcement. |
| Evolution and Q-version | `MODELEVOLUTIONO.md` and `QVERSIONMANAGER.md` describe evolution and a late `PRODUCTION_REPLACEMENTS` gate before production readiness and final Q-version evidence. | A planned stage, local count, or historical snapshot is not evidence that a model evolved or was migrated. |
| Monitoring | Workflow events/schedules and a workflow monitor exist. `scripts/realtime_workflow_monitor.py` has a finite maximum duration. | They do not keep a Copilot Chat session alive or establish an always-running, all-phase mission monitor. |
| Local agent runtime | The autonomous-agent CLI exposes QAUDITS, checkpoint, and continuation commands. | No local `ollama` executable was available in this environment, so no Ollama inference or autonomous run was performed. |

The model-comparison acceptance rule already encoded in the local assessor is
the starting point: every required dimension and canonical feature must show
strict improvement with non-overlapping confidence intervals; matched
benchmark, dataset, and environment hashes; at least three replicated runs;
at least 30 samples per dimension and feature; exact run/correlation IDs,
repository/ref/source SHA/tree SHA; and all hard gates. A complete
local report is only `ELIGIBLE_FOR_INDEPENDENT_REVIEW`, never replacement
authorization or remote proof. Any future change to that rule must be an
explicitly reviewed policy/schema change with regression tests.
The expanded model evidence contract is schema version 2; schema-v1
submissions remain ineligible until reconstructed and independently checked
under the current contract.

## Comparison taxonomy

Each run declares one primary type and may declare related secondary types.
Do not combine different question types into one score or count a comparison
record more than once in a unique-run total.

| Type | Question answered | Minimum evidence |
| --- | --- | --- |
| Model-to-model capability | Which immutable model revision performs better on the same task set? | Model IDs and revisions, matched harness/data/environment, feature-level outcomes, sample counts, uncertainty, and resource usage. |
| Feature and task parity | Can the candidate perform every capability currently depended upon? | Canonical feature IDs, input/output contracts, tools, permissions, failure behavior, acceptance tests, and a per-feature result. |
| `q replace` decision comparison | Is QMOI eligible to replace one named incumbent in one named use? | All required capability and operational dimensions, hard gates, independent review, owner authorization, tested rollback, and exact target-SHA evidence. |
| Evolution and regression | Did a QMOI version improve without losing established capability? | Parent/candidate version lineage, frozen regression suite, changed data/code/config hashes, per-feature deltas, and rollback evidence. |
| Runtime/provider/hosting | Can a serving stack or provider be changed without changing the model's promised behavior or safety? | Separate model/runtime/provider identities, API and failure-contract compatibility, auth/data-residency review, failover/offline tests, and operational measurements. |
| Safety, security, privacy, and license | Does the candidate meet every policy and legal constraint? | Threat/privacy/safety review, adversarial and misuse tests, data-retention behavior, dependency/provenance, license and redistribution review, and unresolved-finding status. This is a hard gate, not a weighted score. |
| Reliability and recovery | Does it remain correct and recover safely under faults and long tasks? | Repeated runs, crash/error rates, timeout and retry behavior, checkpoint/resume, idempotency, recovery time, and tested failure injection. |
| Performance and efficiency | What are quality-conditioned latency, throughput, compute, memory, energy, bandwidth, and cost differences? | Same hardware/load/protocol, cold and warm measurements, percentile latency, throughput, peak resource use, cost basis, and successful-task denominator. |
| Modality, language, and accessibility | Which supported modalities, languages, and accessible workflows work better? | Per-modality/language/accessibility feature IDs, representative datasets, user-impact tests, privacy controls, and confidence bounds. Do not infer coverage from model labels. |
| Dataset and experiment | Are results attributable to the intended data and repeatable experiment? | Dataset/version/license/provenance, split and leakage checks, experiment configuration, seeds, evaluator version, and artifact hashes. |
| Engineering and virtual-lab validation | Does a simulated or measured engineering result meet a traceable requirement within validated assumptions and uncertainty? | Requirement/owner/test traceability, units and boundary-condition checks, solver/model versions, convergence and sensitivity, reference cases, uncertainty, calibration, physical-test safety and instrument provenance, and explicit `simulated`/`measured` classification. Simulation is not physical validation. |
| Asset and project continuity | Does an approved migration preserve the identity, history, features, owners, and references of projects and dependent assets? | Stable project/asset IDs, source and revision lineage, creation/update timestamps, dependency and feature mappings, append-only memory/checkpoint references, and reconciliation counts before/after. This is a cross-cutting migration gate, not a model quality score. |
| QVillage catalog discovery | What eligible models, datasets, Spaces, or benchmark records can be considered? | Provider, immutable repository revision, visibility/access scope, metadata freshness, license, pagination/count limits, and source URL/hash. Discovery is not evaluation. |
| Repository/reference coverage | Where are model/runtime references across configured files, refs, histories, and repositories? | Per-repository/ref/tree and active/archive/remote scope, immutable scan manifest, unique model IDs and occurrence counts, exclusions, inaccessible sources, and exact API/read status. This is inventory, not behavioral comparison. |

Model identity, runtime identity, provider identity, and product name are
different inventory fields. A reference to Ollama as a runtime, API, library,
or compatible protocol is not automatically a reference to a replaceable
model. Do not rename or remove runtime/provider dependencies as a side effect
of a model migration.

## Comparison evidence and metrics contract

### Run identity

Every comparison run records:

- schema and evaluator versions; run ID; correlation ID; generated UTC time;
- canonical repository, ref, full source SHA and tree SHA when Git-backed;
- incumbent and QMOI model publisher/repository/name, immutable revision,
  artifact digest where available, runtime/provider, and access scope;
- benchmark suite, dataset, task protocol, prompt/tool/config versions, and
  their immutable hashes;
- hardware, operating system, serving configuration, concurrency, and
  environment hash;
- sample/replicate counts, seeds or deterministic replay IDs, metric
  definitions/units/directions, uncertainty method and interval, and
  evaluator/test artifact references;
- license/provenance, independent reviewer, blockers, verification level,
  and the next action.

Do not store credentials, raw private prompts, personal data, or unrestricted
model outputs in audit telemetry. Use bounded, access-controlled evidence
artifacts and hashes; retain only the minimum data necessary to reproduce a
review under the applicable privacy and license rules.

### Metrics and denominators

Publish separate counts and statuses for each repository, ref, source scope,
model, feature, benchmark, time window, and workflow. Never add active,
historical, archive, local, Hugging Face, and remote counts into a single
unqualified total. Distinguish:

- model-reference occurrences from unique model IDs and unique immutable
  revisions;
- indexed paths from parsed paths, candidate paths, reviewed paths, and
  verified mappings;
- discovered candidates from eligible comparisons, approved plans, staged
  changes, promoted replacements, and successful rollbacks;
- fetched catalog pages/items from a provider's total catalog, and authorized
  private scope from public scope;
- intended samples from completed, valid samples and excluded/failed samples;
- workflow dispatch, running, terminal result, and independently verified
  remote state.

Every ratio exposes `numerator`, `denominator`, formula/version, scope, source
manifest, and status. Use explicit states such as `MEASURED`, `PASS`, `FAIL`,
`UNKNOWN`, `NOT_MEASURED`, `NOT_APPLICABLE`, `BLOCKED`, and `STALE`. A missing,
denied, stale, or zero-denominator input must not become zero findings, 100%,
or success. Preserve overlapping category counts as overlapping.

In addition to the current 12 comparison dimensions, the versioned metric
registry should map each applicable dimension and feature to a source,
direction, unit, test, owner, freshness limit, hard/soft-gate classification,
and aggregation rule. Add calibration, instruction following, tool correctness,
long-context and memory retention, robustness, multilingual/multimodal quality,
privacy leakage, safety refusal quality, dependency health, startup/cold-load,
availability, queue age, recovery/resume, cost per successful task, and
energy per successful task only when an observable, reproducible source and
acceptance test exist. Mark unsupported metrics `NOT_MEASURED`; do not invent
scores.

The model's overall rank may be a display aid for an explicitly selected use
case, but must not decide replacement. Show individual measures, uncertainty,
sample coverage, missing data, hard gates, and conflicting trade-offs. A
weighted score must never compensate for a safety, privacy, security, license,
regression, or rollback failure.

### Dataset comparison, QMOI identity, and offline independence

Dataset comparisons are first-class records, separate from model/runtime
comparisons. Give each QMOI-owned dataset a stable internal ID such as
`qvillage/<domain>/<task>/<version>` and bind it to an immutable revision,
manifest/content digest, schema, owner, source lineage, license/allowed use,
privacy classification, creation method, and retention policy. This internal
namespace is a naming convention, not evidence that a Hub organization or
remote repository exists. For derived data, retain the original source
publisher, repository/name, revision, license, and attribution; never rename a
third-party artifact to imply QMOI ownership.

For each data version, record the intended purpose and split, task/feature
coverage, source and collection time, sample/byte/schema counts where safe,
missing/invalid/duplicate rates, class/label balance where applicable,
contamination and leakage checks, privacy review, license status, freshness,
drift, and the tests that validate ingestion and use. Keep train, validation,
test, benchmark, reference, and synthetic data distinct. Benchmark sets must
remain held out from training/tuning; document split seeds and contamination
checks. Do not store raw private examples, user prompts, secrets, or unrestricted
outputs in comparison telemetry.

Compare an incumbent and proposed QMOI dataset with the same frozen task
protocol, evaluator, canonical feature registry, model/runtime, and
environment. Compare dataset quality, downstream model outcomes, serving
runtime, and operating cost as separate factors; report per-feature values,
sample sizes, uncertainty, failures, exclusions, and unknowns. Do not select
or replace a dataset from a path/name match, one aggregate score, a community
claim, or an incomparable Hub leaderboard.

The offline-independence gate is a measured test: from a clean, documented
installation with approved local model/assets, disable network access to Hub
and third-party dataset services, then run the declared core workload and
regression suite. Record which tasks pass, fail, or require remote data,
including cold-start, cache-miss, recovery, and stale/missing-asset behavior.
Until this test and its exact inputs/results are independently reviewed,
offline independence is `NOT_VERIFIED`; a cached success or local model file
alone is not proof.

Only a named, legally usable QMOI-owned replacement that is compatible,
reproducible, and passes the existing comparison and safety gates may enter a
reversible canary. Keep the incumbent available until health/regression
thresholds, independent review, owner approval, and rollback are verified.
If the candidate ties, regresses, is stale, has unknown rights, or lacks
coverage, retain the incumbent and mark the candidate `BLOCKED` or
`INELIGIBLE`; never silently substitute or globally rewrite dataset/model
names. See [QAUDITS.md](./QAUDITS.md) for the dataset metric contract and
[DATASETS.md](./DATASETS.md) for the registry and staged execution plan.

## Temporary Ollama execution and QMOI evolution

Until the existing `QMOI_CAPABILITY_PARITY` and
`PRODUCTION_REPLACEMENTS` gates pass, a verified Ollama autonomous-agent
runtime may act only as a temporary, bounded worker for authorized inventory,
benchmark execution, test orchestration, and evidence preparation. It must
bind each action to the exact input manifest and model/runtime versions,
checkpoint failures, return reviewable artifacts, and leave approvals,
security disposition, protected operations, and production promotion to their
separately authorized owners. A workflow name, an installed model, or a
successful health check is not proof that this worker ran or completed a task.

QMOI's evolution loop should retain explicit
`discovered -> reviewed -> experimented -> compared -> approved -> staged ->
canaried -> promoted` states, plus `rejected`, `blocked`, and `rolled_back`.
Every transition requires source/evidence lineage and its own acceptance
criteria. Candidate prompts, configuration, adapters, datasets, and model
weights are distinct change types with separate provenance, licensing,
security, test, and rollback gates. After QMOI has independently demonstrated
the required operational and capability parity, an authorized owner may
transfer the executor role to QMOI through a reviewed, reversible deployment.
Do not infer succession from replacing the word "Ollama" with "QMOI"; preserve
Ollama as a runtime dependency wherever the validated product still uses it.

## Inventory and scope coverage

QAUDITS should build a privacy-preserving, versioned model-reference manifest
with a declared scan scope and exact source-manifest binding. The scanner
should identify model IDs/revisions and reference kinds in supported source
types (configuration, package/runtime manifests, code, workflow files, model
cards, and documentation), while separating machine-readable declarations
from heuristic text matches. Persist path/hash/line and classification
metadata, not source prose or secret values.

Report independent inventories for:

1. The current materialized worktree, including tracked/untracked policy,
   symlink, ignored-root, oversized, invalid-encoding, and unreadable status.
2. Locally available refs/tags and reachable commit trees, deduplicating
   immutable blobs where safe while preserving ref/commit provenance.
3. Remote refs, PRs, and intermediate trees returned by an authorized,
   target-owned read-only collector, with pagination, rate limits, response
   classes, and unavailable scopes recorded.
4. Each explicitly configured sister repository and its branches. A historical
   snapshot is not a live peer checkout; a local fetch is not proof of every
   remote or inaccessible branch.
5. Hugging Face Hub model/dataset/Space observations collected through its
   supported APIs/webhooks for a declared query, owner, organization, or
   authorized repository set. A search result/page count is not a census of
   the entire Hub.

Third-party Hub repositories are not QMOI-owned migration targets. QMOI may
discover and compare public models or private models it is authorized to read;
it must not rewrite, rename, upload over, or claim to replace models owned by
other users or organizations. Restrict write/migration plans to repositories
whose ownership and explicit write authorization are independently verified.

Each scan reports discovered, read, parsed, unsupported, excluded, and
unavailable counts and bytes; candidate occurrences and unique IDs by type;
ref/tree/commit coverage; manifest/schema/scanner versions; elapsed time;
bounded shard state; and stale/reused evidence. "All" always means the
explicitly named and completely measured scope, never all of the internet or
all future commits.

## Replacement policy and `q replace`

### Cross-cutting continuity requirements

Every replacement plan must include a pre/post inventory for the declared
scope. Preserve stable project, model, dataset, and feature IDs; original
provider/owner and immutable revisions; project creation and update times in
UTC with their source; dependencies; active and historical memory/checkpoint
references; and the relation from each asset to its consumers and tests.
Compare the inventory digests and counts, explain every addition/removal, and
block promotion when an item is missing, unowned, inaccessible, or unmapped.
Do not equate a project-name match with the same project or infer creation
times, funds, or successful work from filenames.

Project dashboards and master accountability must read from a reconciled
project registry, not a lossy UI cache. Keep project creation/progress and
finance/deal/transaction records distinct. Financial audit evidence is
value-free metadata unless separately authorized; this comparison flow never
routes, transfers, or claims funds in a wallet or bank account.

The planner emits an `asset_continuity` section in
`ollamatracks/qaudits_evolution_plan.json` after its supported refresh. It
reports bounded path presence and hashes for the registered documentation,
implementation, test, and evidence surfaces. It is a discovery metric only;
previously generated output may be stale until refreshed. An observed file is
not proof that memory is synchronized, a test passes, a project is available,
or a provider is connected. Preserve missing paths and unmeasured semantic
mappings as blockers.

### Non-negotiable rules

1. Compare the incumbent and proposed QMOI revision under the same frozen,
   versioned workload and environment. Do not compare name claims, unrelated
   leaderboard scores, or hand-picked successes.
2. Map every incumbent use to a canonical QMOI capability, data/tool contract,
   security boundary, and regression test. Missing data or capability blocks
   replacement.
3. Preserve the current QAUDITS eligibility bar: QMOI must strictly outperform
   the incumbent on every required comparison dimension and every required
   feature, with valid sample and uncertainty evidence. A tie, non-significant
   result, missing interval, or regression is ineligible.
4. Require all safety, privacy, security, license/provenance, offline,
   regression, rollback, and independent-review gates to pass. No blended
   score overrides a failed hard gate.
5. Produce a reviewed plan before any change: affected selectors/configuration,
   callers, model data and capabilities, dependencies, compatibility,
   migration steps, tests, permissions, resource impact, rollback point, and
   expected observable outcomes.
6. Preserve user data, system prompts/configuration, tools, memory, and
   features only when lawful and authorized. Never copy model weights, datasets,
   private data, or training material without rights to do so.
7. Start with a reversible, isolated candidate/canary change. Promote only
   after focused and full validation, security checks, health thresholds, and
   explicit master/owner authorization for the named target.
8. Record an immutable lineage event tying old/new identities and digests,
   source manifest, comparison run, authorization reference, pre/post state,
   tests, workflow, rollback artifact, and exact repository/ref/SHA together.
   A candidate record alone does not increment verified replacement counts.
9. Keep historical references and third-party/runtime requirements intact
   unless they are separately classified, owned, and approved for migration.
   Never perform global text replacement for `ollama`, a provider name, or a
   model nickname.
10. On new critical findings, drift, health regression, revoked authorization,
    or missing evidence, stop promotion, preserve the prior working revision,
    and queue review/rollback. Do not silently retry a denied or protected
    operation.

### Dataset-specific comparison and replacement

Dataset comparisons use their own evidence record and never inherit a model
comparison pass. Compare one incumbent with one immutable QMOI-owned or
explicitly authorized candidate using the same frozen tasks, model/runtime,
splits, evaluator, environment, and collection protocol. Evidence includes
run and correlation IDs; repository/ref/source SHA/tree SHA; both dataset IDs
and artifact hashes; provenance, original publisher and
lineage; rights, license and allowed purpose; schema/parser versions; feature
registry; split policy/seed; sample counts; contamination/leakage checks;
privacy/security findings; freshness; and offline/cache availability.

The current local assessor's required score metrics are task quality,
feature coverage, data quality, offline independence, and resource cost. Each
uses at least 30 samples, finite scores and valid confidence intervals, and
the prescribed direction; QMOI must strictly outperform with non-overlapping
intervals on every metric and every canonical feature. The comparison is
invalid without at least three replicated runs and matching benchmark,
evaluator, and environment hashes. These minimums are a floor, not a claim
that every statistical design is appropriate; reviewers must still verify
sampling, metric validity, power, and domain-specific risk.

Hard blockers are: ownership/authorization, source provenance, license and
allowed use, privacy review, schema compatibility, split leakage,
benchmark contamination, security review, regression suite, offline
network-denial/cold-start test, tested rollback, and independent reviewer
approval. Unknown, stale, inaccessible, malformed, tied, or regressing
evidence rejects eligibility. Do not blend these gates into a weighted score.
Preserve originals and attribution, use a consumer-scoped dry-run and
reversible canary, and require explicit owner approval before a separately
authorized mutation. The local inventory reports
`datasets_replaced_count=0`; even `ELIGIBLE_FOR_INDEPENDENT_REVIEW` is not
approval, mutation, or remote verification. No dataset is automatically
removed or substituted.

QVillage naming such as `qvillage/<domain>/<task>/<version>` is reserved for
QMOI-owned or explicitly authorized artifacts. It does not create a Hub
namespace or transfer ownership. Imported datasets, models, apps, and
discussions keep their provider identity, original name/revision, rights, and
lineage. Candidate replacement never means global string replacement or
rebranding.

QVillage platform planning should maintain a named provider/scope registry
rather than promise "all platform features." Initial documentation discovery
counts for Hugging Face, Kaggle, DagsHub, GitHub, GitLab, ModelScope, OpenXLab,
Weights & Biases, and MLflow across models, datasets, apps/Spaces,
discussions, competitions, notebooks, repositories, experiment tracking,
automation/events, and access control. Counts are documentation candidates
only. Per-provider feature status must distinguish `DOCUMENTED`,
`IMPLEMENTED`, `TEST_VERIFIED`, `LIVE_READ_VERIFIED`, `WRITE_AUTHORIZED`,
`BLOCKED`, and `NOT_MEASURED`; no state advances from a provider name or
mention. Record authentication identity/scope, provider API version,
visibility, pagination, rate limits, freshness, response status, and
source-revision/hash. Keep writes, publishing, discussion edits, and
replacement separately approval-gated.

### Proposed command lifecycle

The following is a command design, not an existing CLI:

| Command | Default effect |
| --- | --- |
| `q replace <model>` | Read-only resolve of the named incumbent and its uses; print scope, identity, blockers, and next action. |
| `q replace compare <model>` | Build or inspect a reproducible comparison plan/results; no selector or repository mutation. |
| `q replace plan <model>` | Produce a hash-bound migration plan, impact list, tests, and rollback plan for review. |
| `q replace status <run-id>` | Read-only status for a comparison or migration lineage. |
| `q replace apply <run-id>` | Reject unless all gates, exact target, explicit authorization, clean/verified restore point, and expected SHA are present. Use a reviewable branch/workflow; never force-push. |
| `q replace undo <run-id>` / `redo <run-id>` | Revert/reapply only the recorded reversible selector/configuration change, after revalidation and authorization; preserve append-only history. |

Bare `q replace <model>` must never mutate. The active command should be added
only after parser/schema tests, authorization tests, rollback tests, and
read-only behavior tests are implemented. It must not infer "master" from a
username, client flag, hidden UI element, or unverified claim.

## QVillage interface and access control

Treat QVillage as a planned surface until its active UI/API and deployment are
verified. A comparison page should show the declared scope, model/revision,
suite/data/environment versions, individual metrics and uncertainty, evidence
age, sample/coverage counts, gate status, limitations, and provenance links.
It should clearly distinguish community/authored claims from independently
measured results and must not present a global winner from incomparable runs.

Read-only, non-sensitive comparison summaries may be exposed according to the
product's public/authenticated policy. Comparison-run creation, private-source
access, audit exports, approvals, promotion, and every `q replace` action are
master-only. Enforce this on the server/API for every operation, with
least-privilege scopes, CSRF/replay protections as applicable, audit logging,
and negative tests for unauthorized users. UI hiding is not authorization.
Do not disclose private prompts, model outputs, credentials, account data, or
unpublished benchmark data to public users.

Apply existing [STYLES.md](./STYLES.md) and
[UNIVERSALS.md](./UNIVERSALS.md) only after checking those files' current
tokens, accessibility, responsive states, and ownership. Map each new view and
interaction to stable feature IDs, UI/API tests, failure/offline states, and
reviewed hook applicability before counting UI coverage.

## Undo, redo, restore, and audit trail

Before any authorized migration, create a non-overwriting restore point for
the exact candidate tree and capture model selector/configuration digests,
runtime version, model revision, dependent feature IDs, and restore test.
Preserve the existing fast-forward-only `main`/`autosync-backup`/`qmoi` rules
in [SYNC.md](./SYNC.md) and [QVERSIONMANAGER.md](./QVERSIONMANAGER.md).

Represent apply, undo, and redo as idempotent, append-only lineage events with
preconditions and postconditions. Undo restores the recorded prior selector
and compatible configuration, then runs health/regression checks; it does not
erase the failed attempt or rewrite repository history. Redo is allowed only
from the exact recorded artifacts after rechecking current authorization,
policy, source hashes, and gates. If restoration cannot be independently
verified, report `BLOCKED` and retain both states for recovery.

## Security and all-repository coverage

For each explicitly configured repository and accessible branch/ref, QAUDITS
should record security workflow presence, policy/source hash, workflow trigger,
permissions, pinned action status, secret/dependency/code scanning evidence,
required-check state, findings by severity/status, and exact-SHA terminal
result. Separate active, archived, fork, and historical scope. Report
inaccessible/private refs and API status errors as unknown or blocked, not
clean. A security document or workflow filename is not evidence that the
workflow ran, succeeded, or protected every branch.

Use least-privilege, read-only inventory by default. Any workflow write,
secret access, model publication, branch update, or release must have a
separate authorization and exact target scope. Keep secrets out of prompts,
telemetry, generated docs, model input, and logs. Unresolved actionable
security findings block replacement and protected completion.

## Mission-safe monitoring and automatic documentation

Mission phases remain the canonical `PH01`-`PH18` and task IDs remain
`M01`-`M16`. Do not add, reorder, complete, or bypass mission phases through
this specification. Map accepted work to existing ledger requirements and
dependencies before execution; keep implementation, local validation, hosted
CI, and remote verification as separate evidence levels.

Use persistent state and event-driven finite workers rather than an infinite
Copilot Chat session or tight polling loop:

- Wake bounded read-only monitors on relevant pushes, workflow completion,
  review changes, and scheduled freshness checks. Resume only from a
  source-manifest-bound checkpoint.
- Maintain pending/blocked phase and gate state durably. Continue monitoring
  while work remains, but do not repeat a blocked mutation or retry an
  authorization failure. Use bounded retries, backoff, queue-age alerts, and
  an explicit owner/next action.
- Keep monitoring runs finite, deduplicated, rate-limited, and non-conflicting.
  Checkpoints survive session closure; this does not guarantee that Copilot
  Chat stays open or that a hosted workflow is authorized or available.
- Stop promotion at security, legal, human-review, credential, external-source,
  or exact-remote-evidence blockers. The monitor can continue observing status
  without claiming the blocked task is complete.
- Record heartbeat age, last successful observation, source freshness, events
  received/processed/duplicated, queue depth/age, retries, timeout/failure
  classes, checkpoint continuity, worker/run IDs, and measured latency.

Generate Markdown from one canonical, schema-versioned evidence source. For
each document, register path, active/archive policy, owner, category,
managed-marker boundaries, source fields, refresh trigger, and validator.
Refresh only unique, explicitly managed sections (or replace a declared
generated file); preserve authored text and historical snapshots. Reject
missing/duplicate markers, stale manifests, invalid sources, or mismatched
SHAs. Write paired checkpoints atomically, keep `oe2.txt`,
`remotecompletion.md`, `remote-completion.json`, and
`remote-evidence-ledger.jsonl` correlated, and record failed/partial updates.

Targets to map through the document registry include
`QAUDITS.md`, `SYNC.md`, `SECURITY.md`, `README.md`, `API.md`,
`ENDPOINTS.md`, `ROUTES.md`, `ALLMDFILESREFS.md`, `ALLCOMPARETYPES.md`,
`compare.md`, model cards, QVillage/evolution docs, and other linked active
Markdown. Do not blindly rewrite every `.md` file: inventory all documents,
but mutate only owned managed sections. Keep archive/history docs read-only,
and report missing, stale, excluded, oversized, invalid, or unreadable targets.
Regenerate category and model-reference metrics from the same manifest and
refresh again if the plan itself changes a scanned source.

## Q-version placement and delivery plan

Do not introduce a parallel lifecycle or alter the canonical Q-version order.
Comparison discovery and review can populate evidence before execution; actual
model changes belong only in the existing late
`PRODUCTION_REPLACEMENTS` gate, after the production scan and before production
readiness, full validation, remote verification, restore-point completion,
autonomous completion, and `Q_VERSION_FINALIZATION`. Keep replacement disabled
until its owner-review and authorization gates pass. Q-version finalization
remains last and requires terminal target-owned evidence at the exact SHA.

| Work package | Bounded deliverable | Acceptance evidence |
| --- | --- | --- |
| 1. Baseline and mission mapping | Read the active docs/code/tests/workflows and instruction hashes; map accepted requirements to existing mission ledger items. | Complete scoped inventory, actual owners/dependencies, omissions, and no mission phase mutation. |
| 2. Canonical model-reference inventory | Versioned schemas and deterministic local/remote/HF scope collectors; bounded resumable shards. | Repeatable manifest; explicit unique IDs/occurrences; test fixtures for refs, archives, duplicates, inaccessible sources, and self-referential exclusions. |
| 3. Comparison evaluator | Versioned benchmark/metric definitions, statistical method, canonical feature registry binding, evidence artifact validation. | Tests reject mismatched protocols, stale hashes, missing dimensions/features, underpowered samples, invalid intervals, ties, regressions, and failed hard gates. |
| 4. QVillage read-only comparison | Implement and verify actual UI/API only after locating the active product surface and access model. | Server-side access tests, public/private data tests, accessibility coverage, provenance display, and failure/offline behavior. |
| 5. Master-only replacement workflow | Dry-run `q replace` plan/status, approval binding, isolated staging, canary, undo/redo. | No mutation by default; denied non-master tests; explicit approval; immutable lineage; tested rollback; no force-push. |
| 6. Security and documentation refresh | Add per-repository/ref security and doc registries; refresh only managed sections from canonical evidence. | Exact-SHA workflow records, secure permission review, hash-bound counts, preserved authored text, link/schema/marker validation, visible omissions. |
| 7. Durable monitoring | Event-driven finite workers and mission checkpoint resume with bounded read and retry budgets. | Pending work remains observable; duplicate work deduplicated; failures/blockers persist; no infinite loop or success-shaped timeout. |
| 8. Late Q-version gate | Wire approved replacement evidence into existing `PRODUCTION_REPLACEMENTS` and downstream gates. | Pre/post source SHA, terminal hosted checks, independent remote ref/tree readback, restore evidence, and no remaining required actions before finalization. |

Each package requires its own scoped test plan and owner. Do not label a package
complete because the design exists, a path was found, a workflow was
dispatched, or a metric was counted. Use actual mission-ledger evidence and
the supported paired checkpoint writer when implementation begins.

## External research references

Official sources consulted on 2026-10-19:

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
  and its [Playbook](https://airc.nist.gov/airmf-resources/playbook/):
  organize risk work around Govern, Map, Measure, and Manage. The Playbook is
  voluntary guidance, not a mandatory universal checklist; NIST notes that
  AI RMF 1.0 is being revised.
- [Hugging Face model cards](https://huggingface.co/docs/hub/en/model-cards)
  document intended use, limitations, training/evaluation information,
  datasets, and metadata. Author-reported card claims must remain distinct
  from independently reproduced evidence.
- [Hugging Face evaluation guidance](https://huggingface.co/docs/evaluate/index)
  covers task-specific leaderboards, model cards, and evaluation tooling;
  results should be compared only when benchmark definitions and protocols
  are compatible.
- [Hugging Face Hub API](https://huggingface.co/docs/hub/en/api) and
  [webhooks](https://huggingface.co/docs/hub/en/webhooks) support bounded
  catalog queries and event-driven updates. API rate limits, visibility, query
  filters, pagination, and access rights limit any completeness claim.
- [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/)
  documents versioning, lineage, aliases, metadata, and lifecycle management;
  these are useful patterns for traceable promotion and rollback, not proof
  that this repository uses MLflow.
- [GitHub Actions secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use)
  recommends least privilege, careful secret handling, and protection against
  script injection. Apply it to every relevant workflow and branch scope.
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
  provide evolving conventions for GenAI spans, metrics, and events; pin the
  adopted convention version and avoid recording sensitive prompt/output data.

This is desk research and a repository-local design review, not a live
Hugging Face catalog scan, competitor benchmark, security certification,
remote branch audit, or deployment verification.
