# QMOICLONEVERCEL.md

<!-- BEGIN QMOI MANAGED: vercel-clone-contract -->
## Vercel-compatible integration and Quantum extensions

QMOI's Vercel integration tracks Vercel-owned deployments and links, while Quantum is a separate QMOI control-plane integration designed to provide a compatible hosting baseline plus additional compute capabilities. This is not a claim of implementation parity or a copy of Vercel internals.

### Compatibility inventory

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

### Quantum-only extension inventory

- [ ] Capability discovery for simulator, hybrid runtime, and provider-backed QPU execution.
- [ ] Provider adapters with explicit availability, region, queue, and maintenance state.
- [ ] Circuit/job submission, validation, cancellation, retry, and result retrieval.
- [ ] Qubit, shots, compiler, backend, fidelity, and execution metadata when supplied by the provider.
- [ ] Hybrid classical/quantum workflow orchestration and reproducible job manifests.
- [ ] Queue time, runtime, quota, cost estimate, and spend confirmation before execution.
- [ ] Result provenance, artifact integrity, simulator-versus-hardware labeling, and replay metadata.
- [ ] Provider outage, unsupported operation, quota, and job-failure recovery states.

- Each surface is enabled only when a real provider capability is independently verified.
- See [VERCELPAYED.md](VERCELPAYED.md), [QUANTUMPAYED.md](QUANTUMPAYED.md), [QUANTUM.md](QUANTUM.md), and [APP_LINKS.md](APP_LINKS.md).
<!-- END QMOI MANAGED: vercel-clone-contract -->

## Vercel clone resource protection and unlimited-capacity failover

The current failure pattern for `alpha-q-ai` (`Resource is limited - try again in 24 hours (more than 100, code: "api-deployments-free-per-day")`) must be treated as a clone-system design problem, not as a single-project bug. Every Vercel and Vercel-derived clone must be able to continue operating even when one free-tier project is throttled.

### Clone-fabric automation rules
- Every clone project uses its own unique deployment alias and environment registry so one project cannot consume the entire shared quota.
- The system keeps a single canonical project per app plus a preview/staging pool, and rotates among them when quotas are exhausted.
- Redundant redeploys are prevented by caching build artifacts, comparing commit SHA and config hash, and skipping no-op deploys.
- Clone surfaces stay in sync with the canonical QMOI design tokens, auth modes, and API/route inventory so they do not drift from the shared contract.
- QMOI always keeps a fallback path to non-Vercel providers or prebuilt static output when a required Vercel project is blocked by free-tier policy.

### Unlimited-resource policy for QMOI clones
- QMOI remains the orchestrator of all platform clones and therefore must be able to move deployments across GitHub, GitLab, Netlify, Vercel, Gitpod, Hugging Face, Quantum, and derived surfaces without losing the same app identity.
- The clone layer must treat provider quotas as operational metadata and react with rotation or alternative routing instead of failing the app surface.
- The QMOI guarantee is not "free-tier Vercel is unlimited"; the guarantee is "QMOI keeps a resource-unlimited failover fabric across all supported cloned platforms by using paid entitlement, provider rotation, artifact caching, and deployment queueing."

### Checklist for all Vercel and auto-cloned Vercel projects
- [ ] unique project names and canonical alias registry
- [ ] environment-secret separation by project, not shared emergency values
- [ ] no-op deploy detection and build artifact cache reuse
- [ ] paid-plan or team-plan failover trigger for quota exhaustion
- [ ] daily quota monitor and alerting with provider response logs
- [ ] alternative provider or static fallback route for blocked previews
- [ ] cross-platform parity validation against the QMOI universal/UI contract
- [ ] domain, region, and rollback controls for production access paths

This model ensures the system prevents the "more than 100" daily limit from becoming a recurring blocker and keeps QMOI's clone surfaces consistently resource-aware and resource-resilient.
