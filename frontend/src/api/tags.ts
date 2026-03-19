import api from './index'
import { useMock, mockGetTags } from '../mock/data'
import type { Tag } from '../types'

interface DataResponse<T> {
  data: T
}

/**
 * 获取所有标签
 */
export function getTags(): Promise<DataResponse<Tag[]>> {
  if (useMock) return mockGetTags()
  return api.get('/tags')
}
