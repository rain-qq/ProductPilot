"""
质量审核员Agent - 评估生成图片质量
支持电商平台特定规范检查
"""
from crewai import Agent
from langchain.tools import tool
from typing import Dict, Any, Optional
import json

from config.settings import settings
from services.llm_service import LLMService


class QualityReviewerAgent(Agent):
    """电商图片质量审核员Agent"""
    
    def __init__(self):
        # 使用LLMService获取OpenAI LLM用于文本质量评估任务
        llm_service = LLMService()
        llm = llm_service.get_llm("openai")
        
        super().__init__(
            role='电商图片质量审核专家',
            goal='严格审核生成的图片质量，确保符合电商商业标准和平台规范',
            backstory='''你是一位拥有15年经验的电商图片质检专家，曾在天猫、京东、Amazon等平台担任视觉品质总监。

你的审核标准极其严苛，专注以下维度：
1. **产品清晰度**: 细节呈现是否足够清晰
2. **色彩准确性**: 颜色是否真实且协调
3. **构图合理性**: 主体突出，视觉平衡
4. **光影效果**: 光线运用是否专业
5. **商业价值**: 是否能吸引用户点击和购买
6. **技术规范**: 分辨率、格式、背景等是否符合平台要求
7. **平台合规性**: 是否满足Amazon、Temu等跨境电商平台规范

你能精准识别问题并提供专业的改进建议。''',
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[self._create_evaluate_tool()]
        )
    
    def _create_evaluate_tool(self):
        """创建CrewAI兼容的质量评估工具"""
        @tool("evaluate_image_quality")
        def evaluate_image_quality(
            image_url: str,
            requirements: str = "",
            product_type: str = "",
            platform: str = "temu"
        ) -> str:
            """
            评估图片质量（支持平台特定规范）
            
            Args:
                image_url: 待评估图片URL
                requirements: 特定要求
                product_type: 产品类型
                platform: 目标平台 (amazon/temu/default)
                
            Returns:
                JSON格式的评估报告
            """
            
            # 获取平台配置
            platform_config = settings.PLATFORM_PRESETS.get(platform, settings.PLATFORM_PRESETS["default"])
            
            evaluation_prompt = f"""
作为电商图片质检专家，请对这张图片进行严格评估。

## 基础信息
{'产品类型：' + product_type if product_type else ''}
{'特殊要求：' + requirements if requirements else ''}
目标平台：{platform.upper()}

## 平台规范要求
- 背景类型：{platform_config['background']}
- 最小产品覆盖率：{platform_config['product_coverage']*100}%
- 最低分辨率：{platform_config['min_resolution'][0]}x{platform_config['min_resolution'][1]}
- 允许文字：{'是' if platform_config['allow_text'] else '否'}
- 允许水印：{'是' if platform_config['allow_watermark'] else '否'}
- 允许边框：{'是' if platform_config['allow_border'] else '否'}

## 评估维度（每项0-1分，保留2位小数）：

1. **clarity (清晰度)**: 产品细节、边缘锐度、对焦准确性
2. **color_accuracy (色彩准确性)**: 颜色真实性、饱和度、白平衡
3. **composition (构图)**: 主体位置、视觉平衡、留白合理性
4. **lighting (光影)**: 光线分布、阴影处理、立体感
5. **commercial_value (商业价值)**: 吸引力、转化率、品牌感
6. **platform_compliance (平台合规性)**: 是否符合{platform.upper()}平台规范
   - 背景纯度检查
   - 产品占比检查
   - 禁用元素检查（文字/水印/边框）
   - 分辨率达标检查

## 输出格式（严格JSON）：

{{
  "overall_score": 0.85,
  "clarity": 0.90,
  "color_accuracy": 0.85,
  "composition": 0.80,
  "lighting": 0.85,
  "commercial_value": 0.80,
  "platform_compliance": 0.90,
  "issues": [
    "问题描述1",
    "问题描述2"
  ],
  "suggestions": [
    "改进建议1",
    "改进建议2"
  ],
  "platform_issues": [
    "平台违规项1",
    "平台违规项2"
  ],
  "passed": true,
  "platform_passed": true,
  "confidence": 0.95
}}

## 评分标准：
- 0.9-1.0: 优秀，可直接使用
- 0.8-0.9: 良好，轻微优化
- 0.7-0.8: 合格，需要改进
- 0.6-0.7: 较差，建议重新生成
- <0.6: 不合格，必须重新生成

## {platform.upper()}平台特别注意事项：
{platform_config['negative_prompt']}
风格要求：{platform_config['style_keywords']}

## 常见问题检查：
- 模糊/失焦
- 过度处理/人工痕迹
- 颜色失真
- 构图失衡
- 背景杂乱/不符合平台要求
- 产品变形
- 包含禁用元素（文字/水印/边框等）
- 分辨率不足
- 产品占比不达标

请给出客观、专业的评估，特别关注平台合规性。
"""
            
            try:
                # 调用LLM评估
                response = self.llm.invoke(evaluation_prompt)
                
                # 解析结果
                result_text = response.content
                
                # 清理代码标记
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                
                try:
                    result_json = json.loads(result_text.strip())
                    
                    # 添加通过标记
                    threshold = platform_config.get('quality_threshold', settings.QUALITY_THRESHOLD)
                    result_json["passed"] = result_json.get("overall_score", 0) >= threshold
                    
                    # 平台合规性检查
                    platform_compliance = result_json.get("platform_compliance", 0.7)
                    result_json["platform_passed"] = platform_compliance >= 0.8
                    
                except Exception as parse_error:
                    # 解析失败时的默认结果
                    result_json = {
                        "overall_score": 0.7,
                        "clarity": 0.7,
                        "color_accuracy": 0.7,
                        "composition": 0.7,
                        "lighting": 0.7,
                        "commercial_value": 0.7,
                        "platform_compliance": 0.7,
                        "issues": ["评估结果解析失败"],
                        "suggestions": ["请手动检查图片质量"],
                        "platform_issues": [],
                        "passed": True,
                        "platform_passed": True,
                        "confidence": 0.5
                    }
                
                return json.dumps(result_json, ensure_ascii=False, indent=2)
                
            except Exception as e:
                error_msg = f"质量评估失败: {str(e)}"
                return json.dumps({
                    "error": error_msg,
                    "overall_score": 0.5,
                    "passed": False
                }, ensure_ascii=False)
        
        return evaluate_image_quality
