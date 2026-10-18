from tools import add, multiply, greet

TOOL_REGISTRY = {
    "add": add,
    "multiply": multiply,
    "greet": greet,
}

def dispatch(payload): 
    try:
        name = payload["name"]
        arguments = payload["arguments"]

        tool = TOOL_REGISTRY[name]
        result = tool(**arguments)

        return {"success": True, "result": result}

    except KeyError as e:
        return {"success": False, "error": f"KeyError: {e}"}

    except TypeError as e:
        return {"success": False, "error": f"TypeError: {e}"}