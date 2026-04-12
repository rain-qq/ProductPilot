# ProductPilot 快速启动指南

## 🚀 5分钟快速上手

### 前置要求

确保已安装:
- ✅ Python 3.9+
- ✅ Node.js 18+ 
- ✅ pnpm (`npm install -g pnpm`)
- ✅ MinIO (用于图片存储)

### 第一步: 克隆项目

```bash
git clone <your-repo-url>
cd ProductPilot
```

### 第二步: 配置环境变量

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑 .env 文件,至少配置以下项:
# - OPENAI_API_KEY 或 GOOGLE_API_KEY
# - MINIO_ENDPOINT=localhost:9000
# - MINIO_ACCESS_KEY=minioadmin
# - MINIO_SECRET_KEY=minioadmin
```

### 第三步: 启动 MinIO (如未运行)

```bash
# 使用 Docker (推荐)
docker run -p 9000:9000 -p 9001:9001 \
  --name minio \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"

# 或直接下载 MinIO 二进制文件运行
```

访问 MinIO 控制台: http://localhost:9001  
默认账号/密码: `minioadmin` / `minioadmin`

### 第四步: 安装依赖

**后端:**
```bash
pip install -r requirements.txt
```

**前端:**
```bash
cd frontend
pnpm install
cd ..
```

### 第五步: 启动服务

**方式1: 分别启动 (推荐用于开发)**

终端1 - 后端:
```bash
python main.py
```

终端2 - 前端:
```bash
# Windows
start-frontend.bat

# Linux/Mac
./start-frontend.sh
```

**方式2: 一键启动**
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

### 第六步: 访问应用

- 🌐 **前端界面**: http://localhost:5173
- 📚 **API文档**: http://localhost:8000/docs
- 💾 **MinIO控制台**: http://localhost:9001

## 🎯 第一次生成图片

1. 打开浏览器访问 http://localhost:5173
2. 在表单中填写:
   - **商品名称**: 例如 "无线蓝牙耳机"
   - **商品描述**: 详细描述产品特点
   - **核心卖点**: 添加几个关键特性
3. 选择生成模式 (推荐 "混合模式")
4. 点击 "开始生成"
5. 等待处理完成 (约30-60秒)
6. 查看生成的图片并下载

## 🔍 故障排查

### 问题1: 前端无法连接后端

**症状**: 提交表单后显示网络错误

**解决**:
1. 确认后端服务正在运行 (`python main.py`)
2. 检查 `frontend/.env` 中的 `VITE_API_BASE_URL=http://localhost:8000`
3. 重启前端开发服务器

### 问题2: MinIO 连接失败

**症状**: 生成图片时报错 "MinIO connection failed"

**解决**:
1. 确认 MinIO 服务正在运行
2. 检查 `.env` 中的 MinIO 配置是否正确
3. 访问 http://localhost:9001 测试 MinIO 控制台
4. 确保 bucket `ecommerce-images` 已创建 (首次会自动创建)

### 问题3: API Key 未配置

**症状**: 报错 "API key not found" 或 "Authentication failed"

**解决**:
1. 检查 `.env` 文件中是否配置了 `OPENAI_API_KEY` 或 `GOOGLE_API_KEY`
2. 确保 API Key 有效且有足够余额
3. 重启后端服务使配置生效

### 问题4: 端口被占用

**症状**: 启动时报错 "Address already in use"

**解决**:
```bash
# Windows - 查找并关闭占用端口的进程
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

或修改端口:
- 后端: 编辑 `main.py` 中的 `port` 参数
- 前端: 编辑 `frontend/vite.config.ts` 添加 `server: { port: 5174 }`

### 问题5: pnpm 未安装

**症状**: 命令找不到 pnpm

**解决**:
```bash
npm install -g pnpm
```

## 📖 更多资源

- 📘 [完整API文档](./API_DOCUMENTATION.md)
- 🏗️ [架构说明](./ARCHITECTURE.md)
- 🎨 [前端开发指南](./frontend/README.md)
- 💾 [MinIO使用指南](./MINIO_GUIDE.md)

## 💡 小贴士

1. **首次运行较慢**: 首次生成图片需要加载模型,请耐心等待
2. **调整质量阈值**: 如果生成时间过长,可降低 `QUALITY_THRESHOLD` (建议 0.75-0.85)
3. **批量生成**: 使用异步接口可同时处理多个任务
4. **查看日志**: 后端日志会输出详细的处理步骤和错误信息
5. **清除缓存**: 如遇奇怪问题,尝试删除 `frontend/node_modules` 后重新 `pnpm install`

## 🆘 获取帮助

- 查看 [常见问题](./README.md#-常见问题)
- 提交 [GitHub Issue](https://github.com/your-repo/ProductPilot/issues)
- 查看后端控制台日志了解详细错误

---

祝你使用愉快! 🎉