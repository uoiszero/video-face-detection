#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试马赛克抖动修复功能
使用人脸跟踪技术减少视频中马赛克的抖动现象
"""

import os
from face_detector import VideoFaceDetector

def test_anti_jitter_mosaic():
    """
    测试修复马赛克抖动的功能
    """
    print("=== 马赛克抖动修复测试 ===")
    print("此测试将使用人脸跟踪技术来减少马赛克抖动")
    print("当某些帧检测不到人脸时，会使用历史帧信息保持马赛克连续性\n")
    
    # 检查输入文件
    input_file = "input.mp4"
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 {input_file} 不存在")
        return
    
    # 输出文件
    output_file = "anti_jitter_mosaic.mp4"
    
    try:
        # 创建检测器实例
        detector = VideoFaceDetector()
        
        print(f"输入文件: {input_file}")
        print(f"输出文件: {output_file}")
        print("开始处理...\n")
        
        # 处理视频，应用马赛克效果
        result = detector.process_video(
            input_path=input_file,
            output_path=output_file,
            show_preview=False,
            apply_mosaic=True,
            mosaic_size=15
        )
        
        print("\n=== 处理结果 ===")
        print(f"✅ 成功生成防抖动马赛克视频: {output_file}")
        print(f"📊 处理统计:")
        print(f"   - 总帧数: {result['processed_frames']}")
        print(f"   - 检测到人脸的帧数: {result['frames_with_faces']}")
        print(f"   - 人脸检测率: {result['detection_rate']:.2%}")
        print(f"   - 处理时间: {result['processing_time']:.2f}秒")
        print(f"   - 处理速度: {result['fps_processed']:.2f}帧/秒")
        
        # 计算改进效果
        undetected_frames = result['processed_frames'] - result['frames_with_faces']
        if undetected_frames > 0:
            print(f"\n🎯 抖动修复效果:")
            print(f"   - 未检测到人脸的帧数: {undetected_frames}")
            print(f"   - 这些帧现在会使用历史信息保持马赛克连续性")
            print(f"   - 预期减少马赛克抖动现象")
        else:
            print(f"\n✨ 所有帧都检测到了人脸，马赛克效果本身就很稳定")
            
        print(f"\n💡 技术说明:")
        print(f"   - 使用5帧历史记录进行人脸跟踪")
        print(f"   - 当检测失败时，如果最近3帧中有2帧检测成功，则使用历史位置")
        print(f"   - 这样可以显著减少马赛克的突然出现和消失")
        
    except Exception as e:
        print(f"❌ 处理过程中出现错误: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_anti_jitter_mosaic()
    if success:
        print("\n🎉 测试完成！请查看生成的视频文件对比效果。")
    else:
        print("\n❌ 测试失败，请检查错误信息。")