<template>
  <div class="text-adventure-layout">
    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧：故事和交互区域 -->
      <div class="story-section">
        <!-- 故事显示区 -->
        <div class="story-display">
          <StoryDisplay @choice-made="handleChoiceMade" />
        </div>
        
        <!-- 快速操作栏 -->
        <div class="quick-actions">
          <el-button-group>
            <el-button size="small" @click="openPanel('map')">
              <el-icon><Location /></el-icon>
              海图
            </el-button>
            <el-button size="small" @click="openPanel('log')">
              <el-icon><Notebook /></el-icon>
              日志
            </el-button>
            <el-button size="small" @click="openPanel('inventory')">
              <el-icon><Box /></el-icon>
              物品
            </el-button>
            <el-button size="small" @click="toggleCabin">
              <el-icon><House /></el-icon>
              {{ showCabin ? '隐藏' : '显示' }}船舱
            </el-button>
          </el-button-group>
        </div>
      </div>

      <!-- 右侧：状态和信息面板 -->
      <div class="info-panel">
        <!-- 玩家状态 -->
        <div class="status-card">
          <h3>🧭 船长状态</h3>
          <ComprehensiveStatus />
        </div>

        <!-- 环境信息 -->
        <div class="environment-card">
          <h3>🌊 环境状况</h3>
          <div class="env-grid">
            <div class="env-item">
              <span class="label">天气:</span>
              <span class="value">{{ weatherInfo.label }}</span>
            </div>
            <div class="env-item">
              <span class="label">海况:</span>
              <span class="value">{{ seaCondition }}</span>
            </div>
            <div class="env-item">
              <span class="label">时间:</span>
              <span class="value">{{ timeInfo.label }}</span>
            </div>
            <div class="env-item">
              <span class="label">位置:</span>
              <span class="value">{{ currentLocation }}</span>
            </div>
          </div>
        </div>

        <!-- 船舶信息 -->
        <div class="ship-card">
          <h3>⚓ 船舶状态</h3>
          <div class="ship-stats">
            <div class="stat-item">
              <div class="stat-label">船体完整度</div>
              <el-progress 
                :percentage="shipCondition.hull" 
                :color="getConditionColor(shipCondition.hull)"
                :show-text="false"
                size="small"
              />
              <span class="stat-value">{{ shipCondition.hull }}%</span>
            </div>
            <div class="stat-item">
              <div class="stat-label">帆布状况</div>
              <el-progress 
                :percentage="shipCondition.sails" 
                :color="getConditionColor(shipCondition.sails)"
                :show-text="false"
                size="small"
              />
              <span class="stat-value">{{ shipCondition.sails }}%</span>
            </div>
            <div class="stat-item">
              <div class="stat-label">淡水储量</div>
              <el-progress 
                :percentage="shipCondition.water" 
                color="#4fc3f7"
                :show-text="false"
                size="small"
              />
              <span class="stat-value">{{ shipCondition.water }}%</span>
            </div>
            <div class="stat-item">
              <div class="stat-label">食物储量</div>
              <el-progress 
                :percentage="shipCondition.food" 
                color="#81c784"
                :show-text="false"
                size="small"
              />
              <span class="stat-value">{{ shipCondition.food }}%</span>
            </div>
          </div>
        </div>

        <!-- 聊天面板 -->
        <div class="chat-card">
          <h3>💬 船员对话</h3>
          <ChatPanel ref="chatPanelRef" />
        </div>
      </div>
    </div>

    <!-- 船舱背景（简化版本） -->
    <div v-if="showCabin" class="cabin-background">
      <div class="simple-cabin-bg">
        <div class="cabin-texture"></div>
        <div class="cabin-atmosphere"></div>
      </div>
    </div>

    <!-- 浮动面板 -->
    <el-drawer
      v-model="drawerVisible"
      :title="drawerTitle"
      direction="rtl"
      size="40%"
    >
      <NavigationLog v-if="activePanel === 'log'" ref="navigationLogRef" />
      <div v-else-if="activePanel === 'map'" class="map-panel">
        <h3>🗺️ 海域地图</h3>
        <p>地图功能开发中...</p>
      </div>
      <div v-else-if="activePanel === 'inventory'" class="inventory-panel">
        <h3>📦 物品清单</h3>
        <p>物品系统开发中...</p>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
import { Location, Notebook, Box, House } from '@element-plus/icons-vue'
import StoryDisplay from './StoryDisplay.vue'
import ComprehensiveStatus from './ComprehensiveStatus.vue'
import ChatPanel from './ChatPanel.vue'
import NavigationLog from './NavigationLog.vue'

const gameStore = useGameStore()

// 响应式数据
const showCabin = ref(false)
const drawerVisible = ref(false)
const activePanel = ref('')
const chatPanelRef = ref(null)
const navigationLogRef = ref(null)

// 计算属性
const weatherInfo = computed(() => ({
  label: '🌅 平静',
  condition: 'calm'
}))

