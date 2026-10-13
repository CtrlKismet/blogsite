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
| 博客存储 | Markdown 文件 | 本机可访问的数据目录 |
| Markdown 渲染 | markdown-it-py | 后端预渲染 |
| 数学公式 | KaTeX | 替代原有 MathJax |
| 评论系统 | Artalk | 自托管评论（Go + SQLite） |
| 反向代理 | Traefik v3 | 全局入口、自动 HTTPS (Cloudflare DNS) |
| 图片预览 | Pillow + WebP | 响应式缩放、磁盘缓存 |
| 部署 | Docker Compose | 本机容器化部署 |

## 项目结构

```
blogsite/
├── docker-compose.yml       # 博客服务编排（含 Traefik 路由标签）
├── .env.example             # 公开配置模板（.env 为本地配置，不提交）
├── watcher/                 # 本机文章同步与外部图片下载
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
│       ├── dependencies.py  # 数据库会话依赖
│       ├── routers/         # API 路由
│       ├── services/        # 业务逻辑
│       └── utils/           # 工具函数
└── frontend/                # Vue 3 前端
    ├── Dockerfile           # 多阶段构建 (node + nginx)
    ├── nginx-spa.conf       # SPA 路由配置
    ├── package.json
    ├── vite.config.ts
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
- **数据存储** 包括 SQLite 数据库和 Markdown 文章文件，可使用本机目录或 NAS 挂载目录
- **部署位置** 为同一台本机，watcher 和 API 共享可访问的数据目录
- **前端** 在 Docker 多阶段构建中自动编译（node:22-alpine → nginx:alpine），由 Traefik 反代

## 数据存储

```
/path/to/blog/               # 示例路径，实际位置通过 .env 配置
├── data/blog.db            # SQLite 数据库
└── posts/                  # Markdown 文章
    ├── about/              # 关于页面 (ID=0)
    │   └── content.md
    └── 24-06-15-my-post/   # 文章目录
        ├── content.md
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
| GET | `/api/v1/images/{id}/{filename}` | 原图；可用 `w` 参数请求预览 |

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

博客服务和 watcher 均运行在本机。Traefik 与 remote-file-notifier 依赖独立管理，
服务使用已有的 `traefik-proxy` Docker 网络。数据目录可以使用本机磁盘或 NAS 挂载目录。

在仓库根目录复制 `.env.example` 为 `.env`，填写 `BLOG_DOMAIN`、`DB_DIR` 和
`POSTS_DIR`。图床内网访问可通过 `IMAGE_URL_REWRITES` 配置。
真实域名、主机地址、存储路径和凭据放在本地 `.env` 中；公开模板只使用通用示例。

```bash
cp .env.example .env
# 编辑 .env，设置自己的域名及绝对路径后启动
docker compose up -d --build
docker compose --env-file .env -f watcher/docker-compose.yml up -d --build
```

### 文章图片加速

正文及关于页面的本地文章图片自动使用 640、1280、1920px 响应式预览。
首张正文图片立即加载，其余图片懒加载；点击未带链接的图片可打开原图。
原 Markdown 和原图保持不变，无需重新导入旧文章。

图片接口 `/api/v1/images/{id}/{filename}?w=1280` 首次请求时在线程池生成
质量 80 的 WebP，并复用磁盘缓存。动图、SVG、损坏的图片，以及压缩后体积更大的
图片直接返回原文件。没有 `w` 参数时返回原图。浏览器缓存有效期为一小时。
同名原图更新后会生成新的预览，但浏览器可能在缓存到期后才显示更新。

Compose 将预览保存在 `image_cache` 数据卷中，容器重启后仍可复用。
本地运行可通过 `IMAGE_CACHE_DIR` 指定缓存目录（默认 `/tmp/blog-image-cache`）。
旧预览暂不自动清理；大量替换原图后可在维护时清理预览缓存，后续访问会重新生成。
部署时需重建 `api` 和 `frontend` 服务。若使用 CDN，缓存键需保留 `w` 查询参数，
以区分各尺寸预览。CDN 为可选配置，需单独设置。

```bash
# 更新本机的图片接口和前端（前端在 Docker 内自动构建）
docker compose up -d --build api frontend
```

## License

Apache License, Version 2.0
