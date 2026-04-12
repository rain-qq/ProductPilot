"""
图片创作师Agent - 调用LangGraph工作流执行生图
支持电商平台特定规范
"""
from crewai import Agent
from langchain.tools import tool
from typing import Dict, Any, List, Optional
import json

from config.settings import settings
from workflows.image_generation import ImageGenerationWorkflow
from services.llm_service import LLMService


class ImageCreatorAgent(Agent):
    """AI绘画师Agent - 负责生成电商图片（支持多平台规范）"""
    
    def __init__(self):
        # 使用LLMService获取Gemini Image LLM用于图片生成相关任务
        llm_service = LLMService()
        llm = llm_service.get_llm("gemini_image", use_case="image")
        
        super().__init__(
            role='AI绘画师',
            goal='使用Stable Diffusion或DALL-E生成符合电商平台规范的商业级产品图片',
            backstory='''你是一位专业的AI绘画师，精通Stable Diffusion、DALL-E等AI绘画工具。

你的专长：
1. 根据精准prompt生成高质量产品图
2. 图像到图像的風格迁移和精确控制
3. 使用ControlNet实现构图锁定
4. 多轮迭代优化直到满足质量标准
5. 后期处理和图片增强
6. 熟悉Amazon、Temu等跨境电商平台的图片规范和要求

你生成的每张图片都符合目标平台的商业摄影标准，可直接用于电商平台。''',
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[self._create_generate_tool()]
        )
        
        # 在super().__init__()之后初始化工作流（避免Pydantic初始化问题）
        self._workflow = ImageGenerationWorkflow()
    
    @property
    def workflow(self):
        """获取工作流实例"""
        return self._workflow
    
    def _create_generate_tool(self):
        """创建CrewAI兼容的图片生成工具"""
        @tool("generate_with_workflow")
        def generate_with_workflow(
            prompt: str,
            negative_prompt: str = "",
            reference_image: Optional[str] = None,
            generation_mode: str = "text2img",
            platform: str = "default",
            quality_threshold: float = None,
            max_retries: int = None
        ) -> str:
            """
            调用LangGraph工作流生成图片（支持平台特定规范）
            
            Args:
                prompt: 正向提示词
                negative_prompt: 负向提示词
                reference_image: 参考图片URL (可选)
                generation_mode: 生成模式 (text2img / img2img / mixed)
                platform: 目标平台 (amazon / temu / default)
                quality_threshold: 质量阈值 (默认使用配置)
                max_retries: 最大重试次数
                
            Returns:
                JSON格式的生成结果
            """
            
            try:
                # 执行LangGraph工作流
                result = self._workflow.run(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    reference_image=reference_image,
                    mode=generation_mode,
                    platform=platform,
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
                    "platform": result.get("metadata", {}).get("platform", platform),
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
                    "iteration_count": 0,
                    "platform": platform
                }
                return json.dumps(error_result, ensure_ascii=False, indent=2)
        
        return generate_with_workflow
    
    def batch_generate(
        self,
        prompts: List[str],
        reference_image: Optional[str] = None,
        platform: str = "default",
        **kwargs
    ) -> str:
        """
        批量生成图片
        
        Args:
            prompts: 提示词列表
            reference_image: 参考图片
            platform: 目标平台
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
                    platform=platform,
                    **kwargs
                )
                results.append(json.loads(result))
            except Exception as e:
                results.append({
                    "success": False,
                    "error_message": str(e),
                    "index": i,
                    "platform": platform
                })
        
        return json.dumps(results, ensure_ascii=False, indent=2)
