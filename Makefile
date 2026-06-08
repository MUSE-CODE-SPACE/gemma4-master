.PHONY: setup check text vision audio test
setup:; python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && ollama pull gemma4
check:; python chapters/00_setup/check.py
text:;  python chapters/01_text/main.py
vision:; python chapters/02_vision/main.py
test:;  pytest -q
