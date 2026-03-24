/** 标签 */
export interface Tag {
  id: number
  name: string
}

/** 文章摘要（列表用） */
export interface ArticleSummary {
  id: number
  title: string
  summary: string | null
  tags: Tag[]
  created_at: string
  published_at: string | null
}

/** 文章详情 */
export interface ArticleDetail {
  id: number
  title: string
  summary: string | null
  content_html: string
  content_raw: string
  header_image: string | null
  tags: Tag[]
  prev_article: ArticleNav | null
  next_article: ArticleNav | null
  created_at: string
  updated_at: string
  published_at: string | null
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
  page_size: number
  total_pages: number
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
  content_raw: string
  updated_at: string
}

/** TOC 菜单项 */
export interface TocItem {
  title: string
  pos: string
  level: number
}
