# CLI 使用手册

## 概述

本项目提供了三条 CLI 入口，满足从「一键傻瓜式」到「精细调参」的不同需求：

| 脚本 | 用途 | 推荐场景 |
|------|------|----------|
| `main.py` | 完整命令行工具，全部参数可配 | 需要精确控制检测器/马赛克/编码的用户 |
| `quick_mosaic.py` | 一键打码，自动生成输出文件名 | 快速处理单个视频，无需纠结参数 |
| `scripts/quick_mosaic.sh` | Shell 版一键打码（macOS/Linux） | 终端习惯、脚本集成 |
| `scripts/quick_mosaic.bat` | 批处理版一键打码（Windows） | Windows 原生环境 |

---

## 1. 完整 CLI：`main.py`

### 基本用法

```bash
python main.py <input_video> [options]
```

### 参数总表

| 参数 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `input_video` | — | 必选 | — | 输入视频文件路径（也支持摄像头 ID，如 `0`） |
| `--output` | `-o` | 字符串 | 无 | 输出视频路径；不指定则仅检测不保存 |
| `--preview` | `-p` | 开关 | 关 | 显示实时预览窗口（按 `q` 退出） |
| `--mosaic` | `-m` | 开关 | 关 | 对检测到的人脸应用椭圆形马赛克（隐私保护） |
| `--mosaic-size` | — | 整数 | `30` | 马赛克块大小（像素），**值越小越细腻** |
| `--detector` | — | 枚举 | `yunet` | 检测器：`yunet` / `deepface` / `hybrid` |
| `--deepface-backend` | — | 枚举 | `mtcnn` | DeepFace 后端：`opencv` / `ssd` / `dlib` / `mtcnn` / `retinaface` |
| `--continuation-frames` | — | 整数 | `5` | 无人脸检测时延续打码的帧数 |
| `--model` | — | 字符串 | 无 | 自定义 YuNet ONNX 模型文件路径 |
| `--codec` / `--encoder` | — | 枚举 | `auto` | 输出编码器：`auto` / `h264`（H.264/AVC） |

---

### 参数详解

#### `--output / -o`

指定输出视频的保存路径。

- **不指定**：程序仅做检测分析，**不保存**处理后的视频。
- **指定**：按原视频分辨率 + 帧率写入结果。

```bash
python main.py video.mp4                                          # 仅检测
python main.py video.mp4 -o result.mp4                            # 保存检测结果
python main.py video.mp4 -m -o /path/to/mosaic.mp4                # 保存打码结果
```

#### `--mosaic / -m` + `--mosaic-size`

对人脸区域应用**椭圆形马赛克**，比矩形马赛克更贴合人脸轮廓，边缘有渐变过渡。

- `--mosaic-size` 默认 `30`。值越小马赛克块越细密，视觉效果更好但计算量略增。
- 启用马赛克时会**自动启用抗抖动算法**，避免打码区域闪烁。

```bash
python main.py video.mp4 -m -o mosaic.mp4                         # 默认粒度 30
python main.py video.mp4 -m --mosaic-size 10 -o fine_mosaic.mp4   # 细腻马赛克
```

#### `--detector`：选择检测器

| 值 | 速度 | 侧脸检测 | 推荐场景 |
|----|------|----------|----------|
| `yunet`（默认） | 最快 | 一般 | 实时预览、正脸为主、资源受限 |
| `deepface` | 较慢 | 优秀 | 侧脸较多、高精度要求 |
| `hybrid` | 中等 | 最佳 | 复杂场景、多角度、最佳效果 |

```bash
python main.py video.mp4 --detector yunet                         # 默认，速度优先
python main.py video.mp4 --detector deepface --deepface-backend mtcnn -m
python main.py video.mp4 --detector hybrid --deepface-backend retinaface -m  # 推荐
```

> **注意**：`deepface` 和 `hybrid` 需要安装 `deepface` 及 TensorFlow 等依赖，首次运行会自动下载远端模型。

#### `--deepface-backend`

当 `--detector` 为 `deepface` 或 `hybrid` 时有效。

| 后端 | 说明 | 推荐 |
|------|------|------|
| `opencv` | 速度最快，基础检测 | 实时预览 |
| `ssd` | 平衡速度与精度 | 通用 |
| `dlib` | 传统方法，稳定 | 无 GPU 环境 |
| `mtcnn` | 侧脸检测优秀 | **推荐**（默认） |
| `retinaface` | 综合性能最佳 | **推荐**（高质量场景） |

#### `--continuation-frames`

当某帧未检测到人脸时，以最后一帧的人脸位置**延续打码**，防止闪烁。

- **快速运动**：建议 `10`-`15` 帧
- **静态场景**：默认 `5` 帧即可
- **实时预览**：可降至 `3` 帧

```bash
python main.py video.mp4 --continuation-frames 10 -m -o result.mp4
```

#### `--codec` / `--encoder`

控制输出视频的编码格式。

- `auto`（默认）：根据输出文件扩展名自动选择（如 `.mp4` → H.264）。
- `h264`：显式指定 H.264 编码器。

> 某些 macOS 系统需要 `h264` 才能获得正确的播放兼容性。

```bash
python main.py video.mp4 -o result.mp4 --codec h264
```

