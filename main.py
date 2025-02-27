# main.py
import asyncio
import aiohttp
from internal.format_output import clear_terminal, print_error, print_info
from internal.api.OneBot11 import get_login_info
from internal.chat_thesaurus import while_msg
from internal.config import config
from internal.ai.chat_ai import start_chat_ai_process, stop_chat_ai_process  # 引入 chat_ai 进程管理函数

# 运行机器人
async def run_bot(chat_ai_instance):
    async with aiohttp.ClientSession() as session:
        try:
            ws = await session.ws_connect(
                f"ws://{config['host']}:{config['port']}/",
                headers={"Authorization": f"Bearer {config['access_token']}"}
            )
        except Exception:
            # 清空终端窗口输出
            clear_terminal()
            if config['debug']:
                import traceback
                traceback.print_exc()
            print_error("Creating websocket connection.")
            return
        print_info("WebSocket connection established successfully.")
        await get_login_info(ws)
        await while_msg(ws, chat_ai_instance)  # 传递 ChatAIProcess 实例


if __name__ == '__main__':
    # 启动 chat_ai 进程并获取 ChatAIProcess 实例
    chat_ai_instance = start_chat_ai_process()

    try:
        if config['auto_reconnect']:
            while True:
                asyncio.run(run_bot(chat_ai_instance))
        else:
            asyncio.run(run_bot(chat_ai_instance))
    except KeyboardInterrupt:
        print_info("程序正在退出...")
    finally:
        # 停止 chat_ai 进程
        stop_chat_ai_process()
        print_info("chat_ai 进程已关闭。")