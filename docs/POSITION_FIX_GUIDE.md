# 人脸位置不重合问题修复指南

## 问题描述

用户反馈使用 `--preview` 命令获得的预览和 `--mosaic` 命令的打码位置不重合，导致预览时看到的人脸检测框与实际马赛克位置不一致。

## 问题分析

经过深入分析，发现问题出现在两个方面：

### 1. 人脸跟踪算法不一致

**原始问题：**
- 预览模式直接使用 `detect_faces_in_frame()` 的原始检测结果
- 马赛克模式使用 `track_faces_with_history()` 进行人脸跟踪平滑处理
- 两种模式使用不同的人脸位置数据，导致位置不一致

**解决方案：**
```python
# 修改前：两种模式使用不同的人脸数据
if apply_mosaic:
    faces = self.track_faces_with_history(detected_faces)  # 使用跟踪
    result_frame = self.apply_mosaic_to_faces(frame, faces, mosaic_size)
else:
    faces = detected_faces  # 直接使用检测结果
    result_frame = self.draw_faces(frame, faces)

# 修改后：两种模式统一使用跟踪算法
faces = self.track_faces_with_history(detected_faces)  # 统一使用跟踪
if apply_mosaic:
    result_frame = self.apply_mosaic_to_faces(frame, faces, mosaic_size)
else:
    result_frame = self.draw_faces(frame, faces)
```

### 2. 坐标缩放不一致

**原始问题：**
- `draw_faces()` 方法直接使用原始坐标绘制检测框
- `apply_mosaic_to_faces()` 方法将坐标缩小到 0.9 倍
- 坐标处理不一致导致位置偏移

**解决方案：**
```python
# 修改前：马赛克模式缩小坐标
x = max(0, int(x * 0.9))  # 缩小到90%
y = max(0, int(y * 0.9))  # 缩小到90%

# 修改后：保持原始坐标
x = max(0, x)  # 保持原始坐标
y = max(0, y)  # 保持原始坐标
```

## 修复文件

主要修改了 `face_detector.py` 文件中的以下方法：

1. **`process_video()` 方法**：统一两种模式的人脸跟踪逻辑
2. **`apply_mosaic_to_faces()` 方法**：移除坐标缩放，保持与预览模式一致

## 测试验证

修复后生成的测试文件：
- `fixed_preview_test.mp4` - 修复后的预览模式输出
- `fixed_mosaic_test.mp4` - 修复后的马赛克模式输出

两个文件中的人脸位置现在应该完全重合。

## 技术要点

### 人脸跟踪算法的作用

`track_faces_with_history()` 方法通过以下机制减少检测抖动：

1. **历史记录维护**：保存最近几帧的人脸检测结果
2. **连续性检查**：当前帧未检测到人脸时，检查历史记录的一致性
3. **位置预测**：基于历史位置预测当前帧的人脸位置
4. **平滑过渡**：避免因单帧检测失败导致的马赛克闪烁

### 椭圆形马赛克的优势

相比矩形马赛克，椭圆形马赛克具有以下优势：

1. **更自然的遮挡效果**：符合人脸的自然轮廓
2. **更好的视觉体验**：边缘过渡更平滑
3. **精确的遮挡范围**：只遮挡面部关键区域

## 使用建议

1. **预览测试**：在生成最终马赛克视频前，先使用 `--preview` 模式确认检测效果
2. **参数调整**：根据视频质量调整马赛克块大小 `--mosaic-size`
3. **性能优化**：对于长视频，建议先测试短片段确认效果

## 相关文件

- `face_detector.py` - 核心人脸检测和处理逻辑
- `main.py` - 命令行接口和参数处理
- `deepface_detector.py` - DeepFace 集成支持

修复完成后，预览模式和马赛克模式将使用完全一致的人脸位置检测和跟踪算法，确保位置完美重合。