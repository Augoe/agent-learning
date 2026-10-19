import pathlib
from agent_practice.day1 import tools
tool_path =pathlib.Path(__file__).parent / 'day1/tools.py'
tool={
     "add": tools.add,
     "divide": tools.divide
}


def run_tool(name, arguments):
    try:
        func=tool[name]
        data={
            "success": "True",
            "result": func(*arguments)
        }
        return data
    except KeyError:
        print(f"Tool {name} not found")
        return {
            "success": "False",
            "result": None
        }
    except TypeError:
        print(f"Tool {name} received incorrect arguments")
        return {
            "success": "False",
            "result": None
        }
    except Exception as e:
        print(f"An error occurred while running tool {name}: {e}")
        return {
            "success": "False",
            "result": None
        }