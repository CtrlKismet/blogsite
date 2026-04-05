# BlogSite — 个人博客系统

> 从阿里云迁移到 NUC 上的个人博客重建项目

## 背景

毕业之后阿里云服务器到期了，续费居然要**112￥/月**！！！满脸写着吃人……

买了台 NUC,想着迁到NUC上来，保留内容：
- 原前端样式与交互动画（金黄 + 深棕配色、时钟翻转、打字机效果等）
- 所有已导出的博客正文（Markdown 文件）

> 一转眼三年过去了，博客计划一点没动呢（xs

在 AI 发达的当下，**复活吧！我的 blog！**

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 后端 | Python + FastAPI | REST API 服务 |
| 包管理 | uv + venv | Python 依赖管理 |
| 前端 | Vue 3 + Vite + Pinia | SPA 单页应用 |
| 数据库 | SQLite (SQLAlchemy + aiosqlite) | 文章元信息、标签 |
| 博客存储 | Markdown 文件 | NAS 挂载目录 |
| Markdown 渲染 | markdown-it-py | 后端预渲染 |
| 代码高亮 | highlight.js | 前端处理 |
| 数学公式 | KaTeX | 替代原有 MathJax |
| 评论系统 | Artalk | 自托管评论（Go + SQLite） |
| 反向代理 | Traefik v3 | 全局入口、自动 HTTPS (Cloudflare DNS) |
| 部署 | Docker Compose | NUC 容器化部署 |

## 项目结构

```
blogsite/
├── docker-compose.yml       # 博客服务编排（含 Traefik 路由标签）
├── .env                     # 环境变量（JWT 密钥、管理员凭据）
├── backend/                 # FastAPI 后端
│   ├── Dockerfile
│   ├── pyproject.toml       # uv 项目配置
│   ├── uv.lock
│   └── app/
│       ├── main.py          # FastAPI 入口
│       ├── config.py        # 配置管理
│       ├── database.py      # SQLite 连接
│       ├── models.py        # ORM 模型
│       ├── schemas.py       # Pydantic 模型
│       ├── dependencies.py  # JWT 认证等
│       ├── routers/         # API 路由
│       ├── services/        # 业务逻辑
│       └── utils/           # 工具函数
└── frontend/                # Vue 3 前端
    ├── Dockerfile           # 多阶段构建 (node + nginx)
    ├── nginx-spa.conf       # SPA 路由配置
    ├── package.json
    ├── vite.config.js
    ├── src/
    └── dist/                # 构建产物（nginx 托管）
```

## 架构概览

```
用户浏览器 → Traefik (HTTPS) ─┬─ /*       → blog-frontend (nginx 容器)
                              ├─ /api/*   → blog-api (FastAPI 容器)
                              └─ /artalk/* → blog-artalk (评论容器)
                                            ├── SQLite (NAS)
                                            └── Markdown files (NAS)
```

- **Traefik v3** 作为全局反向代理，独立项目管理，通过 Cloudflare DNS 自动签发 HTTPS 证书
- **所有容器** 通过 `traefik-proxy` 外部网络接入，使用 Docker labels 声明路由规则
- **数据存储** 在 NAS（通过 CIFS 挂载），包括 SQLite 数据库和 Markdown 文章文件
- **前端** 在 Docker 多阶段构建中自动编译（node:22-alpine → nginx:alpine），由 Traefik 反代

## 数据存储

```
/mnt/nas_smb/nas/blog/
├── data/blog.db            # SQLite 数据库
└── posts/                  # Markdown 文章
    ├── about.md            # 关于页面 (ID=0)
    └── 24-06-15-my-post/   # 文章目录
        ├── 24-06-15-my-post.md
        └── images/         # 文章图片
```

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/articles` | 文章列表（分页） |
| GET | `/api/v1/articles/{id}` | 文章详情 |
| GET | `/api/v1/articles/about` | 关于页面 |
| GET | `/api/v1/articles/archive` | 归档列表 |
| GET | `/api/v1/tags` | 标签列表 |
| GET | `/api/v1/site/info` | 站点信息 |
| POST | `/api/v1/auth/login` | 管理员登录 |
| POST | `/api/v1/admin/articles` | 创建文章 |
| PUT | `/api/v1/admin/articles/{id}` | 更新文章 |
| DELETE | `/api/v1/admin/articles/{id}` | 删除文章 |

## 本地开发

```bash
# 后端
cd backend
uv sync                                # 安装依赖
uv run uvicorn app.main:app --reload   # 启动开发服务器

# 前端
cd frontend
npm install
npm run dev                            # Vite 开发服务器
```

## 部署

```bash
# 启动服务（需先启动 Traefik，前端在 Docker 内自动构建）
docker compose up -d --build
```

## License

Apache License, Version 2.0
