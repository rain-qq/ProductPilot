"""
FastAPI路由定义
支持电商平台特定规范
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
import uuid
import time
from datetime import datetime
from loguru import logger

from models.schemas import (
    ImageGenerationRequest,
    ImageGenerationResult,
    GeneratedImage,
    TaskInfo,
    TaskStatus,
    ProductInfo,
    GenerationMode,
    PlatformType
)
from agents.product_analyst import ProductAnalystAgent
from agents.prompt_engineer import PromptEngineerAgent
from agents.image_creator import ImageCreatorAgent
from agents.quality_reviewer import QualityReviewerAgent
from crewai import Crew, Process, Task
from config.settings import settings

router = APIRouter()

# 简单的任务存储 (生产环境应该用数据库)
task_store = {}


@router.post("/generate", response_model=ImageGenerationResult)
async def generate_image(request: ImageGenerationRequest):
    """
    生成电商图片（支持多平台规范）

    Args:
        request: 图片生成请求

    Returns:
        生成结果
    """
    try:
        platform = request.platform.value

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

        # 任务2: 优化提示词（传入平台参数）
        prompt_context = f"""
产品信息:
- 名称: {request.product_info.name}
- 描述: {request.product_info.description}
- 类别: {request.product_info.category or '未指定'}
- 目标人群: {request.product_info.target_audience or '未指定'}
- 卖点: {', '.join(request.product_info.key_features) if request.product_info.key_features else '未指定'}

生成模式: {request.mode.value}
目标平台: {platform.upper()}
{f'风格偏好: {request.style_preference}' if request.style_preference else ''}
"""

        if request.product_info.reference_image_url:
            prompt_context += f"\n参考分析: {{analysis_task.output}}"

        prompt_task = Task(
            description=f"为{platform.upper()}平台生成优化的AI绘画提示词:\n{prompt_context}",
            agent=engineer,
            context=tasks if tasks else [],
            expected_output="包含positive和negative prompt的结构化JSON，符合平台规范"
        )
        tasks.append(prompt_task)

        # 任务3: 生成图片 (调用LangGraph工作流，传入平台参数)
        logger.info(f"📋 [CrewAI] 准备创建 generation_task")
        logger.info(f"   - agent: {creator.role}")
        logger.info(f"   - platform: {platform}")
        logger.info(f"   - mode: {request.mode.value}")

        generation_task = Task(
            description=f"""
你现在的任务是生成电商图片。请直接使用你手中的 `generate_with_workflow` 工具。

你需要从上下文中获取以下信息作为工具参数：
1. **positive_prompt**: 查看上一个任务（Prompt Engineer）的输出，找到其中的 positive_prompt 字段。
2. **negative_prompt**: 查看上一个任务的输出，找到 negative_prompt 字段。
3. **platform**: 目标平台是 "{platform}"。

其他固定参数：
- reference_image: {request.product_info.reference_image_url or 'null'}
- generation_mode: "{request.mode.value}"
- quality_threshold: {request.quality_threshold}
- max_retries: {request.max_retries}

请立即调用工具开始生成，不要输出多余的分析过程。
""",
            agent=creator,
            context=[prompt_task],
            expected_output="生成的图片URL和质量评分JSON"
        )
        logger.info(f"✅ [CrewAI] generation_task 创建成功")
        tasks.append(generation_task)


        # 任务4: 质量审核（传入平台参数）
        review_task = Task(
            description=f"审核生成的图片质量，确保符合{platform.upper()}平台规范并给出评估报告",
            agent=reviewer,
            context=[generation_task],
            expected_output="质量评估报告JSON，包含平台合规性检查"
        )
        tasks.append(review_task)

        # 组建团队并执行
        logger.info(f"👥 [CrewAI] 正在创建 Crew 团队")
        logger.info(f"   - agents: {[a.role for a in ([analyst, engineer, creator, reviewer] if request.product_info.reference_image_url else [engineer, creator, reviewer])]}")
        logger.info(f"   - tasks count: {len(tasks)}")

        crew = Crew(
            agents=[analyst, engineer, creator, reviewer] if request.product_info.reference_image_url
                   else [engineer, creator, reviewer],
            tasks=tasks,
            process=Process.sequential,
            verbose=2
        )

        logger.info(f"🚀 [CrewAI] 开始执行 Crew.kickoff()...")
        result = crew.kickoff()
        logger.info(f"✅ [CrewAI] Crew.kickoff() 执行完成")
        logger.info(f"   - result type: {type(result)}")
        logger.info(f"   - result length: {len(str(result)) if result else 0}")

        # TODO: 更完善的结果解析
        return ImageGenerationResult(
            success=True,
            images=[],  # 需要从result中提取
            selected_image=None,
            quality_scores=[],
            iteration_count=0,
            platform=platform,
            metadata={"raw_result": str(result)}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/async", response_model=TaskInfo)
async def generate_image_async(request: ImageGenerationRequest, background_tasks: BackgroundTasks):
    """
    异步生成电商图片（支持多平台规范）

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


@router.get("/platforms")
async def get_platform_presets():
    """
    获取所有支持的平台预设配置

    Returns:
        平台配置字典
    """
    return {
        "platforms": settings.PLATFORM_PRESETS,
        "supported_platforms": list(settings.PLATFORM_PRESETS.keys())
    }


