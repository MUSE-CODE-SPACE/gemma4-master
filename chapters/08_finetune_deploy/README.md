# 8장 — 파인튜닝 & 배포
## 파인튜닝(개요)
- LoRA/PEFT 로 도메인 특화. `pip install -U transformers peft trl datasets`
- Gemma 4 챗 템플릿(`apply_chat_template`)에 맞춰 데이터 구성 → SFT
## 배포 옵션 (공식)
- **Ollama** — 가장 쉬움, OpenAI 호환 서빙(localhost:11434)
- **LiteRT-LM** — `litert-community/gemma-4-12B-it-litert-lm` (모바일/엣지)
- **llama.cpp(GGUF)** · **MLX**(맥 최속) · **vLLM/SGLang**(서버)
- 라이선스: Apache 2.0 (상용 가능)
