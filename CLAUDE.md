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
├── watcher/           # 文件监听服务（remote-file-notifier 消费者）
│   ├── app/
│   │   ├── main.py        # 启动入口：全量同步 + HTTP 回调监听 + 消抖处理
│   │   ├── sync.py        # 文章同步逻辑（含变更检测）
│   │   ├── intake.py      # 散落 .md 文件整理
│   │   ├── metadata.py    # 顶部 summary/tags/published_at 解析及 .meta 读取
│   │   ├── image_processor.py  # 外部图片下载本地化
│   │   ├── config.py      # 配置
│   │   └── database.py    # 同步 SQLAlchemy ORM
│   ├── Dockerfile
│   ├── docker-compose.yml # 本机部署（接入 traefik-proxy 网络）
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
- **文件监听**: remote-file-notifier (Server 端 inotify → WebSocket → Client 端 HTTP 回调)
- **HTTP 回调**: Python 内置 `http.server`（轻量，无额外依赖）
- **数据库**: SQLAlchemy (同步)
- **变更检测**: SHA-256 内容 hash 对比，避免重复处理

### 部署
- **容器化**: Docker + Docker Compose
- **本机服务**: `docker-compose.yml` — frontend + api + artalk
- **本机文章同步**: `watcher/docker-compose.yml` — watcher（remote-file-notifier 消费者）
- **前置依赖**: 文件存储端运行 `remote-file-notifier` server，本机运行 client
- **网络**: watcher 接入 `traefik-proxy` 网络，通过 Docker DNS 访问 notifier client
- **数据访问**: watcher 与 API 共享本机可访问的数据库及文章目录，可使用 NAS 挂载目录
- **反向代理**: Traefik v3 (HTTPS + Docker labels 路由)
- **前端部署**: 多阶段 Docker 构建 (node:22-alpine → nginx:alpine) → Traefik 反代

## 数据模型

- **Article**: id, title, summary, file_path, header_image, status, created_at, published_at, updated_at
- **Tag**: id, name (unique)
- **ArticleTag**: article_id, tag_id (多对多关联)

## API 路由

后端 API 前缀为 `/api/v1`，主要路由模块：
- `articles` — 文章分页、详情、归档及关于页面
- `tags` — 标签列表、按标签筛选
- `images` — 原图及磁盘缓存的 WebP 响应式预览
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
# 在仓库根目录准备 .env，并设置域名及数据目录
cp .env.example .env
# 先启动独立管理的 Traefik 与 notifier 依赖
docker compose up -d --build

# 在同一台主机上启动 watcher，显式复用根目录的环境变量
docker compose --env-file .env -f watcher/docker-compose.yml up -d --build

docker compose logs -f         # 查看博客服务日志
```

## 环境变量

参考 `.env.example`：
| 变量 | 说明 |
|------|------|
| `BLOG_DOMAIN` | 博客访问域名，用于 Traefik 路由 |
| `DB_DIR` | SQLite 数据库目录 (宿主机路径) |
| `POSTS_DIR` | Markdown 文章目录 (宿主机路径) — 同时作为 notifier watch 注册路径 |
| `IMAGE_URL_REWRITES` | 可选图床内网映射，格式为 `public_origin=internal_base`，多个映射用逗号分隔 |

### Watcher 容器内变量（docker-compose.yml 中设定）
| 变量 | 默认值 | 说明 |
|------|--------|------|
| `POSTS_DIR` | `${POSTS_DIR}` | 透传宿主路径，用于 notifier 注册 |
| `POSTS_MOUNT` | `/data/posts` | 容器内挂载点，文件 I/O 使用 |
| `NOTIFIER_API` | `http://remote-file-notifier-client:9877` | notifier client API 地址 |
| `WATCH_EVENTS` | `closed,created,moved` | 监听的事件类型 |
| `WATCH_PATTERN` | `\.md$` | 文件路径正则过滤 |
| `WATCH_EXCLUDE` | `.meta,.title,.~*,.DS_Store,Thumbs.db` | fnmatch 排除模式 |

## 文章图片加速

- 本地文章图片由前端在插入正文前转换为响应式预览请求，首张立即加载，其余懒加载
- `w` 参数仅接受 `640`、`1280`、`1920`；省略时返回原图
- API 在线程池中生成质量 80 的 WebP，并通过原图路径、修改时间、大小及预览宽度区分缓存
- 动图、SVG、转换失败及预览体积更大的情况返回原文件
- `IMAGE_CACHE_DIR` 指定缓存目录；Compose 使用独立的 `image_cache` 数据卷
- 图片浏览器缓存期限为一小时；旧磁盘缓存暂不自动清理

## 文章发布时间

- 新文章的 `published_at` 默认取 watcher 首次导入的站点本地时间，不从目录日期补零生成
- Markdown 顶部可用 `published_at: YYYY-MM-DD HH:mm:ss` 指定完整发布时间；空值或省略使用首次导入时间
- 已有文章目录也可在首次同步前通过 `.meta` 的 `published_at` 字段指定时间
- 不带偏移的时间按 watcher 的 `TZ` 解释；带偏移的 ISO 时间转换为站点本地时间
- 目录日期及仅含日期的旧 Markdown 头只影响目录命名；现有文章时间不迁移，正文修改也不重置发布时间
- 时间元信息无效时不导入相应文件或目录，避免静默丢失手动时间
- 验证：在 `watcher/` 下运行 `.venv/bin/python -m unittest discover -s tests -v`

## 开发注意事项

- 前端开发时 Vite 会将 `/api` 代理到 `http://localhost:8000`
- 生产环境前端打包在 nginx 容器中，由 Traefik 反代提供服务
- 数据库为 SQLite，使用 WAL 模式，watcher 和 backend 共享同一个 db 文件
- watcher 启动流程：全量同步 → HTTP 回调服务器 → 向 notifier client 注册 watch → 事件循环
- watcher 通过 SHA-256 hash 检测文章内容变更，仅在 hash 变化时触发 meta 重新提取
- `POSTS_DIR`（宿主路径）用于 notifier 注册，`POSTS_MOUNT`（容器挂载点）用于文件读写，两者通过 `_to_local()` 前缀替换桥接
- watcher 仅从 Markdown 顶部元信息读取 `summary`、`tags`、`published_at`，不再扫描正文中的 `简介：` 或 `tag：`
- 顶部元信息保存到 `.meta` 并从正文移除，摘要与标签同步入库；省略字段保留已有值，显式空摘要或空标签则清空对应值
- `tags` 使用英文逗号分隔，也支持中文逗号、顿号及中英文分号；去除首尾空格并去重
- 提交规范遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/)

## 公开仓库配置

- `.env` 仅存放在部署主机上，已被 Git 忽略
- 文档及 `.env.example` 使用示例域名和通用路径；真实域名、主机地址、存储路径及凭据通过本地配置提供
