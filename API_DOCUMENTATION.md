# ProductPilot API 接口文档

## 📖 概述

ProductPilot 是一个基于 AI 的智能电商图片生成系统,提供 RESTful API 接口用于自动生成高质量的电商营销图片。

**基础信息:**
- **Base URL**: `http://localhost:8000`
- **API 文档**: `http://localhost:8000/docs` (Swagger UI)
- **OpenAPI 规范**: `http://localhost:8000/openapi.json`
- **健康检查**: `GET /health`

---

## 🔐 认证说明

当前版本暂不需要 API Key,生产环境建议添加认证机制。

---

## 📋 接口列表

### 1. 健康检查

**接口地址**: `GET /health`

**功能描述**: 检查服务是否正常运行

**请求参数**: 无

**响应示例**:
``json
{
  "status": "healthy",
  "timestamp": "2026-04-12T18:44:59.123456"
}
```

---

### 2. 同步生成图片

**接口地址**: `POST /generate`

**功能描述**: 同步生成电商图片,等待生成完成后返回结果(适合少量图片生成)

**请求头**:
```
Content-Type: application/json
```

**请求体**:
```json
{
  "product_info": {
    "name": "无线蓝牙耳机",
    "description": "高品质降噪无线蓝牙耳机,续航时间长达30小时",
    "category": "数码配件",
    "target_audience": "年轻白领、学生群体",
    "key_features": [
      "主动降噪",
      "长续航",
      "舒适佩戴",
      "高清音质"
    ],
    "reference_image_url": "https://example.com/reference.jpg"
  },
  "mode": "mixed",
  "num_images": 4,
  "quality_threshold": 0.8,
  "max_retries": 3,
  "negative_prompt": "blurry, low quality, distorted",
  "style_preference": "现代简约风格",
  "custom_settings": {
    "aspect_ratio": "1:1"
  }
}
```

**请求参数说明**:

| 参数路径 | 类型 | 必填 | 说明 |
|---------|------|------|------|
| `product_info.name` | string | ✅ | 商品名称 |
| `product_info.description` | string | ✅ | 商品描述 |
| `product_info.category` | string | ❌ | 商品类别 |
| `product_info.target_audience` | string | ❌ | 目标人群 |
| `product_info.key_features` | array[string] | ❌ | 核心卖点列表 |
| `product_info.reference_image_url` | string | ❌ | 参考图片URL(用于img2img模式) |
| `mode` | enum | ❌ | 生成模式:`text2img`/`img2img`/`mixed`,默认`mixed` |
| `num_images` | integer | ❌ | 生成图片数量(1-10),默认4 |
| `quality_threshold` | float | ❌ | 质量阈值(0.0-1.0),默认0.8 |
| `max_retries` | integer | ❌ | 最大重试次数(1-5),默认3 |
| `negative_prompt` | string | ❌ | 负向提示词 |
| `style_preference` | string | ❌ | 风格偏好描述 |
| `custom_settings` | object | ❌ | 自定义设置 |

**响应示例**(成功):
``json
{
  "success": true,
  "images": [
    {
      "url": "https://cdn.example.com/generated/image_001.png",
      "thumbnail_url": "https://cdn.example.com/thumbnails/thumb_001.png",
      "width": 1024,
      "height": 1024,
      "format": "png",
      "size_bytes": 2048576
    },
    {
      "url": "https://cdn.example.com/generated/image_002.png",
      "thumbnail_url": "https://cdn.example.com/thumbnails/thumb_002.png",
      "width": 1024,
      "height": 1024,
      "format": "png",
      "size_bytes": 1987654
    }
  ],
  "selected_image": {
    "url": "https://cdn.example.com/generated/image_001.png",
    "thumbnail_url": "https://cdn.example.com/thumbnails/thumb_001.png",
    "width": 1024,
    "height": 1024,
    "format": "png",
    "size_bytes": 2048576
  },
  "quality_scores": [0.92, 0.88, 0.85, 0.90],
  "iteration_count": 1,
  "analysis_result": {
    "color_scheme": ["#FF5733", "#33FF57", "#3357FF"],
    "composition_type": "中心构图",
    "lighting_style": "柔和自然光",
    "background_type": "纯色背景",
    "viewing_angle": "正面视角",
    "style_tags": ["简约", "现代", "科技感"],
    "marketing_points": ["突出产品质感", "强调功能特性"]
  },
  "prompt_result": {
    "positive_prompt": "professional product photography of wireless earbuds, clean white background, studio lighting, high detail, 8k",
    "negative_prompt": "blurry, low quality, distorted, watermark",
    "suggested_settings": {
      "steps": 30,
      "cfg_scale": 7.5
    }
  },
  "quality_evaluations": [
    {
      "overall_score": 0.92,
      "clarity": 0.95,
      "color_accuracy": 0.90,
      "composition": 0.88,
      "commercial_value": 0.94,
      "issues": [],
      "suggestions": ["可以尝试增加一些场景元素"]
    }
  ],
  "error_message": null,
  "metadata": {
    "generation_time": 45.2,
    "model_version": "sd-xl-1.0"
  }
}
```

