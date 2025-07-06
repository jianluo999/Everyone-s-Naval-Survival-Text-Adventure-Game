<template>
  <div class="clean-game-layout">
    <!-- 顶部状态栏 -->
    <div class="top-status-bar">
      <div class="player-info">
        <div class="avatar">🧙‍♂️</div>
        <div class="basic-info">
          <div class="player-name">杨逸</div>
          <div class="ship-name">梦魇号</div>
        </div>
      </div>
      
      <div class="vital-stats">
        <div class="stat-item health">
          <span class="icon">❤️</span>
          <span class="value">76/100</span>
        </div>
        <div class="stat-item sanity">
          <span class="icon">🧠</span>
          <span class="value">93/100</span>
        </div>
        <div class="stat-item energy">
          <span class="icon">⚡</span>
          <span class="value">35/100</span>
        </div>
      </div>
      
      <div class="resources">
        <div class="resource-item">
          <span class="icon">🪙</span>
          <span class="amount">500</span>
        </div>
        <div class="resource-item">
          <span class="icon">🪵</span>
          <span class="amount">125</span>
        </div>
        <div class="resource-item">
          <span class="icon">🧵</span>
          <span class="amount">98</span>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="main-content-area">
      <!-- 左侧隐藏侧边栏 -->
      <div 
        class="left-sidebar"
        :class="{ 'expanded': sidebarExpanded }"
        @mouseenter="expandSidebar"
        @mouseleave="collapseSidebar"
      >
        <div class="sidebar-trigger">
          <div class="trigger-icon">⚙️</div>
        </div>
        
        <div class="sidebar-content" v-show="sidebarExpanded">
          <div class="sidebar-header">
            <h3>功能菜单</h3>
          </div>
          
          <div class="function-menu">
            <div 
              v-for="func in secondaryFunctions" 
              :key="func.id"
              class="menu-item"
              :class="{ 'active': activeFunction === func.id }"
              @click="selectFunction(func.id)"
            >
              <div class="item-icon">{{ func.icon }}</div>
              <div class="item-label">{{ func.label }}</div>
              <div class="item-badge" v-if="func.badge">{{ func.badge }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 中央游戏区域 -->
      <div class="center-game-area">
        <!-- 主要游戏视图 -->
        <div class="game-viewport">
          <component :is="getCurrentComponent()" />
        </div>
        
        <!-- 底部快捷操作 -->
        <div class="quick-actions">
          <el-button-group>
            <el-button 
              v-for="action in quickActions" 
              :key="action.id"
              :type="action.type"
              @click="executeAction(action)"
              :disabled="action.disabled"
            >
              {{ action.icon }} {{ action.label }}
            </el-button>
          </el-button-group>
        </div>
      </div>
      
      <!-- 右侧信息面板 -->
      <div class="right-info-panel">
        <el-tabs v-model="activeInfoTab" tab-position="right">
          <el-tab-pane 
            v-for="tab in infoPanelTabs" 
            :key="tab.id"
            :label="tab.label" 
            :name="tab.id"
          >
            <template #label>
              <div class="info-tab-label">
                <span class="tab-icon">{{ tab.icon }}</span>
                <el-badge v-if="tab.badge" :value="tab.badge" />
              </div>
            </template>
            
            <div class="info-content">
              <component :is="getInfoComponent(tab.id)" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
    
    <!-- 功能面板弹窗 -->
    <el-drawer
      v-model="functionDrawerVisible"
      :title="selectedFunctionTitle"
      direction="ltr"
      size="400px"
      class="function-drawer"
    >
      <component :is="getSelectedFunctionComponent()" />
    </el-drawer>
    
    <!-- 通知系统 -->
    <div class="notification-area">
      <transition-group name="notification" tag="div">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          class="notification-item"
          :class="notification.type"
        >
          <span class="notification-icon">{{ notification.icon }}</span>
          <span class="notification-text">{{ notification.message }}</span>
          <span class="notification-close" @click="dismissNotification(notification.id)">×</span>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 导入核心组件
import StoryEngine from './StoryEngine.vue'
import ComprehensiveStatus from './ComprehensiveStatus.vue'
import NavigationLog from './NavigationLog.vue'
import ChatPanel from './ChatPanel.vue'

// 导入次要功能组件
import IslandExploration from './IslandExploration.vue'
import EnhancedTrading from './EnhancedTrading.vue'
import AstrologySystem from './AstrologySystem.vue'
import TalentSystem from './TalentSystem.vue'

// 响应式数据
const sidebarExpanded = ref(false)
const activeFunction = ref('story')
const activeInfoTab = ref('status')
const functionDrawerVisible = ref(false)
const notifications = ref([])

// 次要功能菜单
const secondaryFunctions = ref([
  { id: 'exploration', icon: '🏝️', label: '岛屿探索', badge: null },
  { id: 'trading', icon: '🏪', label: '交易市场', badge: 3 },
  { id: 'combat', icon: '⚔️', label: 'PvP战斗', badge: null },
  { id: 'astrology', icon: '🔮', label: '占星系统', badge: null },
  { id: 'talents', icon: '✨', label: '天赋系统', badge: 1 }
])

// 信息面板标签
const infoPanelTabs = ref([
  { id: 'status', icon: '📊', label: '状态', badge: null },
  { id: 'log', icon: '📜', label: '日志', badge: 5 },
  { id: 'chat', icon: '💬', label: '聊天', badge: 2 }
])

// 快捷操作
const quickActions = ref([
  { id: 'fishing', icon: '🎣', label: '钓鱼', type: 'primary', disabled: false },
  { id: 'rest', icon: '😴', label: '休息', type: 'success', disabled: false },
  { id: 'sail', icon: '⛵', label: '航行', type: 'info', disabled: false }
])

// 计算属性
const selectedFunctionTitle = computed(() => {
  const func = secondaryFunctions.value.find(f => f.id === activeFunction.value)
  return func ? func.label : ''
})

// 方法
const expandSidebar = () => {
  sidebarExpanded.value = true
}

const collapseSidebar = () => {
  sidebarExpanded.value = false
}

const selectFunction = (functionId) => {
  activeFunction.value = functionId
  functionDrawerVisible.value = true
  sidebarExpanded.value = false
}

const getCurrentComponent = () => {
  // 主要显示剧情引擎
  return StoryEngine
}

const getInfoComponent = (tabId) => {
  const components = {
    status: ComprehensiveStatus,
    log: NavigationLog,
    chat: ChatPanel
  }
  return components[tabId] || ComprehensiveStatus
}

const getSelectedFunctionComponent = () => {
  const components = {
    exploration: IslandExploration,
    trading: EnhancedTrading,
    combat: PvPCombat,
    astrology: AstrologySystem,
    talents: TalentSystem
  }
  return components[activeFunction.value] || IslandExploration
}

const executeAction = (action) => {
  switch (action.id) {
    case 'fishing':
      addNotification('info', '🎣', '开始钓鱼...')
      break
    case 'rest':
      addNotification('success', '😴', '开始休息，恢复精力...')
      break
    case 'sail':
      addNotification('info', '⛵', '开始航行...')
      break
  }
}

const addNotification = (type, icon, message) => {
  const notification = {
    id: Date.now(),
    type,
    icon,
    message
  }
  
  notifications.value.push(notification)
  
  setTimeout(() => {
    dismissNotification(notification.id)
  }, 3000)
}

const dismissNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}
</script>

