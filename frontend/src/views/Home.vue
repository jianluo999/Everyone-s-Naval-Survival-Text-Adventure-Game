<template>
  <div class="retro-game-container">
    <!-- CRT显示器效果 -->
    <div class="crt-screen">
      <div class="scanlines"></div>
      <div class="crt-content">
        
        <!-- 游戏标题 -->
        <div class="game-header">
          <div class="title-line">==============<br></div>
          <div class="game-title">
            <span class="blink">►</span> 全民航海求生游戏 <span class="blink">◄</span>
          </div>
          <div class="subtitle">[ 在无尽的海洋中，书写你的传奇故事 ]</div>
          <div class="title-line">==============<br></div>
        </div>

        <!-- 游戏介绍 -->
        <div v-if="showIntro" class="game-intro" @click="showIntro = false" @keyup="showIntro = false">
          <div class="intro-text">
            <div class="title">游戏介绍</div>
            <div class="welcome">「欢迎来到航海求生的危险海域！」</div>
            <div class="description">
              这里没有怯懦者的立足之地，只有勇敢的冒险者才能在<br>
              这无情的大海中生存下来。您将面临种种挑战：
            </div>
            <div class="challenges">
              <div>▲ 饥饿、口渴、海怪</div>
              <div>▲ 无数不可预知的危险</div>
              <div>▲ 生存还是毁灭？</div>
            </div>
            <div class="ready">准备好开始您的传奇航程了吗？</div>
            <div class="continue blink">[ 按任意键继续 ]</div>
          </div>
        </div>

        <!-- 主菜单 -->
        <div class="main-menu" v-if="!showIntro">
          <div class="menu-header">
                                    主菜单 - MAIN MENU<br>
          </div>

          <!-- 输入区域 -->
          <div class="input-section">
            <div class="input-label">
              ▶ 输入船长名字 (CAPTAIN NAME):
            </div>
            <div class="input-field">
              <input 
                v-model="playerName" 
                type="text" 
                placeholder="请输入船长名字"
                class="retro-input"
                maxlength="20"
                @keypress.enter="handleStartGame"
              />
            </div>
          </div>

          <!-- 菜单选项 -->
          <div class="menu-options">
            <div class="option-item" @click="handleStartGame" :class="{ disabled: !playerName.trim() }">
              <span class="option-arrow">►</span> 1. 开始新游戏 (NEW GAME)
            </div>
            <div class="option-item" @click="handleContinueGame" :class="{ disabled: !playerName.trim() }">
              <span class="option-arrow">►</span> 2. 继续游戏 (CONTINUE)
            </div>
            <div class="option-item" @click="showFeatures = !showFeatures">
              <span class="option-arrow">►</span> 3. 游戏特色 (FEATURES)
            </div>
            <div class="option-item" @click="showHelp = !showHelp">
              <span class="option-arrow">►</span> 4. 帮助说明 (HELP)
            </div>
            <div class="option-item" @click="handleCabinDemo">
              <span class="option-arrow">►</span> 5. 船舱环境演示 (CABIN DEMO)
            </div>
          </div>

          <!-- 游戏特色 -->
          <div class="features-section" v-if="showFeatures">
            <div class="section-border">
                                    游戏特色 - FEATURES<br>
                                                                         <br>
                ▲ 装备系统: 力量、精神、敏捷、体质、感知五大属性<br>
                ▲ 理智机制: 保持理智，避免船员暴动<br>
                ▲ 船只升级: 从破旧小舢板到海上王者<br>
                ▲ 海洋探索: 神秘海域等待探索<br>
            </div>
          </div>

          <!-- 帮助说明 -->
          <div class="help-section" v-if="showHelp">
            <div class="section-border">
                                    帮助说明 - HELP<br>
                                                                         <br>
                ▲ 使用方向键或鼠标选择菜单项<br>
                ▲ 按 ENTER 键确认选择<br>
                ▲ 在游戏中保持理智值和生命值<br>
                ▲ 合理分配资源，规划航线<br>
            </div>
          </div>

          <!-- 状态信息 -->
          <div class="status-bar">
            <div class="status-left">
              STATUS: {{ getGameStatus() }}
            </div>
            <div class="status-right">
              PLAYER: {{ playerName || 'UNKNOWN' }}
            </div>
          </div>
        </div>

        <!-- 底部信息 -->
        <div class="footer-info">
          <div class="version-info">
            VERSION 1.0.0 | 8-BIT SAILING SURVIVAL GAME
          </div>
          <div class="copyright">
            © 2024 RETRO GAMING STUDIOS
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'

