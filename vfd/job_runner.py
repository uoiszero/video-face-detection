from __future__ import annotations

import os
import pathlib
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, Dict

from vfd.ffmpeg import build_transcode_cmd, find_ffmpeg
from vfd.job_types import JobParams


@dataclass(frozen=True)
class JobResult:
    """
    单次 Job 执行结果。

    Attributes:
        output_path: 最终输出文件路径。
        stats: OpenCV 阶段返回的统计信息（来自 detector.process_video）。
    """

    output_path: str
    stats: Dict


def validate_input_path(path: str) -> None:
    """
    校验输入视频路径。

    Args:
        path: 输入视频路径。

    Raises:
        FileNotFoundError: path 不存在或不是文件。
    """

    if not os.path.isfile(path):
        raise FileNotFoundError(path)


def run_job(
    job_id: str,
    params: JobParams,
    outputs_dir: str,
    log: Callable[[str], None],
    progress: Callable[[int, int], bool],
) -> JobResult:
    """
    运行一次视频处理任务（进程内调用现有检测器）。

    处理流程：
    1) 使用 OpenCV（现有 detector.process_video）生成中间视频文件；
    2) 若用户选择输出分辨率/码率/编码器，则用 ffmpeg 转码生成最终文件。

    Args:
        job_id: Job 唯一标识，用于命名输出文件。
        params: Job 参数（来自 WebUI/CLI 的归一化结果）。
        outputs_dir: 输出目录（最终文件写入该目录；中间文件写入 outputs_dir/.tmp）。
        log: 日志回调函数。
        progress: 进度回调函数，签名为 (current, total) -> bool，返回 False 表示终止处理。

    Returns:
        JobResult: 最终输出路径与处理统计信息。
    """

    validate_input_path(params.input_path)

    outputs = pathlib.Path(outputs_dir)
    tmp_dir = outputs / ".tmp"
    outputs.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    tmp_path = str(tmp_dir / f"{job_id}.tmp.mp4")
    final_path = str(outputs / f"{job_id}.mp4")

    log("initializing detector")

    from face_detector import VideoFaceDetector

    hybrid_available = False
    HybridFaceDetector = None
    try:
        from deepface_detector import HybridFaceDetector as _HybridFaceDetector

        HybridFaceDetector = _HybridFaceDetector
        hybrid_available = True
    except Exception:
        hybrid_available = False

    if params.detector == "yunet":
        detector = VideoFaceDetector(continuation_frames=params.continuation_frames)
    elif params.detector in ("deepface", "hybrid"):
        if not hybrid_available or HybridFaceDetector is None:
            raise RuntimeError("deepface not available")

        detector = HybridFaceDetector(
            primary_backend="yunet" if params.detector == "hybrid" else params.deepface_backend,
            enable_deepface=True,
            deepface_backend=params.deepface_backend,
            continuation_frames=params.continuation_frames,
        )
    else:
        raise ValueError("invalid detector")

    started_at = time.time()
    stats = detector.process_video(
        input_path=params.input_path,
        output_path=tmp_path,
        show_preview=False,
        apply_mosaic=params.apply_mosaic,
        mosaic_size=params.mosaic_size,
        progress_callback=progress,
        codec="auto",
    )
    log(f"opencv stage done in {time.time() - started_at:.2f}s")

    need_transcode = (
        params.output_resolution is not None
        or params.video_bitrate is not None
        or params.codec == "h264"
    )
    if not need_transcode:
        os.replace(tmp_path, final_path)
        return JobResult(output_path=final_path, stats=stats)

    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path is None:
        raise RuntimeError("ffmpeg not found")

    cmd = build_transcode_cmd(
        input_path=tmp_path,
        output_path=final_path,
        output_resolution=params.output_resolution,
        video_bitrate=params.video_bitrate,
        codec=params.codec,
    )
    cmd[0] = ffmpeg_path

    log("running ffmpeg transcode")
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    os.remove(tmp_path)

    return JobResult(output_path=final_path, stats=stats)
