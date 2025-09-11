#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频人脸打码GUI应用程序
提供用户友好的界面来配置和执行视频人脸检测与打码
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
from datetime import datetime
from pathlib import Path

class MosaicGUI:
    """视频人脸打码GUI主类"""
    
    def __init__(self, root):
        """初始化GUI界面
        
        Args:
            root: tkinter根窗口对象
        """
        self.root = root
        self.root.title("视频人脸打码工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置窗口图标和样式
        self.setup_styles()
        
        # 初始化变量
        self.input_file_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        self.detector_var = tk.StringVar(value="hybrid")
        self.output_mode_var = tk.StringVar(value="mosaic")
        self.mosaic_size_var = tk.IntVar(value=20)
        self.continuation_frames_var = tk.IntVar(value=15)
        
        # 创建界面
        self.create_widgets()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Section.TLabel', font=('Arial', 10, 'bold'))
        
    def create_widgets(self):
        """创建所有GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # 标题
        title_label = ttk.Label(main_frame, text="视频人脸打码工具", style='Title.TLabel')
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # 1. 文件选择器
        self.create_file_selector(main_frame, row)
        row += 2
        
        # 2. 输出文件夹选择器
        self.create_output_selector(main_frame, row)
        row += 2
        
        # 3. 检测器选择
        self.create_detector_selector(main_frame, row)
        row += 2
        
        # 4. 输出模式选择
        self.create_output_mode_selector(main_frame, row)
        row += 2
        
        # 5. 马赛克大小设置
        self.create_mosaic_size_selector(main_frame, row)
        row += 2
        
        # 6. 延续帧数设置
        self.create_continuation_frames_selector(main_frame, row)
        row += 2
        
        # 控制按钮
        self.create_control_buttons(main_frame, row)
        
    def create_file_selector(self, parent, row):
        """创建输入文件选择器
        
        Args:
            parent: 父容器
            row: 行号
        """
        # 标签
        ttk.Label(parent, text="输入视频文件:", style='Section.TLabel').grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # 文件路径显示和选择按钮
        file_frame = ttk.Frame(parent)
        file_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.input_file_var, state='readonly')
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(file_frame, text="选择文件", command=self.select_input_file).grid(
            row=0, column=1
        )
        
    def create_output_selector(self, parent, row):
        """创建输出文件夹选择器
        
        Args:
            parent: 父容器
            row: 行号
        """
        # 标签
        ttk.Label(parent, text="输出文件夹:", style='Section.TLabel').grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # 文件夹路径显示和选择按钮
        dir_frame = ttk.Frame(parent)
        dir_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, state='readonly')
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(dir_frame, text="选择文件夹", command=self.select_output_dir).grid(
            row=0, column=1
        )
        
    def create_detector_selector(self, parent, row):
        """创建检测器选择器
        
        Args:
            parent: 父容器
            row: 行号
        """
        # 标签
        ttk.Label(parent, text="检测器类型:", style='Section.TLabel').grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # 单选按钮框架
        detector_frame = ttk.Frame(parent)
        detector_frame.grid(row=row+1, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        detectors = [
            ("YuNet (快速)", "yunet"),
            ("DeepFace (精确)", "deepface"),
            ("Hybrid (推荐)", "hybrid")
        ]
        
        for i, (text, value) in enumerate(detectors):
            ttk.Radiobutton(
                detector_frame, 
                text=text, 
                variable=self.detector_var, 
                value=value
            ).grid(row=0, column=i, padx=(0, 20), sticky=tk.W)
            
    def create_output_mode_selector(self, parent, row):
        """创建输出模式选择器
        
        Args:
            parent: 父容器
            row: 行号
        """
        # 标签
        ttk.Label(parent, text="输出模式:", style='Section.TLabel').grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # 单选按钮框架
        mode_frame = ttk.Frame(parent)
        mode_frame.grid(row=row+1, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        modes = [
            ("预览模式", "preview"),
            ("打码输出", "mosaic")
        ]
        
        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(
                mode_frame, 
                text=text, 
                variable=self.output_mode_var, 
                value=value,
                command=self.on_output_mode_change
            ).grid(row=0, column=i, padx=(0, 20), sticky=tk.W)
            
    def create_mosaic_size_selector(self, parent, row):
        """创建马赛克大小选择器
        
        Args:
            parent: 父容器
            row: 行号
        """
        # 标签
        self.mosaic_label = ttk.Label(parent, text="马赛克大小:", style='Section.TLabel')
        self.mosaic_label.grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        
        # 滑块和数值显示框架
        mosaic_frame = ttk.Frame(parent)
        mosaic_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        mosaic_frame.columnconfigure(0, weight=1)
        
        # 滑块
        self.mosaic_scale = ttk.Scale(
            mosaic_frame, 
            from_=5, 
            to=50, 
            variable=self.mosaic_size_var, 
            orient=tk.HORIZONTAL,
            command=self.on_mosaic_size_change
        )
        self.mosaic_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 数值显示
        self.mosaic_value_label = ttk.Label(mosaic_frame, text="20")
        self.mosaic_value_label.grid(row=0, column=1)
        
    def create_continuation_frames_selector(self, parent, row):
        """创建延续帧数选择器
        
        Args:
            parent: 父容器
            row: 行号
        """
        # 标签
        ttk.Label(parent, text="延续打码帧数:", style='Section.TLabel').grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # 滑块和数值显示框架
        frames_frame = ttk.Frame(parent)
        frames_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        frames_frame.columnconfigure(0, weight=1)
        
        # 滑块
        self.frames_scale = ttk.Scale(
            frames_frame, 
            from_=10, 
            to=60, 
            variable=self.continuation_frames_var, 
            orient=tk.HORIZONTAL,
            command=self.on_continuation_frames_change
        )
        self.frames_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 数值显示
        self.frames_value_label = ttk.Label(frames_frame, text="15")
        self.frames_value_label.grid(row=0, column=1)
        
    def create_control_buttons(self, parent, row):
        """创建控制按钮
        
        Args:
            parent: 父容器
            row: 行号
        """
        # 按钮框架
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(20, 0))
        
        # 开始处理按钮
        self.start_button = ttk.Button(
            button_frame, 
            text="开始处理", 
            command=self.start_processing,
            style='Accent.TButton'
        )
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # 重置按钮
        ttk.Button(
            button_frame, 
            text="重置设置", 
            command=self.reset_settings
        ).grid(row=0, column=1)
        
    def select_input_file(self):
        """选择输入视频文件"""
        filetypes = [
            ('视频文件', '*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v'),
            ('所有文件', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file_var.set(filename)
            
    def select_output_dir(self):
        """选择输出文件夹"""
        dirname = filedialog.askdirectory(
            title="选择输出文件夹",
            initialdir=self.output_dir_var.get()
        )
        
        if dirname:
            self.output_dir_var.set(dirname)
            
    def on_output_mode_change(self):
        """输出模式改变时的回调"""
        is_mosaic = self.output_mode_var.get() == "mosaic"
        
        # 控制马赛克大小控件的可用性
        state = 'normal' if is_mosaic else 'disabled'
        self.mosaic_scale.configure(state=state)
        
        # 更新标签颜色
        if is_mosaic:
            self.mosaic_label.configure(foreground='black')
        else:
            self.mosaic_label.configure(foreground='gray')
            
    def on_mosaic_size_change(self, value):
        """马赛克大小改变时的回调
        
        Args:
            value: 滑块当前值
        """
        self.mosaic_value_label.configure(text=str(int(float(value))))
        
    def on_continuation_frames_change(self, value):
        """延续帧数改变时的回调
        
        Args:
            value: 滑块当前值
        """
        self.frames_value_label.configure(text=str(int(float(value))))
        
    def generate_output_filename(self):
        """生成输出文件名
        
        Returns:
            str: 完整的输出文件路径
        """
        input_file = self.input_file_var.get()
        if not input_file:
            return ""
            
        # 获取文件名和扩展名
        input_path = Path(input_file)
        name_without_ext = input_path.stem
        extension = input_path.suffix
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 生成输出文件名
        output_filename = f"{name_without_ext}-out-{timestamp}{extension}"
        output_path = Path(self.output_dir_var.get()) / output_filename
        
        return str(output_path)
        
    def validate_inputs(self):
        """验证用户输入
        
        Returns:
            bool: 输入是否有效
        """
        # 检查输入文件
        if not self.input_file_var.get():
            messagebox.showerror("错误", "请选择输入视频文件")
            return False
            
        if not os.path.exists(self.input_file_var.get()):
            messagebox.showerror("错误", "输入文件不存在")
            return False
            
        # 检查输出文件夹
        if not os.path.exists(self.output_dir_var.get()):
            messagebox.showerror("错误", "输出文件夹不存在")
            return False
            
        return True
        
    def build_command(self):
        """构建命令行参数
        
        Returns:
            list: 命令行参数列表
        """
        cmd = ["python", "main.py", self.input_file_var.get()]
        
        # 检测器参数
        detector = self.detector_var.get()
        cmd.extend(["--detector", detector])
        
        # 如果使用deepface或hybrid，添加后端参数
        if detector in ["deepface", "hybrid"]:
            cmd.extend(["--deepface-backend", "retinaface"])
            
        # 输出模式
        if self.output_mode_var.get() == "preview":
            cmd.append("--preview")
        else:
            cmd.append("--mosaic")
            # 马赛克大小
            cmd.extend(["--mosaic-size", str(self.mosaic_size_var.get())])
            # 输出文件
            output_file = self.generate_output_filename()
            cmd.extend(["--output", output_file])
            
        # 延续帧数
        cmd.extend(["--continuation-frames", str(self.continuation_frames_var.get())])
        
        return cmd
        
    def start_processing(self):
        """开始处理视频"""
        if not self.validate_inputs():
            return
            
        # 构建命令
        cmd = self.build_command()
        
        # 显示命令预览
        cmd_str = " ".join(cmd)
        result = messagebox.askyesno(
            "确认处理", 
            f"即将执行以下命令:\n\n{cmd_str}\n\n是否继续？"
        )
        
        if not result:
            return
            
        try:
            # 禁用开始按钮
            self.start_button.configure(state='disabled', text='处理中...')
            self.root.update()
            
            # 执行命令
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            
            # 等待完成
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                if self.output_mode_var.get() == "mosaic":
                    output_file = self.generate_output_filename()
                    messagebox.showinfo("成功", f"处理完成！\n输出文件: {output_file}")
                else:
                    messagebox.showinfo("成功", "预览完成！")
            else:
                messagebox.showerror("错误", f"处理失败:\n{stderr}")
                
        except Exception as e:
            messagebox.showerror("错误", f"执行失败: {str(e)}")
            
        finally:
            # 恢复开始按钮
            self.start_button.configure(state='normal', text='开始处理')
            
    def reset_settings(self):
        """重置所有设置到默认值"""
        self.input_file_var.set("")
        self.output_dir_var.set(os.getcwd())
        self.detector_var.set("hybrid")
        self.output_mode_var.set("mosaic")
        self.mosaic_size_var.set(20)
        self.continuation_frames_var.set(15)
        
        # 更新界面
        self.on_output_mode_change()
        self.on_mosaic_size_change(20)
        self.on_continuation_frames_change(15)

def main():
    """主函数"""
    root = tk.Tk()
    app = MosaicGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()