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
            <el-button size="small" @click="openPanel('inventory')">
              <el-icon><Box /></el-icon>
              物品
            </el-button>
            <el-button size="small" @click="openPanel('gachapon')">
              🎰 扭蛋机
            </el-button>
            <el-button size="small" @click="openPanel('talents')">
              ✨ 天赋
            </el-button>
            <el-button size="small" @click="openPanel('capture')" v-if="showCaptureButton">
              🚢 占领
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

        <!-- 玩家状态、航海日志和船员对话切换 -->
        <div class="status-card">
          <div class="status-header">
            <div class="tab-buttons">
              <button
                :class="['tab-btn', { active: activeStatusTab === 'status' }]"
                @click="activeStatusTab = 'status'"
              >
                🧭 船长状态
              </button>
              <button
                :class="['tab-btn', { active: activeStatusTab === 'log' }]"
                @click="activeStatusTab = 'log'"
              >
                📖 航海日志
                <span v-if="newLogEntries > 0" class="log-badge">{{ newLogEntries }}</span>
              </button>
              <button
                :class="['tab-btn', { active: activeStatusTab === 'chat' }]"
                @click="activeStatusTab = 'chat'"
              >
                💬 船员对话
                <span v-if="newChatMessages > 0" class="chat-badge">{{ newChatMessages }}</span>
              </button>
            </div>
          </div>

          <div class="status-content">
            <ComprehensiveStatus v-if="activeStatusTab === 'status'" />
            <NavigationLog
              v-else-if="activeStatusTab === 'log'"
              ref="navigationLogRef"
              :compact="true"
              @entries-read="newLogEntries = 0"
            />
            <ChatPanel
              v-else-if="activeStatusTab === 'chat'"
              ref="chatPanelRef"
              @messages-read="newChatMessages = 0"
            />
          </div>
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
      <div v-if="activePanel === 'map'" class="map-panel">
        <h3>🗺️ 海域地图</h3>
        <p>地图功能开发中...</p>
      </div>
      <div v-else-if="activePanel === 'inventory'" class="inventory-panel">
        <h3>📦 物品清单</h3>
        <p>物品系统开发中...</p>
      </div>
      <div v-else-if="activePanel === 'gachapon'" class="gachapon-panel">
        <MonsterGachapon />
      </div>
      <div v-else-if="activePanel === 'talents'" class="talents-panel">
        <TalentSystem />
      </div>
      <div v-else-if="activePanel === 'capture'" class="capture-panel">
        <ShipCapture
          :target-ship="captureTargetShip"
          @capture-complete="handleCaptureComplete"
          @dismantle-complete="handleDismantleComplete"
          @cancel="closeCapturePanel"
        />
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
import MonsterGachapon from './MonsterGachapon.vue'
import TalentSystem from './TalentSystem.vue'
import ShipCapture from './ShipCapture.vue'

const gameStore = useGameStore()

// 响应式数据
const showCabin = ref(false)
const drawerVisible = ref(false)
const activePanel = ref('')
const activeStatusTab = ref('status') // 状态面板切换
const newLogEntries = ref(0) // 新日志条目计数
const newChatMessages = ref(0) // 新聊天消息计数
const showCaptureButton = ref(false)
const captureTargetShip = ref(null)
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
    inventory: '📦 物品清单',
    gachapon: '🎰 怪物扭蛋机',
    talents: '✨ 神秘天赋',
    capture: '🚢 船只占领'
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

    // 增加新聊天消息计数
    if (activeStatusTab.value !== 'chat') {
      newChatMessages.value++
    }
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

    // 增加新日志条目计数
    if (activeStatusTab.value !== 'log') {
      newLogEntries.value++
    }

    // 自动切换到航海日志（延迟一点时间让用户看到选择结果）
    setTimeout(() => {
      activeStatusTab.value = 'log'
    }, 500)
  }
}

// 船只占领相关方法
const handleCaptureComplete = (data) => {
  ElMessage.success(`成功占领了${data.ship.name}！`)
  showCaptureButton.value = false
  captureTargetShip.value = null
  drawerVisible.value = false
}

const handleDismantleComplete = (data) => {
  ElMessage.success(`成功分解了${data.ship.name}，获得了大量资源！`)
  showCaptureButton.value = false
  captureTargetShip.value = null
  drawerVisible.value = false
}

