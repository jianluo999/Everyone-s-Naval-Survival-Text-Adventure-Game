// 自动保存管理器
class AutoSaveManager {
  constructor() {
    this.enabled = true
    this.interval = 30000 // 30秒自动保存
    this.maxSaves = 10 // 最多保留10个自动保存
    this.timer = null
    this.gameStore = null
    this.lastSaveTime = 0
    this.saveQueue = []
  }

  // 初始化
  init(gameStore) {
    this.gameStore = gameStore
    this.startAutoSave()
    this.setupEventListeners()
  }

  // 开始自动保存
  startAutoSave() {
    if (this.timer) {
      clearInterval(this.timer)
    }

    this.timer = setInterval(() => {
      if (this.enabled && this.gameStore?.player) {
        this.performAutoSave()
      }
    }, this.interval)
  }

  // 停止自动保存
  stopAutoSave() {
    if (this.timer) {
      clearInterval(this.timer)
      this.timer = null
    }
  }

  // 执行自动保存
  async performAutoSave() {
    try {
      const now = Date.now()
      
      // 防止频繁保存
      if (now - this.lastSaveTime < 10000) {
        return
      }

      const saveData = {
        player: this.gameStore.player,
        timeInfo: this.gameStore.timeInfo,
        gameState: this.gameStore.gameState,
        timestamp: now,
        type: 'auto',
        version: '1.0'
      }

      // 保存到本地存储
      const saveKey = `autosave_${now}`
      localStorage.setItem(saveKey, JSON.stringify(saveData))
      
      // 添加到保存队列
      this.saveQueue.push(saveKey)
      
      // 清理旧的自动保存
      this.cleanupOldSaves()
      
      this.lastSaveTime = now
      
      // 显示保存提示
      this.showSaveNotification('自动保存完成')
      
    } catch (error) {
      console.error('自动保存失败:', error)
    }
  }

  // 清理旧的自动保存
  cleanupOldSaves() {
    // 保持最新的N个自动保存
    while (this.saveQueue.length > this.maxSaves) {
      const oldSave = this.saveQueue.shift()
      localStorage.removeItem(oldSave)
    }
  }

  // 获取所有自动保存
  getAutoSaves() {
    const saves = []
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && key.startsWith('autosave_')) {
        try {
          const data = JSON.parse(localStorage.getItem(key))
          saves.push({
            key,
            timestamp: data.timestamp,
            data
          })
        } catch (error) {
          console.error('读取自动保存失败:', error)
        }
      }
    }
    
    // 按时间排序
    return saves.sort((a, b) => b.timestamp - a.timestamp)
  }

  // 加载自动保存
  loadAutoSave(saveKey) {
    try {
      const saveData = localStorage.getItem(saveKey)
      if (saveData) {
        const data = JSON.parse(saveData)
        return data
      }
    } catch (error) {
      console.error('加载自动保存失败:', error)
    }
    return null
  }

  // 删除自动保存
  deleteAutoSave(saveKey) {
    localStorage.removeItem(saveKey)
    this.saveQueue = this.saveQueue.filter(key => key !== saveKey)
  }

  // 设置自动保存间隔
  setInterval(interval) {
    this.interval = interval
    if (this.enabled) {
      this.startAutoSave()
    }
  }

  // 启用/禁用自动保存
  setEnabled(enabled) {
    this.enabled = enabled
    if (enabled) {
      this.startAutoSave()
    } else {
      this.stopAutoSave()
    }
  }

  // 设置事件监听
  setupEventListeners() {
    // 监听游戏状态变化
    document.addEventListener('gameStateChanged', () => {
      // 延迟保存，避免频繁操作
      setTimeout(() => {
        if (this.enabled) {
          this.performAutoSave()
        }
      }, 1000)
    })

    // 页面关闭前保存
    window.addEventListener('beforeunload', () => {
      if (this.enabled && this.gameStore?.player) {
        this.performAutoSave()
      }
    })

    // 页面失去焦点时保存
    window.addEventListener('blur', () => {
      if (this.enabled && this.gameStore?.player) {
        setTimeout(() => this.performAutoSave(), 500)
      }
    })
  }

  // 显示保存通知
  showSaveNotification(message) {
    // 创建通知元素
    const notification = document.createElement('div')
    notification.className = 'auto-save-notification'
    notification.textContent = message
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: rgba(0, 40, 80, 0.9);
      color: #66ffcc;
      padding: 8px 16px;
      border-radius: 4px;
      border: 1px solid #66ffcc;
      font-size: 12px;
      z-index: 9999;
      opacity: 0;
      transition: opacity 0.3s ease;
    `
    
    document.body.appendChild(notification)
    
    // 显示动画
    setTimeout(() => {
      notification.style.opacity = '1'
    }, 100)
    
    // 自动消失
    setTimeout(() => {
      notification.style.opacity = '0'
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification)
        }
      }, 300)
    }, 2000)
  }

  // 获取保存统计
  getSaveStats() {
    const saves = this.getAutoSaves()
    return {
      totalSaves: saves.length,
      lastSaveTime: saves.length > 0 ? saves[0].timestamp : null,
      oldestSaveTime: saves.length > 0 ? saves[saves.length - 1].timestamp : null,
      totalSize: saves.reduce((size, save) => {
        return size + JSON.stringify(save.data).length
      }, 0)
    }
  }
}

export const autoSaveManager = new AutoSaveManager()
export default autoSaveManager
