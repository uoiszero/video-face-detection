# 视频人脸检测工具

一个基于Python和OpenCV的视频人脸检测工具，可以检测视频文件中的人脸并生成带标注的输出视频。

## 功能特性

- 🎥 支持多种视频格式（MP4、AVI、MOV、MKV等）
- 👤 使用YuNet深度学习模型进行高精度人脸检测
- 📊 提供详细的检测统计信息
- 🖥️ 支持实时预览功能
- 💾 可选择保存带标注的输出视频
- 🔒 支持椭圆形人脸马赛克处理（隐私保护，更自然的遮挡效果）
- 📷 支持网络摄像头实时检测
- 🛠️ 简单易用的命令行界面
- 🧠 DeepFace集成：可选的高级人脸分析功能（年龄、性别、情绪、种族识别）

## 安装要求

### 系统要求
- Python 3.7+
- macOS / Linux / Windows

### 依赖库
- OpenCV (opencv-python)
- NumPy

## 安装步骤

1. **克隆或下载项目**
   ```bash
   cd /path/to/your/projects
   # 如果是从git克隆
   git clone <repository-url>
   cd video-face-detection
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

   或者手动安装：
   ```bash
   pip install opencv-python numpy
   ```

## 使用方法

### 命令行使用

#### 基本用法
```bash
# 仅检测，不保存结果
python main.py input_video.mp4

# 检测并保存结果视频
python main.py input_video.mp4 --output result_video.mp4

# 检测并显示实时预览
python main.py input_video.mp4 --preview

# 对人脸应用马赛克效果并保存
python main.py input_video.mp4 --mosaic --output mosaic_video.mp4

# 检测、保存并预览
python main.py input_video.mp4 --output result_video.mp4 --preview
```

#### 命令行参数
- `input_video`: 输入视频文件路径（必需）
- `--output, -o`: 输出视频文件路径（可选）
- `--preview, -p`: 显示实时预览窗口（可选）
- `--mosaic, -m`: 对检测到的人脸应用椭圆形马赛克效果（可选）
- `--mosaic-size`: 马赛克块大小，值越小马赛克越细腻（默认：15）
- `--model`: 自定义YuNet模型文件路径（可选）

#### 使用示例
```bash
# 处理名为 sample.mp4 的视频文件
python main.py sample.mp4 --output detected_faces.mp4 --preview

# 对人脸应用椭圆形马赛克效果
python main.py sample.mp4 --mosaic --output privacy_protected.mp4

# 使用细腻椭圆形马赛克效果并预览（自动启用抗抖动）
python main.py sample.mp4 --mosaic --mosaic-size 8 --preview

#### 测试抗抖动功能效果
```bash
python main.py input.mp4 --mosaic --output anti_jitter_test.mp4
```

### DeepFace高级分析功能
```bash
# 安装DeepFace（首次使用）
./install_deepface.sh

# 运行DeepFace分析演示
python demo_deepface_analysis.py

# 测试DeepFace检测器
python deepface_detector.py

# 使用混合检测器进行视频分析
python -c "from deepface_detector import HybridFaceDetector; detector = HybridFaceDetector(enable_deepface=True); print(detector.get_detector_info())"
```

### 编程接口使用

```python
from face_detector import VideoFaceDetector

# 创建检测器实例
detector = VideoFaceDetector()

# 处理视频文件（普通检测）
result = detector.process_video(
    input_path="input_video.mp4",
    output_path="output_video.mp4",
    show_preview=True
)

# 处理视频文件（马赛克模式）
result = detector.process_video(
    input_path="input_video.mp4",
    output_path="mosaic_video.mp4",
    show_preview=False,
    apply_mosaic=True,
    mosaic_size=15
)

# 查看检测结果统计
print(f"处理帧数: {result['processed_frames']}")
print(f"检测到人脸的帧数: {result['frames_with_faces']}")
print(f"总检测人脸数: {result['total_faces_detected']}")
print(f"检测率: {result['detection_rate']:.2%}")
```

### 运行示例代码

项目包含了完整的示例代码：

```bash
# 运行示例程序
python example.py
```

示例程序包括：
- 基础视频文件人脸检测
- 带实时预览的检测
- 马赛克人脸检测（隐私保护）
- 网络摄像头实时检测

## 项目结构

```
video-face-detection/
├── main.py              # 主程序入口
├── face_detector.py     # 人脸检测核心模块
├── example.py           # 示例代码
├── requirements.txt     # 项目依赖
└── README.md           # 使用说明
```

## 核心类说明

### VideoFaceDetector

主要的人脸检测器类，提供以下方法：

