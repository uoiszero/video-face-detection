import pytest

from vfd.job_runner import validate_input_path


def test_validate_input_path_missing_file() -> None:
    """当输入文件不存在时，应抛出 FileNotFoundError，便于上层直接展示错误信息。"""
    with pytest.raises(FileNotFoundError):
        validate_input_path("/path/does/not/exist.mp4")
