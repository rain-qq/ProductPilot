"""
图片创作师Agent - 调用LangGraph工作流执行生图
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Optional
import json

from config.settings import settings
from workflows.image_generation import ImageGenerationWorkflow


class ImageCreatorAgent(Agent):
    """AI绘画师Agent - 负责生成电商图片"""
    
    def __init__(self):
        # 初始化LangGraph工作流
        self.workflow = ImageGenerationWorkflow()
        
        super().__init__(
            role='AI绘画师',
            goal='使用Stable Diffusion或DALL-E生成商业级电商产品图片',
            backstory='''你是一位专业的AI绘画师，精通Stable Diffusion、DALL-E等AI绘画工具。

你的专长：
1. 根据精准prompt生成高质量产品图
2. 图像到图像的風格迁移和精确控制
3. 使用ControlNet实现构图锁定
4. 多轮迭代优化直到满足质量标准
5. 后期处理和图片增强

你生成的每张图片都符合商业摄影标准，可直接用于电商平台。''',
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                openai_api_key=settings.OPENAI_API_KEY
            ),
            tools=[self.generate_with_workflow]
        )
    
    def generate_with_workflow(
        self,
        prompt: str,
        negative_prompt: str = "",
        reference_image: Optional[str] = None,
        generation_mode: str = "text2img",
        quality_threshold: float = None,
        max_retries: int = None
    ) -> str:
        """
        调用LangGraph工作流生成图片
        
        Args:
            prompt: 正向提示词
            negative_prompt: 负向提示词
            reference_image: 参考图片URL (可选)
            generation_mode: 生成模式 (text2img / img2img / mixed)
            quality_threshold: 质量阈值 (默认使用配置)
            max_retries: 最大重试次数
            
        Returns:
            JSON格式的生成结果
        """
        
        try:
            # 执行LangGraph工作流
            result = self.workflow.run(
                prompt=prompt,
                negative_prompt=negative_prompt,
                reference_image=reference_image,
                mode=generation_mode,
                quality_threshold=quality_threshold or settings.QUALITY_THRESHOLD,
                max_retries=max_retries or settings.MAX_IMAGE_GENERATION_RETRIES
            )
            
            # 构造返回结果
            output = {
                "success": result.get("success", False),
                "images": result.get("generated_images", []),
                "selected_image": result.get("selected_image"),
                "quality_scores": result.get("quality_scores", []),
                "iteration_count": result.get("iteration_count", 0),
                "metadata": result.get("metadata", {})
            }
            
            if not result.get("success"):
                output["error_message"] = result.get("error_message", "生成失败")
            
            return json.dumps(output, ensure_ascii=False, indent=2)
            
        except Exception as e:
            error_result = {
                "success": False,
                "error_message": f"工作流执行失败: {str(e)}",
                "images": [],
                "quality_scores": [],
                "iteration_count": 0
            }
            return json.dumps(error_result, ensure_ascii=False, indent=2)
    
    def batch_generate(
        self,
        prompts: List[str],
        reference_image: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        批量生成图片
        
        Args:
            prompts: 提示词列表
            reference_image: 参考图片
            **kwargs: 其他参数
            
        Returns:
            JSON格式的结果列表
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            try:
                result = self.generate_with_workflow(
                    prompt=prompt,
                    reference_image=reference_image,
                    **kwargs
                )
                results.append(json.loads(result))
            except Exception as e:
                results.append({
                    "success": False,
                    "error_message": str(e),
                    "index": i
                })
        
        return json.dumps(results, ensure_ascii=False, indent=2)