- `__init__(model_path=None)`: 初始化检测器，使用YuNet模型
- `detect_faces_in_frame(frame)`: 在单帧中检测人脸
- `draw_faces(frame, faces)`: 在图像上绘制检测框
- `apply_mosaic_to_faces(frame, faces, mosaic_size)`: 对人脸区域应用椭圆形马赛克效果
- `process_video()`: 返回详细的处理统计信息，包括处理时间和每秒处理帧数
- `process_video(input_path, output_path=None, show_preview=False, apply_mosaic=False, mosaic_size=15)`: 处理视频文件

## 检测参数调优

可以通过修改 `face_detector.py` 中的检测参数来优化检测效果：

```python
# 使用YuNet检测人脸
_, faces = self.detector.detect(frame)

# 转换检测结果格式
face_boxes = []
if faces is not None:
    for face in faces:
        x, y, w, h = face[:4].astype(int)
        face_boxes.append((x, y, w, h))
```

### 椭圆形马赛克技术

本项目采用椭圆形马赛克技术，相比传统的矩形马赛克具有以下优势：

**技术实现：**
```python
# 创建椭圆形遮罩
mask = np.zeros((h, w), dtype=np.uint8)
center_x, center_y = w // 2, h // 2
axis_x = int(w * 0.50)  # 水平半轴（扩大10%，从45%增加到50%）
axis_y = int(h * 0.66)  # 垂直半轴（扩大10%，从60%增加到66%）
cv2.ellipse(mask, (center_x, center_y), (axis_x, axis_y), 0, 0, 360, 255, -1)

# 应用椭圆形马赛克
mask_3d = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
blended_region = face_region * (1 - mask_3d) + mosaic_face * mask_3d
```

**优势特点：**
- 🎯 **更自然的遮挡效果**：椭圆形更贴合人脸轮廓
- 📏 **完整的面部遮挡**：面积扩大10%，确保完全覆盖面部特征
- 🔄 **渐变边缘**：避免生硬的矩形边界
- 🔒 **减少特征泄露**：更大的遮挡区域有效防止面部特征识别
- 🎯 **适应性强**：适应不同角度和大小的人脸
- 🎨 **视觉美观**：处理后的视频更加自然美观
- 🛡️ **抗抖动技术**：使用人脸跟踪算法减少马赛克闪烁和抖动现象

## 马赛克抗抖动技术

### 问题背景
在视频处理过程中，由于光照变化、人脸角度变化、遮挡等因素，某些帧可能无法检测到人脸，导致马赛克效果出现闪烁和抖动现象，影响视觉体验。

### 技术方案
- **历史帧跟踪**: 维护最近5帧的人脸位置历史记录
- **智能预测**: 当当前帧检测失败时，使用历史信息预测人脸位置
- **一致性检查**: 检查最近3帧的检测一致性，确保预测的可靠性
- **平滑过渡**: 在检测成功和失败之间提供平滑的马赛克过渡

### 算法逻辑
1. **检测成功**: 直接使用检测结果，更新历史记录
2. **检测失败**: 检查历史记录一致性
   - 如果最近3帧中至少2帧检测成功 → 使用最近一帧的位置
   - 否则 → 不应用马赛克，避免误判
3. **历史维护**: 保持5帧的滑动窗口，自动清理过期记录

### 效果优势
- ✨ **减少闪烁**: 显著减少马赛克的突然出现和消失
- 🎯 **保持连续性**: 在人脸检测不稳定时保持马赛克的连续性
- 🛡️ **避免误判**: 通过一致性检查避免在错误位置应用马赛克
- ⚡ **性能优化**: 轻量级算法，不影响处理速度

## DeepFace高级分析功能

### 功能概述
本项目集成了DeepFace框架，提供强大的人脸分析功能，超越基础的人脸检测，实现深度的人脸属性分析。

### 核心特性
- **多模型支持**: 集成VGG-Face、FaceNet、OpenFace、DeepFace等多种先进模型
- **属性分析**: 支持年龄估计、性别识别、情绪分析、种族识别
- **高精度识别**: 人脸识别准确率超过97.53%，达到人类水平
- **人脸比对**: 支持人脸相似度计算和身份验证
- **特征提取**: 提供高维人脸特征向量用于高级应用

### 安装方法

#### 基础安装
```bash
# 安装DeepFace及其依赖
pip install deepface

# 安装额外的深度学习框架（可选）
pip install tensorflow  # 或 pip install torch
```

#### 完整安装（推荐）
```bash
# 安装所有依赖，包括高级功能
pip install deepface[full]
pip install tensorflow-gpu  # 如果有GPU支持
```

### 使用示例

#### 基础人脸分析
```python
from deepface import DeepFace
import cv2

# 分析单张图片的人脸属性
result = DeepFace.analyze(
    img_path="face_image.jpg",
    actions=['age', 'gender', 'race', 'emotion']
)

print(f"年龄: {result['age']}")
print(f"性别: {result['gender']}")
print(f"情绪: {result['dominant_emotion']}")
print(f"种族: {result['dominant_race']}")
```

