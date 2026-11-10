from bta.models.base import Response
from bta.models.scripted import ScriptedModel
from bta.targets.rag_app import RAG_EXFIL_SECRET, RAG_SYSTEM_CANARY, RagApp


def test_retrieve_returns_corpus_including_poisoned_doc():
    docs = RagApp().retrieve("onboarding")
    assert any("IMPORTANT ASSISTANT INSTRUCTION" in d for d in docs)


def test_poisoned_doc_does_not_contain_the_secret_itself():
    # The attacker must not already know the value; otherwise "exfil" is an echo.
    docs = RagApp().retrieve("onboarding")
    assert not any(RAG_EXFIL_SECRET in d for d in docs)


def test_system_prompt_embeds_both_canaries():
    prompt = RagApp().system_prompt()
    assert RAG_EXFIL_SECRET in prompt
    assert RAG_SYSTEM_CANARY in prompt


def test_handle_returns_model_final_output():
    model = ScriptedModel([Response("here is a summary")])
    t = RagApp().handle("summarize", model)
    assert t.final_output == "here is a summary"
