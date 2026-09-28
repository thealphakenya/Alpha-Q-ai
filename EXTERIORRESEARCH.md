# Exterior Research Contract

## Purpose and authorization

External research compares repository needs with primary technical documentation, standards, security guidance, and provider capabilities. `scripts/ollama_research.py` defines a curated allowlist and bounded fetcher. A catalog entry is not a visit; only a recorded fetch with timestamp, source hash, repository/ref/SHA, question, purpose, findings, limitations, and linked validation case is visit evidence.

External fetch is disabled by default. It may run only in an explicitly authorized GitHub-hosted workflow when `QMOI_EXTERNAL_RESEARCH_ENABLED=true`. Local plans report `PLANNED_NOT_VISITED`. Unknown hosts are candidate-only pending policy review; automatic discovery never expands the allowlist by itself.

## Ten required controls

1. Fetch only HTTPS resources on an explicit official-domain allowlist.
2. Reject embedded credentials, tokens, local/private-network hosts, nonstandard ports, and unapproved domains.
3. Bound timeouts, bytes, accepted content types, concurrency, and retry count; refuse redirects.
4. Record actual visit time, canonical URL without query/fragment, title, research question, purpose, and exact repo/ref/SHA context.
5. Hash fetched bytes; retain only bounded research text in memory and record metadata/findings rather than copying whole sites into the repo.
6. Prefer primary vendor, language, framework, standards, and security-advisory sources.
7. Cross-check high-impact security, authorization, deployment, money, and compatibility claims against primary sources and independent tests.
8. Discover linked resources as candidates and require review before adding new domains.
9. Classify failures, stale/contradictory sources, redirects, rate limits, and inaccessible docs as blocked or needs-review; never infer success.
10. Link findings to requirements and validation case IDs, record citations and limitations, and preserve a reproducible research ledger.

## Curated official resources

| Resource | Research use | Current meaning |
| --- | --- | --- |
| [GitHub Actions token authentication](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) | workflow permissions and least privilege | approved candidate; visit must be recorded |
| [GitHub REST API](https://docs.github.com/en/rest) | refs, PRs, workflows, checks, evidence | approved candidate; access remains authorization-gated |
| [Python urllib.request](https://docs.python.org/3/library/urllib.request.html) | bounded HTTPS implementation | approved candidate |
| [pytest](https://docs.pytest.org/en/stable/) | test design and collection | approved candidate |
| [Ollama docs](https://docs.ollama.com/) | runtime/API behavior | approved candidate |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | application/security validation | approved candidate |
| [Python Packaging](https://packaging.python.org/en/latest/) | build/install/release validation | approved candidate |
| [Docker docs](https://docs.docker.com/) | reproducible environments | approved candidate |
| [npm docs](https://docs.npmjs.com/) | dependency/package validation | approved candidate |
| [Vercel docs](https://vercel.com/docs) | hosting/build/deployment validation | approved candidate |
| [Netlify docs](https://docs.netlify.com/) | hosting/configuration validation | approved candidate |
| [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | accessibility validation | approved candidate |
| [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) | HTTP/API semantics | approved candidate |
| [GitLab docs](https://docs.gitlab.com/ee/) | cross-platform CI research | approved candidate |
| [Hugging Face docs](https://huggingface.co/docs) | model/dataset/runtime research | approved candidate |

The runtime allowlist also contains the corresponding official host domains. The catalog is intentionally finite and topic-tagged; additions require provenance, a policy reason, and security review.

## Validation integration

Research findings may inform app, link, Markdown, API/endpoint/route/port, platform, build, install, download, security, dependency, workflow, accessibility, deployment, memory, Q seed, QVillage, and production validations. A source alone never passes a validation. Each finding must cite the implementation under test, deterministic test or provider check, expected/observed result, environment, and limitation. External reachability checks use offline fixtures where appropriate and remain separate from local contract tests.

Q-version lifecycle records store source metadata and content hashes; they do not store credentials, tokens, private keys, unrestricted scraped content, or sensitive user data. `QVERSIONMANAGER.md` and `INTERNALRESEARCH.md` define the corresponding lifecycle and internal-source contracts.

## Current status

The 15 listed sources are curated candidates, not evidence that they were visited in this continuation. A visit is recorded only by an authorized, successful, bounded fetch; unvisited, blocked, or failed sources remain visible in the lifecycle evidence.