**响应示例**(失败):
``json
{
  "detail": "图片生成失败: API调用超时"
}
```

**错误码**:
- `400`: 请求参数错误
- `500`: 服务器内部错误

---

### 3. 异步生成图片

**接口地址**: `POST /generate/async`

**功能描述**: 异步提交图片生成任务,立即返回任务ID(适合批量处理)

**请求头**:
```
Content-Type: application/json
```

**请求体**: 与 `/generate` 接口相同

**响应示例**:
``json
{
  "task_id": "a3f2b1c4-5d6e-7f8g-9h0i-1j2k3l4m5n6o",
  "status": "pending",
  "progress": 0.0,
  "current_step": "等待处理",
  "result": null,
  "error_message": null,
  "created_at": "2026-04-12T18:44:59.123456",
  "updated_at": "2026-04-12T18:44:59.123456"
}
```

**使用流程**:
1. 调用此接口提交任务,获取 `task_id`
2. 使用 `GET /task/{task_id}` 轮询查询任务状态
3. 当 `status` 为 `completed` 时,从 `result` 字段获取生成结果

---

### 4. 查询任务状态

**接口地址**: `GET /task/{task_id}`

**功能描述**: 查询异步任务的执行状态和结果

**路径参数**:
- `task_id` (string, 必填): 任务ID

**响应示例**(处理中):
``json
{
  "task_id": "a3f2b1c4-5d6e-7f8g-9h0i-1j2k3l4m5n6o",
  "status": "processing",
  "progress": 60.0,
  "current_step": "生成图片",
  "result": null,
  "error_message": null,
  "created_at": "2026-04-12T18:44:59.123456",
  "updated_at": "2026-04-12T18:45:30.654321"
}
```

**响应示例**(已完成):
``json
{
  "task_id": "a3f2b1c4-5d6e-7f8g-9h0i-1j2k3l4m5n6o",
  "status": "completed",
  "progress": 100.0,
  "current_step": "完成",
  "result": {
    "success": true,
    "images": [
      {
        "url": "https://cdn.example.com/generated/image_001.png",
        "thumbnail_url": "https://cdn.example.com/thumbnails/thumb_001.png",
        "width": 1024,
        "height": 1024,
        "format": "png",
        "size_bytes": 2048576
      }
    ],
    "selected_image": {
      "url": "https://cdn.example.com/generated/image_001.png",
      "thumbnail_url": "https://cdn.example.com/thumbnails/thumb_001.png",
      "width": 1024,
      "height": 1024,
      "format": "png",
      "size_bytes": 2048576
    },
    "quality_scores": [0.92],
    "iteration_count": 1,
    "analysis_result": null,
    "prompt_result": null,
    "quality_evaluations": [],
    "error_message": null,
    "metadata": {}
  },
  "error_message": null,
  "created_at": "2026-04-12T18:44:59.123456",
  "updated_at": "2026-04-12T18:46:15.987654"
}
```

