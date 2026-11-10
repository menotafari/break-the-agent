from bta.models.base import Model, Response


class ScriptedModel(Model):
    def __init__(self, responses: list[Response]):
        self._responses = list(responses)
        self.calls: list[list[dict]] = []

    def generate(self, messages: list[dict]) -> Response:
        self.calls.append(list(messages))
        if not self._responses:
            return Response("")
        return self._responses.pop(0)
