"""
数据模型定义
支持电商平台特定规范
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class GenerationMode(str, Enum):
    """生成模式"""
    TEXT2IMG = "text2img"
    IMG2IMG = "img2img"
    MIXED = "mixed"


class PlatformType(str, Enum):
    """目标平台类型"""
    AMAZON = "amazon"
    TEMU = "temu"
    DEFAULT = "default"


class ProductInfo(BaseModel):
    """产品信息"""
    name: str = Field(..., description="商品名称")
    description: str = Field(..., description="商品描述")
    category: Optional[str] = Field(None, description="商品类别")
    target_audience: Optional[str] = Field(None, description="目标人群")
    key_features: Optional[List[str]] = Field(default_factory=list, description="核心卖点")
    reference_image_url: Optional[str] = Field(None, description="参考图片URL")


class ImageGenerationRequest(BaseModel):
    """图片生成请求"""
    product_info: ProductInfo
    mode: GenerationMode = Field(GenerationMode.MIXED, description="生成模式")
    platform: PlatformType = Field(PlatformType.TEMU, description="目标平台 (amazon/temu/default)")
    num_images: int = Field(4, ge=1, le=10, description="生成图片数量")
    quality_threshold: float = Field(0.8, ge=0.0, le=1.0, description="质量阈值")
    max_retries: int = Field(3, ge=1, le=5, description="最大重试次数")
    
    # 高级选项
    negative_prompt: Optional[str] = Field(None, description="负向提示词")
    style_preference: Optional[str] = Field(None, description="风格偏好")
    custom_settings: Optional[Dict[str, Any]] = Field(None, description="自定义设置")


class AnalysisResult(BaseModel):
    """产品分析结果"""
    color_scheme: List[str] = Field(default_factory=list, description="配色方案")
    composition_type: str = Field("", description="构图类型")
    lighting_style: str = Field("", description="光影风格")
    background_type: str = Field("", description="背景类型")
    viewing_angle: str = Field("", description="拍摄角度")
    style_tags: List[str] = Field(default_factory=list, description="风格标签")
    marketing_points: List[str] = Field(default_factory=list, description="营销要点")


class PromptResult(BaseModel):
    """提示词优化结果"""
    positive_prompt: str = Field(..., description="正向提示词")
    negative_prompt: str = Field(..., description="负向提示词")
    suggested_settings: Dict[str, Any] = Field(default_factory=dict, description="建议参数")
    platform: Optional[str] = Field(None, description="目标平台")
    platform_compliance_notes: Optional[str] = Field(None, description="平台合规性说明")


class QualityEvaluation(BaseModel):
    """质量评估结果"""
    overall_score: float = Field(0.0, ge=0.0, le=1.0, description="总体评分")
    clarity: float = Field(0.0, ge=0.0, le=1.0, description="清晰度")
    color_accuracy: float = Field(0.0, ge=0.0, le=1.0, description="色彩准确性")
    composition: float = Field(0.0, ge=0.0, le=1.0, description="构图")
    lighting: float = Field(0.0, ge=0.0, le=1.0, description="光影")
    commercial_value: float = Field(0.0, ge=0.0, le=1.0, description="商业价值")
    platform_compliance: float = Field(0.0, ge=0.0, le=1.0, description="平台合规性")
    issues: List[str] = Field(default_factory=list, description="问题列表")
    suggestions: List[str] = Field(default_factory=list, description="改进建议")
    platform_issues: List[str] = Field(default_factory=list, description="平台违规项")
    passed: bool = Field(True, description="是否通过质检")
    platform_passed: bool = Field(True, description="是否通过平台合规检查")


class GeneratedImage(BaseModel):
    """生成的图片"""
    url: str = Field(..., description="图片URL")
    thumbnail_url: Optional[str] = Field(None, description="缩略图URL")
    width: int = Field(..., description="宽度")
    height: int = Field(..., description="高度")
    format: str = Field("png", description="格式")
    size_bytes: Optional[int] = Field(None, description="文件大小")


class ImageGenerationResult(BaseModel):
    """图片生成结果"""
    success: bool = Field(..., description="是否成功")
    images: List[GeneratedImage] = Field(default_factory=list, description="生成的图片列表")
    selected_image: Optional[GeneratedImage] = Field(None, description="选中的最佳图片")
    quality_scores: List[float] = Field(default_factory=list, description="质量评分列表")
    iteration_count: int = Field(0, description="迭代次数")
    platform: Optional[str] = Field(None, description="目标平台")
    analysis_result: Optional[AnalysisResult] = Field(None, description="产品分析结果")
    prompt_result: Optional[PromptResult] = Field(None, description="提示词结果")
    quality_evaluations: List[QualityEvaluation] = Field(default_factory=list, description="质量评估详情")
    error_message: Optional[str] = Field(None, description="错误信息")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskInfo(BaseModel):
    """任务信息"""
    task_id: str = Field(..., description="任务ID")
    status: TaskStatus = Field(TaskStatus.PENDING, description="任务状态")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="进度百分比")
    current_step: Optional[str] = Field(None, description="当前步骤")
    result: Optional[ImageGenerationResult] = Field(None, description="生成结果")
    error_message: Optional[str] = Field(None, description="错误信息")
    created_at: Optional[str] = Field(None, description="创建时间")
    updated_at: Optional[str] = Field(None, description="更新时间")
