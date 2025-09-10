#!/usr/bin/env python3
"""
测试GUI后端功能
用于验证HybridFaceDetector和进度回调是否正常工作
"""

import sys
import os
from pathlib import Path

# 导入检测器
from face_detector import VideoFaceDetector
try:
    from deepface_detector import HybridFaceDetector
    HYBRID_AVAILABLE = True
    print("✓ HybridFaceDetector 可用")
except ImportError as e:
    HYBRID_AVAILABLE = False
    print(f"✗ HybridFaceDetector 不可用: {e}")

def test_progress_callback():
    """测试进度回调功能"""
    print("\n=== 测试进度回调功能 ===")
    
    # 创建进度回调函数
    def progress_callback(processed_frames, total_frames=None):
        if total_frames:
            print(f"进度更新: 已处理 {processed_frames}/{total_frames} 帧")
        else:
            print(f"进度更新: 已处理 {processed_frames} 帧")
        return True  # 继续处理
    
    # 测试YuNet检测器
    print("\n1. 测试 YuNet 检测器")
    detector = VideoFaceDetector()
    
    # 检查输入文件是否存在
    input_file = "input.mp4"
    if not os.path.exists(input_file):
        print(f"✗ 输入文件 {input_file} 不存在")
        return False
    
    try:
        result = detector.process_video(
            input_file, 
            "test_yunet_progress.mp4",
            show_preview=False,
            apply_mosaic=False,
            progress_callback=progress_callback
        )
        print(f"✓ YuNet 处理完成: {result}")
    except Exception as e:
        print(f"✗ YuNet 处理失败: {e}")
        return False
    
    # 测试HybridFaceDetector（如果可用）
    if HYBRID_AVAILABLE:
        print("\n2. 测试 HybridFaceDetector (YuNet模式)")
        try:
            hybrid_detector = HybridFaceDetector(
                primary_backend='yunet',
                enable_deepface=False
            )
            
            result = hybrid_detector.process_video(
                input_file,
                "test_hybrid_yunet_progress.mp4",
                show_preview=False,
                apply_mosaic=False,
                progress_callback=progress_callback
            )
            print(f"✓ HybridFaceDetector (YuNet) 处理完成: {result}")
        except Exception as e:
            print(f"✗ HybridFaceDetector (YuNet) 处理失败: {e}")
            return False
        
        print("\n3. 测试 HybridFaceDetector (DeepFace模式)")
        try:
            hybrid_detector_df = HybridFaceDetector(
                primary_backend='deepface',
                enable_deepface=True
            )
            
            result = hybrid_detector_df.process_video(
                input_file,
                "test_hybrid_deepface_progress.mp4",
                show_preview=False,
                apply_mosaic=False,
                progress_callback=progress_callback
            )
            print(f"✓ HybridFaceDetector (DeepFace) 处理完成: {result}")
        except Exception as e:
            print(f"✗ HybridFaceDetector (DeepFace) 处理失败: {e}")
            print("注意: DeepFace模式可能需要额外的依赖")
    
    return True

def test_detector_info():
    """测试检测器信息获取"""
    print("\n=== 测试检测器信息 ===")
    
    # 测试YuNet检测器
    print("\n1. YuNet 检测器信息")
    detector = VideoFaceDetector()
    print(f"检测器类型: {type(detector).__name__}")
    
    # 测试HybridFaceDetector（如果可用）
    if HYBRID_AVAILABLE:
        print("\n2. HybridFaceDetector 信息")
        try:
            hybrid_detector = HybridFaceDetector(
                primary_backend='yunet',
                enable_deepface=False
            )
            info = hybrid_detector.get_detector_info()
            print("检测器配置:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"✗ 获取HybridFaceDetector信息失败: {e}")

def main():
    """主函数"""
    print("GUI后端功能测试")
    print("=" * 50)
    
    # 检查当前目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python版本: {sys.version}")
    
    # 测试检测器信息
    test_detector_info()
    
    # 测试进度回调功能
    if os.path.exists("input.mp4"):
        test_progress_callback()
    else:
        print("\n⚠️  跳过视频处理测试: input.mp4 文件不存在")
        print("如需测试视频处理功能，请确保 input.mp4 文件存在")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()