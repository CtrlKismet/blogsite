/** 标签 */
export interface Tag {
  id: number
  name: string
}

/** 文章摘要（列表用） */
export interface ArticleSummary {
  id: number
  title: string
  summary: string
  status: string
  published_at: string
  updated_at: string
  tags: Tag[]
}

/** 文章详情 */
export interface ArticleDetail extends ArticleSummary {
  content_html: string
  header_image: string | null
  prev_article?: ArticleNav | null
  next_article?: ArticleNav | null
}

/** 上下篇导航 */
export interface ArticleNav {
  id: number
  title: string
}

/** 文章列表分页 */
export interface ArticleListResponse {
  items: ArticleSummary[]
  total: number
  page: number
  size: number
}

/** 归档分组 */
export interface ArchiveGroup {
  year: number
  articles: ArchiveArticle[]
}

/** 归档文章 */
export interface ArchiveArticle {
  id: number
  title: string
  published_at: string
}

/** About 页数据 */
export interface AboutArticle {
  id: number
  title: string
  content_html: string
  published_at: string
  updated_at: string
}

/** 编辑器表单 */
export interface ArticleForm {
  title: string
  summary: string
  header_image: string
  content: string
}

/** 登录响应 */
export interface LoginResponse {
  access_token: string
}

/** TOC 菜单项 */
export interface TocItem {
  title: string
  pos: string
  level: number
}
