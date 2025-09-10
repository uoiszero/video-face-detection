#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比马赛克抖动修复前后的效果
生成两个视频文件进行对比：一个使用抗抖动技术，一个不使用
"""

import os
import cv2
import numpy as np
from face_detector import VideoFaceDetector

class VideoFaceDetectorNoTracking(VideoFaceDetector):
    """
    不使用人脸跟踪的检测器（用于对比）
    """
    
    def __init__(self, model_path=None):
        """
        初始化检测器，但不启用跟踪功能
        """
        super().__init__(model_path)
        # 禁用跟踪功能
        self.tracking_enabled = False
    
    def process_video_no_tracking(self, input_path, output_path=None, show_preview=False, apply_mosaic=False, mosaic_size=15):
        """
        处理视频但不使用人脸跟踪（会产生抖动）
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入视频文件不存在: {input_path}")
        
        # 打开视频文件
        cap = cv2.VideoCapture(input_path)
        
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {input_path}")
        
        # 获取视频属性
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"视频信息: {width}x{height}, {fps}fps, 总帧数: {total_frames}")
        
        # 设置输出视频编码器
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            if not out.isOpened():
                raise ValueError(f"无法初始化视频编码器，请检查输出路径: {output_path}")
        
        # 统计信息
        processed_frames = 0
        frames_with_faces = 0
        total_faces_detected = 0
        
        print("开始处理视频（不使用抗抖动）...")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 直接检测人脸，不使用跟踪
                faces = self.detect_faces_in_frame(frame)
                
                # 应用马赛克效果
                if apply_mosaic:
                    result_frame = self.apply_mosaic_to_faces(frame, faces, mosaic_size)
                else:
                    result_frame = self.draw_faces(frame, faces)
                
                # 更新统计信息
                processed_frames += 1
                if len(faces) > 0:
                    frames_with_faces += 1
                    total_faces_detected += len(faces)
                
                # 保存到输出视频
                if out:
                    out.write(result_frame)
                
                # 显示进度
                if processed_frames % 30 == 0:
                    progress = (processed_frames / total_frames) * 100
                    print(f"处理进度: {progress:.1f}% ({processed_frames}/{total_frames})")
        
        finally:
            # 释放资源
            cap.release()
            if out:
                out.release()
        
        # 返回处理结果
        result = {
            'processed_frames': processed_frames,
            'frames_with_faces': frames_with_faces,
            'total_faces_detected': total_faces_detected,
            'detection_rate': frames_with_faces / processed_frames if processed_frames > 0 else 0
        }
        
        return result

def compare_jitter_fix():
    """
    对比马赛克抖动修复前后的效果
    """
    print("=== 马赛克抖动修复效果对比 ===")
    print("此测试将生成两个视频文件进行对比：")
    print("1. 使用抗抖动技术的视频")
    print("2. 不使用抗抖动技术的视频（会有抖动）\n")
    
    # 检查输入文件
    input_file = "input.mp4"
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 {input_file} 不存在")
        return False
    
    # 输出文件
    output_with_tracking = "mosaic_with_anti_jitter.mp4"
    output_without_tracking = "mosaic_with_jitter.mp4"
    
    try:
        print("🎬 第一步：生成使用抗抖动技术的视频")
        print(f"输出文件: {output_with_tracking}")
        
        # 创建带跟踪的检测器
        detector_with_tracking = VideoFaceDetector()
        
        result_with = detector_with_tracking.process_video(
            input_path=input_file,
            output_path=output_with_tracking,
            show_preview=False,
            apply_mosaic=True,
            mosaic_size=15
        )
        
        print(f"✅ 完成！检测率: {result_with['detection_rate']:.2%}")
        print(f"   处理速度: {result_with['fps_processed']:.2f}帧/秒\n")
        
        print("🎬 第二步：生成不使用抗抖动技术的视频（对比用）")
        print(f"输出文件: {output_without_tracking}")
        
        # 创建不带跟踪的检测器
        detector_without_tracking = VideoFaceDetectorNoTracking()
        
        result_without = detector_without_tracking.process_video_no_tracking(
            input_path=input_file,
            output_path=output_without_tracking,
            show_preview=False,
            apply_mosaic=True,
            mosaic_size=15
        )
        
        print(f"✅ 完成！检测率: {result_without['detection_rate']:.2%}\n")
        
        # 分析对比结果
        print("📊 对比分析:")
        print(f"   总帧数: {result_with['processed_frames']}")
        print(f"   检测到人脸的帧数: {result_with['frames_with_faces']}")
        print(f"   未检测到人脸的帧数: {result_with['processed_frames'] - result_with['frames_with_faces']}")
        
        undetected_frames = result_with['processed_frames'] - result_with['frames_with_faces']
        if undetected_frames > 0:
            print(f"\n🎯 预期效果差异:")
            print(f"   - {output_with_tracking}: 在{undetected_frames}个未检测帧中使用历史位置，马赛克连续")
            print(f"   - {output_without_tracking}: 在{undetected_frames}个未检测帧中无马赛克，会产生闪烁")
        
        print(f"\n🎉 对比视频生成完成！")
        print(f"请播放以下两个文件对比效果：")
        print(f"   1. {output_with_tracking} (抗抖动版本)")
        print(f"   2. {output_without_tracking} (原始版本，有抖动)")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理过程中出现错误: {str(e)}")
        return False

if __name__ == "__main__":
    success = compare_jitter_fix()
    if success:
        print("\n💡 观看建议：")
        print("   - 注意观察人脸区域马赛克的连续性")
        print("   - 对比两个视频中马赛克出现/消失的平滑度")
        print("   - 抗抖动版本应该显著减少马赛克闪烁现象")
    else:
        print("\n❌ 对比测试失败，请检查错误信息。")