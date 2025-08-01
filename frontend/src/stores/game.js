import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import gameApi from '@/api/game'
import { ElMessage } from 'element-plus'

export const useGameStore = defineStore('game', () => {
  // 状态
  const player = ref(null)
  const currentStory = ref(null)
  const loading = ref(false)
  const error = ref('')
  const gameStarted = ref(false)
  const fishingResult = ref(null)
  const caughtFish = ref(null)
  // 时间信息应该从后端获取，不应该硬编码默认值
  const timeInfo = ref({
    currentDay: 0,
    currentHour: 0,
    timeDescription: '',
    actionsToday: 0,
    maxActionsPerDay: 0,
    remainingActions: 0
  })

  // 计算属性
  const isPlayerAlive = computed(() => {
    return player.value && player.value.health > 0 && player.value.sanity > 0
  })

  const playerLevel = computed(() => {
    return player.value ? player.value.level : 1
  })

  const shipStatus = computed(() => {
    if (!player.value || !player.value.ship) return 'unknown'
    const ship = player.value.ship
    const durabilityPercent = (ship.durability / ship.maxDurability) * 100
    
    if (durabilityPercent > 80) return 'excellent'
    if (durabilityPercent > 60) return 'good'
    if (durabilityPercent > 40) return 'fair'
    if (durabilityPercent > 20) return 'poor'
    return 'critical'
  })

  const canFish = computed(() => {
    return player.value && 
           player.value.energy >= 10 && 
           player.value.sanity >= 20
  })

  const survivalStatus = computed(() => {
    if (!player.value) return 'unknown'
    const hunger = player.value.hunger || 100
    const thirst = player.value.thirst || 100
    
    if (hunger < 20 || thirst < 20) return 'critical'
    if (hunger < 40 || thirst < 40) return 'poor' 
    if (hunger < 60 || thirst < 60) return 'fair'
    return 'good'
  })

  // 动作
  async function createPlayer(playerName) {
    loading.value = true
    error.value = ''
    
    try {
      const response = await gameApi.createPlayer(playerName)
      player.value = response.player
      gameStarted.value = true
      
      // 获取初始故事
      await loadCurrentStory()
      
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function loadPlayer(playerName) {
    loading.value = true
    error.value = ''
    
    try {
      const response = await gameApi.getPlayer(playerName)
      player.value = response.player
      gameStarted.value = true
      
      // 获取当前故事
      await loadCurrentStory()
      
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function loadCurrentStory() {
    if (!player.value || !player.value.gameState) return
    
    loading.value = true
    
    try {
      const storyId = player.value.gameState.currentStoryId
      const response = await gameApi.getStory(storyId)
      currentStory.value = response.story
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function makeChoice(choiceId, nextStoryId) {
    if (!player.value) return
    
    loading.value = true
    error.value = ''
    
    try {
      const response = await gameApi.makeChoice({
        playerName: player.value.name,
        choiceId,
        nextStoryId
      })
      
      // 记录选择前的属性值
      const oldPlayer = { ...player.value }
      
      player.value = response.player
      
      // 更新时间信息
      if (player.value.gameState) {
        timeInfo.value = {
          currentDay: player.value.gameState.currentDay || 1,
          currentHour: player.value.gameState.currentHour || 8,
          timeDescription: player.value.gameState.timeDescription || '上午',
          actionsToday: player.value.gameState.actionsToday || 0,
          maxActionsPerDay: player.value.gameState.maxActionsPerDay || 10,
          remainingActions: (player.value.gameState.maxActionsPerDay || 10) - (player.value.gameState.actionsToday || 0)
        }
      }
      
      // 计算并显示属性变化
      showAttributeChanges(oldPlayer, player.value)
      
      // 加载新故事
      await loadCurrentStory()
      
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 显示属性变化
  function showAttributeChanges(oldPlayer, newPlayer) {
    const changes = []
    
    // 检查各种属性变化
    const attributes = [
      { key: 'gold', name: '金币' },
      { key: 'health', name: '生命值' },
      { key: 'energy', name: '精力' },
      { key: 'sanity', name: '理智' },
      { key: 'hunger', name: '饥饿值' },
      { key: 'thirst', name: '口渴值' },
      { key: 'experience', name: '经验值' }
    ]
    
    attributes.forEach(attr => {
      const oldValue = oldPlayer[attr.key] || 0
      const newValue = newPlayer[attr.key] || 0
      const change = newValue - oldValue
      
      if (change !== 0) {
        const symbol = change > 0 ? '+' : ''
        changes.push(`${attr.name}${symbol}${change}`)
      }
    })
    
    // 检查船只属性变化
    if (oldPlayer.ship && newPlayer.ship) {
      const shipAttributes = [
        { key: 'fuel', name: '燃料' },
        { key: 'food', name: '食物' },
        { key: 'water', name: '淡水' },
        { key: 'durability', name: '耐久' }
      ]
      
      shipAttributes.forEach(attr => {
        const oldValue = oldPlayer.ship[attr.key] || 0
        const newValue = newPlayer.ship[attr.key] || 0
        const change = newValue - oldValue
        
        if (change !== 0) {
          const symbol = change > 0 ? '+' : ''
          changes.push(`${attr.name}${symbol}${change}`)
        }
      })
    }
    
    // 显示变化
    if (changes.length > 0) {
      const message = `属性变化：${changes.join(', ')}`
      
      // 根据变化类型显示不同的消息类型
      const hasNegativeChange = changes.some(change => change.includes('-'))
      const hasPositiveChange = changes.some(change => change.includes('+'))
      
      if (hasNegativeChange && !hasPositiveChange) {
        ElMessage.warning(message)
      } else if (hasPositiveChange && !hasNegativeChange) {
        ElMessage.success(message)
      } else {
        ElMessage.info(message)
      }
    }
  }

  async function updatePlayerStats(changes) {
    if (!player.value) return
    
    loading.value = true
    error.value = ''
    
    try {
      const response = await gameApi.updatePlayerStats(player.value.name, changes)
      player.value = response.player
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function goFishing() {
    if (!player.value || !canFish.value) {
      error.value = '无法钓鱼：精力不足或理智过低'
      return
    }

    loading.value = true
    error.value = ''

    try {
      const response = await gameApi.goFishing(player.value.name)
      fishingResult.value = response

      if (response.fish) {
        caughtFish.value = response.fish
      }

      // 更新玩家状态
      if (response.playerChanges) {
        applyPlayerChanges(response.playerChanges)
      }

      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function goFishingWithSpot(spot) {
    if (!player.value || !canFish.value) {
      error.value = '无法钓鱼：精力不足或理智过低'
      return
    }

    loading.value = true
    error.value = ''

    try {
      const response = await gameApi.goFishingWithSpot(player.value.name, spot)
      fishingResult.value = response

      if (response.fish) {
        caughtFish.value = response.fish
      }

      // 更新玩家状态
      if (response.playerChanges) {
        applyPlayerChanges(response.playerChanges)
      }

      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 注意：所有游戏数据都应该从后端获取，不在前端硬编码
  // 这些数据仅作为类型定义参考，实际使用时从API获取

  async function eatFish(fishId) {
    if (!player.value) return;

    try {
      // 修复API调用 - 使用正确的参数格式
      const response = await gameApi.eatFish(player.value.name, fishId);

      // 更新玩家状态
      if (response.success) {
        // 应用玩家状态变化
        if (response.playerChanges) {
          applyPlayerChanges(response.playerChanges);
        }
        ElMessage.success(response.message);

        // 清除已食用的鱼
        caughtFish.value = null;

        // 同步最新状态
        await syncPlayerState();
      } else {
        ElMessage.error(response.message || '食用失败');
      }

    } catch (error) {
      ElMessage.error(error.message || '食用失败');
      console.error('食用鱼失败:', error);
    }
  }

  function clearCaughtFish() {
    caughtFish.value = null;
  }

  function applyPlayerChanges(changes) {
    if (!player.value) return;
    
    Object.keys(changes).forEach(key => {
      if (key === 'levelUp') return
      
      const currentValue = player.value[key]
      if (typeof currentValue === 'number') {
        player.value[key] = Math.max(0, currentValue + changes[key])
      }
    })
  }

  async function advanceTime() {
    if (!player.value) return
    
    loading.value = true
    error.value = ''
    
    try {
      const response = await gameApi.advanceTime(player.value.name)
      
      if (response.success) {
        player.value = response.player
        timeInfo.value = {
          currentDay: response.currentDay,
          currentHour: response.currentHour,
          timeDescription: response.timeDescription,
          actionsToday: response.actionsToday || 0,
          maxActionsPerDay: response.maxActionsPerDay || 10,
          remainingActions: (response.maxActionsPerDay || 10) - (response.actionsToday || 0)
        }
      }
      
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getTimeInfo() {
    if (!player.value) return
    
    try {
      const response = await gameApi.getTimeInfo(player.value.name)
      
      if (response.success) {
        timeInfo.value = {
          currentDay: response.currentDay,
          currentHour: response.currentHour,
          timeDescription: response.timeDescription,
          actionsToday: response.actionsToday || 0,
          maxActionsPerDay: response.maxActionsPerDay || 10,
          remainingActions: (response.maxActionsPerDay || 10) - (response.actionsToday || 0)
        }
      }
      
      return response
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  function resetGame() {
    player.value = null
    currentStory.value = null
    gameStarted.value = false
    error.value = ''
    fishingResult.value = null
    caughtFish.value = null
    timeInfo.value = {
      currentDay: 0,
      currentHour: 0,
      timeDescription: '',
      actionsToday: 0,
      maxActionsPerDay: 0,
      remainingActions: 0
    }
  }

  // 统一的状态同步方法 - 确保前端状态与后端一致
  async function syncPlayerState() {
    if (!player.value?.name) return

    try {
      const response = await gameApi.getPlayer(player.value.name)
      player.value = response.player

      // 同步时间信息
      if (player.value.gameState) {
        timeInfo.value = {
          currentDay: player.value.gameState.currentDay || 1,
          currentHour: player.value.gameState.currentHour || 8,
          timeDescription: player.value.gameState.timeDescription || '上午',
          actionsToday: player.value.gameState.actionsToday || 0,
          maxActionsPerDay: player.value.gameState.maxActionsPerDay || 10,
          remainingActions: (player.value.gameState.maxActionsPerDay || 10) - (player.value.gameState.actionsToday || 0)
        }
      }

      // 同步当前故事
      await loadCurrentStory()

      console.log('✅ 状态同步成功:', player.value)
    } catch (err) {
      console.error('❌ 状态同步失败:', err)
      error.value = '状态同步失败: ' + err.message
    }
  }

  // 定期同步状态（可选，防止前后端数据偏差）
  let syncInterval = null

  function startAutoSync(intervalMs = 30000) { // 30秒同步一次
    if (syncInterval) clearInterval(syncInterval)

    syncInterval = setInterval(() => {
      if (gameStarted.value && player.value) {
        syncPlayerState()
      }
    }, intervalMs)
  }

  function stopAutoSync() {
    if (syncInterval) {
      clearInterval(syncInterval)
      syncInterval = null
    }
  }

  return {
    // 状态
    player,
    currentStory,
    loading,
    error,
    gameStarted,
    fishingResult,
    caughtFish,
    timeInfo,

    // 计算属性
    isPlayerAlive,
    playerLevel,
    shipStatus,
    canFish,
    survivalStatus,

    // 动作
    createPlayer,
    loadPlayer,
    loadCurrentStory,
    makeChoice,
    updatePlayerStats,
    goFishing,
    goFishingWithSpot,
    eatFish,
    clearCaughtFish,
    advanceTime,
    getTimeInfo,
    resetGame,

    // 新增：状态同步方法
    syncPlayerState,
    startAutoSync,
    stopAutoSync
  }
}) 