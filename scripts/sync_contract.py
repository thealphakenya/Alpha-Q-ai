"""Structured cross-repository synchronization contract."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class SyncContract:
    sync_id: str
    source: str
    target: str
    source_sha: str | None
    target_sha_before: str | None
    direction: str
    mode: str
    authorization: str
    created_at: str

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["contract_hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return payload

    def requires_target_workflow(self) -> bool:
        return self.mode in {"apply", "promote"} and self.authorization != "AUTH_READY"


def build_sync_contract(sync_id: str, source: str, target: str, source_sha: str | None, target_sha_before: str | None, *, mode: str = "dry-run", authorization: str = "AUTH_UNKNOWN") -> SyncContract:
    return SyncContract(sync_id, source, target, source_sha, target_sha_before, f"{source}->{target}", mode, authorization, utc_iso())
