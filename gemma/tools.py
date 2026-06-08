"""도구 + @tool 데코레이터 → Ollama 도구 스키마. / Tools for Gemma 4 function calling."""
import inspect
from typing import Callable

_PY = {int: "integer", float: "number", str: "string", bool: "boolean"}


def tool(fn: Callable) -> Callable:
    """함수 시그니처 → Ollama/OpenAI 호환 함수 스키마."""
    sig = inspect.signature(fn)
    props, required = {}, []
    for name, p in sig.parameters.items():
        props[name] = {"type": _PY.get(p.annotation, "string")}
        if p.default is inspect.Parameter.empty:
            required.append(name)
    fn.schema = {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": (fn.__doc__ or "").strip().split("\n")[0],
            "parameters": {"type": "object", "properties": props, "required": required},
        },
    }
    return fn


# ── 예시 도구 / sample tools ──
@tool
def add(a: int, b: int) -> int:
    """두 정수를 더한다."""
    return a + b


@tool
def power(base: int, exp: int) -> int:
    """base 의 exp 제곱."""
    return base ** exp


@tool
def now() -> str:
    """현재 시각(로컬)."""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


TOOLS = [add, power, now]
REGISTRY = {t.__name__: t for t in TOOLS}
SCHEMAS = [t.schema for t in TOOLS]
