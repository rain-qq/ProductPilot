"""
ProductPilot 使用示例
演示如何使用CrewAI + LangGraph混合架构生成电商图片
"""
import json
from models.schemas import ProductInfo, GenerationMode, ImageGenerationRequest
from agents.product_analyst import ProductAnalystAgent
from agents.prompt_engineer import PromptEngineerAgent
from agents.image_creator import ImageCreatorAgent
from agents.quality_reviewer import QualityReviewerAgent
from crewai import Crew, Process, Task


def example_1_text_to_image():
    """
    示例1: 纯提示词生图 (text2img)
    """
    print("=" * 60)
    print("示例1: 纯提示词生图")
    print("=" * 60)
    
    # 定义产品信息
    product_info = ProductInfo(
        name="高端蓝牙耳机",
        description="黑色磨砂质感，无线降噪耳机，悬浮展示",
        category="数码配件",
        target_audience="商务人士、音乐爱好者",
        key_features=["主动降噪", "40小时续航", "HiFi音质"]
    )
    
    # 创建团队
    engineer = PromptEngineerAgent()
    creator = ImageCreatorAgent()
    reviewer = QualityReviewerAgent()
    
    # 任务1: 优化提示词
    prompt_task = Task(
        description=f"""
为以下产品生成AI绘画提示词：
产品名称: {product_info.name}
产品描述: {product_info.description}
特点: {', '.join(product_info.key_features)}

要求：商业级电商产品图，高质量，专业摄影风格。
""",
        agent=engineer,
        expected_output="JSON格式的优化提示词"
    )
    
    # 任务2: 生成图片
    generation_task = Task(
        description=f"""
根据提示词生成电商图片：
提示词: {{prompt_task.output}}
生成模式: text2img
质量阈值: 0.8
""",
        agent=creator,
        context=[prompt_task],
        expected_output="生成的图片URL和质量评分"
    )
    
    # 任务3: 质量审核
    review_task = Task(
        description="审核生成图片的质量",
        agent=reviewer,
        context=[generation_task],
        expected_output="质量评估报告"
    )
    
    # 执行
    crew = Crew(
        agents=[engineer, creator, reviewer],
        tasks=[prompt_task, generation_task, review_task],
        process=Process.sequential,
        verbose=2
    )
    
    result = crew.kickoff()
    print("\n生成结果:")
    print(result)
    

def example_2_image_to_image():
    """
    示例2: 参照产品生图 (img2img)
    """
    print("\n" + "=" * 60)
    print("示例2: 参照产品生图")
    print("=" * 60)
    
    # 参考图片URL (实际使用时替换为真实URL)
    reference_url = "https://example.com/reference_product.jpg"
    
    product_info = ProductInfo(
        name="运动鞋",
        description="类似参考图片风格的跑步鞋，白色透气",
        reference_image_url=reference_url
    )
    
    # 创建团队
    analyst = ProductAnalystAgent()
    engineer = PromptEngineerAgent()
    creator = ImageCreatorAgent()
    
    # 任务1: 分析参考产品
    analysis_task = Task(
        description=f"分析参考图片的视觉特征: {reference_url}",
        agent=analyst,
        expected_output="结构化的视觉分析报告"
    )
    
    # 任务2: 基于分析生成提示词
    prompt_task = Task(
        description=f"""
根据参考分析和产品描述生成提示词：
- 参考分析: {{analysis_task.output}}
- 新产品描述: {product_info.description}

保持参考产品的成功设计元素，适配新产品特性。
""",
        agent=engineer,
        context=[analysis_task],
        expected_output="优化的提示词JSON"
    )
    
    # 任务3: 生成图片 (img2img模式)
    generation_task = Task(
        description=f"""
使用img2img模式生成图片：
- 提示词: {{prompt_task.output}}
- 参考图片: {reference_url}
- 模式: img2img
""",
        agent=creator,
        context=[prompt_task],
        expected_output="生成的图片列表"
    )
    
    crew = Crew(
        agents=[analyst, engineer, creator],
        tasks=[analysis_task, prompt_task, generation_task],
        process=Process.sequential,
        verbose=2
    )
    
    result = crew.kickoff()
    print("\n生成结果:")
    print(result)


def example_3_mixed_mode():
    """
    示例3: 混合模式 (mixed - 推荐)
    结合参考图片和提示词的优势
    """
    print("\n" + "=" * 60)
    print("示例3: 混合模式生图 (推荐)")
    print("=" * 60)
    
    product_info = ProductInfo(
        name="智能手表",
        description="科技感强的智能手表，黑色表带，圆形表盘",
        category="智能穿戴",
        key_features=["AMOLED屏幕", "心率监测", "防水"],
        reference_image_url="https://example.com/smartwatch_ref.jpg"
    )
    
    # 直接使用ImageCreator的工作流接口
    creator = ImageCreatorAgent()
    
    # 先优化提示词
    engineer = PromptEngineerAgent()
    prompt_result = engineer.optimize_prompt(
        user_input=f"{product_info.name} - {product_info.description}",
        reference_analysis=None
    )
    
    prompt_data = json.loads(prompt_result)
    
    print(f"\n优化的提示词:")
    print(prompt_data.get("positive_prompt", "")[:200] + "...")
    
    # 调用工作流生成
    result = creator.generate_with_workflow(
        prompt=prompt_data["positive_prompt"],
        negative_prompt=prompt_data.get("negative_prompt", ""),
        reference_image=product_info.reference_image_url,
        generation_mode="mixed",
        quality_threshold=0.8,
        max_retries=3
    )
    
    print("\n生成结果:")
    print(result)


def example_4_direct_workflow():
    """
    示例4: 直接使用LangGraph工作流
    适合需要精细控制的场景
    """
    print("\n" + "=" * 60)
    print("示例4: 直接使用LangGraph工作流")
    print("=" * 60)
    
    from workflows.image_generation import ImageGenerationWorkflow
    
    workflow = ImageGenerationWorkflow()
    
    # 执行工作流
    result = workflow.run(
        prompt="professional product photo of wireless earbuds, black matte, floating, studio lighting, 8k",
        negative_prompt="blurry, low quality, distorted",
        reference_image=None,
        mode="text2img",
        quality_threshold=0.8,
        max_retries=3
    )
    
    print(f"\n工作流执行结果:")
    print(f"成功: {result.get('success')}")
    print(f"生成图片数: {len(result.get('generated_images', []))}")
    print(f"迭代次数: {result.get('iteration_count')}")
    print(f"最佳评分: {max(result.get('quality_scores', [0])):.2f}")


if __name__ == "__main__":
    # 运行示例
    print("ProductPilot - 电商图片生成系统\n")
    
    # 注意: 运行示例前请确保:
    # 1. 已安装所有依赖
    # 2. 配置了.env文件 (特别是OPENAI_API_KEY)
    # 3. Stable Diffusion WebUI正在运行 (如果使用SD)
    
    try:
        # 选择要运行的示例
        example_4_direct_workflow()
        
        # 取消注释以运行其他示例
        # example_1_text_to_image()
        # example_2_image_to_image()
        # example_3_mixed_mode()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n请确保:")
        print("1. 已复制 .env.example 为 .env 并填写API密钥")
        print("2. 已安装所有依赖: pip install -r requirements.txt")
        print("3. Stable Diffusion WebUI正在运行 (如使用)")
