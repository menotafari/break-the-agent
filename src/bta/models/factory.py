import os

from bta.models.base import Model
from bta.models.ollama_model import OllamaModel


def get_model(backend: str | None = None, name: str | None = None) -> Model:
    backend = backend or os.environ.get("BTA_MODEL_BACKEND", "ollama")
    if backend == "ollama":
        return OllamaModel(model_name=name)
    raise ValueError(f"unknown model backend: {backend}")
