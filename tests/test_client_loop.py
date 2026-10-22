"""Offline tests for the Ollama client request shape and the ReAct tool loop."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma import client as client_mod  # noqa: E402
from gemma import loop as loop_mod  # noqa: E402
from gemma.client import OllamaChat, image_message  # noqa: E402


class _Resp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


class _FakeRequests:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.posts = []

    def post(self, url, json=None, timeout=None, stream=False):
        self.posts.append({"url": url, "json": json})
        return _Resp(self.payloads.pop(0))


def _patched_chat(fake):
    g = OllamaChat(model="gemma4", host="http://localhost:11434/")
    g._requests = fake
    return g


def test_chat_builds_native_api_body():
    fake = _FakeRequests([{"message": {"role": "assistant", "content": "hi"}}])
    g = _patched_chat(fake)
    out = g.chat([{"role": "user", "content": "hello"}], think=False, num_predict=42,
                 format="json", temperature=0.2)
    assert out["message"]["content"] == "hi"
    body = fake.posts[0]["json"]
    assert fake.posts[0]["url"] == "http://localhost:11434/api/chat"  # trailing slash stripped
    assert body["model"] == "gemma4" and body["stream"] is False and body["think"] is False
    assert body["format"] == "json" and "format" not in body["options"]
    assert body["options"]["num_predict"] == 42 and body["options"]["temperature"] == 0.2
    assert body["options"]["top_p"] == 0.95


def test_ask_and_image_message():
    fake = _FakeRequests([{"message": {"role": "assistant", "content": "answer"}}])
    g = _patched_chat(fake)
    assert g.ask("q", system="sys") == "answer"
    msgs = fake.posts[0]["json"]["messages"]
    assert msgs[0] == {"role": "system", "content": "sys"} and msgs[1]["content"] == "q"
    assert image_message("what is this", ["abc="]) == {"role": "user", "content": "what is this", "images": ["abc="]}


def test_tool_loop_executes_tool_then_answers(monkeypatch):
    fake = _FakeRequests([
        {"message": {"role": "assistant", "content": "",
                     "tool_calls": [{"function": {"name": "add", "arguments": {"a": 2, "b": 3}}}]}},
        {"message": {"role": "assistant", "content": "답은 5입니다."}},
    ])
    monkeypatch.setattr(loop_mod, "OllamaChat", lambda: _patched_chat(fake))
    events = []
    out = loop_mod.run("2+3은?", on_event=lambda kind, data: events.append((kind, data)))
    assert out == "답은 5입니다."
    assert events == [("call", {"name": "add", "args": {"a": 2, "b": 3}}),
                      ("result", {"name": "add", "result": 5})]
    second = fake.posts[1]["json"]["messages"]
    assert {"role": "tool", "content": "5", "tool_name": "add"} in second
    assert fake.posts[0]["json"]["tools"], "tool schemas must be sent"


def test_tool_loop_unknown_tool_and_step_cap(monkeypatch):
    tool_turn = {"message": {"role": "assistant", "content": "",
                             "tool_calls": [{"function": {"name": "nope", "arguments": {}}}]}}
    fake = _FakeRequests([tool_turn, tool_turn])
    monkeypatch.setattr(loop_mod, "OllamaChat", lambda: _patched_chat(fake))
    out = loop_mod.run("?", max_steps=2)
    assert "max steps" in out
    assert any("unknown tool" in m.get("content", "") for m in fake.posts[1]["json"]["messages"]
               if m.get("role") == "tool")


def test_module_defaults():
    assert client_mod.OLLAMA_HOST.startswith("http") and client_mod.OLLAMA_MODEL
