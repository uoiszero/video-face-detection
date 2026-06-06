from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Callable, Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from vfd.job_runner import run_job as default_runner
from vfd.job_types import JobParams, JobStatus, normalize_bitrate, normalize_output_resolution
from vfd.webui.job_store import JobStore


def create_app(
    runner: Optional[
        Callable[
            [str, JobParams, str, Callable[[str], None], Callable[[int, int], bool]],
            object,
        ]
    ] = None,
    run_async: bool = True,
) -> FastAPI:
    """
    创建 WebUI 的 FastAPI 应用。

    - 使用 Jinja2Templates 渲染模板
    - 若存在 vfd/webui/static 目录，则自动挂载到 /static
    - runner/run_async 用于可测性：测试中可注入 fake runner，并通过 run_async=False 让任务同步执行
    """

    base_dir = Path(__file__).resolve().parent
    templates = Jinja2Templates(directory=str(base_dir / "templates"))

    app = FastAPI()
    store = JobStore()
    runner_func = default_runner if runner is None else runner
    outputs_dir = str(Path.cwd() / "outputs")

    static_dir = base_dir / "static"
    if static_dir.is_dir():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    def _parse_bool(value: str) -> bool:
        """
        解析布尔表单字段（兼容 true/false 与 on/off）。
        """

        v = value.strip().lower()
        return v in ("1", "true", "on", "yes")

    def _run_job(job_id: str, params: JobParams) -> None:
        """
        执行单次 job，并将进度/日志/状态回写到 JobStore。
        """

        store.update_status(job_id=job_id, status=JobStatus.running)

        def log(message: str) -> None:
            """
            runner 的日志回调，将日志写入 JobStore。
            """

            store.append_log(job_id=job_id, message=message)

        def progress(current: int, total: int) -> bool:
            """
            runner 的进度回调，将进度归一化为 0-100 写入 JobStore。
            """

            pct = 0 if total <= 0 else int(current / total * 100)
            store.update_progress(job_id=job_id, progress=pct)
            return True

        try:
            result = runner_func(
                job_id,
                params,
                outputs_dir,
                log,
                progress,
            )
            output_path = getattr(result, "output_path", None)
            if isinstance(output_path, str):
                store.set_output_path(job_id=job_id, output_path=output_path)
            store.update_progress(job_id=job_id, progress=100)
            store.update_status(job_id=job_id, status=JobStatus.succeeded)
        except Exception as e:
            store.set_error(job_id=job_id, error=str(e))
            store.update_status(job_id=job_id, status=JobStatus.failed)

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> HTMLResponse:
        """
        渲染首页（最小表单页面）。
        """

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"request": request},
        )

    @app.get("/jobs/{job_id}", response_class=HTMLResponse)
    def job_page(request: Request, job_id: str) -> HTMLResponse:
        """
        渲染单个 job 页面。
        """

        snap = store.snapshot(job_id=job_id)
        if snap is None:
            raise HTTPException(status_code=404, detail="job not found")

        return templates.TemplateResponse(
            request=request,
            name="job.html",
            context={"request": request, "job_id": job_id},
        )

    @app.post("/jobs")
    def create_job(
        input_path: str = Form(...),
        detector: str = Form(...),
        deepface_backend: str = Form("opencv"),
        continuation_frames: int = Form(5),
        output_resolution: str = Form("original"),
        video_bitrate: str = Form(""),
        codec: str = Form("auto"),
        apply_mosaic: str = Form("false"),
        mosaic_size: int = Form(15),
    ) -> JSONResponse:
        """
        创建并启动一个 job。
        """

        try:
            params = JobParams(
                input_path=input_path,
                detector=detector,
                deepface_backend=deepface_backend,
                continuation_frames=int(continuation_frames),
                apply_mosaic=_parse_bool(apply_mosaic),
                mosaic_size=int(mosaic_size),
                output_resolution=normalize_output_resolution(output_resolution),
                video_bitrate=normalize_bitrate(video_bitrate),
                codec=codec,
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e

        try:
            job = store.create_job(input_path=input_path)
        except RuntimeError as e:
            raise HTTPException(status_code=409, detail=str(e)) from e

        store.append_log(job_id=job.id, message=f"detector={params.detector}")
        store.append_log(job_id=job.id, message=f"continuation_frames={params.continuation_frames}")

        if run_async:
            t = threading.Thread(target=_run_job, args=(job.id, params), daemon=True)
            t.start()
        else:
            _run_job(job.id, params)

        return JSONResponse({"id": job.id, "url": f"/jobs/{job.id}"})

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str) -> JSONResponse:
        """
        获取 job 状态 JSON。
        """

        snap = store.snapshot(job_id=job_id)
        if snap is None:
            raise HTTPException(status_code=404, detail="job not found")
        return JSONResponse(snap)

    @app.get("/api/jobs/{job_id}/events")
    def job_events(job_id: str) -> StreamingResponse:
        """
        返回 job 事件流（SSE）。
        """

        def gen() -> object:
            """
            SSE 生成器：周期性输出 snapshot，直到 job 成功/失败。
            """

            while True:
                snap = store.snapshot(job_id=job_id)
                if snap is None:
                    payload = json.dumps({"error": "job not found"}, ensure_ascii=False)
                    yield f"event: error\ndata: {payload}\n\n"
                    return

                payload = json.dumps(snap, ensure_ascii=False)
                yield f"event: snapshot\ndata: {payload}\n\n"

                if snap["status"] in (JobStatus.succeeded.value, JobStatus.failed.value):
                    return

                time.sleep(0.2)

        return StreamingResponse(gen(), media_type="text/event-stream")

    return app
