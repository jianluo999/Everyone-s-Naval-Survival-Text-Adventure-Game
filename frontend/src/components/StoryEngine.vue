<template>
  <div class="story-engine">
    <!-- 主剧情显示区域 -->
    <div class="story-display">
      <div class="chapter-header">
        <h2 class="chapter-title">{{ currentChapter.title }}</h2>
        <div class="chapter-progress">
          <span class="current-page">{{ currentPage }}</span>
          <span class="separator">/</span>
          <span class="total-pages">{{ currentChapter.totalPages }}</span>
        </div>
      </div>
      
      <!-- 剧情内容 -->
      <div class="story-content" ref="storyContent">
        <div 
          v-for="(paragraph, index) in currentPageContent" 
          :key="index"
          class="story-paragraph"
          :class="paragraph.type"
          v-html="formatParagraph(paragraph.text)"
        ></div>
      </div>
      
      <!-- 物品获得提示 -->
      <div v-if="itemsGained.length > 0" class="items-gained">
        <h4>📦 获得物品：</h4>
        <div class="items-list">
          <div 
            v-for="item in itemsGained" 
            :key="item.id"
            class="item-card"
            :class="item.quality"
          >
            <div class="item-icon">{{ item.icon }}</div>
            <div class="item-info">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-description">{{ item.description }}</div>
              <div class="item-effect" v-if="item.effect">{{ item.effect }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 状态变化提示 -->
      <div v-if="statusChanges.length > 0" class="status-changes">
        <div 
          v-for="change in statusChanges" 
          :key="change.id"
          class="status-change"
          :class="change.type"
        >
          <span class="change-icon">{{ change.icon }}</span>
          <span class="change-text">{{ change.text }}</span>
          <span class="change-value">{{ change.value }}</span>
        </div>
      </div>
    </div>
    
    <!-- 选择系统 -->
    <div v-if="currentChoices.length > 0" class="choice-system">
      <h4>🤔 你的选择：</h4>
      <div class="choices-list">
        <div 
          v-for="(choice, index) in currentChoices" 
          :key="index"
          class="choice-option"
          :class="{ 'disabled': choice.disabled, 'dangerous': choice.risk > 70 }"
          @click="makeChoice(choice)"
        >
          <div class="choice-text">{{ choice.text }}</div>
          <div class="choice-info">
            <span v-if="choice.requirement" class="requirement">
              需要：{{ choice.requirement }}
            </span>
            <span v-if="choice.risk > 0" class="risk-level">
              风险：{{ getRiskText(choice.risk) }}
            </span>
            <span v-if="choice.energyCost > 0" class="energy-cost">
              精力：-{{ choice.energyCost }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 剧情控制 -->
    <div class="story-controls">
      <el-button-group>
        <el-button 
          @click="previousPage" 
          :disabled="currentPage <= 1"
          icon="ArrowLeft"
        >
          上一页
        </el-button>
        
        <el-button 
          @click="nextPage" 
          :disabled="currentPage >= currentChapter.totalPages && currentChoices.length === 0"
          type="primary"
        >
          {{ currentChoices.length > 0 ? '等待选择' : '下一页' }}
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </el-button-group>
      
      <div class="auto-play-controls">
        <el-switch
          v-model="autoPlay"
          active-text="自动播放"
          @change="toggleAutoPlay"
        />
        <el-slider
          v-if="autoPlay"
          v-model="autoPlaySpeed"
          :min="1"
          :max="10"
          :step="1"
          style="width: 100px; margin-left: 10px;"
        />
      </div>
    </div>
    
    <!-- 剧情历史 -->
    <div class="story-history" v-if="showHistory">
      <h4>📚 剧情回顾</h4>
      <div class="history-list">
        <div 
          v-for="entry in storyHistory" 
          :key="entry.id"
          class="history-entry"
          @click="jumpToHistory(entry)"
        >
          <div class="history-chapter">{{ entry.chapter }}</div>
          <div class="history-content">{{ entry.summary }}</div>
          <div class="history-time">{{ formatTime(entry.timestamp) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { getChapter, getChapterContent, getChapterChoices, getNextChapter } from '@/data/chapters'

const gameStore = useGameStore()

// 响应式数据
const currentChapterId = ref(13)
const currentPage = ref(1)
const autoPlay = ref(false)
const autoPlaySpeed = ref(3)
const showHistory = ref(false)
const storyContent = ref(null)

// 当前章节数据
const currentChapter = computed(() => {
  return getChapter(currentChapterId.value)
})
    1: [
      {
        type: 'narrative',
        text: '航海日志提供了很多方便的功能。但离开航海日志，这世界简直和现实没区别。'
      },
      {
        type: 'action',
        text: '像砍树，是个力气活，也是技术活，尤其石斧还不怎么锋利，震手。'
      },
      {
        type: 'status',
        text: '砍下这棵最大的椰子树，杨逸精力直接扣了13点，只剩30点。'
      },
      {
        type: 'thought',
        text: '满打满算，满精力，他最多也就砍个五六棵树。再多就不行了，精力低于30，有昏厥的风险。'
      }
    ],
    2: [
      {
        type: 'discovery',
        text: '树倒后，杨逸立刻去捡椰子，刚拿起来，脸上就露出喜色。'
      },
      {
        type: 'item',
        text: '【名称：活力椰子】【类型：食物】【简介：这是一种罕见的特殊椰子，富含维生素和矿物质，里面的椰汁可以提高精力恢复速度。】'
      },
      {
        type: 'action',
        text: '杨逸二话不说，劈开一个椰子痛饮起来，获得了精力恢复加速的buff。'
      },
      {
        type: 'narrative',
        text: '这东西，正是杨逸急缺的，这一趟算是赚大了。'
      }
    ],
    3: [
      {
        type: 'discovery',
        text: '他打开青铜宝箱，里面立刻掉出几个光球，触摸之后变成了三件道具。'
      },
      {
        type: 'item',
        text: '【名称：活力椰汁爽配方】【类型：配方】【品质：良品】【简介：使用后获得活力椰汁爽的配方，需要试剂瓶，盐，活力椰子。】'
      },
      {
        type: 'item',
        text: '【名称：可食用海盐500克】【类型：食物】【简介：调味品，可增加风味，补充盐分。】'
      },
      {
        type: 'item',
        text: '【名称：试剂架】【种类：工具】【品质：良品】【简介：制作各种试剂必不可缺的工具，可用水晶合成。它可以提供试剂瓶，试剂喝完后，试剂瓶将消失。】'
      }
    ],
    4: [
      {
        type: 'action',
        text: '一个宝箱，不仅有配方，还有配方所需的其他两种素材。杨逸大喜，立刻就用掉了配方，然后开始动手调配活力椰汁爽。'
      },
      {
        type: 'crafting',
        text: '所需素材：活力椰子*1，盐10克。必备工具：试剂架'
      },
      {
        type: 'item',
        text: '【名称：活力椰汁爽】【种类：消耗品】【品质：良品】【简介：一款让人活力四射的饮料。可恢复10精力，提高精力恢复速度50%，持续8小时。每次生效间隔24小时。】'
      },
      {
        type: 'narrative',
        text: '杨逸笑了，转头看向海岸线上，那满满当当的椰子，手里的斧头舞出了花。'
      }
    ]
  },
  choices: {
    4: [
      {
        id: 'continue_chopping',
        text: '继续砍伐椰子树，收集更多活力椰子',
        energyCost: 15,
        risk: 30,
        requirement: '精力 > 30'
      },
      {
        id: 'explore_island',
        text: '探索岛屿内部，寻找更多资源',
        energyCost: 20,
        risk: 60,
        requirement: '装备武器'
      },
      {
        id: 'return_ship',
        text: '返回船只，准备离开这个岛屿',
        energyCost: 5,
        risk: 10,
        requirement: null
      }
    ]
  }
})

// 物品获得数据
const itemsGained = ref([
  {
    id: 'vitality_coconut',
    name: '活力椰子',
    icon: '🥥',
    quality: 'rare',
    description: '富含维生素和矿物质的特殊椰子',
    effect: '提高精力恢复速度'
  },
  {
    id: 'vitality_drink_recipe',
    name: '活力椰汁爽配方',
    icon: '📜',
    quality: 'good',
    description: '制作活力饮料的配方',
    effect: '学会制作活力椰汁爽'
  },
  {
    id: 'sea_salt',
    name: '可食用海盐',
    icon: '🧂',
    quality: 'common',
    description: '调味品，补充盐分',
    effect: '制作材料'
  },
  {
    id: 'reagent_rack',
    name: '试剂架',
    icon: '🧪',
    quality: 'good',
    description: '制作试剂的必备工具',
    effect: '提供试剂瓶'
  }
])

// 状态变化数据
const statusChanges = ref([
  {
    id: 'energy_loss',
    type: 'negative',
    icon: '⚡',
    text: '精力消耗',
    value: '-13'
  },
  {
    id: 'energy_buff',
    type: 'positive',
    icon: '✨',
    text: '精力恢复加速',
    value: '+50%'
  }
])

// 剧情历史
const storyHistory = ref([
  {
    id: 1,
    chapter: '第12章',
    summary: '发现椰林岛，开始探索...',
    timestamp: new Date(Date.now() - 3600000)
  },
  {
    id: 2,
    chapter: '第11章',
    summary: '占星预测，发现神秘岛屿...',
    timestamp: new Date(Date.now() - 7200000)
  }
])

// 计算属性
const currentPageContent = computed(() => {
  return getChapterContent(currentChapterId.value, currentPage.value) || []
})

const currentChoices = computed(() => {
  return getChapterChoices(currentChapterId.value, currentPage.value) || []
})

// 方法
const formatParagraph = (text) => {
  // 格式化物品信息
  text = text.replace(/【([^】]+)】/g, '<span class="item-tag">【$1】</span>')
  
  // 格式化数值变化
  text = text.replace(/(\d+)点/g, '<span class="number-value">$1点</span>')
  
  // 格式化状态效果
  text = text.replace(/(buff|debuff)/gi, '<span class="status-effect">$1</span>')
  
  return text
}

const nextPage = () => {
  if (currentChoices.value.length > 0) {
    ElMessage.warning('请先做出选择')
    return
  }
  
  if (currentPage.value < currentChapter.value.totalPages) {
    currentPage.value++
    scrollToTop()
    
    // 添加到历史记录
    addToHistory()
  } else {
    // 章节结束，跳转到下一章
    loadNextChapter()
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    scrollToTop()
  }
}

const makeChoice = (choice) => {
  if (choice.disabled) {
    ElMessage.error('不满足选择条件')
    return
  }
  
  // 检查精力要求
  if (choice.energyCost && gameStore.player.energy < choice.energyCost) {
    ElMessage.error('精力不足')
    return
  }
  
  // 执行选择结果
  executeChoice(choice)
  
  // 继续剧情
  nextPage()
}

const executeChoice = (choice) => {
  switch (choice.id) {
    case 'continue_chopping':
      gameStore.player.energy -= choice.energyCost
      gameStore.addResource('wood', 15)
      gameStore.addResource('vitality_coconut', 8)
      ElMessage.success('获得了更多椰子和木料')
      break
      
    case 'explore_island':
      gameStore.player.energy -= choice.energyCost
      // 触发探索事件
      triggerExplorationEvent()
      break
      
    case 'return_ship':
      gameStore.player.energy -= choice.energyCost
      ElMessage.info('安全返回船只')
      break
  }
}

const triggerExplorationEvent = () => {
  // 这里会触发第14章的海妖事件
  ElMessage.warning('发现了神秘的发光痕迹...')
  
  // 可能触发危险事件
  if (Math.random() < 0.3) {
    ElMessage.error('遭遇了未知生物！')
    gameStore.player.sanity -= 5
  }
}

const getRiskText = (risk) => {
  if (risk < 30) return '低'
  if (risk < 60) return '中'
  if (risk < 80) return '高'
  return '极高'
}

const toggleAutoPlay = (enabled) => {
  if (enabled) {
    startAutoPlay()
  } else {
    stopAutoPlay()
  }
}

let autoPlayTimer = null

const startAutoPlay = () => {
  autoPlayTimer = setInterval(() => {
    if (currentChoices.value.length === 0) {
      nextPage()
    }
  }, (11 - autoPlaySpeed.value) * 1000)
}

const stopAutoPlay = () => {
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer)
    autoPlayTimer = null
  }
}

const scrollToTop = () => {
  nextTick(() => {
    if (storyContent.value) {
      storyContent.value.scrollTop = 0
    }
  })
}

const addToHistory = () => {
  const entry = {
    id: Date.now(),
    chapter: currentChapter.value.title,
    summary: currentPageContent.value[0]?.text.substring(0, 30) + '...',
    timestamp: new Date()
  }
  
  storyHistory.value.unshift(entry)
  
  // 限制历史记录数量
  if (storyHistory.value.length > 20) {
    storyHistory.value = storyHistory.value.slice(0, 20)
  }
}

const jumpToHistory = (entry) => {
  ElMessage.info(`跳转到：${entry.chapter}`)
  // 这里可以实现历史回顾功能
}

const loadNextChapter = () => {
  ElMessage.success('第13章完成！准备进入第14章...')
  // 这里可以加载第14章内容
}

const formatTime = (timestamp) => {
  return timestamp.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 监听器
watch(currentPage, () => {
  // 页面变化时的处理
  itemsGained.value = []
  statusChanges.value = []
  
  // 根据当前页面显示相应的物品和状态变化
  if (currentPage.value === 2) {
    itemsGained.value = [itemsGained.value[0]] // 活力椰子
    statusChanges.value = [statusChanges.value[1]] // 精力buff
  } else if (currentPage.value === 3) {
    itemsGained.value = itemsGained.value.slice(1) // 配方和材料
  }
})

onMounted(() => {
  // 初始化
  addToHistory()
})
</script>

<style lang="scss" scoped>
.story-engine {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #fff;
  padding: 1rem;
  overflow: hidden;
}

.story-display {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(52, 152, 219, 0.3);
}

.chapter-title {
  color: #3498db;
  margin: 0;
  font-size: 1.5rem;
}

.chapter-progress {
  color: #bbb;
  font-size: 0.9rem;
}

.story-content {
  margin-bottom: 2rem;
}

.story-paragraph {
  margin-bottom: 1rem;
  line-height: 1.8;
  padding: 0.8rem;
  border-radius: 0.5rem;
  
  &.narrative {
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid #3498db;
  }
  
  &.action {
    background: rgba(46, 204, 113, 0.1);
    border-left: 3px solid #2ecc71;
  }
  
  &.thought {
    background: rgba(155, 89, 182, 0.1);
    border-left: 3px solid #9b59b6;
    font-style: italic;
  }
  
  &.discovery {
    background: rgba(243, 156, 18, 0.1);
    border-left: 3px solid #f39c12;
  }
  
  &.item {
    background: rgba(231, 76, 60, 0.1);
    border-left: 3px solid #e74c3c;
    font-family: monospace;
  }
  
  &.status {
    background: rgba(52, 152, 219, 0.1);
    border-left: 3px solid #3498db;
  }
  
  &.crafting {
    background: rgba(142, 68, 173, 0.1);
    border-left: 3px solid #8e44ad;
  }
}

:deep(.item-tag) {
  color: #f39c12;
  font-weight: bold;
}

:deep(.number-value) {
  color: #e74c3c;
  font-weight: bold;
}

:deep(.status-effect) {
  color: #2ecc71;
  font-weight: bold;
  text-transform: uppercase;
}

.items-gained {
  background: rgba(46, 204, 113, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  
  h4 {
    color: #2ecc71;
    margin: 0 0 0.5rem 0;
  }
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  
  &.rare {
    border: 1px solid #9b59b6;
    box-shadow: 0 0 10px rgba(155, 89, 182, 0.3);
  }
  
  &.good {
    border: 1px solid #3498db;
    box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
  }
  
  &.common {
    border: 1px solid #95a5a6;
  }
}

.item-icon {
  font-size: 2rem;
  width: 50px;
  text-align: center;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: bold;
  color: #f39c12;
  margin-bottom: 0.2rem;
}

.item-description {
  color: #bbb;
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

.item-effect {
  color: #2ecc71;
  font-size: 0.8rem;
  font-style: italic;
}

.status-changes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.status-change {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.8rem;
  border-radius: 1rem;
  font-size: 0.9rem;
  
  &.positive {
    background: rgba(46, 204, 113, 0.2);
    color: #2ecc71;
  }
  
  &.negative {
    background: rgba(231, 76, 60, 0.2);
    color: #e74c3c;
  }
}

.choice-system {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  
  h4 {
    color: #f39c12;
    margin: 0 0 0.8rem 0;
  }
}

.choices-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.choice-option {
  padding: 1rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover:not(.disabled) {
    background: rgba(52, 152, 219, 0.1);
    border-color: #3498db;
  }
  
  &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  &.dangerous {
    border-color: #e74c3c;
    background: rgba(231, 76, 60, 0.1);
  }
}

.choice-text {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.choice-info {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #bbb;
}

.requirement {
  color: #f39c12;
}

.risk-level {
  color: #e74c3c;
}

.energy-cost {
  color: #3498db;
}

.story-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
}

.auto-play-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.story-history {
  max-height: 200px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-top: 1rem;
  
  h4 {
    color: #3498db;
    margin: 0 0 0.5rem 0;
  }
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.history-entry {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.5rem;
  border-radius: 0.3rem;
  cursor: pointer;
  transition: background 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.05);
  }
}

.history-chapter {
  color: #f39c12;
  font-weight: bold;
  min-width: 80px;
}

.history-content {
  flex: 1;
  color: #bbb;
  font-size: 0.9rem;
}

.history-time {
  color: #666;
  font-size: 0.8rem;
}
</style>
