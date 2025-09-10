#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFace人脸马赛克处理脚本
使用DeepFace进行人脸检测并应用马赛克效果
"""

import cv2
import numpy as np
import os
import sys
from deepface_detector import HybridFaceDetector

class DeepFaceMosaicProcessor:
    """使用DeepFace进行人脸检测和马赛克处理的类"""
    
    def __init__(self, mosaic_size=15):
        """
        初始化DeepFace马赛克处理器
        
        Args:
            mosaic_size (int): 马赛克块大小，默认15
        """
        self.mosaic_size = mosaic_size
        self.detector = HybridFaceDetector(primary_backend='deepface', enable_deepface=True)
        
    def apply_mosaic(self, image, x, y, w, h):
        """
        在指定区域应用马赛克效果
        
        Args:
            image: 输入图像
            x, y, w, h: 马赛克区域坐标和尺寸
            
        Returns:
            处理后的图像
        """
        # 确保坐标在图像范围内
        x = max(0, x)
        y = max(0, y)
        w = min(w, image.shape[1] - x)
        h = min(h, image.shape[0] - y)
        
        if w <= 0 or h <= 0:
            return image
            
        # 提取人脸区域
        face_region = image[y:y+h, x:x+w]
        
        # 计算马赛克后的尺寸
        mosaic_h = max(1, h // self.mosaic_size)
        mosaic_w = max(1, w // self.mosaic_size)
        
        # 缩小图像
        small_face = cv2.resize(face_region, (mosaic_w, mosaic_h))
        
        # 放大回原尺寸，产生马赛克效果
        mosaic_face = cv2.resize(small_face, (w, h), interpolation=cv2.INTER_NEAREST)
        
        # 将马赛克区域放回原图
        image[y:y+h, x:x+w] = mosaic_face
        
        return image
    
    def process_frame(self, frame):
        """
        处理单帧图像，检测人脸并应用马赛克
        
        Args:
            frame: 输入帧
            
        Returns:
            处理后的帧
        """
        # 使用DeepFace检测人脸
        faces = self.detector.detect_faces(frame)
        
        # 为每个检测到的人脸应用马赛克
        for face in faces:
            x, y, w, h = face['bbox']
            frame = self.apply_mosaic(frame, x, y, w, h)
            
        return frame
    
    def process_video(self, input_path, output_path):
        """
        处理视频文件，对所有人脸应用马赛克效果
        
        Args:
            input_path (str): 输入视频路径
            output_path (str): 输出视频路径
            
        Returns:
            bool: 处理是否成功
        """
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            print(f"错误：输入文件 {input_path} 不存在")
            return False
            
        # 打开视频文件
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"错误：无法打开视频文件 {input_path}")
            return False
            
        # 获取视频属性
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"视频信息：{width}x{height}, {fps}fps, 总帧数：{total_frames}")
        
        # 设置视频编码器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print(f"错误：无法创建输出视频文件 {output_path}")
            cap.release()
            return False
            
        frame_count = 0
        processed_faces = 0
        
        print("开始处理视频...")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                frame_count += 1
                
                # 处理当前帧
                processed_frame = self.process_frame(frame)
                
                # 统计检测到的人脸数量
                faces = self.detector.detect_faces(frame)
                processed_faces += len(faces)
                
                # 写入输出视频
                out.write(processed_frame)
                
                # 显示进度
                if frame_count % 30 == 0 or frame_count == total_frames:
                    progress = (frame_count / total_frames) * 100
                    print(f"处理进度：{frame_count}/{total_frames} ({progress:.1f}%)")
                    
        except KeyboardInterrupt:
            print("\n用户中断处理")
        except Exception as e:
            print(f"处理过程中发生错误：{e}")
            return False
        finally:
            # 释放资源
            cap.release()
            out.release()
            
        print(f"\n处理完成！")
        print(f"总帧数：{frame_count}")
        print(f"检测到的人脸总数：{processed_faces}")
        print(f"平均每帧人脸数：{processed_faces/frame_count:.2f}")
        print(f"输出文件：{output_path}")
        
        return True

def main():
    """
    主函数
    """
    input_file = "input.mp4"
    output_file = "deepface_mosaic_output.mp4"
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件 {input_file}")
        print("请确保 input.mp4 文件存在于当前目录中")
        return
        
    print("=== DeepFace人脸马赛克处理 ===")
    print(f"输入文件：{input_file}")
    print(f"输出文件：{output_file}")
    print()
    
    # 创建处理器
    processor = DeepFaceMosaicProcessor(mosaic_size=15)
    
    # 检查DeepFace是否可用
    if not processor.detector.enable_deepface:
        print("警告：DeepFace不可用，将使用YuNet进行人脸检测")
        print("要使用DeepFace，请运行：./install_deepface.sh")
        print()
    else:
        print("使用DeepFace进行人脸检测")
        print()
    
    # 处理视频
    success = processor.process_video(input_file, output_file)
    
    if success:
        print("\n✅ 马赛克处理完成！")
        print(f"输出文件已保存为：{output_file}")
    else:
        print("\n❌ 处理失败")
        sys.exit(1)

if __name__ == "__main__":
    main()