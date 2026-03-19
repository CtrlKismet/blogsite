import api from './index'

/**
 * 创建文章
 */
export function createArticle(data: Record<string, unknown>): Promise<any> {
  return api.post('/admin/articles', data)
}

/**
 * 更新文章
 */
export function updateArticle(id: number | string, data: Record<string, unknown>): Promise<any> {
  return api.put(`/admin/articles/${id}`, data)
}

/**
 * 删除文章
 */
export function deleteArticle(id: number | string): Promise<any> {
  return api.delete(`/admin/articles/${id}`)
}

/**
 * 创建标签
 */
export function createTag(data: { name: string }): Promise<any> {
  return api.post('/admin/tags', data)
}

/**
 * 删除标签
 */
export function deleteTag(id: number | string): Promise<any> {
  return api.delete(`/admin/tags/${id}`)
}

/**
 * 上传图片
 */
export function uploadImage(articleId: number | string, formData: FormData): Promise<any> {
  return api.post(`/admin/images/${articleId}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
