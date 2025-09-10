#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频人脸检测主程序
用于从命令行运行视频人脸检测功能

使用方法:
    python main.py input_video.mp4 [--output output_video.mp4] [--preview]
"""

import argparse
import sys
import os
from face_detector import VideoFaceDetector
try:
    from deepface_detector import HybridFaceDetector
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False

def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        description='视频人脸检测工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py video.mp4                           # 使用YuNet检测器，仅检测不保存(已优化侧脸检测,延续打码5帧)
  python main.py video.mp4 --output result.mp4      # 检测并保存结果视频
  python main.py video.mp4 --preview                # 检测并显示实时预览
  python main.py video.mp4 --detector deepface --deepface-backend mtcnn      # 使用DeepFace检测器(MTCNN后端,适合侧脸)
  python main.py video.mp4 --detector deepface --deepface-backend retinaface # 使用DeepFace检测器(RetinaFace后端,适合侧脸)
  python main.py video.mp4 --detector hybrid --deepface-backend mtcnn        # 使用混合检测器（YuNet+DeepFace）
  python main.py video.mp4 --mosaic --output mosaic.mp4  # 应用马赛克并保存
  python main.py video.mp4 --mosaic --mosaic-size 10 --preview  # 细腻马赛克预览
  python main.py video.mp4 --continuation-frames 10 --mosaic --output output.mp4  # 延续打码10帧策略
        """
    )
    
    parser.add_argument(
        'input_video',
        help='输入视频文件路径'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='输出视频文件路径（可选）'
    )
    
    parser.add_argument(
        '--preview', '-p',
        action='store_true',
        help='显示实时预览窗口'
    )
    
    parser.add_argument(
        '--model',
        help='自定义YuNet模型文件路径（可选）'
    )
    
    parser.add_argument(
        '--mosaic', '-m',
        action='store_true',
        help='对检测到的人脸应用马赛克效果（隐私保护）'
    )
    
    parser.add_argument(
        '--mosaic-size',
        type=int,
        default=30,
        help='马赛克块大小，值越小马赛克越细腻（默认：30）'
    )
    
    parser.add_argument(
        '--detector',
        choices=['yunet', 'deepface', 'hybrid'],
        default='yunet',
        help='选择人脸检测器：yunet（默认，快速）、deepface（高精度）、hybrid（混合模式）'
    )
    
    parser.add_argument(
        '--deepface-backend',
        choices=['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface'],
        default='mtcnn',
        help='DeepFace检测后端（仅在使用deepface或hybrid时有效）：opencv、ssd、dlib、mtcnn（默认，推荐）、retinaface（推荐）'
    )
    
    parser.add_argument(
        '--continuation-frames',
        type=int,
        default=5,
        help='无人脸检测时延续打码的帧数（默认：5帧）'
    )
    
    return parser.parse_args()

def validate_input(args):
    """
    验证输入参数
    
    Args:
        args (argparse.Namespace): 命令行参数
        
    Returns:
        bool: 验证是否通过
    """
    # 检查输入文件是否存在
    if not os.path.exists(args.input_video):
        print(f"错误: 输入视频文件不存在: {args.input_video}")
        return False
    
    # 检查输入文件是否为视频格式
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v']
    input_ext = os.path.splitext(args.input_video)[1].lower()
    if input_ext not in video_extensions:
        print(f"警告: 输入文件可能不是支持的视频格式: {input_ext}")
        print(f"支持的格式: {', '.join(video_extensions)}")
    
    # 检查输出目录是否存在
    if args.output:
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            print(f"错误: 输出目录不存在: {output_dir}")
            return False
    
    # 检查自定义模型文件
    if args.model and not os.path.exists(args.model):
        print(f"错误: YuNet模型文件不存在: {args.model}")
        return False
    
    return True

def main():
    """
    主函数
    """
    print("视频人脸检测工具 v1.0")
    print("=" * 40)
    
    # 解析命令行参数
    args = parse_arguments()
    
    # 验证输入参数
    if not validate_input(args):
        sys.exit(1)
    
    try:
        # 创建人脸检测器
        if args.detector == 'yunet':
            print("初始化YuNet人脸检测器...")
            detector = VideoFaceDetector(model_path=args.model, continuation_frames=args.continuation_frames)
        elif args.detector == 'deepface':
            if not DEEPFACE_AVAILABLE:
                print("错误: DeepFace不可用，请先安装DeepFace或选择其他检测器")
                print("安装命令: pip install deepface")
                sys.exit(1)
            print(f"初始化DeepFace检测器 - 后端: {args.deepface_backend}...")
            detector = HybridFaceDetector(primary_backend=args.deepface_backend, enable_deepface=True, continuation_frames=args.continuation_frames)
        elif args.detector == 'hybrid':
            if not DEEPFACE_AVAILABLE:
                print("错误: DeepFace不可用，回退到YuNet检测器")
                detector = VideoFaceDetector(model_path=args.model, continuation_frames=args.continuation_frames)
            else:
                print(f"初始化混合检测器（YuNet + DeepFace） - DeepFace后端: {args.deepface_backend}...")
                detector = HybridFaceDetector(primary_backend='yunet', enable_deepface=True, deepface_backend=args.deepface_backend, continuation_frames=args.continuation_frames)
        else:
            print("错误: 未知的检测器类型")
            sys.exit(1)
        
        # 处理视频
        print(f"输入视频: {args.input_video}")
        if args.output:
            print(f"输出视频: {args.output}")
        if args.preview:
            print("实时预览: 启用 (按 'q' 键退出预览)")
        if args.mosaic:
            print(f"马赛克模式: 启用 (块大小: {args.mosaic_size})")
        
        print("\n开始处理...")
        result = detector.process_video(
            input_path=args.input_video,
            output_path=args.output,
            show_preview=args.preview,
            apply_mosaic=args.mosaic,
            mosaic_size=args.mosaic_size
        )
        
        # 显示处理结果摘要
        print("\n" + "=" * 40)
        print("处理完成!")
        
        if args.output and os.path.exists(args.output):
            output_size = os.path.getsize(args.output) / (1024 * 1024)  # MB
            print(f"输出文件已保存: {args.output} ({output_size:.1f} MB)")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()