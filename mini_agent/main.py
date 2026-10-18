import json
from tools import tools
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / "tool_call.json"
output_file = BASE_DIR / "result.json"

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
name = data['name']
arguments = data['arguments']

tool = tools.get(name)
if tool is None:
    result_message ={
        "success": False,
        "error": f"工具 {name} 不存在"
    }
else:
     try:
        result = tool(**arguments)
        result_message = {
            "success": True,
            "result": result
        }
     except TypeError as e:
        result_message = {
            "success": False,
            "error": f"参数错误，错误信息：{e}"
        }
     except Exception as e:
        result_message = {
            "success": False,
            "error": f"工具执行失败！错误信息：{e}"
        }

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result_message, 
              f, 
              ensure_ascii=False,
              indent=2
            )
print("工具调用完成，结果已写入 result.json 文件。")