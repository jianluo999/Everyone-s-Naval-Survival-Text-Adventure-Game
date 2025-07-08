<template>
  <div class="fishing-progress" v-if="visible">
    <div class="modal-overlay">
      <div class="progress-container">
        <div class="fishing-header">
          <h3>🎣 钓鱼中...</h3>
          <div class="spot-info">
            <span class="spot-name">{{ spotName }}</span>
            <span class="time-remaining">{{ timeRemaining }}秒</span>
          </div>
        </div>
        
        <div class="fishing-scene">
          <!-- 钓鱼动画区域 -->
          <div class="water-surface">
            <div class="fishing-line" :class="{ tension: hasTension }"></div>
            <div class="float" :class="{ bobbing: isBobbing, pulled: hasTension }"></div>
            <div class="ripples" v-if="showRipples">
              <div class="ripple" v-for="n in 3" :key="n"></div>
            </div>
          </div>
          
          <!-- 鱼类活动指示器 -->
          <div class="fish-activity">
            <div class="activity-bar">
              <div class="activity-fill" :style="{ width: `${fishActivity}%` }"></div>
            </div>
            <span class="activity-label">鱼类活动度: {{ fishActivity }}%</span>
          </div>
          
          <!-- 钓鱼技巧提示 -->
          <div class="fishing-tips" v-if="currentTip">
            <div class="tip-content">
              <span class="tip-icon">💡</span>
              <span class="tip-text">{{ currentTip }}</span>
            </div>
          </div>
        </div>
        
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
          <span class="progress-text">{{ Math.round(progress) }}%</span>
        </div>
        
        <!-- 钓鱼事件 -->
        <div class="fishing-events" v-if="currentEvent">
          <div class="event-message" :class="eventType">
            {{ currentEvent }}
          </div>
        </div>
        
        <!-- 取消按钮 -->
        <div class="action-buttons">
          <button class="cancel-btn" @click="cancelFishing">
            取消钓鱼
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  selectedSpot: {
    type: String,
    default: ''
  },
  fishingDuration: {
    type: Number,
    default: 15 // 默认15秒
  }
})

const emit = defineEmits(['fishing-complete', 'fishing-cancelled'])

// 钓鱼状态
const progress = ref(0)
const timeRemaining = ref(0)
const fishActivity = ref(50)
const isBobbing = ref(false)
const hasTension = ref(false)
const showRipples = ref(false)
const currentTip = ref('')
const currentEvent = ref('')
const eventType = ref('info')

let fishingTimer = null
let eventTimer = null
let activityTimer = null

// 钓点名称映射
const spotNames = {
  bow: '船头',
  port: '左舷',
  starboard: '右舷',
  stern: '船尾',
  captain: '船长专用钓点'
}

const spotName = computed(() => spotNames[props.selectedSpot] || '未知位置')

// 钓鱼技巧提示
const fishingTips = [
  '保持耐心，好鱼需要等待...',
  '注意浮标的动静，鱼儿可能在试探',
  '深海中隐藏着更珍贵的鱼类',
  '不同时间段鱼类活动度不同',
  '船只的稳定性影响钓鱼成功率',
  '经验丰富的渔夫知道何时收线',
  '有些鱼类只在特定条件下出现'
]

// 钓鱼事件消息
const fishingEvents = {
  nibble: { message: '有鱼在试探鱼饵...', type: 'info' },
  bite: { message: '鱼儿上钩了！', type: 'success' },
  escape: { message: '鱼儿逃脱了...', type: 'warning' },
  bigFish: { message: '感觉到了大鱼的存在！', type: 'success' },
  strange: { message: '水下似乎有什么奇怪的东西...', type: 'warning' },
  calm: { message: '海面很平静...', type: 'info' }
}

