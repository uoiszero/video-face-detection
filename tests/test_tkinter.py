#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tkinter GUI测试脚本
用于诊断GUI显示问题
"""

import tkinter as tk
from tkinter import ttk
import sys

def test_basic_window():
    """
    测试基础tkinter窗口
    """
    print("创建基础tkinter窗口...")
    
    root = tk.Tk()
    root.title("tkinter测试窗口")
    root.geometry("400x300")
    
    # 添加一些基础组件
    label = tk.Label(root, text="这是一个测试窗口", font=('Arial', 14))
    label.pack(pady=20)
    
    button = tk.Button(root, text="测试按钮", command=lambda: print("按钮被点击"))
    button.pack(pady=10)
    
    entry = tk.Entry(root)
    entry.pack(pady=10)
    entry.insert(0, "测试输入框")
    
    # 添加退出按钮
    quit_btn = tk.Button(root, text="退出", command=root.quit)
    quit_btn.pack(pady=10)
    
    print("窗口已创建，启动主循环...")
    print("如果看到这条消息但没有窗口，说明存在显示问题")
    
    root.mainloop()
    print("窗口已关闭")

def test_ttk_widgets():
    """
    测试ttk组件
    """
    print("创建ttk组件测试窗口...")
    
    root = tk.Tk()
    root.title("ttk组件测试")
    root.geometry("500x400")
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    title = ttk.Label(main_frame, text="ttk组件测试", font=('Arial', 16, 'bold'))
    title.pack(pady=10)
    
    # 按钮
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=10)
    
    ttk.Button(btn_frame, text="按钮1").pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="按钮2").pack(side=tk.LEFT, padx=5)
    
    # 输入框
    ttk.Label(main_frame, text="输入框:").pack(anchor=tk.W)
    entry = ttk.Entry(main_frame, width=30)
    entry.pack(pady=5, anchor=tk.W)
    
    # 下拉框
    ttk.Label(main_frame, text="下拉框:").pack(anchor=tk.W, pady=(10,0))
    combo = ttk.Combobox(main_frame, values=["选项1", "选项2", "选项3"])
    combo.pack(pady=5, anchor=tk.W)
    combo.set("选项1")
    
    # 进度条
    ttk.Label(main_frame, text="进度条:").pack(anchor=tk.W, pady=(10,0))
    progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
    progress.pack(pady=5, anchor=tk.W)
    progress['value'] = 50
    
    # 退出按钮
    ttk.Button(main_frame, text="退出", command=root.quit).pack(pady=20)
    
    print("ttk窗口已创建，启动主循环...")
    root.mainloop()
    print("ttk窗口已关闭")

def main():
    """
    主测试函数
    """
    print("=" * 50)
    print("tkinter GUI 诊断测试")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print(f"tkinter版本: {tk.TkVersion}")
    print(f"tcl版本: {tk.TclVersion}")
    print()
    
    try:
        print("测试1: 基础tkinter窗口")
        test_basic_window()
        print()
        
        print("测试2: ttk组件窗口")
        test_ttk_widgets()
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("测试完成")

if __name__ == "__main__":
    main()