const closeCapturePanel = () => {
  showCaptureButton.value = false
  captureTargetShip.value = null
  drawerVisible.value = false
}

// 模拟发现敌方船只
const discoverEnemyShip = () => {
  captureTargetShip.value = {
    name: '海盗号',
    type: 'pirate',
    level: 1,
    durability: 800,
    maxDurability: 1000,
    capacity: 800,
    speed: 45,
    usedCapacity: 200,
    flag: '🏴‍☠️',
    abilities: [
      {
        id: 'extra_hooks',
        name: '额外爪钩',
        icon: '🪝',
        description: '左右两侧各有两个爪钩，可以抓取物体或其他船只'
      },
      {
        id: 'pirate_assault',
        name: '海盗强袭',
        icon: '⚡',
        description: '航速提高25%，持续15分钟'
      }
    ],
    cargo: [
      { id: 'wood', name: '木料', icon: '🪵', amount: 125, quality: 'common' },
      { id: 'cloth', name: '布料', icon: '🧵', amount: 98, quality: 'common' },
      { id: 'bread', name: '黑面包', icon: '🍞', amount: 2, quality: 'common' },
      { id: 'water', name: '淡水', icon: '💧', amount: 5, quality: 'common' }
    ]
  }
  showCaptureButton.value = true
  ElMessage.info('发现了一艘无主船只！')
}

// 暴露方法给父组件
defineExpose({
  toggleCabin,
  openPanel,
  discoverEnemyShip
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
  grid-template-columns: 2.5fr 1fr; // 调整比例，给右侧更多空间
  gap: 0.75rem; // 减少间距
  padding: 0.75rem; // 减少内边距
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
  gap: 0.5rem; // 进一步减少间距
  overflow-y: auto;
  min-height: 0;
}

.status-card, .environment-card, .ship-card, .chat-card {
  background: rgba(0, 20, 40, 0.9);
  border: 1px solid #66ffcc;
  border-radius: 6px;
  padding: 0.5rem; // 进一步减少内边距
  backdrop-filter: blur(10px);

  h3 {
    margin: 0 0 0.4rem 0; // 减少标题间距
    color: #66ffcc;
    font-size: 0.8rem; // 进一步减小字体
    border-bottom: 1px solid rgba(102, 255, 204, 0.3);
    padding-bottom: 0.2rem;
  }
}

// 状态面板标签样式
.status-header {
  margin-bottom: 0.5rem;
}

.tab-buttons {
  display: flex;
  gap: 2px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  padding: 2px;
}

.tab-btn {
  flex: 1;
  background: transparent;
  border: none;
  color: #66ffcc;
  padding: 0.4rem 0.6rem;
  border-radius: 3px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;

  &:hover {
    background: rgba(102, 255, 204, 0.1);
  }

  &.active {
    background: rgba(102, 255, 204, 0.2);
    color: #fff;
    box-shadow: 0 0 8px rgba(102, 255, 204, 0.3);
  }
}

.log-badge, .chat-badge {
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.2rem;
  animation: pulse-badge 2s infinite;
}

.chat-badge {
  background: #2ed573; // 聊天徽章用绿色区分
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.status-content {
  min-height: 200px; // 确保内容区域有足够高度
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

// 响应式布局
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 2fr 1fr; // 中等屏幕调整比例
  }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr; // 移动端单列布局
    grid-template-rows: 1fr auto;
    gap: 0.5rem;
    padding: 0.5rem;
  }

  .info-panel {
    max-height: 40vh; // 限制右侧面板高度
    gap: 0.4rem;
  }

  .status-card, .environment-card, .ship-card, .chat-card {
    padding: 0.4rem;

    h3 {
      font-size: 0.75rem;
      margin-bottom: 0.3rem;
    }
  }

  .quick-actions {
    padding: 0.4rem;

    .el-button-group .el-button {
      font-size: 0.75rem;
      padding: 0.3rem 0.6rem;
    }
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 0.3rem;
    gap: 0.3rem;
  }

  .info-panel {
    max-height: 35vh;
  }

  .quick-actions .el-button-group {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.3rem;

    .el-button {
      margin: 0;
      border-radius: 4px;
    }
  }
}
</style>
