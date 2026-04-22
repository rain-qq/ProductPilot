# 故障排除指南 (Troubleshooting)

## 常见问题及解决方案

### 1. Windows 环境下日志编码错误

**问题描述:**
运行程序时出现以下错误:
```
UnicodeEncodeError: 'gbk' codec can't encode character '\U0001f4cb' in position 100: illegal multibyte sequence
```

**原因:**
- Windows 控制台默认使用 GBK 编码
- 日志消息中包含 Unicode emoji 字符(如 📋、✅、👥、🚀)
- GBK 编码无法处理这些字符

**解决方案:**

已在以下文件中完成修复:

1. **main.py** - 设置 UTF-8 环境变量
   ```python
   if os.name == 'nt':  # Windows环境
       os.environ['PYTHONIOENCODING'] = 'utf-8'
       os.system('chcp 65001 >nul 2>&1')  # 设置控制台代码页为UTF-8
   ```
   - **注意**: Loguru 的 `add()` 方法不支持 `encoding` 参数
   - 通过环境变量 `PYTHONIOENCODING` 让 Python 使用 UTF-8 编码

2. **api/routes.py** - 移除 emoji 字符
   - 将所有 emoji 替换为 ASCII 文本标记
   - 示例:`[TASK]`、`[OK]`、`[TEAM]`、`[START]`

3. **agents/image_creator.py** - 移除 emoji 字符
   - 统一使用 `[START]`、`[OK]`、`[WARN]`、`[ERROR]`、`[SUCCESS]` 标记

4. **test_minimal.py** - 移除 emoji 字符
   - 使用 `[OK]` 和 `[FAIL]` 替代 ✅ 和 ❌

**代码规范:**
为避免未来出现类似问题,请遵循以下规范:
- 禁止在日志中使用 emoji 字符
- 使用 ASCII 兼容的文本标记,如:`[INFO]`、`[WARN]`、`[ERROR]`
- Windows 环境下在应用启动时设置 `PYTHONIOENCODING=utf-8`
- 所有 logger 调用确保只包含 ASCII 字符或正确配置 UTF-8 编码

**验证方法:**
```bash
python test_logging.py
```
如果看到 `[OK]` 且没有报错,说明日志配置正常。

---

### 2. requirements.txt 文件编码错误

**问题描述:**
执行 `pip install -r requirements.txt` 时出现:
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0xXX in position XX: illegal multibyte sequence
```

**解决方案:**
- 确保 `requirements.txt` 文件以 UTF-8 无 BOM 格式保存
- 在 VSCode 中:右下角点击编码 -> "通过编码保存" -> 选择 "UTF-8"
- 或使用记事本打开后另存为 UTF-8 格式

---

### 3. MinIO 连接失败

**问题描述:**
```
ConnectionRefusedError: [WinError 10061] 由于目标计算机积极拒绝，无法连接
```

**解决方案:**
1. 确认 MinIO 服务已启动
2. 检查 `.env` 中的配置:
   ```
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   ```
3. 访问 http://localhost:9000 确认 MinIO Console 可访问
4. 首次运行需创建 bucket: `ecommerce-images`

---

### 4. Gemini API 调用超时

**问题描述:**
```
TimeoutError: Request timed out after 120 seconds
```

**解决方案:**
1. 检查网络连接是否稳定
2. 确认 `GOOGLE_API_KEY` 配置正确
3. 考虑增加超时时间(修改 `services/image_service.py`)
4. 检查 Gemini API 配额是否用完

---

### 5. CrewAI Agent 初始化失败

**问题描述:**
```
ValueError: LLM provider not configured
```

**解决方案:**
1. 确认 `.env` 文件中配置了有效的 API Key:
   ```
   OPENAI_API_KEY=your-key-here
   GOOGLE_API_KEY=your-key-here
   ```
2. 重启应用使配置生效
3. 运行 `python test_minimal.py` 验证配置

---

## 调试技巧

### 启用详细日志
修改 `.env`:
```
LOG_LEVEL=DEBUG
```

### 测试单个组件
```bash
# 测试基础配置
python test_minimal.py

# 测试 LLM 配置
python test_llm_config.py

# 测试 MinIO 连接
python test_minio.py

# 快速功能测试
python test_quick.py
```

### 查看实时日志
```bash
# Windows PowerShell
Get-Content -Path logs/app.log -Wait -Tail 50

# Linux/Mac
tail -f logs/app.log
```

---

## 获取帮助

如果以上方法无法解决问题:

1. 检查项目 README.md 和 INSTALL.md
2. 查看 GitHub Issues 是否有类似问题
3. 提供以下信息以便排查:
   - 操作系统版本
   - Python 版本 (`python --version`)
   - 完整的错误日志
   - `.env` 配置(隐藏敏感信息)
