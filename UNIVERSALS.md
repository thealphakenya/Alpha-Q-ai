# Autonomous Universal and Authentication Contract

The Ollama autonomous agent must consult this document before creating or
changing authentication, login, identity, permissions, security, device,
protected-data, or cross-platform behavior. Such features must reuse the
universal rules and authentication boundaries defined here, preserve existing
security behavior, and update this document in the same change whenever a new
universal capability or protected-flow rule is introduced.

## Ollama autonomous agent merge and automation contract

The Ollama autonomous agent must read this file together with [STYLES.md](STYLES.md), [ALLMDFILESREFS.md](ALLMDFILESREFS.md), [API.md](API.md), [ENDPOINTS.md](ENDPOINTS.md), [ROUTES.md](ROUTES.md), [ALLPORTS.md](ALLPORTS.md), and the historical guidance in [qmoi-enhanced-history-14](qmoi-enhanced-history-14) before making any repo merge, automation, UI, or protected-flow decision. The active repository remains the source of truth for live behavior, while the historical archive is the reference layer used to recover missing patterns, valid features, and prior architecture decisions without overwriting working code.

The agent must always:
- verify the full markdown inventory against [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- compare active repo state with [qmoi-enhanced-history-14](qmoi-enhanced-history-14) before merge or conflict resolution
- use [STYLES.md](STYLES.md) for all UI, theme, dashboard, and multimodal interface changes
- enforce universal login, identity, access, and risk gating for all protected actions
- record the justification, tested scope, and evidence for every change before marking work complete

## Full-surface universal automation and memory sync

The universal model applies to all QMOI repos, all clone surfaces, all hosted
platforms, and every user-visible surface derived from them. It is not limited
to login screens or account pages. The system must keep the same memory, access,
validation, and proof model synchronized across the active repository, the
historical merge sources, and every clone or platform that is treated as a
QMOI-owned experience.

The agent must automatically:

- inventory every app, platform, clone, and provider surface in the repo
- classify each feature as public, authenticated, mixed-access, or master-only
- synchronize the same access policy across `STYLES.md`, `ALLFRONTEND.md`,
  `ALLBACKEND.md`, `UNIVERSALS.md`, `APP_LINKS.md`, `VERCELLINKS.md`, and the
  clone-specific product docs
- ensure each clone has a valid identity, access gate, and feature contract
- preserve operational safety even when a clone is a partial or derived surface
- keep memory and live-status tracking aligned with the active repo and all clone
  surfaces so the system remains aware, conscious, and synchronized everywhere

This includes QCity, QStore, QStream, QMOI AI, QALPHA, Quantum, QVillage,
GitHub/GitLab/Netlify/Vercel/Hugging Face/Gitpod clones, and all other
platform surfaces discovered in the merge and app inventory. When a clone is
added, the universal contract must be extended at the same time so the platform
is not left without access rules, styling, or a proof-backed link.

## Universal authentication and protected-flow rules

Any feature requiring login, identity, role checks, wallet access, protected data, or user-specific personalization must satisfy the following rules:
- require explicit identity or session validation before access is granted
- preserve audit visibility for security-sensitive actions and state changes
- ensure the UI does not hide risk, wallet health, or decision evidence behind cosmetic personalization
- keep user-specific styling consistent with platform-wide safety and authentication rules
- compare historical and current implementations before enabling a new protected flow or login pattern
- never allow a merge or automation pass to bypass validation, documentation, or route/port alignment

## Public vs. authenticated vs. mixed-access UI classification

The Ollama autonomous agent must classify UI features into three categories before applying universal styling or authentication rules.

### Public/no-account UI

Use public, no-account behavior only when the feature is safe for anonymous browsing and does not reveal user-owned state, private workspace data, protected history, payment information, or privileged controls.

Examples:
- public product catalog pages
- public docs and pricing summaries
- public previews without account-specific data
- public status pages without personal or operational risk details

These views should use the generalized universal UX layer only when the feature is truly public, and should not inherit account-based styling or user-protection features.

### Account/user-scoped UI

Use account-scoped or user-specific behavior when the feature includes private workspace state, profile data, billing or wallet actions, uploaded assets, project ownership, or any action that mutates user-owned resources.

Examples:
- user profile and preference pages
- account-linked wallet, billing, and finance dashboards
- private project or deployment management
- user media libraries, notes, and saved content
- admin or approval workflows that require authorization

These views must use the universal access model with session verification, authorization checks, consent prompts, audit logging, and least-privilege controls.

### Mixed-access UI

Mixed-access pages are public by default but require a user session or authorization for the private or product-changing portion.

Examples:
- a public catalog with a private save, purchase, or deploy action
- a public dashboard that reveals account totals only after identity check
- a public project listing with authenticated editing and approval controls
- public feed pages that include user-specific state or private comments after login

The mixed-access path must keep public and authenticated functions clearly separated, and the universal contract must ensure the UI is not incorrectly rendered as fully public or fully private.

### Universal style selection rules

- public/no-account features should not automatically use account, wallet, or admin visuals unless the feature is explicitly account-scoped
- authenticated features must always use the universal identity/session/auth contract and protection gates
- mixed-access features must render the public shell using the public token set and the private actions using authenticated gating
- if a feature is both public and account-bound, the agent must classify it explicitly as mixed-access and validate the true access boundary before styling

## Feature matrix for access-aware behavior

The agent must track the following access matrix for all apps and platforms:

- public-only features: display, content browse, public info, read-only docs, public preview shells
- authenticated-only features: profile edit, private history, wallet actions, billing decisions, private project control, private media management
- mixed-access features: public detail cards with authenticated publish/save/edit controls; public feed pages with private user data after session validation
- master-only features: billing approvals, production deployment, domain changes, security actions, audit policy changes, and protected infrastructure controls

A feature is only considered universal-safe when its access class, UI treatment, and backend authorization boundary are documented together. If the UI layer and backend policy do not match, the feature must remain blocked and marked for review.

# UNIVERSALS.md - Universal QMOI Standards

## Purpose
This file defines the universal principles and cross-platform capabilities that remain consistent across the QMOI apps and repositories.

## Universal Principles
- resilient automation
- self-healing repo behavior
- monorepo documentation consistency
- GitHub-native execution model
- validation-before-merge workflow
- accountability and traceability
- cross-platform functional parity

## Common Features
- repository health validation
- workflow integrity checks
- memory and checkpoint tracking
- resilience handling for missing or broken files
- sync planning across repos
- branch and PR readiness validation
- deal lifecycle validation across financial workflows
- wallet balance, proof, and settlement verification
- revenue generation and money-making activity monitoring

## Universal Financial and Deal Standards

Every QMOI financial workflow must preserve the same universal standards regardless of platform, user, or revenue model:

- all deals require validation before execution
- all wallet and account actions must be recorded, reconciled, and monitored
- all deals must produce auditable proof of confirmation and settlement
- all revenue and money-making flows must be memory-synced with monitoring and automation
- all user-visible financial UI must preserve operational safety and risk visibility
- all revenue channels, trading surfaces, and deal actions remain part of the same QMOI system memory

## Standard Expectations
Any implementation that enters the QMOI repo is expected to preserve the universal standards above and remain operable even when partial state loss occurs.

QMOI must keep every financial action, deal, wallet flow, trading operation, and user-facing revenue dashboard aligned with the same live memory, validation, and automation model so real-funds operations remain transparent, recoverable, and reliable.

## Orchestration interoperability

The central QMOI orchestrator is part of the universal model. It must be able to discover, rank, and coordinate all workflow, deployment, security, network, style, and autonomous-agent subsystems.

- every orchestrator must declare capability and health metadata
- every automation path must respect validation-before-action rules
- network, VPN, and mask systems are operational dependencies, not optional extras
- live streams and monitoring outputs must share the same source-of-truth state
- historical archive components remain visible to the orchestrator but cannot bypass active safety rules

## Universal policy for live automation

QMOI automation must remain resilient, readable, and auditable at every layer. That means:

- automation decisions are reproducible
- failures produce traceable evidence
- user-visible interfaces preserve safety decisions
- security and privacy remain active even when the system is in a self-healing state
- the repo can continue operating reliably even when local state is unavailable and remote GitHub state remains authoritative


---

## Merged source: ../Alpha-Q-ai/UNIVERSALS.md

# UNIVERSALS.md - Universal QMOI Standards

## Purpose
This file defines the universal principles and cross-platform capabilities that remain consistent across the QMOI apps and repositories.

## Universal Principles
- resilient automation
- self-healing repo behavior
- monorepo documentation consistency
- GitHub-native execution model
- validation-before-merge workflow
- accountability and traceability
- cross-platform functional parity

## Common Features
- repository health validation
- workflow integrity checks
- memory and checkpoint tracking
- resilience handling for missing or broken files
- sync planning across repos
- branch and PR readiness validation
- deal lifecycle validation across financial workflows
- wallet balance, proof, and settlement verification
- revenue generation and money-making activity monitoring

## Universal Financial and Deal Standards

Every QMOI financial workflow must preserve the same universal standards regardless of platform, user, or revenue model:

- all deals require validation before execution
- all wallet and account actions must be recorded, reconciled, and monitored
- all deals must produce auditable proof of confirmation and settlement
- all revenue and money-making flows must be memory-synced with monitoring and automation
- all user-visible financial UI must preserve operational safety and risk visibility
- all revenue channels, trading surfaces, and deal actions remain part of the same QMOI system memory

## Standard Expectations
Any implementation that enters the QMOI repo is expected to preserve the universal standards above and remain operable even when partial state loss occurs.

QMOI must keep every financial action, deal, wallet flow, trading operation, and user-facing revenue dashboard aligned with the same live memory, validation, and automation model so real-funds operations remain transparent, recoverable, and reliable.

## Orchestration interoperability

The central QMOI orchestrator is part of the universal model. It must be able to discover, rank, and coordinate all workflow, deployment, security, network, style, and autonomous-agent subsystems.

- every orchestrator must declare capability and health metadata
- every automation path must respect validation-before-action rules
- network, VPN, and mask systems are operational dependencies, not optional extras
- live streams and monitoring outputs must share the same source-of-truth state
- historical archive components remain visible to the orchestrator but cannot bypass active safety rules

## Universal policy for live automation

QMOI automation must remain resilient, readable, and auditable at every layer. That means:

- automation decisions are reproducible
- failures produce traceable evidence
- user-visible interfaces preserve safety decisions
- security and privacy remain active even when the system is in a self-healing state
- the repo can continue operating reliably even when local state is unavailable and remote GitHub state remains authoritative


---

## Merged source: ../Alpha-Q-ai/Alpha-Q-ai-2025/UNIVERSALS.md

# UNIVERSALS.md - Universal QMOI Standards

## Purpose
This file defines the universal principles and cross-platform capabilities that remain consistent across the QMOI apps and repositories.

## Universal Principles
- resilient automation
- self-healing repo behavior
- monorepo documentation consistency
- GitHub-native execution model
- validation-before-merge workflow
- accountability and traceability
- cross-platform functional parity

## Common Features
- repository health validation
- workflow integrity checks
- memory and checkpoint tracking
- resilience handling for missing or broken files
- sync planning across repos
- branch and PR readiness validation
- deal lifecycle validation across financial workflows
- wallet balance, proof, and settlement verification
- revenue generation and money-making activity monitoring

## Universal Financial and Deal Standards

Every QMOI financial workflow must preserve the same universal standards regardless of platform, user, or revenue model:

- all deals require validation before execution
- all wallet and account actions must be recorded, reconciled, and monitored
- all deals must produce auditable proof of confirmation and settlement
- all revenue and money-making flows must be memory-synced with monitoring and automation
- all user-visible financial UI must preserve operational safety and risk visibility
- all revenue channels, trading surfaces, and deal actions remain part of the same QMOI system memory

## Standard Expectations
Any implementation that enters the QMOI repo is expected to preserve the universal standards above and remain operable even when partial state loss occurs.

QMOI must keep every financial action, deal, wallet flow, trading operation, and user-facing revenue dashboard aligned with the same live memory, validation, and automation model so real-funds operations remain transparent, recoverable, and reliable.

## Orchestration interoperability

The central QMOI orchestrator is part of the universal model. It must be able to discover, rank, and coordinate all workflow, deployment, security, network, style, and autonomous-agent subsystems.

- every orchestrator must declare capability and health metadata
- every automation path must respect validation-before-action rules
- network, VPN, and mask systems are operational dependencies, not optional extras
- live streams and monitoring outputs must share the same source-of-truth state
- historical archive components remain visible to the orchestrator but cannot bypass active safety rules

## Universal policy for live automation

QMOI automation must remain resilient, readable, and auditable at every layer. That means:

- automation decisions are reproducible
- failures produce traceable evidence
- user-visible interfaces preserve safety decisions
- security and privacy remain active even when the system is in a self-healing state
- the repo can continue operating reliably even when local state is unavailable and remote GitHub state remains authoritative


---

## Merged source: qmoi-enhanced-history-14/UNIVERSALS.md

# UNIVERSALS.md

This document defines universal patterns, shared user experience expectations, and memory-aware interaction systems.

## Universal principles

- Prefer production-ready implementations over [AUTOFIXED by Ollama at 2026-07-26T18:54:39.572576Z] or non-production fallbacks.
- Keep documentation, manifests, and implementation state synchronized.
- Maintain consistent role-aware UI and workflow behavior across the QMOI ecosystem.
- Preserve user trust by surfacing verification status, errors, and automation state explicitly.

## Repository-wide expectations

- Backend, frontend, and workflow documentation should remain cross-linked through the manifest files.
- Automation should update the resume ledger and related inventories after each meaningful change.
- The canonical model name remains qmoi and should be referenced consistently across docs and automation.

<!-- BEGIN QMOI MANAGED: universal-ui-access-link -->
## Shared account and UI access contract

The detailed public, authenticated-user, and master-operator UI contract is maintained in [UNIVERSAL.md](UNIVERSAL.md). All apps and cloned-platform consoles must follow the same server-side authorization, consent, audit, and human-confirmation rules.

The autonomous agent updates this section during every validation/runtime documentation refresh; implementation and account access still require source-level and authenticated-session verification.
<!-- END QMOI MANAGED: universal-ui-access-link -->
