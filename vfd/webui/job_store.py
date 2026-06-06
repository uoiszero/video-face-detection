from __future__ import annotations

import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional

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

    def get_by_id(self, job_id: str) -> Optional[JobState]:
        """
        按 job_id 获取当前 job。

        由于当前实现为“单用户单任务”，因此只有当 job_id 与当前 job 匹配时才返回。
        """

        with self._lock:
            if self._job is None or self._job.id != job_id:
                return None
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

    def snapshot(self, job_id: str) -> Optional[Dict]:
        """
        返回 job 的 JSON 友好快照（用于 API/SSE 输出）。
        """

        with self._lock:
            if self._job is None or self._job.id != job_id:
                return None

            return {
                "id": self._job.id,
                "status": self._job.status.value,
                "created_at": self._job.created_at,
                "updated_at": self._job.updated_at,
                "progress": self._job.progress,
                "logs": list(self._job.logs),
                "output_path": self._job.output_path,
                "error": self._job.error,
            }

    def update_status(self, job_id: str, status: JobStatus) -> None:
        """
        更新 job 状态。
        """

        with self._lock:
            job = self._require_job_locked(job_id=job_id)
            job.status = status
            job.updated_at = time.time()

    def update_progress(self, job_id: str, progress: int) -> None:
        """
        更新 job 进度（0-100）。
        """

        with self._lock:
            job = self._require_job_locked(job_id=job_id)
            job.progress = max(0, min(100, int(progress)))
            job.updated_at = time.time()

    def append_log(self, job_id: str, message: str) -> None:
        """
        追加一条日志到 job 日志队列中。
        """

        with self._lock:
            job = self._require_job_locked(job_id=job_id)
            job.logs.append(message)
            job.updated_at = time.time()

    def set_output_path(self, job_id: str, output_path: Optional[str]) -> None:
        """
        更新 job 输出路径。
        """

        with self._lock:
            job = self._require_job_locked(job_id=job_id)
            job.output_path = output_path
            job.updated_at = time.time()

    def set_error(self, job_id: str, error: Optional[str]) -> None:
        """
        更新 job 错误信息。
        """

        with self._lock:
            job = self._require_job_locked(job_id=job_id)
            job.error = error
            job.updated_at = time.time()

    def _require_job_locked(self, job_id: str) -> JobState:
        """
        在持锁状态下获取 job；若 job 不存在或 id 不匹配则抛出 KeyError。
        """

        if self._job is None or self._job.id != job_id:
            raise KeyError(job_id)
        return self._job
