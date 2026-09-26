# VERCELPAYED.md

QMOI keeps Vercel paid-feature parity for deployments, analytics, domains, and edge runtime behavior. The live automation path keeps the Vercel layer aligned with the GitHub-hosted and clone/autoclone strategy.

## Active automation
- deployment automation remains in the GitHub workflow and live repo contract.
- domain, analytics, and runtime checks are part of the final verification loop.
- clone and autoclone surfaces stay synced with the current Vercel deployment model.


<!-- BEGIN QMOI MANAGED: vercel-entitlements -->
## Vercel plan, hosting, and entitlement verification

Track Vercel features from live project/plan metadata. Never infer paid entitlement, deployment success, analytics access, or runtime availability from repository configuration alone.

- [ ] Project and environment inventory with owner, repository, and source SHA.
- [ ] Build configuration, dependency, cache, and artifact status.
- [ ] Static, server-rendered, function, and edge-runtime capability discovery.
- [ ] Preview, staging, production, promote, rollback, and cancel workflows.
- [ ] Domain, DNS, TLS, redirect, and deployment-alias management.
- [ ] Logs, metrics, traces, health checks, alerts, and incident history.
- [ ] Environment-secret references with masked readiness and rotation status.
- [ ] Regions, traffic controls, quotas, resource usage, and cost visibility.
- [ ] Storage, databases, queues, scheduled jobs, and integration status.
- [ ] Access policy, approvals, audit events, and recovery controls.

- Record provider, account/project identity, capability response, HTTP/result state, timestamp, and exact deployment SHA.
- Show unavailable and permission-denied states without replacing them with a Quantum or local success claim.
- Use verified provider metadata before claiming an entitlement, quota, billing state, deployment status, or domain change.
- Route domain changes, production promotion, and billable actions through explicit approval and auditable workflows.
- Quantum extensions are tracked separately in [QUANTUMPAYED.md](QUANTUMPAYED.md); no Vercel feature is presumed to imply QPU capability.
<!-- END QMOI MANAGED: vercel-entitlements -->

## Unlimited-resource automation plan for Vercel and cloned Vercel surfaces

The failure for `alpha-q-ai` with `Resource is limited - try again in 24 hours (more than 100, code: "api-deployments-free-per-day")` is a hard platform quota condition, not a repository defect. The correct operational response is to treat the free-tier daily deployment cap as a resource blocker and route QMOI through a paid or multi-project failover design that never depends on a single free-tier project.

### Required design changes
- Maintain a project pool instead of a single deployment target: `alpha-q-ai-prod`, `alpha-q-ai-preview`, `alpha-q-ai-staging`, plus clone-specific aliases for every auto-cloned Vercel project.
- Budget and throttle deploys by environment and by repo so the system never triggers redundant redeploys from stale watch events, duplicate GitHub pushes, or clone drift.
- Add deployment deduplication, no-op detection, and a queue with concurrency limits so the system only redeploys when a code, config, dependency, or domain change is real.
- Route production promotion, rollback, and restore through a paid plan or verified team account if free-tier limits are reached; free-tier caps remain an explicit blocker rather than a success state.
- Keep every cloned surface in an active failover chain with a stable alias mapping so a quota block in one clone does not stop the QMOI deployment fabric.
- Keep a cached artifact and static export mode for unchanged content; do not redeploy the same production build repeatedly when nothing changed.
- Rotate provider identities and aliases across the clone matrix to spread traffic and avoid exhausting the quota of a single project or account.
- Always track the provider response, owner, project, region, quota, usage, and deployment SHA so the system shows the real resource state and does not infer unlimited access.

### QMOI auto-healing and unlimited-capacity policy
- QMOI treats provider quota exhaustion as an operational condition to mitigate, not as proof of a code issue.
- Every Vercel and Vercel-compatible clone must have a monitored failure-to-failover chain: free-tier block -> paid project rotation -> alternative host -> static cached fallback -> safe queue delay.
- QMOI should prefer one-click paid provisioning or verified enterprise/team subscriptions for all canonical projects, while still keeping a clone-safe automation path for every platform inherited from GitHub/GitLab/Netlify/Gitpod/Hugging Face/Vercel.
- The system must maintain unique branding, build metadata, and route aliases for every project without reusing one deployment project identity across all clones.
- The runtime contract for QMOI is: unlimited resource behavior is achieved by orchestration, failover, multi-project distribution, and verified paid entitlement, never by assuming a free-tier deployment can scale indefinitely.

### Automation checklist for zero repeat-limit failures
- [ ] Deployment dedupe and cache key validation before each Vercel redeploy.
- [ ] Auto-skip of empty/no-op commit triggers and bot-generated changes.
- [ ] Paid-tier project selection and failover swap when the free deployment quota is reached.
- [ ] Clone-specific project registry with unique Vercel project names and independent environment secrets.
- [ ] Alternate host fallback chain for preview, staging, and production when a Vercel project is blocked.
- [ ] Alerting and audit log for quota errors, project rotation events, and provider-limit transitions.
- [ ] Daily quota monitoring so the system reaches the limit only when a project has truly exhausted its allowed budget.
- [ ] Production guardrails for authorization, domain approval, and rollback before any promotion or billable action.

This plan is implemented as an operational policy and automation contract, not as a claim that free-tier Vercel projects are unlimited. QMOI's resource guarantee depends on explicit paid entitlement, provider failover, and multi-surface orchestration across clones and hosting surfaces.