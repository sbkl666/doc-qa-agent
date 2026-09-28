@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo 没有找到虚拟环境，请先在此目录完成过一次依赖安装。
    pause
    exit /b 1
)

echo 正在启动文档问答，浏览器稍后会打开 http://localhost:8501
echo 关闭本窗口即停止服务。
echo.

".venv\Scripts\python.exe" -m streamlit run app.py --server.headless false
if errorlevel 1 (
    echo.
    echo 启动失败，请把上面的报错发给我。
    pause
)
