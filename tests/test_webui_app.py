from fastapi.testclient import TestClient


def test_create_app_exists():
    """create_app 应该存在且可调用。"""

    from vfd.webui.app import create_app

    assert callable(create_app)


def test_get_root_returns_200_and_contains_form_keyword():
    """GET / 应返回 200 且返回内容包含表单关键字。"""

    from vfd.webui.app import create_app

    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert "<form" in resp.text.lower()