#### `--model`

指定自定义 YuNet ONNX 模型路径。不指定时使用 `models/` 目录下的默认模型。

```bash
python main.py video.mp4 --model ./my_models/yunet_int8.onnx
```

---

### 典型使用场景

#### 场景 1：快速检测，只看统计信息

```bash
python main.py input.mp4
```

#### 场景 2：预览 + 保存检测结果

```bash
python main.py input.mp4 -o detected.mp4 -p
```

#### 场景 3：隐私打码，保存结果

```bash
python main.py input.mp4 -m -o blurred.mp4
```

#### 场景 4：侧脸较多的视频打码

```bash
python main.py input.mp4 -m --detector deepface --deepface-backend mtcnn -o output.mp4
```

#### 场景 5：最佳效果（推荐配置）

```bash
python main.py input.mp4 -m --detector hybrid --deepface-backend retinaface --continuation-frames 10 -o best.mp4
```

#### 场景 6：摄像头实时检测

```bash
python main.py 0 -p                               # 默认摄像头，仅检测
python main.py 0 --detector yunet -m -p           # 实时马赛克（推荐 YuNet）
python main.py 1 -p                               # 摄像头 ID=1
```

按 `q` 键退出实时预览。

---

## 2. 一键打码：`quick_mosaic.py`

针对「不想管参数，就想打个码」的场景。

### 用法

```bash
python quick_mosaic.py <input_video>
```

### 内置配置

| 选项 | 值 |
|------|----|
| 检测器 | `hybrid`（YuNet + DeepFace） |
| DeepFace 后端 | `retinaface` |
| 延续帧数 | `15` |
| 马赛克 | 启用 |
| 输出命名 | `原文件名_out_时间戳.扩展名` |

### 示例

```bash
python quick_mosaic.py family.mp4
# 生成：family_out_20240624_153022.mp4
```

### 依赖检查

脚本会自动检查 `main.py` 和 YuNet 模型文件是否存在，缺失时提示运行安装脚本。

---

## 3. Shell 版一键打码

```bash
chmod +x scripts/quick_mosaic.sh
./scripts/quick_mosaic.sh video.mp4
```

Windows 用户可直接双击 `scripts\quick_mosaic.bat` 或执行：

```cmd
scripts\quick_mosaic.bat video.mp4
```

> 注意：Shell/批处理版是 `quick_mosaic.py` 的封装，实际仍调用 `main.py`。

---

## 4. 输出与控制台信息

### 控制台输出示例

```
视频人脸检测工具 v1.0
========================================
初始化混合检测器（YuNet + DeepFace） - DeepFace后端: retinaface...
输入视频: sample.mp4
输出视频: result.mp4
输出编码器: auto
马赛克模式: 启用 (块大小: 30)

开始处理...
正在处理帧 1/900...
检测到 2 个人脸
正在处理帧 2/900...
检测到 1 个人脸
正在处理帧 3/900...
延续打码: 使用历史位置 (1/5)
...
========================================
处理完成!
输出文件已保存: result.mp4 (45.3 MB)
```

### 状态行说明

| 信息 | 含义 |
|------|------|
| `检测到 X 个人脸` | 当前帧检测结果 |
| `延续打码: 使用历史位置 (X/5)` | 本帧未检测到人脸，使用历史位置延续打码 |
| `使用历史信息延续打码` | 分析最近 3 帧检测历史后做延续 |
| `清空人脸历史` | 超过延续帧数限制，重置跟踪状态 |

---

## 5. 常见用法速查表

| 目标 | 命令 |
|------|------|
| 仅检测不保存 | `python main.py video.mp4` |
| 检测 + 保存 | `python main.py video.mp4 -o out.mp4` |
| 检测 + 预览 | `python main.py video.mp4 -p` |
| 默认打码 | `python main.py video.mp4 -m -o out.mp4` |
| 细腻打码 | `python main.py video.mp4 -m --mosaic-size 10 -o out.mp4` |
| 侧脸打码 | `python main.py video.mp4 -m --detector deepface --deepface-backend mtcnn -o out.mp4` |
| 最佳效果 | `python main.py video.mp4 -m --detector hybrid --deepface-backend retinaface -o out.mp4` |
| 长延续打码 | `python main.py video.mp4 -m --continuation-frames 15 -o out.mp4` |
| H.264 编码 | `python main.py video.mp4 -o out.mp4 --codec h264` |
| 一键傻瓜式 | `python quick_mosaic.py video.mp4` |
| 摄像头实时 | `python main.py 0 --detector yunet -m -p` |

---

## 6. 注意事项

1. **DeepFace 依赖**：使用 `deepface` 或 `hybrid` 检测器前需要安装 `deepface` 及相关库，参见 [INSTALL.md](INSTALL.md)。
2. **首次运行**：DeepFace 首次使用时会自动下载远端模型（TensorFlow 后端等），耗时较长。
3. **摄像头 ID**：`main.py 0` 表示使用默认摄像头，数字对应系统摄像头编号。
4. **多段延续** 消息为正常提示，代表当前帧检测置信度低，正在使用历史位置补帧。
5. **处理大文件**：建议确保磁盘有足够空间存放输出文件（约等于输入文件大小）。
