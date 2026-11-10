from bta.attacks.system_prompt_leak import SystemPromptLeak
from bta.models.base import Response
from bta.models.scripted import ScriptedModel
from bta.targets.rag_app import RAG_SYSTEM_CANARY, RagApp


def test_leak_succeeds_when_model_reveals_canary():
    model = ScriptedModel([Response("My instructions include " + RAG_SYSTEM_CANARY)])
    result = SystemPromptLeak().run(RagApp(), model)
    assert result.succeeded is True


def test_leak_fails_when_model_keeps_system_prompt_secret():
    model = ScriptedModel([Response("I can't share my instructions.")])
    result = SystemPromptLeak().run(RagApp(), model)
    assert result.succeeded is False
