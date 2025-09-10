# 视频人脸检测 GUI 使用指南

## 概述

本项目现在提供了一个图形用户界面（GUI），让用户可以通过鼠标点击的方式选择文件和设置参数，无需使用命令行。

## 功能特性

### 🎯 核心功能
- **文件选择**: 通过文件浏览器选择输入视频和输出路径
- **检测器选择**: 支持多种人脸检测后端
- **处理模式**: 预览模式和马赛克模式
- **实时进度**: 显示处理进度和统计信息
- **预览功能**: 可以预览输入视频的第一帧

### 🔧 检测器类型
1. **YuNet**: 基础的高性能人脸检测器
2. **Hybrid (YuNet)**: 混合检测器，以YuNet为主，可选DeepFace增强
3. **Hybrid (DeepFace)**: 混合检测器，以DeepFace为主，支持高级分析

### ⚙️ 参数设置
- **马赛克大小**: 调整马赛克块的大小（10-100像素）
- **DeepFace增强**: 启用高级人脸分析功能（需要安装DeepFace）

## 启动方式

### 方法1: 使用启动器（推荐）
```bash
python3 launch_gui.py
```

启动器会自动：
- 检测支持tkinter的Python环境
- 验证必要依赖
- 启动GUI应用

### 方法2: 直接启动
```bash
# 使用虚拟环境（如果tkinter可用）
python3 gui_app.py

# 或使用系统Python
/usr/bin/python3 gui_app.py
```

## 使用步骤

### 1. 选择输入文件
- 点击"选择输入文件"按钮
- 在文件浏览器中选择要处理的视频文件
- 支持常见视频格式（MP4、AVI、MOV等）

### 2. 设置输出路径
- 点击"选择输出文件"按钮
- 选择输出视频的保存位置和文件名
- 建议使用.mp4格式

### 3. 配置参数
- **检测器类型**: 根据需要选择检测器
  - YuNet: 快速、稳定
  - Hybrid: 功能更丰富，但需要更多依赖
- **马赛克大小**: 调整滑块设置马赛克块大小
- **DeepFace增强**: 如果需要高级分析功能可以启用

### 4. 选择处理模式
- **预览模式**: 在人脸周围绘制检测框，用于验证检测效果
- **马赛克模式**: 对检测到的人脸应用马赛克效果

### 5. 开始处理
- 点击"开始处理"按钮
- 观察进度条和日志输出
- 处理完成后可选择打开输出目录

### 6. 预览功能
- 点击"预览输入"按钮可以查看输入视频的第一帧
- 帮助确认视频内容和质量

## 界面说明

### 文件选择区域
- 输入文件路径显示
- 输出文件路径显示
- 文件选择按钮

### 参数设置区域
- 检测器类型下拉菜单
- 马赛克大小滑块
- DeepFace增强复选框

### 处理模式区域
- 预览模式单选按钮
- 马赛克模式单选按钮

### 控制区域
- 开始处理按钮
- 停止处理按钮
- 预览输入按钮
- 打开输出目录按钮

### 进度显示区域
- 进度条
- 当前状态文本

### 日志区域
- 详细的处理日志
- 错误信息显示
- 处理统计信息

## 依赖要求

### 基础依赖
```bash
# 系统Python需要的包
pip3 install opencv-python numpy Pillow
```

### 可选依赖（用于HybridFaceDetector）
```bash
# 在虚拟环境中安装
pip install deepface tf-keras
```

## 故障排除

### tkinter相关问题

**问题**: `ModuleNotFoundError: No module named '_tkinter'`

**解决方案**:
1. 使用系统自带的Python: `/usr/bin/python3 gui_app.py`
2. 安装tkinter支持:
   ```bash
   # macOS Homebrew
   brew install python-tk
   
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   ```

### 依赖缺失问题

**问题**: 缺少opencv、numpy或PIL

**解决方案**:
```bash
# 为系统Python安装
/usr/bin/python3 -m pip install opencv-python numpy Pillow
```

### DeepFace相关问题

**问题**: DeepFace功能不可用

**解决方案**:
1. 在虚拟环境中安装DeepFace:
   ```bash
   source venv/bin/activate
   pip install deepface tf-keras
   ```
2. 如果不需要DeepFace功能，可以只使用YuNet检测器

### 性能问题

**建议**:
- 对于大视频文件，建议先用预览模式测试
- YuNet检测器比DeepFace更快
- 可以调整马赛克大小来平衡效果和性能

## 命令行备选方案

如果GUI无法正常工作，可以使用命令行版本：

```bash
# 预览模式
python3 main.py input.mp4 --output preview.mp4 --preview

# 马赛克模式
python3 main.py input.mp4 --output mosaic.mp4 --mosaic --mosaic-size 30
```

## 技术特性

### 进度回调
- 实时显示处理进度
- 支持用户中断处理
- 详细的统计信息

### 多检测器支持
- YuNet: OpenCV的高性能检测器
- HybridFaceDetector: 结合多种检测技术
- 自动回退机制

### 椭圆形马赛克
- 更自然的马赛克效果
- 可调节大小
- 高质量的边缘处理

## 更新日志

### v1.0.0
- ✅ 基础GUI界面
- ✅ 文件选择功能
- ✅ 参数配置
- ✅ 实时进度显示
- ✅ 多检测器支持
- ✅ 预览功能
- ✅ 自动环境检测

## 支持

如果遇到问题，请检查：
1. Python版本（建议3.8+）
2. 依赖安装情况
3. 输入文件格式
4. 系统权限

更多技术细节请参考项目中的其他文档文件。