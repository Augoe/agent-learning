from agent_practice.day1.tools import TOOL_REGISTRY



def run_tool(name, arguments):
    # 1. 查找工具
    func = TOOL_REGISTRY.get(name)

    if func is None:
        return {
            "success": False,
            "error": f"Tool {name} not found"
        }

    # 2. 执行工具
    try:
        result = func(**arguments)

        return {
            "success": True,
            "result": result
        }

    # 3. 处理参数错误
    except TypeError as e:
        return {
            "success": False,
            "error": f"Invalid arguments: {e}"
        }

    # 4. 处理其他异常
    except Exception as e:
        return {
            "success": False,
            "error": f"Tool execution failed: {e}"
        }