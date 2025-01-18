import asyncio

import aiohttp

# 导入自己写的模块
from internal.functions import print_green, print_error, clear_terminal, receive_messages
from internal.chat_thesaurus import while_msg
from internal.config import config


# 运行机器人
async def run_bot():
    async with aiohttp.ClientSession() as session:
        try:
            ws = await session.ws_connect(f"ws://{config['host']}:{config['port']}/",
                                          headers={"Authorization": f"Bearer {config['access_token']}"})
        except Exception:
            # 清空终端窗口输出
            clear_terminal()
            if config['debug']:
                import traceback
                traceback.print_exc()
            print_error("Error: Creating websocket connection.")
            return
        print_green("Notice: WebSocket connection established successfully.")
        await receive_messages(ws)
        await while_msg(ws)


if __name__ == '__main__':
    if config['auto_reconnect']:
        while True:
            asyncio.run(run_bot())
    else:
        asyncio.run(run_bot())
