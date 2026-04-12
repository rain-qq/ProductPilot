# ProductPilot 快速启动指南

## 🚀 5分钟快速开始

### 前置要求

1. ✅ Python 3.9+
2. ✅ Docker Desktop (运行 MinIO)
3. ✅ Stable Diffusion WebUI (可选,用于本地生图)
4. ✅ LLM API Key (OpenAI 或 Google Gemini)

---

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd ProductPilot
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件,填入你的 API Key:

```bash
# 选择一种 LLM 提供商
OPENAI_API_KEY=sk-your-openai-key
# 或
GOOGLE_API_KEY=your-gemini-key
GEMINI_MODEL=gemini-pro
```

### 4. 启动 MinIO (Docker)

```bash
docker run -d \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio \
  -v minio_data:/data \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

**验证 MinIO:**
- API: http://localhost:9000
- 控制台: http://localhost:9001 (账号: minioadmin/minioadmin)

### 5. (可选) 启动 Stable Diffusion WebUI

如果使用本地 SD,确保 WebUI 正在运行并开启 API 模式:

```bash
# 在 SD WebUI 目录执行
./webui.sh --api  # Linux/Mac
webui.bat --api   # Windows
```

默认地址: http://localhost:7860

---

## ▶️ 启动服务

### 方式 1: 直接运行

```bash
python main.py
```

### 方式 2: 使用启动脚本

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

服务将在 **http://localhost:8000** 启动

---

## 🧪 测试功能

### 1. 访问 API 文档

浏览器打开: **http://localhost:8000/docs**

### 2. 健康检查

```bash
curl http://localhost:8000/health
```

预期输出:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-12T19:00:00.000000"
}
```

### 3. 测试 MinIO 存储

```bash
python test_minio.py
```

预期看到:
```
✅ MinIO 客户端初始化成功
✅ Bucket 'ecommerce-images' 已存在
✅ 上传成功!
```

### 4. 生成第一张图片

#### 方法 A: 使用 Swagger UI

1. 访问 http://localhost:8000/docs
2. 找到 `POST /generate/async` 接口
3. 点击 "Try it out"
4. 填写请求体:

```json
{
  "product_info": {
    "name": "无线蓝牙耳机",
    "description": "高品质降噪无线蓝牙耳机,续航时间长达30小时",
    "category": "数码配件",
    "key_features": ["主动降噪", "长续航", "舒适佩戴"]
  },
  "mode": "text2img",
  "num_images": 2,
  "quality_threshold": 0.8
}
```

5. 点击 "Execute"
6. 记录返回的 `task_id`
7. 使用 `GET /task/{task_id}` 查询结果

#### 方法 B: 使用 cURL

```bash
curl -X POST "http://localhost:8000/generate/async" \
  -H "Content-Type: application/json" \
  -d '{
    "product_info": {
      "name": "智能手表",
      "description": "多功能运动智能手表",
      "category": "智能穿戴",
      "key_features": ["心率监测", "防水设计"]
    },
    "mode": "text2img",
    "num_images": 2
  }'
```

#### 方法 C: 使用示例脚本

```bash
python examples/basic_usage.py
```

---

## 📸 查看生成的图片

### 方法 1: MinIO 控制台

1. 访问 http://localhost:9001
2. 登录 (minioadmin/minioadmin)
3. 进入 `ecommerce-images` bucket
4. 查看所有生成的图片

### 方法 2: 直接访问 URL

从 API 响应中获取图片 URL:

```
http://localhost:9000/ecommerce-images/20260412_190326_a3f2b1c4.png
```

在浏览器中打开即可查看。

---

## 🔍 故障排查

### 问题 1: MinIO 连接失败

**症状:**
```
❌ MinIO 客户端未初始化
```

**解决方案:**
1. 检查 Docker 容器是否运行:
   ```bash
   docker ps | grep minio
   ```
2. 如果未运行,重新启动 MinIO
3. 检查端口 9000 是否被占用

### 问题 2: SD WebUI 连接失败

**症状:**
```
Error in text_to_image: Connection refused
```

**解决方案:**
1. 确保 SD WebUI 正在运行
2. 检查 `.env` 中的 `SD_WEBUI_URL` 配置
3. 确认 WebUI 已启用 API 模式 (`--api` 参数)

### 问题 3: LLM API 调用失败

**症状:**
```
OpenAI API error: Invalid API key
```

**解决方案:**
1. 检查 `.env` 中的 API Key 是否正确
2. 确认账户余额充足
3. 如使用 Gemini,确保安装了 `langchain-google-genai`

### 问题 4: 图片生成质量低

**优化建议:**
1. 提高 `quality_threshold` (0.85-0.95)
2. 增加 `max_retries` (3-5)
3. 提供更详细的产品描述
4. 使用参考图片 (img2img 模式)

---

## 📚 下一步

- 📖 阅读 [API 文档](./API_DOCUMENTATION.md) 了解所有接口
- 🗄️ 查看 [MinIO 使用指南](./MINIO_GUIDE.md) 管理图片存储
- 🏗️ 了解 [系统架构](./ARCHITECTURE.md)
- 💡 查看更多 [使用示例](./examples/)

---

## 🆘 获取帮助

- 📝 查看 [常见问题](./API_DOCUMENTATION.md#-常见问题)
- 🐛 提交 GitHub Issue
- 📧 联系技术支持

---

**祝你使用愉快! 🎉**