<style lang="scss" scoped>
.clean-game-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #fff;
  overflow: hidden;
}

.top-status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  z-index: 100;
}

.player-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db, #2980b9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  border: 2px solid #f39c12;
}

.basic-info {
  .player-name {
    font-weight: bold;
    color: #f39c12;
    font-size: 0.9rem;
  }
  
  .ship-name {
    font-size: 0.8rem;
    color: #bbb;
  }
}

.vital-stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.8rem;
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.1);
  
  &.health { border-left: 3px solid #e74c3c; }
  &.sanity { border-left: 3px solid #9b59b6; }
  &.energy { border-left: 3px solid #f1c40f; }
}

.resources {
  display: flex;
  gap: 1rem;
}

.resource-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.6rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
}

.main-content-area {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.left-sidebar {
  position: relative;
  width: 50px;
  background: rgba(0, 0, 0, 0.2);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  z-index: 50;
  
  &.expanded {
    width: 250px;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
  }
}

.sidebar-trigger {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: rgba(52, 152, 219, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(52, 152, 219, 1);
    transform: translate(-50%, -50%) scale(1.1);
  }
}

.sidebar-content {
  padding: 1rem;
  height: 100%;
  overflow-y: auto;
}

.sidebar-header {
  margin-bottom: 1rem;
  
  h3 {
    color: #3498db;
    margin: 0;
    font-size: 1rem;
  }
}

.function-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  
  &.active {
    background: rgba(52, 152, 219, 0.2);
    border-left: 3px solid #3498db;
  }
}

.item-icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}

.item-label {
  flex: 1;
  font-size: 0.9rem;
}

.item-badge {
  background: #e74c3c;
  color: white;
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 0.8rem;
  min-width: 16px;
  text-align: center;
}

.center-game-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.game-viewport {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.quick-actions {
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: center;
}

.right-info-panel {
  width: 300px;
  background: rgba(0, 0, 0, 0.2);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  
  :deep(.el-tabs) {
    height: 100%;
    
    .el-tabs__header {
      margin: 0;
      width: 50px;
      
      .el-tabs__item {
        padding: 1rem 0.5rem;
        writing-mode: vertical-rl;
        text-orientation: mixed;
        height: auto;
        
        &.is-active {
          background: rgba(52, 152, 219, 0.2);
          color: #3498db;
        }
      }
    }
    
    .el-tabs__content {
      flex: 1;
      padding: 0;
    }
  }
}

.info-tab-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}

.info-content {
  height: 100%;
  overflow-y: auto;
  padding: 1rem;
}

.function-drawer {
  :deep(.el-drawer) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #fff;
  }
  
  :deep(.el-drawer__header) {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    color: #3498db;
  }
}

.notification-area {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.notification-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  min-width: 250px;
  border-left: 4px solid;
  
  &.info { border-left-color: #3498db; }
  &.success { border-left-color: #2ecc71; }
  &.warning { border-left-color: #f39c12; }
  &.error { border-left-color: #e74c3c; }
}

.notification-close {
  cursor: pointer;
  opacity: 0.7;
  margin-left: auto;
  
  &:hover {
    opacity: 1;
  }
}

// 通知动画
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
