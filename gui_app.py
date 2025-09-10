#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频人脸检测工具 - GUI版本
提供图形用户界面，让用户可以通过鼠标点击选择文件和参数

作者: AI Assistant
版本: 1.0
日期: 2025-09-10
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
import cv2
from PIL import Image, ImageTk

# 导入我们的人脸检测模块
from face_detector import VideoFaceDetector
try:
    from deepface_detector import HybridFaceDetector
    HYBRID_AVAILABLE = True
except ImportError:
    HYBRID_AVAILABLE = False
    print("警告: HybridFaceDetector不可用，将仅使用YuNet检测器")

class VideoFaceDetectorGUI:
    """
    视频人脸检测工具的图形用户界面
    
    提供以下功能：
    - 文件选择（输入视频、输出路径）
    - 参数配置（马赛克大小、检测后端等）
    - 实时预览
    - 处理进度显示
    - 结果展示
    """
    
    def __init__(self, root):
        """
        初始化GUI应用
        
        Args:
            root: tkinter根窗口
        """
        self.root = root
        self.root.title("视频人脸检测工具 v1.0")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 应用变量
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.mosaic_size = tk.IntVar(value=30)
        self.detector_var = tk.StringVar(value="YuNet")
        self.processing_mode = tk.StringVar(value="preview")
        
        # 处理状态
        self.is_processing = False
        self.detector = None
        self.current_thread = None
        
        # 创建界面
        self.create_widgets()
        
        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """
        创建GUI组件
        """
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="视频人脸检测工具", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文件选择区域
        self.create_file_selection_frame(main_frame, 1)
        
        # 参数配置区域
        self.create_parameter_frame(main_frame, 2)
        
        # 处理模式选择
        self.create_mode_frame(main_frame, 3)
        
        # 控制按钮
        self.create_control_frame(main_frame, 4)
        
        # 进度显示
        self.create_progress_frame(main_frame, 5)
        
        # 日志输出
        self.create_log_frame(main_frame, 6)
    
    def create_file_selection_frame(self, parent, row):
        """
        创建文件选择区域
        
        Args:
            parent: 父容器
            row: 行号
        """
        file_frame = ttk.LabelFrame(parent, text="文件选择", padding="10")
        file_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # 输入文件
        ttk.Label(file_frame, text="输入视频:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(file_frame, text="浏览", command=self.select_input_file).grid(row=0, column=2)
        
        # 输出文件
        ttk.Label(file_frame, text="输出视频:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        ttk.Entry(file_frame, textvariable=self.output_file, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        ttk.Button(file_frame, text="浏览", command=self.select_output_file).grid(row=1, column=2, pady=(10, 0))
    
    def create_parameter_frame(self, parent, row):
        """
        创建参数配置区域
        
        Args:
            parent: 父容器
            row: 行号
        """
        param_frame = ttk.LabelFrame(parent, text="参数配置", padding="10")
        param_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 马赛克大小
        ttk.Label(param_frame, text="马赛克块大小:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        mosaic_scale = ttk.Scale(param_frame, from_=10, to=50, variable=self.mosaic_size, orient=tk.HORIZONTAL)
        mosaic_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Label(param_frame, textvariable=self.mosaic_size).grid(row=0, column=2)
        
        # 检测器类型选择
        ttk.Label(param_frame, text="检测器类型:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        detector_combo = ttk.Combobox(param_frame, textvariable=self.detector_var, 
                                   values=["YuNet", "Hybrid (YuNet)", "Hybrid (DeepFace)"], state="readonly")
        detector_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # DeepFace增强选项
        self.deepface_var = tk.BooleanVar(value=False)
        ttk.Label(param_frame, text="启用DeepFace增强:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        deepface_check = ttk.Checkbutton(param_frame, variable=self.deepface_var)
        deepface_check.grid(row=2, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # 如果HybridFaceDetector不可用，禁用相关选项
        if not HYBRID_AVAILABLE:
            detector_combo.config(values=["YuNet"])
            deepface_check.config(state=tk.DISABLED)
        
        param_frame.columnconfigure(1, weight=1)
    
    def create_mode_frame(self, parent, row):
        """
        创建处理模式选择区域
        
        Args:
            parent: 父容器
            row: 行号
        """
        mode_frame = ttk.LabelFrame(parent, text="处理模式", padding="10")
        mode_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="预览模式（显示检测框）", 
                       variable=self.processing_mode, value="preview").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="马赛克模式（人脸打码）", 
                       variable=self.processing_mode, value="mosaic").grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
    
    def create_control_frame(self, parent, row):
        """
        创建控制按钮区域
        
        Args:
            parent: 父容器
            row: 行号
        """
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=row, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="开始处理", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="停止处理", command=self.stop_processing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="预览输入视频", command=self.preview_input).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="打开输出目录", command=self.open_output_dir).pack(side=tk.LEFT)
    
    def create_progress_frame(self, parent, row):
        """
        创建进度显示区域
        
        Args:
            parent: 父容器
            row: 行号
        """
        progress_frame = ttk.LabelFrame(parent, text="处理进度", padding="10")
        progress_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, text="就绪")
        self.progress_label.grid(row=1, column=0, sticky=tk.W)
    
    def create_log_frame(self, parent, row):
        """
        创建日志输出区域
        
        Args:
            parent: 父容器
            row: 行号
        """
        log_frame = ttk.LabelFrame(parent, text="处理日志", padding="10")
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架的行权重
        parent.rowconfigure(row, weight=1)
    
    def select_input_file(self):
        """
        选择输入视频文件
        """
        filename = filedialog.askopenfilename(
            title="选择输入视频文件",
            filetypes=[
                ("视频文件", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            # 自动设置输出文件名
            if not self.output_file.get():
                input_path = Path(filename)
                output_path = input_path.parent / f"{input_path.stem}_processed{input_path.suffix}"
                self.output_file.set(str(output_path))
    
    def select_output_file(self):
        """
        选择输出视频文件
        """
        filename = filedialog.asksaveasfilename(
            title="选择输出视频文件",
            defaultextension=".mp4",
            filetypes=[
                ("MP4文件", "*.mp4"),
                ("AVI文件", "*.avi"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)
    
    def log_message(self, message):
        """
        在日志区域显示消息
        
        Args:
            message: 要显示的消息
        """
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_progress(self, progress, message):
        """
        更新进度显示
        
        Args:
            progress: 进度百分比 (0-100)
            message: 进度消息
        """
        self.progress_var.set(progress)
        self.progress_label.config(text=message)
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """
        验证输入参数
        
        Returns:
            bool: 验证是否通过
        """
        if not self.input_file.get():
            messagebox.showerror("错误", "请选择输入视频文件")
            return False
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("错误", "输入视频文件不存在")
            return False
        
        if not self.output_file.get():
            messagebox.showerror("错误", "请设置输出视频文件路径")
            return False
        
        # 确保输出目录存在
        output_dir = os.path.dirname(self.output_file.get())
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出目录: {e}")
                return False
        
        return True
    
    def start_processing(self):
        """
        开始视频处理
        """
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            messagebox.showwarning("警告", "正在处理中，请等待完成")
            return
        
        # 更新UI状态
        self.is_processing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中处理视频
        self.current_thread = threading.Thread(target=self.process_video_thread)
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def stop_processing(self):
        """
        停止视频处理
        """
        self.is_processing = False
        self.log_message("用户请求停止处理...")
    
    def process_video_thread(self):
        """
        在后台线程中处理视频
        """
        try:
            # 初始化检测器
            self.log_message("初始化人脸检测器...")
            
            detector_type = self.detector_var.get()
            if HYBRID_AVAILABLE and detector_type == "Hybrid (DeepFace)":
                enable_deepface = self.deepface_var.get()
                self.detector = HybridFaceDetector(
                    primary_backend='deepface',
                    enable_deepface=enable_deepface
                )
                self.log_message("使用 Hybrid (DeepFace) 检测器")
            elif HYBRID_AVAILABLE and detector_type == "Hybrid (YuNet)":
                enable_deepface = self.deepface_var.get()
                self.detector = HybridFaceDetector(
                    primary_backend='yunet',
                    enable_deepface=enable_deepface
                )
                self.log_message("使用 Hybrid (YuNet) 检测器")
            else:
                self.detector = VideoFaceDetector()
                self.log_message("使用 YuNet 检测器")
            
            # 获取参数
            input_path = self.input_file.get()
            output_path = self.output_file.get()
            apply_mosaic = self.processing_mode.get() == "mosaic"
            mosaic_size = self.mosaic_size.get()
            
            self.log_message(f"输入文件: {input_path}")
            self.log_message(f"输出文件: {output_path}")
            self.log_message(f"处理模式: {'马赛克' if apply_mosaic else '预览'}")
            if apply_mosaic:
                self.log_message(f"马赛克大小: {mosaic_size}")
            
            # 开始处理
            self.update_progress(0, "开始处理视频...")
            
            # 这里需要修改 VideoFaceDetector 来支持进度回调
            result = self.process_video_with_progress(
                input_path, output_path, apply_mosaic, mosaic_size
            )
            
            if self.is_processing:  # 检查是否被用户停止
                self.update_progress(100, "处理完成")
                self.log_message("\n=== 处理完成 ===")
                self.log_message(f"总处理帧数: {result['processed_frames']}")
                self.log_message(f"检测到人脸的帧数: {result['frames_with_faces']}")
                self.log_message(f"总检测人脸数: {result['total_faces_detected']}")
                self.log_message(f"人脸检测率: {result['detection_rate']:.2%}")
                self.log_message(f"处理时间: {result['processing_time']:.2f}秒")
                
                # 询问是否打开输出文件
                if messagebox.askyesno("完成", "处理完成！是否打开输出文件所在目录？"):
                    self.open_output_dir()
            
        except Exception as e:
            self.log_message(f"处理出错: {str(e)}")
            messagebox.showerror("错误", f"处理失败: {str(e)}")
        
        finally:
            # 恢复UI状态
            self.is_processing = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            if not self.is_processing:
                self.update_progress(0, "就绪")
    
    def process_video_with_progress(self, input_path, output_path, apply_mosaic, mosaic_size):
        """
        带进度回调的视频处理
        
        Args:
            input_path: 输入视频路径
            output_path: 输出视频路径
            apply_mosaic: 是否应用马赛克
            mosaic_size: 马赛克大小
            
        Returns:
            dict: 处理结果
        """
        # 这是一个简化版本，实际需要修改 VideoFaceDetector 来支持进度回调
        # 这里我们模拟进度更新
        
        cap = cv2.VideoCapture(input_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        # 使用自定义的进度回调
        class ProgressCallback:
            def __init__(self, gui, total_frames):
                self.gui = gui
                self.total_frames = total_frames
                self.processed = 0
            
            def update(self, processed_frames):
                self.processed = processed_frames
                progress = (processed_frames / self.total_frames) * 100
                self.gui.update_progress(progress, f"处理进度: {processed_frames}/{self.total_frames}")
                return self.gui.is_processing  # 返回是否继续处理
        
        callback = ProgressCallback(self, total_frames)
        
        # 调用检测器处理视频（带进度回调）
        result = self.detector.process_video(
            input_path, output_path, 
            show_preview=False, 
            apply_mosaic=apply_mosaic, 
            mosaic_size=mosaic_size,
            progress_callback=callback.update
        )
        
        return result
    
    def preview_input(self):
        """
        预览输入视频
        """
        if not self.input_file.get():
            messagebox.showwarning("警告", "请先选择输入视频文件")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("错误", "输入视频文件不存在")
            return
        
        try:
            # 使用系统默认程序打开视频
            if sys.platform == "darwin":  # macOS
                os.system(f"open '{self.input_file.get()}'")
            elif sys.platform == "win32":  # Windows
                os.startfile(self.input_file.get())
            else:  # Linux
                os.system(f"xdg-open '{self.input_file.get()}'")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开视频文件: {e}")
    
    def open_output_dir(self):
        """
        打开输出文件所在目录
        """
        output_path = self.output_file.get()
        if not output_path:
            messagebox.showwarning("警告", "请先设置输出文件路径")
            return
        
        output_dir = os.path.dirname(output_path) or "."
        
        try:
            if sys.platform == "darwin":  # macOS
                os.system(f"open '{output_dir}'")
            elif sys.platform == "win32":  # Windows
                os.startfile(output_dir)
            else:  # Linux
                os.system(f"xdg-open '{output_dir}'")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开目录: {e}")
    
    def on_closing(self):
        """
        窗口关闭事件处理
        """
        if self.is_processing:
            if messagebox.askokcancel("退出", "正在处理视频，确定要退出吗？"):
                self.is_processing = False
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """
    主函数 - 启动GUI应用
    """
    try:
        print("正在启动GUI应用...")
        
        # 创建主窗口
        root = tk.Tk()
        print("✓ 主窗口创建成功")
        
        # Mac系统特定设置
        if sys.platform == "darwin":  # macOS
            try:
                # 强制应用显示在前台
                root.lift()
                root.call('wm', 'attributes', '.', '-topmost', True)
                root.after_idle(root.attributes, '-topmost', False)
                print("✓ Mac系统窗口设置完成")
            except Exception as e:
                print(f"Mac系统设置警告: {e}")
        
        # 设置窗口图标（如果有的话）
        try:
            # 可以在这里设置应用图标
            # root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        print("正在创建GUI组件...")
        # 创建应用实例
        app = VideoFaceDetectorGUI(root)
        print("✓ GUI组件创建完成")
        
        # 确保窗口更新
        root.update_idletasks()
        root.update()
        print("✓ 窗口更新完成")
        
        print("GUI应用启动成功！如果看不到窗口，请检查Dock或按Cmd+Tab切换应用")
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()