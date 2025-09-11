# 视频人脸检测工具

一个基于Python和OpenCV的视频人脸检测工具，可以检测视频文件中的人脸并生成带标注的输出视频。

## 功能特性

### 🎯 核心功能
- 🎥 支持多种视频格式（MP4、AVI、MOV、MKV等）
- 👤 使用YuNet深度学习模型进行高精度人脸检测
- 🔄 **侧脸检测优化**：多尺度检测技术，显著提升侧脸和困难角度的检测效果
- 🎯 **延续打码策略**：智能跟踪算法，在检测失败时自动延续打码，避免闪烁
- 📊 提供详细的检测统计信息
- 🖥️ 支持实时预览功能
- 💾 可选择保存带标注的输出视频
- 🔒 支持椭圆形人脸马赛克处理（隐私保护，更自然的遮挡效果）
- 📷 支持网络摄像头实时检测
- 🛠️ 简单易用的命令行界面
- 🧠 **DeepFace集成**：多后端支持（MTCNN、RetinaFace等），可选的高级人脸分析功能
- 🔀 **混合检测器**：结合YuNet和DeepFace的优势，提供最佳检测效果

### 🎨 图形界面功能
- **现代化界面**: 基于PyQt5的美观用户界面
- **可视化操作**: 通过鼠标点击完成所有操作，无需命令行
- **实时进度显示**: 图形化进度条和详细处理日志
- **文件浏览器**: 便捷的文件选择和路径管理
- **参数可视化**: 滑块和下拉菜单直观设置参数
- **多检测器支持**: 支持hybrid、yunet、retinaface等多种检测器
- **多种输出模式**: 支持马赛克、模糊、黑框等多种处理效果

## 技术特性

### 侧脸检测优化
本项目采用多尺度检测技术，显著提升侧脸和困难角度的人脸检测效果：
- **多尺度检测**：使用不同尺度的检测窗口，提高小脸和远距离人脸的检测率
- **DeepFace集成**：支持MTCNN、RetinaFace等先进检测后端，专门优化侧脸检测
- **混合检测器**：结合YuNet的速度优势和DeepFace的精度优势
- **角度适应**：对各种头部姿态（正脸、侧脸、仰头、低头）都有良好的检测效果

### 延续打码策略
智能跟踪算法确保打码的连续性和稳定性：
- **智能延续**：当检测失败时，使用最后检测到的人脸位置继续打码
- **可配置帧数**：通过 `--continuation-frames` 参数自定义延续帧数（默认5帧）
- **历史信息利用**：分析最近3帧的检测历史，提供更准确的延续位置
- **进度提示**：控制台显示延续打码的详细信息和统计数据

### 椭圆形马赛克处理
本项目采用椭圆形马赛克技术，相比传统的矩形马赛克，提供更自然的人脸遮挡效果：
- **自适应椭圆形状**：根据检测到的人脸区域自动调整椭圆大小和形状
- **可调节马赛克粒度**：通过 `--mosaic-size` 参数控制马赛克块大小（默认15像素）
- **边缘平滑处理**：椭圆边缘采用渐变过渡，避免生硬的边界效果
- **隐私保护优化**：椭圆形状更贴合人脸轮廓，在保护隐私的同时保持画面美观

### 抗抖动技术
为了解决视频中人脸检测可能出现的抖动问题，本项目实现了智能抗抖动算法：
- **位置平滑**：对连续帧中的人脸位置进行平滑处理
- **尺寸稳定**：避免马赛克区域大小的突然变化
- **自动启用**：使用马赛克功能时自动启用抗抖动
- **实时优化**：在保持检测精度的同时提供稳定的视觉效果

## 性能优化建议

### 检测器选择策略
- **实时预览**：使用YuNet检测器（`--detector yunet`）
- **侧脸较多**：使用DeepFace + MTCNN（`--detector deepface --deepface-backend mtcnn`）
- **最佳效果**：使用混合检测器（`--detector hybrid --deepface-backend retinaface`）
- **资源受限**：使用YuNet + 较少延续帧数（`--continuation-frames 3`）

