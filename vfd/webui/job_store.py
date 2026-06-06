from __future__ import annotations

import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Optional

from vfd.job_types import JobStatus


@dataclass
class JobState:
    id: str
    status: JobStatus
    created_at: float
    updated_at: float
    progress: int = 0
    logs: Deque[str] = field(default_factory=lambda: deque(maxlen=2000))
    output_path: Optional[str] = None
    error: Optional[str] = None


class JobStore:
    def __init__(self) -> None:
        """
        初始化单用户单任务的 Job 存储。
        """

        self._lock = threading.Lock()
        self._job: Optional[JobState] = None

    def get(self) -> Optional[JobState]:
        """
        获取当前 job（没有则返回 None）。
        """

        with self._lock:
            return self._job

    def create_job(self, input_path: str) -> JobState:
        """
        创建一个新 job。

        约束：
        - 若已有 job 且其状态为 queued/running，则拒绝创建并抛出 RuntimeError。
        """

        with self._lock:
            if self._job is not None and self._job.status in (
                JobStatus.queued,
                JobStatus.running,
            ):
                raise RuntimeError("job already running")

            now = time.time()
            self._job = JobState(
                id=str(uuid.uuid4()),
                status=JobStatus.queued,
                created_at=now,
                updated_at=now,
            )
            self._job.logs.append(f"input={input_path}")
            return self._job
