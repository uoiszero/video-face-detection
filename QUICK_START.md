# 🚀 快速开始指南

本指南将帮助您快速上手视频人脸检测和打码功能。

## 📋 准备工作

### 1. 安装依赖

选择适合您系统的安装方式：

```bash
# 方式一：Python安装脚本（推荐）
python3 install_dependencies.py

# 方式二：Shell脚本（macOS/Linux）
chmod +x install.sh && ./install.sh

# 方式三：批处理脚本（Windows）
install.bat
```

### 2. 准备视频文件

确保您有一个要处理的视频文件，支持的格式包括：
- MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V

## 🎯 一键打码使用

### 最简单的使用方式

```bash
# Python版本（跨平台推荐）
python quick_mosaic.py your_video.mp4

# Shell版本（macOS/Linux）
./quick_mosaic.sh your_video.mp4

# Windows批处理版本
quick_mosaic.bat your_video.mp4
```

### 使用示例

假设您有一个名为 `sample.mp4` 的视频文件：

```bash
# 运行一键打码
python quick_mosaic.py sample.mp4
```

**输出结果：**
- 自动生成输出文件：`sample_out_20240115_143022.mp4`
- 使用最优配置：混合检测器 + 侧脸优化 + 延续15帧
- 智能检测和处理所有人脸

## 🔧 一键打码配置

一键打码脚本使用以下优化配置：

| 配置项 | 值 | 说明 |
|--------|----|---------|
| 检测器 | hybrid | 混合检测器（YuNet + DeepFace） |
| 后端 | retinaface | 侧脸检测优化 |
| 延续帧数 | 15 | 减少打码闪烁 |
| 输出格式 | 自动 | 保持原视频格式 |
| 文件命名 | 自动 | 原名_out_时间戳 |

## 📊 处理流程

1. **依赖检查** - 自动检测必要文件和模型
2. **格式验证** - 确认视频格式支持
3. **文件检查** - 验证输入文件存在
4. **智能处理** - 使用优化配置进行检测和打码
5. **结果验证** - 确认输出文件生成成功

## 🎨 界面特性

### Python版本特性
- ✅ 跨平台兼容
- ✅ 详细的进度信息
- ✅ 彩色状态提示
- ✅ 智能错误处理

### Shell版本特性（macOS/Linux）
- ✅ 原生Shell性能
- ✅ 彩色终端输出
- ✅ 实时处理状态
- ✅ 文件大小显示

### Windows批处理特性
- ✅ Windows原生支持
- ✅ 中文界面友好
- ✅ 自动暂停显示结果
- ✅ 简单双击运行

## 🔍 输出文件命名规则

输出文件自动按以下规则命名：

```
原文件名_out_时间戳.扩展名
```

**示例：**
- 输入：`family_video.mp4`
- 输出：`family_video_out_20240115_143022.mp4`
- 时间戳格式：`YYYYMMDD_HHMMSS`

## 🚨 常见问题

### Q: 脚本提示缺少依赖文件
**A:** 运行安装脚本：`python install_dependencies.py`

### Q: 视频格式不支持
**A:** 转换为支持的格式（MP4推荐）或选择继续处理

### Q: 输出文件已存在
**A:** 脚本会询问是否覆盖，选择 `y` 覆盖或 `N` 取消

### Q: 处理速度慢
**A:** 这是正常现象，混合检测器会进行精确分析，请耐心等待

### Q: 某些人脸未被检测到
**A:** 一键打码已使用最优配置，如需调整可使用高级命令行选项

## 🎯 高级使用

如果需要更多控制选项，可以使用完整的命令行界面：

```bash
# 自定义检测器
python main.py video.mp4 --detector yunet --mosaic

# 调整延续帧数
python main.py video.mp4 --detector hybrid --continuation-frames 20 --mosaic

# 实时预览
python main.py video.mp4 --detector hybrid --mosaic --preview

# 摄像头实时检测
python main.py 0 --detector yunet --mosaic --preview
```

## 📈 性能建议

### 快速处理
- 使用 YuNet 检测器：`--detector yunet`
- 较少延续帧数：`--continuation-frames 5`

### 高精度处理
- 使用混合检测器：`--detector hybrid`（默认）
- 增加延续帧数：`--continuation-frames 20`

### 侧脸优化
- 使用 DeepFace：`--detector deepface`
- RetinaFace后端：`--deepface-backend retinaface`（默认）

## 🎉 完成！

现在您已经掌握了一键打码的使用方法！

**下一步：**
- 尝试处理您的第一个视频
- 查看 [README.md](README.md) 了解更多功能
- 探索 [INSTALL.md](INSTALL.md) 了解安装详情
- 参考 [docs/](docs/) 目录获取高级功能指南

---

**提示：** 首次使用 DeepFace 功能时，会自动下载额外的模型文件，这可能需要一些时间和网络连接。