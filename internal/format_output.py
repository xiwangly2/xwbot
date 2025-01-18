from colorama import Fore, Style


# 输出彩色消息
def print_colored(message, color: str):
    print(color + str(message) + Style.RESET_ALL)


# 输出红色错误消息的函数
def print_error(message):
    print_colored("ERROR: " + message, Fore.RED)


# 输出白色信息消息的函数
def print_info(message):
    print_colored("INFO: " + message, Fore.WHITE)


# 输出黄色警告消息的函数
def print_warning(message):
    print_colored("WARNING: " + message, Fore.YELLOW)


# 输出绿色消息的函数
def print_green(message):
    print_colored(message, Fore.GREEN)


# 输出紫色消息的函数
def print_purple(message):
    print_colored(message, Fore.MAGENTA)


# 输出蓝色消息的函数
def print_blue(message):
    print_colored(message, Fore.BLUE)


# 输出白色消息的函数
def print_white(message):
    print_colored(message, Fore.WHITE)


# 输出黑色消息的函数
def print_black(message):
    print_colored(message, Fore.BLACK)


# 输出粉色消息的函数
def print_pink(message):
    print_colored(message, Fore.LIGHTMAGENTA_EX)


# 输出青色消息的函数
def print_cyan(message):
    print_colored(message, Fore.CYAN)


# 输出亮绿色消息的函数
def print_light_green(message):
    print_colored(message, Fore.LIGHTGREEN_EX)


# 输出金色消息的函数
def print_gold(message):
    print_colored(message, Fore.LIGHTYELLOW_EX)


# 清空终端窗口输出的函数
def clear_terminal():
    import os
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        pass