### 延续打码参数调优
- **快速运动场景**：增加延续帧数（`--continuation-frames 10-15`）
- **静态场景**：使用默认值（`--continuation-frames 5`）
- **实时处理**：减少延续帧数（`--continuation-frames 3`）

### 马赛克效果优化
- **高清视频**：使用较小马赛克块（`--mosaic-size 8-12`）
- **标清视频**：使用默认值（`--mosaic-size 15`）
- **快速处理**：使用较大马赛克块（`--mosaic-size 20-25`）

## 安装要求

### 系统要求
- Python 3.8+
- OpenCV 4.8+
- NumPy 1.21+
- DeepFace 0.0.79+
- TensorFlow 2.12+
- MTCNN 0.1.1+
- RetinaFace 0.0.13+
- macOS / Linux / Windows

### GUI界面依赖

```bash
# 安装PyQt5
pip install PyQt5
```

## 🚀 快速安装

### 一键安装脚本（推荐）

本项目提供了多种自动安装脚本，可以一次性安装所有依赖：

```bash
# 克隆项目
git clone <repository-url>
cd video-face-detection

# 方式一：Python安装脚本（跨平台推荐）
python3 install_dependencies.py

# 方式二：Shell脚本（macOS/Linux）
chmod +x scripts/install.sh
./scripts/install.sh

# 方式三：批处理脚本（Windows）
scripts\install.bat
```

**安装脚本功能：**
- ✅ 自动检测Python环境
- ✅ 安装所有必需的Python包
- ✅ 下载YuNet模型文件
- ✅ 验证安装结果
- ✅ 提供详细的安装日志

### 手动安装

如果自动安装脚本失败，可以手动安装：

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 创建模型目录并下载模型文件
mkdir -p models
cd models
wget https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
cd ..
```

详细安装说明请参考 [docs/INSTALL.md](docs/INSTALL.md) 文档。

## 使用方法

### 🎨 GUI图形界面（推荐）

项目提供了基于PyQt5的现代化图形用户界面，让您无需使用命令行即可轻松处理视频：

```bash
python gui_mosaic_pyqt.py
```

**功能特性：**
- 🎨 现代化界面：基于PyQt5的美观界面
- 🔄 多检测器支持：hybrid、yunet、retinaface等
- 👤 侧脸检测：专门的侧脸检测器选择
- 🎭 输出模式：支持马赛克、模糊、黑框等多种效果
- ⚡ 延续帧数：智能的人脸跟踪优化
- 📋 实时日志：详细的处理过程显示

### 🚀 一键打码（推荐）

最简单的使用方式，使用优化配置进行视频打码：

```bash
# Python版本（跨平台）
python quick_mosaic.py input_video.mp4

# Shell版本（macOS/Linux）
chmod +x scripts/quick_mosaic.sh
./scripts/quick_mosaic.sh input_video.mp4

# 批处理版本（Windows）
scripts\quick_mosaic.bat input_video.mp4
```

**一键打码特性：**
- ✅ 混合检测器（YuNet + DeepFace）
- ✅ 侧脸检测优化（RetinaFace后端）
- ✅ 延续打码（15帧）
- ✅ 自动生成输出文件名（原文件名_out_时间戳.扩展名）
- ✅ 智能依赖检查和错误处理

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
- `--detector`: 选择检测器类型（yunet、deepface、hybrid）
- `--deepface-backend`: DeepFace检测后端（opencv、ssd、dlib、mtcnn、retinaface）
- `--continuation-frames`: 无人脸检测时延续打码的帧数（默认：5帧）

#### 使用示例
```bash
# 基础检测（已优化侧脸检测，延续打码5帧）
python main.py sample.mp4 --output detected_faces.mp4 --preview

# 对人脸应用椭圆形马赛克效果
python main.py sample.mp4 --mosaic --output privacy_protected.mp4

