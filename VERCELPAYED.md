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
