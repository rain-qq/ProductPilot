# ⚠️ 重要：依赖安装指南

## 📋 当前状态

项目代码已完整生成，但**依赖包正在安装中**。

### ✅ 已完成
- [x] 虚拟环境已创建 (`.venv`)
- [x] pip已升级到最新版本
- [x] 所有依赖版本冲突已修复
- [x] requirements.txt已优化

### ⏳ 正在进行
- [ ] 安装Python依赖包（约50个包，500MB）

---

## 🔧 安装方法

### 方法一：继续等待当前安装完成

在终端中查看输出，当看到：
```
Successfully installed crewai-0.28.8 langgraph-0.0.xx ...
```
说明安装成功！

### 方法二：使用国内镜像源（更快）

如果当前安装很慢或卡住，可以：

**Windows:**
```bash
# 激活虚拟环境
.venv\Scripts\activate

# 使用清华镜像源安装
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

**Mac/Linux:**
```bash
source .venv/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

---

## ✅ 验证安装

安装完成后，运行测试：

```bash
# 激活虚拟环境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 运行测试
python test_minimal.py
```

应该看到：
```
✅ Python版本: 3.11.9
✅ .env 文件存在
✅ Gemini API Key: AIzaSyD7phu...
✅ Pydantic: 2.6.4
✅ Requests: 2.31.0
✅ CrewAI: 0.28.8
✅ LangGraph: 已安装
```

---

## 🐛 常见问题

### Q1: 安装一直卡住不动
**解决**: 使用国内镜像源
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### Q2: 某些包下载失败
**解决**: 逐个安装
```bash
pip install crewai langgraph langchain
pip install langchain-openai langchain-google-genai
# ... 继续安装其他包
```

### Q3: 虚拟环境问题
**解决**: 重建虚拟环境
```bash
# 删除旧环境
rm -rf .venv  # Mac/Linux
rmdir /s /q .venv  # Windows

# 重新创建
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 🚀 安装完成后的下一步

1. **测试配置**
   ```bash
   python test_quick.py
   ```

2. **运行示例**
   ```bash
   python examples/gemini_example.py
   ```

3. **启动服务**
   ```bash
   python main.py
   ```

---

## 📞 需要帮助？

如果安装过程中遇到问题：
1. 检查网络连接
2. 使用国内镜像源
3. 查看终端的错误信息
4. 截图错误信息寻求帮助

---

**预计时间**: 首次安装需要 5-15 分钟（取决于网络速度）
