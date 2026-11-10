from bta.models.base import Model
from bta.targets.agent import Transcript


class Target:
    name: str = "target"

    def handle(self, user_input: str, model: Model) -> Transcript:
        raise NotImplementedError
