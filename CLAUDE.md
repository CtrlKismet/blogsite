# CLAUDE.md — CtrlKismet's Blog

> 供 LLM 快速了解本项目的上下文文档。

## 项目概述

个人博客系统，采用前后端分离架构。前端为 Vue 3 SPA，后端为 Python FastAPI 只读 API，配合文件监听服务（watcher）自动同步 Markdown 文章到 SQLite 数据库，评论系统使用 Artalk，反向代理使用 Traefik v3。

## 仓库结构

```
blogsite/
├── frontend/          # Vue 3 前端 SPA
│   ├── src/
│   │   ├── api/       # Axios API 封装 (articles.ts, tags.ts)
│   │   ├── components/
│   │   │   ├── admin/     # 管理后台组件
│   │   │   ├── archive/   # 归档页组件
│   │   │   ├── article/   # 文章相关组件
│   │   │   ├── common/    # 通用组件
│   │   │   └── layout/    # 布局组件
│   │   ├── router/    # Vue Router 路由配置
│   │   ├── stores/    # Pinia 状态管理 (site.ts)
│   │   ├── styles/    # 全局样式
│   │   │   ├── variables.css   # CSS 变量/主题
│   │   │   ├── global.css      # 全局基础样式
│   │   │   ├── components.css  # 组件样式
│   │   │   ├── layout.css      # 布局样式
│   │   │   └── responsive.css  # 响应式样式
│   │   ├── types/     # TypeScript 类型定义
│   │   ├── utils/     # 工具函数
│   │   └── views/     # 页面视图
│   │       ├── HomeView.vue        # 首页
│   │       ├── ArchiveView.vue     # 归档页
│   │       ├── AboutView.vue       # 关于页
│   │       └── BlogDetailView.vue  # 文章详情页
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── backend/           # FastAPI 后端 API
│   ├── app/
│   │   ├── main.py        # FastAPI 入口 + CORS + 异常处理
│   │   ├── config.py      # pydantic-settings 配置
│   │   ├── database.py    # SQLAlchemy async 数据库设置
│   │   ├── models.py      # ORM 模型 (Article, Tag, ArticleTag)
│   │   ├── schemas.py     # Pydantic 请求/响应 schema
│   │   ├── dependencies.py
│   │   ├── routers/       # API 路由
│   │   │   ├── articles.py
│   │   │   ├── tags.py
│   │   │   ├── images.py
│   │   │   └── site.py
│   │   ├── services/      # 业务逻辑
│   │   └── utils/         # 工具函数
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
├── watcher/           # 文件监听 + AI 标签服务
│   ├── app/
│   │   ├── main.py        # 启动入口：全量同步 + watchdog 监听
│   │   ├── watcher.py     # watchdog 事件处理
│   │   ├── sync.py        # 文章同步逻辑
│   │   ├── ai_service.py  # AI 摘要/标签生成 (OpenAI API)
│   │   ├── config.py      # 配置
│   │   └── database.py    # 同步 SQLAlchemy 会话
│   ├── Dockerfile
│   └── pyproject.toml
├── docker-compose.yml # 容器编排
├── .env.example       # 环境变量模板
└── .gitignore
```

## 技术栈

### 前端
- **框架**: Vue 3 (Composition API) + TypeScript
- **构建**: Vite 8
- **路由**: Vue Router 4
- **状态管理**: Pinia 3
- **HTTP**: Axios
- **Markdown 渲染**: markdown-it + KaTeX (数学公式)
- **评论**: Artalk
- **图标**: Font Awesome 7

### 后端
- **框架**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy 2 (async) + aiosqlite
- **数据库**: SQLite (WAL 模式)
- **校验**: Pydantic 2 + pydantic-settings
- **包管理**: uv
- **Lint**: Ruff

### Watcher 服务
- **文件监听**: watchdog
- **AI 服务**: OpenAI API (可配置 base_url/model)
- **数据库**: SQLAlchemy (同步)

### 部署
- **容器化**: Docker + Docker Compose
- **VPS**: `docker-compose.yml` — api + artalk（只读服务）
- **NUC**: `watcher/docker-compose.yml` — watcher（文件监听 + AI）
- **数据同步**: NUC → VPS 单向 rsync（DB + posts）
- **反向代理**: Traefik v3 (HTTPS + Docker labels 路由)
- **前端部署**: 多阶段 Docker 构建 (node:22-alpine → nginx:alpine) → Traefik 反代

## 数据模型

- **Article**: id, title, summary, file_path, header_image, status, created_at, published_at, updated_at
- **Tag**: id, name (unique)
- **ArticleTag**: article_id, tag_id (多对多关联)

## API 路由

后端 API 前缀为 `/api`，主要路由模块：
- `articles` — 文章 CRUD、分页、详情
- `tags` — 标签列表、按标签筛选
- `images` — 图片服务
- `site` — 站点配置信息

## 开发命令

### 前端
```bash
cd frontend
npm install          # 安装依赖
npm run dev          # 启动开发服务器 (localhost:5173)
npm run build        # 生产构建 → dist/
```

### 后端 (本地)
```bash
cd backend
uv sync              # 安装依赖
uv run uvicorn app.main:app --reload  # 启动开发服务器
uv run pytest        # 运行测试
uv run ruff check .  # Lint 检查
```

### Docker
```bash
# .env 使用绝对路径，docker compose 自动读取，无需 source
# 启动所有服务（前端在 Docker 内自动构建，无需手动 npm build）
sudo docker compose up -d --build

# NUC: 启动 watcher
cd watcher && sudo docker compose up -d --build

sudo docker compose logs -f         # 查看日志
```

## 环境变量

参考 `.env.example`：
| 变量 | 说明 |
|------|------|
| `DB_DIR` | SQLite 数据库目录 (宿主机路径) |
| `POSTS_DIR` | Markdown 文章目录 (宿主机路径) |
| `AI_BASE_URL` | AI API 地址 (默认 OpenAI) |
| `AI_API_KEY` | AI API 密钥 |
| `AI_MODEL` | AI 模型名称 (默认 gpt-4o-mini) |

## 开发注意事项

- 前端开发时 Vite 会将 `/api` 代理到 `http://localhost:8000`
- 生产环境前端打包在 nginx 容器中，由 Traefik 反代提供服务
- 数据库为 SQLite，使用 WAL 模式，watcher 和 backend 共享同一个 db 文件
- watcher 服务在启动时执行全量同步，之后通过 watchdog 监听文件变更
- 新文章创建后 watcher 会调用 AI 生成摘要和标签
- 提交规范遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/)
