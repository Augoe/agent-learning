# 任务 D：用 httpx.MockTransport 模拟 API 响应，测试 fetch_json
import httpx
import pytest

from agent_practice.day4.api_client import fetch_json


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    """把测试里的 asyncio.sleep 换成"立刻返回"，避免测试时真的等待。

    autouse=True 表示每个测试自动生效，不用手动传入。
    """
    async def fake_sleep(seconds):
        return None

    monkeypatch.setattr("agent_practice.day4.api_client.asyncio.sleep", fake_sleep)


def make_client(handler):
    """创建一个"假"的异步客户端：所有请求都被 MockTransport 拦截，
    返回 handler 函数里写好的假响应，不产生真实网络请求。
    """
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


# 测试1：200 + 合法 JSON → 成功
@pytest.mark.asyncio
async def test_success():
    def handler(request):
        return httpx.Response(200, json={"city": "Beijing", "temperature": 25})

    async with make_client(handler) as client:
        result = await fetch_json(client, "http://test/get")

    assert result["success"] is True
    assert result["data"] == {"city": "Beijing", "temperature": 25}
    assert result["error"] is None


# 测试2：404 → 失败，且不重试
@pytest.mark.asyncio
async def test_404():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        return httpx.Response(404, text="Not Found")

    async with make_client(handler) as client:
        result = await fetch_json(client, "http://test/missing")

    assert result["success"] is False
    assert result["data"] is None
    assert "404" in result["error"]
    assert call_count == 1  # 404 不重试，只请求 1 次


# 测试3：请求超时 → 正确捕获异常
@pytest.mark.asyncio
async def test_timeout():
    def handler(request):
        raise httpx.ReadTimeout("模拟超时")

    async with make_client(handler) as client:
        result = await fetch_json(client, "http://test/timeout")

    assert result["success"] is False
    assert "超时" in result["error"]


# 测试4：第一次 429，第二次成功 → 自动重试后成功
@pytest.mark.asyncio
async def test_retry():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # 第一次限流，告诉客户端等待 0 秒（测试里不用真等）
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"ok": True})

    async with make_client(handler) as client:
        result = await fetch_json(client, "http://test/retry")

    assert result["success"] is True
    assert result["data"] == {"ok": True}
    assert call_count == 2  # 确认确实请求了 2 次


# 测试5：一直 429 → 达到重试上限（1 次正常 + 2 次重试 = 3 次）后失败
@pytest.mark.asyncio
async def test_retry_limit():
    call_count = 0

    def handler(request):
        nonlocal call_count
        call_count += 1
        return httpx.Response(429, headers={"Retry-After": "0"})

    async with make_client(handler) as client:
        result = await fetch_json(client, "http://test/always-429", max_retries=2)

    assert result["success"] is False
    assert "429" in result["error"]
    assert call_count == 3