// 开始钓鱼
const startFishing = () => {
  if (!props.visible) return
  
  progress.value = 0
  timeRemaining.value = props.fishingDuration
  fishActivity.value = Math.random() * 40 + 30 // 30-70%
  
  // 显示初始提示
  showRandomTip()
  
  // 开始计时器
  fishingTimer = setInterval(() => {
    progress.value += (100 / props.fishingDuration)
    timeRemaining.value = Math.max(0, timeRemaining.value - 1)
    
    // 随机触发钓鱼事件
    if (Math.random() < 0.3) {
      triggerRandomEvent()
    }
    
    // 钓鱼完成
    if (progress.value >= 100) {
      completeFishing()
    }
  }, 1000)
  
  // 鱼类活动度变化
  activityTimer = setInterval(() => {
    fishActivity.value = Math.max(0, Math.min(100, 
      fishActivity.value + (Math.random() - 0.5) * 20
    ))
    
    // 根据活动度调整动画
    isBobbing.value = fishActivity.value > 60
    hasTension.value = fishActivity.value > 80
    showRipples.value = fishActivity.value > 70
  }, 2000)
  
  // 定期更换提示
  eventTimer = setInterval(() => {
    if (Math.random() < 0.4) {
      showRandomTip()
    }
  }, 5000)
}

// 显示随机提示
const showRandomTip = () => {
  const randomTip = fishingTips[Math.floor(Math.random() * fishingTips.length)]
  currentTip.value = randomTip
  
  setTimeout(() => {
    currentTip.value = ''
  }, 3000)
}

// 触发随机事件
const triggerRandomEvent = () => {
  const events = Object.keys(fishingEvents)
  const randomEvent = events[Math.floor(Math.random() * events.length)]
  const event = fishingEvents[randomEvent]
  
  currentEvent.value = event.message
  eventType.value = event.type
  
  // 根据事件类型调整鱼类活动度
  switch (randomEvent) {
    case 'nibble':
      fishActivity.value = Math.min(100, fishActivity.value + 10)
      break
    case 'bite':
      fishActivity.value = Math.min(100, fishActivity.value + 20)
      hasTension.value = true
      break
    case 'escape':
      fishActivity.value = Math.max(0, fishActivity.value - 15)
      break
    case 'bigFish':
      fishActivity.value = Math.min(100, fishActivity.value + 30)
      break
    case 'strange':
      fishActivity.value = Math.max(0, fishActivity.value - 10)
      break
  }
  
  setTimeout(() => {
    currentEvent.value = ''
    if (randomEvent === 'bite') {
      hasTension.value = false
    }
  }, 2000)
}

// 完成钓鱼
const completeFishing = () => {
  clearTimers()
  
  // 根据鱼类活动度和钓点计算结果
  const finalActivity = fishActivity.value
  const spotBonus = getSpotBonus(props.selectedSpot)
  const successChance = (finalActivity + spotBonus) / 2
  
  emit('fishing-complete', {
    spot: props.selectedSpot,
    activity: finalActivity,
    successChance: successChance,
    duration: props.fishingDuration
  })
}

// 取消钓鱼
const cancelFishing = () => {
  clearTimers()
  emit('fishing-cancelled')
}

// 获取钓点加成
const getSpotBonus = (spot) => {
  const bonuses = {
    bow: 20,
    port: 10,
    starboard: 15,
    stern: 5,
    captain: 30
  }
  return bonuses[spot] || 10
}

// 清理计时器
const clearTimers = () => {
  if (fishingTimer) {
    clearInterval(fishingTimer)
    fishingTimer = null
  }
  if (eventTimer) {
    clearInterval(eventTimer)
    eventTimer = null
  }
  if (activityTimer) {
    clearInterval(activityTimer)
    activityTimer = null
  }
}

// 监听可见性变化
watch(() => props.visible, (newVal) => {
  if (newVal) {
    startFishing()
  } else {
    clearTimers()
  }
})

onUnmounted(() => {
  clearTimers()
})
</script>

