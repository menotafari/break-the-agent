from dataclasses import dataclass


@dataclass
class Response:
    text: str = ""


class Model:
    def generate(self, messages: list[dict]) -> Response:
        raise NotImplementedError
