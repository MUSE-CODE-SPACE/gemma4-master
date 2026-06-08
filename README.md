<!-- 🌏 한국어 + English -->
# Gemma 4 12B 마스터 — 로컬에서 텍스트부터 네이티브 멀티모달 에이전트까지
### Master Gemma 4 12B locally — from text to native multimodal agents

> 구글 딥마인드 **Gemma 4 12B**(2026-06-03, Apache 2.0)를 **내 노트북에서** 100% 활용하는 실습 강좌.
> 공식 문서 기준으로 구현했고, **이 맥북(Apple M4·16GB)에서 실제로 돌려 검증**했습니다. (환각·생략 없이)
>
> A hands-on course to use **Gemma 4 12B** fully on your own laptop — verified on a real 16GB Apple M4 MacBook.

## ✅ 실측 (docs/HARDWARE.md)
- **MacBook Pro · Apple M4 · 16GB · macOS 26 · Ollama 0.30** 에서 **gemma4 (Q4, 9.6GB) 로컬 구동 성공**
- 텍스트 생성 **~25–31 tok/s** · 클라우드/인터넷 0 · 비용 0
- 설치하며 겪은 **모든 함정은 docs/TROUBLESHOOTING.md** 에 빠짐없이 기록

## Gemma 4 12B 가 특별한 이유 (공식)
- **인코더-프리 멀티모달**: 텍스트·이미지·비디오 + **중형 모델 최초 네이티브 오디오**(ASR·화자분리)를 한 디코더에
- **256K 컨텍스트** · 성능 ≈ 구글 26B급 · **Multi-Token Prediction**으로 빠른 응답
- **Apache 2.0 오픈웨이트** · Ollama·Transformers·llama.cpp·MLX·vLLM·LiteRT 어디서든
- 출처: developers.googleblog.com/gemma-4-12b · huggingface.co/google/gemma-4-12B-it · ollama.com/library/gemma4

## 두 가지 경로 (gemma/client.py)
| 경로 | 무엇 | 검증 |
|---|---|---|
| **OllamaChat** (네이티브 /api/chat) | 텍스트·이미지·도구·thinking | ✅ 16GB 노트북 실측 |
| **GemmaMultimodal** (Transformers) | + **네이티브 오디오·비디오** 풀 멀티모달 | 공식 API 구현 (GPU/대용량 권장) |

## 빠른 시작
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull gemma4          # ~9.6GB (Q4)
python chapters/00_setup/check.py     # 설치 점검
python chapters/01_text/main.py       # 첫 실행
```

## 커리큘럼 (자세히는 COURSE.md)
0. 설치 & 양자화 & 두 경로  1. 텍스트·샘플링·thinking  2. 비전(이미지)
3. **네이티브 오디오**(전사·화자분리)  4. 비디오 이해  5. 256K 롱컨텍스트
6. 구조화 출력 & 도구 호출  7. 멀티모달 로컬 에이전트(캡스톤)  8. 파인튜닝 & 배포

## License — MIT (교육용). Gemma 4 모델 자체는 Apache 2.0 (Google).
