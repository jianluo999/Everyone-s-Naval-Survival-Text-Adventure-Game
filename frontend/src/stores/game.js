import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import gameApi from '@/api/game'

export const useGameStore = defineStore('game', () => {
  // 状态
  const player = ref(null)
  const currentStory = ref(null)
  const loading = ref(false)
  const error = ref('')
  const gameStarted = ref(false)
  const fishingResult = ref(null)
  const caughtFish = ref(null)

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
      
      player.value = response.player
      
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

  async function eatFish(fishId) {
    if (!player.value || !fishId) return
    
    loading.value = true
    error.value = ''
    
    try {
      const response = await gameApi.eatFish(player.value.name, fishId)
      
      // 更新玩家状态
      if (response.playerChanges) {
        applyPlayerChanges(response.playerChanges)
      }
      
      // 清除已食用的鱼
      if (caughtFish.value && caughtFish.value.id === fishId) {
        caughtFish.value = null
      }
      
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  function applyPlayerChanges(changes) {
    if (!player.value || !changes) return
    
    Object.keys(changes).forEach(key => {
      if (key === 'levelUp') return
      
      const currentValue = player.value[key]
      if (typeof currentValue === 'number') {
        player.value[key] = Math.max(0, currentValue + changes[key])
      }
    })
  }

  function resetGame() {
    player.value = null
    currentStory.value = null
    gameStarted.value = false
    error.value = ''
    fishingResult.value = null
    caughtFish.value = null
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
    eatFish,
    resetGame
  }
}) 