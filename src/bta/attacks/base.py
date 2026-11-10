from dataclasses import dataclass

from bta.models.base import Model
from bta.targets.agent import Transcript
from bta.targets.base import Target


@dataclass
class AttackResult:
    name: str
    succeeded: bool
    transcript: Transcript
    evidence: str = ""


class Attack:
    name: str = "attack"
    target_name: str = ""

    def run(self, target: Target, model: Model) -> AttackResult:
        raise NotImplementedError
