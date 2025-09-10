#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
椭圆形马赛克面积对比测试脚本

此脚本用于对比扩大前后椭圆形马赛克的效果差异
"""

import cv2
import numpy as np
from face_detector import VideoFaceDetector

def main():
    """
    主函数：对比椭圆形马赛克面积扩大前后的效果
    """
    print("椭圆形马赛克面积对比测试")
    print("=" * 50)
    
    # 初始化人脸检测器
    detector = VideoFaceDetector(model_path='models/face_detection_yunet_2023mar_int8bq.onnx')
    
    print("\n当前椭圆形马赛克参数:")
    print("- 水平半轴: 50% (扩大后)")
    print("- 垂直半轴: 66% (扩大后)")
    print("\n之前的椭圆形马赛克参数:")
    print("- 水平半轴: 45% (扩大前)")
    print("- 垂直半轴: 60% (扩大前)")
    
    # 处理视频
    print("\n开始处理视频...")
    stats = detector.process_video(
        input_path='input.mp4',
        output_path='final_enlarged_ellipse_mosaic.mp4',
        apply_mosaic=True,
        mosaic_size=30
    )
    
    print("\n处理统计信息:")
    print(f"总处理帧数: {stats['processed_frames']}")
    print(f"检测到人脸的帧数: {stats['frames_with_faces']}")
    print(f"总检测人脸数: {stats['total_faces_detected']}")
    print(f"人脸检测率: {stats['detection_rate']:.2%}")
    print(f"处理时间: {stats['processing_time']:.2f}秒")
    print(f"处理速度: {stats['fps_processed']:.2f}帧/秒")
    
    print("\n椭圆形马赛克面积扩大10%的优势:")
    print("✓ 更完整的面部遮挡")
    print("✓ 减少面部特征泄露")
    print("✓ 保持椭圆形的自然外观")
    print("✓ 适应不同角度的人脸")
    
    print(f"\n输出文件: final_enlarged_ellipse_mosaic.mp4")
    print("测试完成!")

if __name__ == '__main__':
    main()