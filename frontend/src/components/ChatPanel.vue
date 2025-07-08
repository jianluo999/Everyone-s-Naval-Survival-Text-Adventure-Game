<template>
  <div class="chat-panel">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <div class="chat-title">
        <el-icon><ChatRound /></el-icon>
        <span>航海日志</span>
        <!-- 连接状态指示器 -->
        <div class="connection-status" :class="connectionStatus">
          <el-icon v-if="connectionStatus === 'connected'"><SuccessFilled /></el-icon>
          <el-icon v-else-if="connectionStatus === 'connecting'"><Loading /></el-icon>
          <el-icon v-else><WarningFilled /></el-icon>
          <span class="status-text">
            {{ connectionStatus === 'connected' ? '已连接' :
               connectionStatus === 'connecting' ? '连接中' : '未连接' }}
          </span>
        </div>
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

        <el-tab-pane label="交易" name="trade">
          <template #label>
            <span class="tab-label">
              <el-icon><ShoppingBag /></el-icon>
              交易
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

        <!-- 交易频道 -->
        <div v-else-if="activeTab === 'trade'" class="trade-panel">
          <EnhancedTrading />
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
              <span class="message-time">{{ formatTime(message.timestamp || message.time) }}</span>
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
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useGameStore } from '@/stores/game'
import { useChatStore } from '@/stores/chat'
import { ElMessage } from 'element-plus'
import EnhancedTrading from './EnhancedTrading.vue'

// Emits
const emit = defineEmits(['messages-read'])

const gameStore = useGameStore()
const chatStore = useChatStore()

// 响应式数据
const activeTab = ref('system')
const inputMessage = ref('')
const sending = ref(false)
const chatContentRef = ref(null)

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
  return chatStore.getChannelMessages(activeTab.value)
})

// 连接状态
const connectionStatus = computed(() => chatStore.connectionStatus)
const isConnected = computed(() => chatStore.connected)

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
  // 初始化聊天连接
  initializeChat()

  // 监听玩家状态变化
  watch(() => gameStore.player, (newPlayer) => {
    if (newPlayer?.name && !chatStore.connected) {
      initializeChat()
    }
  }, { immediate: true })

  scrollToBottom()
})

onUnmounted(() => {
  // 断开WebSocket连接
  chatStore.disconnect()
})

// 方法
const formatTime = (time) => {
  if (!time) return ''

  // 处理后端返回的时间戳格式
  const messageTime = typeof time === 'string' ? new Date(time) : time
  const now = new Date()
  const diff = now - messageTime

  if (diff < 60000) { // 1分钟内
    return '刚刚'
  } else if (diff < 3600000) { // 1小时内
    return Math.floor(diff / 60000) + '分钟前'
  } else if (diff < 86400000) { // 24小时内
    return Math.floor(diff / 3600000) + '小时前'
  } else {
    return messageTime.toLocaleDateString()
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return

  sending.value = true

  try {
    // 使用WebSocket发送消息
    const success = chatStore.sendMessage(inputMessage.value.trim(), activeTab.value)

    if (success) {
      inputMessage.value = ''

      // 滚动到底部
      nextTick(() => {
        scrollToBottom()
      })
    }

  } catch (err) {
    console.error('发送消息失败:', err)
    ElMessage.error('消息发送失败')
  } finally {
    sending.value = false
  }
}

const addSystemMessage = (content) => {
  // 系统消息现在通过WebSocket处理
  console.log('系统消息:', content)
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

// 初始化聊天连接
const initializeChat = () => {
  if (gameStore.player?.name && !chatStore.connected) {
    console.log('🔗 [CHAT] 初始化聊天连接 - 玩家:', gameStore.player.name)
    chatStore.connect(gameStore.player.name)
  }
}

// 交易相关方法
const getTradeTypeText = (type) => {
  return type === 'sell' ? '🏪 出售' : '🛒 求购'
}

const contactTrader = (tradeMessage) => {
  ElMessage.info(`正在联系 ${tradeMessage.playerName}...`)
  // 这里可以实现私聊或交易界面
}

const addTradeMessage = (tradeData) => {
  // 交易消息现在通过WebSocket处理
  console.log('交易消息:', tradeData)
}

// 暴露方法供外部组件调用
defineExpose({
  recordPlayerChoice,
  addSystemMessage,
  addTradeMessage
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
    justify-content: space-between;
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

    .connection-status {
      display: flex;
      align-items: center;
      gap: 0.3rem;
      font-size: 0.8rem;
      padding: 0.2rem 0.5rem;
      border-radius: 12px;
      background: rgba(0, 0, 0, 0.3);

      &.connected {
        color: #67C23A;
        .el-icon {
          color: #67C23A;
        }
      }

      &.connecting {
        color: #E6A23C;
        .el-icon {
          color: #E6A23C;
          animation: spin 1s linear infinite;
        }
      }

      &.disconnected {
        color: #F56C6C;
        .el-icon {
          color: #F56C6C;
        }
      }

      .status-text {
        font-size: 0.7rem;
      }
    }
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
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