"""
提示词工程师Agent - 优化生图提示词
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
import json

from config.settings import settings


class PromptEngineerAgent(Agent):
    """AI绘画提示词专家Agent"""
    
    def __init__(self):
        super().__init__(
            role='AI绘画提示词专家',
            goal='根据产品分析和用户需求，生成高质量的Stable Diffusion和DALL-E提示词',
            backstory='''你是一位世界级的AI绘画提示词工程师，专注于电商产品图生成。
            
你的核心能力：
1. 精通Stable Diffusion、DALL-E、Midjourney等主流AI绘画工具的prompt工程
2. 深谙电商摄影美学和产品呈现技巧
3. 擅长编写精准的negative prompt避免常见问题
4. 能够根据参考产品的分析结果优化提示词策略

你生成的提示词总能产生商业级高质量的产品图片。''',
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                openai_api_key=settings.OPENAI_API_KEY
            ),
            tools=[self.optimize_prompt]
        )
    
    def optimize_prompt(
        self,
        user_input: str,
        reference_analysis: Optional[str] = None,
        style_preference: Optional[str] = None
    ) -> str:
        """
        优化提示词
        
        Args:
            user_input: 用户原始输入/产品描述
            reference_analysis: 参考产品分析结果 (JSON字符串)
            style_preference: 风格偏好
            
        Returns:
            JSON格式的优化结果
        """
        
        system_instruction = """
你是一个专业的电商AI绘画提示词工程师。你的任务是根据产品信息生成高质量的提示词。

## 提示词编写原则：

### Positive Prompt应包含：
1. **主体描述**: 清晰描述产品本身
2. **材质质感**: 如"磨砂质感"、"金属光泽"、"透明玻璃"
3. **光影效果**: 如"柔和光线"、"专业摄影灯光"、"自然光"
4. **构图方式**: 如"居中构图"、"45度角"、"俯拍"
5. **背景环境**: 如"纯色背景"、"生活场景"、"悬浮效果"
6. **画质要求**: 如"8k超高清"、"商业级摄影"、"细节丰富"

### Negative Prompt应包含：
- 通用负面词汇: "blurry, low quality, distorted, deformed..."
- 产品特定负面: 根据产品类型调整

### 参数建议：
- steps: 20-40 (质量与速度平衡)
- cfg_scale: 7-9 (遵循prompt的程度)
- sampler: 推荐适合产品的采样器

## 输出格式（严格JSON）：

{
  "positive_prompt": "详细的正向提示词",
  "negative_prompt": "详细的负向提示词",
  "suggested_settings": {
    "steps": 30,
    "cfg_scale": 7.5,
    "sampler": "DPM++ 2M Karras",
    "width": 1024,
    "height": 1024
  },
  "style_description": "风格描述",
  "key_elements": ["元素1", "元素2"]
}
"""
        
        # 构建完整prompt
        if reference_analysis:
            prompt_template = f"""
{system_instruction}

---

**参考产品分析结果：**
{reference_analysis}

**用户需求：**
{user_input}

**任务：**
基于参考产品的成功视觉元素（配色方案、构图风格、光影处理），
结合用户需求，生成优化的提示词。

重点：
1. 保留参考产品的成功设计模式
2. 适配新产品的特性
3. 确保商业级别的视觉效果
"""
        else:
            prompt_template = f"""
{system_instruction}

---

**用户需求：**
{user_input}

{f'**风格偏好：** {style_preference}' if style_preference else ''}

**任务：**
根据用户需求生成专业的电商产品图提示词。

要求：
1. 突出产品主体和专业性
2. 商业级画质标准
3. 吸引人的视觉效果
4. 符合电商营销审美
"""
        
        try:
            # 调用LLM生成
            response = self.llm.invoke(prompt_template)
            
            # 尝试解析JSON
            result_text = response.content
            
            # 清理可能的markdown标记
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            try:
                result_json = json.loads(result_text.strip())
            except:
                # 如果解析失败，构造默认结构
                result_json = {
                    "positive_prompt": user_input + ", professional product photography, high quality, detailed",
                    "negative_prompt": "blurry, low quality, distorted, ugly, bad lighting",
                    "suggested_settings": {
                        "steps": 30,
                        "cfg_scale": 7.5,
                        "sampler": "DPM++ 2M Karras",
                        "width": 1024,
                        "height": 1024
                    },
                    "style_description": "专业电商风格",
                    "key_elements": []
                }
            
            return json.dumps(result_json, ensure_ascii=False, indent=2)
            
        except Exception as e:
            error_msg = f"提示词优化失败: {str(e)}"
            return json.dumps({"error": error_msg}, ensure_ascii=False)
