import asyncio

import aiohttp

# 导入自己写的模块
from internal.config import load_config
from internal.functions import *


# 运行机器人
async def run_bot(xwbot_config):
    async with aiohttp.ClientSession() as session:
        try:
            ws = await session.ws_connect(f"ws://{xwbot_config['host']}:{xwbot_config['port']}/",
                                          headers={"Authorization": f"Bearer {xwbot_config['access_token']}"})
        except:
            # 清空终端窗口输出
            await clear_terminal()
            if xwbot_config['debug']:
                import traceback
                traceback.print_exc()
            await print_error("Error: Creating websocket connection.")
            return
        await print_green("Notice: WebSocket connection established successfully.")
        await receive_messages(ws, xwbot_config['access_token'])
        await while_msg(ws, xwbot_config)


if __name__ == '__main__':
    xwbot_config = asyncio.run(load_config())
    asyncio.run(run_bot(xwbot_config))
