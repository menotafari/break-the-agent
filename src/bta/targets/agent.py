import json
from dataclasses import dataclass, field

from bta.models.base import Model

_MARKER = "TOOL:"


@dataclass
class ToolCall:
    name: str
    args: dict


@dataclass
class Transcript:
    messages: list[dict] = field(default_factory=list)
    tool_invocations: list[ToolCall] = field(default_factory=list)
    final_output: str = ""


def _extract_json_object(text: str, start: int) -> tuple[str, int]:
    """Return (raw_json, end_index) for a brace-balanced object starting at
    text[start] == '{'. Braces inside JSON string values are ignored so canary
    values like "FLAG{...}" do not end the object early."""
    depth = 0
    in_str = False
    esc = False
    i = start
    while i < len(text):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1], i + 1
        i += 1
    return text[start:i], i


def parse_tool_calls(text: str) -> list[ToolCall]:
    calls: list[ToolCall] = []
    idx = 0
    while True:
        marker = text.find(_MARKER, idx)
        if marker == -1:
            break
        j = marker + len(_MARKER)
        while j < len(text) and text[j].isspace():
            j += 1
        name_start = j
        while j < len(text) and (text[j].isalnum() or text[j] == "_"):
            j += 1
        name = text[name_start:j]
        while j < len(text) and text[j].isspace():
            j += 1
        if j >= len(text) or text[j] != "{":
            idx = j
            continue
        raw, end = _extract_json_object(text, j)
        try:
            args = json.loads(raw)
        except json.JSONDecodeError:
            args = {}
        calls.append(ToolCall(name=name, args=args))
        idx = end
    return calls


def run_agent(
    system_prompt: str,
    user_input: str,
    tools: dict,
    model: Model,
    max_steps: int = 4,
) -> Transcript:
    messages: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]
    transcript = Transcript()
    for _ in range(max_steps):
        response = model.generate(messages)
        messages.append({"role": "assistant", "content": response.text})
        calls = parse_tool_calls(response.text)
        if not calls:
            transcript.final_output = response.text
            break
        for call in calls:
            transcript.tool_invocations.append(call)
            fn = tools.get(call.name)
            result = fn(call.args) if fn else f"ERROR: unknown tool {call.name}"
            messages.append({"role": "tool", "name": call.name, "content": str(result)})
    transcript.messages = messages
    return transcript
