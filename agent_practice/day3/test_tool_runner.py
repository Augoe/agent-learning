from tool_runner import run_tool
import tool_runner

# 测试1：正常执行
def test_add_success(valid_tool_calls):
    data = valid_tool_calls

    result = run_tool(
        data["name"],
        data["arguments"]
    )

    assert result["success"] is True
    assert result["result"] == data["expected"]


# 测试2：负数相加
def test_add_negative():
    result = run_tool(
        "add",
        {"a": -5, "b": 3}
    )

    assert result["success"] is True
    assert result["result"] == -2


# 测试3：工具不存在
def test_unknown_tool():
    result = run_tool(
        "unknown",
        {"a": 1, "b": 2}
    )

    assert result["success"] is False
    assert "not found" in result["error"]


# 测试4：参数缺失
def test_invalid_arguments():
    result = run_tool(
        "add",
        {"a": 1}
    )

    assert result["success"] is False
    assert "Invalid arguments" in result["error"]


# 测试5：工具执行异常
def test_divide_by_zero():
    result = run_tool(
        "divide",
        {"a": 1, "b": 0}
    )

    assert result["success"] is False
    assert "division by zero" in result["error"]


# 测试6：Mock 模拟工具调用
def test_mock_tool(monkeypatch, mock_tool):

    # 将模拟工具注册到工具注册表
    monkeypatch.setitem(
        tool_runner.TOOL_REGISTRY,
        "mock_api",
        mock_tool
    )

    # 执行工具
    result = tool_runner.run_tool(
        "mock_api",
        {"a": 1, "b": 2}
    )

    # 验证返回结果
    assert result["success"] is True
    assert result["result"] == "模拟成功"

    # 验证 Mock 被调用
    mock_tool.assert_called_once_with(a=1, b=2)


# 测试7：Mock 模拟网络异常
def test_mock_exception(monkeypatch, mock_tool):

    # 设置模拟函数抛出异常
    mock_tool.side_effect = ConnectionError("网络断开")

    # 注册模拟工具
    monkeypatch.setitem(
        tool_runner.TOOL_REGISTRY,
        "mock_api",
        mock_tool
    )

    # 执行工具
    result = tool_runner.run_tool(
        "mock_api",
        {"city": "北京"}
    )

    # 验证异常被正确处理
    assert result["success"] is False
    assert "网络断开" in result["error"]

    # 验证调用参数
    mock_tool.assert_called_once_with(city="北京")