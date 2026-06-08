# 5장 — 256K 롱컨텍스트
`python chapters/05_long_context/main.py [문서경로]`
- 긴 문서 통째 주입(num_ctx) vs RAG — 트레이드오프
- Gemma 4 최대 **256K 토큰**. 길수록 메모리↑ → 필요한 만큼만 num_ctx
- 매우 긴 문서는 중간 망각(Lost in the Middle) 주의 → 중요한 건 앞/뒤로
