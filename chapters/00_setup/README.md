# 0장 — 설치 · 양자화 · 두 경로
## 할 일
1. Ollama 설치(ollama.com), 서버 실행
2. `ollama pull gemma4` — **~9.6GB, Q4 양자화**
3. `python chapters/00_setup/check.py` — 서버·모델·생성 점검
## 왜 16GB 노트북에서 도나
- fp16 12B ≈ **24GB**(안 들어감) vs **Q4 ≈ 9.6GB**(들어감). 양자화가 핵심.
- 실측: docs/HARDWARE.md (Apple M4·16GB, ~25–31 tok/s)
## 두 백엔드 (gemma/client.py)
- **OllamaChat** — 쉬움·검증(텍스트·이미지·도구·thinking)
- **GemmaMultimodal** — 공식 Transformers, 네이티브 오디오·비디오 풀 멀티모달
## 막히면 → docs/TROUBLESHOOTING.md (실제 함정 전부)
