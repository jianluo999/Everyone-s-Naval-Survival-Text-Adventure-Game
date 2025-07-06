<template>
  <div class="navigation-log">
    <el-card class="log-card">
      <template #header>
        <div class="card-header">
          <el-icon><Notebook /></el-icon>
          <span>航海日志</span>
          <div class="header-actions">
            <el-button-group>
              <el-button 
                :type="activeTab === 'log' ? 'primary' : ''"
                size="small"
                @click="activeTab = 'log'"
              >
                <el-icon><Document /></el-icon>
                日志
              </el-button>
              <el-button 
                :type="activeTab === 'map' ? 'primary' : ''"
                size="small"
                @click="activeTab = 'map'"
              >
                <el-icon><Location /></el-icon>
                地图
              </el-button>
              <el-button 
                :type="activeTab === 'stats' ? 'primary' : ''"
                size="small"
                @click="activeTab = 'stats'"
              >
                <el-icon><DataAnalysis /></el-icon>
                统计
              </el-button>
            </el-button-group>
          </div>
        </div>
      </template>

      <!-- 日志内容 -->
      <div v-if="activeTab === 'log'" class="log-content">
        <div class="log-entries">
          <div 
            v-for="entry in logEntries" 
            :key="entry.id"
            class="log-entry"
            :class="entry.type"
          >
            <div class="entry-header">
              <span class="entry-time">{{ formatTime(entry.timestamp) }}</span>
              <el-tag :type="getEntryTagType(entry.type)" size="small">
                {{ getEntryTypeText(entry.type) }}
              </el-tag>
            </div>
            <div class="entry-content">
              <h4 v-if="entry.title">{{ entry.title }}</h4>
              <p>{{ entry.content }}</p>
              <div v-if="entry.effects" class="entry-effects">
                <span 
                  v-for="effect in entry.effects" 
                  :key="effect.type"
                  class="effect-item"
                  :class="effect.value > 0 ? 'positive' : 'negative'"
                >
                  {{ effect.type }}: {{ effect.value > 0 ? '+' : '' }}{{ effect.value }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="logEntries.length === 0" class="empty-log">
          <el-icon><Document /></el-icon>
          <p>还没有任何航海记录</p>
          <p class="hint">开始你的冒险，记录将自动添加到这里</p>
        </div>
      </div>

      <!-- 地图内容 -->
      <div v-if="activeTab === 'map'" class="map-content">
        <NavigationMap />
      </div>

      <!-- 统计内容 -->
      <div v-if="activeTab === 'stats'" class="stats-content">
        <div class="stats-grid">
          <div class="stat-card">
            <h4>探索统计</h4>
            <div class="stat-item">
              <span>已探索区域</span>
              <span class="stat-value">{{ exploredAreas }}/{{ totalAreas }}</span>
            </div>
            <div class="stat-item">
              <span>航行距离</span>
              <span class="stat-value">{{ travelDistance }} 海里</span>
            </div>
            <div class="stat-item">
              <span>遭遇事件</span>
              <span class="stat-value">{{ encounterCount }} 次</span>
            </div>
          </div>
          
          <div class="stat-card">
            <h4>战斗统计</h4>
            <div class="stat-item">
              <span>战斗胜利</span>
              <span class="stat-value">{{ battleWins }}</span>
            </div>
            <div class="stat-item">
              <span>怪物击败</span>
              <span class="stat-value">{{ monstersDefeated }}</span>
            </div>
            <div class="stat-item">
              <span>理智损失</span>
              <span class="stat-value negative">-{{ sanityLost }}</span>
            </div>
          </div>
          
          <div class="stat-card">
            <h4>生存统计</h4>
            <div class="stat-item">
              <span>存活天数</span>
              <span class="stat-value">{{ survivalDays }} 天</span>
            </div>
            <div class="stat-item">
              <span>获得经验</span>
              <span class="stat-value positive">+{{ totalExperience }}</span>
            </div>
            <div class="stat-item">
              <span>获得金币</span>
              <span class="stat-value positive">+{{ totalGold }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import NavigationMap from './NavigationMap.vue'

const gameStore = useGameStore()
const activeTab = ref('log')

// 日志条目
const logEntries = ref([
  {
    id: 1,
    timestamp: new Date(Date.now() - 3600000),
    type: 'story',
    title: '神秘的觉醒',
    content: '你在一艘陌生的船上苏醒，身体的疾病和残缺都已完全治愈...',
    effects: [
      { type: '经验', value: 10 }
    ]
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 1800000),
    type: 'choice',
    title: '选择了解游戏规则',
    content: '你打开了航海日志，了解了这个世界的基本规则。',
    effects: [
      { type: '经验', value: 20 }
    ]
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 900000),
    type: 'battle',
    title: '遭遇溺亡者',
    content: '在东方小岛的夜晚，你遭遇了恐怖的溺亡者，经过激烈战斗后获得胜利。',
    effects: [
      { type: '理智', value: -15 },
      { type: '经验', value: 50 },
      { type: '生命', value: -20 }
    ]
  }
])

