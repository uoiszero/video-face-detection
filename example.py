#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频人脸检测示例代码
演示如何使用VideoFaceDetector类进行人脸检测
"""

from face_detector import VideoFaceDetector
import os

def example_basic_detection():
    """
    基础人脸检测示例
    """
    print("=== 基础人脸检测示例 ===")
    
    # 创建检测器实例
    detector = VideoFaceDetector()
    
    # 示例视频文件路径（请替换为实际的视频文件）
    input_video = "sample_video.mp4"
    output_video = "output_with_faces.mp4"
    
    # 检查输入文件是否存在
    if not os.path.exists(input_video):
        print(f"请将测试视频文件命名为 '{input_video}' 并放在当前目录下")
        print("或者修改此脚本中的文件路径")
        return
    
    try:
        # 处理视频（保存结果但不显示预览）
        result = detector.process_video(
            input_path=input_video,
            output_path=output_video,
            show_preview=False
        )
        
        print(f"检测完成! 结果已保存到: {output_video}")
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

def example_with_preview():
    """
    带实时预览的人脸检测示例
    """
    print("\n=== 带预览的人脸检测示例 ===")
    
    # 创建检测器实例
    detector = VideoFaceDetector()
    
    # 示例视频文件路径
    input_video = "sample_video.mp4"
    
    # 检查输入文件是否存在
    if not os.path.exists(input_video):
        print(f"请将测试视频文件命名为 '{input_video}' 并放在当前目录下")
        return
    
    try:
        print("开始处理视频，将显示实时预览窗口")
        print("按 'q' 键可以随时退出预览")
        
        # 处理视频（显示预览但不保存）
        result = detector.process_video(
            input_path=input_video,
            output_path=None,
            show_preview=True
        )
        
        print("预览结束")
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

def example_webcam_detection():
    """
    网络摄像头实时人脸检测示例
    """
    print("\n=== 网络摄像头实时检测示例 ===")
    
    import cv2
    
    # 创建检测器实例
    detector = VideoFaceDetector()
    
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    print("开始实时人脸检测，按 'q' 键退出")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 检测人脸
            faces = detector.detect_faces_in_frame(frame)
            
            # 绘制检测结果
            result_frame = detector.draw_faces(frame, faces)
            
            # 显示结果
            cv2.imshow('实时人脸检测', result_frame)
            
            # 按 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("摄像头检测结束")

def example_mosaic_detection():
    """
    马赛克人脸检测示例
    """
    print("\n=== 马赛克人脸检测示例 ===")
    
    # 创建检测器实例
    detector = VideoFaceDetector()
    
    # 示例视频文件路径
    input_video = "sample_video.mp4"
    output_video = "output_with_mosaic.mp4"
    
    # 检查输入文件是否存在
    if not os.path.exists(input_video):
        print(f"请将测试视频文件命名为 '{input_video}' 并放在当前目录下")
        return
    
    try:
        print("开始处理视频，将对检测到的人脸应用马赛克效果")
        
        # 处理视频（应用马赛克效果）
        result = detector.process_video(
            input_path=input_video,
            output_path=output_video,
            show_preview=False,
            apply_mosaic=True,
            mosaic_size=15
        )
        
        print(f"马赛克处理完成! 结果已保存到: {output_video}")
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

def main():
    """
    主函数，运行所有示例
    """
    print("视频人脸检测示例程序")
    print("=" * 50)
    
    # 运行基础检测示例
    example_basic_detection()
    
    # 询问用户是否要运行预览示例
    response = input("\n是否要运行带预览的检测示例? (y/n): ")
    if response.lower() in ['y', 'yes', '是']:
        example_with_preview()
    
    # 询问用户是否要运行马赛克示例
    response = input("\n是否要运行马赛克人脸检测示例? (y/n): ")
    if response.lower() in ['y', 'yes', '是']:
        example_mosaic_detection()
    
    # 询问用户是否要运行摄像头检测
    response = input("\n是否要运行摄像头实时检测? (y/n): ")
    if response.lower() in ['y', 'yes', '是']:
        example_webcam_detection()
    
    print("\n示例程序结束")

if __name__ == '__main__':
    main()