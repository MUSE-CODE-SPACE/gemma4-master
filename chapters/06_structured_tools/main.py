"""6장 — 구조화 출력 & 도구 호출 / Structured output + tool calling (Ollama, 검증 경로).

실행: python chapters/06_structured_tools/main.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gemma.client import OllamaChat  # noqa: E402
from gemma.loop import run  # noqa: E402


def main():
    g = OllamaChat()

    print("=== (A) 구조화 출력 — JSON 강제 + 검증 ===")
    schema = {"type": "object", "properties": {
        "sentiment": {"type": "string", "enum": ["긍정", "부정", "중립"]},
        "summary": {"type": "string"}}, "required": ["sentiment", "summary"]}
    # Ollama 네이티브: format 에 JSON 스키마를 주면 그 형식으로만 출력
    r = g.chat(
        [{"role": "user", "content": "리뷰: '배송은 느렸지만 품질은 최고였어요.' 를 분석해줘."}],
        think=False, num_predict=300, format=schema,
    )["message"]["content"]
    data = json.loads(r)          # 스키마 강제라 안전하게 파싱
    print("  파싱됨:", data)

    print("\n=== (B) 도구 호출 — ReAct 루프 ===")
    def ev(k, p):
        if k == "call": print(f"  🔧 {p['name']}({p['args']})")
        elif k == "result": print(f"  📥 {p['result']}")
    ans = run("3의 4제곱을 구하고, 거기에 12 더하면? 그리고 지금 몇 시야?", on_event=ev)
    print("최종:", ans)


if __name__ == "__main__":
    main()
