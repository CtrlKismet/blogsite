import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器：解包 { code, message, data } 响应信封 + 统一错误处理
api.interceptors.response.use(
  (response) => {
    // 后端 API 返回 { code, message, data } 格式
    // 将 response.data 从信封中解包为实际数据
    const body = response.data
    if (body && typeof body === 'object' && 'code' in body) {
      if (body.code !== 200) {
        return Promise.reject(new Error(body.message || '请求失败'))
      }
      // 解包：让 response.data 直接指向 body.data
      response.data = body.data
    }
    return response
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api
