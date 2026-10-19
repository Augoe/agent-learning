import pytest
from tool_runner import run_tool


def test_add():
    result = run_tool("add", [1, 2])
    assert result["success"] == "True"
    assert result["result"] == 3

def test_unknown():
    result = run_tool("unknown", [1, 2])
    assert result["success"] == "False"

def test_add():
    result = run_tool("add", [1])
    assert result["success"] == "False"    

def test_divide():
    result = run_tool("divide", [1, 0])
    assert result["success"] == "False"

def test_add():
    result = run_tool("add", [-5,3])
    assert result["result"] == -2