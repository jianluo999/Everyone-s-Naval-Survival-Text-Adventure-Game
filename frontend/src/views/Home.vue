<template>
  <div class="home-container">
    <!-- 背景动画效果 -->
    <div class="ocean-waves">
      <div class="wave wave1"></div>
      <div class="wave wave2"></div>
      <div class="wave wave3"></div>
    </div>
    
    <!-- 浮动粒子效果 -->
    <div class="particles">
      <div v-for="i in 20" :key="i" class="particle" :style="getParticleStyle(i)"></div>
    </div>

    <!-- 游戏标题 -->
    <div class="game-header">
      <h1 class="game-title">
        <span class="ship-icon">🚢</span>
        <span class="title-text">全民航海求生游戏</span>
        <span class="ship-icon">⚓</span>
      </h1>
      <p class="game-subtitle typewriter">在无尽的海洋中，书写你的传奇故事</p>
    </div>

    <!-- 游戏介绍 -->
    <div class="game-intro">
      <el-card class="intro-card glass-effect">
        <template #header>
          <div class="card-header">
            <el-icon class="header-icon"><Compass /></el-icon>
            <span>游戏背景</span>
            <el-icon class="header-icon"><Compass /></el-icon>
          </div>
        </template>
        <div class="intro-content">
          <div class="intro-text">
            <p class="highlight-text">「欢迎来到全民航海求生游戏...」</p>
            <p>接下来，你们将在海上度过余生...</p>
            <p>不必担心你们身体有疾病或者残缺，本系统会帮你们通通治好，给你们一个相对公平的起点...</p>
            <p class="highlight danger-text">
              <el-icon class="warning-icon"><Warning /></el-icon>
              保持前进，不要被背后的黑雾追上。
            </p>
            <p class="warning critical-text">
              <el-icon class="danger-icon pulse"><Lightning /></el-icon>
              黑雾的速度目前为十节！
            </p>
          </div>
          
          <!-- 添加装饰性元素 -->
          <div class="decoration-elements">
            <div class="compass-decoration">🧭</div>
            <div class="anchor-decoration">⚓</div>
            <div class="wheel-decoration rotating">⛵</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 玩家操作区域 -->
    <div class="player-actions">
      <el-card class="action-card glass-effect">
        <template #header>
          <div class="card-header">
            <el-icon class="header-icon"><Sail /></el-icon>
            <span>开始你的航海之旅</span>
            <el-icon class="header-icon"><Sail /></el-icon>
          </div>
        </template>
        
        <div class="action-content">
          <div class="input-section">
            <div class="input-wrapper">
              <el-input
                v-model="playerName"
                placeholder="请输入你的船长名字"
                size="large"
                maxlength="20"
                show-word-limit
                :disabled="loading"
                @keyup.enter="handleStartGame"
                class="captain-input"
              >
                <template #prepend>
                  <el-icon><User /></el-icon>
                  <span>船长</span>
                </template>
              </el-input>
            </div>
          </div>

          <div class="button-section">
            <el-button 
              type="primary" 
              size="large" 
              :loading="loading"
              :disabled="!playerName.trim()"
              @click="handleStartGame"
              class="start-btn magical-btn"
            >
              <el-icon class="btn-icon"><Promotion /></el-icon>
              <span>开始新游戏</span>
              <div class="btn-effects"></div>
            </el-button>

            <el-button 
              type="success" 
              size="large" 
              :loading="loading"
              :disabled="!playerName.trim()"
              @click="handleContinueGame"
              class="continue-btn magical-btn"
            >
              <el-icon class="btn-icon"><RefreshRight /></el-icon>
              <span>继续游戏</span>
              <div class="btn-effects"></div>
            </el-button>
          </div>

          <!-- 错误提示 -->
          <div v-if="error" class="error-message">
            <el-alert
              :title="error"
              type="error"
              :closable="false"
              show-icon
              effect="dark"
            />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 游戏特色 -->
    <div class="game-features">
      <div class="feature-grid">
        <div class="feature-item glass-effect" v-for="(feature, index) in features" :key="index">
          <div class="feature-icon" :style="{ animationDelay: (index * 0.2) + 's' }">
            {{ feature.icon }}
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
          <div class="feature-decoration"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'

const router = useRouter()
const gameStore = useGameStore()

// 响应式数据
const playerName = ref('')
const loading = ref(false)
const error = ref('')

// 游戏特色数据
const features = [
  {
    icon: '⚔️',
    title: '属性系统',
    description: '力量、精神、敏捷、体质、感知五大属性，打造专属角色'
  },
  {
    icon: '🧠',
    title: '理智机制',
    description: '保持理智，避免陷入疯狂，钢铁意志助你渡过难关'
  },
  {
    icon: '⛵',
    title: '船只升级',
    description: '从破旧木筏到强大战舰，不断升级你的海上家园'
  },
  {
    icon: '🌊',
    title: '海洋探索',
    description: '神秘的海域等待你的探索，每个选择都影响命运'
  }
]

// 粒子样式生成
const getParticleStyle = (index) => {
  const delay = Math.random() * 20
  const duration = 15 + Math.random() * 10
  const left = Math.random() * 100
  const size = 2 + Math.random() * 3
  
  return {
    left: left + '%',
    animationDelay: delay + 's',
    animationDuration: duration + 's',
    width: size + 'px',
    height: size + 'px'
  }
}

