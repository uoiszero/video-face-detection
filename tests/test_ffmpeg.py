from vfd.ffmpeg import build_transcode_cmd


def test_build_transcode_cmd_with_scale_and_bitrate():
    cmd = build_transcode_cmd(
        input_path="/tmp/in.mp4",
        output_path="/tmp/out.mp4",
        output_resolution=(1280, 720),
        video_bitrate="6M",
        codec="h264",
    )
    joined = " ".join(cmd)
    assert "-vf" in cmd
    assert "scale=1280:720" in joined
    assert "-b:v" in cmd
    assert "6M" in cmd
    assert "libx264" in joined
