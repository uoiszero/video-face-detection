#!/bin/bash

# 视频人脸检测项目 - 依赖安装脚本
# 自动检测并安装所需依赖

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_header() {
    echo -e "${BLUE}==========================================================${NC}"
    echo -e "${BLUE}🎯 视频人脸检测项目 - 依赖安装脚本${NC}"
    echo -e "${BLUE}==========================================================${NC}"
    echo -e "📁 项目路径: $(pwd)"
    echo -e "🖥️  系统信息: $(uname -s) $(uname -m)"
    echo -e "${BLUE}==========================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}🔍 $1${NC}"
}

# 检查Python环境
check_python() {
    print_info "检查Python环境..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "未找到Python，请先安装Python 3.8+"
        exit 1
    fi
    
    # 检查Python版本
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_success "找到Python: $PYTHON_CMD (版本: $PYTHON_VERSION)"
    
    # 检查版本是否满足要求
    if $PYTHON_CMD -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_success "Python版本检查通过"
    else
        print_error "需要Python 3.8或更高版本，当前版本: $PYTHON_VERSION"
        exit 1
    fi
}

# 检查pip
check_pip() {
    print_info "检查pip..."
    
    if $PYTHON_CMD -m pip --version &> /dev/null; then
        print_success "pip可用"
    else
        print_error "pip不可用，请先安装pip"
        exit 1
    fi
}

# 升级pip
upgrade_pip() {
    print_info "升级pip到最新版本..."
    $PYTHON_CMD -m pip install --upgrade pip
    print_success "pip升级完成"
}

# 创建虚拟环境（可选）
create_venv() {
    if [ "$1" = "--venv" ]; then
        print_info "创建虚拟环境..."
        if [ ! -d "venv" ]; then
            $PYTHON_CMD -m venv venv
            print_success "虚拟环境创建完成"
        else
            print_warning "虚拟环境已存在"
        fi
        
        print_info "激活虚拟环境..."
        source venv/bin/activate
        print_success "虚拟环境已激活"
    fi
}

# 安装Python依赖
install_python_deps() {
    print_info "安装Python依赖包..."
    
    # 首先尝试从requirements.txt安装
    if [ -f "requirements.txt" ]; then
        print_info "从requirements.txt安装依赖..."
        $PYTHON_CMD -m pip install -r requirements.txt
        print_success "requirements.txt依赖安装完成"
    else
        print_warning "未找到requirements.txt，安装基础依赖..."
        
        # 基础依赖列表
        PACKAGES=(
            "opencv-python>=4.8.0"
            "numpy>=1.21.0"
            "deepface>=0.0.79"
            "tensorflow>=2.12.0"
            "mtcnn>=0.1.1"
            "retina-face>=0.0.13"
        )
        
        for package in "${PACKAGES[@]}"; do
            print_info "安装 $package..."
            $PYTHON_CMD -m pip install "$package"
            print_success "$package 安装完成"
        done
    fi
}

# 创建模型目录
create_models_dir() {
    print_info "创建模型目录..."
    mkdir -p models
    print_success "模型目录已创建: $(pwd)/models"
}

# 下载YuNet模型
download_yunet_models() {
    print_info "下载YuNet模型文件..."
    
    cd models
    
    # YuNet模型URL和文件名
    declare -A MODELS=(
        ["face_detection_yunet_2023mar.onnx"]="https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
        ["face_detection_yunet_2023mar_int8.onnx"]="https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar_int8.onnx"
    )
    
    for model_file in "${!MODELS[@]}"; do
        if [ -f "$model_file" ]; then
            print_success "$model_file 已存在，跳过下载"
        else
            print_info "下载 $model_file..."
            if curl -L -o "$model_file" "${MODELS[$model_file]}"; then
                print_success "$model_file 下载完成"
            else
                print_error "$model_file 下载失败"
                # 尝试使用wget
                if command -v wget &> /dev/null; then
                    print_info "尝试使用wget下载 $model_file..."
                    if wget -O "$model_file" "${MODELS[$model_file]}"; then
                        print_success "$model_file 下载完成 (wget)"
                    else
                        print_error "$model_file 下载失败 (wget)"
                    fi
                fi
            fi
        fi
    done
    
    cd ..
}

# 验证安装
verify_installation() {
    print_info "验证安装结果..."
    
    # 运行Python验证脚本
    $PYTHON_CMD -c "
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
    
    if [ $? -eq 0 ]; then
        print_success "安装验证通过"
        return 0
    else
        print_error "安装验证失败"
        return 1
    fi
}

# 打印使用指南
print_usage_guide() {
    echo -e "${BLUE}==========================================================${NC}"
    echo -e "${GREEN}🚀 安装完成! 使用指南:${NC}"
    echo -e "${BLUE}==========================================================${NC}"
    echo -e "\n📖 基础使用:"
    echo -e "   python main.py sample.mp4 --mosaic --preview"
    echo -e "\n🔄 侧脸检测优化:"
    echo -e "   python main.py sample.mp4 --detector deepface --deepface-backend mtcnn --mosaic"
    echo -e "\n🔀 混合检测器 (推荐):"
    echo -e "   python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic"
    echo -e "\n🎯 自定义延续打码:"
    echo -e "   python main.py sample.mp4 --continuation-frames 10 --mosaic"
    echo -e "\n📷 实时摄像头检测:"
    echo -e "   python main.py 0 --detector yunet --mosaic --preview"
    echo -e "\n📚 更多帮助:"
    echo -e "   python main.py --help"
    echo -e "   查看 README.md 获取详细文档"
    echo -e "${BLUE}==========================================================${NC}"
}

# 主函数
main() {
    print_header
    
    # 解析命令行参数
    USE_VENV=false
    for arg in "$@"; do
        case $arg in
            --venv)
                USE_VENV=true
                shift
                ;;
            --help|-h)
                echo "使用方法: $0 [选项]"
                echo "选项:"
                echo "  --venv    创建并使用虚拟环境"
                echo "  --help    显示此帮助信息"
                exit 0
                ;;
        esac
    done
    
    # 执行安装步骤
    check_python
    check_pip
    
    if [ "$USE_VENV" = true ]; then
        create_venv --venv
    fi
    
    upgrade_pip
    create_models_dir
    install_python_deps
    download_yunet_models
    
    if verify_installation; then
        print_usage_guide
        print_success "🎉 所有依赖安装完成!"
    else
        print_error "安装过程中出现问题，请检查上述错误信息"
        echo -e "\n💡 建议:"
        echo -e "   1. 检查网络连接"
        echo -e "   2. 手动运行: python install_dependencies.py"
        echo -e "   3. 查看详细错误信息并手动安装失败的包"
        exit 1
    fi
}

# 运行主函数
main "$@"