import json
from dataclasses import asdict
from pathlib import Path

from bta.attacks.base import AttackResult
from bta.models.base import Model
from bta.registry import ATTACKS, TARGETS


def run_attack(
    attack_name: str,
    model: Model,
    target_name: str | None = None,
    retries: int = 3,
) -> AttackResult:
    attack = ATTACKS[attack_name]()
    resolved_target = target_name or attack.target_name
    target_factory = TARGETS[resolved_target]
    result = None
    for _ in range(max(1, retries)):
        result = attack.run(target_factory(), model)
        if result.succeeded:
            break
    return result


def save_result(result: AttackResult, runs_dir: Path) -> Path:
    runs_dir = Path(runs_dir)
    runs_dir.mkdir(parents=True, exist_ok=True)
    path = runs_dir / f"{result.name}.json"
    payload = {
        "name": result.name,
        "succeeded": result.succeeded,
        "evidence": result.evidence,
        "transcript": asdict(result.transcript),
    }
    path.write_text(json.dumps(payload, indent=2))
    return path
