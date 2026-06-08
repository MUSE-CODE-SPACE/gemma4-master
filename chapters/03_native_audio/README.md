# 3장 — 네이티브 오디오 (핵심 신기능)
`python chapters/03_native_audio/main.py <audio.wav|URL>`  (Transformers 경로)
- **인코더-프리 네이티브 오디오**: 16kHz·40ms 프레임을 LLM 입력으로 직접 투영 → 별도 STT 불필요
- 음성 인식(ASR) · 화자 분리(diarization)
- 공식 형식: `{"type":"audio","audio": ...}` + `AutoModelForMultimodalLM`
- ⚠ 풀 가중치라 무거움: `pip install -U transformers torch accelerate` (GPU/대용량 메모리 권장)
