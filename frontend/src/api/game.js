import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8080/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('发送请求:', config.method?.toUpperCase(), config.url, config.data)
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('响应数据:', response.data)
    return response.data
  },
  (error) => {
    console.error('响应错误:', error.response || error)
    
    let errorMessage = '网络错误，请稍后重试'
    
    if (error.response) {
      // 服务器响应了错误状态码
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          errorMessage = data.error || '请求参数错误'
          break
        case 404:
          errorMessage = data.message || '资源不存在'
          break
        case 500:
          errorMessage = data.message || '服务器内部错误'
          break
        default:
          errorMessage = data.message || `服务器错误 (${status})`
      }
    } else if (error.request) {
      // 请求已发送但没有收到响应
      errorMessage = '无法连接到服务器，请检查网络'
    }
    
    return Promise.reject(new Error(errorMessage))
  }
)

// 游戏API
const gameApi = {
  // 健康检查
  async healthCheck() {
    return await api.get('/game/health')
  },

  // 创建玩家
  async createPlayer(playerName) {
    return await api.post('/game/player', { name: playerName })
  },

  // 获取玩家信息
  async getPlayer(playerName) {
    return await api.get(`/game/player/${playerName}`)
  },

  // 获取故事
  async getStory(storyId) {
    return await api.get(`/game/story/${storyId}`)
  },

  // 做出选择
  async makeChoice(data) {
    return await api.post('/game/choice', data)
  },

  // 更新玩家状态
  async updatePlayerStats(playerName, changes) {
    return await api.put(`/game/player/${playerName}/stats`, changes)
  },

  // 钓鱼
  async goFishing(playerName) {
    return await api.post(`/game/player/${playerName}/fishing`)
  },

  // 食用鱼类
  async eatFish(playerName, fishId) {
    return await api.post(`/game/player/${playerName}/eat/${fishId}`)
  },

  // 时间推进
  async advanceTime(playerName) {
    return await api.post(`/game/player/${playerName}/advance-time`)
  },

  // 获取时间信息
  async getTimeInfo(playerName) {
    return await api.get(`/game/player/${playerName}/time`)
  }
}

export default gameApi 