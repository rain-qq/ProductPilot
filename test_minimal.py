"""
最小化测试 - 只测试最基本的导入
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("="*60)
print("ProductPilot 最小化测试")
print("="*60)

# 测试1: Python版本
print(f"\n✅ Python版本: {sys.version}")

# 测试2: 环境变量文件
import os
env_file = project_root / ".env"
if env_file.exists():
    print(f"✅ .env 文件存在")
    
    # 读取并显示API Key（隐藏部分）
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
        for line in content.split('\n'):
            if line.startswith('GOOGLE_API_KEY='):
                key = line.split('=')[1]
                print(f"✅ Gemini API Key: {key[:15]}...")
            elif line.startswith('GEMINI_MODEL='):
                model = line.split('=')[1]
                print(f"✅ 模型: {model}")
else:
    print(f"❌ .env 文件不存在")

# 测试3: 尝试导入基础模块
print("\n" + "="*60)
print("测试基础模块")
print("="*60)

try:
    import pydantic
    print(f"✅ Pydantic: {pydantic.__version__}")
except ImportError as e:
    print(f"❌ Pydantic未安装: {e}")

try:
    import requests
    print(f"✅ Requests: {requests.__version__}")
except ImportError as e:
    print(f"❌ Requests未安装: {e}")

try:
    import crewai
    print(f"✅ CrewAI: {crewai.__version__}")
except ImportError as e:
    print(f"❌ CrewAI未安装: {e}")

try:
    import langgraph
    print(f"✅ LangGraph: 已安装")
except ImportError as e:
    print(f"❌ LangGraph未安装: {e}")

print("\n" + "="*60)
print("建议")
print("="*60)
print("\n如果看到很多 ❌，说明依赖还没安装完。")
print("请运行以下命令：")
print("\nWindows:")
print("  .venv\\Scripts\\activate")
print("  pip install -r requirements.txt")
print("\n等待安装完成后，再运行此测试脚本。")
print("\n或者直接使用启动脚本：")
print("  双击 start.bat")
