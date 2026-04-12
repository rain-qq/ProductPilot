# 📖 ProductPilot 使用指南

## 🚀 快速开始（3步）

### Windows 用户

**方式A：双击启动（最简单）**
```
双击 start.bat 文件
```

**方式B：命令行启动**
```bash
cd d:\workspace\ProductPilot
.venv\Scripts\activate
python test_quick.py
```

---

### Mac/Linux 用户

```bash
cd /path/to/ProductPilot
chmod +x start.sh
./start.sh
```

或手动执行：
```bash
source .venv/bin/activate
python test_quick.py
```

---

## 📋 常用命令

### 1️⃣ 激活虚拟环境

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 2️⃣ 测试配置
```bash
python test_quick.py
```

### 3️⃣ 运行示例

**测试 Gemini API:**
```bash
python examples/gemini_example.py
```

**测试完整流程:**
```bash
python examples/basic_usage.py
```

### 4️⃣ 启动 API 服务器
```bash
python main.py
```
访问: http://localhost:8000/docs

---

## 🎯 推荐执行顺序

### 第一次运行

1. **激活虚拟环境**
   ```bash
   .venv\Scripts\activate  # Windows
   ```

2. **测试配置**
   ```bash
   python test_quick.py
   ```
   应该看到所有测试通过 ✅

3. **测试 Gemini**
   ```bash
   python examples/gemini_example.py
   ```
   应该看到 Gemini 的回复

4. **测试 Agent 协作**
   ```bash
   python examples/basic_usage.py
   ```

5. **启动完整服务**
   ```bash
   python main.py
   ```

---

## 🐛 故障排除

### 问题1: "ModuleNotFoundError"
**原因**: 虚拟环境未激活或依赖未安装

**解决**:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### 问题2: "Gemini LLM not initialized"
**原因**: `.env` 文件缺失或 API Key 错误

**解决**:
1. 检查 `.env` 文件存在
2. 确认 `GOOGLE_API_KEY` 已填写
3. 运行 `python test_quick.py` 验证

### 问题3: 依赖安装失败
**原因**: 编码问题或网络问题

**解决**:
```bash
# 升级 pip
python -m pip install --upgrade pip

# 重新安装
pip install -r requirements.txt --no-cache-dir
```

### 问题4: 虚拟环境问题
**原因**: 虚拟环境损坏

**解决**:
```bash
# 删除旧环境
rm -rf .venv          # Mac/Linux
rmdir /s /q .venv     # Windows

# 重新创建
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

---

## 📊 功能检查清单

运行以下命令检查所有功能：

```bash
python test_quick.py
```

应该看到：
```
✅ 配置加载成功
✅ LLM初始化成功
✅ Agents导入成功
✅ Workflow导入成功

总计: 4/4 测试通过
🎉 所有测试通过！项目可以正常运行！
```

---

## 💡 提示

1. **始终使用虚拟环境**
   - 避免与系统Python冲突
   - 依赖隔离，更干净

2. **先测试再运行**
   - 每次修改后运行 `test_quick.py`
   - 确保配置正确

3. **查看日志**
   - 设置 `LOG_LEVEL=DEBUG` 在 `.env` 中
   - 查看详细错误信息

4. **文档齐全**
   - README.md - 完整文档
   - RUN_GUIDE.md - 运行指南
   - API_CONFIG.md - API配置

---

## 🎉 成功标志

当你看到以下输出时，说明一切正常：

```
🧪 ProductPilot 项目测试

============================================================
测试配置加载
============================================================
✅ 配置加载成功
  - Gemini API Key: AIzaSyD7phu...
  - 选定模型: gemini-pro
  - 应用环境: development

============================================================
测试 LLM 初始化
============================================================
✅ LLM服务初始化成功
  - 可用提供商: ['gemini']
  - Gemini LLM: ✅ 可用

============================================================
测试 Agents 导入
============================================================
✅ 所有 Agents 导入成功

============================================================
测试 Workflow 导入
============================================================
✅ 工作流导入成功

============================================================
测试总结
============================================================
✅ 通过 - 配置加载
✅ 通过 - LLM初始化
✅ 通过 - Agents导入
✅ 通过 - Workflow导入

总计: 4/4 测试通过
🎉 所有测试通过！项目可以正常运行！
```

---

**准备好了吗？** 运行 `start.bat` (Windows) 或 `./start.sh` (Mac/Linux) 开始吧！🚀
