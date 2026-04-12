# ProductPilot 架构详解 🏗️

## 整体架构

ProductPilot采用创新的 **CrewAI + LangGraph 混合架构**，结合了Agent的灵活性和Workflow的可控性。

```
┌────────────────────────────────────────────────────┐
│                  API Layer (FastAPI)                │
│  /generate  /generate/async  /task/{id}  /health   │
└──────────────────┬─────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────┐
│              CrewAI Agent Team Layer                │
│                                                     │
│  ┌──────────────┐    ┌──────────────────┐          │
│  │ Analyst      │───▶│ Prompt Engineer  │          │
│  │ (产品分析)    │    │ (提示词优化)      │          │
│  └──────────────┘    └────────┬─────────┘          │
│                               │                     │
│                    ┌──────────▼─────────┐          │
│                    │ Image Creator      │          │
│                    │ (调用工作流)         │          │
│                    └──────────┬─────────┘          │
│                               │                     │
│                    ┌──────────▼─────────┐          │
│                    │ Quality Reviewer   │          │
│                    │ (质量审核)          │          │
│                    └────────────────────┘          │
└───────────────────┼───────────────────────────────┘
                    │ 调用
┌───────────────────▼───────────────────────────────┐
│           LangGraph Workflow Engine                │
│                                                    │
│  State: ImageGenerationState                       │
│                                                    │
│  ┌──────────┐                                     │
│  │preprocess│ (参考图预处理)                        │
│  └────┬─────┘                                     │
│       │                                            │
│  ┌────▼──────┐                                    │
│  │ generate  │ (图片生成 - SD/DALL-E)             │
│  └────┬──────┘                                    │
│       │                                            │
│  ┌────▼────────┐                                  │
│  │quality_check│ (自动质量评估)                     │
│  └────┬────────┘                                  │
│       │                                            │
│  ┌────▼────────┐                                  │
│  │post_process │ (增强、选择最佳)                   │
│  └─────────────┘                                  │
│                                                    │
│  支持循环: quality_check → regenerate → generate  │
└───────────────────┼───────────────────────────────┘
                    │
┌───────────────────▼───────────────────────────────┐
│                 Service Layer                      │
│                                                    │
│  ┌──────────────────┐   ┌──────────────┐          │
│  │ ImageService     │   │ LLMService   │          │
│  │ - 图片生成        │   │ - LLM调用    │          │
│  │ - 预处理          │   │ - Embedding  │          │
│  │ - 后处理          │   └──────────────┘          │
│  └──────────────────┘                              │
└────────────────────────────────────────────────────┘
```

## 核心组件

### 1. Agents层 (`agents/`)

#### ProductAnalystAgent (产品分析师)
- **职责**: 分析参考产品的视觉特征
- **能力**:
  - 提取配色方案
  - 识别构图类型
  - 分析光影风格
  - 挖掘营销卖点
- **工具**: `analyze_reference_image()`

#### PromptEngineerAgent (提示词工程师)
- **职责**: 将产品描述转换为专业AI绘画提示词
- **能力**:
  - 生成positive prompt
  - 生成negative prompt
  - 推荐采样参数
  - 融合参考产品元素
- **工具**: `optimize_prompt()`

#### ImageCreatorAgent (图片创作师)
- **职责**: 调用LangGraph工作流生成图片
- **能力**:
  - 支持text2img模式
  - 支持img2img模式
  - 支持mixed模式 (ControlNet)
  - 自动质量迭代
- **工具**: `generate_with_workflow()`
- **内部**: 使用 `ImageGenerationWorkflow`

#### QualityReviewerAgent (质量审核员)
- **职责**: 评估生成图片的质量
- **评分维度**:
  - 清晰度 (clarity)
  - 色彩准确性 (color_accuracy)
  - 构图 (composition)
  - 光影效果 (lighting)
  - 商业价值 (commercial_value)
- **工具**: `evaluate_image_quality()`

### 2. Workflow层 (`workflows/`)

#### ImageGenerationState
工作流状态定义：
```python
{
    "prompt": str,                    # 输入提示词
    "reference_image": str,           # 参考图片(可选)
    "mode": "text2img" | "img2img" | "mixed",
    "generated_images": List[str],    # 生成的图片
    "quality_scores": List[float],    # 质量评分
    "selected_image": str,            # 选中的最佳图片
    "iteration_count": int,           # 迭代次数
    ...
}
```

