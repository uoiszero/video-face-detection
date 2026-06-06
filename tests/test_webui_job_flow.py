from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, Dict

from fastapi.testclient import TestClient

from vfd.job_types import JobParams, JobStatus
from vfd.webui.app import create_app


@dataclass(frozen=True)
class _FakeJobResult:
    output_path: str
    stats: Dict


def _fake_runner(
    job_id: str,
    params: JobParams,
    outputs_dir: str,
    log: Callable[[str], None],
    progress: Callable[[int, int], bool],
) -> _FakeJobResult:
    log(f"runner-start job_id={job_id} outputs_dir={outputs_dir}")
    progress(1, 4)
    progress(2, 4)
    progress(4, 4)
    log(f"runner-done detector={params.detector}")
    return _FakeJobResult(output_path=f"{outputs_dir}/{job_id}.mp4", stats={"ok": True})


def test_create_job_runs_and_can_query_status_success():
    app = create_app(runner=_fake_runner, run_async=False)
    client = TestClient(app)

    resp = client.post(
        "/jobs",
        data={
            "input_path": "/tmp/a.mp4",
            "detector": "yunet",
            "deepface_backend": "opencv",
            "continuation_frames": "5",
            "output_resolution": "original",
            "video_bitrate": "",
            "codec": "auto",
            "apply_mosaic": "false",
            "mosaic_size": "15",
        },
    )
    assert resp.status_code == 200
    job_id = resp.json()["id"]

    status_resp = client.get(f"/api/jobs/{job_id}")
    assert status_resp.status_code == 200
    payload = status_resp.json()
    assert payload["id"] == job_id
    assert payload["status"] == JobStatus.succeeded.value
    assert payload["output_path"].endswith(f"/{job_id}.mp4")
    assert payload["progress"] == 100
    assert any("runner-done" in line for line in payload["logs"])


def test_events_endpoint_returns_event_stream_and_has_data_field():
    app = create_app(runner=_fake_runner, run_async=False)
    client = TestClient(app)

    resp = client.post(
        "/jobs",
        data={
            "input_path": "/tmp/a.mp4",
            "detector": "yunet",
            "deepface_backend": "opencv",
            "continuation_frames": "1",
            "output_resolution": "original",
            "video_bitrate": "",
            "codec": "auto",
            "apply_mosaic": "false",
            "mosaic_size": "15",
        },
    )
    job_id = resp.json()["id"]

    events_resp = client.get(f"/api/jobs/{job_id}/events")
    assert events_resp.status_code == 200
    assert events_resp.headers["content-type"].startswith("text/event-stream")
    assert "data:" in events_resp.text

    data_lines = [line for line in events_resp.text.splitlines() if line.startswith("data:")]
    assert data_lines
    snapshot = json.loads(data_lines[-1].removeprefix("data:").strip())
    assert snapshot["id"] == job_id
    assert snapshot["status"] in (JobStatus.succeeded.value, JobStatus.failed.value)
