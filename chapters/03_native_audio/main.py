"""3장 — 네이티브 오디오(전사·화자분리) / Native audio. 공식 Transformers 경로.
주의: 풀 멀티모달은 무겁다 → pip install -U transformers torch accelerate (GPU/대용량 권장).
실행: python chapters/03_native_audio/main.py <audio.wav 또는 URL>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

def main():
    from gemma.client import GemmaMultimodal  # 무거운 임포트는 함수 안에서
    audio = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/speech.wav"
    g = GemmaMultimodal()  # AutoProcessor + AutoModelForMultimodalLM
    # 공식 메시지 형식 — 오디오를 LLM 입력으로 직접 (인코더 프리)
    messages = [{"role": "user", "content": [
        {"type": "text", "text": "이 음성을 전사하고, 화자를 분리해줘 (speaker diarization)."},
        {"type": "audio", "audio": audio},
    ]}]
    print(g.generate(messages, max_new_tokens=1024))

if __name__ == "__main__":
    main()