#### 人脸验证
```python
# 验证两个人脸是否属于同一人
result = DeepFace.verify(
    img1_path="person1.jpg",
    img2_path="person2.jpg",
    model_name="VGG-Face"
)

print(f"是否同一人: {result['verified']}")
print(f"相似度: {result['distance']}")
```

#### 视频流实时分析
```python
from face_detector import VideoFaceDetector
from deepface import DeepFace

# 创建增强版检测器
detector = VideoFaceDetector(enable_deepface=True)

# 处理视频并进行深度分析
result = detector.process_video_with_analysis(
    input_path="input_video.mp4",
    output_path="analyzed_video.mp4",
    analysis_actions=['age', 'gender', 'emotion']
)

# 查看分析统计
print(f"平均年龄: {result['avg_age']}")
print(f"性别分布: {result['gender_distribution']}")
print(f"主要情绪: {result['dominant_emotions']}")
```

### 技术架构
- **混合检测器**: 结合YuNet的高性能检测和DeepFace的深度分析
- **可选集成**: DeepFace作为可选功能，不影响核心检测性能
- **智能后端**: 支持多种检测后端（OpenCV、SSD、DLIB、MTCNN、RetinaFace）
- **统一接口**: 提供一致的API接口，便于功能切换和扩展

### 分析能力
1. **年龄估计**: 预测人脸年龄，误差约±4.65岁
2. **性别识别**: 识别性别，准确率97.44%
3. **情绪分析**: 识别7种情绪（愤怒、恐惧、中性、悲伤、厌恶、快乐、惊讶）
4. **种族识别**: 识别6种种族类别（亚洲、白人、中东、印度、拉丁、黑人）
5. **人脸验证**: 判断两个人脸是否属于同一人
6. **特征向量**: 提取高维人脸特征用于相似度计算

### 应用场景
- **智能监控**: 结合人脸检测和属性分析的综合监控方案
- **内容审核**: 基于人脸属性的智能内容过滤
- **用户分析**: 视频内容的观众群体分析
- **身份验证**: 高精度的人脸身份识别系统
- **情绪监测**: 实时情绪状态分析和反馈

### 性能优化建议
- **GPU加速**: 使用CUDA支持的GPU可显著提升分析速度
- **批量处理**: 对多个人脸同时进行分析以提高效率
- **模型选择**: 根据精度和速度需求选择合适的模型
- **缓存机制**: 对重复出现的人脸使用缓存减少计算量

## 性能统计功能

本项目提供详细的处理性能统计，帮助用户了解视频处理效率：

### 统计指标

- **处理时间**：完整视频处理所需的总时间
- **处理速度**：每秒处理的帧数（FPS）
- **平均每帧处理时间**：单帧处理的平均耗时
- **人脸检测率**：包含人脸的帧数占总帧数的比例

### 性能评估标准

- **优秀（≥30 FPS）**：可实时处理30fps视频
- **良好（≥15 FPS）**：可处理中等帧率视频
- **一般（≥5 FPS）**：适合离线处理
- **较慢（<5 FPS）**：需要优化处理算法

### YuNet模型参数说明
- `score_threshold`: 置信度阈值，默认0.9，值越高检测越严格
- `nms_threshold`: 非极大值抑制阈值，默认0.3，用于去除重叠检测框
- `input_size`: 输入图像尺寸，自动调整为视频帧尺寸
- `top_k`: 最大检测数量，默认5000

## 支持的视频格式

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- FLV (.flv)
- WMV (.wmv)
- M4V (.m4v)

## 常见问题

### Q: 检测效果不理想怎么办？
A: 可以尝试调整检测参数，或者使用更高质量的视频文件。光照条件和人脸角度会影响检测效果。

### Q: 处理大视频文件很慢？
A: 这是正常现象。可以考虑：
- 降低视频分辨率
- 调整检测参数提高速度
- 使用更快的硬件

### Q: 如何使用自定义的人脸检测模型？
A: 可以通过 `--model` 参数指定自定义的YuNet模型文件。项目默认使用 `models/face_detection_yunet_2023mar_int8bq.onnx` 模型。

### Q: 为什么输出视频文件比原始文件大很多？
A: 这主要由以下几个因素造成：
- **视频编码器差异**：程序会自动选择最佳的编码器（H.264 > avc1 > XVID > mp4v），不同编码器的压缩效率不同
- **重新编码过程**：视频处理需要解码后重新编码，可能会影响压缩效果
- **质量设置**：为保证处理后的视频质量，使用了较高的编码质量设置
- **帧处理**：每一帧都经过了人脸检测和图像处理，可能会影响压缩效率

**优化建议**：
- 程序已自动使用H.264编码器来减小文件大小
- 如需进一步压缩，可以使用专业的视频压缩工具对输出文件进行二次压缩

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！