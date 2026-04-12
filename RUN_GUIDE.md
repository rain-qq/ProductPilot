# 🚀 运行 ProductPilot 项目

## 方法一：运行示例脚本（推荐新手）

最简单的方式，测试核心功能：

```bash
cd d:/workspace/ProductPilot
python examples/gemini_example.py
```

这会：
- ✅ 测试 Gemini API 连接
- ✅ 演示 Agent 工作
- ✅ 不需要 Stable Diffusion

---

## 方法二：启动 API 服务器

如果你想启动完整的 Web API 服务：

```bash
cd d:/workspace/ProductPilot
python main.py
```

启动后访问：
- 📖 API 文档: http://localhost:8000/docs
- 💚 健康检查: http://localhost:8000/api/v1/health

---

## 方法三：直接使用工作流（最快）

创建测试脚本：

```python
# test.py
from workflows.image_generation import ImageGenerationWorkflow

workflow = ImageGenerationWorkflow()

# 测试文本生图
result = workflow.run(
    prompt="professional product photo of wireless earbuds",
    mode="text2img"
)

print(f"成功: {result['success']}")
```

运行：
```bash
python test.py
```

---

## ⚠️ 运行前检查清单

### ✅ 必需配置
- [x] Python 3.11.9 已安装
- [x] `.env` 文件已创建
- [x] `GOOGLE_API_KEY` 已配置
- [ ] 依赖包已安装 (`pip install -r requirements.txt`)

### ⚙️ 可选配置
- [ ] Stable Diffusion WebUI (如需本地生图)
  - 下载: https://github.com/AUTOMATIC1111/stable-diffusion-webui
  - 运行: `webui-user.bat` (Windows)
  - 默认地址: http://localhost:7860

---

## 🐛 常见问题

### Q1: "ModuleNotFoundError: No module named 'xxx'"
**解决**: 依赖未安装完整
```bash
pip install -r requirements.txt
```

### Q2: "Gemini LLM not initialized"
**解决**: 检查 `.env` 文件中的 `GOOGLE_API_KEY` 是否正确

### Q3: "SD WebUI connection failed"
**解决**: 这是正常的，你可以：
- 选项A: 忽略此错误（使用DALL-E或仅测试LLM功能）
- 选项B: 安装并启动 Stable Diffusion WebUI

### Q4: 如何只测试 Gemini 不测试图片生成？
**运行**: 
```bash
python examples/gemini_example.py
```

---

## 📊 当前可用功能

| 功能 | 状态 | 说明 |
|------|------|------|
| Gemini LLM | ✅ 可用 | 已配置API密钥 |
| CrewAI Agents | ✅ 可用 | 多Agent协作 |
| LangGraph Workflow | ✅ 可用 | 工作流引擎 |
| FastAPI Server | ✅ 可用 | RESTful API |
| SD txt2img | ⚠️ 需配置 | 需要SD WebUI运行 |
| SD img2img | ⚠️ 需配置 | 需要SD WebUI运行 |
| ControlNet | ⚠️ 需配置 | 需要SD + ControlNet扩展 |

---

## 💡 建议的运行顺序

1. **第一步**: 测试 Gemini API
   ```bash
   python examples/gemini_example.py
   ```

2. **第二步**: 测试 Agent 协作
   ```bash
   python examples/basic_usage.py
   # 修改第165行，调用 example_4_direct_workflow()
   ```

3. **第三步**: 启动 API 服务器
   ```bash
   python main.py
   ```

4. **第四步** (可选): 配置 Stable Diffusion
   - 安装 SD WebUI
   - 启动后配置 `SD_WEBUI_URL=http://localhost:7860`

---

## 🎯 快速验证是否成功

运行这个命令：

```bash
python -c "
from config.settings import settings
from services.llm_service import LLMService

print('✅ 配置加载成功')
print(f'Gemini API Key: {settings.GOOGLE_API_KEY[:10]}...')
print(f'选定模型: {settings.GEMINI_MODEL}')

llm_service = LLMService()
providers = llm_service.get_available_providers()
print(f'可用LLM提供商: {providers}')
"
```

如果看到输出，说明配置正确！🎉

---

## 📚 更多帮助

- 📖 完整文档: `README.md`
- 🔧 API配置: `API_CONFIG.md`
- 🏗️ 架构说明: `ARCHITECTURE.md`
- 📂 项目导航: `NAVIGATION.md`

有问题随时提问！😊
