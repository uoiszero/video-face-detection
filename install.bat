@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 视频人脸检测项目 - Windows依赖安装脚本
REM 自动检测并安装所需依赖

echo ============================================================
echo 🎯 视频人脸检测项目 - 依赖安装脚本 (Windows)
echo ============================================================
echo 📁 项目路径: %CD%
echo 🖥️  系统信息: Windows
echo ============================================================
echo.

REM 检查Python环境
echo 🔍 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，尝试python3命令...
    python3 --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo ❌ 未找到Python，请先安装Python 3.8+
        echo 💡 下载地址: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

REM 获取Python版本
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ 找到Python: %PYTHON_CMD% (版本: %PYTHON_VERSION%)

REM 检查pip
echo.
echo 🔍 检查pip...
%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip不可用，请先安装pip
    pause
    exit /b 1
)
echo ✅ pip可用

REM 升级pip
echo.
echo 🔍 升级pip到最新版本...
%PYTHON_CMD% -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ⚠️  pip升级失败，继续安装...
) else (
    echo ✅ pip升级完成
)

REM 创建模型目录
echo.
echo 📁 创建模型目录...
if not exist "models" mkdir models
echo ✅ 模型目录已创建: %CD%\models

REM 安装Python依赖
echo.
echo 📦 安装Python依赖包...

REM 首先尝试从requirements.txt安装
if exist "requirements.txt" (
    echo 📋 从requirements.txt安装依赖...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo ⚠️  requirements.txt安装失败，尝试逐个安装...
        goto install_individual
    ) else (
        echo ✅ requirements.txt依赖安装完成
        goto download_models
    )
) else (
    echo ⚠️  未找到requirements.txt，安装基础依赖...
    goto install_individual
)

:install_individual
echo 📦 逐个安装必需包...

REM 基础依赖列表
set packages=opencv-python>=4.8.0 numpy>=1.21.0 deepface>=0.0.79 tensorflow>=2.12.0 mtcnn>=0.1.1 retina-face>=0.0.13

for %%p in (%packages%) do (
    echo 📦 安装 %%p...
    %PYTHON_CMD% -m pip install "%%p"
    if !errorlevel! neq 0 (
        echo ❌ %%p 安装失败
    ) else (
        echo ✅ %%p 安装成功
    )
)

:download_models
echo.
echo 🤖 下载YuNet模型文件...

cd models

REM 下载主模型文件
if not exist "face_detection_yunet_2023mar.onnx" (
    echo 📥 下载 face_detection_yunet_2023mar.onnx...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar.onnx' -OutFile 'face_detection_yunet_2023mar.onnx'"
    if !errorlevel! neq 0 (
        echo ❌ face_detection_yunet_2023mar.onnx 下载失败
    ) else (
        echo ✅ face_detection_yunet_2023mar.onnx 下载完成
    )
) else (
    echo ✅ face_detection_yunet_2023mar.onnx 已存在，跳过下载
)

REM 下载INT8量化模型文件
if not exist "face_detection_yunet_2023mar_int8.onnx" (
    echo 📥 下载 face_detection_yunet_2023mar_int8.onnx...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar_int8.onnx' -OutFile 'face_detection_yunet_2023mar_int8.onnx'"
    if !errorlevel! neq 0 (
        echo ❌ face_detection_yunet_2023mar_int8.onnx 下载失败
    ) else (
        echo ✅ face_detection_yunet_2023mar_int8.onnx 下载完成
    )
) else (
    echo ✅ face_detection_yunet_2023mar_int8.onnx 已存在，跳过下载
)

cd ..

REM 验证安装
echo.
echo 🔍 验证安装结果...

%PYTHON_CMD% -c "
import sys
print('🔍 验证Python包导入...')

# 测试导入
test_packages = [
    ('cv2', 'OpenCV'),
    ('numpy', 'NumPy'),
    ('deepface', 'DeepFace'),
    ('tensorflow', 'TensorFlow')
]

failed = []
for module, name in test_packages:
    try:
        __import__(module)
        print(f'✅ {name} 导入成功')
    except ImportError as e:
        print(f'❌ {name} 导入失败: {e}')
        failed.append(name)

# 检查模型文件
import os
model_files = [
    'models/face_detection_yunet_2023mar.onnx',
    'models/face_detection_yunet_2023mar_int8.onnx'
]

model_count = 0
for model_file in model_files:
    if os.path.exists(model_file):
        model_count += 1
        print(f'✅ 模型文件存在: {model_file}')
    else:
        print(f'❌ 模型文件缺失: {model_file}')

if failed:
    print(f'❌ 验证失败: {len(failed)} 个包导入失败')
    sys.exit(1)
elif model_count == 0:
    print('❌ 验证失败: 没有可用的模型文件')
    sys.exit(1)
else:
    print('✅ 安装验证成功!')
    print(f'   📦 Python包: 全部导入成功')
    print(f'   🤖 模型文件: {model_count}/2 个可用')
"

if %errorlevel% neq 0 (
    echo.
    echo ❌ 安装过程中出现问题，请检查上述错误信息
    echo.
    echo 💡 建议:
    echo    1. 检查网络连接
    echo    2. 手动运行: python install_dependencies.py
    echo    3. 查看详细错误信息并手动安装失败的包
    echo.
    pause
    exit /b 1
)

REM 打印使用指南
echo.
echo ============================================================
echo 🚀 安装完成! 使用指南:
echo ============================================================
echo.
echo 📖 基础使用:
echo    python main.py sample.mp4 --mosaic --preview
echo.
echo 🔄 侧脸检测优化:
echo    python main.py sample.mp4 --detector deepface --deepface-backend mtcnn --mosaic
echo.
echo 🔀 混合检测器 (推荐):
echo    python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic
echo.
echo 🎯 自定义延续打码:
echo    python main.py sample.mp4 --continuation-frames 10 --mosaic
echo.
echo 📷 实时摄像头检测:
echo    python main.py 0 --detector yunet --mosaic --preview
echo.
echo 📚 更多帮助:
echo    python main.py --help
echo    查看 README.md 获取详细文档
echo ============================================================
echo.
echo ✅ 🎉 所有依赖安装完成!
echo.
pause