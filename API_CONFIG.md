# API配置指南 🔑

ProductPilot支持多种LLM提供商，你可以选择最适合你的方案。

## 📋 支持的LLM提供商

| 提供商 | 模型 | 成本 | 速度 | 推荐场景 |
|--------|------|------|------|---------|
| **OpenAI** | GPT-4, GPT-3.5 | 中等 | 快 | 通用场景，效果最佳 |
| **Google Gemini** | Gemini Pro | 较低 | 快 | 性价比之选 |
| **Anthropic Claude** | Claude-3 | 较高 | 中等 | 复杂推理任务 |

## ⚙️ 配置步骤

### 方案A: 使用 Google Gemini (推荐 - 性价比高)

#### 1. 获取API密钥
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录Google账号
3. 创建新的API密钥
4. 复制密钥

#### 2. 配置 `.env` 文件

```env
# Google Gemini API Configuration
GOOGLE_API_KEY=AIzaSy...your_gemini_key_here
GEMINI_MODEL=gemini-pro

# OpenAI API (可选 - 如不使用可留空)
OPENAI_API_KEY=
```

#### 3. 测试Gemini

```bash
python examples/gemini_example.py
```

---

### 方案B: 使用 OpenAI (经典方案)

#### 1. 获取API密钥
1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 注册/登录账号
3. 创建新的secret key
4. 复制密钥 (以 `sk-` 开头)

#### 2. 配置 `.env` 文件

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# Google Gemini (可选 - 如不使用可留空)
GOOGLE_API_KEY=
```

#### 3. 测试

```bash
python examples/basic_usage.py
```

---

### 方案C: 同时配置多个提供商 (灵活切换)

```env
# 同时配置多个API密钥
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=AIzaSy-your-gemini-key
ANTHROPIC_API_KEY=sk-ant-your-claude-key

# 默认使用Gemini (在代码中指定)
```

然后在代码中选择使用：

```python
from services.llm_service import LLMService

llm_service = LLMService()

# 方式1: 自动选择第一个可用的
llm = llm_service.get_llm(provider="auto")

# 方式2: 明确指定使用Gemini
llm = llm_service.get_llm(provider="gemini")

# 方式3: 明确指定使用OpenAI
llm = llm_service.get_llm(provider="openai")
```

---

## 🔧 常见问题

### Q1: 如何查看当前可用的LLM提供商?

```python
from services.llm_service import LLMService

llm_service = LLMService()
providers = llm_service.get_available_providers()
print(f"可用的提供商: {providers}")
# 输出: ['gemini', 'openai']
```

### Q2: Gemini的API密钥格式是什么?

Gemini密钥以 `AIzaSy` 开头，例如:
```
AIzaSyA1b2C3d4E5f6G7h8I9j0KlMnOpQrStUvWxYz
```

### Q3: OpenAI的API密钥格式是什么?

OpenAI密钥以 `sk-` 开头，例如:
```
sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx
```

### Q4: 如何在Agent中指定使用Gemini?

```python
from crewai import Agent
from services.llm_service import LLMService

# 获取Gemini LLM
llm_service = LLMService()
gemini_llm = llm_service.get_llm(provider="gemini")

# 创建Agent时使用Gemini
my_agent = Agent(
    role='我的角色',
    goal='我的目标',
    backstory='我的背景',
    llm=gemini_llm  # 指定使用Gemini
)
```

### Q5: 如何全局切换到Gemini?

修改所有Agent的初始化，传入Gemini LLM：

```python
# 在 agents/product_analyst.py 中
class ProductAnalystAgent(Agent):
    def __init__(self):
        llm_service = LLMService()
        gemini_llm = llm_service.get_llm(provider="gemini")
        
        super().__init__(
            role='...',
            goal='...',
            llm=gemini_llm  # 使用Gemini
        )
```

---

## 💰 成本对比

以生成1000张电商图片为例（需要调用LLM约5000次）：

| 提供商 | 模型 | 预估成本 |
|--------|------|---------|
| OpenAI | GPT-4 | $50-100 |
| OpenAI | GPT-3.5 | $5-10 |
| **Google** | **Gemini Pro** | **$2-5** ⭐ |
| Anthropic | Claude-3 | $30-60 |

**Gemini性价比最高!** 🎯

---

## 🚀 快速开始 (Gemini)

```bash
# 1. 配置环境变量
echo "GOOGLE_API_KEY=AIzaSy-your-key-here" > .env

# 2. 安装依赖
pip install -r requirements.txt

# 3. 测试Gemini
python examples/gemini_example.py

# 4. 启动应用
python main.py
```

---

## 📝 总结

✅ **推荐使用Gemini**:
- 成本低 (比GPT-4便宜20倍)
- 速度快
- 效果好
- 免费额度充足

✅ **配置简单**:
- 只需设置 `GOOGLE_API_KEY`
- 代码自动适配

✅ **灵活切换**:
- 支持多提供商
- 运行时可选择

---

**有问题?** 查阅文档或提Issue 🐛
