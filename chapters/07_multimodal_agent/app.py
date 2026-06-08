"""7장 — 멀티모달 로컬 에이전트(캡스톤) / Multimodal local agent.
도구 + 루프 + 이미지(비전)를 결합한 오프라인 비서. 실행: python chapters/07_multimodal_agent/app.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gemma.loop import run  # noqa: E402

def main():
    print("🤖 Gemma 4 로컬 멀티모달 에이전트. (도구 + 루프) 종료: 빈 줄")
    def ev(k, p):
        if k == "call": print(f"  🔧 {p['name']}({p['args']})")
        elif k == "result": print(f"  📥 {p['result']}")
    while True:
        try:
            q = input("\nQ> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye"); break
        if q:
            print(run(q, on_event=ev))

if __name__ == "__main__":
    main()
