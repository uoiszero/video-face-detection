#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
椭圆形马赛克效果测试脚本

这个脚本演示了椭圆形马赛克与传统矩形马赛克的区别，
展示了更自然的人脸遮挡效果。
"""

import cv2
import numpy as np
from face_detector import VideoFaceDetector
import os

def create_comparison_demo():
    """
    创建椭圆形马赛克效果的对比演示
    """
    print("椭圆形马赛克效果演示")
    print("=" * 40)
    
    # 检查输入文件
    input_file = "input.mp4"
    if not os.path.exists(input_file):
        print(f"错误: 找不到输入文件 {input_file}")
        return
    
    # 初始化检测器
    print("初始化YuNet人脸检测器...")
    detector = VideoFaceDetector()
    
    # 处理视频 - 椭圆形马赛克
    print("\n正在生成椭圆形马赛克效果...")
    result = detector.process_video(
        input_path=input_file,
        output_path="demo_ellipse_mosaic.mp4",
        apply_mosaic=True,
        mosaic_size=20
    )
    
    print(f"\n椭圆形马赛克处理完成!")
    print(f"检测统计:")
    print(f"  - 总帧数: {result['processed_frames']}")
    print(f"  - 检测到人脸的帧数: {result['frames_with_faces']}")
    print(f"  - 总检测人脸数: {result['total_faces_detected']}")
    print(f"  - 人脸检测率: {result['detection_rate']:.2%}")
    
    # 检查输出文件大小
    if os.path.exists("demo_ellipse_mosaic.mp4"):
        file_size = os.path.getsize("demo_ellipse_mosaic.mp4") / (1024 * 1024)
        print(f"  - 输出文件大小: {file_size:.1f} MB")
    
    print("\n椭圆形马赛克的优势:")
    print("🎯 更自然的遮挡效果 - 椭圆形更贴合人脸轮廓")
    print("🔄 渐变边缘 - 避免生硬的矩形边界")
    print("👤 保留面部特征 - 只遮挡核心区域")
    print("🎨 视觉美观 - 处理后的视频更加自然")
    
    print(f"\n演示文件已保存: demo_ellipse_mosaic.mp4")
    print("您可以播放该文件查看椭圆形马赛克的效果!")

def main():
    """
    主函数
    """
    try:
        create_comparison_demo()
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())