from dispatcher import dispatch

def test_add():
    result = dispatch({
        "name": "add",
        "arguments": {"a": 10, "b": 20}
    })

    assert result["success"] is True
    assert result["result"] == 30
