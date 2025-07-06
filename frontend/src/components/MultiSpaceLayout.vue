<template>
  <div class="multi-space-layout">
    <!-- 顶部导航栏 -->
    <div class="top-navigation">
      <div class="nav-left">
        <div class="player-avatar">
          <div class="avatar-image">🧙‍♂️</div>
          <div class="player-level">Lv.{{ playerLevel }}</div>
        </div>
        <div class="player-basic-info">
          <div class="player-name">{{ playerName }}</div>
          <div class="ship-name">{{ shipName }}</div>
        </div>
      </div>
      
      <div class="nav-center">
        <div class="quick-stats">
          <div class="stat-item health">
            <span class="stat-icon">❤️</span>
            <span class="stat-value">{{ playerStats.health }}/{{ playerStats.maxHealth }}</span>
          </div>
          <div class="stat-item sanity">
            <span class="stat-icon">🧠</span>
            <span class="stat-value">{{ playerStats.sanity }}/{{ playerStats.maxSanity }}</span>
          </div>
          <div class="stat-item energy">
            <span class="stat-icon">⚡</span>
            <span class="stat-value">{{ playerStats.energy }}/{{ playerStats.maxEnergy }}</span>
          </div>
        </div>
      </div>
      
      <div class="nav-right">
        <div class="resource-display">
          <div class="resource-item">
            <span class="resource-icon">🪙</span>
            <span class="resource-amount">{{ resources.gold }}</span>
          </div>
          <div class="resource-item">
            <span class="resource-icon">🪵</span>
            <span class="resource-amount">{{ resources.wood }}</span>
          </div>
          <div class="resource-item">
            <span class="resource-icon">🧵</span>
            <span class="resource-amount">{{ resources.cloth }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧功能面板 -->
      <div class="left-panel" :class="{ 'collapsed': leftPanelCollapsed }">
        <div class="panel-toggle" @click="toggleLeftPanel">
          <span>{{ leftPanelCollapsed ? '→' : '←' }}</span>
        </div>
        
        <div class="function-tabs" v-if="!leftPanelCollapsed">
          <div 
            v-for="tab in leftTabs" 
            :key="tab.id"
            class="tab-item"
            :class="{ 'active': activeLeftTab === tab.id }"
            @click="switchLeftTab(tab.id)"
          >
            <div class="tab-icon">{{ tab.icon }}</div>
            <div class="tab-label">{{ tab.label }}</div>
            <div class="tab-badge" v-if="tab.badge">{{ tab.badge }}</div>
          </div>
        </div>
        
        <div class="panel-content" v-if="!leftPanelCollapsed">
          <component :is="getLeftComponent()" />
        </div>
      </div>
      
      <!-- 中央游戏区域 -->
      <div class="center-area">
        <!-- 游戏主视图 -->
        <div class="game-viewport">
          <component :is="getCurrentGameView()" />
        </div>
        
        <!-- 底部快捷操作栏 -->
        <div class="bottom-toolbar">
          <div class="toolbar-section">
            <button 
              v-for="action in quickActions" 
              :key="action.id"
              @click="executeQuickAction(action)"
              :disabled="action.disabled"
              class="quick-action-btn"
            >
              {{ action.icon }} {{ action.label }}
            </button>
          </div>
          
          <div class="view-switcher">
            <select v-model="currentView" @change="switchView">
              <option v-for="option in viewOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- 右侧信息面板 -->
      <div class="right-panel" :class="{ 'collapsed': rightPanelCollapsed }">
        <div class="panel-toggle" @click="toggleRightPanel">
          <span>{{ rightPanelCollapsed ? '←' : '→' }}</span>
        </div>
        
        <div class="info-tabs" v-if="!rightPanelCollapsed">
          <div class="tab-headers">
            <div 
              v-for="tab in rightTabs" 
              :key="tab.id"
              class="tab-header"
              :class="{ 'active': activeRightTab === tab.id }"
              @click="activeRightTab = tab.id"
            >
              <span class="tab-icon">{{ tab.icon }}</span>
              <span class="tab-text">{{ tab.label }}</span>
              <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
            </div>
          </div>
          
          <div class="right-panel-content">
            <component :is="getRightComponent(activeRightTab)" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 导入组件
import StoryEngine from './StoryEngine.vue'
import ShipCabin from './ShipCabin.vue'

// 响应式数据
const leftPanelCollapsed = ref(false)
const rightPanelCollapsed = ref(false)
const activeLeftTab = ref('exploration')
const activeRightTab = ref('status')
const currentView = ref('story')

// 玩家信息
const playerName = ref('杨逸')
const shipName = ref('梦魇号')
const playerLevel = ref(5)

const playerStats = ref({
  health: 76,
  maxHealth: 100,
  sanity: 93,
  maxSanity: 100,
  energy: 35,
  maxEnergy: 100
})

const resources = ref({
  gold: 500,
  wood: 125,
  cloth: 98
})

// 左侧功能标签
const leftTabs = ref([
  { id: 'exploration', icon: '🏝️', label: '探索', badge: null },
  { id: 'astrology', icon: '🔮', label: '占星', badge: null },
  { id: 'gachapon', icon: '🎰', label: '扭蛋', badge: null },
  { id: 'talents', icon: '✨', label: '天赋', badge: 1 },
  { id: 'trading', icon: '🏪', label: '交易', badge: 3 },
  { id: 'combat', icon: '⚔️', label: '战斗', badge: null }
])

// 右侧信息标签
const rightTabs = ref([
  { id: 'status', icon: '📊', label: '状态', badge: null },
  { id: 'log', icon: '📜', label: '日志', badge: 5 },
  { id: 'chat', icon: '💬', label: '聊天', badge: 2 }
])

// 视图选项
const viewOptions = ref([
  { label: '剧情', value: 'story' },
  { label: '船舱', value: 'cabin' },
  { label: '探索', value: 'exploration' },
  { label: '占星', value: 'astrology' },
  { label: '风暴', value: 'storm' }
])

// 快捷操作
const quickActions = ref([
  { id: 'fishing', icon: '🎣', label: '钓鱼', disabled: false },
  { id: 'rest', icon: '😴', label: '休息', disabled: false },
  { id: 'sail', icon: '⛵', label: '航行', disabled: false },
  { id: 'anchor', icon: '⚓', label: '抛锚', disabled: false }
])

// 方法
const toggleLeftPanel = () => {
  leftPanelCollapsed.value = !leftPanelCollapsed.value
}

const toggleRightPanel = () => {
  rightPanelCollapsed.value = !rightPanelCollapsed.value
}

const switchLeftTab = (tabId) => {
  activeLeftTab.value = tabId
}

const switchView = () => {
  // 视图切换逻辑
}

const getLeftComponent = () => {
  // 返回一个简单的占位组件
  return { template: '<div class="placeholder">功能开发中...</div>' }
}

const getCurrentGameView = () => {
  const components = {
    story: StoryEngine,
    cabin: ShipCabin,
    exploration: { template: '<div class="placeholder">探索功能开发中...</div>' },
    astrology: { template: '<div class="placeholder">占星功能开发中...</div>' },
    storm: { template: '<div class="placeholder">风暴功能开发中...</div>' }
  }
  return components[currentView.value] || StoryEngine
}

const getRightComponent = (tabId) => {
  // 返回简单的占位组件
  const components = {
    status: { template: '<div class="placeholder">状态面板开发中...</div>' },
    log: { template: '<div class="placeholder">日志面板开发中...</div>' },
    chat: { template: '<div class="placeholder">聊天面板开发中...</div>' }
  }
  return components[tabId] || components.status
}

const executeQuickAction = (action) => {
  console.log('执行快捷操作:', action.id)
}
</script>

<style lang="scss" scoped>
.multi-space-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a1a2a 0%, #1a2a3a 100%);
  color: #ffffff;
}