// 统计数据
const exploredAreas = computed(() => 2)
const totalAreas = computed(() => 5)
const travelDistance = computed(() => 45)
const encounterCount = computed(() => 3)
const battleWins = computed(() => 1)
const monstersDefeated = computed(() => 2)
const sanityLost = computed(() => 35)
const survivalDays = computed(() => 1)
const totalExperience = computed(() => gameStore.player?.experience || 0)
const totalGold = computed(() => gameStore.player?.gold || 0)

// 格式化时间
const formatTime = (timestamp) => {
  return new Intl.DateTimeFormat('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(timestamp)
}

// 获取条目标签类型
const getEntryTagType = (type) => {
  switch (type) {
    case 'story': return 'primary'
    case 'choice': return 'success'
    case 'battle': return 'danger'
    case 'discovery': return 'warning'
    default: return 'info'
  }
}

// 获取条目类型文本
const getEntryTypeText = (type) => {
  switch (type) {
    case 'story': return '故事'
    case 'choice': return '选择'
    case 'battle': return '战斗'
    case 'discovery': return '发现'
    default: return '事件'
  }
}

// 添加日志条目
const addLogEntry = (entry) => {
  logEntries.value.unshift({
    id: Date.now(),
    timestamp: new Date(),
    ...entry
  })
}

// 暴露方法给父组件
defineExpose({
  addLogEntry
})

onMounted(() => {
  // 可以从游戏状态加载日志
})
</script>

<style lang="scss" scoped>
.navigation-log {
  height: 100%;
}

.log-card {
  height: 100%;
  background: rgba(0, 20, 40, 0.95);
  border: 1px solid #66ffcc;

  :deep(.el-card__header) {
    background: rgba(0, 40, 80, 0.8);
    border-bottom: 1px solid #66ffcc;
    padding: 12px 16px;
    min-height: 48px;
  }

  :deep(.el-card__body) {
    height: calc(100% - 48px);
    overflow: hidden;
    padding: 0;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #66ffcc;
  
  span {
    font-weight: bold;
    margin-left: 8px;
  }
}

.log-content, .map-content, .stats-content {
  height: 100%;
  overflow-y: auto;
  padding: 16px;
}

.log-content {
  max-height: calc(100vh - 200px);
}

.log-entries {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: calc(100vh - 280px);
  overflow-y: auto;
  padding-right: 8px;

  /* 自定义滚动条 */
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(0, 40, 80, 0.3);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: #66ffcc;
    border-radius: 3px;

    &:hover {
      background: #FFD700;
    }
  }
}

.log-entry {
  padding: 1rem;
  background: rgba(0, 40, 80, 0.6);
  border-radius: 8px;
  border-left: 4px solid #66ffcc;
  margin-bottom: 1rem;
  
  &.battle {
    border-left-color: #F56C6C;
  }
  
  &.choice {
    border-left-color: #67C23A;
  }
  
  &.discovery {
    border-left-color: #E6A23C;
  }
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.entry-time {
  font-size: 12px;
  color: #999;
}

.entry-content {
  h4 {
    margin: 0 0 0.5rem 0;
    color: #66ffcc;
  }
  
  p {
    margin: 0 0 0.5rem 0;
    color: #ccc;
    line-height: 1.5;
  }
}

.entry-effects {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.effect-item {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  
  &.positive {
    background: rgba(103, 194, 58, 0.2);
    color: #67C23A;
  }
  
  &.negative {
    background: rgba(245, 108, 108, 0.2);
    color: #F56C6C;
  }
}

.empty-log {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
  
  .el-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  
  .hint {
    font-size: 14px;
    margin-top: 0.5rem;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: rgba(0, 40, 80, 0.6);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #66ffcc;
  
  h4 {
    margin: 0 0 1rem 0;
    color: #66ffcc;
    text-align: center;
  }
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #ccc;
  
  .stat-value {
    font-weight: bold;
    
    &.positive {
      color: #67C23A;
    }
    
    &.negative {
      color: #F56C6C;
    }
  }
}
</style>
