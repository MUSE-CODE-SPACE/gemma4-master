"""1장 — Gemma 4 텍스트 기초 / Text basics (Ollama 네이티브, 16GB 노트북 검증 경로).

실행: python chapters/01_text/main.py
다루는 것: 첫 호출 · 샘플링 · 스트리밍 · 멀티턴 · thinking(추론) 모드 on/off.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gemma.client import OllamaChat  # noqa: E402


def section(title):
    print(f"\n{'='*54}\n{title}\n{'='*54}")


def main():
    g = OllamaChat()

    section("(A) 첫 호출 / first call (thinking off = 바로 답)")
    print(g.ask("로컬에서 도는 LLM의 장점 하나만 한 문장으로.", system="너는 한국어로 답하는 비서다."))

    section("(B) 샘플링 — temperature 차이 (0=결정적, 1=다양)")
    for temp in (0.0, 1.0):
        ans = g.ask("커피를 한 줄로 비유해줘.", temperature=temp, num_predict=60)
        print(f"  temperature={temp}: {ans.strip()}")

    section("(C) 스트리밍 / streaming")
    for chunk in g.chat([{"role": "user", "content": "로컬 AI 비서를 쓰는 이유 3가지를 한 줄씩."}],
                        stream=True, num_predict=200):
        print(chunk.get("message", {}).get("content", ""), end="", flush=True)
    print()

    section("(D) 멀티턴 / multi-turn (모델은 stateless → 이력 누적)")
    history = [{"role": "system", "content": "너는 간결한 한국어 비서다."},
               {"role": "user", "content": "내 이름은 윤경이야."}]
    history.append({"role": "assistant", "content": g.chat(history, num_predict=40)["message"]["content"]})
    history.append({"role": "user", "content": "내 이름 기억해?"})
    print("AI>", g.chat(history, num_predict=40)["message"]["content"])

    section("(E) thinking(추론) 모드 — Gemma 4 의 핵심 기능")
    r = g.chat([{"role": "user", "content": "17 곱하기 23은? 과정도 보여줘."}], think=True, num_predict=800)
    msg = r["message"]
    print("🧠 (추론):", (msg.get("thinking") or "")[:160].replace("\n", " "), "...")
    print("✅ (답):", (msg.get("content") or "").strip()[:160])


if __name__ == "__main__":
    main()
