# VFD WebUI 使用说明

本目录提供基于 FastAPI 的 WebUI，用于通过浏览器提交视频处理任务，并在页面中实时查看进度与日志。

## 1. 依赖与安装

### 1.1 Python 依赖

建议在虚拟环境中安装：

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip

pip install -r requirements.txt -r requirements-webui.txt
```

如需使用 `detector=deepface` 或 `detector=hybrid`，还需要额外安装 DeepFace 相关依赖（项目内也提供了安装脚本）：

```bash
./scripts/install_deepface.sh
```

### 1.2 ffmpeg（可选但推荐）

当你在 WebUI 中设置了以下任一参数时，会触发转码步骤，此时必须安装 `ffmpeg`：

- `output_resolution != original`
- `video_bitrate` 非空
- `codec = h264`

macOS（Homebrew）：

```bash
brew install ffmpeg
```

Ubuntu/Debian：

```bash
sudo apt-get install ffmpeg
```

## 2. 启动 WebUI

在项目根目录执行：

```bash
python -m uvicorn vfd.webui.app:create_app --factory --host 127.0.0.1 --port 8000
```

打开浏览器访问：

- http://127.0.0.1:8000/

说明：

- `--factory` 表示 uvicorn 会调用 `create_app()` 来创建 FastAPI 实例
- 默认输出目录以进程的当前工作目录为准；推荐在项目根目录启动，确保输出落在 `./outputs/`

## 3. 使用流程

1) 打开首页表单
2) 填写 `input_path`（本机/服务器上的视频文件绝对路径或相对路径）
3) 选择检测器与参数后提交
4) 提交成功后会返回 Job 页面：`/jobs/<job_id>`
5) Job 页面会持续刷新状态（SSE），直至 `succeeded` 或 `failed`

## 4. 参数说明

WebUI 表单字段与含义如下（字段名与页面一致）：

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `input_path` | string | 无 | 输入视频路径（必须是服务器可访问路径） |
| `detector` | enum | `yunet` | `yunet` / `deepface` / `hybrid` |
| `deepface_backend` | string | `opencv` | deepface 后端名（仅 deepface/hybrid 生效） |
| `continuation_frames` | int | `5` | 检测失败时延续打码的帧数 |
| `apply_mosaic` | enum | `false` | 是否对检测到的人脸打码：`true/false` |
| `mosaic_size` | int | `15` | 马赛克粒度，越小越细腻 |
| `output_resolution` | string | `original` | `original` / `720p` / `1080p` / `WxH`（如 `1024x768`） |
| `video_bitrate` | string | 空 | 空表示不设置；支持 `6000k`、`6M` 或纯数字（视为 Mbps，如 `6` -> `6M`） |
| `codec` | enum | `auto` | `auto`（不强制转码）/ `h264`（强制用 H.264 编码） |

## 5. 输出文件位置（outputs）

WebUI 的输出位置固定在当前工作目录下的 `outputs/`：

- 最终输出：`outputs/<job_id>.mp4`
- 中间文件：`outputs/.tmp/<job_id>.tmp.mp4`

Job 成功时，Job 的 JSON 快照里会包含 `output_path` 字段，用于定位文件。

## 6. 常见问题

### 6.1 提交后报错 “deepface not available”

说明你选择了 `detector=deepface/hybrid`，但运行环境没有安装 deepface 相关依赖。请安装后重试：

```bash
./scripts/install_deepface.sh
```

### 6.2 提交后报错 “ffmpeg not found”

说明触发了转码（见上文 1.2），但系统中找不到 `ffmpeg`。请安装并确保 `ffmpeg` 在 `PATH` 中：

```bash
brew install ffmpeg
```

