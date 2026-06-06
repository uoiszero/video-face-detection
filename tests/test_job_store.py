import pytest

from vfd.webui.job_store import JobStore


def test_job_store_single_job_only():
    store = JobStore()
    job1 = store.create_job(input_path="/tmp/a.mp4")
    assert job1.id
    with pytest.raises(RuntimeError):
        store.create_job(input_path="/tmp/b.mp4")
