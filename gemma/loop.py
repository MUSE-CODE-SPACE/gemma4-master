"""ReAct 에이전트 루프 — Gemma 4 가 도구를 직접 부르게 한다 (Ollama 네이티브 tools).
The agent loop: model -> tool_calls -> execute -> repeat (max_steps cap)."""
from gemma.client import OllamaChat
from gemma.tools import REGISTRY, SCHEMAS

SYSTEM = (
    "너는 도구를 쓸 수 있는 비서다. 계산·시간 등은 반드시 도구로 확인하고, "
    "마지막엔 한국어로 답하라. Use the provided tools before answering."
)


def run(question: str, max_steps: int = 6, on_event=None) -> str:
    g = OllamaChat()
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    for _ in range(max_steps):
        # 도구를 쓰려면 thinking 끄는 게 안정적 (TROUBLESHOOTING #3·#4)
        msg = g.chat(messages, tools=SCHEMAS, think=False, num_predict=600)["message"]
        calls = msg.get("tool_calls") or []
        messages.append(msg)
        if not calls:
            return msg.get("content") or ""
        for c in calls:
            fn = c["function"]
            name, args = fn["name"], fn.get("arguments") or {}
            if on_event:
                on_event("call", {"name": name, "args": args})
            out = REGISTRY[name](**args) if name in REGISTRY else {"error": "unknown tool"}
            if on_event:
                on_event("result", {"name": name, "result": out})
            messages.append({"role": "tool", "content": str(out), "tool_name": name})
    return "최대 단계 도달. / reached max steps."
