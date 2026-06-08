# 6장 — 구조화 출력 & 도구 호출  ✅ 실측
`python chapters/06_structured_tools/main.py`
- 구조화 출력: Ollama `format`에 **JSON 스키마**(top-level 필드!) → 그 형식으로만 출력 후 검증
  - 함정: `format`을 options 안에 넣으면 무시됨 (TROUBLESHOOTING)
- 도구 호출: `@tool`→스키마, ReAct 루프(gemma/loop.py), 도구 쓸 땐 `think=False` 안정적
