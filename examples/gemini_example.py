"""
Gemini API 使用示例
演示如何使用Google Gemini替代OpenAI
"""
from services.llm_service import LLMService
from langchain.prompts import ChatPromptTemplate

def test_gemini():
    """测试Gemini API"""
    
    # 初始化LLM服务
    llm_service = LLMService()
    
    # 检查可用的提供商
    providers = llm_service.get_available_providers()
    print(f"可用的LLM提供商: {providers}")
    
    if "gemini" not in providers:
        print("❌ Gemini不可用，请检查GOOGLE_API_KEY配置")
        return
    
    # 获取Gemini LLM
    gemini_llm = llm_service.get_llm(provider="gemini")
    
    # 测试对话
    print("\n" + "="*60)
    print("测试Gemini对话")
    print("="*60)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的电商产品专家"),
        ("user", "请为蓝牙耳机生成一个电商图片的提示词")
    ])
    
    chain = prompt | gemini_llm
    response = chain.invoke({})
    
    print(f"\nGemini回复:\n{response.content}")


def use_gemini_in_agents():
    """在Agent中使用Gemini"""
    from crewai import Agent
    from services.llm_service import LLMService
    
    # 初始化LLM服务
    llm_service = LLMService()
    gemini_llm = llm_service.get_llm(provider="gemini")
    
    # 创建使用Gemini的Agent
    product_expert = Agent(
        role='电商产品专家',
        goal='分析产品特点并生成营销文案',
        backstory='你是一位资深电商专家',
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm  # 使用Gemini而非默认的GPT-4
    )
    
    # 执行任务
    from crewai import Task, Crew
    
    task = Task(
        description="为智能手表生成产品卖点描述",
        agent=product_expert,
        expected_output="结构化的产品卖点列表"
    )
    
    crew = Crew(
        agents=[product_expert],
        tasks=[task],
        verbose=2
    )
    
    result = crew.kickoff()
    print(f"\nAgent执行结果:\n{result}")


if __name__ == "__main__":
    try:
        # 测试Gemini基础功能
        test_gemini()
        
        # 测试在Agent中使用
        use_gemini_in_agents()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n请确保:")
        print("1. 已在 .env 中配置 GOOGLE_API_KEY")
        print("2. 已安装依赖: pip install -r requirements.txt")
        print("3. Google API密钥有效")
