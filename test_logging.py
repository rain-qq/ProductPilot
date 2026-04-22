"""
测试日志配置 - 验证 Windows 环境下日志编码是否正常
"""
import sys
from pathlib import Path
import os

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("="*60)
print("日志配置测试")
print("="*60)
print(f"操作系统: {os.name}")
print(f"Python 版本: {sys.version}")
print()

# 设置环境变量 (模拟 main.py 的行为)
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    print("[INFO] 已设置 PYTHONIOENCODING=utf-8")

# 测试1: 导入 Loguru
print("\n[TEST] 1. 导入 Loguru...")
try:
    from loguru import logger
    print("[OK] Loguru 导入成功")
except Exception as e:
    print(f"[FAIL] Loguru 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试2: 记录包含中文的日志
print("\n[TEST] 2. 测试中文日志...")
try:
    logger.info("这是一条测试日志 - 中文内容")
    logger.info("[TASK] 任务开始")
    logger.info("[OK] 操作成功")
    logger.warning("[WARN] 警告信息")
    logger.error("[ERROR] 错误信息")
    print("[OK] 中文日志测试通过")
except Exception as e:
    print(f"[FAIL] 中文日志测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3: 验证不包含 emoji
print("\n[TEST] 3. 检查代码中是否还有 emoji...")
emoji_chars = ['📋', '✅', '👥', '🚀', '🎯', '⚠️', '❌', '🔄', '🔍', '💡', '📊', '✨']
found_emoji = []

# 检查关键文件
key_files = [
    'main.py',
    'api/routes.py',
    'agents/image_creator.py',
    'test_minimal.py'
]

for file_name in key_files:
    file_path = project_root / file_name
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for emoji in emoji_chars:
                if emoji in content:
                    found_emoji.append(f"{file_name}: 发现 {emoji}")

if found_emoji:
    print("[WARN] 以下文件中仍包含 emoji:")
    for item in found_emoji:
        print(f"  - {item}")
else:
    print("[OK] 关键文件中未发现 emoji 字符")

print("\n" + "="*60)
print("测试完成!")
print("="*60)
print("\n如果看到 '[OK]' 且没有报错,说明日志配置正常。")
print("现在可以安全运行: python main.py")
