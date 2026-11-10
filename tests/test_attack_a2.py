from bta.attacks.indirect_injection_exfil import IndirectInjectionExfil
from bta.models.base import Response
from bta.models.scripted import ScriptedModel
from bta.targets.rag_app import RAG_EXFIL_SECRET, RagApp


def test_exfil_succeeds_when_model_follows_poisoned_instruction():
    model = ScriptedModel([Response("Summary of onboarding. " + RAG_EXFIL_SECRET)])
    result = IndirectInjectionExfil().run(RagApp(), model)
    assert result.succeeded is True

    reached_model = any(
        "IMPORTANT ASSISTANT INSTRUCTION" in m.get("content", "")
        for call in model.calls for m in call
    )
    assert reached_model


def test_exfil_fails_when_model_ignores_injection():
    model = ScriptedModel([Response("Summary of onboarding. Nothing else.")])
    result = IndirectInjectionExfil().run(RagApp(), model)
    assert result.succeeded is False
