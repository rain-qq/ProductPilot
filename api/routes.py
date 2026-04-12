"""
FastAPI路由定义
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
import uuid
import time
from datetime import datetime

from models.schemas import (
    ImageGenerationRequest,
    ImageGenerationResult,
    GeneratedImage,
    TaskInfo,
    TaskStatus,
    ProductInfo,
    GenerationMode
)
from agents.product_analyst import ProductAnalystAgent
from agents.prompt_engineer import PromptEngineerAgent
from agents.image_creator import ImageCreatorAgent
from agents.quality_reviewer import QualityReviewerAgent
from crewai import Crew, Process, Task

router = APIRouter()

# 简单的任务存储 (生产环境应该用数据库)
task_store = {}


@router.post("/generate", response_model=ImageGenerationResult)
async def generate_image(request: ImageGenerationRequest):
    """
    生成电商图片
    
    Args:
        request: 图片生成请求
        
    Returns:
        生成结果
    """
    try:
        # 创建团队
        analyst = ProductAnalystAgent()
        engineer = PromptEngineerAgent()
        creator = ImageCreatorAgent()
        reviewer = QualityReviewerAgent()
        
        tasks = []
        
        # 任务1: 分析参考产品 (如果有)
        if request.product_info.reference_image_url:
            analysis_task = Task(
                description=f"""分析参考图片的视觉特征: {request.product_info.reference_image_url}
                
请提取配色方案、构图风格、光影效果等关键设计元素。""",
                agent=analyst,
                expected_output="结构化的产品视觉分析报告"
            )
            tasks.append(analysis_task)
        
        # 任务2: 优化提示词
        prompt_context = f"""
产品信息:
- 名称: {request.product_info.name}
- 描述: {request.product_info.description}
- 类别: {request.product_info.category or '未指定'}
- 目标人群: {request.product_info.target_audience or '未指定'}
- 卖点: {', '.join(request.product_info.key_features) if request.product_info.key_features else '未指定'}

生成模式: {request.mode.value}
{f'风格偏好: {request.style_preference}' if request.style_preference else ''}
"""
        
        if request.product_info.reference_image_url:
            prompt_context += f"\n参考分析: {{analysis_task.output}}"
        
        prompt_task = Task(
            description=f"为产品生成优化的AI绘画提示词:\n{prompt_context}",
            agent=engineer,
            context=tasks if tasks else [],
            expected_output="包含positive和negative prompt的结构化JSON"
        )
        tasks.append(prompt_task)
        
        # 任务3: 生成图片 (调用LangGraph工作流)
        generation_task = Task(
            description=f"""
使用工作流生成电商图片:
- 提示词: {{prompt_task.output}}
- 参考图片: {request.product_info.reference_image_url or '无'}
- 生成模式: {request.mode.value}
- 质量阈值: {request.quality_threshold}
- 最大重试: {request.max_retries}
""",
            agent=creator,
            context=[prompt_task],
            expected_output="生成的图片URL和质量评分JSON"
        )
        tasks.append(generation_task)
        
        # 任务4: 质量审核
        review_task = Task(
            description="审核生成的图片质量并给出评估报告",
            agent=reviewer,
            context=[generation_task],
            expected_output="质量评估报告JSON"
        )
        tasks.append(review_task)
        
        # 组建团队并执行
        crew = Crew(
            agents=[analyst, engineer, creator, reviewer] if request.product_info.reference_image_url 
                   else [engineer, creator, reviewer],
            tasks=tasks,
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff()
        
        # 解析结果
        # TODO: 更完善的结果解析
        return ImageGenerationResult(
            success=True,
            images=[],  # 需要从result中提取
            selected_image=None,
            quality_scores=[],
            iteration_count=0,
            metadata={"raw_result": str(result)}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/async", response_model=TaskInfo)
async def generate_image_async(request: ImageGenerationRequest, background_tasks: BackgroundTasks):
    """
    异步生成电商图片
    
    Args:
        request: 图片生成请求
        background_tasks: 后台任务
        
    Returns:
        任务信息
    """
    task_id = str(uuid.uuid4())
    
    # 保存任务状态
    task_info = TaskInfo(
        task_id=task_id,
        status=TaskStatus.PENDING,
        progress=0.0,
        current_step="等待处理",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    task_store[task_id] = task_info
    
    # 添加后台任务
    background_tasks.add_task(process_generation_task, task_id, request)
    
    return task_info


@router.get("/task/{task_id}", response_model=TaskInfo)
async def get_task_status(task_id: str):
    """
    查询任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        任务信息
    """
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return task_store[task_id]


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


async def process_generation_task(task_id: str, request: ImageGenerationRequest):
    """
    后台处理生成任务
    
    Args:
        task_id: 任务ID
        request: 生成请求
    """
    try:
        # 更新状态为处理中
        task_store[task_id].status = TaskStatus.PROCESSING
        task_store[task_id].progress = 10.0
        task_store[task_id].current_step = "初始化Agent"
        task_store[task_id].updated_at = datetime.now().isoformat()
        
        # TODO: 实现实际的生成逻辑
        # 这里简化处理，实际应该调用CrewAI + LangGraph
        
        await simulate_generation(task_id)
        
    except Exception as e:
        task_store[task_id].status = TaskStatus.FAILED
        task_store[task_id].error_message = str(e)
        task_store[task_id].updated_at = datetime.now().isoformat()


async def simulate_generation(task_id: str):
    """
    模拟生成过程 (用于测试)
    
    Args:
        task_id: 任务ID
    """
    steps = [
        ("分析产品需求", 20.0),
        ("优化提示词", 35.0),
        ("生成图片", 60.0),
        ("质量检查", 80.0),
        ("后处理", 95.0),
        ("完成", 100.0)
    ]
    
    for step_name, progress in steps:
        task_store[task_id].current_step = step_name
        task_store[task_id].progress = progress
        task_store[task_id].updated_at = datetime.now().isoformat()
        
        # 模拟处理时间
        await __import__("asyncio").sleep(2)
    
    # 标记为完成
    task_store[task_id].status = TaskStatus.COMPLETED
    task_store[task_id].result = ImageGenerationResult(
        success=True,
        images=[
            GeneratedImage(
                url="https://example.com/image1.png",
                width=1024,
                height=1024,
                format="png"
            )
        ],
        selected_image=GeneratedImage(
            url="https://example.com/best.png",
            width=1024,
            height=1024,
            format="png"
        ),
        quality_scores=[0.85],
        iteration_count=1
    )
    task_store[task_id].updated_at = datetime.now().isoformat()
