#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键打码脚本
使用混合检测器、侧脸检测优化、延续15帧的配置进行视频人脸打码

使用方法:
    python quick_mosaic.py input_video.mp4
    
输出文件将自动命名为: input_video_out_20231201_143022.mp4
"""

import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

def get_output_filename(input_path):
    """
    根据输入文件名生成输出文件名
    格式: 原文件名_out_当前时间.扩展名
    
    Args:
        input_path (str): 输入文件路径
        
    Returns:
        str: 输出文件路径
    """
    input_file = Path(input_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 构建输出文件名: 原文件名_out_时间戳.扩展名
    output_name = f"{input_file.stem}_out_{timestamp}{input_file.suffix}"
    output_path = input_file.parent / output_name
    
    return str(output_path)

def check_dependencies():
    """
    检查必要的依赖是否存在
    
    Returns:
        bool: 依赖是否完整
    """
    required_files = [
        "main.py",
        "models/face_detection_yunet_2023mar.onnx"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n请先运行安装脚本: python install_dependencies.py")
        return False
    
    return True

def run_mosaic(input_file, output_file):
    """
    执行视频打码处理
    
    Args:
        input_file (str): 输入视频文件路径
        output_file (str): 输出视频文件路径
        
    Returns:
        bool: 处理是否成功
    """
    # 构建命令参数
    cmd = [
        "python", "main.py",
        input_file,
        "--detector", "hybrid",              # 使用混合检测器
        "--deepface-backend", "retinaface",  # 侧脸检测优化
        "--continuation-frames", "15",       # 延续15帧
        "--mosaic",                          # 启用打码
        "--output", output_file              # 指定输出文件
    ]
    
    print(f"🚀 开始处理视频: {input_file}")
    print(f"📁 输出文件: {output_file}")
    print(f"⚙️  使用配置: 混合检测器 + RetinaFace后端 + 延续15帧")
    print("\n" + "="*60)
    
    try:
        # 执行命令
        result = subprocess.run(cmd, check=True, capture_output=False)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print(f"✅ 处理完成! 输出文件: {output_file}")
            
            # 检查输出文件是否存在
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
                print(f"📊 文件大小: {file_size:.2f} MB")
                return True
            else:
                print("⚠️  输出文件未找到，可能处理失败")
                return False
        else:
            print(f"❌ 处理失败，退出码: {result.returncode}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  用户中断处理")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def print_usage():
    """
    打印使用说明
    """
    print("🎯 一键打码脚本")
    print("="*50)
    print("使用方法:")
    print("  python quick_mosaic.py <输入视频文件>")
    print("")
    print("示例:")
    print("  python quick_mosaic.py sample.mp4")
    print("  python quick_mosaic.py /path/to/video.avi")
    print("")
    print("功能特性:")
    print("  ✅ 混合检测器 (YuNet + DeepFace)")
    print("  ✅ 侧脸检测优化 (RetinaFace后端)")
    print("  ✅ 延续打码 (15帧)")
    print("  ✅ 自动生成输出文件名")
    print("")
    print("输出文件命名规则:")
    print("  原文件名_out_时间戳.扩展名")
    print("  例: sample_out_20231201_143022.mp4")

def main():
    """
    主函数
    """
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("❌ 参数错误!\n")
        print_usage()
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        sys.exit(1)
    
    # 检查文件是否为视频格式
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
    file_ext = Path(input_file).suffix.lower()
    if file_ext not in video_extensions:
        print(f"⚠️  警告: {file_ext} 可能不是支持的视频格式")
        print(f"支持的格式: {', '.join(video_extensions)}")
        
        # 询问是否继续
        response = input("是否继续处理? (y/N): ").strip().lower()
        if response not in ['y', 'yes', '是']:
            print("已取消处理")
            sys.exit(0)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 生成输出文件名
    output_file = get_output_filename(input_file)
    
    # 检查输出文件是否已存在
    if os.path.exists(output_file):
        print(f"⚠️  输出文件已存在: {output_file}")
        response = input("是否覆盖? (y/N): ").strip().lower()
        if response not in ['y', 'yes', '是']:
            print("已取消处理")
            sys.exit(0)
    
    # 执行打码处理
    success = run_mosaic(input_file, output_file)
    
    if success:
        print("\n🎉 一键打码完成!")
        print(f"📁 输出文件: {output_file}")
        sys.exit(0)
    else:
        print("\n💥 处理失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()