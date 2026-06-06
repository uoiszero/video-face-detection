from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


def create_app() -> FastAPI:
    """
    创建 WebUI 的 FastAPI 应用。

    - 使用 Jinja2Templates 渲染模板
    - 若存在 vfd/webui/static 目录，则自动挂载到 /static
    """

    base_dir = Path(__file__).resolve().parent
    templates = Jinja2Templates(directory=str(base_dir / "templates"))

    app = FastAPI()

    static_dir = base_dir / "static"
    if static_dir.is_dir():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

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

    return app
