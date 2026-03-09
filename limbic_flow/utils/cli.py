"""
CLI 界面 - 彩色终端 UI
"""

import os
import sys
from typing import Optional


class Colors:
    """终端颜色"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # 前景色
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 背景色
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class CLI:
    """CLI 工具类"""
    
    @staticmethod
    def clear():
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(text: str, color: str = Colors.CYAN):
        """打印标题"""
        print(f"\n{color}{Colors.BOLD}{'=' * 50}{Colors.RESET}")
        print(f"{color}{Colors.BOLD}  {text}{Colors.RESET}")
        print(f"{color}{Colors.BOLD}{'=' * 50}{Colors.RESET}\n")
    
    @staticmethod
    def print_success(text: str):
        """打印成功"""
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")
    
    @staticmethod
    def print_error(text: str):
        """打印错误"""
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")
    
    @staticmethod
    def print_warning(text: str):
        """打印警告"""
        print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")
    
    @staticmethod
    def print_info(text: str):
        """打印信息"""
        print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")
    
    @staticmethod
    def print_menu(options: list, title: str = "请选择:"):
        """打印菜单"""
        print(f"\n{Colors.BOLD}{title}{Colors.RESET}")
        for i, option in enumerate(options, 1):
            print(f"  {Colors.CYAN}{i}.{Colors.RESET} {option}")
        print()
    
    @staticmethod
    def input(prompt: str = "") -> str:
        """带颜色的输入"""
        return input(f"{Colors.CYAN}{prompt}{Colors.RESET}")
    
    @staticmethod
    def spinner(text: str = "处理中"):
        """简单的加载动画"""
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        for char in chars:
            sys.stdout.write(f"\r{char} {text}")
            sys.stdout.flush()
            import time
            time.sleep(0.1)
        sys.stdout.write(f"\r{Colors.GREEN}✓{Colors.RESET} {text}\n")


def print_banner():
    """打印启动 banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
   _      _              _      
  | |    (_)            | |     
  | |     _ _ __   __ _| | ___ 
  | |    | | '_ \\ / _` | |/ _ \\
  | |____| | | | | (_| | |  __/
  |______|_|_| |_|\\__,_|_|\\___|
  
  {Colors.RESET}{Colors.DIM}V0.5.0 - 有情绪的 AI 助手{Colors.RESET}
    """
    print(banner)


def main_cli():
    """CLI 主函数"""
    CLI.clear()
    print_banner()
    
    CLI.print_info("初始化中...")
    
    # 加载配置
    try:
        from config import get_config
        config = get_config()
        CLI.print_success("配置加载完成")
    except Exception as e:
        CLI.print_warning(f"配置加载失败: {e}")
    
    # 显示菜单
    while True:
        CLI.print_menu([
            "启动 API 服务",
            "启动 Web 界面",
            "测试对话",
            "查看状态",
            "退出"
        ])
        
        choice = CLI.input("请选择: ")
        
        if choice == "1":
            CLI.print_info("启动 API 服务...")
            # 启动服务
        elif choice == "2":
            CLI.print_info("启动 Web 界面...")
        elif choice == "3":
            CLI.print_info("测试对话模式...")
        elif choice == "4":
            CLI.print_info("查看状态...")
        elif choice == "5":
            CLI.print_success("再见!")
            break
        else:
            CLI.print_error("无效选择")


if __name__ == "__main__":
    main_cli()
