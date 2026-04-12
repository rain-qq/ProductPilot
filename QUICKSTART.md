# 快速开始指南 🚀

5分钟快速运行ProductPilot

## 步骤1: 安装依赖 (2分钟)

```bash
cd ProductPilot
pip install -r requirements.txt
```

## 步骤2: 配置API密钥 (1分钟)

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件，填入你的OpenAI API密钥：

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**获取API密钥:**
- 访问 https://platform.openai.com/api-keys
- 注册/登录OpenAI账号
- 创建新的API密钥

## 步骤3: 运行 (2分钟)

### 选项A: 运行示例脚本 (推荐新手)

```bash
python examples/basic_usage.py
```

这会演示如何使用工作流直接生成图片。

### 选项B: 启动API服务器

```bash
python main.py
```

然后访问 http://localhost:8000/docs 查看和测试API。

## 常见问题

### ❓ 没有Stable Diffusion可以运行吗?

**可以!** 有两种方式:

1. **使用DALL-E 3 API** (简单): 
   - 修改 `services/image_service.py`
   - 添加DALL-E 3调用逻辑
   - 无需本地GPU

2. **安装Stable Diffusion WebUI** (推荐用于批量):
   - 下载: https://github.com/AUTOMATIC1111/stable-diffusion-webui
   - 运行: `./webui.sh --api` (Linux) 或 `webui-user.bat` (Windows)
   - 默认地址: http://localhost:7860

### ❓ 需要GPU吗?

- **不使用SD**: 不需要GPU (使用DALL-E API)
- **使用SD本地部署**: 建议有NVIDIA GPU (4GB+显存)

### ❓ 如何测试是否正常工作?

运行测试脚本:

```bash
python -c "
from config.settings import settings
print('✅ 配置加载成功')
print(f'OpenAI API Key: {settings.OPENAI_API_KEY[:10]}...')
"
```

## 下一步

1. 📖 阅读完整文档: `README.md`
2. 🔧 自定义Agent: 修改 `agents/` 目录下的文件
3. 🎨 调整工作流: 编辑 `workflows/image_generation.py`
4. 🚀 集成到你的项目: 使用API接口

## 需要帮助?

- 查看 `README.md` 了解更多细节
- 查看 `examples/basic_usage.py` 了解代码示例
- 提Issue报告问题

---

祝你使用愉快! 🎉
