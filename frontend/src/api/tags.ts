import api from './index'
import type { Tag } from '../types'

interface DataResponse<T> {
  data: T
}

/**
 * 获取所有标签
 */
export function getTags(): Promise<DataResponse<Tag[]>> {
  return api.get('/tags')
}
