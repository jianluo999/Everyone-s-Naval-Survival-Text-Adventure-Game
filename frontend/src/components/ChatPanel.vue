<template>
  <div class="chat-panel">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <div class="chat-title">
        <el-icon><ChatRound /></el-icon>
        <span>航海日志</span>
      </div>
      
      <!-- 频道切换 -->
      <el-tabs v-model="activeTab" class="chat-tabs" size="small">
        <el-tab-pane label="世界" name="world">
          <template #label>
            <span class="tab-label">
              <el-icon><Globe /></el-icon>
              世界
            </span>
          </template>
        </el-tab-pane>
        
        <el-tab-pane label="区域" name="region">
          <template #label>
            <span class="tab-label">
              <el-icon><Location /></el-icon>
              区域
            </span>
          </template>
        </el-tab-pane>
        
        <el-tab-pane label="系统" name="system">
          <template #label>
            <span class="tab-label">
              <el-icon><Bell /></el-icon>
              系统
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 聊天消息区域 -->
    <div class="chat-content" ref="chatContentRef">
      <div class="messages-container">
        <!-- 系统消息 -->
        <div v-if="activeTab === 'system'" class="system-messages">
          <div 
            v-for="message in systemMessages" 
            :key="message.id"
            class="message-item system-message"
          >
            <div class="message-header">
              <el-icon class="message-icon"><Notification /></el-icon>
              <span class="message-time">{{ formatTime(message.time) }}</span>
            </div>
            <div class="message-content" v-html="message.content"></div>
          </div>
        </div>

        <!-- 世界/区域聊天 -->
        <div v-else class="chat-messages">
          <div 
            v-for="message in currentMessages" 
            :key="message.id"
            class="message-item chat-message"
          >
            <div class="message-header">
              <span class="player-name">{{ message.playerName }}</span>
              <span class="message-time">{{ formatTime(message.time) }}</span>
            </div>
            <div class="message-content">{{ message.content }}</div>
          </div>
          
          <!-- 无消息提示 -->
          <div v-if="currentMessages.length === 0" class="no-messages">
            <el-icon class="empty-icon"><ChatRound /></el-icon>
            <p>暂无{{ activeTab === 'world' ? '世界' : '区域' }}消息</p>
            <p class="tip">成为第一个发言的人吧！</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 消息输入区域 -->
    <div class="chat-input" v-if="activeTab !== 'system'">
      <div class="input-container">
        <el-input
          v-model="inputMessage"
          placeholder="输入消息..."
          maxlength="200"
          show-word-limit
          :disabled="sending"
          @keyup.enter="sendMessage"
          class="message-input"
        >
          <template #prepend>
            <el-icon><Edit /></el-icon>
          </template>
        </el-input>
        
        <el-button 
          type="primary" 
          @click="sendMessage"
          :disabled="!inputMessage.trim() || sending"
          :loading="sending"
          class="send-btn"
        >
          <el-icon><Promotion /></el-icon>
        </el-button>
      </div>
      
      <!-- 快捷消息 -->
      <div class="quick-messages">
        <el-button 
          v-for="quick in quickMessages" 
          :key="quick"
          size="small"
          type="info"
          plain
          @click="inputMessage = quick"
          class="quick-btn"
        >
          {{ quick }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'

// Emits
const emit = defineEmits(['messages-read'])

const gameStore = useGameStore()

// 响应式数据
const activeTab = ref('system')
const inputMessage = ref('')
const sending = ref(false)
const chatContentRef = ref(null)

// 模拟消息数据
const worldMessages = ref([
  {
    id: 1,
    playerName: '冒险者小明',
    content: '有人吗？这游戏太真实了！',
    time: new Date(Date.now() - 300000)
  },
  {
    id: 2,
    playerName: '海上老兵',
    content: '新人建议先熟悉航海日志的功能',
    time: new Date(Date.now() - 240000)
  },
  {
    id: 3,
    playerName: '探索者萨拉',
    content: '我的船刚刚遇到了海怪！差点沉了...',
    time: new Date(Date.now() - 180000)
  }
])

const regionMessages = ref([
  {
    id: 1,
    playerName: '附近的船长',
    content: '这片海域有黑雾接近，大家小心！',
    time: new Date(Date.now() - 120000)
  }
])

const systemMessages = ref([
  {
    id: 1,
    content: '<strong>🎮 欢迎来到全民航海求生游戏！</strong><br/>你已成功觉醒，开始你的海上冒险之旅。',
    time: new Date(Date.now() - 600000)
  },
  {
    id: 2,
    content: '<strong>📖 游戏提示：</strong><br/>• 查看航海日志了解游戏规则<br/>• 注意船只状态和资源管理<br/>• 小心后方追来的黑雾',
    time: new Date(Date.now() - 480000)
  },
  {
    id: 3,
    content: '<strong>⚠️ 黑雾警告：</strong><br/>黑雾正在以10节的速度向前推进，请保持船只前进！',
    time: new Date(Date.now() - 360000)
  }
])

// 快捷消息
const quickMessages = [
  '有人吗？',
  '求助！',
  '这里有物资',
  '小心黑雾！',
  '有交易需求'
]

// 计算属性
const currentMessages = computed(() => {
  switch (activeTab.value) {
    case 'world':
      return worldMessages.value
    case 'region':
      return regionMessages.value
    case 'system':
      return systemMessages.value
    default:
      return []
  }
})

// 监听tab切换，滚动到底部并触发消息已读事件
watch(activeTab, () => {
  nextTick(() => {
    scrollToBottom()
  })
  // 触发消息已读事件
  emit('messages-read')
})

// 生命周期
onMounted(() => {
  // 添加欢迎消息
  addSystemMessage('欢迎船长 ' + (gameStore.player?.name || '未知') + ' 加入游戏！')
  
  // 模拟定期收到消息
  startMessageSimulation()
  
  scrollToBottom()
})

// 方法
const formatTime = (time) => {
  const now = new Date()
  const diff = now - time
  
  if (diff < 60000) { // 1分钟内
    return '刚刚'
  } else if (diff < 3600000) { // 1小时内
    return Math.floor(diff / 60000) + '分钟前'
  } else if (diff < 86400000) { // 24小时内
    return Math.floor(diff / 3600000) + '小时前'
  } else {
    return time.toLocaleDateString()
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  
  sending.value = true
  
  try {
    // 模拟发送延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const newMessage = {
      id: Date.now(),
      playerName: gameStore.player?.name || '匿名船长',
      content: inputMessage.value.trim(),
      time: new Date()
    }
    
    // 添加到对应频道
    if (activeTab.value === 'world') {
      worldMessages.value.push(newMessage)
    } else if (activeTab.value === 'region') {
      regionMessages.value.push(newMessage)
    }
    
    inputMessage.value = ''
    ElMessage.success('消息发送成功')
    
    // 滚动到底部
    nextTick(() => {
      scrollToBottom()
    })
    
  } catch (err) {
    ElMessage.error('消息发送失败')
  } finally {
    sending.value = false
  }
}

const addSystemMessage = (content) => {
  systemMessages.value.push({
    id: Date.now(),
    content: content,
    time: new Date()
  })
  
  // 限制系统消息数量
  if (systemMessages.value.length > 50) {
    systemMessages.value = systemMessages.value.slice(-50)
  }
}

// 记录玩家选择
const recordPlayerChoice = (choice, storyTitle) => {
  let effectText = ''
  
  // 记录选择效果
  const effects = []
  if (choice.goldCost > 0) effects.push(`-${choice.goldCost}金币`)
  if (choice.goldReward > 0) effects.push(`+${choice.goldReward}金币`)
  if (choice.healthCost > 0) effects.push(`-${choice.healthCost}生命`)
  if (choice.healthReward > 0) effects.push(`+${choice.healthReward}生命`)
  if (choice.experienceReward > 0) effects.push(`+${choice.experienceReward}经验`)
  
  if (effects.length > 0) {
    effectText = `<br/><span style="color: #00ffc8; font-size: 0.9em;">效果：${effects.join('，')}</span>`
  }
  
  const choiceRecord = `<strong>🎯 选择记录：</strong><br/>` +
    `<span style="color: #66ffcc;">「${storyTitle}」</span><br/>` +
    `选择：${choice.text}${effectText}`
  
  addSystemMessage(choiceRecord)
  
  // 如果当前在系统频道，滚动到底部
  if (activeTab.value === 'system') {
    nextTick(() => {
      scrollToBottom()
    })
  }
}

const scrollToBottom = () => {
  if (chatContentRef.value) {
    chatContentRef.value.scrollTop = chatContentRef.value.scrollHeight
  }
}

const startMessageSimulation = () => {
  // 模拟其他玩家消息
  const simulatedMessages = [
    { player: '深海探险家', content: '发现了一个神秘岛屿！', delay: 30000 },
    { player: '商人船长', content: '有人需要交易食物吗？', delay: 60000 },
    { player: '老练水手', content: '暴风雨要来了，大家做好准备', delay: 90000 }
  ]
  
  simulatedMessages.forEach((msg, index) => {
    setTimeout(() => {
      if (Math.random() > 0.5) { // 随机决定是否发送
        worldMessages.value.push({
          id: Date.now() + index,
          playerName: msg.player,
          content: msg.content,
          time: new Date()
        })
        
        // 如果当前在世界频道，滚动到底部
        if (activeTab.value === 'world') {
          nextTick(() => {
            scrollToBottom()
          })
        }
      }
    }, msg.delay)
  })
  
  // 模拟系统公告
  setTimeout(() => {
    addSystemMessage('<strong>🌊 海况更新：</strong><br/>海面风力增强，建议加强船只防护')
  }, 45000)
}

// 暴露方法供外部组件调用
defineExpose({
  recordPlayerChoice,
  addSystemMessage
})
</script>

<style lang="scss" scoped>
.chat-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(0, 30, 25, 0.95);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
}

