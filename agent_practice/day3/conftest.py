import pytest
from unittest.mock import Mock

@pytest.fixture
def valid_tool_calls():
    return {
        "name": "add",
        "arguments": {"a": 1, "b": 2},
        "expected": 3
    }

@pytest.fixture
def mock_tool():
    return Mock(return_value="模拟成功")
