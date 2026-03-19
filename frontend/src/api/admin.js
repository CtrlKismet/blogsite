import api from './index'

/**
 * 创建文章
 */
export function createArticle(data) {
  return api.post('/admin/articles', data)
}

/**
 * 更新文章
 */
export function updateArticle(id, data) {
  return api.put(`/admin/articles/${id}`, data)
}

/**
 * 删除文章
 */
export function deleteArticle(id) {
  return api.delete(`/admin/articles/${id}`)
}

/**
 * 创建标签
 */
export function createTag(data) {
  return api.post('/admin/tags', data)
}

/**
 * 删除标签
 */
export function deleteTag(id) {
  return api.delete(`/admin/tags/${id}`)
}

/**
 * 上传图片
 */
export function uploadImage(articleId, formData) {
  return api.post(`/admin/images/${articleId}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
