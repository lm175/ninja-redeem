import asyncio, requests

from .entity import RedeemCode


async def process_chunk(dhm: str, chunk: list[str]):
    redeem = RedeemCode(dhm)
    
    try:
        for uid in chunk:
            # 使用 to_thread 将阻塞调用转为异步
            tip_msg = await asyncio.to_thread(redeem.redeem_for_user, uid)
            print(tip_msg)
    finally:
        redeem.close()


async def redeem_for_users(dhm: str, uids: list[str], coroutine_nums: int):
    """
    批量兑换函数

    参数:
    - dhm: 兑换码
    - uids: 执行兑换的uid的字符串列表
    - coroutine_nums: 创建的异步协程数量
    """
    num_coroutines = min(coroutine_nums, len(uids))
    chunk_size = (len(uids) + num_coroutines - 1) // num_coroutines
    chunks = [uids[i:i + chunk_size] for i in range(0, len(uids), chunk_size)]

    tasks = [asyncio.create_task(process_chunk(dhm, chunk)) for chunk in chunks]
    await asyncio.gather(*tasks)



def serch_uid(uid: int) -> str | None:
    res = requests.get(f"https://statistics.pandadastudio.com/player/simpleInfo?uid={uid}")
    data: dict = res.json().get('data')
    if not data:
        return None
    
    return f"uid: {data.get('uid')}\n{data.get('name')} - {data.get('serverId') + 1}服 - {data.get('title')}"