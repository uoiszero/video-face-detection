#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频处理性能测试脚本

此脚本用于测试和展示视频处理的性能指标，包括处理时间和每秒处理帧数
"""

import cv2
import numpy as np
from face_detector import VideoFaceDetector

def main():
    """
    主函数：测试视频处理性能
    """
    print("视频处理性能测试")
    print("=" * 50)
    
    # 初始化人脸检测器
    detector = VideoFaceDetector(model_path='models/face_detection_yunet_2023mar_int8bq.onnx')
    
    print("\n测试配置:")
    print("- 输入视频: input.mp4")
    print("- 椭圆形马赛克: 启用")
    print("- 马赛克块大小: 30")
    
    # 处理视频并记录性能
    print("\n开始性能测试...")
    stats = detector.process_video(
        input_path='input.mp4',
        output_path='performance_test_output.mp4',
        apply_mosaic=True,
        mosaic_size=30
    )
    
    print("\n=" * 50)
    print("性能测试结果")
    print("=" * 50)
    
    print("\n📊 处理统计:")
    print(f"   总处理帧数: {stats['processed_frames']}")
    print(f"   检测到人脸的帧数: {stats['frames_with_faces']}")
    print(f"   总检测人脸数: {stats['total_faces_detected']}")
    print(f"   人脸检测率: {stats['detection_rate']:.2%}")
    
    print("\n⏱️  性能指标:")
    print(f"   处理时间: {stats['processing_time']:.2f}秒")
    print(f"   处理速度: {stats['fps_processed']:.2f}帧/秒")
    
    # 计算额外的性能指标
    if stats['processed_frames'] > 0:
        avg_time_per_frame = stats['processing_time'] / stats['processed_frames']
        print(f"   平均每帧处理时间: {avg_time_per_frame*1000:.2f}毫秒")
    
    if stats['total_faces_detected'] > 0:
        avg_time_per_face = stats['processing_time'] / stats['total_faces_detected']
        print(f"   平均每个人脸处理时间: {avg_time_per_face*1000:.2f}毫秒")
    
    print("\n🚀 性能评估:")
    if stats['fps_processed'] >= 30:
        print("   ✅ 优秀 - 可实时处理30fps视频")
    elif stats['fps_processed'] >= 15:
        print("   ✅ 良好 - 可处理中等帧率视频")
    elif stats['fps_processed'] >= 5:
        print("   ⚠️  一般 - 适合离线处理")
    else:
        print("   ❌ 较慢 - 需要优化处理算法")
    
    print(f"\n输出文件: performance_test_output.mp4")
    print("性能测试完成!")

if __name__ == '__main__':
    main()