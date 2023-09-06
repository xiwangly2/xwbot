import asyncio

import aiohttp

# 导入自己写的模块
from internal.config import load_config
from internal.functions import *

# 全局变量
global_config = None
global_ws = None
global_db = None


# 运行机器人
async def run_bot(global_config):
    async with aiohttp.ClientSession() as session:
        try:
            ws = await session.ws_connect(f"ws://{global_config['host']}:{global_config['port']}/",
                                          headers={"Authorization": f"Bearer {global_config['access_token']}"})
        except:
            # 清空终端窗口输出
            await clear_terminal()
            if global_config['debug']:
                import traceback
                traceback.print_exc()
            await print_error("Error: Creating websocket connection.")
            return
        await print_green("Notice: WebSocket connection established successfully.")
        await receive_messages(ws, global_config['access_token'])
        await while_msg(ws, global_config)


if __name__ == '__main__':
    # 判断变量是否存在，如果不存在就初始化
    if 'global_config' not in locals():
        global_config = asyncio.run(load_config())
    # 创建数据库实例并传递配置
    xwbot_database = Database(global_config).__init__(global_config)
    asyncio.run(run_bot(global_config))