<style scoped>
.fishing-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2000;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.progress-container {
  background: linear-gradient(135deg, #1a4b5c 0%, #2d5a6b 100%);
  border: 3px solid #4a9eff;
  border-radius: 15px;
  padding: 30px;
  max-width: 600px;
  width: 90%;
  color: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.fishing-header {
  text-align: center;
  margin-bottom: 20px;
}

.fishing-header h3 {
  margin: 0 0 10px 0;
  font-size: 1.8em;
  color: #ffd700;
}

.spot-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 15px;
  border-radius: 8px;
}

.spot-name {
  font-weight: bold;
  color: #4a9eff;
}

.time-remaining {
  font-weight: bold;
  color: #ffd700;
  font-size: 1.2em;
}

.fishing-scene {
  position: relative;
  height: 200px;
  background: linear-gradient(180deg, #87CEEB 0%, #4682B4 50%, #191970 100%);
  border-radius: 10px;
  margin: 20px 0;
  overflow: hidden;
}

.water-surface {
  position: relative;
  width: 100%;
  height: 100%;
}

.fishing-line {
  position: absolute;
  top: 0;
  left: 50%;
  width: 2px;
  height: 60%;
  background: #8B4513;
  transform: translateX(-50%);
  transition: all 0.3s ease;
}

.fishing-line.tension {
  background: #ff4757;
  width: 3px;
  animation: lineTension 0.5s ease-in-out infinite alternate;
}

.float {
  position: absolute;
  top: 60%;
  left: 50%;
  width: 12px;
  height: 12px;
  background: #ff6b6b;
  border-radius: 50%;
  transform: translateX(-50%);
  transition: all 0.3s ease;
}

.float.bobbing {
  animation: bobbing 2s ease-in-out infinite;
}

.float.pulled {
  top: 50%;
  background: #ffd700;
  animation: pulled 0.5s ease-in-out infinite alternate;
}

.ripples {
  position: absolute;
  top: 65%;
  left: 50%;
  transform: translateX(-50%);
}

.ripple {
  position: absolute;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: ripple 2s ease-out infinite;
}

.ripple:nth-child(2) {
  animation-delay: 0.5s;
}

.ripple:nth-child(3) {
  animation-delay: 1s;
}

.fish-activity {
  position: absolute;
  bottom: 10px;
  left: 10px;
  right: 10px;
}

.activity-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.activity-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff4757, #ffd700, #2ed573);
  transition: width 0.5s ease;
}

.activity-label {
  font-size: 12px;
  color: white;
  margin-top: 5px;
  display: block;
}

.fishing-tips {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
}

.tip-content {
  background: rgba(0, 0, 0, 0.7);
  padding: 8px 12px;
  border-radius: 5px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tip-icon {
  font-size: 16px;
}

.progress-bar {
  position: relative;
  width: 100%;
  height: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  overflow: hidden;
  margin: 20px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4a9eff, #0066cc);
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: bold;
  color: white;
  font-size: 14px;
}

.fishing-events {
  margin: 15px 0;
  min-height: 30px;
}

.event-message {
  padding: 10px 15px;
  border-radius: 8px;
  font-weight: bold;
  text-align: center;
  animation: fadeInOut 2s ease-in-out;
}

.event-message.info {
  background: rgba(74, 158, 255, 0.2);
  border: 1px solid #4a9eff;
}

.event-message.success {
  background: rgba(46, 213, 115, 0.2);
  border: 1px solid #2ed573;
}

.event-message.warning {
  background: rgba(255, 215, 0, 0.2);
  border: 1px solid #ffd700;
}

.action-buttons {
  text-align: center;
  margin-top: 20px;
}

.cancel-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #ff4757, #cc3644);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #cc3644, #992733);
  transform: translateY(-2px);
}

/* 动画 */
@keyframes bobbing {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(-5px); }
}

@keyframes pulled {
  0% { transform: translateX(-50%) translateY(0); }
  100% { transform: translateX(-50%) translateY(-10px); }
}

@keyframes lineTension {
  0% { transform: translateX(-50%) rotate(-2deg); }
  100% { transform: translateX(-50%) rotate(2deg); }
}

@keyframes ripple {
  0% {
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    width: 60px;
    height: 60px;
    opacity: 0;
  }
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(10px); }
  20% { opacity: 1; transform: translateY(0); }
  80% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-10px); }
}
</style>
