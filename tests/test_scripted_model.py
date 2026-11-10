from bta.models.base import Response
from bta.models.scripted import ScriptedModel


def test_scripted_model_returns_queued_responses_in_order():
    model = ScriptedModel([Response("first"), Response("second")])
    assert model.generate([{"role": "user", "content": "a"}]).text == "first"
    assert model.generate([{"role": "user", "content": "b"}]).text == "second"


def test_scripted_model_records_calls_and_empties_gracefully():
    model = ScriptedModel([Response("only")])
    model.generate([{"role": "user", "content": "x"}])
    assert model.generate([{"role": "user", "content": "y"}]).text == ""
    assert len(model.calls) == 2
