<template>
  <div class="island-exploration">
    <div class="exploration-header">
      <h3>🏝️ 岛屿探索</h3>
      <p>探索神秘的海岛，寻找宝藏和资源</p>
    </div>
    
    <div class="exploration-content">
      <div class="island-map">
        <div class="map-grid">
          <div 
            v-for="(area, index) in explorationAreas" 
            :key="index"
            class="map-area"
            :class="{ 'explored': area.explored, 'current': area.current }"
            @click="exploreArea(area)"
          >
            <div class="area-icon">{{ area.icon }}</div>
            <div class="area-name">{{ area.name }}</div>
            <div class="area-status" v-if="area.explored">✓</div>
          </div>
        </div>
      </div>
      
      <div class="exploration-info">
        <div class="current-area" v-if="currentArea">
          <h4>{{ currentArea.name }}</h4>
          <p>{{ currentArea.description }}</p>
          
          <div class="area-actions">
            <button 
              v-for="action in currentArea.actions" 
              :key="action.id"
              @click="performAction(action)"
              class="action-btn"
              :disabled="!canPerformAction(action)"
            >
              {{ action.icon }} {{ action.name }}
            </button>
          </div>
        </div>
        
        <div class="exploration-log">
          <h4>探索日志</h4>
          <div class="log-entries">
            <div 
              v-for="(entry, index) in explorationLog" 
              :key="index"
              class="log-entry"
            >
              <span class="log-time">{{ entry.time }}</span>
              <span class="log-text">{{ entry.text }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 响应式数据
const currentArea = ref(null)
// 从后端API获取探索数据
const explorationLog = ref([])
const explorationAreas = ref([])
const loadingExploration = ref(false)

// 方法
const exploreArea = (area) => {
  if (area.explored) {
    currentArea.value = area
    area.current = true
    // 取消其他区域的当前状态
    explorationAreas.value.forEach(a => {
      if (a.id !== area.id) a.current = false
    })
  } else {
    // 首次探索
    area.explored = true
    area.current = true
    currentArea.value = area
    
    // 取消其他区域的当前状态
    explorationAreas.value.forEach(a => {
      if (a.id !== area.id) a.current = false
    })
    
    addLogEntry(`发现了新区域：${area.name}`)
  }
}

const performAction = (action) => {
  if (!canPerformAction(action)) return
  
  // 模拟执行动作
  addLogEntry(`执行了动作：${action.name}`)
  
  // 这里可以添加具体的动作逻辑
  switch (action.id) {
    case 'collect_shells':
      addLogEntry('收集到了一些美丽的贝壳')
      break
    case 'search_debris':
      addLogEntry('在漂流物中发现了有用的物品')
      break
    case 'gather_wood':
      addLogEntry('收集到了一些优质木材')
      break
    case 'hunt_animals':
      addLogEntry('成功捕获了一些小动物')
      break
    case 'explore_cave':
      addLogEntry('在洞穴深处发现了闪闪发光的东西')
      break
    case 'mine_ore':
      addLogEntry('挖掘到了珍贵的矿石')
      break
    case 'investigate_ruins':
      addLogEntry('在遗迹中发现了古老的文物')
      break
    case 'decipher_symbols':
      addLogEntry('成功解读了一些古老的符文')
      break
  }
}

const canPerformAction = (action) => {
  // 简单的能量检查（这里假设玩家有足够的能量）
  return true
}

const addLogEntry = (text) => {
  const now = new Date()
  const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
  explorationLog.value.push({ time, text })
  
  // 限制日志条目数量
  if (explorationLog.value.length > 10) {
    explorationLog.value.shift()
  }
}
</script>

<style lang="scss" scoped>
.island-exploration {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(0, 20, 40, 0.9);
  border-radius: 10px;
  overflow: hidden;
}

.exploration-header {
  background: rgba(0, 30, 50, 0.9);
  padding: 1rem;
  border-bottom: 2px solid #66ffcc;
  
  h3 {
    color: #66ffcc;
    margin: 0 0 0.5rem 0;
    font-size: 1.3rem;
  }
  
  p {
    color: #ffffff;
    margin: 0;
    opacity: 0.8;
    font-size: 0.9rem;
  }
}

.exploration-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
}

.island-map {
  background: rgba(0, 10, 20, 0.8);
  border-radius: 8px;
  padding: 1rem;
  
  .map-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  
  .map-area {
    background: rgba(102, 255, 204, 0.1);
    border: 2px solid transparent;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    
    &:hover {
      border-color: #66ffcc;
      background: rgba(102, 255, 204, 0.2);
    }
    
    &.explored {
      border-color: #32CD32;
      background: rgba(50, 205, 50, 0.1);
    }
    
    &.current {
      border-color: #FFD700;
      background: rgba(255, 215, 0, 0.2);
      box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }
    
    .area-icon {
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }
    
    .area-name {
      color: #ffffff;
      font-weight: bold;
      font-size: 0.9rem;
    }
    
    .area-status {
      position: absolute;
      top: 5px;
      right: 5px;
      color: #32CD32;
      font-size: 1.2rem;
    }
  }
}

.exploration-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.current-area {
  background: rgba(0, 10, 20, 0.8);
  border-radius: 8px;
  padding: 1rem;
  
  h4 {
    color: #66ffcc;
    margin: 0 0 0.5rem 0;
  }
  
  p {
    color: #ffffff;
    margin: 0 0 1rem 0;
    opacity: 0.9;
    line-height: 1.4;
  }
  
  .area-actions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .action-btn {
    background: rgba(102, 255, 204, 0.1);
    border: 1px solid #66ffcc;
    color: #66ffcc;
    padding: 0.8rem;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
    
    &:hover:not(:disabled) {
      background: rgba(102, 255, 204, 0.2);
      transform: translateX(5px);
    }
    
    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}

.exploration-log {
  background: rgba(0, 10, 20, 0.8);
  border-radius: 8px;
  padding: 1rem;
  flex: 1;
  
  h4 {
    color: #66ffcc;
    margin: 0 0 1rem 0;
  }
  
  .log-entries {
    max-height: 200px;
    overflow-y: auto;
  }
  
  .log-entry {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    background: rgba(102, 255, 204, 0.05);
    border-radius: 4px;
    
    .log-time {
      color: #FFD700;
      font-size: 0.8rem;
      min-width: 40px;
    }
    
    .log-text {
      color: #ffffff;
      font-size: 0.9rem;
      opacity: 0.9;
    }
  }
}
</style>
