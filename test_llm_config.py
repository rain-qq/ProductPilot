"""
快速测试脚本 - 验证LLM配置
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from services.llm_service import LLMService
from config.settings import settings
from loguru import logger

def test_llm_configuration():
    """测试LLM配置是否正确"""
    print("=" * 60)
    print("ProductPilot LLM 配置测试")
    print("=" * 60)
    
    # 显示配置信息
    print("\n📋 当前配置:")
    print(f"  - OpenAI Model: {settings.OPENAI_MODEL}")
    print(f"  - Gemini Text Model: {settings.GEMINI_MODEL}")
    print(f"  - Gemini Image Model: {settings.GEMINI_IMAGE_MODEL}")
    print(f"  - OpenAI API Key: {'✓' if settings.OPENAI_API_KEY else '✗'}")
    print(f"  - Google API Key: {'✓' if settings.GOOGLE_API_KEY else '✗'}")
    
    # 初始化LLM服务
    print("\n🔧 初始化LLM服务...")
    try:
        llm_service = LLMService()
        print("✓ LLM服务初始化成功")
    except Exception as e:
        print(f"✗ LLM服务初始化失败: {e}")
        return False
    
    # 测试OpenAI LLM（用于文本任务）
    print("\n🤖 测试OpenAI LLM (文本任务)...")
    try:
        openai_llm = llm_service.get_llm("openai")
        print(f"✓ OpenAI LLM 可用: {openai_llm.model_name if hasattr(openai_llm, 'model_name') else 'Unknown'}")
    except Exception as e:
        print(f"✗ OpenAI LLM 不可用: {e}")
    
    # 测试Gemini Image LLM（用于图片生成）
    print("\n🎨 测试Gemini Image LLM (图片生成)...")
    try:
        gemini_image_llm = llm_service.get_llm("gemini_image", use_case="image")
        print(f"✓ Gemini Image LLM 可用: {gemini_image_llm.model if hasattr(gemini_image_llm, 'model') else 'Unknown'}")
    except Exception as e:
        print(f"✗ Gemini Image LLM 不可用: {e}")
    
    # 测试自动选择（文本任务应该选OpenAI）
    print("\n🔄 测试自动选择 (文本任务)...")
    try:
        auto_llm_text = llm_service.get_llm("auto", use_case="text")
        model_name = auto_llm_text.model_name if hasattr(auto_llm_text, 'model_name') else (auto_llm_text.model if hasattr(auto_llm_text, 'model') else 'Unknown')
        print(f"✓ 自动选择的文本LLM: {model_name}")
    except Exception as e:
        print(f"✗ 自动选择失败: {e}")
    
    # 测试自动选择（图片任务应该选Gemini Image）
    print("\n🔄 测试自动选择 (图片任务)...")
    try:
        auto_llm_image = llm_service.get_llm("auto", use_case="image")
        model_name = auto_llm_image.model if hasattr(auto_llm_image, 'model') else 'Unknown'
        print(f"✓ 自动选择的图片LLM: {model_name}")
    except Exception as e:
        print(f"✗ 自动选择失败: {e}")
    
    # 显示可用的提供商
    print("\n📊 可用的LLM提供商:")
    providers = llm_service.get_available_providers()
    for provider in providers:
        print(f"  ✓ {provider}")
    
    print("\n" + "=" * 60)
    print("✅ 配置测试完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    test_llm_configuration()
