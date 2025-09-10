#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFace人脸分析演示脚本
展示如何使用DeepFace进行人脸属性分析（年龄、性别、情绪、种族）
并与YuNet检测结果进行对比
"""

import cv2
import numpy as np
import os
import time
from typing import Dict, List

try:
    from deepface_detector import HybridFaceDetector, DEEPFACE_AVAILABLE
except ImportError:
    print("错误: 无法导入deepface_detector模块")
    exit(1)

def draw_analysis_results(frame: np.ndarray, faces: List, analysis: List) -> np.ndarray:
    """
    在图像上绘制人脸检测和分析结果
    
    Args:
        frame: 输入图像
        faces: 人脸检测结果
        analysis: 人脸分析结果
    
    Returns:
        绘制结果的图像
    """
    result_frame = frame.copy()
    
    for i, (x, y, w, h) in enumerate(faces):
        # 绘制人脸框
        cv2.rectangle(result_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 如果有分析结果，添加属性信息
        if i < len(analysis):
            face_analysis = analysis[i]
            
            # 准备文本信息
            texts = []
            
            # 年龄
            if 'age' in face_analysis:
                age = face_analysis['age']
                texts.append(f"Age: {age}")
            
            # 性别
            if 'gender' in face_analysis:
                gender_info = face_analysis['gender']
                if isinstance(gender_info, dict):
                    # 获取概率最高的性别
                    gender = max(gender_info.items(), key=lambda x: x[1])[0]
                    confidence = gender_info[gender]
                    texts.append(f"Gender: {gender} ({confidence:.1f}%)")
                else:
                    texts.append(f"Gender: {gender_info}")
            
            # 情绪
            if 'emotion' in face_analysis:
                emotion_info = face_analysis['emotion']
                if isinstance(emotion_info, dict):
                    # 获取概率最高的情绪
                    emotion = max(emotion_info.items(), key=lambda x: x[1])[0]
                    confidence = emotion_info[emotion]
                    texts.append(f"Emotion: {emotion} ({confidence:.1f}%)")
                else:
                    texts.append(f"Emotion: {emotion_info}")
            
            # 种族
            if 'race' in face_analysis:
                race_info = face_analysis['race']
                if isinstance(race_info, dict):
                    # 获取概率最高的种族
                    race = max(race_info.items(), key=lambda x: x[1])[0]
                    confidence = race_info[race]
                    texts.append(f"Race: {race} ({confidence:.1f}%)")
                else:
                    texts.append(f"Race: {race_info}")
            
            # 绘制文本信息
            text_y = y - 10
            for text in texts:
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                # 绘制背景矩形
                cv2.rectangle(result_frame, 
                            (x, text_y - text_size[1] - 5), 
                            (x + text_size[0] + 5, text_y + 5), 
                            (0, 0, 0), -1)
                # 绘制文本
                cv2.putText(result_frame, text, (x + 2, text_y), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                text_y -= (text_size[1] + 8)
    
    return result_frame

def analyze_video_with_deepface(input_path: str, output_path: str = None, max_frames: int = 100):
    """
    使用DeepFace分析视频中的人脸属性
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        max_frames: 最大处理帧数（用于演示）
    """
    if not DEEPFACE_AVAILABLE:
        print("错误: DeepFace不可用，请先安装: pip install deepface")
        return
    
    # 初始化混合检测器
    print("初始化混合检测器...")
    detector = HybridFaceDetector(
        primary_backend='yunet',  # 使用YuNet进行快速检测
        enable_deepface=True      # 启用DeepFace分析
    )
    
    # 显示检测器信息
    info = detector.get_detector_info()
    print("\n检测器配置:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # 打开视频文件
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"错误: 无法打开视频文件 {input_path}")
        return
    
    # 获取视频属性
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"\n视频信息:")
    print(f"  分辨率: {width}x{height}")
    print(f"  帧率: {fps} FPS")
    print(f"  总帧数: {total_frames}")
    print(f"  处理帧数: {min(max_frames, total_frames)}")
    
    # 设置输出视频编码器
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # 统计信息
    stats = {
        'processed_frames': 0,
        'faces_detected': 0,
        'faces_analyzed': 0,
        'analysis_time': 0,
        'detection_time': 0
    }
    
    print("\n开始处理视频...")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= max_frames:
            break
        
        frame_count += 1
        stats['processed_frames'] += 1
        
        # 检测和分析人脸
        start_time = time.time()
        
        # 使用混合检测器进行检测和分析
        result = detector.analyze_faces_with_attributes(frame)
        
        analysis_time = time.time() - start_time
        stats['analysis_time'] += analysis_time
        
        faces = result['faces']
        analysis = result['analysis']
        
        if faces:
            stats['faces_detected'] += len(faces)
            if analysis:
                stats['faces_analyzed'] += len(analysis)
        
        # 绘制结果
        if faces or analysis:
            result_frame = draw_analysis_results(frame, faces, analysis)
        else:
            result_frame = frame.copy()
            # 添加"未检测到人脸"文本
            cv2.putText(result_frame, "No faces detected", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 添加帧信息
        info_text = f"Frame: {frame_count}/{min(max_frames, total_frames)}"
        cv2.putText(result_frame, info_text, (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # 保存到输出视频
        if output_path:
            out.write(result_frame)
        
        # 显示进度
        if frame_count % 10 == 0:
            progress = (frame_count / min(max_frames, total_frames)) * 100
            print(f"  处理进度: {progress:.1f}% ({frame_count}/{min(max_frames, total_frames)})")
    
    # 释放资源
    cap.release()
    if output_path:
        out.release()
    
    # 显示统计信息
    print("\n=== 处理完成 ===")
    print(f"总处理帧数: {stats['processed_frames']}")
    print(f"检测到人脸数: {stats['faces_detected']}")
    print(f"分析人脸数: {stats['faces_analyzed']}")
    print(f"平均检测时间: {stats['analysis_time']/stats['processed_frames']:.3f}秒/帧")
    print(f"处理速度: {stats['processed_frames']/stats['analysis_time']:.1f} FPS")
    
    if output_path:
        print(f"输出视频已保存: {output_path}")

def compare_detection_methods(input_path: str, sample_frames: int = 10):
    """
    对比YuNet和DeepFace的检测性能
    
    Args:
        input_path: 输入视频路径
        sample_frames: 采样帧数
    """
    print("\n=== 检测方法对比 ===")
    
    # 打开视频
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"错误: 无法打开视频文件 {input_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(1, total_frames // sample_frames)
    
    # 初始化检测器
    yunet_detector = HybridFaceDetector(primary_backend='yunet', enable_deepface=False)
    
    if DEEPFACE_AVAILABLE:
        deepface_detector = HybridFaceDetector(primary_backend='deepface', enable_deepface=True)
    
    yunet_stats = {'time': 0, 'faces': 0, 'frames': 0}
    deepface_stats = {'time': 0, 'faces': 0, 'frames': 0}
    
    print(f"采样 {sample_frames} 帧进行对比...")
    
    for i in range(sample_frames):
        # 跳转到指定帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
        ret, frame = cap.read()
        if not ret:
            break
        
        # 测试YuNet
        start_time = time.time()
        yunet_faces = yunet_detector.detect_faces_in_frame(frame)
        yunet_time = time.time() - start_time
        
        yunet_stats['time'] += yunet_time
        yunet_stats['faces'] += len(yunet_faces)
        yunet_stats['frames'] += 1
        
        # 测试DeepFace（如果可用）
        if DEEPFACE_AVAILABLE:
            start_time = time.time()
            deepface_faces = deepface_detector.detect_faces_in_frame(frame)
            deepface_time = time.time() - start_time
            
            deepface_stats['time'] += deepface_time
            deepface_stats['faces'] += len(deepface_faces)
            deepface_stats['frames'] += 1
        
        print(f"  帧 {i+1}/{sample_frames}: YuNet={len(yunet_faces)}人脸 "
              f"({yunet_time:.3f}s)" + 
              (f", DeepFace={len(deepface_faces)}人脸 ({deepface_time:.3f}s)" 
               if DEEPFACE_AVAILABLE else ""))
    
    cap.release()
    
    # 显示对比结果
    print("\n=== 对比结果 ===")
    print(f"YuNet:")
    print(f"  平均检测时间: {yunet_stats['time']/yunet_stats['frames']:.3f}秒/帧")
    print(f"  平均检测速度: {yunet_stats['frames']/yunet_stats['time']:.1f} FPS")
    print(f"  总检测人脸: {yunet_stats['faces']}")
    print(f"  平均人脸数: {yunet_stats['faces']/yunet_stats['frames']:.1f}")
    
    if DEEPFACE_AVAILABLE:
        print(f"DeepFace:")
        print(f"  平均检测时间: {deepface_stats['time']/deepface_stats['frames']:.3f}秒/帧")
        print(f"  平均检测速度: {deepface_stats['frames']/deepface_stats['time']:.1f} FPS")
        print(f"  总检测人脸: {deepface_stats['faces']}")
        print(f"  平均人脸数: {deepface_stats['faces']/deepface_stats['frames']:.1f}")
        
        # 性能对比
        speed_ratio = (yunet_stats['frames']/yunet_stats['time']) / (deepface_stats['frames']/deepface_stats['time'])
        print(f"\n性能对比: YuNet比DeepFace快 {speed_ratio:.1f}x")
    else:
        print("DeepFace: 不可用")

def main():
    """
    主函数
    """
    input_video = "input.mp4"
    
    if not os.path.exists(input_video):
        print(f"错误: 找不到输入视频文件 {input_video}")
        print("请确保项目目录中有 input.mp4 文件")
        return
    
    print("DeepFace人脸分析演示")
    print("=" * 50)
    
    # 检查DeepFace可用性
    if DEEPFACE_AVAILABLE:
        print("✓ DeepFace可用")
        
        # 进行人脸属性分析演示
        print("\n1. 人脸属性分析演示")
        analyze_video_with_deepface(
            input_path=input_video,
            output_path="deepface_analysis_demo.mp4",
            max_frames=50  # 限制处理帧数以加快演示
        )
        
        # 对比检测方法
        print("\n2. 检测方法性能对比")
        compare_detection_methods(input_video, sample_frames=20)
        
    else:
        print("✗ DeepFace不可用")
        print("\n安装DeepFace以体验完整功能:")
        print("pip install deepface")
        print("\n注意: DeepFace首次使用时会自动下载模型文件，可能需要一些时间")
        
        # 仅使用YuNet进行演示
        print("\n使用YuNet进行基础检测演示")
        detector = HybridFaceDetector(primary_backend='yunet', enable_deepface=False)
        info = detector.get_detector_info()
        print("检测器配置:")
        for key, value in info.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()