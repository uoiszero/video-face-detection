from __future__ import annotations

import shutil
from typing import List, Optional, Tuple


def find_ffmpeg() -> Optional[str]:
    """
    查找系统中的 ffmpeg 可执行文件路径。

    Returns:
        若能在 PATH 中找到 ffmpeg，则返回其绝对路径；否则返回 None。
    """

    return shutil.which("ffmpeg")


def build_transcode_cmd(
    input_path: str,
    output_path: str,
    output_resolution: Optional[Tuple[int, int]],
    video_bitrate: Optional[str],
    codec: str,
) -> List[str]:
    """
    构建用于转码的 ffmpeg 命令行参数（不执行）。

    Args:
        input_path: 输入视频路径。
        output_path: 输出视频路径。
        output_resolution: 输出分辨率 (w, h)，None 表示不缩放。
        video_bitrate: 视频码率（如 "6000k"、"6M"），None 表示不设置。
        codec: 编码器选择；当前约定 "h264" 表示使用 libx264，否则按无损直拷贝处理。

    Returns:
        以 list[str] 形式返回的命令行参数，可直接用于 subprocess.run。
    """

    cmd: List[str] = ["ffmpeg", "-y", "-i", input_path]

    if output_resolution is not None:
        w, h = output_resolution
        cmd += ["-vf", f"scale={w}:{h}"]

    if video_bitrate is not None:
        cmd += ["-b:v", video_bitrate]

    if codec == "h264":
        cmd += ["-c:v", "libx264"]
    else:
        cmd += ["-c:v", "copy"]

    cmd += ["-movflags", "+faststart", output_path]
    return cmd

