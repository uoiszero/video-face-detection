@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 一键打码脚本 (Windows批处理版本)
REM 使用混合检测器、侧脸检测优化、延续15帧的配置进行视频人脸打码
REM
REM 使用方法:
REM   quick_mosaic.bat input_video.mp4
REM   
REM 输出文件将自动命名为: input_video_out_20231201_143022.mp4

REM 检查参数
if "%~1"=="" (
    echo ❌ 参数错误!
    echo.
    call :print_usage
    pause
    exit /b 1
)

set "input_file=%~1"

REM 检查输入文件是否存在
if not exist "%input_file%" (
    echo ❌ 输入文件不存在: %input_file%
    pause
    exit /b 1
)

REM 检查视频格式
call :check_video_format "%input_file%"
if errorlevel 1 exit /b 1

REM 检查依赖
call :check_dependencies
if errorlevel 1 (
    pause
    exit /b 1
)

REM 生成输出文件名
call :get_output_filename "%input_file%" output_file

REM 检查输出文件是否已存在
if exist "%output_file%" (
    echo ⚠️  输出文件已存在: %output_file%
    set /p "overwrite=是否覆盖? (y/N): "
    if /i not "!overwrite!"=="y" if /i not "!overwrite!"=="yes" if /i not "!overwrite!"=="是" (
        echo 已取消处理
        pause
        exit /b 0
    )
)

REM 执行打码处理
call :run_mosaic "%input_file%" "%output_file%"
if errorlevel 1 (
    echo.
    echo 💥 处理失败!
    pause
    exit /b 1
) else (
    echo.
    echo 🎉 一键打码完成!
    echo 📁 输出文件: %output_file%
    pause
    exit /b 0
)

REM ==================== 函数定义 ====================

:get_output_filename
REM 生成输出文件名
set "input_path=%~1"
set "input_dir=%~dp1"
set "input_name=%~n1"
set "input_ext=%~x1"

REM 获取当前时间戳
for /f "tokens=1-6 delims=/:. " %%a in ("%date% %time%") do (
    set "timestamp=%%c%%a%%b_%%d%%e%%f"
)
REM 移除时间戳中的空格
set "timestamp=%timestamp: =0%"

REM 构建输出文件名
set "%~2=%input_dir%%input_name%_out_%timestamp%%input_ext%"
goto :eof

:check_dependencies
REM 检查依赖文件
set "missing_files="

if not exist "..\main.py" (
    set "missing_files=!missing_files! ..\main.py"
)

if not exist "..\models\face_detection_yunet_2023mar.onnx" (
    set "missing_files=!missing_files! ..\models\face_detection_yunet_2023mar.onnx"
)

if not "!missing_files!"=="" (
    echo ❌ 缺少必要文件:
    for %%f in (!missing_files!) do (
        echo    - %%f
    )
    echo.
    echo ℹ️  请先运行安装脚本: python install_dependencies.py
    exit /b 1
)

exit /b 0

:check_video_format
REM 检查视频文件格式
set "input_file=%~1"
set "extension=%~x1"
set "extension=%extension:~1%"
set "extension=%extension%"

REM 转换为小写
for %%i in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    call set "extension=%%extension:%%i=%%i%%"
)
for %%i in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do (
    call set "extension=%%extension:%%i=%%i%%"
)

REM 检查是否为支持的格式
set "supported=0"
for %%f in (mp4 avi mov mkv wmv flv webm m4v) do (
    if /i "%extension%"=="%%f" set "supported=1"
)

if "%supported%"=="0" (
    echo ⚠️  警告: %extension% 可能不是支持的视频格式
    echo 支持的格式: mp4, avi, mov, mkv, wmv, flv, webm, m4v
    set /p "continue=是否继续处理? (y/N): "
    if /i not "!continue!"=="y" if /i not "!continue!"=="yes" if /i not "!continue!"=="是" (
        echo 已取消处理
        exit /b 1
    )
)

exit /b 0

:run_mosaic
REM 执行视频打码处理
set "input_file=%~1"
set "output_file=%~2"

echo 🚀 开始处理视频: %input_file%
echo 📁 输出文件: %output_file%
echo ⚙️  使用配置: 混合检测器 + RetinaFace后端 + 延续15帧
echo.
echo ==========================================================

REM 构建并执行命令
cd ..
python main.py "%input_file%" --detector hybrid --deepface-backend retinaface --continuation-frames 15 --mosaic --output "scripts\%output_file%"
cd scripts

if errorlevel 1 (
    echo ==========================================================
    echo ❌ 处理失败
    exit /b 1
)

echo ==========================================================
echo ✅ 处理完成! 输出文件: %output_file%

REM 检查输出文件并显示大小
if exist "%output_file%" (
    for %%A in ("%output_file%") do (
        set "file_size=%%~zA"
    )
    set /a "file_size_mb=!file_size! / 1048576"
    echo 📊 文件大小: !file_size_mb! MB
) else (
    echo ⚠️  输出文件未找到，可能处理失败
    exit /b 1
)

exit /b 0

:print_usage
REM 打印使用说明
echo 🎯 一键打码脚本
echo ==================================================
echo 使用方法:
echo   quick_mosaic.bat ^<输入视频文件^>
echo.
echo 示例:
echo   quick_mosaic.bat sample.mp4
echo   quick_mosaic.bat C:\path\to\video.avi
echo.
echo 功能特性:
echo   ✅ 混合检测器 (YuNet + DeepFace)
echo   ✅ 侧脸检测优化 (RetinaFace后端)
echo   ✅ 延续打码 (15帧)
echo   ✅ 自动生成输出文件名
echo.
echo 输出文件命名规则:
echo   原文件名_out_时间戳.扩展名
echo   例: sample_out_20231201_143022.mp4
goto :eof