#!/bin/bash

# DeepFace安装脚本
# 用于安装DeepFace及其依赖项

echo "DeepFace人脸分析功能安装脚本"
echo "=================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3，请先安装pip"
    exit 1
fi

echo "当前Python版本:"
python3 --version
echo ""

# 询问用户是否继续
read -p "是否要安装DeepFace及其依赖？这将下载约500MB的文件 (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "安装已取消"
    exit 0
fi

echo "开始安装DeepFace..."
echo ""

# 升级pip
echo "1. 升级pip..."
pip3 install --upgrade pip

# 安装TensorFlow（DeepFace的主要依赖）
echo ""
echo "2. 安装TensorFlow..."
pip3 install tensorflow>=2.12.0

# 安装tf-keras
echo ""
echo "3. 安装tf-keras..."
pip3 install tf-keras>=2.12.0

# 安装DeepFace
echo ""
echo "4. 安装DeepFace..."
pip3 install deepface>=0.0.79

# 安装其他可能需要的依赖
echo ""
echo "5. 安装其他依赖..."
pip3 install Pillow
pip3 install matplotlib
pip3 install pandas

echo ""
echo "安装完成！"
echo ""

# 测试安装
echo "测试DeepFace安装..."
cd ..
python3 -c "
try:
    import deepface
    print('✓ DeepFace安装成功')
    print('版本:', deepface.__version__)
except ImportError as e:
    print('✗ DeepFace安装失败:', e)
    exit(1)

try:
    import tensorflow as tf
    print('✓ TensorFlow安装成功')
    print('版本:', tf.__version__)
except ImportError as e:
    print('✗ TensorFlow安装失败:', e)
    exit(1)

print('\n所有依赖安装成功！')
print('现在可以使用DeepFace人脸分析功能了')
"
cd scripts

echo ""
echo "安装说明:"
echo "- 首次使用DeepFace时，会自动下载预训练模型"
echo "- 模型文件较大，首次运行可能需要等待几分钟"
echo "- 模型会缓存在 ~/.deepface/ 目录中"
echo ""
echo "使用方法:"
echo "python3 demo_deepface_analysis.py  # 运行DeepFace演示"
echo "python3 deepface_detector.py       # 测试DeepFace检测器"
echo ""
echo "如需卸载DeepFace:"
echo "pip3 uninstall deepface tensorflow tf-keras"