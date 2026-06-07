# AGENTS.md

本文件用于指导自动化代码助手/Agent 在本仓库内协作开发与维护，确保改动可测试、可维护、可持续开源。

## 项目概述

本项目是一个基于 Python 的视频人脸检测与（可选）隐私马赛克处理工具，当前主入口为：
- CLI：`main.py`
- WebUI（FastAPI）：`vfd/webui`

旧桌面 GUI（PyQt/Tkinter）已标记为 Deprecated，仅保留用于历史兼容与参考。

## 开发原则

- 先测试后实现（TDD）：新增/修复功能必须先写测试，确认失败（RED）后再写最小实现（GREEN）。
- 最小改动：优先复用现有模块与模式，避免无关重构。
- 函数级注释：新增的函数/方法必须包含 docstring（用于说明用途、参数与返回值）。
- 不要引入或输出任何密钥：禁止把 API Key、Token、个人隐私写入代码、日志或文档。
- 依赖最小化：WebUI 与核心算法分层，避免 UI 依赖污染核心依赖。

## 目录结构（关键部分）

- `vfd/`：新增的可复用库代码（job 类型、runner、ffmpeg、webui）
- `vfd/webui/`：FastAPI WebUI（app、模板、静态资源、job store）
- `tests/`：测试用例（默认跳过 GUI/交互型测试）
- `scripts/`：脚本（包括一键启动 WebUI）
- `outputs/`：输出目录（产物默认落盘在这里，不提交到 Git）

## 环境与依赖

本项目建议使用虚拟环境运行：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-webui.txt -r requirements-dev.txt
```

说明：
- `requirements.txt`：核心依赖（OpenCV/NumPy）
- `requirements-webui.txt`：WebUI 依赖（FastAPI/Uvicorn/Jinja2 等）
- `requirements-dev.txt`：测试/开发依赖（pytest 等）

## 启动 WebUI

推荐脚本方式启动：

```bash
bash scripts/webui.sh
```

默认访问地址：
- `http://127.0.0.1:7860/`

可用环境变量：
- `VFD_HOST`（默认 `127.0.0.1`）
- `VFD_PORT`（默认 `7860`）

## ffmpeg 说明

当你需要控制输出分辨率/码率（转码）时，需要系统安装 `ffmpeg`。

macOS（Homebrew）：

```bash
brew install ffmpeg
```

## 运行测试

```bash
. .venv/bin/activate
python -m pytest -q
```

GUI/交互类测试默认跳过，如需显式运行：
- `VFD_RUN_GUI_TESTS=1 python -m pytest -q`

## CI 约定

仓库 CI 运行 `python -m pytest -q`（macOS runner + Python 版本矩阵）。新增测试需满足：
- 可在无 GUI、无摄像头、无大模型依赖的环境下稳定运行
- 对于需要外部依赖的测试必须默认跳过，并提供显式启用方式

## 变更交付要求

- 每个逻辑改动应配套测试与最小文档更新
- 测试通过后再提交（commit）
- 提交信息使用清晰的约定式前缀（例如 `feat:` / `fix:` / `docs:` / `ci:` / `chore:`）

