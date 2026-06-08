"""0장 — 설치 스모크 테스트 / Setup smoke test.

확인: (1) Ollama 서버, (2) gemma4 모델 받음, (3) 실제 한 토큰 생성.
Checks: Ollama up, gemma4 pulled, and a real generation.
"""
import sys

import urllib.request
import json

BASE = "http://localhost:11434"
MODEL = "gemma4"


def _get(path):
    with urllib.request.urlopen(BASE + path, timeout=5) as r:
        return json.loads(r.read())


def main() -> int:
    # 1) 서버
    try:
        tags = _get("/api/tags")
    except Exception as e:
        print(f"✗ Ollama 서버에 연결 못함 ({e}). `ollama serve` 또는 Ollama 앱 실행 필요.")
        return 1
    print("✓ Ollama 서버 연결됨")

    # 2) 모델
    names = [m["name"] for m in tags.get("models", [])]
    if not any(n.startswith(MODEL) for n in names):
        print(f"✗ '{MODEL}' 모델이 없음. `ollama pull {MODEL}` 먼저 실행. (~9.6GB, Q4)")
        return 1
    print(f"✓ 모델 {MODEL} 준비됨")

    # 3) 실제 생성
    req = urllib.request.Request(
        BASE + "/api/generate",
        data=json.dumps({"model": MODEL, "prompt": "Reply with just: OK", "stream": False,
                         "options": {"num_predict": 8}}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            out = json.loads(r.read())
    except Exception as e:
        print(f"✗ 생성 실패 ({e})")
        return 1
    print(f"✓ 생성 동작 — 응답: {out.get('response','').strip()[:60]!r}")
    print("\n준비 완료! 1장으로 가세요. / All set — go to chapter 01.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
