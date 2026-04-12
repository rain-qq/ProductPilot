# ProductPilot - MinIO 图片存储使用指南

## 📋 概述

ProductPilot 现已集成 **MinIO 对象存储**,所有生成的电商图片都会自动上传并持久化存储,确保数据安全和高效访问。

---

## ✨ 主要特性

- ✅ **自动上传**: 工作流完成后自动上传图片到 MinIO
- ✅ **持久化存储**: 图片不会因服务重启而丢失
- ✅ **唯一命名**: 使用时间戳 + UUID 确保文件名唯一
- ✅ **批量支持**: 支持单张和批量上传
- ✅ **容错机制**: 上传失败时自动降级为 base64 Data URL
- ✅ **易于管理**: 通过 MinIO 控制台统一管理所有图片

---

## 🔧 配置说明

### 1. 环境变量配置

在 `.env` 文件中配置 MinIO 连接信息:

```bash
# MinIO Storage Configuration
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=ecommerce-images
```

### 2. MinIO 服务启动

确保 Docker 中的 MinIO 服务正在运行:

```bash
# 如果还未启动 MinIO,使用以下命令
docker run -d \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio \
  -v /path/to/data:/data \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

**端口说明:**
- `9000`: API 访问端口
- `9001`: Web 控制台端口

---

## 🚀 使用方法

### 自动上传 (推荐)

无需额外配置,系统会自动将生成的图片上传到 MinIO:

```python
from workflows.image_generation import ImageGenerationWorkflow

workflow = ImageGenerationWorkflow()
result = workflow.run(
    prompt="professional product photography of wireless earbuds",
    mode="text2img"
)

# 返回的图片 URL 已经是 MinIO 地址
print(result["selected_image"])  
# 输出: http://localhost:9000/ecommerce-images/20260412_190326_a3f2b1c4.png
```

### 手动上传

如果需要手动上传图片:

```python
from services.image_service import ImageService

service = ImageService()

# 单张上传
image_url = service.upload_to_minio(base64_data_url)
print(f"Uploaded: {image_url}")

# 批量上传
images = [base64_url_1, base64_url_2, base64_url_3]
urls = service.upload_multiple_images(images)
for url in urls:
    print(url)
```

### 删除图片

```python
from services.image_service import ImageService

service = ImageService()

# 删除指定文件
success = service.delete_from_minio("20260412_190326_a3f2b1c4.png")
if success:
    print("删除成功")
```

---

## 📊 文件命名规则

生成的图片文件名格式:

```
{YYYYMMDD_HHMMSS}_{UUID_SHORT}.{EXT}
```

**示例:**
- `20260412_190326_a3f2b1c4.png`
- `20260412_185931_d7e8f9a0.jpg`

**优势:**
- 按时间排序,便于查找
- UUID 保证唯一性,避免冲突
- 清晰的扩展名标识格式

---

## 🌐 访问图片

### 直接访问

生成的图片可通过 HTTP URL 直接访问:

```
http://localhost:9000/ecommerce-images/{filename}
```

**示例:**
```
http://localhost:9000/ecommerce-images/20260412_190326_a3f2b1c4.png
```

### 在浏览器中查看

直接在浏览器地址栏输入上述 URL 即可查看图片。

### 在 HTML 中使用

```html
<img src="http://localhost:9000/ecommerce-images/20260412_190326_a3f2b1c4.png" 
     alt="Generated Product Image" />