# 使用细腻椭圆形马赛克效果并预览（自动启用抗抖动）
python main.py sample.mp4 --mosaic --mosaic-size 8 --preview

# 使用DeepFace检测器进行侧脸检测（推荐MTCNN后端）
python main.py sample.mp4 --detector deepface --deepface-backend mtcnn --mosaic

# 使用混合检测器（YuNet + DeepFace）获得最佳效果
python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic

# 自定义延续打码策略（延续10帧）
python main.py sample.mp4 --continuation-frames 10 --mosaic --output output.mp4
```

## 检测器选择指南

本项目提供三种检测器类型，适用于不同的使用场景：

### YuNet 检测器（默认）
- **优势**：速度快，资源占用低，适合实时处理
- **适用场景**：正脸检测，实时预览，资源受限环境
- **使用方法**：`--detector yunet`（默认，可省略）

### DeepFace 检测器
- **优势**：侧脸检测效果优秀，支持多种后端
- **适用场景**：侧脸较多的视频，高精度要求
- **推荐后端**：
  - `mtcnn`：侧脸检测效果最佳
  - `retinaface`：综合性能优秀
  - `opencv`：速度最快（默认）
- **使用方法**：`--detector deepface --deepface-backend mtcnn`

### 混合检测器（推荐）
- **优势**：结合两种检测器的优势，检测效果最佳
- **适用场景**：复杂场景，多角度人脸，高质量要求
- **工作原理**：YuNet快速检测 + DeepFace补充检测
- **使用方法**：`--detector hybrid --deepface-backend retinaface`

## DeepFace 集成功能

本项目集成了 DeepFace 库，提供高级人脸分析和检测功能。

### 检测后端支持
- **OpenCV**：速度最快，基础检测效果
- **SSD**：平衡速度和精度
- **Dlib**：传统机器学习方法，稳定可靠
- **MTCNN**：多任务CNN，侧脸检测效果优秀
- **RetinaFace**：最新技术，综合性能最佳

### 使用方法
```bash
# 使用MTCNN后端进行侧脸检测
python main.py sample.mp4 --detector deepface --deepface-backend mtcnn --mosaic

# 使用混合检测器获得最佳效果
python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic

# 自定义延续打码策略
python main.py sample.mp4 --continuation-frames 10 --mosaic
```

### 注意事项
- DeepFace 检测会增加处理时间，但检测效果更好
- 首次使用时会自动下载必要的模型文件
- 混合检测器提供最佳的检测覆盖率和稳定性

## 故障排除

### 常见问题

#### 1. 侧脸检测效果不佳
**解决方案**：
```bash
# 使用MTCNN后端，专门优化侧脸检测
python main.py sample.mp4 --detector deepface --deepface-backend mtcnn --mosaic

# 或使用混合检测器获得最佳效果
python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic
```

#### 2. 打码出现闪烁或不连续
**解决方案**：
```bash
# 增加延续打码帧数
python main.py sample.mp4 --continuation-frames 10 --mosaic

# 对于快速运动场景，可以进一步增加
python main.py sample.mp4 --continuation-frames 15 --mosaic
```

#### 3. 处理速度过慢
**解决方案**：
```bash
# 使用默认YuNet检测器（最快）
python main.py sample.mp4 --detector yunet --mosaic

# 减少延续帧数
python main.py sample.mp4 --continuation-frames 3 --mosaic