// 开始新游戏
const handleStartGame = async () => {
  if (!playerName.value.trim()) {
    ElMessage.warning('请输入船长名字')
    return
  }

  loading.value = true
  error.value = ''

  try {
    await gameStore.createPlayer(playerName.value.trim())
    ElMessage.success('欢迎登船，船长！')
    router.push('/game')
  } catch (err) {
    error.value = err.message || '发生未知错误'
    ElMessage.error(err.message || '发生未知错误')
  } finally {
    loading.value = false
  }
}

// 继续游戏
const handleContinueGame = async () => {
  if (!playerName.value.trim()) {
    ElMessage.warning('请输入船长名字')
    return
  }

  loading.value = true
  error.value = ''

  try {
    await gameStore.loadPlayer(playerName.value.trim())
    ElMessage.success('欢迎回来，船长！')
    router.push('/game')
  } catch (err) {
    error.value = err.message || '发生未知错误'
    ElMessage.error(err.message || '发生未知错误')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.home-container {
  min-height: 100vh;
  position: relative;
  padding: 2rem;
  overflow: hidden;
  background: linear-gradient(135deg, #0f2027 0%, #203a43 25%, #2c5364 75%, #1e3c72 100%);
}

// 海浪动画
.ocean-waves {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  z-index: 1;
  
  .wave {
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 200%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    border-radius: 50%;
    transform: translateX(-50%);
    animation: wave 6s ease-in-out infinite;
    
    &.wave1 {
      animation-delay: 0s;
      opacity: 0.3;
    }
    
    &.wave2 {
      animation-delay: 2s;
      opacity: 0.2;
      animation-duration: 8s;
    }
    
    &.wave3 {
      animation-delay: 4s;
      opacity: 0.1;
      animation-duration: 10s;
    }
  }
}

@keyframes wave {
  0%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-20px);
  }
}

// 粒子效果
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
  
  .particle {
    position: absolute;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    animation: float-up linear infinite;
  }
}

@keyframes float-up {
  0% {
    opacity: 0;
    transform: translateY(100vh) rotate(0deg);
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateY(-100px) rotate(360deg);
  }
}

.game-header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
  z-index: 10;
  
  .game-title {
    font-size: 4rem;
    font-weight: 900;
    margin-bottom: 1rem;
    color: #ffffff;
    text-shadow: 
      0 0 10px rgba(255, 255, 255, 0.5),
      0 0 20px rgba(64, 158, 255, 0.3),
      0 0 30px rgba(64, 158, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    
    .ship-icon {
      animation: float 3s ease-in-out infinite;
      filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
    }
    
    .title-text {
      background: linear-gradient(45deg, #ffffff, #64b5f6, #ffffff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      animation: shimmer 3s ease-in-out infinite;
    }
  }
  
  .game-subtitle {
    font-size: 1.3rem;
    color: #b3d4fc;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
}

@keyframes shimmer {
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.2); }
}

// 玻璃效果
.glass-effect {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.game-intro, .player-actions {
  position: relative;
  z-index: 10;
  max-width: 800px;
  margin: 0 auto 3rem;
  
  .intro-card, .action-card {
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
      animation: slide 3s infinite;
    }
  }
}

@keyframes slide {
  0% { left: -100%; }
  100% { left: 100%; }
}

.decoration-elements {
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  opacity: 0.3;
  
  div {
    font-size: 2rem;
    animation: float 4s ease-in-out infinite;
    
    &.rotating {
      animation: rotate 8s linear infinite;
    }
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

// 魔法按钮效果
.magical-btn {
  position: relative;
  overflow: hidden;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
  }
  
  .btn-effects {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    animation: shimmer-btn 2s infinite;
  }
}

@keyframes shimmer-btn {
  0% { left: -100%; }
  100% { left: 100%; }
}

.start-btn {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%) !important;
}

.continue-btn {
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%) !important;
}

.captain-input {
  .el-input__wrapper {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    color: white;
    
    .el-input__inner {
      color: white;
      
      &::placeholder {
        color: rgba(255, 255, 255, 0.6);
      }
    }
  }
}

// 特色功能区域
.game-features {
  position: relative;
  z-index: 10;
  max-width: 1200px;
  margin: 0 auto;
  
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    
    .feature-item {
      position: relative;
      padding: 2.5rem;
      border-radius: 20px;
      text-align: center;
      transition: all 0.4s ease;
      overflow: hidden;
      
      &:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
      }
      
      .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        animation: bounce 2s infinite;
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
      }
      
      h3 {
        color: #ffffff;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
      }
      
      p {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
        margin: 0;
      }
      
      .feature-decoration {
        position: absolute;
        bottom: -50px;
        right: -50px;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1), transparent);
        border-radius: 50%;
        animation: pulse 3s infinite;
      }
    }
  }
}

// 高亮文本样式
.highlight-text {
  color: #64b5f6;
  font-weight: bold;
  font-size: 1.1rem;
}

.danger-text {
  color: #ff7043;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  .warning-icon {
    animation: pulse 2s infinite;
  }
}

.critical-text {
  color: #f44336;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  .danger-icon {
    color: #ffeb3b;
  }
}

.typewriter {
  border-right: 2px solid #64b5f6;
  overflow: hidden;
  white-space: nowrap;
  animation: typing 4s steps(20, end), blink-caret 0.75s step-end infinite;
}

@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}

@keyframes blink-caret {
  from, to { border-color: transparent; }
  50% { border-color: #64b5f6; }
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  font-weight: bold;
  font-size: 1.3rem;
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  
  .header-icon {
    font-size: 1.5rem;
    color: #64b5f6;
    animation: pulse 2s infinite;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .home-container {
    padding: 1rem;
  }
  
  .game-header .game-title {
    font-size: 2.5rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .button-section {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .decoration-elements {
    display: none;
  }
}
</style> 