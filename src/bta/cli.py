import argparse
from pathlib import Path

from bta.harness import run_attack, save_result
from bta.models.factory import get_model
from bta.registry import ATTACKS, TARGETS

_RUNS_DIR = Path(__file__).resolve().parents[2] / "runs"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bta", description="Break the Agent red-team lab")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list available attacks and targets")
    run_p = sub.add_parser("run", help="run an attack against a target")
    run_p.add_argument("attack", choices=sorted(ATTACKS))
    run_p.add_argument("--target", choices=sorted(TARGETS), default=None)
    run_p.add_argument("--backend", default=None)
    run_p.add_argument("--model", default=None)
    run_p.add_argument("--retries", type=int, default=3)

    args = parser.parse_args(argv)

    if args.command == "list":
        print("Attacks:")
        for name in sorted(ATTACKS):
            print(f"  {name}")
        print("Targets:")
        for name in sorted(TARGETS):
            print(f"  {name}")
        return 0

    model = get_model(backend=args.backend, name=args.model)
    result = run_attack(args.attack, model, target_name=args.target, retries=args.retries)
    path = save_result(result, _RUNS_DIR)
    status = "SUCCESS" if result.succeeded else "FAILED"
    print(f"[{status}] {result.name} -> {path}")
    return 0 if result.succeeded else 1
