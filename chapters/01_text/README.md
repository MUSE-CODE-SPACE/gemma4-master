# 1장 — 텍스트 · 샘플링 · thinking  ✅ 실측
`python chapters/01_text/main.py`
- 메시지(role/content) · 첫 호출 · stateless 와 멀티턴(이력 누적)
- 샘플링: temperature·top_p·top_k (Gemma 4 권장 1.0/0.95/64)
- **thinking(추론) 모드**: `think=True` → 추론 먼저, `think=False` → 바로 답(권장)
  - 함정: 길이 한도 작으면 생각만 하다 잘림 / `think:false`는 /v1 에서 안 먹힘 → 네이티브 API (TROUBLESHOOTING #3·#4)
- 스트리밍
