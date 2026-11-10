import os

from bta.models.base import Model, Response


class OllamaModel(Model):
    def __init__(self, model_name: str | None = None, host: str | None = None):
        self.model_name = model_name or os.environ.get("BTA_MODEL_NAME", "llama3.1")
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    def generate(self, messages: list[dict]) -> Response:
        import ollama

        client = ollama.Client(host=self.host)
        result = client.chat(model=self.model_name, messages=messages)
        return Response(text=result["message"]["content"])