#### 工作流节点

1. **preprocess_node**: 预处理参考图片
   - 下载图片
   - 去除背景 (rembg)
   - 调整尺寸
   - 颜色校正

2. **generate_node**: 生成图片
   - 根据mode选择生成方式
   - 调用SD WebUI API
   - 返回多张候选图片

3. **quality_check_node**: 质量检查
   - 对每张图片评分
   - 调用QualityReviewerAgent
   - 记录评分详情

4. **decide_next_step**: 决策函数
   - 质量达标 → post_process
   - 未达标且未超限 → regenerate
   - 超限或错误 → accept/error

5. **regenerate_node**: 重新生成
   - 调整prompt (增加细节描述)
   - 调整参数
   - 回到generate_node

6. **post_process_node**: 后处理
   - 选择最佳图片
   - 应用增强 (超分、调色)
   - 返回最终结果

7. **error_handler_node**: 错误处理
   - 记录错误信息
   - 返回失败状态

### 3. Services层 (`services/`)

#### ImageService
封装所有图片处理逻辑：
- `text_to_image()`: SD txt2img API
- `image_to_image()`: SD img2img API
- `controlnet_generate()`: ControlNet生成
- `preprocess()`: 图片预处理
- `enhance()`: 图片增强
- `extract_features()`: 特征提取

#### LLMService
封装LLM调用：
- `get_llm()`: 获取LLM实例
- `get_embeddings()`: 获取Embedding模型

### 4. API层 (`api/`)

#### RESTful接口

**POST /api/v1/generate**
- 同步生成图片
- 适用于单次请求

**POST /api/v1/generate/async**
- 异步生成图片
- 返回task_id
- 配合 GET /api/v1/task/{task_id} 查询进度

**GET /api/v1/task/{task_id}**
- 查询任务状态
- 返回进度百分比

**GET /api/v1/health**
- 健康检查

## 数据流

### 完整生成流程

```
用户请求
   ↓
[API Router] 接收请求
   ↓
[Main Process] 解析参数
   ↓
[CrewAI] 启动Agent团队
   ↓
1. ProductAnalyst (如有参考图)
   └─> 分析视觉特征
   ↓
2. PromptEngineer
   └─> 生成优化prompt
   ↓
3. ImageCreator
   └─> [LangGraph Workflow]
         ├─> preprocess
         ├─> generate
         ├─> quality_check
         ├─> [循环: regenerate if needed]
         └─> post_process
   ↓
4. QualityReviewer
   └─> 最终评估
   ↓
返回结果给用户
```

## 扩展点

### 1. 添加新Agent
在 `agents/` 目录创建新文件，继承Agent类

### 2. 自定义工作流节点
在 `ImageGenerationWorkflow._build_workflow()` 中添加新节点

### 3. 支持新的图片生成模型
在 `ImageService` 中添加新方法，如 `dalle_generate()`

### 4. 添加中间件
在 `main.py` 中使用 `app.add_middleware()`

## 性能考虑

### 优化建议

1. **批量处理**: 使用异步接口 + 任务队列
2. **缓存策略**: 缓存常用prompt和配置
3. **连接池**: SD API使用连接池
4. **并发控制**: 限制同时生成的图片数
5. **CDN加速**: 图片存储使用CDN

### 资源需求

| 组件 | CPU | GPU | 内存 |
|------|-----|-----|------|
| CrewAI + LangGraph | 1核 | 无 | 1GB |
| SD WebUI (本地) | 4核 | 4GB+ | 8GB |
| DALL-E API | 无 | 无 | 无 |

## 安全考虑

1. **API密钥**: 使用环境变量，不要硬编码
2. **输入验证**: Pydantic模型验证
3. **速率限制**: API添加限流中间件
4. **图片审核**: 添加内容安全检查

## 监控与日志

- 使用 `loguru` 记录详细日志
- 集成 LangSmith 追踪Agent执行
- Prometheus + Grafana 监控系统指标

---

**理解架构后，你可以:**
- ✅ 快速定位代码位置
- ✅ 添加新功能
- ✅ 调试问题
- ✅ 优化性能
