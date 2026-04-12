# ProductPilot Frontend

ProductPilot 的现代化 React 前端界面,用于可视化交互和电商图片生成。

## 🚀 技术栈

- **框架**: React 19 + TypeScript
- **构建工具**: Vite 8
- **样式**: TailwindCSS 4
- **HTTP 客户端**: Axios
- **图标**: Lucide React
- **工具库**: clsx, tailwind-merge

## 📦 安装

```bash
cd frontend
pnpm install
```

## 🏃 运行开发服务器

```bash
pnpm dev
```

访问 http://localhost:5173

## 🏗️ 构建生产版本

```bash
pnpm build
```

## 📁 项目结构

```
frontend/
├── src/
│   ├── components/        # React 组件
│   │   ├── Layout.tsx    # 布局组件(Header, Footer)
│   │   ├── GenerationForm.tsx  # 图片生成表单
│   │   ├── ImageGallery.tsx    # 图片展示画廊
│   │   └── TaskProgress.tsx    # 任务进度显示
│   ├── pages/            # 页面组件
│   │   └── Home.tsx      # 主页
│   ├── services/         # API 服务层
│   │   └── imageService.ts  # 图片生成 API
│   ├── lib/              # 工具函数
│   │   ├── api.ts        # Axios 配置
│   │   └── utils.ts      # 通用工具
│   ├── App.tsx           # 应用根组件
│   ├── main.tsx          # 入口文件
│   └── index.css         # 全局样式
├── .env                  # 环境变量
├── vite.config.ts        # Vite 配置
└── tsconfig.app.json     # TypeScript 配置
```

## 🎨 设计特点

- **现代深色主题**: 采用 slate/violet/fuchsia 配色方案
- **流畅动画**: 平滑的过渡效果和加载动画
- **响应式布局**: 适配桌面和移动设备
- **直观交互**: 清晰的表单流程和实时进度反馈
- **无 AI 味**: 简洁专业的界面设计,避免过度装饰

## 🔧 配置

### 环境变量

在 `.env` 文件中配置:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

### API 端点

前端会调用以下后端接口:

- `POST /generate/async` - 异步生成图片
- `GET /task/{task_id}` - 查询任务状态
- `GET /health` - 健康检查

## 📝 功能特性

1. **多种生成模式**: 支持文生图、图生图、混合模式
2. **实时进度追踪**: 6 个步骤的可视化进度条
3. **图片质量评分**: 显示清晰度和商业价值评分
4. **批量生成**: 一次生成多张图片并对比选择
5. **一键下载**: 快速下载生成的图片
6. **错误处理**: 友好的错误提示和重试机制

## 🤝 开发规范

- 使用 TypeScript 严格模式
- 组件采用函数式编程 + Hooks
- 样式使用 TailwindCSS 原子类
- 遵循 ESLint 代码规范

## 📄 License

MIT
