"""
质量审核员Agent - 评估生成图片质量
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import json

from config.settings import settings


class QualityReviewerAgent(Agent):
    """电商图片质量审核员Agent"""
    
    def __init__(self):
        super().__init__(
            role='电商图片质量审核专家',
            goal='严格审核生成的图片质量，确保符合电商商业标准',
            backstory='''你是一位拥有15年经验的电商图片质检专家，曾在天猫、京东等平台担任视觉品质总监。

你的审核标准极其严苛，专注以下维度：
1. **产品清晰度**: 细节呈现是否足够清晰
2. **色彩准确性**: 颜色是否真实且协调
3. **构图合理性**: 主体突出，视觉平衡
4. **光影效果**: 光线运用是否专业
5. **商业价值**: 是否能吸引用户点击和购买
6. **技术规范**: 分辨率、格式等是否符合要求

你能精准识别问题并提供专业的改进建议。''',
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(
                model="gpt-4-vision-preview",
                temperature=0.3,
                openai_api_key=settings.OPENAI_API_KEY
            ),
            tools=[self.evaluate_image_quality]
        )
    
    def evaluate_image_quality(
        self,
        image_url: str,
        requirements: str = "",
        product_type: str = ""
    ) -> str:
        """
        评估图片质量
        
        Args:
            image_url: 待评估图片URL
            requirements: 特定要求
            product_type: 产品类型
            
        Returns:
            JSON格式的评估报告
        """
        
        evaluation_prompt = f"""
作为电商图片质检专家，请对这张图片进行严格评估。

{'产品类型：' + product_type if product_type else ''}
{'特殊要求：' + requirements if requirements else ''}

## 评估维度（每项0-1分，保留2位小数）：

1. **clarity (清晰度)**: 产品细节、边缘锐度、对焦准确性
2. **color_accuracy (色彩准确性)**: 颜色真实性、饱和度、白平衡
3. **composition (构图)**: 主体位置、视觉平衡、留白合理性
4. **lighting (光影)**: 光线分布、阴影处理、立体感
5. **commercial_value (商业价值)**: 吸引力、转化率、品牌感

## 输出格式（严格JSON）：

{{
  "overall_score": 0.85,
  "clarity": 0.90,
  "color_accuracy": 0.85,
  "composition": 0.80,
  "lighting": 0.85,
  "commercial_value": 0.80,
  "issues": [
    "问题描述1",
    "问题描述2"
  ],
  "suggestions": [
    "改进建议1",
    "改进建议2"
  ],
  "passed": true,
  "confidence": 0.95
}}

## 评分标准：
- 0.9-1.0: 优秀，可直接使用
- 0.8-0.9: 良好，轻微优化
- 0.7-0.8: 合格，需要改进
- 0.6-0.7: 较差，建议重新生成
- <0.6: 不合格，必须重新生成

## 常见问题检查：
- 模糊/失焦
- 过度处理/人工痕迹
- 颜色失真
- 构图失衡
- 背景杂乱
- 产品变形
- 文字错误（如有）

请给出客观、专业的评估。
"""
        
        try:
            # 调用LLM评估
            response = self.llm.invoke(evaluation_prompt)
            
            # 解析结果
            result_text = response.content
            
            # 清理markdown标记
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            try:
                result_json = json.loads(result_text.strip())
                
                # 添加通过标记
                threshold = settings.QUALITY_THRESHOLD
                result_json["passed"] = result_json.get("overall_score", 0) >= threshold
                
            except Exception as parse_error:
                # 解析失败时的默认结果
                result_json = {
                    "overall_score": 0.7,
                    "clarity": 0.7,
                    "color_accuracy": 0.7,
                    "composition": 0.7,
                    "lighting": 0.7,
                    "commercial_value": 0.7,
                    "issues": ["评估结果解析失败"],
                    "suggestions": ["请手动检查图片质量"],
                    "passed": True,
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
