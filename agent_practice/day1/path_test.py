from pathlib import Path

# 当前工作目录
print("工作目录：", Path.cwd())

# 当前 Python 文件的绝对路径
print("文件路径：", Path(__file__).resolve())

# 当前 Python 文件所在目录
BASE_DIR = Path(__file__).resolve().parent
print("脚本目录：", BASE_DIR)

# 拼接文件路径
file_path = BASE_DIR / "tool_call.json"
print("目标文件：", file_path)

# 判断文件是否存在
print("文件存在吗：", file_path.exists())