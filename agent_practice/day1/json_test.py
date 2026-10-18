import json
from pathlib import Path
import tools

BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / "tool_call.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

name = data["name"]
arguments = data["arguments"]

if name in tools.TOOL_REGISTRY:
    value = tools.TOOL_REGISTRY[name](**arguments)
    result = {"success": True, "value": value}
else:
    result = {"success": False, "error": "Tool not found"}

output_file = BASE_DIR / "result.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