const timeInfo = computed(() => ({
  label: '☀️ 白天',
  time: 'day'
}))

const seaCondition = computed(() => '风平浪静')
const currentLocation = computed(() => '未知海域')

const shipCondition = ref({
  hull: 85,
  sails: 92,
  water: 67,
  food: 43
})

const drawerTitle = computed(() => {
  const titles = {
    map: '🗺️ 海域地图',
    log: '📖 航海日志',
    inventory: '📦 物品清单'
  }
  return titles[activePanel.value] || ''
})

// 方法
const toggleCabin = () => {
  showCabin.value = !showCabin.value
}

const openPanel = (panel) => {
  activePanel.value = panel
  drawerVisible.value = true
}

const getConditionColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 50) return '#e6a23c'
  return '#f56c6c'
}

const handleChoiceMade = (choiceData) => {
  // 记录到聊天面板
  if (chatPanelRef.value && chatPanelRef.value.recordPlayerChoice) {
    chatPanelRef.value.recordPlayerChoice(choiceData.choice, choiceData.storyTitle)
  }

  // 记录到航海日志
  if (navigationLogRef.value && navigationLogRef.value.addLogEntry) {
    navigationLogRef.value.addLogEntry({
      type: 'choice',
      title: `选择：${choiceData.choice.text}`,
      content: choiceData.storyTitle,
      timestamp: new Date(),
      rewards: [
        ...(choiceData.choice.goldReward > 0 ? [{ type: '金币', value: choiceData.choice.goldReward }] : []),
        ...(choiceData.choice.experienceReward > 0 ? [{ type: '经验', value: choiceData.choice.experienceReward }] : [])
      ]
    })
  }
}

// 暴露方法给父组件
defineExpose({
  toggleCabin,
  openPanel
})
</script>

<style lang="scss" scoped>
.text-adventure-layout {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 3fr 1fr; // 增加故事区域比例
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;
}

.story-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 0;
}

.story-display {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.quick-actions {
  flex-shrink: 0;
  padding: 0.5rem;
  background: rgba(0, 20, 40, 0.8);
  border: 1px solid #66ffcc;
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.info-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem; // 减少间距
  overflow-y: auto;
  min-height: 0;
}

.status-card, .environment-card, .ship-card, .chat-card {
  background: rgba(0, 20, 40, 0.9);
  border: 1px solid #66ffcc;
  border-radius: 6px;
  padding: 0.75rem; // 减少内边距
  backdrop-filter: blur(10px);

  h3 {
    margin: 0 0 0.5rem 0; // 减少标题间距
    color: #66ffcc;
    font-size: 0.85rem; // 稍微减小字体
    border-bottom: 1px solid rgba(102, 255, 204, 0.3);
    padding-bottom: 0.2rem;
  }
}

.env-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.env-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  
  .label {
    color: #ccc;
  }
  
  .value {
    color: #FFD700;
    font-weight: bold;
  }
}

.ship-stats {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  .stat-label {
    flex: 0 0 80px;
    font-size: 0.8rem;
    color: #ccc;
  }
  
  .el-progress {
    flex: 1;
  }
  
  .stat-value {
    flex: 0 0 40px;
    font-size: 0.8rem;
    color: #FFD700;
    text-align: right;
  }
}

.chat-card {
  flex: 1;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  
  :deep(.chat-panel) {
    flex: 1;
    min-height: 0;
  }
}

.cabin-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  opacity: 0.05;
  pointer-events: none;

  .simple-cabin-bg {
    width: 100%;
    height: 100%;
    position: relative;
    background: linear-gradient(
      135deg,
      rgba(139, 69, 19, 0.1) 0%,
      rgba(160, 82, 45, 0.1) 50%,
      rgba(101, 67, 33, 0.1) 100%
    );

    .cabin-texture {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: repeating-linear-gradient(
        90deg,
        transparent 0px,
        rgba(139, 69, 19, 0.05) 2px,
        transparent 4px
      );
    }

    .cabin-atmosphere {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(
        ellipse at center,
        rgba(102, 255, 204, 0.02) 0%,
        transparent 70%
      );
    }
  }
}

.map-panel, .inventory-panel {
  padding: 1rem;
  color: #ccc;
  
  h3 {
    color: #66ffcc;
    margin-bottom: 1rem;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto;
  }
  
  .info-panel {
    max-height: 40vh;
  }
  
  .quick-actions {
    :deep(.el-button-group) {
      display: flex;
      flex-wrap: wrap;
      gap: 0.25rem;
      
      .el-button {
        flex: 1;
        min-width: 0;
      }
    }
  }
}

// 自定义滚动条
.info-panel::-webkit-scrollbar {
  width: 6px;
}

.info-panel::-webkit-scrollbar-track {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 3px;
}

.info-panel::-webkit-scrollbar-thumb {
  background: #66ffcc;
  border-radius: 3px;
  
  &:hover {
    background: #FFD700;
  }
}
</style>
