# ProductPilot - AI电商图片生成系统

基于 **CrewAI + LangGraph 混合架构**的智能电商图片生成系统，支持参照产品生图和提示词生图两种模式。

## 🌟 特性

- ✅ **混合架构**: CrewAI负责任务协调，LangGraph负责精确流程控制
- ✅ **多种模式**: 支持 text2img、img2img、mixed 三种生成模式
- ✅ **智能质检**: 自动质量评估和重新生成循环
- ✅ **角色协作**: 产品经理、设计师、画师、质检员多Agent协同
- ✅ **灵活扩展**: 模块化设计，易于添加新Agent和工作流
- ✅ **生产就绪**: FastAPI异步接口，支持批量处理

## 📋 目录结构

```
ProductPilot/
├── agents/                    # CrewAI Agents层
│   ├── product_analyst.py    # 产品分析师
│   ├── prompt_engineer.py    # 提示词工程师
│   ├── image_creator.py      # 图片创作师(调用工作流)
│   └── quality_reviewer.py   # 质量审核员
├── workflows/                 # LangGraph工作流层
│   └── image_generation.py   # 图片生成工作流
├── services/                  # 服务层
│   ├── image_service.py      # 图片处理服务
│   └── llm_service.py        # LLM服务
├── models/                    # 数据模型
│   └── schemas.py            # Pydantic模型
├── api/                       # API接口
│   └── routes.py             # FastAPI路由
├── config/                    # 配置
│   └── settings.py           # 应用配置
├── examples/                  # 使用示例
│   └── basic_usage.py
├── main.py                    # 应用入口
├── requirements.txt           # Python依赖
├── .env.example              # 环境变量示例
└── README.md                  # 本文档
```

## 🚀 快速开始

### 1. 环境准备

**要求:**
- Python 3.9+
- (可选) Stable Diffusion WebUI - 用于本地图片生成

### 2. 安装依赖

```bash
# 克隆项目
git clone <your-repo>
cd ProductPilot

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填入你的API密钥
```

编辑 `.env` 文件：

```env
# OpenAI API (必需)
OPENAI_API_KEY=sk-your-openai-key-here

# Stable Diffusion WebUI (可选 - 如使用本地SD)
SD_WEBUI_URL=http://localhost:7860

# 质量阈值
QUALITY_THRESHOLD=0.8
```

### 4. 运行应用

#### 方式A: 启动API服务器

```bash
python main.py
```

访问 http://localhost:8000/docs 查看API文档

#### 方式B: 运行示例脚本

```bash
python examples/basic_usage.py
```

## 💡 使用方式

### 1. 通过API使用

```python
import requests

# 生成电商图片
response = requests.post("http://localhost:8000/api/v1/generate", json={
    "product_info": {
        "name": "蓝牙耳机",
        "description": "黑色磨砂质感，无线降噪",
        "category": "数码配件"
    },
    "mode": "text2img",
    "quality_threshold": 0.8
})

result = response.json()
print(result)
```

### 2. 直接在代码中使用

```python
from workflows.image_generation import ImageGenerationWorkflow

# 直接使用工作流
workflow = ImageGenerationWorkflow()
result = workflow.run(
    prompt="professional photo of wireless earbuds, black matte, studio lighting",
    negative_prompt="blurry, low quality",
    reference_image=None,
    mode="text2img"
)

print(f"生成成功! 最佳图片评分: {max(result['quality_scores']):.2f}")
```

### 3. 使用CrewAI团队

```python
from agents.prompt_engineer import PromptEngineerAgent
from agents.image_creator import ImageCreatorAgent
from crewai import Crew, Process, Task

# 创建团队
engineer = PromptEngineerAgent()
creator = ImageCreatorAgent()

# 定义任务
prompt_task = Task(
    description="为蓝牙耳机生成AI绘画提示词",
    agent=engineer
)

generation_task = Task(
    description="根据提示词生成图片",
    agent=creator,
    context=[prompt_task]
)

# 执行
crew = Crew(
    agents=[engineer, creator],
    tasks=[prompt_task, generation_task],
    process=Process.sequential
)

result = crew.kickoff()
```

