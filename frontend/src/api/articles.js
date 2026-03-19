import api from './index'

/**
 * 获取文章列表（分页，排除 About）
 * @param {Object} params - { page, size, tag_id }
 */
export function getArticles(params) {
  return api.get('/articles', { params })
}

/**
 * 获取文章详情
 * @param {number} id
 */
export function getArticle(id) {
  return api.get(`/articles/${id}`)
}

/**
 * 获取 About 页面
 */
export function getAbout() {
  return api.get('/articles/about')
}

/**
 * 获取归档列表
 */
export function getArchive() {
  return api.get('/articles/archive')
}
