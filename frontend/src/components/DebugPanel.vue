<template>
  <div class="debug-panel">
    <h3>🔧 调试面板</h3>
    
    <div class="debug-section">
      <h4>玩家数据完整性检查</h4>
      <div class="debug-info">
        <p><strong>玩家对象存在:</strong> {{ !!player }}</p>
        <p><strong>精力值:</strong> {{ player?.energy || '未定义' }}/{{ player?.maxEnergy || '未定义' }}</p>
        <p><strong>理智值:</strong> {{ player?.sanity || '未定义' }}/{{ player?.maxSanity || '未定义' }}</p>
        <p><strong>饥饿值:</strong> {{ player?.hunger || '未定义' }}</p>
        <p><strong>口渴值:</strong> {{ player?.thirst || '未定义' }}</p>
      </div>
    </div>

    <div class="debug-section">
      <h4>钓鱼系统检查</h4>
      <div class="debug-info">
        <p><strong>canFish 状态:</strong> {{ canFish }}</p>
        <p><strong>精力检查 (≥10):</strong> {{ (player?.energy || 0) >= 10 }}</p>
        <p><strong>理智检查 (≥20):</strong> {{ (player?.sanity || 0) >= 20 }}</p>
        <p><strong>计算结果:</strong> {{ player && (player.energy >= 10) && (player.sanity >= 20) }}</p>
      </div>
    </div>

    <div class="debug-section">
      <h4>完整玩家数据</h4>
      <pre class="debug-json">{{ JSON.stringify(player, null, 2) }}</pre>
    </div>

    <div class="debug-actions">
      <button @click="refreshPlayer" :disabled="loading">
        {{ loading ? '刷新中...' : '刷新玩家数据' }}
      </button>
      <button @click="testFishing" :disabled="loading">
        测试钓鱼API
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()

const { player, loading, canFish } = gameStore

const refreshPlayer = async () => {
  if (!player.value?.name) return
  
  try {
    await gameStore.loadPlayer(player.value.name)
  } catch (error) {
    console.error('刷新玩家数据失败:', error)
  }
}

const testFishing = async () => {
  if (!player.value?.name) return
  
  try {
    console.log('测试钓鱼API...')
    console.log('当前玩家数据:', player.value)
    console.log('canFish状态:', canFish.value)
    
    if (canFish.value) {
      await gameStore.goFishing()
    } else {
      console.log('钓鱼条件不满足')
    }
  } catch (error) {
    console.error('钓鱼测试失败:', error)
  }
}
</script>

<style scoped>
.debug-panel {
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px 0;
  font-family: monospace;
  max-height: 400px;
  overflow-y: auto;
}

.debug-panel h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.2em;
}

.debug-section {
  margin-bottom: 15px;
  padding: 10px;
  background: white;
  border-radius: 4px;
  border-left: 4px solid #007bff;
}

.debug-section h4 {
  margin: 0 0 10px 0;
  color: #007bff;
  font-size: 1em;
}

.debug-info {
  font-size: 0.9em;
}

.debug-info p {
  margin: 5px 0;
  padding: 2px 0;
}

.debug-json {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 10px;
  max-height: 200px;
  overflow-y: auto;
  font-size: 0.8em;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.debug-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.debug-actions button {
  padding: 8px 15px;
  border: 1px solid #007bff;
  background: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.debug-actions button:hover:not(:disabled) {
  background: #0056b3;
}

.debug-actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style> 