# Gemma 4 12B 마스터 — 전체 커리큘럼 (생략 없이)

> 목표: 따라 하면 **Gemma 4 의 발표 기능을 100% 쓸 수 있게** 된다. 각 장 = 개념 + 실행 코드 + 함정.
> 모든 코드/주장은 **공식 문서 + 이 맥북 실측** 기반. (docs/HARDWARE.md, docs/TROUBLESHOOTING.md)

## 0장 — 설치 · 양자화 · 두 경로
- Ollama 설치, `ollama pull gemma4`(Q4 9.6GB), 스모크 테스트(check.py)
- **왜 16GB 에서 도나**: fp16(24GB) vs Q4(9.6GB) — 양자화가 핵심
- 두 백엔드: OllamaChat(쉬움·검증) vs GemmaMultimodal(풀 멀티모달)
- 실습: 00_setup/check.py

## 1장 — 텍스트 · 샘플링 · thinking
- 메시지(role/content), 첫 호출, stateless 와 멀티턴
- 샘플링: temperature·top_p·top_k (Gemma 4 권장 1.0 / 0.95 / 64)
- **thinking(추론) 모드**: think on/off, 길이 한도와 잘림 함정(TROUBLESHOOTING #3·#4)
- 스트리밍
- 실습: 01_text/main.py ✅ 실측

## 2장 — 비전 (이미지)
- 인코더-프리 비전(48×48 패치, 35M 임베더)의 의미
- Ollama 네이티브 `images`(base64)로 이미지 Q&A, OCR, 표/차트 읽기
- 실습: 02_vision/main.py

## 3장 — 네이티브 오디오 (핵심 신기능)
- 왜 "인코더-프리 네이티브 오디오"인가: 16kHz·40ms 프레임을 LLM 입력으로 직접 투영
- **음성 인식(ASR)·화자 분리(diarization)** — 별도 STT 불필요
- 공식 Transformers 경로: `{"type":"audio","audio": ...}`
- 실습: 03_native_audio/main.py (Transformers)

## 4장 — 비디오 이해
- 프레임(1FPS) + 오디오 동시 이해 (공식 예: 313프레임)
- `{"type":"video","video": ...}` — 요약·질의·이벤트 검출
- 실습: 04_video/main.py (Transformers)

## 5장 — 256K 롱컨텍스트
- 긴 문서 통째 주입 vs RAG — 언제 무엇을
- 컨텍스트 한계·비용(길이 한도)·Lost in the Middle 주의
- 실습: 05_long_context/main.py (Ollama, num_ctx)

## 6장 — 구조화 출력 & 도구 호출
- JSON 강제·검증, 도구 스키마, Ollama 네이티브 tools 로 함수 호출
- 실습: 06_structured_tools/main.py (Ollama)

## 7장 — 멀티모달 로컬 에이전트 (캡스톤)
- 도구 + 루프 + 메모리 + (이미지/오디오) → 오프라인 멀티모달 비서
- 실습: 07_multimodal_agent/app.py

## 8장 — 파인튜닝 & 배포
- LoRA/PEFT 도메인 튜닝 개요, 배포 옵션: LiteRT-LM·llama.cpp(GGUF)·MLX·vLLM·OpenAI 호환 서빙
- 실습: 08_finetune_deploy/README.md
