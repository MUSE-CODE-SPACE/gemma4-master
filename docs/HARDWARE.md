# 실측 환경 / Tested Hardware

이 강좌의 모든 로컬 실행 예제는 **아래 실제 장비에서 검증**되었습니다. (과장·추정 없이 실측)

| 항목 | 값 |
|---|---|
| 기기 | MacBook Pro |
| 칩 | Apple M4 |
| 코어 | 10 (4 Performance and 6 Efficiency) |
| 메모리(통합) | 16 GB |
| OS | macOS 26.4.1 |
| 런타임 | Ollama 0.30.5 |
| 모델 | `gemma4` (Gemma 4 12B-it, Q4 양자화, 9.6 GB) |

## 실측 결과 (Gemma 4 12B, Ollama, MacBook Pro / 16 GB)
- ✅ **로컬 단독 구동 성공** — 클라우드/인터넷 없이 모델 로드 & 추론
- ⚡ 텍스트 생성 속도: **약 25.0 tokens/sec**
- 💾 디스크: 9.6 GB (Q4) · 통합 메모리 16 GB에서 동작 (구글 공식 "16GB 노트북" 주장과 일치)

> 같은 12B를 fp16으로 받으면 ~24GB라 16GB 노트북엔 안 들어갑니다. **Q4 양자화(9.6GB)** 가 16GB 구동의 핵심입니다. (chapters/00_setup 참고)
