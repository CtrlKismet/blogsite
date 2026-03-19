import api from './index'

/**
 * 获取所有标签
 */
export function getTags() {
  return api.get('/tags')
}
