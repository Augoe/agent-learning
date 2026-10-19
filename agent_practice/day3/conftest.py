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

@pytest.fixture
def mock_tool_with_assertion():
    tool = Mock(return_value="模拟成功")
    tool.assert_called_once_with = Mock()
    return tool