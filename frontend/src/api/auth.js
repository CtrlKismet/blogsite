import api from './index'

/**
 * 登录
 */
export function login(username, password) {
  return api.post('/auth/login', { username, password })
}

/**
 * 验证 token
 */
export function verify() {
  return api.get('/auth/verify')
}