const router = useRouter()
const gameStore = useGameStore()

const playerName = ref('')
const showIntro = ref(true)
const showFeatures = ref(false)
const showHelp = ref(false)
const loading = ref(false)

const handleStartGame = async () => {
  if (!playerName.value.trim()) {
    playBeep()
    return
  }
  
  loading.value = true
  playStartSound()
  
  try {
    await gameStore.createPlayer(playerName.value.trim())
    router.push('/game')
  } catch (error) {
    console.error('Failed to start game:', error)
    playErrorSound()
  } finally {
    loading.value = false
  }
}

const handleContinueGame = async () => {
  if (!playerName.value.trim()) {
    playBeep()
    return
  }
  
  loading.value = true
  playStartSound()
  
  try {
    await gameStore.loadPlayer(playerName.value.trim())
    router.push('/game')
  } catch (error) {
    console.error('Failed to continue game:', error)
    playErrorSound()
  } finally {
    loading.value = false
  }
}

const handleCabinDemo = () => {
  playStartSound()
  router.push('/cabin-demo')
}

const getGameStatus = () => {
  if (loading.value) return 'LOADING...'
  if (!playerName.value.trim()) return 'WAITING FOR INPUT'
  return 'READY'
}

// 8-bit音效
const playBeep = () => {
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext
    const audioContext = new AudioContextClass()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()
    
    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)
    
    oscillator.frequency.value = 800
    oscillator.type = 'square'
    gainNode.gain.value = 0.1
    
    oscillator.start()
    oscillator.stop(audioContext.currentTime + 0.1)
  } catch (e) {
    console.log('Audio not supported')
  }
}

const playStartSound = () => {
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext
    const audioContext = new AudioContextClass()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()
    
    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)
    
    oscillator.frequency.value = 440
    oscillator.type = 'square'
    gainNode.gain.value = 0.1
    
    oscillator.start()
    oscillator.stop(audioContext.currentTime + 0.2)
  } catch (e) {
    console.log('Audio not supported')
  }
}

const playErrorSound = () => {
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext
    const audioContext = new AudioContextClass()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()
    
    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)
    
    oscillator.frequency.value = 200
    oscillator.type = 'square'
    gainNode.gain.value = 0.1
    
    oscillator.start()
    oscillator.stop(audioContext.currentTime + 0.3)
  } catch (e) {
    console.log('Audio not supported')
  }
}

onMounted(() => {
  playBeep()
})
</script>

<style lang="scss" scoped>
.retro-game-container {
  width: 100vw;
  height: 100vh;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Courier New', 'Lucida Console', monospace;
  overflow: hidden;
}

.crt-screen {
  position: relative;
  width: 90%;
  max-width: 800px;
  height: 90%;
  background: #001100;
  border: 8px solid #333;
  border-radius: 20px;
  box-shadow: 
    0 0 50px rgba(0, 255, 0, 0.3),
    inset 0 0 50px rgba(0, 255, 0, 0.1);
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.4) 100%),
      linear-gradient(90deg, transparent 50%, rgba(0, 255, 0, 0.03) 50%);
    background-size: 100% 100%, 2px 2px;
    pointer-events: none;
    z-index: 1;
  }
}

.scanlines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(transparent 50%, rgba(0, 255, 0, 0.05) 50%);
  background-size: 100% 4px;
  pointer-events: none;
  z-index: 2;
  animation: scanline 0.1s linear infinite;
}

@keyframes scanline {
  0% { background-position: 0 0; }
  100% { background-position: 0 4px; }
}

