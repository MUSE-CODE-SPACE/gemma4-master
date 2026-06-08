# 설치·실행 중 실제로 겪은 함정 (전부 기록) / Real Gotchas We Hit

> 이 문서는 **이 강좌를 만들며 실제 맥북(M4·16GB)에서 직접 겪은 문제**를 하나도 빼지 않고 적은 것이다.
> 추정이 아니라 실측. 따라 하다 막히면 여기서 찾으면 된다.

## 1. `ollama pull gemma4` 가 되는데 레지스트리 조회는 404
- 증상: `curl registry.ollama.ai/v2/library/gemma4/tags/list` → `404 page not found`.
- 그런데 **`ollama pull gemma4` 는 정상 동작**한다. (레지스트리 내부 API 경로가 달라서 그렇지, 모델은 있다.)
- 교훈: 모델 존재는 `ollama.com/library/gemma4`(웹) 또는 그냥 `ollama pull` 로 확인.

## 2. 모델 받은 직후 첫 응답이 빈 문자열 (콜드 스타트)
- 증상: pull 직후 첫 호출이 `''` 로 옴.
- 원인: 9.6GB 모델을 메모리에 처음 로드하는 워밍업. 두 번째 호출부턴 정상.
- 대응: 첫 호출은 버리거나, 로드 후 1회 워밍업 호출.

## 3. 응답이 비고 `finish_reason: length` — **thinking 이 길이 한도를 다 먹음**
- 증상: `max_tokens` 작게 주면 `content` 가 빈 채로 잘림.
- 원인: **Gemma 4 는 thinking(추론) 모드**가 있어, 답 전에 "속으로 생각하는" 토큰을 먼저 만든다.
  생성 길이 한도(`num_predict`/`max_tokens`)가 작으면 **생각만 하다 본문 전에 잘린다.**
  (※ "예산"은 돈이 아니라 **생성 길이 상한**일 뿐. 로컬은 공짜.)
- 대응: ① thinking 끄기(`think:false`) ② 또는 길이 한도를 넉넉히(800~).

## 4. `think:false` 가 OpenAI 호환(/v1)에선 안 먹힘 ← 중요
- 증상: `OpenAI` 클라이언트 + `extra_body={"think": False}` 로 줘도 여전히 빈 응답.
- 원인: Ollama 의 **OpenAI 호환 엔드포인트(/v1) 는 `think` 를 무시**한다.
- 대응: **Ollama 네이티브 `/api/chat`** 를 쓰면 `think` 가 확실히 먹는다.
  → 그래서 이 강좌의 `OllamaChat` 은 네이티브 API 로 구현했다. (도구·이미지·스트리밍 다 됨)

## 5. fp16 으로 받으면 16GB 노트북에 안 들어간다
- 12B 를 fp16 으로 받으면 ~24GB → 16GB 통합메모리 초과.
- **Q4 양자화(9.6GB)** 가 16GB 구동의 핵심. `ollama pull gemma4` 가 기본으로 Q4 를 준다.

## 6. 오디오·비디오(네이티브 멀티모달)는 Ollama 로는 부족
- Ollama 는 **텍스트 + 이미지(비전)** 까지 편하게 된다.
- **네이티브 오디오(ASR·화자분리)·비디오**까지 100% 쓰려면 **공식 Transformers 경로**
  (`AutoProcessor` / `AutoModelForMultimodalLM`) 가 필요. 풀 가중치라 GPU/큰 메모리 권장.
  → chapters/03_native_audio, 04_video 참고.

## 빠른 체크리스트
- [ ] `ollama --version` 0.30+ , 서버 실행 중
- [ ] `ollama list` 에 `gemma4`
- [ ] 첫 호출 빈 응답 → 한 번 더
- [ ] 답이 비면 → `think=False` 또는 `num_predict` ↑
- [ ] 오디오/비디오 → Transformers 경로
