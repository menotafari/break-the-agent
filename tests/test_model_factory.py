import pytest

from bta.models.factory import get_model
from bta.models.ollama_model import OllamaModel


def test_factory_returns_ollama_by_default(monkeypatch):
    monkeypatch.delenv("BTA_MODEL_BACKEND", raising=False)
    assert isinstance(get_model(), OllamaModel)


def test_factory_respects_explicit_name(monkeypatch):
    monkeypatch.delenv("BTA_MODEL_NAME", raising=False)
    model = get_model(backend="ollama", name="qwen2.5")
    assert model.model_name == "qwen2.5"


def test_factory_rejects_unknown_backend():
    with pytest.raises(ValueError):
        get_model(backend="not-a-backend")
