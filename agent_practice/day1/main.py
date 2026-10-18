#主程序，负责验证、调度、执行和处理异常
import json
import logging
from pathlib import Path

from pydantic import ValidationError

import tools
from schemas import ToolCall, AddInput, RepeatInput


# =========================
# 1. 路径配置
# =========================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "tool_call.json"
OUTPUT_FILE = BASE_DIR / "result.json"
LOG_FILE = BASE_DIR / "agent.log"


# =========================
# 2. 日志配置
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# =========================
# 3. 参数模型注册表
# =========================

ARGUMENT_MODELS = {
    "add": AddInput,
    "repeat_text": RepeatInput
}


# =========================
# 4. 工具执行器
# =========================

def execute_tool(data: dict) -> dict:

    # 第一层：通用结构验证
    try:
        tool_call = ToolCall.model_validate(data)

    except ValidationError as e:
        logger.warning("工具调用结构错误: %s", e)

        return {
            "success": False,
            "error": "工具调用结构不合法"
        }

    name = tool_call.name
    arguments = tool_call.arguments

    # 第二层：查找工具
    tool = tools.get(name)

    if tool is None:
        logger.warning("工具不存在: %s", name)

        return {
            "success": False,
            "error": f"工具 {name} 不存在"
        }

    # 第三层：查找参数模型
    model = ARGUMENT_MODELS.get(name)

    if model is None:
        logger.error("工具缺少参数模型: %s", name)

        return {
            "success": False,
            "error": f"工具 {name} 未配置参数模型"
        }

    # 第四层：验证工具参数
    try:
        validated = model.model_validate(arguments)

    except ValidationError as e:
        logger.warning("参数校验失败 [%s]: %s", name, e)

        return {
            "success": False,
            "error": f"工具 {name} 参数校验失败"
        }

    # 第五层：执行工具
    try:
        logger.info("开始执行工具: %s", name)

        params = validated.model_dump()

        result = tool(**params)

        logger.info("工具执行成功: %s", name)

        return {
            "success": True,
            "result": result
        }

    except Exception:
        logger.exception("工具执行失败: %s", name)

        return {
            "success": False,
            "error": f"工具 {name} 执行失败"
        }


# =========================
# 5. 主程序
# =========================

def main():

    # 读取 JSON 文件
    try:
        with INPUT_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        result = execute_tool(data)

    except (OSError, json.JSONDecodeError) as e:
        logger.error("读取输入文件失败: %s", e)

        result = {
            "success": False,
            "error": f"输入文件读取失败: {e}"
        }

    # 写入执行结果
    try:
        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            json.dump(
                result,
                f,
                ensure_ascii=False,
                indent=2
            )

    except (OSError, TypeError, ValueError):
        logger.exception("无法写入结果文件")
        raise


if __name__ == "__main__":
    main()