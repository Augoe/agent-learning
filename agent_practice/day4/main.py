# 任务 C：创建一个 AsyncClient，用 asyncio.gather 并发调用三个 API
import asyncio
import time

import httpx

# 兼容两种运行方式：
#   从项目根目录运行：python -m agent_practice.day4.main
#   从 day4 目录运行：python main.py
try:
    from agent_practice.day4.api_client import fetch_json
except ImportError:
    from api_client import fetch_json


async def main():
    # (名称, 网址) 三个测试 API：
    #   /get        正常返回 JSON
    #   /delay/2    延迟 2 秒后返回（用来验证并发）
    #   /status/404 返回 404（用来验证异常处理）
    api_list = [
        ("正常接口", "https://httpbin.org/get"),
        ("延迟接口", "https://httpbin.org/delay/2"),
        ("404接口", "https://httpbin.org/status/404"),
    ]

    start = time.perf_counter()

    # 一个客户端复用给三个请求；timeout=10 表示每个请求最多等 10 秒
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 先把三个协程都创建出来（此时还没执行）
        tasks = [fetch_json(client, url) for _, url in api_list]
        # gather 让三个请求同时跑；return_exceptions=True 保证
        # 某个请求失败时，其他请求的结果仍然能收集到
        results = await asyncio.gather(*tasks, return_exceptions=True)

    elapsed = time.perf_counter() - start

    for (name, url), result in zip(api_list, results):
        print(f"\n===== {name} =====")
        print(f"URL: {url}")
        print(f"结果: {result}")

    print(f"\n总耗时: {elapsed:.2f} 秒")
    print("（如果并发生效，总耗时接近 2 秒，而不是 2+2 秒以上）")


if __name__ == "__main__":
    asyncio.run(main())