**响应示例**(失败):
``json
{
  "task_id": "a3f2b1c4-5d6e-7f8g-9h0i-1j2k3l4m5n6o",
  "status": "failed",
  "progress": 35.0,
  "current_step": "优化提示词",
  "result": null,
  "error_message": "LLM API调用失败: 余额不足",
  "created_at": "2026-04-12T18:44:59.123456",
  "updated_at": "2026-04-12T18:45:20.123456"
}
```

**任务状态枚举**:
- `pending`: 等待处理
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败

**进度说明**:
- `0-20%`: 分析产品需求
- `20-35%`: 优化提示词
- `35-60%`: 生成图片
- `60-80%`: 质量检查
- `80-95%`: 后处理
- `100%`: 完成

**错误码**:
- `404`: 任务不存在

---

## 🧪 测试示例

### 使用 cURL 测试

#### 1. 同步生成
```
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "product_info": {
      "name": "智能手表",
      "description": "多功能运动智能手表,支持心率监测",
      "category": "智能穿戴",
      "key_features": ["心率监测", "防水设计", "长续航"]
    },
    "mode": "text2img",
    "num_images": 2,
    "quality_threshold": 0.85
  }'
```

#### 2. 异步生成
```
curl -X POST "http://localhost:8000/generate/async" \
  -H "Content-Type: application/json" \
  -d '{
    "product_info": {
      "name": "运动鞋",
      "description": "专业跑步运动鞋,轻量化设计",
      "category": "运动装备"
    },
    "mode": "mixed",
    "num_images": 4
  }'
```

#### 3. 查询任务状态
```
curl -X GET "http://localhost:8000/task/a3f2b1c4-5d6e-7f8g-9h0i-1j2k3l4m5n6o"
```

### 使用 Python requests 测试

```
import requests
import time

BASE_URL = "http://localhost:8000"

# 异步生成任务
response = requests.post(f"{BASE_URL}/generate/async", json={
    "product_info": {
        "name": "咖啡杯",
        "description": "陶瓷保温咖啡杯,简约设计",
        "category": "家居用品",
        "key_features": ["保温", "环保材质", "易清洗"]
    },
    "mode": "text2img",
    "num_images": 3,
    "quality_threshold": 0.8
})

task_id = response.json()["task_id"]
print(f"任务ID: {task_id}")

# 轮询查询状态
while True:
    status_response = requests.get(f"{BASE_URL}/task/{task_id}")
    task_info = status_response.json()
    
    print(f"状态: {task_info['status']}, 进度: {task_info['progress']}%")
    
    if task_info["status"] in ["completed", "failed"]:
        break
    
    time.sleep(3)

# 输出结果
if task_info["status"] == "completed":
    result = task_info["result"]
    print(f"生成成功! 共 {len(result['images'])} 张图片")
    for img in result["images"]:
        print(f"  - {img['url']}")
else:
    print(f"生成失败: {task_info['error_message']}")
```

### 使用 Bruno 测试

1. 打开 Bruno,创建新 Collection
2. 导入 OpenAPI 规范:
   - 启动服务: `python main.py`
   - 访问 `http://localhost:8000/openapi.json` 下载 JSON
   - 在 Bruno 中选择 "Import" → "OpenAPI/Swagger" → 选择下载的 JSON 文件
3. 自动生成所有接口,填写参数后发送请求

---

## 📊 数据模型详解

### GenerationMode (生成模式)
- `text2img`: 纯文本生成图片
- `img2img`: 基于参考图生成
- `mixed`: 混合模式(推荐)

### TaskStatus (任务状态)
- `pending`: 等待处理
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败

### GeneratedImage (生成的图片)
| 字段 | 类型 | 说明 |
|------|------|------|
| `url` | string | 图片完整URL |
| `thumbnail_url` | string | 缩略图URL(可选) |
| `width` | integer | 图片宽度(像素) |
| `height` | integer | 图片高度(像素) |
| `format` | string | 图片格式(png/jpg/webp) |
| `size_bytes` | integer | 文件大小(字节,可选) |

### QualityEvaluation (质量评估)
| 字段 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `overall_score` | float | 0.0-1.0 | 总体评分 |
| `clarity` | float | 0.0-1.0 | 清晰度 |
| `color_accuracy` | float | 0.0-1.0 | 色彩准确性 |
| `composition` | float | 0.0-1.0 | 构图质量 |
| `commercial_value` | float | 0.0-1.0 | 商业价值 |
| `issues` | array | - | 问题列表 |
| `suggestions` | array | - | 改进建议 |

