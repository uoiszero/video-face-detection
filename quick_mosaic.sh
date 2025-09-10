#!/bin/bash
# -*- coding: utf-8 -*-

# 一键打码脚本 (Shell版本)
# 使用混合检测器、侧脸检测优化、延续15帧的配置进行视频人脸打码
#
# 使用方法:
#   chmod +x quick_mosaic.sh
#   ./quick_mosaic.sh input_video.mp4
#   
# 输出文件将自动命名为: input_video_out_20231201_143022.mp4

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🎯 $1${NC}"
}

# 生成输出文件名
get_output_filename() {
    local input_file="$1"
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local dir=$(dirname "$input_file")
    local basename=$(basename "$input_file")
    local filename="${basename%.*}"
    local extension="${basename##*.}"
    
    echo "${dir}/${filename}_out_${timestamp}.${extension}"
}

# 检查依赖文件
check_dependencies() {
    local missing_files=()
    
    # 检查必要文件
    if [[ ! -f "main.py" ]]; then
        missing_files+=("main.py")
    fi
    
    if [[ ! -f "models/face_detection_yunet_2023mar.onnx" ]]; then
        missing_files+=("models/face_detection_yunet_2023mar.onnx")
    fi
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "缺少必要文件:"
        for file in "${missing_files[@]}"; do
            echo "   - $file"
        done
        echo ""
        print_info "请先运行安装脚本: python install_dependencies.py"
        return 1
    fi
    
    return 0
}

# 检查视频文件格式
check_video_format() {
    local input_file="$1"
    local extension="${input_file##*.}"
    extension=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
    
    local supported_formats=("mp4" "avi" "mov" "mkv" "wmv" "flv" "webm" "m4v")
    
    for format in "${supported_formats[@]}"; do
        if [[ "$extension" == "$format" ]]; then
            return 0
        fi
    done
    
    print_warning "$extension 可能不是支持的视频格式"
    print_info "支持的格式: ${supported_formats[*]}"
    
    read -p "是否继续处理? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy是]$ ]]; then
        print_info "已取消处理"
        exit 0
    fi
}

# 执行视频打码处理
run_mosaic() {
    local input_file="$1"
    local output_file="$2"
    
    print_header "开始处理视频: $input_file"
    print_info "输出文件: $output_file"
    print_info "使用配置: 混合检测器 + RetinaFace后端 + 延续15帧"
    echo ""
    echo "=========================================================="
    
    # 构建命令
    local cmd=(
        "python" "main.py"
        "$input_file"
        "--detector" "hybrid"
        "--deepface-backend" "retinaface"
        "--continuation-frames" "15"
        "--mosaic"
        "--output" "$output_file"
    )
    
    # 执行命令
    if "${cmd[@]}"; then
        echo ""
        echo "=========================================================="
        print_success "处理完成! 输出文件: $output_file"
        
        # 检查输出文件
        if [[ -f "$output_file" ]]; then
            local file_size=$(du -h "$output_file" | cut -f1)
            print_info "文件大小: $file_size"
            return 0
        else
            print_warning "输出文件未找到，可能处理失败"
            return 1
        fi
    else
        print_error "处理失败"
        return 1
    fi
}

# 打印使用说明
print_usage() {
    print_header "一键打码脚本"
    echo "=================================================="
    echo "使用方法:"
    echo "  ./quick_mosaic.sh <输入视频文件>"
    echo ""
    echo "示例:"
    echo "  ./quick_mosaic.sh sample.mp4"
    echo "  ./quick_mosaic.sh /path/to/video.avi"
    echo ""
    echo "功能特性:"
    print_success "混合检测器 (YuNet + DeepFace)"
    print_success "侧脸检测优化 (RetinaFace后端)"
    print_success "延续打码 (15帧)"
    print_success "自动生成输出文件名"
    echo ""
    echo "输出文件命名规则:"
    echo "  原文件名_out_时间戳.扩展名"
    echo "  例: sample_out_20231201_143022.mp4"
    echo ""
    echo "首次使用请确保脚本有执行权限:"
    echo "  chmod +x quick_mosaic.sh"
}

# 主函数
main() {
    # 检查参数
    if [[ $# -ne 1 ]]; then
        print_error "参数错误!"
        echo ""
        print_usage
        exit 1
    fi
    
    local input_file="$1"
    
    # 检查输入文件是否存在
    if [[ ! -f "$input_file" ]]; then
        print_error "输入文件不存在: $input_file"
        exit 1
    fi
    
    # 检查视频格式
    check_video_format "$input_file"
    
    # 检查依赖
    if ! check_dependencies; then
        exit 1
    fi
    
    # 生成输出文件名
    local output_file
    output_file=$(get_output_filename "$input_file")
    
    # 检查输出文件是否已存在
    if [[ -f "$output_file" ]]; then
        print_warning "输出文件已存在: $output_file"
        read -p "是否覆盖? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy是]$ ]]; then
            print_info "已取消处理"
            exit 0
        fi
    fi
    
    # 执行打码处理
    if run_mosaic "$input_file" "$output_file"; then
        echo ""
        print_success "🎉 一键打码完成!"
        print_info "📁 输出文件: $output_file"
        exit 0
    else
        echo ""
        print_error "💥 处理失败!"
        exit 1
    fi
}

# 脚本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi