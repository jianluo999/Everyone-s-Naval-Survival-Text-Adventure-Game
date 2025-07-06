<template>
  <div class="game-container deep-sea-game">
    <!-- 隐藏的移动侧边栏 -->
    <div class="mobile-sidebar" :class="{ 'expanded': sidebarExpanded }" @mouseenter="expandSidebar" @mouseleave="collapseSidebar">
      <div class="sidebar-toggle">
        <span class="toggle-icon">{{ sidebarExpanded ? '◄' : '►' }}</span>
      </div>

      <div class="sidebar-content" v-if="sidebarExpanded">
        <div class="sidebar-header">
          <h3>🎮 扩展功能</h3>
        </div>

        <div class="sidebar-sections">
          <!-- 岛屿探索系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('island')">
              <span class="section-icon">🏝️</span>
              <span class="section-name">岛屿探索</span>
              <span class="expand-icon">{{ expandedSections.island ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.island">
              <div class="feature-item" @click="openFeature('island-map')">
                <span class="feature-icon">🗺️</span>
                <span class="feature-name">交互式地图</span>
              </div>
              <div class="feature-item" @click="openFeature('resource-collect')">
                <span class="feature-icon">🥥</span>
                <span class="feature-name">资源收集</span>
              </div>
              <div class="feature-item" @click="openFeature('tool-craft')">
                <span class="feature-icon">🪓</span>
                <span class="feature-name">工具制作</span>
              </div>
              <div class="feature-item" @click="openFeature('treasure-hunt')">
                <span class="feature-icon">📦</span>
                <span class="feature-name">宝箱探索</span>
              </div>
            </div>
          </div>

          <!-- 占星系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('astrology')">
              <span class="section-icon">🔮</span>
              <span class="section-name">占星系统</span>
              <span class="expand-icon">{{ expandedSections.astrology ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.astrology">
              <div class="feature-item" @click="openFeature('sea-map')">
                <span class="feature-icon">🌊</span>
                <span class="feature-name">海域地图</span>
              </div>
              <div class="feature-item" @click="openFeature('spy-ships')">
                <span class="feature-icon">👁️</span>
                <span class="feature-name">窥探船只</span>
              </div>
              <div class="feature-item" @click="openFeature('prophecy')">
                <span class="feature-icon">⭐</span>
                <span class="feature-name">预言系统</span>
              </div>
              <div class="feature-item" @click="openFeature('crystal-ball')">
                <span class="feature-icon">🔮</span>
                <span class="feature-name">水晶球</span>
              </div>
            </div>
          </div>

          <!-- 风暴系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('storm')">
              <span class="section-icon">⛈️</span>
              <span class="section-name">风暴系统</span>
              <span class="expand-icon">{{ expandedSections.storm ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.storm">
              <div class="feature-item" @click="openFeature('storm-warning')">
                <span class="feature-icon">⚠️</span>
                <span class="feature-name">风暴预警</span>
              </div>
              <div class="feature-item" @click="openFeature('storm-effects')">
                <span class="feature-icon">⚡</span>
                <span class="feature-name">风暴特效</span>
              </div>
              <div class="feature-item" @click="openFeature('damage-system')">
                <span class="feature-icon">🔧</span>
                <span class="feature-name">损伤系统</span>
              </div>
              <div class="feature-item" @click="openFeature('storm-rewards')">
                <span class="feature-icon">💎</span>
                <span class="feature-name">风暴奖励</span>
              </div>
            </div>
          </div>

          <!-- PvP战斗系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('pvp')">
              <span class="section-icon">⚔️</span>
              <span class="section-name">PvP战斗</span>
              <span class="expand-icon">{{ expandedSections.pvp ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.pvp">
              <div class="feature-item" @click="openFeature('multi-weapon')">
                <span class="feature-icon">🗡️</span>
                <span class="feature-name">多武器系统</span>
              </div>
              <div class="feature-item" @click="openFeature('poison-attack')">
                <span class="feature-icon">☠️</span>
                <span class="feature-name">毒素攻击</span>
              </div>
              <div class="feature-item" @click="openFeature('ship-capture')">
                <span class="feature-icon">🚢</span>
                <span class="feature-name">船只占领</span>
              </div>
              <div class="feature-item" @click="openFeature('battle-log')">
                <span class="feature-icon">📋</span>
                <span class="feature-name">战斗日志</span>
              </div>
            </div>
          </div>

          <!-- 增强交易系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('trading')">
              <span class="section-icon">🏪</span>
              <span class="section-name">交易系统</span>
              <span class="expand-icon">{{ expandedSections.trading ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.trading">
              <div class="feature-item" @click="openFeature('trade-hall')">
                <span class="feature-icon">🏛️</span>
                <span class="feature-name">交易大厅</span>
              </div>
              <div class="feature-item" @click="openFeature('private-trade')">
                <span class="feature-icon">🤝</span>
                <span class="feature-name">私人交易</span>
              </div>
              <div class="feature-item" @click="openFeature('friend-system')">
                <span class="feature-icon">👥</span>
                <span class="feature-name">好友系统</span>
              </div>
              <div class="feature-item" @click="openFeature('reputation')">
                <span class="feature-icon">⭐</span>
                <span class="feature-name">声誉系统</span>
              </div>
            </div>
          </div>

          <!-- 天赋系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('talents')">
              <span class="section-icon">✨</span>
              <span class="section-name">天赋系统</span>
              <span class="expand-icon">{{ expandedSections.talents ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.talents">
              <div class="feature-item" @click="openFeature('talent-tree')">
                <span class="feature-icon">🌳</span>
                <span class="feature-name">天赋树</span>
              </div>
              <div class="feature-item" @click="openFeature('unlock-conditions')">
                <span class="feature-icon">🔓</span>
                <span class="feature-name">解锁条件</span>
              </div>
              <div class="feature-item" @click="openFeature('mysterious-abilities')">
                <span class="feature-icon">🎭</span>
                <span class="feature-name">神秘能力</span>
              </div>
              <div class="feature-item" @click="openFeature('talent-points')">
                <span class="feature-icon">💫</span>
                <span class="feature-name">天赋点数</span>
              </div>
            </div>
          </div>

          <!-- 装备效果 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('equipment')">
              <span class="section-icon">⚔️</span>
              <span class="section-name">装备效果</span>
              <span class="expand-icon">{{ expandedSections.equipment ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.equipment">
              <div class="equipment-effects">
                <div class="effect-item" v-for="effect in equipmentEffects" :key="effect.id">
                  <span class="effect-icon">{{ effect.icon }}</span>
                  <div class="effect-info">
                    <div class="effect-name">{{ effect.name }}</div>
                    <div class="effect-value">{{ effect.value }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 寻求与感染 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('infection')">
              <span class="section-icon">🦠</span>
              <span class="section-name">寻求与感染</span>
              <span class="expand-icon">{{ expandedSections.infection ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.infection">
              <div class="infection-status">
                <div class="status-item">
                  <span class="status-icon">🔍</span>
                  <div class="status-info">
                    <div class="status-name">寻求度</div>
                    <div class="status-bar">
                      <div class="bar-fill" :style="{ width: seekingLevel + '%' }"></div>
                    </div>
                  </div>
                </div>
                <div class="status-item">
                  <span class="status-icon">☣️</span>
                  <div class="status-info">
                    <div class="status-name">感染度</div>
                    <div class="status-bar infection">
                      <div class="bar-fill" :style="{ width: infectionLevel + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 玩家对话 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('dialogue')">
              <span class="section-icon">💬</span>
              <span class="section-name">玩家对话</span>
              <span class="expand-icon">{{ expandedSections.dialogue ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.dialogue">
              <div class="dialogue-options">
                <div class="dialogue-item" @click="openFeature('chat')">
                  <span class="dialogue-icon">💭</span>
                  <span class="dialogue-name">聊天</span>
                </div>
                <div class="dialogue-item" @click="openFeature('trade')">
                  <span class="dialogue-icon">🤝</span>
                  <span class="dialogue-name">交易</span>
                </div>
                <div class="dialogue-item" @click="openFeature('alliance')">
                  <span class="dialogue-icon">⚔️</span>
                  <span class="dialogue-name">结盟</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 船只升级系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('shipUpgrade')">
              <span class="section-icon">🚢</span>
              <span class="section-name">船只升级</span>
              <span class="expand-icon">{{ expandedSections.shipUpgrade ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.shipUpgrade">
              <div class="feature-grid">
                <div class="feature-item" @click="handleFeature('ship-materials')">
                  <span class="feature-icon">🪵</span>
                  <span class="feature-name">升级材料</span>
                </div>
                <div class="feature-item" @click="handleFeature('ship-skills')">
                  <span class="feature-icon">⚡</span>
                  <span class="feature-name">船只技能</span>
                </div>
                <div class="feature-item" @click="handleFeature('ship-stats')">
                  <span class="feature-icon">📊</span>
                  <span class="feature-name">船只属性</span>
                </div>
                <div class="feature-item" @click="handleFeature('ship-repair')">
                  <span class="feature-icon">🔧</span>
                  <span class="feature-name">船只维修</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 爪钩抓取系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('grappling')">
              <span class="section-icon">🪝</span>
              <span class="section-name">爪钩抓取</span>
              <span class="expand-icon">{{ expandedSections.grappling ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.grappling">
              <div class="feature-grid">
                <div class="feature-item" @click="handleFeature('auto-grab')">
                  <span class="feature-icon">🎯</span>
                  <span class="feature-name">自动抓取</span>
                </div>
                <div class="feature-item" @click="handleFeature('grab-filter')">
                  <span class="feature-icon">🔍</span>
                  <span class="feature-name">抓取筛选</span>
                </div>
                <div class="feature-item" @click="handleFeature('grab-range')">
                  <span class="feature-icon">📏</span>
                  <span class="feature-name">抓取范围</span>
                </div>
                <div class="feature-item" @click="handleFeature('grab-history')">
                  <span class="feature-icon">📋</span>
                  <span class="feature-name">抓取记录</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 海螺币系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('currency')">
              <span class="section-icon">🐚</span>
              <span class="section-name">海螺币系统</span>
              <span class="expand-icon">{{ expandedSections.currency ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.currency">
              <div class="feature-grid">
                <div class="feature-item" @click="handleFeature('conch-wallet')">
                  <span class="feature-icon">💰</span>
                  <span class="feature-name">海螺钱包</span>
                </div>
                <div class="feature-item" @click="handleFeature('chat-payment')">
                  <span class="feature-icon">💬</span>
                  <span class="feature-name">聊天付费</span>
                </div>
                <div class="feature-item" @click="handleFeature('earn-conch')">
                  <span class="feature-icon">⭐</span>
                  <span class="feature-name">获取途径</span>
                </div>
                <div class="feature-item" @click="handleFeature('conch-shop')">
                  <span class="feature-icon">🏪</span>
                  <span class="feature-name">海螺商店</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 黑雾追击系统 -->
          <div class="sidebar-section">
            <div class="section-title" @click="toggleSection('blackFog')">
              <span class="section-icon">🌫️</span>
              <span class="section-name">黑雾追击</span>
              <span class="expand-icon">{{ expandedSections.blackFog ? '▼' : '▶' }}</span>
            </div>
            <div class="section-content" v-if="expandedSections.blackFog">
              <div class="feature-grid">
                <div class="feature-item" @click="handleFeature('fog-distance')">
                  <span class="feature-icon">📏</span>
                  <span class="feature-name">距离监控</span>
                </div>
                <div class="feature-item" @click="handleFeature('speed-warning')">
                  <span class="feature-icon">⚠️</span>
                  <span class="feature-name">速度警告</span>
                </div>
                <div class="feature-item" @click="handleFeature('escape-route')">
                  <span class="feature-icon">🗺️</span>
                  <span class="feature-name">逃生路线</span>
                </div>
                <div class="feature-item" @click="handleFeature('fog-effects')">
                  <span class="feature-icon">💀</span>
                  <span class="feature-name">黑雾效果</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 船舱第一视角环境 -->
    <ShipCabin
      ref="shipCabinRef"
      class="cabin-environment"
      :class="{ 'cabin-active': showCabin }"
    />

    <!-- 深海迷雾效果 -->
    <div class="deep-sea-fog" :class="{ 'fog-reduced': showCabin }"></div>
    
    <!-- 游戏加载中 -->
    <div v-if="loading && !gameStore.player" class="loading-container deep-sea-loading">
      <div class="eldritch-circle">
        <el-icon class="loading-icon eldritch-spinner"><Loading /></el-icon>
        <div class="circle-text">召唤中...</div>
      </div>
      <p class="loading-text eldritch-text">正在唤醒深海中的古老存在...</p>
      <div class="loading-tentacles">
        <div class="tentacle" v-for="i in 6" :key="i"></div>
      </div>
    </div>

    <!-- 游戏主界面 -->
    <div v-else-if="gameStore.player" class="game-main deep-sea-main">
      <!-- 深海雾气层 -->
      <div class="mist-layer"></div>

      <!-- 使用新的文字冒险布局 -->
      <TextAdventureLayout
        ref="textAdventureRef"
        @choice-made="handleChoiceMade"
      />

      <!-- 底部深海操作栏 -->
      <div class="game-footer deep-sea-footer">
        <div class="footer-bg"></div>
        <div class="footer-tentacles">
          <div class="tentacle-left"></div>
          <div class="tentacle-right"></div>
        </div>
        <div class="footer-controls">
          <el-button 
            type="danger" 
            @click="handleBackToHome"
            :icon="ArrowLeft"
            class="eldritch-button danger-glow"
          >
            <span class="button-text">返回深渊</span>
          </el-button>
          
          <div class="footer-center">
            <div class="eldritch-symbol">⚝</div>
            <div class="status-text">深海探索中...</div>
          </div>
          
          <el-button 
            type="warning" 
            @click="handleSaveGame"
            :icon="Document"
            :loading="saving"
            class="eldritch-button warning-glow"
          >
            <span class="button-text">封印记忆</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 深海错误状态 -->
    <div v-else class="error-container deep-sea-error">
      <div class="error-portal">
        <div class="portal-rings">
          <div class="ring" v-for="i in 4" :key="i"></div>
        </div>
        <el-result
          icon="error"
          title="深海连接中断"
          :sub-title="gameStore.error || '古老的力量拒绝了你的召唤'"
          class="eldritch-result"
        >
          <template #extra>
            <el-button type="primary" @click="$router.push('/')" class="eldritch-button">
              重新连接深海
            </el-button>
          </template>
        </el-result>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Document, Loading, ChatDotRound, Notebook, House } from '@element-plus/icons-vue'

// 组件导入
import StoryDisplay from '@/components/StoryDisplay.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import ComprehensiveStatus from '@/components/ComprehensiveStatus.vue'
import NavigationLog from '@/components/NavigationLog.vue'
import ShipCabin from '@/components/ShipCabin.vue'
import TextAdventureLayout from '@/components/TextAdventureLayout.vue'

const router = useRouter()
const gameStore = useGameStore()

// 响应式数据
const loading = ref(false)
const saving = ref(false)
const showCabin = ref(true) // 控制船舱环境显示
const chatPanelRef = ref(null)
const navigationLogRef = ref(null)
const shipCabinRef = ref(null)
const textAdventureRef = ref(null)
const activeRightTab = ref('chat')

// 侧边栏相关状态
const sidebarExpanded = ref(false)
const expandedSections = ref({
  island: false,
  astrology: false,
  storm: false,
  pvp: false,
  trading: false,
  talents: false,
  equipment: false,
  infection: false,
  dialogue: false,
  shipUpgrade: false,
  grappling: false,
  currency: false,
  blackFog: false
})

// 装备效果数据
const equipmentEffects = ref([
  { id: 1, icon: '⚔️', name: '攻击力', value: '+15' },
  { id: 2, icon: '🛡️', name: '防御力', value: '+12' },
  { id: 3, icon: '💨', name: '速度', value: '+8' },
  { id: 4, icon: '🔥', name: '火焰伤害', value: '+5' }
])

// 寻求与感染状态
const seekingLevel = ref(35)
const infectionLevel = ref(12)

// 生命周期
onMounted(() => {
  // 如果没有玩家数据，重定向到主页
  if (!gameStore.player) {
    ElMessage.warning('请先唤醒你的深海化身')
    router.push('/')
    return
  }

  // 开始深海游戏循环
  startGameLoop()
})

onUnmounted(() => {
  // 清理资源
  stopGameLoop()
})

// 深海游戏循环
let gameLoopTimer = null

const startGameLoop = () => {
  // 每30秒自动保存游戏
  gameLoopTimer = setInterval(async () => {
    if (gameStore.player && gameStore.isPlayerAlive) {
      try {
        await autoSave()
      } catch (err) {
        console.error('深海记忆封印失败:', err)
      }
    }
  }, 30000)
}

const stopGameLoop = () => {
  if (gameLoopTimer) {
    clearInterval(gameLoopTimer)
    gameLoopTimer = null
  }
}

// 自动保存
const autoSave = async () => {
  console.log('正在封印深海记忆...')
}

// 返回主页
const handleBackToHome = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要离开深海吗？你的灵魂印记将被封存。',
      '脱离深海',
      {
        confirmButtonText: '确定离开',
        cancelButtonText: '继续探索',
        type: 'warning'
      }
    )

    await handleSaveGame()
    gameStore.resetGame()
    router.push('/')
  } catch {
    // 用户取消
  }
}

// 保存游戏
const handleSaveGame = async () => {
  if (!gameStore.player) return

  saving.value = true
  
  try {
    // 这里可以调用保存API
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟保存延迟
    ElMessage.success('深海记忆已被成功封印')
  } catch (err) {
    ElMessage.error('封印失败: ' + err.message)
  } finally {
    saving.value = false
  }
}

// 切换船舱显示
const toggleCabin = () => {
  if (textAdventureRef.value && textAdventureRef.value.toggleCabin) {
    textAdventureRef.value.toggleCabin()
  } else {
    showCabin.value = !showCabin.value
    ElMessage.info(showCabin.value ? '船舱环境已显示' : '船舱环境已隐藏')
  }
}

// 侧边栏相关方法
const expandSidebar = () => {
  sidebarExpanded.value = true
}

const collapseSidebar = () => {
  sidebarExpanded.value = false
  // 收起时也收起所有展开的分类
  Object.keys(expandedSections.value).forEach(key => {
    expandedSections.value[key] = false
  })
}

const toggleSection = (section) => {
  expandedSections.value[section] = !expandedSections.value[section]
}

const openFeature = (feature) => {
  console.log('打开功能:', feature)
  ElMessage.info(`${feature} 功能开发中...`)

  // 这里可以添加具体的功能实现
  switch (feature) {
    case 'island-map':
      ElMessage.info('🏝️ 交互式岛屿地图功能开发中...')
      break
    case 'resource-collect':
      ElMessage.info('🥥 资源收集系统开发中...')
      break
    case 'tool-craft':
      ElMessage.info('🪓 工具制作系统开发中...')
      break
    case 'treasure-hunt':
      ElMessage.info('📦 宝箱探索功能开发中...')
      break
    case 'sea-map':
      ElMessage.info('🌊 海域地图功能开发中...')
      break
    case 'spy-ships':
      ElMessage.info('👁️ 船只窥探功能开发中...')
      break
    case 'prophecy':
      ElMessage.info('⭐ 预言系统开发中...')
      break
    case 'crystal-ball':
      ElMessage.info('🔮 水晶球功能开发中...')
      break
    case 'storm-warning':
      ElMessage.info('⚠️ 风暴预警系统开发中...')
      break
    case 'storm-effects':
      ElMessage.info('⚡ 风暴特效系统开发中...')
      break
    case 'damage-system':
      ElMessage.info('🔧 损伤系统开发中...')
      break
    case 'storm-rewards':
      ElMessage.info('💎 风暴奖励系统开发中...')
      break
    case 'multi-weapon':
      ElMessage.info('🗡️ 多武器系统开发中...')
      break
    case 'poison-attack':
      ElMessage.info('☠️ 毒素攻击系统开发中...')
      break
    case 'ship-capture':
      ElMessage.info('🚢 船只占领系统开发中...')
      break
    case 'battle-log':
      ElMessage.info('📋 战斗日志系统开发中...')
      break
    case 'trade-hall':
      ElMessage.info('🏛️ 交易大厅功能开发中...')
      break
    case 'private-trade':
      ElMessage.info('🤝 私人交易系统开发中...')
      break
    case 'friend-system':
      ElMessage.info('👥 好友系统开发中...')
      break
    case 'reputation':
      ElMessage.info('⭐ 声誉系统开发中...')
      break
    case 'talent-tree':
      ElMessage.info('🌳 天赋树系统开发中...')
      break
    case 'unlock-conditions':
      ElMessage.info('🔓 解锁条件系统开发中...')
      break
    case 'mysterious-abilities':
      ElMessage.info('🎭 神秘能力系统开发中...')
      break
    case 'talent-points':
      ElMessage.info('💫 天赋点数系统开发中...')
      break
    // 新增功能
    case 'ship-materials':
      ElMessage.info('🪵 船只升级材料系统开发中...')
      break
    case 'ship-skills':
      ElMessage.info('⚡ 船只技能系统开发中...')
      break
    case 'ship-stats':
      ElMessage.info('📊 船只属性面板开发中...')
      break
    case 'ship-repair':
      ElMessage.info('🔧 船只维修系统开发中...')
      break
    case 'auto-grab':
      ElMessage.info('🎯 自动抓取功能开发中...')
      break
    case 'grab-filter':
      ElMessage.info('🔍 抓取筛选系统开发中...')
      break
    case 'grab-range':
      ElMessage.info('📏 抓取范围设置开发中...')
      break
    case 'grab-history':
      ElMessage.info('📋 抓取记录查看开发中...')
      break
    case 'conch-wallet':
      ElMessage.info('💰 海螺币钱包开发中...')
      break
    case 'chat-payment':
      ElMessage.info('💬 聊天付费系统开发中...')
      break
    case 'earn-conch':
      ElMessage.info('⭐ 海螺币获取途径开发中...')
      break
    case 'conch-shop':
      ElMessage.info('🏪 海螺币商店开发中...')
      break
    case 'fog-distance':
      ElMessage.info('📏 黑雾距离监控开发中...')
      break
    case 'speed-warning':
      ElMessage.info('⚠️ 速度警告系统开发中...')
      break
    case 'escape-route':
      ElMessage.info('🗺️ 逃生路线规划开发中...')
      break
    case 'fog-effects':
      ElMessage.info('💀 黑雾效果系统开发中...')
      break
    default:
      ElMessage.info('功能开发中...')
  }
}

// 处理侧边栏功能点击（新增功能专用）
const handleFeature = (feature) => {
  console.log('点击功能:', feature)

  // 直接调用openFeature来处理
  openFeature(feature)
}

// 处理选择记录
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
      content: `在"${choiceData.storyTitle}"中做出了选择。`,
      effects: [
        ...(choiceData.choice.goldCost > 0 ? [{ type: '金币', value: -choiceData.choice.goldCost }] : []),
        ...(choiceData.choice.goldReward > 0 ? [{ type: '金币', value: choiceData.choice.goldReward }] : []),
        ...(choiceData.choice.healthCost > 0 ? [{ type: '生命', value: -choiceData.choice.healthCost }] : []),
        ...(choiceData.choice.healthReward > 0 ? [{ type: '生命', value: choiceData.choice.healthReward }] : []),
        ...(choiceData.choice.experienceReward > 0 ? [{ type: '经验', value: choiceData.choice.experienceReward }] : [])
      ]
    })
  }
}
</script>

<style lang="scss" scoped>
// 移动侧边栏样式
.mobile-sidebar {
  position: fixed;
  left: -350px; // 默认完全隐藏
  top: 0;
  width: 350px;
  height: 100vh;
  background: rgba(0, 20, 40, 0.95);
  border-right: 2px solid #00ff00;
  z-index: 1000;
  transition: all 0.3s ease;
  overflow: hidden;

  &.expanded {
    left: 0; // 展开时显示
  }

  .sidebar-toggle {
    position: fixed;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #00ff00;
    font-size: 1.2rem;
    cursor: pointer;
    z-index: 1001;
    background: rgba(0, 20, 40, 0.8);
    padding: 8px;
    border-radius: 0 8px 8px 0;
    border: 1px solid #00ff00;
    transition: all 0.3s ease;

    &:hover {
      background: rgba(0, 255, 0, 0.2);
      transform: translateY(-50%) scale(1.1);
    }
  }

  .sidebar-content {
    padding: 60px 20px 20px 20px;
    height: 100%;
    overflow-y: auto;

    .sidebar-header {
      margin-bottom: 20px;

      h3 {
        color: #00ff00;
        font-size: 1.1rem;
        margin: 0;
        text-align: center;
        border-bottom: 1px solid #00ff00;
        padding-bottom: 10px;
      }
    }

    .sidebar-sections {
      .sidebar-section {
        margin-bottom: 15px;
        border: 1px solid rgba(0, 255, 0, 0.3);
        border-radius: 5px;
        overflow: hidden;

        .section-title {
          background: rgba(0, 255, 0, 0.1);
          padding: 12px 15px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 10px;
          transition: all 0.2s ease;

          &:hover {
            background: rgba(0, 255, 0, 0.2);
          }

          .section-icon {
            font-size: 1.2rem;
          }

          .section-name {
            flex: 1;
            color: #00ff00;
            font-weight: bold;
            font-size: 0.9rem;
          }

          .expand-icon {
            color: #00ff00;
            font-size: 0.8rem;
          }
        }

        .section-content {
          background: rgba(0, 0, 0, 0.3);

          .feature-item {
            padding: 10px 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
            border-bottom: 1px solid rgba(0, 255, 0, 0.1);

            &:hover {
              background: rgba(0, 255, 0, 0.1);
              transform: translateX(5px);
            }

            &:last-child {
              border-bottom: none;
            }

            .feature-icon {
              font-size: 1rem;
            }

            .feature-name {
              color: #ffffff;
              font-size: 0.85rem;
              opacity: 0.9;
            }
          }
        }
      }
    }
  }

  // 装备效果样式
  .equipment-effects {
    .effect-item {
      display: flex;
      align-items: center;
      padding: 6px 8px;
      margin: 3px 0;
      background: rgba(0, 60, 120, 0.2);
      border-radius: 4px;

      .effect-icon {
        margin-right: 8px;
        font-size: 1rem;
      }

      .effect-info {
        flex: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .effect-name {
          color: #00ccff;
          font-size: 0.85rem;
        }

        .effect-value {
          color: #00ff00;
          font-weight: bold;
          font-size: 0.85rem;
        }
      }
    }
  }

  // 感染状态样式
  .infection-status {
    .status-item {
      display: flex;
      align-items: center;
      padding: 8px;
      margin: 6px 0;
      background: rgba(0, 40, 80, 0.3);
      border-radius: 4px;

      .status-icon {
        margin-right: 10px;
        font-size: 1.1rem;
      }

      .status-info {
        flex: 1;

        .status-name {
          color: #00ccff;
          font-size: 0.85rem;
          margin-bottom: 4px;
        }

        .status-bar {
          height: 8px;
          background: rgba(0, 0, 0, 0.5);
          border-radius: 4px;
          overflow: hidden;
          border: 1px solid rgba(0, 255, 0, 0.3);

          .bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff00, #00cc00);
            transition: width 0.3s ease;
          }

          &.infection .bar-fill {
            background: linear-gradient(90deg, #ff4444, #cc0000);
          }
        }
      }
    }
  }

  // 对话选项样式
  .dialogue-options {
    .dialogue-item {
      display: flex;
      align-items: center;
      padding: 8px 12px;
      margin: 4px 0;
      background: rgba(0, 40, 80, 0.3);
      border: 1px solid rgba(0, 255, 0, 0.3);
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(0, 255, 0, 0.1);
        border-color: #00ff00;
        transform: translateX(5px);
      }

      .dialogue-icon {
        margin-right: 8px;
        font-size: 1.1rem;
      }

      .dialogue-name {
        color: #00ff00;
        font-size: 0.9rem;
      }
    }
  }

  // 滚动条样式
  ::-webkit-scrollbar {
    width: 6px;
  }

  ::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
  }

  ::-webkit-scrollbar-thumb {
    background: rgba(0, 255, 0, 0.5);
    border-radius: 3px;

    &:hover {
      background: rgba(0, 255, 0, 0.7);
    }
  }
}

.game-container {
  min-height: 100vh;
  position: relative;
  padding: 1rem;
  padding-bottom: 120px; // 为底部操作栏留出空间
}

.deep-sea-game {
  background: 
    radial-gradient(ellipse at 30% 20%, rgba(0, 60, 40, 0.6) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 80%, rgba(0, 80, 60, 0.4) 0%, transparent 50%),
    linear-gradient(180deg, rgba(5, 25, 20, 0.98) 0%, rgba(0, 20, 15, 0.99) 50%, rgba(0, 15, 10, 1) 100%);
  font-family: 'Consolas', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
  color: #ffffff;
  
  // 深海迷雾效果
  .deep-sea-fog {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
      radial-gradient(ellipse at 20% 30%, rgba(0, 255, 136, 0.08) 0%, transparent 40%),
      radial-gradient(ellipse at 80% 70%, rgba(0, 255, 200, 0.06) 0%, transparent 40%);
    animation: fog-drift 25s ease-in-out infinite;
    pointer-events: none;
    z-index: 1;
    transition: opacity 0.5s ease;

    &.fog-reduced {
      opacity: 0.3;
    }
  }
}

// 船舱环境 - 重新设计为背景装饰
.cabin-environment {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  opacity: 0.15; // 大幅降低透明度，作为背景
  transition: opacity 0.5s ease;
  pointer-events: none; // 禁用交互，避免干扰主界面
  filter: blur(1px); // 轻微模糊，增强背景感

  &.cabin-active {
    opacity: 0.25; // 即使激活也保持低透明度
  }
}

// 深海加载界面
.deep-sea-loading {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: #66ffcc;
  
  .eldritch-circle {
    position: relative;
    width: 200px;
    height: 200px;
    border: 2px solid rgba(102, 255, 204, 0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    animation: eldritch-rotate 10s linear infinite;
    
    &::before {
      content: '';
      position: absolute;
      width: 220px;
      height: 220px;
      border: 1px solid rgba(102, 255, 204, 0.2);
      border-radius: 50%;
      animation: eldritch-rotate 15s linear infinite reverse;
    }
    
    &::after {
      content: '';
      position: absolute;
      width: 180px;
      height: 180px;
      border: 1px solid rgba(0, 255, 127, 0.4);
      border-radius: 50%;
      animation: eldritch-rotate 8s linear infinite;
    }
    
    .loading-icon {
      font-size: 4rem;
      color: #66ffcc;
      animation: eldritch-pulse 2s ease-in-out infinite;
      z-index: 2;
    }
    
    .circle-text {
      position: absolute;
      bottom: -30px;
      font-size: 1rem;
      font-weight: bold;
      text-shadow: 0 0 10px rgba(102, 255, 204, 0.8);
    }
  }
  
  .loading-text {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    animation: eldritch-glow 3s ease-in-out infinite;
  }
  
  .loading-tentacles {
    position: relative;
    width: 300px;
    height: 50px;
    
    .tentacle {
      position: absolute;
      width: 4px;
      height: 40px;
      background: linear-gradient(to bottom, rgba(102, 255, 204, 0.8), transparent);
      border-radius: 2px;
      animation: tentacle-sway 3s ease-in-out infinite;
      
             &:nth-child(1) { left: 50px; animation-delay: 0.2s; }
       &:nth-child(2) { left: 100px; animation-delay: 0.4s; }
       &:nth-child(3) { left: 150px; animation-delay: 0.6s; }
       &:nth-child(4) { left: 200px; animation-delay: 0.8s; }
       &:nth-child(5) { left: 250px; animation-delay: 1.0s; }
       &:nth-child(6) { left: 300px; animation-delay: 1.2s; }
    }
  }
}

// 深海主界面
.deep-sea-main {
  position: relative;
  z-index: 2;
  
  .mist-layer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
      repeating-linear-gradient(
        45deg,
        transparent,
        transparent 50px,
        rgba(102, 255, 204, 0.02) 50px,
        rgba(102, 255, 204, 0.02) 52px
      );
    animation: mist-flow 20s linear infinite;
    pointer-events: none;
  }
}



 // 深海内容区域
 .deep-sea-content {
   margin-bottom: 2rem;
 }
 
 // 主要内容区域 - 左右分列
 .deep-sea-main-content {
   display: grid;
   grid-template-columns: 2fr 1fr;
   gap: 2rem;
   min-height: 600px;
 }
 
 // 左侧区域：状态面板 + 故事区域
 .deep-sea-left-section {
   display: flex;
   flex-direction: column;
   gap: 1.5rem;
 }
 
 // 右侧区域：聊天面板占据整个高度
 .deep-sea-right-section {
   display: flex;
   flex-direction: column;
 }
 
 // 顶部综合状态区域
 .deep-sea-top-section {
   flex-shrink: 0;
   
   .comprehensive-card {
     position: relative;
     height: 180px; // 调整为更合适的高度
     
     .card-frame {
       position: relative;
       height: 100%;
       background: rgba(0, 20, 40, 0.8);
       border-radius: 15px;
       backdrop-filter: blur(15px);
       border: 1px solid rgba(255, 255, 255, 0.3);
       
       .frame-corner {
         position: absolute;
         width: 20px;
         height: 20px;
         border: 2px solid rgba(255, 255, 255, 0.6);
         z-index: 1;
         
         &.top-left {
           top: -2px;
           left: -2px;
           border-right: none;
           border-bottom: none;
         }
         
         &.top-right {
           top: -2px;
           right: -2px;
           border-left: none;
           border-bottom: none;
         }
         
         &.bottom-left {
           bottom: -2px;
           left: -2px;
           border-right: none;
           border-top: none;
         }
         
         &.bottom-right {
           bottom: -2px;
           right: -2px;
           border-left: none;
           border-top: none;
         }
       }
     }
   }
 }
 
 // 深海故事区域
.deep-sea-story-section {
  flex: 1;
  
  .story-frame {
    position: relative;
    height: 100%;
    background: rgba(0, 30, 25, 0.95);
    border-radius: 15px;
    
    .frame-corner {
      position: absolute;
      width: 20px;
      height: 20px;
      border: 2px solid rgba(255, 255, 255, 0.5);
      z-index: 1;
      
      &.top-left {
        top: -2px;
        left: -2px;
        border-right: none;
        border-bottom: none;
      }
      
      &.top-right {
        top: -2px;
        right: -2px;
        border-left: none;
        border-bottom: none;
      }
      
      &.bottom-left {
        bottom: -2px;
        left: -2px;
        border-right: none;
        border-top: none;
      }
      
      &.bottom-right {
        bottom: -2px;
        right: -2px;
        border-left: none;
        border-top: none;
      }
    }
  }
}
 
 // 深海聊天区域
.deep-sea-chat-section {
  flex: 1;
  
  .chat-frame {
    position: relative;
    height: 100%;
    background: rgba(0, 30, 25, 0.95);
    border-radius: 15px;
    
    .frame-glow {
      position: absolute;
      top: -5px;
      left: -5px;
      right: -5px;
      bottom: -5px;
      background: linear-gradient(45deg, 
        rgba(102, 255, 204, 0.1) 0%, 
        rgba(0, 255, 127, 0.05) 25%, 
        rgba(102, 255, 204, 0.1) 50%, 
        rgba(0, 255, 127, 0.05) 75%, 
        rgba(102, 255, 204, 0.1) 100%);
      border-radius: 20px;
      animation: frame-glow-pulse 4s ease-in-out infinite;
      z-index: 0;
    }
  }
}

// 深海底部栏
.deep-sea-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120px;
  z-index: 10;
  
  .footer-bg {
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top,
      rgba(0, 0, 0, 0.95) 0%,
      rgba(0, 10, 20, 0.8) 50%,
      rgba(0, 20, 40, 0.4) 100%);
    backdrop-filter: blur(15px);
  }
  
  .footer-tentacles {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden;
    
    .tentacle-left, .tentacle-right {
      position: absolute;
      width: 200px;
      height: 100%;
      background: linear-gradient(45deg,
        rgba(0, 40, 80, 0.6) 0%,
        rgba(0, 60, 120, 0.3) 50%,
        transparent 100%);
      
      &::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(90deg,
          transparent,
          transparent 10px,
          rgba(102, 255, 204, 0.1) 10px,
          rgba(102, 255, 204, 0.1) 12px);
      }
    }
    
    .tentacle-left {
      left: -100px;
      transform: skewX(-15deg);
      animation: tentacle-wave 8s ease-in-out infinite;
    }
    
    .tentacle-right {
      right: -100px;
      transform: skewX(15deg);
      animation: tentacle-wave 8s ease-in-out infinite reverse;
    }
  }
  
  .footer-controls {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
    z-index: 2;
    
    .footer-center {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.5rem;

      .cabin-controls {
        margin-bottom: 0.5rem;

        .cabin-toggle-btn {
          background: rgba(102, 255, 204, 0.1);
          border: 1px solid #66ffcc;
          color: #66ffcc;
          font-size: 12px;
          padding: 4px 8px;
          transition: all 0.3s ease;

          &:hover {
            background: rgba(102, 255, 204, 0.2);
            box-shadow: 0 0 10px rgba(102, 255, 204, 0.5);
          }

          &.el-button--primary {
            background: rgba(102, 255, 204, 0.3);
            border-color: #FFD700;
            color: #FFD700;

            &:hover {
              background: rgba(255, 215, 0, 0.2);
              box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
            }
          }
        }
      }

      .eldritch-symbol {
        font-size: 2rem;
        color: #66ffcc;
        animation: eldritch-glow 3s ease-in-out infinite;
      }

      .status-text {
        color: #66ffcc;
        font-size: 0.9rem;
        opacity: 0.8;
        text-shadow: 0 0 5px rgba(102, 255, 204, 0.5);
      }
    }
  }
}

// 深海错误界面
.deep-sea-error {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  
  .error-portal {
    position: relative;
    text-align: center;
    
    .portal-rings {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 0;
      
      .ring {
        position: absolute;
        border: 2px solid rgba(220, 20, 60, 0.3);
        border-radius: 50%;
        animation: portal-spin 10s linear infinite;
        
        &:nth-child(1) {
          width: 200px;
          height: 200px;
          margin: -100px 0 0 -100px;
          animation-duration: 8s;
        }
        
        &:nth-child(2) {
          width: 150px;
          height: 150px;
          margin: -75px 0 0 -75px;
          animation-duration: 12s;
          animation-direction: reverse;
        }
        
        &:nth-child(3) {
          width: 100px;
          height: 100px;
          margin: -50px 0 0 -50px;
          animation-duration: 6s;
        }
        
        &:nth-child(4) {
          width: 50px;
          height: 50px;
          margin: -25px 0 0 -25px;
          animation-duration: 15s;
          animation-direction: reverse;
        }
      }
    }
  }
}

// 深海特殊按钮
.eldritch-button {
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent, 
      rgba(102, 255, 204, 0.2), 
      transparent);
    transition: left 0.5s ease;
  }
  
  &:hover::before {
    left: 100%;
  }
  
  .button-text {
    position: relative;
    z-index: 1;
  }
  
  &.danger-glow:hover {
    box-shadow: 0 0 30px rgba(220, 20, 60, 0.5) !important;
  }
  
  &.warning-glow:hover {
    box-shadow: 0 0 30px rgba(245, 158, 11, 0.5) !important;
  }
}

// 深海动画
@keyframes fog-drift {
  0%, 100% { transform: translateX(0) translateY(0); }
  25% { transform: translateX(-10px) translateY(-5px); }
  50% { transform: translateX(10px) translateY(0); }
  75% { transform: translateX(-5px) translateY(5px); }
}

@keyframes eldritch-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes eldritch-pulse {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.1); opacity: 1; }
}

@keyframes tentacle-sway {
  0%, 100% { transform: rotate(0deg) scaleY(1); }
  50% { transform: rotate(5deg) scaleY(1.2); }
}

@keyframes mist-flow {
  0% { transform: translateX(-50px); }
  100% { transform: translateX(50px); }
}

 @keyframes frame-glow-pulse {
   0%, 100% { opacity: 0.3; }
   50% { opacity: 0.7; }
 }
 
 @keyframes portal-spin {
   from { transform: rotate(0deg); }
   to { transform: rotate(360deg); }
 }
 
 // 响应式适配
 @media (max-width: 1024px) {
   .deep-sea-top-section {
     .comprehensive-card {
       height: 200px; // 中等屏幕上稍微增加高度
     }
   }
   
   .deep-sea-main-content {
     grid-template-columns: 1.5fr 1fr;
     gap: 1.5rem;
   }
 }
 
 @media (max-width: 900px) {
   .deep-sea-top-section {
     .comprehensive-card {
       height: 180px; // 较小屏幕上减少高度
     }
   }
   
   .deep-sea-main-content {
     grid-template-columns: 1fr;
     gap: 1rem;
   }
 }
 
 @media (max-width: 768px) {
   .game-container {
     padding: 0.5rem;
     padding-bottom: 100px;
   }
   
   .deep-sea-top-section {
     .comprehensive-card {
       height: 160px; // 手机端进一步减少高度
     }
   }

   .right-panel-container {
     height: 100%;
   }

   .deep-sea-tabs {
     height: 100%;
     display: flex;
     flex-direction: column;

     :deep(.el-tabs__header) {
       background: rgba(0, 40, 80, 0.8);
       border-bottom: 2px solid #66ffcc;
       margin: 0;
       flex-shrink: 0;
     }

     :deep(.el-tabs__nav-wrap) {
       background: transparent;
     }

     :deep(.el-tabs__item) {
       color: #66ffcc;
       border: none;
       background: transparent;

       &.is-active {
         color: #FFD700;
         background: rgba(255, 215, 0, 0.1);
       }

       &:hover {
         color: #FFD700;
       }
     }

     :deep(.el-tabs__active-bar) {
       background: #FFD700;
     }

     :deep(.el-tabs__content) {
       flex: 1;
       overflow: hidden;
       height: 0; // 强制flex子元素计算高度
     }

     :deep(.el-tab-pane) {
       height: 100%;
       overflow: hidden;
     }
   }

   .tab-label {
     display: flex;
     align-items: center;
     gap: 4px;
   }

   .log-section {
     height: 100%;
   }

   .log-frame {
     height: 100%;
     position: relative;

     .frame-glow {
       position: absolute;
       top: -2px;
       left: -2px;
       right: -2px;
       bottom: -2px;
       background: linear-gradient(45deg, #66ffcc, #FFD700, #66ffcc);
       border-radius: 8px;
       opacity: 0.3;
       z-index: -1;
       animation: glow-pulse 3s ease-in-out infinite;
     }
   }

   .deep-sea-navigation-log {
     height: 100%;
   }
   
   .deep-sea-footer {
     height: 100px;
     
     .footer-controls {
       padding: 1rem;
       flex-direction: column;
       gap: 1rem;
       
       .footer-center {
         order: 1;
       }
     }
   }
 }
</style> 