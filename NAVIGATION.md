# 📚 ProductPilot 项目导航

快速找到你需要的内容！

## 🎯 我想...

### 快速上手
- 🚀 **5分钟运行** → [`QUICKSTART.md`](QUICKSTART.md)
- 📖 **完整文档** → [`README.md`](README.md)
- 💻 **看代码示例** → [`examples/basic_usage.py`](examples/basic_usage.py)

### 理解架构
- 🏗️ **架构详解** → [`ARCHITECTURE.md`](ARCHITECTURE.md)
- 📊 **项目总结** → [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)

### 开发定制
- 👥 **修改Agent** → [`agents/`](agents/) 目录
- 🔄 **调整工作流** → [`workflows/image_generation.py`](workflows/image_generation.py)
- 🛠️ **扩展服务** → [`services/`](services/) 目录
- 🌐 **添加API** → [`api/routes.py`](api/routes.py)

### 配置部署
- ⚙️ **环境配置** → [`.env.example`](.env.example)
- 📦 **依赖管理** → [`requirements.txt`](requirements.txt)
- 🔧 **启动应用** → [`main.py`](main.py)

## 📂 文件速查

### 核心代码文件

| 文件 | 用途 | 修改频率 |
|------|------|---------|
| `agents/product_analyst.py` | 产品分析师Agent | 🔧 定制分析逻辑 |
| `agents/prompt_engineer.py` | 提示词工程师Agent | 🔧 优化prompt策略 |
| `agents/image_creator.py` | 图片创作师Agent | ⚙️ 较少修改 |
| `agents/quality_reviewer.py` | 质量审核员Agent | 🔧 调整评分标准 |
| `workflows/image_generation.py` | 图片生成工作流 | 🔧🔧 核心逻辑 |
| `services/image_service.py` | 图片处理服务 | 🔧🔧 集成新模型 |
| `services/llm_service.py` | LLM服务 | ⚙️ 较少修改 |
| `models/schemas.py` | 数据模型定义 | ➕ 添加新字段 |
| `api/routes.py` | API路由 | ➕ 添加新接口 |
| `config/settings.py` | 应用配置 | 🔧 添加配置项 |
| `main.py` | 应用入口 | ⚙️ 较少修改 |

### 文档文件

| 文档 | 适合人群 | 内容 |
|------|---------|------|
| `README.md` | 所有人 | 项目介绍、安装、使用 |
| `QUICKSTART.md` | 新手用户 | 5分钟快速开始指南 |
| `ARCHITECTURE.md` | 开发者 | 架构设计、组件说明 |
| `PROJECT_SUMMARY.md` | 项目负责人 | 项目总结、交付清单 |

### 配置文件

| 文件 | 作用 |
|------|------|
| `.env.example` | 环境变量模板 |
| `.gitignore` | Git忽略规则 |
| `requirements.txt` | Python依赖清单 |

## 🔍 按功能查找

### Agent相关
```
agents/
├── product_analyst.py      # 分析参考产品
├── prompt_engineer.py      # 优化提示词
├── image_creator.py        # 生成图片
└── quality_reviewer.py     # 质量审核
```

### 工作流相关
```
workflows/
└── image_generation.py     # 6节点工作流
    ├── preprocess          # 预处理
    ├── generate            # 生成
    ├── quality_check       # 质检
    ├── regenerate          # 重新生成
    ├── post_process        # 后处理
    └── error_handler       # 错误处理
```

### 服务相关
```
services/
├── image_service.py        # 图片处理
│   ├── text_to_image()
│   ├── image_to_image()
│   ├── controlnet_generate()
│   ├── preprocess()
│   ├── enhance()
│   └── extract_features()
└── llm_service.py          # LLM调用
```

### API接口
```
api/routes.py
├── POST /generate          # 同步生成
├── POST /generate/async    # 异步生成
├── GET /task/{id}          # 查询任务
└── GET /health             # 健康检查
```

## 💡 常见场景导航

### 场景1: 我只想快速试试效果
```bash
1. cp .env.example .env
2. 编辑 .env 填入 API_KEY
3. pip install -r requirements.txt
4. python examples/basic_usage.py
```

### 场景2: 我要修改Agent的行为
```
1. 打开 agents/ 目录
2. 找到对应的Agent文件
3. 修改 role/goal/backstory
4. 或添加工具方法
```

### 场景3: 我要调整工作流
```
1. 打开 workflows/image_generation.py
2. 找到 _build_workflow() 方法
3. 添加/修改节点
4. 更新边的连接关系
```

### 场景4: 我要集成到自己的SD
```
1. 修改 services/image_service.py
2. 调整 SD_WEBUI_URL 配置
3. 或替换为DALL-E调用
```

### 场景5: 我要添加新功能
```
1. 查看 models/schemas.py 添加数据模型
2. 在 services/ 添加业务逻辑
3. 在 api/routes.py 添加API接口
4. 更新 README.md 文档
```

## 🎓 学习路径推荐

### Day 1: 了解全貌
1. 阅读 `README.md` (30分钟)
2. 运行 `examples/basic_usage.py` (15分钟)
3. 浏览 `ARCHITECTURE.md` (30分钟)

### Day 2: 深入理解
1. 阅读 `workflows/image_generation.py` (1小时)
2. 阅读各个Agent代码 (1小时)
3. 尝试修改参数和prompt (30分钟)

### Day 3: 动手定制
1. 添加自己的Agent (2小时)
2. 调整工作流节点 (1小时)
3. 测试和优化 (1小时)

## 📞 需要帮助?

1. **查看文档**: 90%的问题文档中都有答案
2. **查看示例**: `examples/basic_usage.py` 包含4个完整示例
3. **搜索代码**: 使用IDE的全局搜索功能
4. **提Issue**: 遇到Bug请提供详细信息

## 🔗 外部资源

- [CrewAI官方文档](https://docs.crewai.com)
- [LangGraph教程](https://langchain-ai.github.io/langgraph)
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [FastAPI文档](https://fastapi.tiangolo.com)
- [OpenAI API文档](https://platform.openai.com/docs)

---

**提示**: 建议先通读 `README.md` 和 `QUICKSTART.md`，再根据需求查看其他文档。

Happy Coding! 🚀
