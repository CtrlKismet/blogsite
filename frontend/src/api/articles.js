import api from './index'
import { useMock, mockGetArticles, mockGetArticle, mockGetAbout, mockGetArchive } from '../mock/data'

/**
 * 获取文章列表（分页，排除 About）
 * @param {Object} params - { page, size, tag_id }
 */
export function getArticles(params) {
  if (useMock) return mockGetArticles(params)
  return api.get('/articles', { params })
}

/**
 * 获取文章详情
 * @param {number} id
 */
export function getArticle(id) {
  if (useMock) return mockGetArticle(id)
  return api.get(`/articles/${id}`)
}

/**
 * 获取 About 页面
 */
export function getAbout() {
  if (useMock) return mockGetAbout()
  return api.get('/articles/about')
}

/**
 * 获取归档列表
 */
export function getArchive() {
  if (useMock) return mockGetArchive()
  return api.get('/articles/archive')
}
