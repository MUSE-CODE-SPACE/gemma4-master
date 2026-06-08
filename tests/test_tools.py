import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gemma.tools import SCHEMAS, add, power

def test_schema():
    assert add.schema["function"]["name"] == "add"
    assert "a" in add.schema["function"]["parameters"]["required"]

def test_run():
    assert add(2, 3) == 5 and power(3, 4) == 81

def test_all_schemas():
    assert len(SCHEMAS) == 3 and all("function" in s for s in SCHEMAS)