.chat-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
  
  .chat-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 1rem;
    text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
    font-family: 'Consolas', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
    letter-spacing: 0.5px;
    
    .el-icon {
      color: #ffffff;
    }
  }
  
  .chat-tabs {
    :deep(.el-tabs__header) {
      margin: 0;
    }
    
    .tab-label {
      display: flex;
      align-items: center;
      gap: 0.3rem;
      font-size: 0.8rem;
    }
  }
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  
  .messages-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .message-item {
    padding: 0.8rem;
    border-radius: 8px;
    
    .message-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.5rem;
      
      .player-name {
        font-weight: 500;
        color: #ffffff;
        font-size: 0.9rem;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
        font-family: 'Consolas', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
        letter-spacing: 0.3px;
      }
      
      .message-icon {
        color: #67C23A;
      }
      
      .message-time {
        font-size: 0.7rem;
        color: #999;
      }
    }
    
    .message-content {
      line-height: 1.5;
      color: #ffffff;
      font-size: 0.9rem;
      text-shadow: 0 0 5px rgba(255, 255, 255, 0.6);
      font-family: 'Consolas', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
      font-weight: 400;
      letter-spacing: 0.2px;
    }
  }
  
  .system-message {
    background: rgba(0, 80, 60, 0.6);
    border-left: 4px solid #00ff88;
    
    .message-content {
      :deep(strong) {
        color: #00ff88;
      }
    }
  }
  
  .chat-message {
    background: rgba(0, 40, 35, 0.6);
    border-left: 4px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    
    &:hover {
      background: rgba(0, 60, 50, 0.8);
      border-left-color: #00ff88;
    }
  }
  
  .no-messages {
    text-align: center;
    padding: 3rem 1rem;
    color: #999;
    
    .empty-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      opacity: 0.5;
    }
    
    p {
      margin: 0.5rem 0;
      
      &.tip {
        font-size: 0.8rem;
        font-style: italic;
      }
    }
  }
}

.chat-input {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
  
  .input-container {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
    
    .message-input {
      flex: 1;
    }
    
    .send-btn {
      width: 40px;
      padding: 0;
      border-radius: 20px;
    }
  }
  
  .quick-messages {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    
    .quick-btn {
      font-size: 0.7rem;
      padding: 0.3rem 0.6rem;
      border-radius: 12px;
      
      &:hover {
        transform: translateY(-1px);
      }
    }
  }
}

// 滚动条样式
.chat-content {
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
    
    &:hover {
      background: #a8a8a8;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .chat-header {
    padding: 0.8rem;
  }
  
  .chat-content {
    padding: 0.8rem;
  }
  
  .chat-input {
    padding: 0.8rem;
    
    .input-container {
      flex-direction: column;
      
      .send-btn {
        width: 100%;
        border-radius: 25px;
      }
    }
    
    .quick-messages {
      justify-content: center;
    }
  }
}
</style> 