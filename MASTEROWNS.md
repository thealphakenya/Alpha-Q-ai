# MASTEROWNS.md

<!-- BEGIN QMOI MANAGED: master-owned-ui-contract -->
## Master-owned dashboard and usable-control requirements

This contract derives from the archived MASTEROWNS dashboard, monitoring, control-panel, Quantum/Vercel, user-management, documentation, domain, and audit requirements. It specifies required UI behavior; it does not assert that the corresponding application routes or access have been implemented.

### Master UI feature inventory

- [ ] System overview with source timestamp, health, and stale/degraded indicators.
- [ ] Repository, application, hosting, and deployment inventory with exact source SHAs.
- [ ] User, role, session, consent, and access review with least-privilege controls.
- [ ] Quantum compute/provider control with capability and billing gates.
- [ ] Deployment preview, approval, promotion, rollback, and audit trail.
- [ ] Domain, DNS, TLS, and ownership management with confirmation before changes.
- [ ] Documentation, styles, app-catalog, and validation report management.
- [ ] Revenue, wallet, and financial dashboards with read/write permissions separated.
- [ ] Monitoring, notifications, incidents, recovery, and automation controls.
- [ ] Security events, audit history, export, retention, and access-revocation controls.
- [ ] Brand customization with QMOI logo, icon, font, motion, and identity tokens without hiding risk state.

### Access and actual usability gate

- Every master-only screen and API requires a server-verified master role/capability; hiding a menu item is not authorization.
- Server-side authorization must confirm the current session, role, resource scope, and requested capability for every protected operation.
- Require MFA/step-up verification for high-impact controls, show read-versus-write capability, and require human confirmation for production, money, domain, user, or provider mutations.
- Test both direct-route and API denial for non-master sessions; test the authorized master path with a real approved identity in a controlled environment.
- Show loading, unavailable, permission-denied, stale, and audit-result states. Never imply a master can use an action until the authenticated route and backend operation are verified.
- Current implementation/access status: unverified from this repository; the autonomous agent tracks these checks but cannot grant itself master access.
<!-- END QMOI MANAGED: master-owned-ui-contract -->
