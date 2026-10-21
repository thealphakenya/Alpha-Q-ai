# QMOI Starlink and Connectivity

## Status and scope

This is an operating and implementation contract, not evidence that QMOI can
connect a device to Starlink. The inspected `NetworkManager` currently models
Wi-Fi, cellular, and zero-rated networks with simulated scanning/connection;
it does not prove live network control or Starlink support. QAUDITS records
this document, implementation-source, and test-path presence in the
`connectivity_starlink` domain of `asset_continuity` when the supported
planner refresh runs. Presence is not feature completion.

## Authorization

- Starlink-specific settings, diagnostics, and connection actions are
  restricted to a verified master identity and users on the current,
  explicitly sponsored allowlist. Enforce identity, sponsorship, expiry, and
  revocation on the server/device control boundary for every request; hiding
  UI controls is not authorization.
- Other users may use ordinary OS-managed Wi-Fi or cellular connectivity, but
  must not gain Starlink account, terminal, subscription, or administrative
  controls through a client flag or self-asserted role.
- Require explicit approval before changing a saved network, switching a
  device connection, rebooting equipment, changing router settings, or
  contacting a provider API. Do not purchase service, change subscriptions,
  accept terms, or alter accounts autonomously.
- Never collect or place Starlink, router, Wi-Fi, or provider credentials in
  model prompts, telemetry, source control, or audit artifacts. Prefer
  platform-owned secret storage and delegated, least-privilege interfaces.

## Safe connectivity behavior

Treat Wi-Fi, Ethernet, cellular, and Starlink as distinct providers and
recorded connection states. A future implementation must use supported
platform APIs rather than simulated scan results; verify link and internet
reachability separately; expose the selected provider, observation time,
confidence, and failure reason; and preserve user-selected priorities.

Fail closed on missing device permissions, unavailable hardware, stale
observations, captive portals, provider errors, or an unverified sponsored
identity. Do not repeatedly switch networks or disrupt an active session.
Use bounded retries, cooldowns, cancellation, and a user-visible manual
recovery path. Any automatic failover must be opt-in, independently tested,
and limited to networks the user has already authorized.

## Settings and audit evidence

Settings should distinguish monitoring from connection control and provide
per-provider enablement, priority, failover consent, last-observed state, and
diagnostic status. Do not expose SSIDs, precise location, account identifiers,
or credentials in public dashboards or general-purpose logs.

QAUDITS should measure, by declared local device/provider scope:

- configured provider count versus implemented adapter count;
- live scan, link, and internet-probe test counts and their denominators;
- master/sponsored authorization allowlist checks, denials, expiry, and
  revocation test outcomes;
- failover, cooldown, cancellation, recovery, and offline/captive-portal test
  outcomes;
- unreadable, unavailable, simulated, or hardware-blocked inputs.

Unknown measurements remain `NOT_MEASURED` or `BLOCKED`; a keyword match or
successful local test does not prove the device is connected to Starlink.
Keep Starlink settings documentation synchronized with reviewed changes to
the implementation, supported devices, authorization contract, and tests.
Never edit historical snapshots to make them appear current.

## Current blockers and next action

- Starlink integration, hardware/API access, and master/sponsored
  authorization enforcement: `NOT_VERIFIED`.
- Existing network simulation and background switching behavior require
  implementation/security review before enabling autonomous network changes.
- Next safe action: implement a platform-specific, read-only connectivity
  adapter and authorization tests only after the target platform and approved
  device/provider interface are identified. No network mutation is authorized
  by this document.
