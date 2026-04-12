@echo off
REM ProductPilot 快速启动脚本 (Windows)

echo ========================================
echo   ProductPilot 启动脚本
echo ========================================
echo.

REM 检查虚拟环境是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] 创建虚拟环境...
    python -m venv .venv
    if errorlevel 1 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
echo [2/3] 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 检查依赖
echo [3/3] 检查依赖...
pip show crewai >nul 2>&1
if errorlevel 1 (
    echo 首次运行，安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 安装依赖失败
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo   环境准备就绪！
echo ========================================
echo.
echo 请选择要运行的命令：
echo.
echo 1. 测试配置          - python test_quick.py
echo 2. 运行Gemini示例    - python examples/gemini_example.py
echo 3. 运行基础示例      - python examples/basic_usage.py
echo 4. 启动API服务器     - python main.py
echo 5. 打开命令行        - cmd
echo.
set /p choice=请输入选项 (1-5): 

if "%choice%"=="1" goto test
if "%choice%"=="2" goto gemini
if "%choice%"=="3" goto basic
if "%choice%"=="4" goto server
if "%choice%"=="5" goto shell
goto end

:test
python test_quick.py
goto end

:gemini
python examples/gemini_example.py
goto end

:basic
python examples/basic_usage.py
goto end

:server
python main.py
goto end

:shell
cmd

:end
echo.
echo 会话结束
pause
