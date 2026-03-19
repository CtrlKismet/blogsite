import api from './index'
import { useMock, mockGetTags } from '../mock/data'

/**
 * 获取所有标签
 */
export function getTags() {
  if (useMock) return mockGetTags()
  return api.get('/tags')
}
