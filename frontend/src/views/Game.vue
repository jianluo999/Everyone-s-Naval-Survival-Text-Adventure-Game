<template>
  <div class="game-container deep-sea-game">
    <!-- 深海迷雾效果 -->
    <div class="deep-sea-fog"></div>
    
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
      
      <!-- 头部信息栏 -->
      <div class="game-header deep-sea-header">
        <div class="header-decoration left-decoration"></div>
        <div class="header-content">
          <PlayerStatus class="deep-sea-player-status" />
          <ShipStatus class="deep-sea-ship-status" />
        </div>
        <div class="header-decoration right-decoration"></div>
      </div>

      <!-- 游戏内容区域 -->
      <div class="game-content deep-sea-content">
        <!-- 深海故事展示区 -->
        <div class="story-section deep-sea-story-section">
          <div class="story-frame">
            <div class="frame-corner top-left"></div>
            <div class="frame-corner top-right"></div>
            <div class="frame-corner bottom-left"></div>
            <div class="frame-corner bottom-right"></div>
            <StoryDisplay class="deep-sea-story-display" />
          </div>
        </div>

        <!-- 深海聊天区域 -->
        <div class="chat-section deep-sea-chat-section">
          <div class="chat-frame">
            <div class="frame-glow"></div>
            <ChatPanel class="deep-sea-chat-panel" />
          </div>
        </div>

        <!-- 深海钓鱼区域 -->
        <div class="fishing-section deep-sea-fishing-section">
          <div class="fishing-frame">
            <div class="frame-glow fishing-glow"></div>
            <FishingPanel class="deep-sea-fishing-panel" />
          </div>
        </div>
      </div>

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
import { ArrowLeft, Document, Loading } from '@element-plus/icons-vue'

// 组件导入
import PlayerStatus from '@/components/PlayerStatus.vue'
import ShipStatus from '@/components/ShipStatus.vue'
import StoryDisplay from '@/components/StoryDisplay.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import FishingPanel from '@/components/FishingPanel.vue'

const router = useRouter()
const gameStore = useGameStore()

// 响应式数据
const loading = ref(false)
const saving = ref(false)

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
</script>

<style lang="scss" scoped>
.game-container {
  min-height: 100vh;
  position: relative;
  padding: 1rem;
  padding-bottom: 120px; // 为底部操作栏留出空间
}

.deep-sea-game {
  background: 
    radial-gradient(ellipse at 30% 20%, rgba(0, 40, 80, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 80%, rgba(0, 60, 120, 0.2) 0%, transparent 50%),
    linear-gradient(180deg, rgba(0, 10, 20, 0.8) 0%, rgba(0, 5, 15, 0.9) 50%, rgba(0, 0, 0, 0.95) 100%);
  
  // 深海迷雾效果
  .deep-sea-fog {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
      radial-gradient(ellipse at 20% 30%, rgba(102, 255, 204, 0.05) 0%, transparent 40%),
      radial-gradient(ellipse at 80% 70%, rgba(0, 255, 127, 0.03) 0%, transparent 40%);
    animation: fog-drift 25s ease-in-out infinite;
    pointer-events: none;
    z-index: 1;
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

// 深海头部
.deep-sea-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
  
  .header-decoration {
    width: 100px;
    height: 3px;
    background: linear-gradient(90deg, transparent, rgba(102, 255, 204, 0.6), transparent);
    position: relative;
    
    &::before {
      content: '◆';
      position: absolute;
      top: -8px;
      color: #66ffcc;
      font-size: 1.2rem;
      text-shadow: 0 0 10px rgba(102, 255, 204, 0.8);
    }
    
    &.left-decoration::before {
      left: 0;
    }
    
    &.right-decoration::before {
      right: 0;
    }
  }
  
  .header-content {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 0 2rem;
  }
}

// 深海内容区域
.deep-sea-content {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
  min-height: 500px;
}

// 深海故事区域
.deep-sea-story-section {
  .story-frame {
    position: relative;
    height: 100%;
    
    .frame-corner {
      position: absolute;
      width: 20px;
      height: 20px;
      border: 2px solid rgba(102, 255, 204, 0.6);
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
  .chat-frame {
    position: relative;
    height: 100%;
    
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

// 深海钓鱼区域
.deep-sea-fishing-section {
  .fishing-frame {
    position: relative;
    height: 100%;
    
    .frame-glow.fishing-glow {
      position: absolute;
      top: -5px;
      left: -5px;
      right: -5px;
      bottom: -5px;
      background: linear-gradient(45deg, 
        rgba(255, 107, 107, 0.15) 0%, 
        rgba(255, 140, 140, 0.08) 25%, 
        rgba(255, 107, 107, 0.15) 50%, 
        rgba(255, 140, 140, 0.08) 75%, 
        rgba(255, 107, 107, 0.15) 100%);
      border-radius: 20px;
      animation: fishing-glow-pulse 3s ease-in-out infinite;
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

@keyframes fishing-glow-pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}

@keyframes portal-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

// 响应式适配
@media (max-width: 1024px) {
  .deep-sea-content {
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  
  .deep-sea-header .header-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 900px) {
  .deep-sea-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .game-container {
    padding: 0.5rem;
    padding-bottom: 100px;
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
  
  .deep-sea-header .header-decoration {
    display: none;
  }
}
</style> 