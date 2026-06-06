from vfd.job_types import normalize_bitrate, normalize_output_resolution


def test_normalize_bitrate_accepts_mbps_int():
    assert normalize_bitrate("6") == "6M"


def test_normalize_bitrate_accepts_ffmpeg_style():
    assert normalize_bitrate("6000k") == "6000k"
    assert normalize_bitrate("6M") == "6M"


def test_normalize_output_resolution_presets():
    assert normalize_output_resolution("original") is None
    assert normalize_output_resolution("720p") == (1280, 720)
    assert normalize_output_resolution("1080p") == (1920, 1080)


def test_normalize_output_resolution_custom():
    assert normalize_output_resolution("1024x768") == (1024, 768)
