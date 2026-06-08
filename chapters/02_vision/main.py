"""2장 — 비전(이미지) / Vision. Ollama 네이티브 images(base64). 실행: python chapters/02_vision/main.py [이미지경로]"""
import base64, io, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gemma.client import OllamaChat  # noqa: E402

def to_b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()

def make_sample(path: str):
    """샘플 이미지가 없으면 글자 들어간 이미지 하나 생성 (pillow)."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (480, 200), "white"); d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 470, 190], outline="black", width=3)
    d.text((40, 80), "GEMMA 4  =  12B", fill="black")
    img.save(path)

def main():
    g = OllamaChat()
    path = sys.argv[1] if len(sys.argv) > 1 else "assets/tmp/sample.png"
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if not Path(path).exists():
        make_sample(path); print(f"샘플 이미지 생성: {path}")
    msg = {"role": "user", "content": "이 이미지에 무엇이 보여? 글자가 있으면 읽어줘.",
           "images": [to_b64(path)]}
    print("AI>", g.chat([msg], think=False, num_predict=300)["message"]["content"])

if __name__ == "__main__":
    main()
