import threading

import pytest

from vfd.job_types import JobStatus
from vfd.webui.job_store import JobStore


def test_job_store_single_job_only():
    store = JobStore()
    job1 = store.create_job(input_path="/tmp/a.mp4")
    assert job1.id
    with pytest.raises(RuntimeError):
        store.create_job(input_path="/tmp/b.mp4")


def test_job_store_updates_status_progress_log_output_error():
    store = JobStore()
    job = store.create_job(input_path="/tmp/a.mp4")

    store.update_status(job_id=job.id, status=JobStatus.running)
    store.update_progress(job_id=job.id, progress=42)
    store.append_log(job_id=job.id, message="hello")
    store.set_output_path(job_id=job.id, output_path="/tmp/out.mp4")
    store.set_error(job_id=job.id, error="boom")

    state = store.get_by_id(job_id=job.id)
    assert state is not None
    assert state.status == JobStatus.running
    assert state.progress == 42
    assert "hello" in list(state.logs)
    assert state.output_path == "/tmp/out.mp4"
    assert state.error == "boom"


def test_job_store_append_log_thread_safe():
    store = JobStore()
    job = store.create_job(input_path="/tmp/a.mp4")

    def worker(i: int) -> None:
        store.append_log(job_id=job.id, message=f"line-{i}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    state = store.get_by_id(job_id=job.id)
    assert state is not None
    logs = list(state.logs)
    assert any(line.startswith("line-") for line in logs)
