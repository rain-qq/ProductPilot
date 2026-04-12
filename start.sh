#!/bin/bash
# ProductPilot 快速启动脚本 (Linux/Mac)

echo "========================================"
echo "  ProductPilot 启动脚本"
echo "========================================"
echo ""

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "[1/3] 创建虚拟环境..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "错误: 创建虚拟环境失败"
        exit 1
    fi
fi

# 激活虚拟环境
echo "[2/3] 激活虚拟环境..."
source .venv/bin/activate

# 检查依赖
echo "[3/3] 检查依赖..."
if ! pip show crewai &> /dev/null; then
    echo "首次运行，安装依赖..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 安装依赖失败"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "  环境准备就绪！"
echo "========================================"
echo ""
echo "请选择要运行的命令："
echo ""
echo "1. 测试配置          - python test_quick.py"
echo "2. 运行Gemini示例    - python examples/gemini_example.py"
echo "3. 运行基础示例      - python examples/basic_usage.py"
echo "4. 启动API服务器     - python main.py"
echo "5. 打开命令行        - bash"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1) python test_quick.py ;;
    2) python examples/gemini_example.py ;;
    3) python examples/basic_usage.py ;;
    4) python main.py ;;
    5) bash ;;
    *) echo "无效选项" ;;
esac
