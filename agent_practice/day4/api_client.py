# 任务 A/B：HTTP 请求、异常处理、自动重试
import asyncio

import httpx

# 不可重试的状态码：认证失败、权限不足、资源不存在（重试多少次都一样）
NO_RETRY_STATUS = {401, 403, 404}

# 服务端临时故障的状态码，可以重试
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

# 读取 Retry-After 时，最多等待这么多秒，避免让程序睡太久
MAX_WAIT_SECONDS = 10


def _wait_seconds(response, attempt):
    """计算重试前等待几秒。

    优先看服务器给的 Retry-After 响应头（并限制上限）；
    没有就用指数退避：第 1 次失败等 1 秒，第 2 次等 2 秒，第 3 次等 4 秒……
    """
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        try:
            return min(float(retry_after), MAX_WAIT_SECONDS)
        except ValueError:
            pass
    # attempt 从 0 开始：2**0 = 1，2**1 = 2
    return min(2 ** attempt, MAX_WAIT_SECONDS)


async def fetch_json(client, url, params=None, max_retries=2):
    """发送 GET 请求，返回统一格式的结果。

    成功：{"success": True,  "data": ..., "error": None}
    失败：{"success": False, "data": None, "error": "错误信息"}

    max_retries=2 表示：第一次正常请求 + 最多 2 次重试 = 最多 3 次请求。
    """
    last_error = None

    # 重试循环的"总开关"：一共尝试 1 + max_retries 次
    for attempt in range(max_retries + 1):
        try:
            # 1. 发请求
            response = await client.get(url, params=params)

            # 2. 429 限流：可重试。必须在 raise_for_status() 之前判断，
            #    否则 429 会被直接变成异常，就没机会重试了
            if response.status_code == 429:
                if attempt < max_retries:
                    wait = _wait_seconds(response, attempt)
                    print(f"[429] 限流，等待 {wait:.0f} 秒后重试（第 {attempt + 1} 次重试）")
                    await asyncio.sleep(wait)
                    continue  # 回到循环开头，重新发一次请求
                last_error = "HTTP 429: 请求过于频繁，已达到重试上限"
                break

            # 3. 401/403/404：不可重试，立即失败
            if response.status_code in NO_RETRY_STATUS:
                last_error = f"HTTP {response.status_code}"
                break

            # 4. 其他 4xx/5xx 状态码：交给 raise_for_status 抛出异常
            response.raise_for_status()

            # 5. 成功：解析 JSON。解析失败会抛 ValueError（JSONDecodeError 是它的子类）
            data = response.json()
            return {
                "success": True,
                "data": data,
                "error": None
            }

        except httpx.TimeoutException as e:
            # 超时：GET 请求可以重试
            last_error = f"请求超时: {e}"
            if attempt < max_retries:
                wait = float(2 ** attempt)
                print(f"[超时] 等待 {wait:.0f} 秒后重试（第 {attempt + 1} 次重试）")
                await asyncio.sleep(wait)
                continue
            break

        except httpx.ConnectError as e:
            # 网络连接失败：也可以重试
            last_error = f"网络连接失败: {e}"
            if attempt < max_retries:
                wait = float(2 ** attempt)
                print(f"[连接失败] 等待 {wait:.0f} 秒后重试（第 {attempt + 1} 次重试）")
                await asyncio.sleep(wait)
                continue
            break

        except httpx.HTTPStatusError as e:
            # 其他状态码错误（比如 500/503）
            status = e.response.status_code
            last_error = f"HTTP {status}"
            if status in RETRYABLE_STATUS and attempt < max_retries:
                wait = _wait_seconds(e.response, attempt)
                print(f"[{status}] 等待 {wait:.0f} 秒后重试（第 {attempt + 1} 次重试）")
                await asyncio.sleep(wait)
                continue
            break

        except ValueError as e:
            # JSON 解析失败：服务器给的不是 JSON，重试没有意义，直接失败
            last_error = f"JSON 解析失败: {e}"
            break

        except httpx.HTTPError as e:
            # 其他 httpx 异常兜底，保证程序不崩溃
            last_error = f"HTTP 请求失败: {e}"
            break

    # 能走到这里说明所有尝试都失败了
    return {
        "success": False,
        "data": None,
        "error": last_error
    }
