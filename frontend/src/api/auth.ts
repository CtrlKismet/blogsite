import api from './index'
import type { LoginResponse } from '../types'

/**
 * 登录
 */
export function login(username: string, password: string): Promise<{ data: LoginResponse }> {
  return api.post('/auth/login', { username, password })
}

/**
 * 验证 token
 */
export function verify(): Promise<{ data: void }> {
  return api.get('/auth/verify')
}
