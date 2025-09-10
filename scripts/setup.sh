#!/bin/bash

# 视频人脸检测项目安装脚本
# 适用于 macOS 和 Linux 系统

echo "=== 视频人脸检测项目安装脚本 ==="
echo

# 检查 Python 3 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3，请先安装 Python 3.7 或更高版本"
    exit 1
fi

echo "检测到 Python 版本:"
python3 --version
echo

# 创建虚拟环境
echo "正在创建 Python 虚拟环境..."
if [ -d "venv" ]; then
    echo "虚拟环境已存在，跳过创建步骤"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✓ 虚拟环境创建成功"
    else
        echo "✗ 虚拟环境创建失败"
        exit 1
    fi
fi
echo

# 激活虚拟环境并安装依赖
echo "正在激活虚拟环境并安装依赖..."
source venv/bin/activate

# 升级 pip 和基础工具
echo "升级 pip 和基础工具..."
python -m pip install --upgrade pip setuptools wheel

# 安装项目依赖
echo "安装 OpenCV 和 NumPy..."
pip install opencv-python numpy

if [ $? -eq 0 ]; then
    echo "✓ 依赖安装成功"
else
    echo "✗ 依赖安装失败"
    exit 1
fi
echo

# 检查必要文件
if [[ ! -f "../main.py" ]]; then
    echo "错误: 找不到 ../main.py 文件"
    echo "请确保在项目根目录下运行此脚本"
    exit 1
fi

# 创建模型目录
echo "创建模型目录..."
mkdir -p ../models

cd ../models

cd ../scripts
echo "模型文件下载完成"

# 测试安装
echo "测试安装是否成功..."
python -c "import cv2; import numpy as np; from face_detector import VideoFaceDetector; print('✓ 所有模块导入成功'); detector = VideoFaceDetector(); print('✓ YuNet人脸检测器初始化成功')"

if [ $? -eq 0 ]; then
    echo
    echo "🎉 安装完成！"
    echo
    echo "使用方法:"
    echo "1. 激活虚拟环境: source venv/bin/activate"
    echo "2. 运行主程序: python main.py your_video.mp4"
    echo "3. 查看帮助: python main.py --help"
    echo "4. 运行示例: python example.py"
    echo
    echo "更多信息请查看 README.md 文件"
else
    echo "✗ 安装测试失败，请检查错误信息"
    exit 1
fi