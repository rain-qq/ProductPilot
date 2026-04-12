"""
图片生成工作流 - LangGraph实现
支持 text2img, img2img, mixed 三种模式，包含质量检查和自动重试
"""
from typing import TypedDict, List, Optional, Dict, Any
from langgraph.graph import StateGraph, END
import json

from config.settings import settings
from services.image_service import ImageService
from agents.quality_reviewer import QualityReviewerAgent
from loguru import logger


# 定义工作流状态
class ImageGenerationState(TypedDict):
    # 输入参数
    prompt: str
    negative_prompt: str
    reference_image: Optional[str]
    mode: str  # text2img / img2img / mixed
    
    # 控制参数
    quality_threshold: float
    max_retries: int
    
    # 中间结果
    optimized_prompt: Dict[str, Any]
    preprocessed_image: Optional[str]
    
    # 输出结果
    generated_images: List[str]
    quality_scores: List[float]
    selected_image: Optional[str]
    
    # 流程控制
    iteration_count: int
    needs_regeneration: bool
    success: bool
    error_message: Optional[str]
    
    # 元数据
    metadata: Dict[str, Any]


class ImageGenerationWorkflow:
    """电商图片生成工作流"""
    
    def __init__(self):
        self.app = self._build_workflow()
        self.image_service = ImageService()
    
    def _build_workflow(self):
        """构建工作流图"""
        
        workflow = StateGraph(ImageGenerationState)
        
        # 添加节点
        workflow.add_node("preprocess", self.preprocess_node)
        workflow.add_node("generate", self.generate_node)
        workflow.add_node("quality_check", self.quality_check_node)
        workflow.add_node("regenerate", self.regenerate_node)
        workflow.add_node("post_process", self.post_process_node)
        workflow.add_node("handle_error", self.error_handler_node)
        
        # 设置入口点
        workflow.set_entry_point("preprocess")
        
        # 定义流程
        workflow.add_edge("preprocess", "generate")
        workflow.add_edge("generate", "quality_check")
        
        # 条件分支：质量检查决策
        workflow.add_conditional_edges(
            "quality_check",
            self.decide_next_step,
            {
                "accept": "post_process",
                "regenerate": "regenerate",
                "error": "handle_error"
            }
        )
        
        # 重新生成后回到生成节点
        workflow.add_edge("regenerate", "generate")
        
        # 后处理完成
        workflow.add_edge("post_process", END)
        
        # 错误处理
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    def preprocess_node(self, state: ImageGenerationState) -> Dict:
        """节点1: 预处理参考图片"""
        logger.info(f"Preprocessing image for mode: {state['mode']}")
        
        try:
            if state.get("reference_image") and state["mode"] in ["img2img", "mixed"]:
                # 预处理参考图片
                processed = self.image_service.preprocess(state["reference_image"])
                return {
                    "preprocessed_image": processed,
                    "metadata": {
                        **state.get("metadata", {}),
                        "preprocessing_status": "completed"
                    }
                }
            else:
                return {
                    "preprocessed_image": None,
                    "metadata": {
                        **state.get("metadata", {}),
                        "preprocessing_status": "skipped"
                    }
                }
        except Exception as e:
            logger.error(f"Preprocessing failed: {str(e)}")
            return {
                "preprocessed_image": None,
                "error_message": f"预处理失败: {str(e)}",
                "metadata": {
                    **state.get("metadata", {}),
                    "preprocessing_status": "failed"
                }
            }
    
    def generate_node(self, state: ImageGenerationState) -> Dict:
        """节点2: 生成图片"""
        logger.info(f"Generating images (iteration {state.get('iteration_count', 0) + 1})")
        
        try:
            mode = state["mode"]
            prompt = state["prompt"]
            negative_prompt = state.get("negative_prompt", "")
            
            # 根据模式选择生成方式
            if mode == "text2img":
                images = self.image_service.text_to_image(
                    prompt=prompt,
                    negative_prompt=negative_prompt
                )
            
            elif mode == "img2img":
                if not state.get("preprocessed_image"):
                    raise ValueError("缺少预处理图片")
                
                images = self.image_service.image_to_image(
                    reference_image=state["preprocessed_image"],
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    strength=0.75
                )
            
            elif mode == "mixed":
                # 使用ControlNet
                if not state.get("preprocessed_image"):
                    raise ValueError("缺少参考图片")
                
                images = self.image_service.controlnet_generate(
                    reference_image=state["preprocessed_image"],
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    control_type="canny"
                )
            
            else:
                raise ValueError(f"不支持的生成模式: {mode}")
            
            logger.info(f"Generated {len(images)} images")
            
            return {
                "generated_images": images,
                "iteration_count": state.get("iteration_count", 0) + 1,
                "metadata": {
                    **state.get("metadata", {}),
                    "generation_mode": mode,
                    "generation_status": "completed"
                }
            }
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            return {
                "generated_images": [],
                "error_message": f"生成失败: {str(e)}",
                "iteration_count": state.get("iteration_count", 0) + 1
            }
    
    def quality_check_node(self, state: ImageGenerationState) -> Dict:
        """节点3: 质量检查"""
        logger.info("Running quality check...")
        
        try:
            if not state.get("generated_images"):
                return {
                    "quality_scores": [],
                    "error_message": "没有可检查的图片"
                }
            
            reviewer = QualityReviewerAgent()
            scores = []
            evaluations = []
            
            # 对每张图片进行评分
            for i, image_url in enumerate(state["generated_images"]):
                eval_result = reviewer.evaluate_image_quality(
                    image_url=image_url,
                    product_type=""
                )
                
                try:
                    eval_data = json.loads(eval_result)
                    score = eval_data.get("overall_score", 0.5)
                    scores.append(score)
                    evaluations.append(eval_data)
                    
                    logger.info(f"Image {i+1} score: {score:.2f}")
                except:
                    scores.append(0.5)
                    evaluations.append({})
            
            best_score = max(scores) if scores else 0
            best_idx = scores.index(best_score)
            
            logger.info(f"Quality check completed. Best score: {best_score:.2f}")
            
            return {
                "quality_scores": scores,
                "metadata": {
                    **state.get("metadata", {}),
                    "evaluations": evaluations,
                    "best_score": best_score,
                    "best_index": best_idx
                }
            }
            
        except Exception as e:
            logger.error(f"Quality check failed: {str(e)}")
            return {
                "quality_scores": [],
                "error_message": f"质检失败: {str(e)}"
            }
    
    def decide_next_step(self, state: ImageGenerationState) -> str:
        """决策函数: 决定下一步操作"""
        
        # 检查是否有错误
        if state.get("error_message"):
            return "error"
        
        # 检查是否超过最大重试次数
        current_iteration = state.get("iteration_count", 0)
        max_retries = state.get("max_retries", settings.MAX_IMAGE_GENERATION_RETRIES)
        
        if current_iteration >= max_retries:
            logger.warning(f"Reached max retries ({max_retries}), accepting current result")
            return "accept"
        
        # 检查质量分数
        quality_scores = state.get("quality_scores", [])
        quality_threshold = state.get("quality_threshold", settings.QUALITY_THRESHOLD)
        
        if quality_scores:
            best_score = max(quality_scores)
            
            if best_score >= quality_threshold:
                logger.info(f"Best score {best_score:.2f} meets threshold {quality_threshold}")
                return "accept"
            else:
                logger.info(f"Best score {best_score:.2f} below threshold, regenerating...")
                return "regenerate"
        
        # 默认接受
        return "accept"
    
    def regenerate_node(self, state: ImageGenerationState) -> Dict:
        """节点4: 重新生成（调整参数）"""
        logger.info("Regenerating with adjusted parameters...")
        
        # 调整提示词以增强细节
        original_prompt = state["prompt"]
        enhanced_prompt = f"{original_prompt}, highly detailed, professional photography, 8k, sharp focus"
        
        return {
            "prompt": enhanced_prompt,
            "needs_regeneration": True,
            "metadata": {
                **state.get("metadata", {}),
                "regeneration_reason": "quality_below_threshold",
                "prompt_enhanced": True
            }
        }
    
    def post_process_node(self, state: ImageGenerationState) -> Dict:
        """节点5: 后处理"""
        logger.info("Post-processing images...")
        
        try:
            if not state.get("generated_images"):
                return {
                    "selected_image": None,
                    "success": False
                }
            
            # 选择最佳图片
            quality_scores = state.get("quality_scores", [])
            if quality_scores:
                best_idx = quality_scores.index(max(quality_scores))
                best_image = state["generated_images"][best_idx]
                
                # 应用增强
                enhanced_image = self.image_service.enhance(best_image)
                
                logger.info(f"Selected and enhanced best image (score: {max(quality_scores):.2f})")
                
                return {
                    "selected_image": enhanced_image,
                    "success": True,
                    "metadata": {
                        **state.get("metadata", {}),
                        "total_iterations": state["iteration_count"],
                        "best_quality_score": max(quality_scores),
                        "post_processing": "completed"
                    }
                }
            else:
                # 没有评分，返回第一张
                return {
                    "selected_image": state["generated_images"][0],
                    "success": True,
                    "quality_scores": [0.5],
                    "metadata": {
                        **state.get("metadata", {}),
                        "post_processing": "no_quality_data"
                    }
                }
        
        except Exception as e:
            logger.error(f"Post-processing failed: {str(e)}")
            return {
                "selected_image": None,
                "success": False,
                "error_message": f"后处理失败: {str(e)}"
            }
    
    def error_handler_node(self, state: ImageGenerationState) -> Dict:
        """节点6: 错误处理"""
        logger.error(f"Workflow error: {state.get('error_message')}")
        
        return {
            "success": False,
            "error_message": state.get("error_message", "未知错误"),
            "metadata": {
                **state.get("metadata", {}),
                "workflow_status": "failed"
            }
        }
    
    def run(
        self,
        prompt: str,
        negative_prompt: str = "",
        reference_image: Optional[str] = None,
        mode: str = "text2img",
        quality_threshold: float = None,
        max_retries: int = None
    ) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            prompt: 正向提示词
            negative_prompt: 负向提示词
            reference_image: 参考图片URL
            mode: 生成模式 (text2img/img2img/mixed)
            quality_threshold: 质量阈值
            max_retries: 最大重试次数
            
        Returns:
            工作流执行结果
        """
        
        initial_state = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "reference_image": reference_image,
            "mode": mode,
            "quality_threshold": quality_threshold or settings.QUALITY_THRESHOLD,
            "max_retries": max_retries or settings.MAX_IMAGE_GENERATION_RETRIES,
            "optimized_prompt": {},
            "preprocessed_image": None,
            "generated_images": [],
            "quality_scores": [],
            "selected_image": None,
            "iteration_count": 0,
            "needs_regeneration": False,
            "success": False,
            "error_message": None,
            "metadata": {}
        }
        
        try:
            logger.info(f"Starting workflow with mode={mode}")
            result = self.app.invoke(initial_state)
            
            logger.info(f"Workflow completed. Success: {result.get('success')}")
            return result
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return {
                "success": False,
                "error_message": f"工作流执行失败: {str(e)}",
                "generated_images": [],
                "quality_scores": [],
                "selected_image": None,
                "iteration_count": 0,
                "metadata": {}
            }
