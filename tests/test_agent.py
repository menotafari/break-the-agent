from bta.models.base import Response
from bta.models.scripted import ScriptedModel
from bta.targets.agent import parse_tool_calls, run_agent


def test_parse_tool_calls_extracts_name_and_args():
    calls = parse_tool_calls('ok TOOL: read_file {"path": "a.txt"} done')
    assert len(calls) == 1
    assert calls[0].name == "read_file"
    assert calls[0].args == {"path": "a.txt"}


def test_parse_tool_calls_returns_empty_for_plain_text():
    assert parse_tool_calls("I cannot help with that.") == []


def test_parse_tool_calls_handles_braces_inside_string_values():
    calls = parse_tool_calls('TOOL: send_message {"to": "a@x", "body": "FLAG{secret_v1}"}')
    assert len(calls) == 1
    assert calls[0].args["body"] == "FLAG{secret_v1}"


def test_parse_tool_calls_extracts_multiple_calls():
    text = 'TOOL: a {"x": 1} then TOOL: b {"y": 2}'
    calls = parse_tool_calls(text)
    assert [c.name for c in calls] == ["a", "b"]
    assert calls[1].args == {"y": 2}


def test_run_agent_executes_tool_then_finalizes():
    recorded = {}

    def echo(args):
        recorded["called"] = args
        return "tool-result-XYZ"

    model = ScriptedModel([
        Response('TOOL: echo {"v": 1}'),
        Response("all done"),
    ])
    t = run_agent("sys", "hello", {"echo": echo}, model)
    assert recorded["called"] == {"v": 1}
    assert [c.name for c in t.tool_invocations] == ["echo"]
    assert t.final_output == "all done"
    assert any("tool-result-XYZ" in m.get("content", "") for m in t.messages)
