from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"


@dataclass(frozen=True)
class JobParams:
    input_path: str
    detector: str
    deepface_backend: str
    continuation_frames: int
    apply_mosaic: bool
    mosaic_size: int
    output_resolution: Optional[Tuple[int, int]]
    video_bitrate: Optional[str]
    codec: str


def normalize_bitrate(value: Optional[str]) -> Optional[str]:
    """
    归一化码率输入，返回 ffmpeg 可接受的格式（如 6000k、6M）。

    规则：
    - None / 空字符串 -> None
    - 纯数字字符串（如 "6"）-> 视为 Mbps，返回 "6M"
    - 已是 ffmpeg 风格（如 "6000k"、"6M"）-> 原样返回
    - 其他 -> 抛出 ValueError
    """
    if value is None:
        return None

    v = value.strip()
    if v == "":
        return None

    if v.lower().endswith(("k", "m")):
        return v

    if v.isdigit():
        return f"{v}M"

    raise ValueError("invalid bitrate")


def normalize_output_resolution(value: str) -> Optional[Tuple[int, int]]:
    """
    归一化输出分辨率输入。

    规则：
    - original / 空字符串 -> None（表示不缩放）
    - 720p / 1080p -> 固定 WxH
    - 形如 1024x768 -> 解析为 (1024, 768)
    - 其他 -> 抛出 ValueError
    """
    v = value.strip().lower()

    if v in ("original", ""):
        return None

    if v == "720p":
        return (1280, 720)

    if v == "1080p":
        return (1920, 1080)

    if "x" in v:
        w_s, h_s = v.split("x", 1)
        return (int(w_s), int(h_s))

    raise ValueError("invalid resolution")

