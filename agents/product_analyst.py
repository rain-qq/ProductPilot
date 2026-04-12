"""
产品分析师Agent - 分析参考产品的视觉特征
"""
from crewai import Agent
from langchain.tools import tool
from typing import Dict, Any
import json

from config.settings import settings
from services.image_service import ImageService
from services.llm_service import LLMService


class ProductAnalystAgent(Agent):
    """电商产品分析师Agent"""

    def __init__(self):
        # 使用LLMService获取OpenAI LLM用于文本分析任务
        llm_service = LLMService()
        llm = llm_service.get_llm("openai")

        super().__init__(
            role='电商产品分析师',
            goal='分析参考产品的视觉特征和卖点，提取可复用的设计元素',
            backstory='''你是一位资深电商产品分析师，拥有10年电商视觉营销经验。

你的专长包括：
1. 深度分析产品图片的构图、配色方案、光影效果
2. 识别产品的核心卖点和目标用户群体
3. 提取成功的视觉营销模式和设计语言
4. 提供可操作的设计优化建议

你擅长从商业角度解读产品视觉呈现，帮助生成高转化率的电商图片。''',
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=[self._create_analyze_tool()]
        )

    def _create_analyze_tool(self):
        """创建CrewAI兼容的工具"""
        @tool("analyze_reference_image")
        def analyze_reference_image(image_url: str) -> str:
            """分析参考图片并返回结构化分析结果
            
            Args:
                image_url: 参考图片URL
                
            Returns:
                JSON格式的分析报告
            """
            try:
                image_service = ImageService()
                
                # 提取图片技术特征
                features = image_service.extract_features(image_url)
                
                # 使用LLM进行语义分析
                analysis_prompt = f"""
作为电商产品分析专家，请分析这张产品图片：

技术特征：
- 尺寸: {features.get('width')}x{features.get('height')}
- 主色调: {features.get('dominant_colors', [])}
- 构图类型: {features.get('composition_type', 'unknown')}
- 背景类型: {features.get('background_type', 'unknown')}

请从以下维度进行专业分析，并以JSON格式返回：

{{
  "color_scheme": ["主色1", "辅色1", "辅色2"],
  "composition_type": "构图类型描述",
  "lighting_style": "光影风格描述",
  "background_type": "背景类型描述",
  "viewing_angle": "拍摄角度",
  "style_tags": ["风格标签1", "风格标签2"],
  "marketing_points": ["卖点1", "卖点2"],
  "target_audience": "目标人群",
  "design_strengths": ["设计优点1", "设计优点2"],
  "improvement_suggestions": ["改进建议"]
}}

要求：
1. color_scheme: 列出2-4个主要颜色
2. style_tags: 3-5个风格标签（如：简约、科技感、奢华等）
3. marketing_points: 2-4个核心营销卖点
4. 用中文回答
"""
                
                # 调用LLM分析
                response = self.llm.invoke(analysis_prompt)
                
                # 尝试解析JSON
                try:
                    analysis_result = json.loads(response.content)
                except:
                    # 如果解析失败，构造基本结构
                    analysis_result = {
                        "color_scheme": features.get("dominant_colors", []),
                        "composition_type": features.get("composition_type", ""),
                        "lighting_style": "专业摄影光效",
                        "background_type": features.get("background_type", ""),
                        "viewing_angle": "正面视角",
                        "style_tags": ["电商", "专业"],
                        "marketing_points": [],
                        "target_audience": "大众消费者",
                        "design_strengths": [],
                        "improvement_suggestions": []
                    }
                
                return json.dumps(analysis_result, ensure_ascii=False, indent=2)
                
            except Exception as e:
                error_msg = f"分析失败: {str(e)}"
                return json.dumps({"error": error_msg}, ensure_ascii=False)
        
        return analyze_reference_image