.top-navigation {
  height: 80px;
  background: rgba(0, 20, 40, 0.9);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  border-bottom: 2px solid #66ffcc;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.player-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .avatar-image {
    font-size: 2rem;
  }
  
  .player-level {
    font-size: 0.8rem;
    color: #66ffcc;
  }
}

.quick-stats {
  display: flex;
  gap: 2rem;
  
  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    
    .stat-icon {
      font-size: 1.2rem;
    }
  }
}

.resource-display {
  display: flex;
  gap: 1rem;
  
  .resource-item {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(102, 255, 204, 0.1);
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
  }
}

.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 250px 1fr 300px;
  gap: 1rem;
  padding: 1rem;
}

.left-panel, .right-panel {
  background: rgba(0, 30, 50, 0.8);
  border-radius: 10px;
  position: relative;
  
  &.collapsed {
    width: 50px;
  }
}

.panel-toggle {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #66ffcc;
  color: #000;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
}

.center-area {
  background: rgba(0, 20, 40, 0.8);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.game-viewport {
  flex: 1;
  padding: 1rem;
}

.bottom-toolbar {
  height: 60px;
  background: rgba(0, 10, 20, 0.9);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  border-top: 1px solid #66ffcc;
}

.quick-action-btn {
  background: rgba(102, 255, 204, 0.1);
  border: 1px solid #66ffcc;
  color: #66ffcc;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 0.5rem;
  
  &:hover {
    background: rgba(102, 255, 204, 0.2);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.placeholder {
  padding: 2rem;
  text-align: center;
  color: #66ffcc;
  font-style: italic;
}

.function-tabs, .tab-headers {
  padding: 1rem;
}

.tab-item, .tab-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem;
  margin-bottom: 0.5rem;
  background: rgba(102, 255, 204, 0.1);
  border-radius: 5px;
  cursor: pointer;
  
  &.active {
    background: rgba(102, 255, 204, 0.3);
    border-left: 3px solid #66ffcc;
  }
  
  &:hover {
    background: rgba(102, 255, 204, 0.2);
  }
}

.right-panel-content {
  padding: 1rem;
  height: calc(100% - 200px);
  overflow-y: auto;
}
</style>
