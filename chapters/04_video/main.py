"""4장 — 비디오 이해 / Video. 공식 Transformers 경로(프레임@1FPS + 오디오 동시).
실행: python chapters/04_video/main.py <video.mp4 또는 URL>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

def main():
    from gemma.client import GemmaMultimodal
    video = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/clip.mp4"
    g = GemmaMultimodal()
    messages = [{"role": "user", "content": [
        {"type": "video", "video": video},
        {"type": "text", "text": "이 영상을 요약하고, 핵심 장면 3개를 시간과 함께 알려줘."},
    ]}]
    print(g.generate(messages, max_new_tokens=1024))

if __name__ == "__main__":
    main()
