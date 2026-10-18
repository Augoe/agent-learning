# 工具函数及注册表

def add(a,b) :
    return a + b

def multiply(a, b):
    return a * b

def greet(name):
    return f"你好，{name}！"

def subtract(a, b):
    return a - b
    


TOOL_REGISTRY = {
    "add": add,
    "multiply": multiply,
    "greet": greet,
    "subtract": subtract
}