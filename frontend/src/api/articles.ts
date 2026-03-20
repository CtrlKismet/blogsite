import api from './index'
import type { ArticleListResponse, ArticleDetail, AboutArticle, ArchiveGroup } from '../types'

export interface ArticleListParams {
  page?: number
  page_size?: number
  tag_id?: number
  year?: number
}

interface DataResponse<T> {
  data: T
}

/**
 * 获取文章列表（分页，排除 About）
 */
export function getArticles(params?: ArticleListParams): Promise<DataResponse<ArticleListResponse>> {
  return api.get('/articles', { params })
}

/**
 * 获取文章详情
 */
export function getArticle(id: number | string): Promise<DataResponse<ArticleDetail>> {
  return api.get(`/articles/${id}`)
}

/**
 * 获取 About 页面
 */
export function getAbout(): Promise<DataResponse<AboutArticle>> {
  return api.get('/articles/about')
}

/**
 * 获取归档列表
 */
export function getArchive(): Promise<DataResponse<ArchiveGroup[]>> {
  return api.get('/articles/archive')
}