---

## ⚙️ 配置说明

### 环境变量

在 `.env` 文件中配置:

```bash
# LLM API Key (必需)
OPENAI_API_KEY=sk-your-key
# 或使用 Gemini
GOOGLE_API_KEY=your-gemini-key
GEMINI_MODEL=gemini-pro

# Stable Diffusion WebUI (可选,如使用本地SD)
SD_WEBUI_URL=http://127.0.0.1:7860

# 质量检查配置
QUALITY_THRESHOLD=0.8
MAX_IMAGE_GENERATION_RETRIES=3

# 服务器配置
HOST=0.0.0.0
PORT=8000
```

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件,填入 API Key
```

### 3. 启动服务
```bash
python main.py
```

### 4. 访问文档
浏览器打开: `http://localhost:8000/docs`

---

## ❓ 常见问题

### Q1: 如何提高生成图片的质量?
**A**: 
- 提高 `quality_threshold` (建议 0.85-0.95)
- 增加 `max_retries` (允许更多次重试)
- 提供详细的 `product_info.description` 和 `key_features`
- 使用 `reference_image_url` 提供参考图

### Q2: 同步和异步接口有什么区别?
**A**:
- **同步接口** (`/generate`): 等待生成完成后返回,适合单次或少量生成
- **异步接口** (`/generate/async`): 立即返回任务ID,需轮询查询结果,适合批量处理

### Q3: 生成的图片存储在哪里?
**A**: 系统使用 **MinIO 对象存储**保存生成的图片。
- **存储位置**: MinIO Bucket (`ecommerce-images`)
- **访问方式**: 通过 HTTP URL 直接访问
- **URL 格式**: `http://localhost:9000/ecommerce-images/{filename}`
- **文件命名**: `{timestamp}_{uuid}.png` (例如: `20260412_185931_a3f2b1c4.png`)
- **查看管理**: 访问 MinIO 控制台 http://localhost:9001 (默认账号: minioadmin/minioadmin)

**配置说明**:
在 `.env` 文件中配置 MinIO:
```bash
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=ecommerce-images
```

### Q4: 任务会保存多久?
**A**: 当前版本任务存储在内存中,服务重启后会丢失。**但生成的图片已持久化到 MinIO**,不会丢失。生产环境建议使用数据库持久化任务状态。

### Q5: 如何调整生成图片的尺寸?
**A**: 通过 `custom_settings` 传递参数,例如:
```json
{
  "custom_settings": {
    "width": 1024,
    "height": 1024,
    "aspect_ratio": "1:1"
  }
}
```

### Q6: 支持哪些图片格式?
**A**: 目前支持 PNG、JPG、WEBP 格式,默认为 PNG。

### Q7: 如何清理旧图片?
**A**: 
1. **通过 MinIO 控制台**: 访问 http://localhost:9001,手动删除
2. **通过 API**: 调用 `ImageService.delete_from_minio(object_name)` 方法
3. **批量清理**: 编写脚本定期清理过期图片

---

## 🗄️ 图片存储架构

### 存储流程
```
SD WebUI 生成 → Base64 Data URL → 上传到 MinIO → 返回 HTTP URL
```

### 优势
- ✅ **持久化存储**: 图片不会因为服务重启而丢失
- ✅ **高性能访问**: MinIO 提供高速对象存储
- ✅ **易于扩展**: 可轻松迁移到云存储 (AWS S3 / 阿里云 OSS)
- ✅ **统一管理**: 所有图片集中在一个 Bucket 中

### 注意事项
- MinIO 服务需要独立运行 (Docker 或本地部署)
- 确保 `.env` 中的 MinIO 配置正确
- 生产环境建议启用 HTTPS 和认证

---

## 📞 技术支持

如有问题,请查看:
- GitHub Issues: [项目仓库](https://github.com/your-repo/ProductPilot)
- 日志文件: 查看控制台输出的详细错误信息

---

**文档版本**: v1.0  
**最后更新**: 2026-04-12
