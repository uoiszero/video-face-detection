# 依赖安装指南

本项目提供了多种方式来自动安装所需的依赖包和模型文件。

## 🚀 快速安装

### 方式一：Python安装脚本（推荐）

```bash
# 运行Python安装脚本
python3 install_dependencies.py
```

**特点：**
- ✅ 跨平台支持（Windows、macOS、Linux）
- ✅ 详细的安装日志和错误提示
- ✅ 自动验证安装结果
- ✅ 智能检测已存在的文件

### 方式二：Shell脚本（macOS/Linux）

```bash
# 给脚本添加执行权限
chmod +x install.sh

# 运行安装脚本
./install.sh

# 或者在虚拟环境中安装
./install.sh --venv
```

**特点：**
- ✅ 原生Shell脚本，速度快
- ✅ 支持虚拟环境创建
- ✅ 彩色输出，界面友好
- ✅ 自动选择下载工具（curl/wget）

### 方式三：批处理脚本（Windows）

```cmd
# 双击运行或在命令提示符中执行
install.bat
```

**特点：**
- ✅ Windows原生支持
- ✅ 使用PowerShell下载文件
- ✅ 中文界面友好
- ✅ 自动暂停显示结果

## 📦 安装内容

### Python依赖包

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| opencv-python | >=4.8.0 | 计算机视觉和图像处理 |
| numpy | >=1.21.0 | 数值计算 |
| deepface | >=0.0.79 | 高级人脸检测和分析 |
| tensorflow | >=2.12.0 | DeepFace后端支持 |
| mtcnn | >=0.1.1 | MTCNN检测后端 |
| retina-face | >=0.0.13 | RetinaFace检测后端 |

### 模型文件

| 模型文件 | 大小 | 用途 |
|----------|------|------|
| face_detection_yunet_2023mar.onnx | ~1.85MB | YuNet标准模型 |
| face_detection_yunet_2023mar_int8.onnx | ~473KB | YuNet量化模型（更快） |

## 🔧 安装选项

### 虚拟环境安装（推荐）

```bash
# 使用Shell脚本创建虚拟环境
./install.sh --venv

# 手动创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 然后运行安装脚本
python install_dependencies.py
```

### 手动安装

如果自动安装脚本失败，可以手动安装：

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 创建模型目录
mkdir -p models

# 3. 下载模型文件
cd models
wget https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
wget https://github.com/opencv/opencv_zoo/raw/master/models/face_detection_yunet/face_detection_yunet_2023mar_int8.onnx
cd ..
```

## 🔍 验证安装

安装完成后，可以运行以下命令验证：

```bash
# 检查Python包导入
python -c "import cv2, numpy, deepface, tensorflow; print('✅ 所有包导入成功')"

# 检查模型文件
ls -la models/

# 运行帮助命令
python main.py --help
```

## 🚨 常见问题

### 1. Python版本不兼容

**问题**：需要Python 3.8或更高版本

**解决方案**：
- 升级Python到3.8+
- 使用pyenv管理多个Python版本

### 2. 网络连接问题

**问题**：模型文件下载失败

**解决方案**：
```bash
# 使用代理下载
export https_proxy=http://your-proxy:port
./install.sh

# 或手动下载模型文件
# 将下载的文件放到 models/ 目录中
```

### 3. 权限问题（macOS/Linux）

**问题**：脚本没有执行权限

**解决方案**：
```bash
chmod +x install.sh
./install.sh
```

### 4. pip安装失败

**问题**：某些包安装失败

**解决方案**：
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 逐个安装失败的包
pip install opencv-python
pip install deepface
```

### 5. TensorFlow安装问题

**问题**：TensorFlow安装失败或版本冲突

**解决方案**：
```bash
# 安装CPU版本
pip install tensorflow-cpu

# 或安装特定版本
pip install tensorflow==2.12.0
```

## 📋 系统要求

### 最低要求
- **Python**: 3.8+
- **内存**: 4GB RAM
- **存储**: 2GB可用空间
- **网络**: 用于下载模型文件

### 推荐配置
- **Python**: 3.9+
- **内存**: 8GB+ RAM
- **存储**: 5GB+ 可用空间
- **GPU**: 支持CUDA的显卡（可选，用于加速）

## 🎯 安装后使用

安装完成后，可以立即开始使用：

```bash
# 基础使用
python main.py sample.mp4 --mosaic --preview

# 侧脸检测优化
python main.py sample.mp4 --detector deepface --deepface-backend mtcnn --mosaic

# 混合检测器（推荐）
python main.py sample.mp4 --detector hybrid --deepface-backend retinaface --mosaic

# 实时摄像头检测
python main.py 0 --detector yunet --mosaic --preview
```

更多使用方法请参考 [README.md](README.md) 文档。

## 📞 获取帮助

如果安装过程中遇到问题：

1. 查看控制台输出的错误信息
2. 检查网络连接
3. 尝试手动安装失败的组件
4. 查看项目的 [Issues](https://github.com/your-repo/issues) 页面
5. 提交新的Issue描述问题

---

**注意**：首次运行DeepFace相关功能时，会自动下载额外的模型文件，这可能需要一些时间。