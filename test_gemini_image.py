"""
测试 Gemini 图片生成功能
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from services.image_service import ImageService
from config.settings import settings
from loguru import logger

def test_gemini_image_generation():
    """测试 Gemini 图片生成"""
    print("=" * 60)
    print("Gemini 图片生成测试")
    print("=" * 60)
    
    # 检查配置
    print("\n📋 配置检查:")
    print(f"  - GOOGLE_API_KEY: {'✓' if settings.GOOGLE_API_KEY else '✗'}")
    print(f"  - GEMINI_IMAGE_MODEL: {settings.GEMINI_IMAGE_MODEL}")
    
    # 初始化服务
    print("\n🔧 初始化 ImageService...")
    try:
        service = ImageService()
        print("✓ ImageService 初始化成功")
        
        if service.gemini_client:
            print("✓ Gemini GenAI 客户端可用")
        else:
            print("✗ Gemini GenAI 客户端不可用")
            return False
            
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        return False
    
    # 测试图片生成
    print("\n🎨 测试 Gemini 图片生成...")
    test_prompt = "A white minimalist hanger on pure white background, professional product photography, studio lighting, high quality, commercial grade"
    
    try:
        print(f"  提示词: {test_prompt[:80]}...")
        images = service.text_to_image(
            prompt=test_prompt,
            use_gemini=True,
            batch_size=1
        )
        
        print(f"\n✅ 成功生成 {len(images)} 张图片!")
        
        # 显示图片信息
        for i, img_url in enumerate(images):
            # 计算大小
            if img_url.startswith("data:"):
                base64_data = img_url.split(",")[1]
                size_kb = len(base64_data) * 3 / 4 / 1024  # 估算大小
                print(f"  图片 {i+1}: {size_kb:.1f} KB")
            else:
                print(f"  图片 {i+1}: URL 格式")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_gemini_image_generation()
    print("\n" + "=" * 60)
    if success:
        print("✅ 测试通过！Gemini 图片生成工作正常")
    else:
        print("❌ 测试失败，请检查配置和网络连接")
    print("=" * 60)
