#!/usr/bin/env python3
"""
GUI启动脚本
自动检测并使用合适的Python环境启动GUI应用
"""

import sys
import os
import subprocess
from pathlib import Path

def check_tkinter(python_cmd):
    """
    检查指定Python命令是否支持tkinter
    
    Args:
        python_cmd (str): Python命令
        
    Returns:
        bool: 是否支持tkinter
    """
    try:
        result = subprocess.run(
            [python_cmd, '-c', 'import tkinter; print("OK")'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0 and 'OK' in result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def find_python_with_tkinter():
    """
    查找支持tkinter的Python解释器
    
    Returns:
        str: Python命令，如果找不到则返回None
    """
    # 获取当前脚本目录
    script_dir = Path(__file__).parent.absolute()
    venv_python = script_dir / 'venv' / 'bin' / 'python3'
    
    # 优先使用虚拟环境的Python，然后是常见的Python命令
    python_commands = []
    
    # 如果存在虚拟环境，优先使用
    if venv_python.exists():
        python_commands.append(str(venv_python))
        print(f"发现虚拟环境: {venv_python}")
    
    # 添加其他Python命令
    python_commands.extend([
        '/usr/bin/python3',  # macOS系统自带
        '/System/Library/Frameworks/Python.framework/Versions/3.9/bin/python3',  # macOS系统Python
        'python3',
        'python',
        '/opt/homebrew/bin/python3',  # Homebrew Python
        '/usr/local/bin/python3',     # 其他安装的Python
    ])
    
    print("正在查找支持tkinter的Python解释器...")
    
    for cmd in python_commands:
        print(f"测试: {cmd}")
        if check_tkinter(cmd):
            print(f"✓ 找到支持tkinter的Python: {cmd}")
            return cmd
        else:
            print(f"✗ {cmd} 不支持tkinter或不可用")
    
    return None

def install_tkinter_instructions():
    """
    显示安装tkinter的说明
    """
    print("\n=== tkinter安装说明 ===")
    print("在macOS上，tkinter通常随系统Python一起提供。")
    print("如果您使用的是自定义Python环境，请尝试以下方法：")
    print("")
    print("1. 使用系统自带的Python:")
    print("   /usr/bin/python3 gui_app.py")
    print("")
    print("2. 如果使用Homebrew安装的Python:")
    print("   brew install python-tk")
    print("")
    print("3. 如果使用pyenv:")
    print("   env PYTHON_CONFIGURE_OPTS='--with-tcltk-includes=-I/usr/local/opt/tcl-tk/include' \\")
    print("       PYTHON_CONFIGURE_OPTS='--with-tcltk-libs=-L/usr/local/opt/tcl-tk/lib' \\")
    print("       pyenv install 3.x.x")
    print("")
    print("4. 或者使用命令行版本:")
    print("   python3 main.py input.mp4 --output output.mp4 --preview")

def setup_environment(python_cmd):
    """
    设置Python环境，确保依赖可用
    
    Args:
        python_cmd (str): Python命令
        
    Returns:
        bool: 设置是否成功
    """
    print(f"\n使用Python: {python_cmd}")
    
    # 检查当前目录是否有虚拟环境
    venv_path = Path('venv')
    if venv_path.exists():
        print("检测到虚拟环境，但GUI需要系统Python的tkinter支持")
        print("将使用系统Python运行GUI，但可能缺少项目依赖")
        
        # 检查必要的依赖
        try:
            result = subprocess.run(
                [python_cmd, '-c', 'import cv2, numpy; print("Dependencies OK")'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                print("\n警告: 系统Python缺少必要依赖 (opencv-python, numpy)")
                print("请安装依赖: pip3 install opencv-python numpy")
                return False
        except subprocess.TimeoutExpired:
            print("依赖检查超时")
            return False
    
    return True

def launch_gui(python_cmd):
    """
    启动GUI应用
    
    Args:
        python_cmd (str): Python命令
    """
    gui_script = Path('gui_app.py')
    if not gui_script.exists():
        print(f"错误: GUI脚本 {gui_script} 不存在")
        return False
    
    print(f"\n启动GUI应用...")
    try:
        # 启动GUI应用
        subprocess.run([python_cmd, str(gui_script)])
        return True
    except KeyboardInterrupt:
        print("\n用户中断")
        return True
    except Exception as e:
        print(f"启动GUI失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("视频人脸检测 GUI 启动器")
    print("=" * 40)
    
    # 检查当前目录
    if not Path('face_detector.py').exists():
        print("错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 查找支持tkinter的Python
    python_cmd = find_python_with_tkinter()
    
    if not python_cmd:
        print("\n❌ 未找到支持tkinter的Python解释器")
        install_tkinter_instructions()
        sys.exit(1)
    
    # 设置环境
    if not setup_environment(python_cmd):
        print("\n❌ 环境设置失败")
        print("\n建议使用命令行版本:")
        print("python3 main.py input.mp4 --output output.mp4 --preview")
        sys.exit(1)
    
    # 启动GUI
    success = launch_gui(python_cmd)
    
    if success:
        print("\n✓ GUI应用已退出")
    else:
        print("\n❌ GUI启动失败")
        print("\n建议使用命令行版本:")
        print("python3 main.py input.mp4 --output output.mp4 --preview")

if __name__ == "__main__":
    main()