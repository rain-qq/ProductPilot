"""
快速测试脚本 - 验证配置是否正确
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_config():
    """测试配置加载"""
    print("="*60)
    print("测试配置加载")
    print("="*60)
    
    try:
        from config.settings import settings
        print("✅ 配置加载成功")
        print(f"  - Gemini API Key: {settings.GOOGLE_API_KEY[:15] if settings.GOOGLE_API_KEY else 'None'}...")
        print(f"  - 选定模型: {settings.GEMINI_MODEL}")
        print(f"  - 应用环境: {settings.APP_ENV}")
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False


def test_llm():
    """测试LLM初始化"""
    print("\n" + "="*60)
    print("测试 LLM 初始化")
    print("="*60)
    
    try:
        from services.llm_service import LLMService
        
        llm_service = LLMService()
        providers = llm_service.get_available_providers()
        
        print(f"✅ LLM服务初始化成功")
        print(f"  - 可用提供商: {providers}")
        
        if "gemini" in providers:
            gemini_llm = llm_service.get_llm(provider="gemini")
            print(f"  - Gemini LLM: ✅ 可用")
        else:
            print(f"  - Gemini LLM: ❌ 未配置")
            
        return True
    except Exception as e:
        print(f"❌ LLM初始化失败: {e}")
        return False


def test_agents():
    """测试Agents导入"""
    print("\n" + "="*60)
    print("测试 Agents 导入")
    print("="*60)
    
    try:
        from agents.product_analyst import ProductAnalystAgent
        from agents.prompt_engineer import PromptEngineerAgent
        from agents.image_creator import ImageCreatorAgent
        from agents.quality_reviewer import QualityReviewerAgent
        
        print("✅ 所有 Agents 导入成功")
        print("  - ProductAnalystAgent")
        print("  - PromptEngineerAgent")
        print("  - ImageCreatorAgent")
        print("  - QualityReviewerAgent")
        return True
    except Exception as e:
        print(f"❌ Agents 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_workflow():
    """测试工作流导入"""
    print("\n" + "="*60)
    print("测试 Workflow 导入")
    print("="*60)
    
    try:
        from workflows.image_generation import ImageGenerationWorkflow
        
        workflow = ImageGenerationWorkflow()
        print("✅ 工作流导入成功")
        return True
    except Exception as e:
        print(f"❌ 工作流导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 ProductPilot 项目测试\n")
    
    results = []
    
    # 运行测试
    results.append(("配置加载", test_config()))
    results.append(("LLM初始化", test_llm()))
    results.append(("Agents导入", test_agents()))
    results.append(("Workflow导入", test_workflow()))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！项目可以正常运行！")
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查错误信息")
