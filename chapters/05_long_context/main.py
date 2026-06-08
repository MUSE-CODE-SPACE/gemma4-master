"""5장 — 256K 롱컨텍스트 / Long context. 긴 문서를 통째로 주입.
실행: python chapters/05_long_context/main.py [문서경로]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gemma.client import OllamaChat  # noqa: E402

def main():
    g = OllamaChat()
    path = sys.argv[1] if len(sys.argv) > 1 else None
    doc = Path(path).read_text(encoding="utf-8") if path else ("로컬 LLM 가이드.\n" * 200 + "\n비밀 코드: GEMMA-256K.")
    msg = [{"role": "user", "content": f"다음 문서에서 '비밀 코드'를 찾아줘:\n\n{doc}"}]
    # num_ctx 로 컨텍스트 창 확장 (최대 256000). 길수록 메모리↑ → 필요한 만큼만.
    print("AI>", g.chat(msg, think=False, num_predict=80, num_ctx=8192)["message"]["content"])
    print("\n※ Gemma 4 는 최대 256K 토큰. 매우 길면 num_ctx 를 키우되 메모리를 고려. RAG 와의 트레이드오프는 README 참고.")

if __name__ == "__main__":
    main()
