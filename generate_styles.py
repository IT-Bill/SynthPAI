import asyncio
import json
import os
import time
from typing import List

import aiofiles
import aiohttp
from tqdm.asyncio import tqdm  # 异步进度条
from openai import AsyncOpenAI

# 系统提示语
SYSTEM_PROMPT = """
你是一个善于从用户的回答中识别用户风格的机器人。\
下面我会给你一个知乎用户的问答，你需要根据用户的问答，判断出用户的风格。\
你的回复使用第二人称“你”，以“写作风格：”开头。
"""

# 输出文件路径
OUTPUT_FILE = "data/profiles/zhihu_comments_with_styles.json"

# 并发限制（根据实际情况调整）
CONCURRENT_REQUESTS = 5

# 最大重试次数
MAX_RETRIES = 5

# 等待时间因子（用于指数回退）
BACKOFF_FACTOR = 2


async def recognize_style(
    client: AsyncOpenAI, user: dict, semaphore: asyncio.Semaphore
) -> dict:
    """
    根据用户的问答内容识别其风格，并将结果添加到用户字典中。

    :param client: AsyncOpenAI 客户端实例
    :param user: 包含用户信息和问答的字典
    :param semaphore: 控制并发的信号量
    :return: 更新后的用户字典，包含识别出的风格
    """
    user_content = json.dumps(user, ensure_ascii=False)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            async with semaphore:
                completion = await client.chat.completions.create(
                    model="gpt-4o-mini-2024-07-18",
                    messages=messages,
                    temperature=1.0,
                    max_tokens=300,
                )
            style = completion.choices[0].message.content.strip()
            user["style"] = style
            return user
        except Exception as e:
            if hasattr(e, 'code') and e.code == 'rate_limit_exceeded':
                # 从错误消息中提取等待时间
                wait_time = 1  # 默认等待1秒
                if 'Please try again in' in str(e):
                    try:
                        wait_str = str(e).split('Please try again in ')[1]
                        wait_ms = int(wait_str.split('ms')[0])
                        wait_time = wait_ms / 1000
                    except (IndexError, ValueError):
                        pass
                print(
                    f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying..."
                )
                await asyncio.sleep(wait_time)
                attempt += 1
            else:
                print(f"Error processing user {user.get('name', 'Unknown')}: {str(e)}")
                user["style"] = "Error: " + str(e)
                return user
    # 如果重试次数用完，记录错误
    print(f"Failed to process user {user.get('name', 'Unknown')} after {MAX_RETRIES} attempts.")
    user["style"] = "Error: Rate limit exceeded after multiple retries."
    return user


async def load_users(file_path: str) -> List[dict]:
    """
    异步读取 JSON 文件并加载用户数据。

    :param file_path: JSON 文件路径
    :return: 用户数据列表
    """
    try:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            content = await f.read()
            users = json.loads(content)
            return users
    except Exception as e:
        print(f"Error loading users from {file_path}: {str(e)}")
        return []


async def save_results(file_path: str, data: List[dict]):
    """
    异步保存结果到 JSON 文件。

    :param file_path: 输出文件路径
    :param data: 需要保存的数据列表
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=4))
        print(f"Results saved to {file_path}")
    except Exception as e:
        print(f"Error saving results to {file_path}: {str(e)}")


async def main():
    # 初始化 AsyncOpenAI 客户端
    client = AsyncOpenAI()

    # 异步加载用户数据
    users = await load_users("data/profiles/zhihu_comments.json")

    if not users:
        print("No users to process.")
        return

    # 初始化信号量以限制并发请求数量
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    # 创建任务列表
    tasks = [
        recognize_style(client, user, semaphore) for user in users
    ]

    # 使用tqdm添加进度条
    results = []
    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Processing users"):
        user_result = await f
        results.append(user_result)

    # 保存结果到文件
    await save_results(OUTPUT_FILE, results)


if __name__ == "__main__":
    asyncio.run(main())
