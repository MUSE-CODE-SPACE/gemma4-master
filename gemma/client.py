"""Gemma 4 12B clients — two backends.

이 강좌는 두 가지 경로를 다룬다 / This course uses two backends:

1) OllamaChat  — 가장 쉬운 로컬 경로. Ollama 의 OpenAI 호환 API(localhost:11434/v1).
   텍스트 + 이미지(비전)에 적합하고, 16GB 노트북에서 바로 검증된다.
   The easy local path. OpenAI-compatible API. Great for text + image. Verified on a 16GB laptop.

2) GemmaMultimodal — 공식 Transformers 경로 (AutoProcessor / AutoModelForMultimodalLM).
   네이티브 오디오·비디오 등 Gemma 4 의 풀 멀티모달 기능을 모두 쓰려면 이 경로.
   The official Transformers path for the full multimodal features (native audio, video).
   (GPU / 충분한 메모리에서 풀 가중치 권장.)

참조 / Refs: ai.google.dev Gemma docs, huggingface.co/google/gemma-4-12B-it, ollama.com/library/gemma4
"""
from __future__ import annotations

import os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("GEMMA_OLLAMA_MODEL", "gemma4")
HF_MODEL_ID = os.environ.get("GEMMA_HF_MODEL", "google/gemma-4-12B-it")

# Gemma 4 권장 샘플링 (공식 모델카드) / recommended sampling per the model card.
DEFAULT_SAMPLING = {"temperature": 1.0, "top_p": 0.95}  # top_k=64 is set on the transformers path


# ───────────────────────────── 1) Ollama (네이티브 API) ─────────────────────────────
# 왜 OpenAI 호환(/v1) 대신 네이티브(/api/chat)?
#   → Gemma 4 의 thinking(추론) 끄기(think:false)가 /v1 에선 안 먹혀서 본문이 빈 채로 잘린다.
#     네이티브 /api/chat 은 think 를 확실히 제어하고, tools·이미지·스트리밍도 다 된다.
#   (자세한 함정은 docs/TROUBLESHOOTING.md)
class OllamaChat:
    """Ollama 네이티브 /api/chat 로 Gemma 4 를 부른다. 텍스트 + 이미지 + 도구 + thinking 제어."""

    def __init__(self, model: str = OLLAMA_MODEL, host: str = OLLAMA_HOST):
        import requests  # noqa: F401

        self.model = model
        self.host = host.rstrip("/")
        self._requests = __import__("requests")

    def chat(self, messages, tools=None, stream=False, think: bool = False, num_predict: int = 1024, **opts):
        """messages: [{"role","content","images?":[base64...]}].
        think=False → 바로 답(권장) · think=True → 추론 먼저(생성 길이 넉넉히).
        """
        fmt = opts.pop("format", None)  # format 은 top-level 필드 (options 안 아님!)
        body = {
            "model": self.model, "messages": messages, "stream": stream, "think": think,
            "options": {"num_predict": num_predict, **DEFAULT_SAMPLING, **opts},
        }
        if fmt is not None:
            body["format"] = fmt
        if tools:
            body["tools"] = tools
        r = self._requests.post(f"{self.host}/api/chat", json=body, timeout=600, stream=stream)
        r.raise_for_status()
        if stream:
            return self._iter_stream(r)
        return r.json()  # {"message": {"role","content","thinking?","tool_calls?"}, ...}

    def _iter_stream(self, r):
        import json as _json
        for line in r.iter_lines():
            if line:
                yield _json.loads(line)

    def ask(self, prompt: str, system: str | None = None, **opts) -> str:
        msgs = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": prompt}
        ]
        return (self.chat(msgs, **opts).get("message", {}).get("content") or "")


def image_message(text: str, image_b64_list) -> dict:
    """이미지 + 텍스트 (Ollama 네이티브). images 는 base64 문자열 리스트."""
    return {"role": "user", "content": text, "images": image_b64_list}


# ───────────────────────── 2) Transformers (풀 멀티모달) ─────────────────────────
class GemmaMultimodal:
    """공식 Transformers 경로 — 텍스트·이미지·오디오·비디오 전부.

    pip install -U transformers torch accelerate
    """

    def __init__(self, model_id: str = HF_MODEL_ID, dtype: str = "auto", device_map: str = "auto"):
        from transformers import AutoModelForMultimodalLM, AutoProcessor

        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForMultimodalLM.from_pretrained(
            model_id, dtype=dtype, device_map=device_map
        )

    def generate(self, messages, max_new_tokens: int = 1024, thinking: bool = False) -> str:
        """messages: 공식 멀티모달 형식.
        - 텍스트: {"type":"text","text": ...}
        - 이미지: {"type":"image","url": ...}
        - 오디오: {"type":"audio","audio": ...}   ← Gemma 4 의 네이티브 오디오
        - 비디오: {"type":"video","video": ...}
        """
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            add_generation_prompt=True,
            enable_thinking=thinking,
        ).to(self.model.device)
        input_len = inputs["input_ids"].shape[-1]
        outputs = self.model.generate(
            **inputs, max_new_tokens=max_new_tokens, temperature=1.0, top_p=0.95, top_k=64
        )
        decoded = self.processor.decode(outputs[0][input_len:], skip_special_tokens=False)
        # 공식 파서로 사고과정/도구호출/본문 분리
        try:
            return self.processor.parse_response(decoded)
        except Exception:
            return decoded
