#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频人脸打码GUI应用程序 (PyQt5版本)
提供用户友好的界面来配置和执行视频人脸检测与打码
"""

import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QFileDialog, QRadioButton, QButtonGroup,
        QSlider, QLineEdit, QMessageBox, QFrame, QSpacerItem, QSizePolicy,
        QTextEdit, QScrollArea
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    from PyQt5.QtGui import QFont
except ImportError:
    print("错误: 需要安装PyQt5")
    print("请运行: pip install PyQt5")
    sys.exit(1)

class ProcessingThread(QThread):
    """处理视频的后台线程"""
    
    finished = pyqtSignal(bool, str)  # 完成信号 (成功, 消息)
    output_received = pyqtSignal(str)  # 输出信号 (输出内容)
    
    def __init__(self, command):
        """初始化处理线程
        
        Args:
            command: 要执行的命令列表
        """
        super().__init__()
        self.command = command
        
    def run(self):
        """执行处理任务"""
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
                text=True,
                bufsize=1,  # 行缓冲
                universal_newlines=True
            )
            
            # 实时读取输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_received.emit(output.strip())
            
            # 等待进程结束
            process.wait()
            
            if process.returncode == 0:
                self.finished.emit(True, "处理完成！")
            else:
                self.finished.emit(False, f"处理失败，退出码: {process.returncode}")
                
        except Exception as e:
            self.finished.emit(False, f"执行失败: {str(e)}")

class MosaicGUI(QMainWindow):
    """视频人脸打码GUI主类"""
    
    def __init__(self):
        """初始化GUI界面"""
        super().__init__()
        self.setWindowTitle("视频人脸打码工具")
        self.setGeometry(100, 100, 600, 500)
        
        # 固定窗口大小，禁用调整大小
        self.setFixedSize(600, 800)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        
        # 初始化变量
        self.input_file = ""
        self.output_dir = os.getcwd()
        self.detector = "hybrid"
        self.profile_detector = "retinaface"
        self.output_mode = "mosaic"
        self.codec = "auto"
        self.mosaic_size = 20
        self.continuation_frames = 15
        
        # 处理线程
        self.processing_thread = None
        
        # 创建界面
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        # 中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 1. 文件选择器
        self.create_file_selector(layout)
        
        # 2. 输出文件夹选择器
        self.create_output_selector(layout)
        
        # 3. 检测器选择
        self.create_detector_selector(layout)
        
        # 4. 侧脸检测器选择
        self.create_profile_detector_selector(layout)
        
        # 5. 输出模式选择
        self.create_output_mode_selector(layout)
        
        # 6. 编码器选择
        self.create_codec_selector(layout)
        
        # 7. 马赛克大小设置
        self.create_mosaic_size_selector(layout)
        
        # 8. 延续帧数设置
        self.create_continuation_frames_selector(layout)
        
        # 9. 输出日志区域
        self.create_output_log(layout)
        
        # 控制按钮
        self.create_control_buttons(layout)
        
    def create_section_label(self, text):
        """创建章节标签
        
        Args:
            text: 标签文本
            
        Returns:
            QLabel: 配置好的标签
        """
        label = QLabel(text)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        label.setFont(font)
        return label
        
    def create_file_selector(self, layout):
        """创建输入文件选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("输入视频文件:"))
        
        # 文件选择布局
        file_layout = QHBoxLayout()
        
        self.file_line_edit = QLineEdit()
        self.file_line_edit.setReadOnly(True)
        self.file_line_edit.setPlaceholderText("请选择视频文件...")
        file_layout.addWidget(self.file_line_edit)
        
        file_button = QPushButton("选择文件")
        file_button.clicked.connect(self.select_input_file)
        file_layout.addWidget(file_button)
        
        layout.addLayout(file_layout)
        
    def create_output_selector(self, layout):
        """创建输出文件夹选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("输出文件夹:"))
        
        # 文件夹选择布局
        dir_layout = QHBoxLayout()
        
        self.dir_line_edit = QLineEdit()
        self.dir_line_edit.setReadOnly(True)
        self.dir_line_edit.setText(self.output_dir)
        dir_layout.addWidget(self.dir_line_edit)
        
        dir_button = QPushButton("选择文件夹")
        dir_button.clicked.connect(self.select_output_dir)
        dir_layout.addWidget(dir_button)
        
        layout.addLayout(dir_layout)
        
    def create_detector_selector(self, layout):
        """创建检测器选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("检测器类型:"))
        
        # 单选按钮布局
        detector_layout = QHBoxLayout()
        
        self.detector_group = QButtonGroup()
        
        detectors = [
            ("YuNet (快速)", "yunet"),
            ("DeepFace (精确)", "deepface"),
            ("Hybrid (推荐)", "hybrid")
        ]
        
        for text, value in detectors:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            radio.toggled.connect(self.on_detector_changed)
            self.detector_group.addButton(radio)
            detector_layout.addWidget(radio)
            
            if value == "hybrid":
                radio.setChecked(True)
                
        detector_layout.addStretch()
        layout.addLayout(detector_layout)
        
    def create_profile_detector_selector(self, layout):
        """创建侧脸检测器选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("侧脸检测器:"))
        
        # 单选按钮布局
        profile_layout = QHBoxLayout()
        
        self.profile_group = QButtonGroup()
        
        profile_detectors = [
            ("MTCNN", "mtcnn"),
            ("RetinaFace (推荐)", "retinaface")
        ]
        
        for text, value in profile_detectors:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            radio.toggled.connect(self.on_profile_detector_changed)
            self.profile_group.addButton(radio)
            profile_layout.addWidget(radio)
            
            if value == "retinaface":
                radio.setChecked(True)
                
        profile_layout.addStretch()
        layout.addLayout(profile_layout)
        
    def create_output_mode_selector(self, layout):
        """创建输出模式选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("输出模式:"))
        
        # 单选按钮布局
        mode_layout = QHBoxLayout()
        
        self.mode_group = QButtonGroup()
        
        modes = [
            ("预览模式", "preview"),
            ("打码输出", "mosaic")
        ]
        
        for text, value in modes:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            radio.toggled.connect(self.on_output_mode_changed)
            self.mode_group.addButton(radio)
            mode_layout.addWidget(radio)
            
            if value == "mosaic":
                radio.setChecked(True)
                
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
    def create_codec_selector(self, layout):
        """创建编码器选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("输出编码器:"))
        
        # 单选按钮布局
        codec_layout = QHBoxLayout()
        
        self.codec_group = QButtonGroup()
        
        codecs = [
            ("源文件编码", "auto"),
            ("H.264", "h264")
        ]
        
        for text, value in codecs:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            radio.toggled.connect(self.on_codec_changed)
            self.codec_group.addButton(radio)
            codec_layout.addWidget(radio)
            
            if value == "auto":
                radio.setChecked(True)
                
        codec_layout.addStretch()
        layout.addLayout(codec_layout)
        
    def create_mosaic_size_selector(self, layout):
        """创建马赛克大小选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        self.mosaic_label = self.create_section_label("马赛克大小:")
        layout.addWidget(self.mosaic_label)
        
        # 滑块布局
        mosaic_layout = QHBoxLayout()
        
        self.mosaic_slider = QSlider(Qt.Horizontal)
        self.mosaic_slider.setMinimum(5)
        self.mosaic_slider.setMaximum(50)
        self.mosaic_slider.setValue(20)
        self.mosaic_slider.valueChanged.connect(self.on_mosaic_size_changed)
        mosaic_layout.addWidget(self.mosaic_slider)
        
        self.mosaic_value_label = QLabel("20")
        self.mosaic_value_label.setMinimumWidth(30)
        mosaic_layout.addWidget(self.mosaic_value_label)
        
        layout.addLayout(mosaic_layout)
        
    def create_continuation_frames_selector(self, layout):
        """创建延续帧数选择器
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("延续打码帧数:"))
        
        # 滑块布局
        frames_layout = QHBoxLayout()
        
        self.frames_slider = QSlider(Qt.Horizontal)
        self.frames_slider.setMinimum(10)
        self.frames_slider.setMaximum(60)
        self.frames_slider.setValue(15)
        self.frames_slider.valueChanged.connect(self.on_continuation_frames_changed)
        frames_layout.addWidget(self.frames_slider)
        
        self.frames_value_label = QLabel("15")
        self.frames_value_label.setMinimumWidth(30)
        frames_layout.addWidget(self.frames_value_label)
        
        layout.addLayout(frames_layout)
        
    def create_output_log(self, layout):
        """创建输出日志区域
        
        Args:
            layout: 父布局
        """
        # 标签
        layout.addWidget(self.create_section_label("程序输出:"))
        
        # 输出文本框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(150)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.output_text)
        
    def create_control_buttons(self, layout):
        """创建控制按钮
        
        Args:
            layout: 父布局
        """
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 重置按钮
        reset_button = QPushButton("重置设置")
        reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_button)
        
        # 开始处理按钮
        self.start_button = QPushButton("开始处理")
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        button_layout.addWidget(self.start_button)
        
        layout.addLayout(button_layout)
        
    def select_input_file(self):
        """选择输入视频文件"""
        file_filter = "视频文件 (*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v);;所有文件 (*)"
        
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            file_filter
        )
        
        if filename:
            self.input_file = filename
            self.file_line_edit.setText(filename)
            
    def select_output_dir(self):
        """选择输出文件夹"""
        dirname = QFileDialog.getExistingDirectory(
            self,
            "选择输出文件夹",
            self.output_dir
        )
        
        if dirname:
            self.output_dir = dirname
            self.dir_line_edit.setText(dirname)
            
    def on_detector_changed(self):
        """检测器改变时的回调"""
        sender = self.sender()
        if sender.isChecked():
            self.detector = sender.property("value")
            
    def on_profile_detector_changed(self):
        """侧脸检测器改变时的回调"""
        sender = self.sender()
        if sender.isChecked():
            self.profile_detector = sender.property("value")
            
    def on_output_mode_changed(self):
        """输出模式改变时的回调"""
        sender = self.sender()
        if sender.isChecked():
            self.output_mode = sender.property("value")
            
            # 控制马赛克大小控件的可用性（如果已创建）
            if hasattr(self, 'mosaic_slider'):
                is_mosaic = self.output_mode == "mosaic"
                self.mosaic_slider.setEnabled(is_mosaic)
                self.mosaic_label.setEnabled(is_mosaic)
                self.mosaic_value_label.setEnabled(is_mosaic)
            
    def on_codec_changed(self):
        """编码器改变时的回调"""
        sender = self.sender()
        if sender.isChecked():
            self.codec = sender.property("value")
            
    def on_mosaic_size_changed(self, value):
        """马赛克大小改变时的回调
        
        Args:
            value: 滑块当前值
        """
        self.mosaic_size = value
        self.mosaic_value_label.setText(str(value))
        
    def on_continuation_frames_changed(self, value):
        """延续帧数改变时的回调
        
        Args:
            value: 滑块当前值
        """
        self.continuation_frames = value
        self.frames_value_label.setText(str(value))
        
    def generate_output_filename(self):
        """生成输出文件名
        
        Returns:
            str: 完整的输出文件路径
        """
        if not self.input_file:
            return ""
            
        # 获取文件名和扩展名
        input_path = Path(self.input_file)
        name_without_ext = input_path.stem
        extension = input_path.suffix
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 生成输出文件名
        output_filename = f"{name_without_ext}-out-{timestamp}{extension}"
        output_path = Path(self.output_dir) / output_filename
        
        return str(output_path)
        
    def validate_inputs(self):
        """验证用户输入
        
        Returns:
            bool: 输入是否有效
        """
        # 检查输入文件
        if not self.input_file:
            QMessageBox.critical(self, "错误", "请选择输入视频文件")
            return False
            
        if not os.path.exists(self.input_file):
            QMessageBox.critical(self, "错误", "输入文件不存在")
            return False
            
        # 检查输出文件夹
        if not os.path.exists(self.output_dir):
            QMessageBox.critical(self, "错误", "输出文件夹不存在")
            return False
            
        return True
        
    def build_command(self):
        """构建命令行参数
        
        Returns:
            list: 命令行参数列表
        """
        cmd = ["python", "main.py", self.input_file]
        
        # 检测器参数
        cmd.extend(["--detector", self.detector])
        
        # 如果使用deepface或hybrid，添加后端参数
        if self.detector in ["deepface", "hybrid"]:
            cmd.extend(["--deepface-backend", self.profile_detector])
            
        # 输出模式
        if self.output_mode == "preview":
            cmd.append("--preview")
        else:
            cmd.append("--mosaic")
            # 马赛克大小
            cmd.extend(["--mosaic-size", str(self.mosaic_size)])
            # 输出文件
            output_file = self.generate_output_filename()
            cmd.extend(["--output", output_file])
            
        # 延续帧数
        cmd.extend(["--continuation-frames", str(self.continuation_frames)])
        
        # 编码器
        cmd.extend(["--codec", self.codec])
        
        return cmd
        
    def start_processing(self):
        """开始处理视频"""
        if not self.validate_inputs():
            return
            
        # 构建命令
        cmd = self.build_command()
        
        # 显示命令预览
        cmd_str = " ".join(cmd)
        reply = QMessageBox.question(
            self,
            "确认处理",
            f"即将执行以下命令:\n\n{cmd_str}\n\n是否继续？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply != QMessageBox.Yes:
            return
            
        # 禁用开始按钮
        self.start_button.setEnabled(False)
        self.start_button.setText("处理中...")
        
        # 清空输出日志
        self.output_text.clear()
        self.output_text.append(f"执行命令: {' '.join(cmd)}")
        self.output_text.append("=" * 50)
        
        # 创建并启动处理线程
        self.processing_thread = ProcessingThread(cmd)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.output_received.connect(self.on_output_received)
        self.processing_thread.start()
        
    def on_processing_finished(self, success, message):
        """处理完成时的回调
        
        Args:
            success: 是否成功
            message: 结果消息
        """
        # 恢复开始按钮
        self.start_button.setEnabled(True)
        self.start_button.setText("开始处理")
        
        # 显示结果
        if success:
            if self.output_mode == "mosaic":
                output_file = self.generate_output_filename()
                QMessageBox.information(self, "成功", f"处理完成！\n输出文件: {output_file}")
            else:
                QMessageBox.information(self, "成功", "预览完成！")
        else:
            QMessageBox.critical(self, "错误", message)
            
    def on_output_received(self, output):
        """接收到程序输出时的回调
        
        Args:
            output: 程序输出内容
        """
        self.output_text.append(output)
        # 自动滚动到底部
        scrollbar = self.output_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
            
    def reset_settings(self):
        """重置所有设置到默认值"""
        self.input_file = ""
        self.output_dir = os.getcwd()
        self.detector = "hybrid"
        self.profile_detector = "retinaface"
        self.output_mode = "mosaic"
        self.codec = "auto"
        self.mosaic_size = 20
        self.continuation_frames = 15
        
        # 更新界面
        self.file_line_edit.setText("")
        self.dir_line_edit.setText(self.output_dir)
        
        # 重置单选按钮
        for button in self.detector_group.buttons():
            if button.property("value") == "hybrid":
                button.setChecked(True)
                
        for button in self.profile_group.buttons():
            if button.property("value") == "retinaface":
                button.setChecked(True)
                
        for button in self.mode_group.buttons():
            if button.property("value") == "mosaic":
                button.setChecked(True)
                
        for button in self.codec_group.buttons():
            if button.property("value") == "auto":
                button.setChecked(True)
                
        # 重置滑块
        self.mosaic_slider.setValue(20)
        self.frames_slider.setValue(15)
        
        # 清空输出日志
        self.output_text.clear()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    window = MosaicGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()