async def process_generation_task(task_id: str, request: ImageGenerationRequest):
    """
    后台处理生成任务（支持多平台规范）

    Args:
        task_id: 任务ID
        request: 生成请求
    """
    import time
    start_time = time.time()
    platform = request.platform.value

    try:
        # 更新状态为处理中
        task_store[task_id].status = TaskStatus.PROCESSING
        task_store[task_id].progress = 10.0
        task_store[task_id].current_step = "初始化Agent"
        task_store[task_id].updated_at = datetime.now().isoformat()

        # 创建团队
        analyst = ProductAnalystAgent()
        engineer = PromptEngineerAgent()
        creator = ImageCreatorAgent()
        reviewer = QualityReviewerAgent()

        tasks = []

        # 任务1: 分析参考产品 (如果有)
        if request.product_info.reference_image_url:
            task_store[task_id].current_step = "分析参考图片"
            task_store[task_id].progress = 20.0
            task_store[task_id].updated_at = datetime.now().isoformat()

            analysis_task = Task(
                description=f"""分析参考图片的视觉特征: {request.product_info.reference_image_url}

请提取配色方案、构图风格、光影效果等关键设计元素。""",
                agent=analyst,
                expected_output="结构化的产品视觉分析报告"
            )
            tasks.append(analysis_task)

        # 任务2: 优化提示词
        task_store[task_id].current_step = "优化提示词"
        task_store[task_id].progress = 35.0
        task_store[task_id].updated_at = datetime.now().isoformat()

        prompt_context = f"""
产品信息:
- 名称: {request.product_info.name}
- 描述: {request.product_info.description}
- 类别: {request.product_info.category or '未指定'}
- 目标人群: {request.product_info.target_audience or '未指定'}
- 卖点: {', '.join(request.product_info.key_features) if request.product_info.key_features else '未指定'}

生成模式: {request.mode.value}
目标平台: {platform.upper()}
{f'风格偏好: {request.style_preference}' if request.style_preference else ''}
"""

        if request.product_info.reference_image_url:
            prompt_context += f"\n参考分析: {{analysis_task.output}}"

        prompt_task = Task(
            description=f"为{platform.upper()}平台生成优化的AI绘画提示词:\n{prompt_context}",
            agent=engineer,
            context=tasks if tasks else [],
            expected_output="包含positive和negative prompt的结构化JSON，符合平台规范"
        )
        tasks.append(prompt_task)

        # 任务3: 生成图片 (调用LangGraph工作流)
        task_store[task_id].current_step = "生成图片"
        task_store[task_id].progress = 50.0
        task_store[task_id].updated_at = datetime.now().isoformat()

        generation_task = Task(
            description=f"""
你现在的任务是生成电商图片。请直接使用你手中的 `generate_with_workflow` 工具。

你需要从上下文中获取以下信息作为工具参数：
1. **positive_prompt**: 查看上一个任务（Prompt Engineer）的输出，找到其中的 positive_prompt 字段。
2. **negative_prompt**: 查看上一个任务的输出，找到 negative_prompt 字段。
3. **platform**: 目标平台是 "{platform}"。

其他固定参数：
- reference_image: {request.product_info.reference_image_url or 'null'}
- generation_mode: "{request.mode.value}"
- quality_threshold: {request.quality_threshold}
- max_retries: {request.max_retries}

请立即调用工具开始生成，不要输出多余的分析过程。
""",
            agent=creator,
            context=[prompt_task],
            expected_output="生成的图片URL和质量评分JSON"
        )
        tasks.append(generation_task)

        # 任务4: 质量审核
        task_store[task_id].current_step = "质量审核"
        task_store[task_id].progress = 80.0
        task_store[task_id].updated_at = datetime.now().isoformat()

        review_task = Task(
            description=f"审核生成的图片质量，确保符合{platform.upper()}平台规范并给出评估报告",
            agent=reviewer,
            context=[generation_task],
            expected_output="质量评估报告JSON，包含平台合规性检查"
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

        # 计算耗时
        generation_time = time.time() - start_time

        # TODO: 更完善的结果解析 - 从CrewAI结果中提取实际数据
        # 目前先返回基础结构
        task_store[task_id].status = TaskStatus.COMPLETED
        task_store[task_id].progress = 100.0
        task_store[task_id].current_step = "完成"
        task_store[task_id].result = ImageGenerationResult(
            success=True,
            images=[],  # 需要从result.raw输出中解析
            selected_image=None,
            quality_scores=[],
            iteration_count=0,
            platform=platform,
            metadata={
                "generation_time": generation_time,
                "model_version": settings.IMAGE_GENERATION_MODEL or "unknown",
                "platform": platform,
                "raw_result": str(result)[:500]  # 截取前500字符避免过长
            }
        )
        task_store[task_id].updated_at = datetime.now().isoformat()

    except Exception as e:
        logger.error(f"Task {task_id} failed for {platform}: {str(e)}")
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
        iteration_count=1,
        platform="temu",
        metadata={
            "generation_time": 12.5,
            "model_version": "sd-webui-v1.0"
        }
    )
    task_store[task_id].updated_at = datetime.now().isoformat()