```

---

## 🎛️ MinIO 控制台管理

### 访问控制台

打开浏览器访问: **http://localhost:9001**

**默认登录凭据:**
- 用户名: `minioadmin`
- 密码: `minioadmin`

### 管理功能

在控制台中可以:
1. **浏览文件**: 查看所有上传的图片
2. **预览图片**: 点击文件即可预览
3. **下载文件**: 右键下载或拖拽到本地
4. **删除文件**: 选择文件后点击删除
5. **创建文件夹**: 组织图片分类
6. **设置权限**: 配置公开/私有访问
7. **查看统计**: Bucket 使用情况、流量等

---

## 🧪 测试验证

运行测试脚本验证 MinIO 集成:

```bash
python test_minio.py
```

**预期输出:**
```
✅ MinIO 客户端初始化成功
✅ Bucket 'ecommerce-images' 已存在
📤 正在上传测试图片...
✅ 上传成功!
   URL: http://localhost:9000/ecommerce-images/test_image.png
```

---

## ⚙️ 高级配置

### 自定义 Bucket 名称

修改 `.env`:
```bash
MINIO_BUCKET_NAME=my-custom-bucket
```

### 启用 HTTPS (生产环境)

1. 配置 SSL 证书
2. 修改 `image_service.py`:
```python
self.minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=True  # 启用 HTTPS
)
```

### 迁移到云存储

只需修改配置即可切换到 AWS S3 / 阿里云 OSS:

```bash
# AWS S3 示例
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=your-aws-access-key
MINIO_SECRET_KEY=your-aws-secret-key
MINIO_BUCKET_NAME=productpilot-images
```

---

## ❓ 常见问题

### Q1: 提示 "MinIO library not installed"

**解决方案:**
```bash
pip install minio
```

### Q2: 连接 MinIO 失败

**检查清单:**
1. Docker 中的 MinIO 容器是否运行: `docker ps | grep minio`
2. 端口 9000 是否可访问: `telnet localhost 9000`
3. `.env` 配置是否正确
4. 防火墙是否阻止连接

### Q3: 图片上传后无法访问

**可能原因:**
1. Bucket 权限设置为私有
2. MinIO 服务未正常运行
3. URL 格式错误

**解决方案:**
- 在 MinIO 控制台中检查 Bucket 策略
- 确保 Bucket 为公开读取或配置正确的访问策略

### Q4: 如何清理旧图片?

**方法 1: MinIO 控制台**
- 登录 http://localhost:9001
- 选择文件批量删除

**方法 2: Python 脚本**
```python
from services.image_service import ImageService

service = ImageService()

# 删除指定文件
service.delete_from_minio("old_image.png")
```

**方法 3: 定期清理任务**
编写定时任务,删除超过 N 天的图片。

### Q5: 存储空间占用过大怎么办?

**优化建议:**
1. 定期清理无用图片
2. 压缩图片后再上传
3. 使用图片缩略图
4. 迁移到云存储并启用生命周期策略

---

## 📈 性能优化

### 1. 异步上传

对于大量图片,可以使用异步上传提升性能:

```python
import asyncio
from services.image_service import ImageService

async def upload_async(service, images):
    tasks = [service.upload_to_minio(img) for img in images]
    return await asyncio.gather(*tasks)
```

### 2. 批量操作

使用 `upload_multiple_images()` 而非循环调用单张上传。

### 3. CDN 加速

在生产环境中,可以在 MinIO 前配置 CDN (如 CloudFlare) 加速图片访问。

---

## 🔒 安全建议

### 生产环境配置

1. **修改默认密码:**
```bash
MINIO_ACCESS_KEY=your-strong-access-key
MINIO_SECRET_KEY=your-strong-secret-key
```

2. **启用 HTTPS:**
- 配置 SSL 证书
- 使用反向代理 (Nginx)

3. **限制访问权限:**
- 配置 CORS 策略
- 设置 IP 白名单
- 使用预签名 URL

4. **备份数据:**
- 定期备份 MinIO 数据目录
- 配置跨区域复制

---

## 📚 相关资源

- [MinIO 官方文档](https://docs.min.io/)
- [MinIO Python SDK](https://docs.min.io/docs/python-client-quickstart-guide.html)
- [ProductPilot API 文档](./API_DOCUMENTATION.md)

---

**最后更新:** 2026-04-12