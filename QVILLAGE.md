# QVILLAGE.md

QVillage is the live QMOI community, model, and knowledge coordination surface. It is treated as the master-only QMOI community layer that stays synchronized with GitHub, Hugging Face, and the live autonomous agent.

## Active automation
- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.
- memory, model, and runtime state are synchronized across repo docs and platform references.
- the live state is refreshed automatically as the repository evolves.

## QVillage model-card and trading UI requirements

QVillage must show the same verified model evidence as the canonical model-card and comparison docs. It should not show a stronger or more optimistic state than the repo can support.

### Required UI blocks
- model name, version, and health state
- validation status and evidence timestamp
- benchmark comparison status against leading frontier models
- memory recovery and data provenance state
- dataset and model-refresh status
- trading platform status: Binance, Bitget, CashOn, and other verified venues
- risk alerts, blocked states, and kill-switch readiness
- last update source and whether the card is stale, blocked, or production-ready

### Required sync standard
- the UI must reflect the same evidence fields shown in [MODEL_CARD.md](MODEL_CARD.md) and [QMOI_MODEL_CARD.md](QMOI_MODEL_CARD.md)
- any comparison claim must be backed by a benchmark or validation proof before publication
- any blocked or missing evidence must remain visible as blocked, not silently converted into green status
- trading and platform metrics must remain aligned with [Qtrade.md](Qtrade.md) and [compare.md](compare.md)

### Safety and automation rule
QVillage should enhance the user experience without creating false confidence. The agent may automate refreshes, but it must never mark the model or trading layer as healthy if the underlying evidence, dataset lineage, or safety checks are incomplete.

