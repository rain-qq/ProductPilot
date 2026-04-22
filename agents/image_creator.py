"""
图片创作师Agent - 调用LangGraph工作流执行生图
支持电商平台特定规范
"""
from crewai import Agent
from langchain_core.tools import BaseTool
from typing import Dict, Any, List, Optional
import json

from config.settings import settings
from workflows.image_generation import ImageGenerationWorkflow
from services.llm_service import LLMService


class GenerateImageTool(BaseTool):
    """自定义工具类 - 调用LangGraph工作流生成图片"""
    
    name: str = "generate_with_workflow"
    description: str = """调用LangGraph工作流生成符合电商平台规范的图片
    
    Args:
        prompt: 正向提示词
        negative_prompt: 负向提示词
        reference_image: 参考图片URL (可选)
        generation_mode: 生成模式 (text2img / img2img / mixed)
        platform: 目标平台 (amazon / temu / default)
        quality_threshold: 质量阈值
        max_retries: 最大重试次数
    
    Returns:
        JSON格式的生成结果
    """
    
    # 这些属性将在初始化时设置
    workflow: Optional[ImageGenerationWorkflow] = None
    
    def _run(
        self,
        prompt: str,
        negative_prompt: str = "",
        reference_image: Optional[str] = None,
        generation_mode: str = "text2img",
        platform: str = "temu",
        quality_threshold: float = None,
        max_retries: int = None
    ) -> str:
        """执行工具"""
        try:
            print(f"\n{'='*80}")
            print(f"🎨 [GenerateImageTool] 开始执行")
            print(f"   - workflow initialized: {self.workflow is not None}")
            
            if not self.workflow:
                raise RuntimeError("工作流未初始化！")
            
            print(f"   - prompt length: {len(prompt)}")
            print(f"   - negative_prompt length: {len(negative_prompt) if negative_prompt else 0}")
            print(f"   - generation_mode: {generation_mode}")
            print(f"   - platform: {platform}")
            print(f"   - quality_threshold: {quality_threshold}")
            print(f"   - max_retries: {max_retries}")
            
            # 标准化 platform 参数为小写
            platform_normalized = platform.lower() if platform else "default"
            print(f"   - platform_normalized: {platform_normalized}")
            
            # 执行LangGraph工作流
            print(f"\n[START] [GenerateImageTool] 正在执行 LangGraph 工作流...")
            result = self.workflow.run(
                prompt=prompt,
                negative_prompt=negative_prompt,
                reference_image=reference_image,
                mode=generation_mode,
                platform=platform_normalized,
                quality_threshold=quality_threshold or settings.QUALITY_THRESHOLD,
                max_retries=max_retries or settings.MAX_IMAGE_GENERATION_RETRIES
            )
            print(f"[OK] [GenerateImageTool] LangGraph 工作流执行完成")
            print(f"   - success: {result.get('success')}")
            print(f"   - iteration_count: {result.get('iteration_count')}")
            print(f"{'='*80}\n")
            
            # 构造返回结果
            output = {
                "success": result.get("success", False),
                "images": result.get("generated_images", []),
                "selected_image": result.get("selected_image"),
                "quality_scores": result.get("quality_scores", []),
                "iteration_count": result.get("iteration_count", 0),
                "platform": platform_normalized,
                "metadata": result.get("metadata", {})
            }
            
            if not result.get("success"):
                output["error_message"] = result.get("error_message", "生成失败")
                print(f"[WARN] [GenerateImageTool] 生成失败: {output['error_message']}")
            else:
                print(f"[SUCCESS] [GenerateImageTool] 生成成功！图片数量: {len(output['images'])}")
            
            return json.dumps(output, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"\n[ERROR] [GenerateImageTool] 执行异常: {str(e)}")
            import traceback
            traceback.print_exc()
            error_result = {
                "success": False,
                "error_message": f"工具执行失败: {str(e)}",
                "images": [],
                "quality_scores": [],
                "iteration_count": 0,
                "platform": platform_normalized if 'platform_normalized' in locals() else "default"
            }
            return json.dumps(error_result, ensure_ascii=False, indent=2)


class ImageCreatorAgent(Agent):
    """AI绘画师Agent - 负责生成电商图片（支持多平台规范）"""
    
    def __init__(self):
        # 使用LLMService获取OpenAI LLM用于任务理解和工具调用
        llm_service = LLMService()
        llm = llm_service.get_llm("openai")
        
        # 先初始化工作流
        workflow = ImageGenerationWorkflow()
        
        # 创建工具实例并注入工作流
        generate_tool = GenerateImageTool()
        generate_tool.workflow = workflow
        
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
            tools=[generate_tool]
        )
        
        # 保存工作流引用（供其他方法使用）
        object.__setattr__(self, '_workflow', workflow)
    
    @property
    def workflow(self):
        """获取工作流实例"""
        return self._workflow
    
    def batch_generate(
        self,
        prompts: List[str],
        reference_image: Optional[str] = None,
        platform: str = "temu",
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
                # 直接调用工作流，避免通过工具层的JSON序列化/反序列化开销
                platform_normalized = platform.lower() if platform else "default"
                result = self._workflow.run(
                    prompt=prompt,
                    reference_image=reference_image,
                    mode=kwargs.get('generation_mode', 'text2img'),
                    platform=platform_normalized,
                    quality_threshold=kwargs.get('quality_threshold') or settings.QUALITY_THRESHOLD,
                    max_retries=kwargs.get('max_retries') or settings.MAX_IMAGE_GENERATION_RETRIES,
                    negative_prompt=kwargs.get('negative_prompt', '')
                )
                
                # 构造与工具返回一致的结构
                output = {
                    "success": result.get("success", False),
                    "images": result.get("generated_images", []),
                    "selected_image": result.get("selected_image"),
                    "quality_scores": result.get("quality_scores", []),
                    "iteration_count": result.get("iteration_count", 0),
                    "platform": platform_normalized,
                    "metadata": result.get("metadata", {})
                }
                
                if not result.get("success"):
                    output["error_message"] = result.get("error_message", "生成失败")
                    
                results.append(output)
            except Exception as e:
                results.append({
                    "success": False,
                    "error_message": str(e),
                    "index": i,
                    "platform": platform
                })
        
        return json.dumps(results, ensure_ascii=False, indent=2)