## 🏗️ 架构说明

### 混合架构设计

```
┌─────────────────────────────────────┐
│       CrewAI Agent Team             │  ← 高层协作
│  ┌──────────┐  ┌──────────┐        │
│  │ Analyst  │  │ Engineer │        │
│  └──────────┘  └──────────┘        │
│  ┌──────────┐  ┌──────────┐        │
│  │ Creator  │  │ Reviewer │        │
│  └────┬─────┘  └──────────┘        │
└───────┼─────────────────────────────┘
        │ 调用
┌───────▼─────────────────────────────┐
│    LangGraph Workflow Engine        │  ← 底层执行
│  ┌────────────────────────────┐     │
│  │ preprocess → generate →    │     │
│  │ quality_check → [loop]     │     │
│  └────────────────────────────┘     │
└─────────────────────────────────────┘
```

### 工作流程

1. **产品分析** (可选): 分析参考图片的视觉特征
2. **提示词优化**: 将产品描述转换为专业prompt
3. **图片生成**: 调用LangGraph工作流
   - 预处理参考图
   - 执行生成 (text2img/img2img/mixed)
   - 质量检查
   - 不合格则重新生成
4. **质量审核**: 最终评估并选择最佳图片

## ⚙️ 配置说明

### 主要配置项 (.env)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| OPENAI_API_KEY | OpenAI API密钥 | 必需 |
| SD_WEBUI_URL | SD WebUI地址 | http://localhost:7860 |
| QUALITY_THRESHOLD | 质量阈值 | 0.8 |
| MAX_IMAGE_GENERATION_RETRIES | 最大重试次数 | 3 |
| DEFAULT_IMAGE_WIDTH | 默认图片宽度 | 1024 |
| DEFAULT_IMAGE_HEIGHT | 默认图片高度 | 1024 |

## 🔧 高级用法

### 自定义工作流节点

在 `workflows/image_generation.py` 中添加新节点：

```python
def custom_node(self, state: ImageGenerationState) -> Dict:
    # 你的自定义逻辑
    return {...}

# 在 _build_workflow 中添加
workflow.add_node("custom", self.custom_node)
workflow.add_edge("previous", "custom")
```

### 添加新的Agent

在 `agents/` 目录创建新文件：

```python
from crewai import Agent

class MyCustomAgent(Agent):
    def __init__(self):
        super().__init__(
            role='角色名称',
            goal='目标',
            backstory='背景故事',
            ...
        )
```

## 📊 性能优化建议

1. **批量处理**: 使用异步接口 `/generate/async`
2. **缓存策略**: 缓存常用prompt模板
3. **GPU加速**: 本地部署SD时使用GPU
4. **CDN加速**: 图片存储使用CDN

## 🐛 常见问题

### Q: 报错 "OpenAI API key not found"
A: 请确保已复制 `.env.example` 为 `.env` 并填写了正确的API密钥。

### Q: Stable Diffusion连接失败
A: 确保SD WebUI正在运行 (`./webui.sh --api`)，并且 `SD_WEBUI_URL` 配置正确。

### Q: 质量检查一直不通过
A: 调整 `.env` 中的 `QUALITY_THRESHOLD`，或优化prompt质量。

### Q: 如何切换DALL-E和Stable Diffusion?
A: 在 `services/image_service.py` 中修改调用逻辑，目前默认使用SD WebUI。

## 📝 开发计划

- [ ] 支持更多图像生成模型 (DALL-E 3, Midjourney)
- [ ] 添加图片后处理功能 (超分、调色)
- [ ] 实现任务队列 (Celery + Redis)
- [ ] 添加数据库持久化
- [ ] Web管理界面
- [ ] 更多预设模板

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题请提Issue或联系开发者。

---

**享受用AI生成电商图片的乐趣！** 🎨✨