# 增大马赛克块大小
python main.py sample.mp4 --mosaic-size 20 --mosaic
```

#### 4. 小脸或远距离人脸检测不到
**解决方案**：
```bash
# 使用混合检测器，提高检测覆盖率
python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic
```

### 控制台信息说明
- `延续打码`: 表示正在使用历史位置进行打码
- `检测到 X 个人脸`: 当前帧的检测结果
- `使用历史信息延续打码`: 分析历史帧进行智能延续
- `清空人脸历史`: 超过延续帧数限制，重置跟踪状态

### DeepFace高级分析功能
```bash
# 安装DeepFace（首次使用）
./scripts/install_deepface.sh

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
├── main.py                    # 主程序入口（命令行版本）
├── face_detector.py           # YuNet人脸检测核心模块
├── deepface_detector.py       # DeepFace集成模块
├── gui_mosaic_pyqt.py         # PyQt5版本GUI应用
├── quick_mosaic.py            # 一键打码脚本（Python）
├── scripts/                   # 脚本文件目录
│   ├── quick_mosaic.sh        # 一键打码脚本（Shell）
│   └── quick_mosaic.bat       # 一键打码脚本（Windows）
├── models/                    # 模型文件目录
│   └── face_detection_yunet_2023mar.onnx
├── requirements.txt           # 依赖包列表
├── docs/                    # 文档目录
│   ├── INSTALL.md             # 安装指南
│   ├── QUICK_START.md         # 快速开始指南
│   ├── CONTINUATION_FRAMES_DEBUG.md # 延续打码调试文档
│   ├── GUI_USAGE_GUIDE.md     # GUI使用指南
│   ├── DEEPFACE_INTEGRATION_GUIDE.md
│   ├── DEEPFACE_MOSAIC_USAGE.md
│   └── POSITION_FIX_GUIDE.md
└── README.md                 # 项目说明文档
```

### 文件说明

#### 核心文件
- `main.py`: 命令行版本的主程序入口
- `face_detector.py`: 包含VideoFaceDetector类，实现核心人脸检测功能
- `deepface_detector.py`: 混合检测器，结合多种检测技术

#### GUI文件
- `gui_mosaic_pyqt.py`: 基于PyQt5的现代化界面，提供完整的GUI体验

#### 文档文件
- `docs/GUI_USAGE_GUIDE.md`: 详细的GUI使用指南和功能说明

## 技术实现

### 核心算法
- **YuNet模型**：基于深度学习的人脸检测算法，具有高精度和实时性能
- **DeepFace集成**：支持多种检测后端（MTCNN、RetinaFace等），专门优化侧脸检测
- **混合检测器**：结合YuNet和DeepFace的优势，提供最佳检测效果
- **延续打码策略**：智能跟踪算法，在检测失败时自动延续打码
- **椭圆形马赛克**：使用椭圆形状替代传统矩形，提供更自然的遮挡效果
- **抗抖动算法**：通过位置平滑和尺寸稳定化技术减少检测抖动

### 性能优化
- 使用OpenCV的硬件加速功能
- 优化的视频读取和写入流程
- 内存使用优化，支持大文件处理
- 智能检测器选择策略
- 可配置的延续打码参数

## 依赖库

主要依赖包：
- `opencv-python`: 计算机视觉和图像处理
- `numpy`: 数值计算
- `deepface`: 高级人脸检测和分析
- `tensorflow`: DeepFace后端支持
- `mtcnn`: MTCNN检测后端
- `retina-face`: RetinaFace检测后端

完整依赖列表请参考 `requirements.txt` 文件。

## 模型文件

### YuNet模型
- **模型文件**: `face_detection_yunet_2023mar.onnx`
- **模型大小**: 约1.84MB
- **检测精度**: 在WIDER FACE数据集上达到业界先进水平
- **推理速度**: 支持实时检测（30+ FPS）
- **适用场景**: 正脸检测，实时处理

### DeepFace模型
- **MTCNN**: 多任务CNN，侧脸检测效果优秀
- **RetinaFace**: 最新技术，综合性能最佳
- **OpenCV**: 速度最快，基础检测效果
- **自动下载**: 首次使用时自动下载到相应目录

## 输出格式

### 控制台输出
程序运行时会显示详细的处理信息：
```
正在处理视频: sample.mp4
视频信息: 1920x1080, 30.0 FPS, 总帧数: 900
使用检测器: hybrid (YuNet + DeepFace-RetinaFace)
延续打码策略: 启用 (5帧)
正在处理帧 1/900...
检测到 2 个人脸
正在处理帧 2/900...
检测到 1 个人脸
正在处理帧 3/900...
延续打码: 使用历史位置 (1/5)
...
处理完成！
总处理时间: 45.2秒
平均FPS: 19.9
检测统计:
- 总帧数: 900
- 检测到人脸的帧数: 856 (95.1%)
- 延续打码帧数: 44 (4.9%)
- 平均每帧人脸数: 1.3
```

### 视频输出
- 支持与输入相同的分辨率和帧率
- 保持原始视频质量
- 可选择是否保存处理后的视频文件
- 椭圆形马赛克效果更自然

## 使用场景

### 隐私保护
- 会议录像中的人脸匿名化
- 公共场所监控视频的隐私处理
- 社交媒体内容的隐私保护
- 侧脸和多角度人脸的有效遮挡

### 内容审核
- 自动识别和标记视频中的人脸
- 批量处理大量视频文件
- 实时监控和预警系统
- 复杂场景下的稳定检测

### 研究和开发
- 人脸检测算法的性能评估
- 计算机视觉项目的基础工具
- 教学和演示用途
- 多检测器性能对比研究

### 👥 不同用户群体

#### 🖱️ PyQt5 GUI界面适合：
- **普通用户**: 不熟悉命令行操作的用户
- **设计师/编辑**: 需要现代化可视化界面的创意工作者
- **教育工作者**: 需要简单易用工具的教师和学生
- **一次性使用**: 偶尔需要处理视频的用户

#### ⌨️ 命令行适合：
- **开发者**: 熟悉命令行的技术人员
- **批量处理**: 需要自动化脚本的场景
- **服务器环境**: 无图形界面的服务器部署
- **高级用户**: 需要精确控制参数的专业用户

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 更新日志

### v3.1.0 (2024-01-15)
- 🚀 **新增一键打码脚本**：Python/Shell/Windows批处理三种版本
- 📝 **自动文件命名**：智能生成带时间戳的输出文件名
- 🔍 **智能依赖检查**：自动检测和提示缺失的依赖包
- 🎨 **彩色界面输出**：跨平台彩色终端界面，提升用户体验
- ⚡ **简化使用流程**：一条命令完成视频打码处理

### v3.0.0 (2024-01)
- 🔄 **新增侧脸检测优化**：集成DeepFace多后端支持
- 🎯 **新增延续打码策略**：智能跟踪算法，避免打码闪烁
- 🔀 **新增混合检测器**：结合YuNet和DeepFace优势
- 📊 **优化控制台输出**：详细的检测统计和进度信息
- 🛠️ **新增参数选项**：检测器选择、后端配置、延续帧数设置

### v2.0.0 (2024-01)
- 新增DeepFace集成功能
- 支持高级人脸分析（年龄、性别、情绪、种族）
- 优化检测算法性能
- 改进用户界面和错误处理

### v1.2.0 (2023-12)
- 新增椭圆形马赛克功能
- 实现抗抖动算法
- 支持网络摄像头实时检测
- 优化内存使用和处理速度

### v1.1.0 (2023-11)
- 新增实时预览功能
- 支持多种视频格式
- 改进检测精度和稳定性
- 添加详细的统计信息

### v1.0.0 (2023-10)
- 初始版本发布
- 基础人脸检测和标注功能
- 支持视频文件处理
- 命令行界面

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

## 网络摄像头支持

本项目支持使用网络摄像头进行实时人脸检测：

```bash
# 使用默认摄像头（通常是摄像头ID 0）
python main.py 0 --preview

# 使用特定摄像头ID
python main.py 1 --preview

# 实时马赛克处理（推荐使用YuNet以获得更好的实时性能）
python main.py 0 --detector yunet --mosaic --preview

# 实时侧脸检测（性能要求较高）
python main.py 0 --detector hybrid --deepface-backend mtcnn --mosaic --preview
```

**注意**：
- 摄像头ID通常从0开始
- 使用摄像头时建议启用预览功能
- 实时处理推荐使用YuNet检测器以获得更好的性能
- 按 'q' 键退出实时检测

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！