.crt-content {
  position: relative;
  padding: 20px;
  height: 100%;
  color: #00ff00;
  font-size: 18px;
  line-height: 1.4;
  z-index: 3;
  text-shadow: 0 0 10px #00ff00;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto;
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: #001100;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #00ff00;
    border-radius: 4px;
  }
}

.game-header {
  text-align: center;
  margin-bottom: 20px;
  
  .title-line {
    color: #00ff00;
    font-size: 16px;
    margin: 5px 0;
  }
  
  .game-title {
    font-size: 28px;
    font-weight: bold;
    color: #00ff00;
    margin: 10px 0;
    text-shadow: 0 0 15px #00ff00;
  }
  
  .subtitle {
    font-size: 16px;
    color: #00aa00;
    margin: 10px 0;
  }
}

.blink {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.game-intro {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  
  .intro-border {
    font-size: 32px !important;
    line-height: 2 !important;
    text-align: center;
    margin: 20px auto;
    max-width: 1000px;
  }
  
  .press-key {
    font-size: 32px !important;
    margin-top: 30px;
    cursor: pointer;
    
    &:hover {
      .blink {
        color: #ffff00;
        text-shadow: 0 0 15px #ffff00;
      }
    }
  }
}

.main-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  
  .menu-header {
    text-align: center;
    font-size: 14px;
    color: #00ff00;
    margin-bottom: 10px;
  }
  
  .input-section {
    margin-bottom: 20px;
    
    .input-label {
      color: #00ff00;
      margin-bottom: 5px;
      font-size: 12px;
    }
    
    .input-field {
      .retro-input {
        background: #000;
        border: 2px solid #00ff00;
        color: #00ff00;
        padding: 8px 12px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        width: 100%;
        max-width: 300px;
        text-shadow: 0 0 5px #00ff00;
        
        &:focus {
          outline: none;
          border-color: #ffff00;
          box-shadow: 0 0 10px #ffff00;
          color: #ffff00;
          text-shadow: 0 0 10px #ffff00;
        }
        
        &::placeholder {
          color: #006600;
        }
      }
    }
  }
  
  .menu-options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    
    .option-item {
      cursor: pointer;
      color: #00ff00;
      font-size: 18px;
      padding: 5px 0;
      transition: all 0.2s ease;
      
      &:hover:not(.disabled) {
        color: #ffff00;
        text-shadow: 0 0 10px #ffff00;
        transform: translateX(10px);
      }
      
      &.disabled {
        color: #004400;
        cursor: not-allowed;
      }
      
      .option-arrow {
        display: inline-block;
        width: 20px;
      }
    }
  }
  
  .features-section,
  .help-section {
    margin-top: 20px;
    
    .section-border {
      font-size: 12px;
      line-height: 1.2;
      white-space: pre-line;
      font-family: 'Courier New', monospace;
      color: #00aa00;
    }
  }
  
  .status-bar {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
    font-size: 16px;
    color: #00aa00;
    border-top: 1px solid #00aa00;
    padding-top: 10px;
  }
}

.footer-info {
  text-align: center;
  font-size: 14px;
  color: #006600;
  margin-top: 20px;
  
  .version-info {
    margin-bottom: 5px;
  }
  
  .copyright {
    margin-top: 5px;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .crt-screen {
    width: 95%;
    height: 95%;
  }
  
  .crt-content {
    padding: 15px;
    font-size: 16px;
  }
  
  .game-title {
    font-size: 24px !important;
  }
  
  .menu-options .option-item {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .crt-content {
    padding: 10px;
    font-size: 14px;
  }
  
  .game-title {
    font-size: 20px !important;
  }
}

.large-text {
  font-size: 32px;
  line-height: 2;
}

.intro-border {
  text-align: center;
  margin: 20px auto;
  max-width: 1000px;
}

.press-key {
  margin-top: 30px;
  cursor: pointer;
  
  &:hover {
    .blink {
      color: #ffff00;
      text-shadow: 0 0 15px #ffff00;
    }
  }
}
</style> 