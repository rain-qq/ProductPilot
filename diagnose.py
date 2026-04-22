"""
快速诊断脚本 - 检查 Gemini 配置和依赖
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("ProductPilot 诊断工具")
print("=" * 60)

# 1. 检查依赖
print("\n1️⃣ 检查依赖包...")
try:
    import google.generativeai as genai
    print(f"   ✓ google-generativeai 已安装 (版本: {getattr(genai, '__version__', 'unknown')})")
except ImportError as e:
    print(f"   ✗ google-generativeai 未安装: {e}")
    print("   💡 请运行: pip install google-generativeai")

try:
    from google.genai import types
    print(f"   ✓ google.genai.types 可用 (新版API)")
except ImportError:
    print(f"   ⚠ google.genai.types 不可用 (将使用旧版API)")

# 2. 检查配置
print("\n2️⃣ 检查环境变量配置...")
from config.settings import settings

if settings.GOOGLE_API_KEY:
    print(f"   ✓ GOOGLE_API_KEY 已配置")
else:
    print(f"   ✗ GOOGLE_API_KEY 未配置")

print(f"   📌 GEMINI_IMAGE_MODEL = {settings.GEMINI_IMAGE_MODEL}")

# 3. 测试 ImageService 初始化
print("\n3️⃣ 测试 ImageService 初始化...")
try:
    from services.image_service import ImageService
    service = ImageService()
    
    if service.gemini_client:
        print(f"   ✓ Gemini 客户端初始化成功")
    else:
        print(f"   ✗ Gemini 客户端初始化失败")
        
    if service.minio_client:
        print(f"   ✓ MinIO 客户端初始化成功")
    else:
        print(f"   ⚠ MinIO 客户端不可用")
        
except Exception as e:
    print(f"   ✗ ImageService 初始化失败: {e}")
    import traceback
    traceback.print_exc()

# 4. 检查 SD WebUI 状态
print("\n4️⃣ 检查 Stable Diffusion WebUI...")
if settings.SD_WEBUI_URL:
    print(f"   📌 SD_WEBUI_URL = {settings.SD_WEBUI_URL}")
    import requests
    try:
        response = requests.get(f"{settings.SD_WEBUI_URL}/sdapi/v1/sd-models", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ SD WebUI 可访问")
        else:
            print(f"   ⚠ SD WebUI 返回异常状态码: {response.status_code}")
    except Exception as e:
        print(f"   ✗ SD WebUI 无法访问: {e}")
        print(f"   💡 如果不使用 SD WebUI，可以忽略此警告")
else:
    print(f"   ⚠ SD_WEBUI_URL 未配置")

print("\n" + "=" * 60)
print("✅ 诊断完成！")
print("=" * 60)
print("\n💡 提示:")
print("   - 如果 Gemini 客户端正常，图片生成将使用 Gemini API")
print("   - 如果 SD WebUI 未运行，系统会自动使用 Gemini")
print("   - 确保 .env 文件中 GOOGLE_API_KEY 配置正确")
