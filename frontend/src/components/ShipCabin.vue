<template>
  <div class="ship-cabin" :class="{ 'storm-mode': isStorm }">
    <!-- 船舱背景 -->
    <div class="cabin-background">
      <!-- 木质船舱结构 -->
      <div class="cabin-structure">
        <!-- 左侧墙壁 -->
        <div class="wall wall-left">
          <div class="wood-planks">
            <div v-for="i in 8" :key="`left-plank-${i}`" class="plank"></div>
          </div>
          <!-- 舷窗 -->
          <div class="porthole porthole-left" @click="lookOutside('left')">
            <div class="porthole-frame"></div>
            <div class="porthole-glass">
              <div class="ocean-view">
                <div class="waves"></div>
                <div class="horizon"></div>
                <div class="sky" :class="timeOfDay"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧墙壁 -->
        <div class="wall wall-right">
          <div class="wood-planks">
            <div v-for="i in 8" :key="`right-plank-${i}`" class="plank"></div>
          </div>
          <!-- 舷窗 -->
          <div class="porthole porthole-right" @click="lookOutside('right')">
            <div class="porthole-frame"></div>
            <div class="porthole-glass">
              <div class="ocean-view">
                <div class="waves"></div>
                <div class="horizon"></div>
                <div class="sky" :class="timeOfDay"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 前方控制台 -->
        <div class="control-panel">
          <div class="panel-background"></div>
          
          <!-- 仪表盘 -->
          <div class="instruments">
            <div class="compass" @click="openMap">
              <div class="compass-face">
                <div class="compass-needle" :style="{ transform: `rotate(${heading}deg)` }"></div>
                <div class="compass-directions">
                  <span class="direction north">N</span>
                  <span class="direction east">E</span>
                  <span class="direction south">S</span>
                  <span class="direction west">W</span>
                </div>
              </div>
              <div class="instrument-label">罗盘</div>
            </div>

            <div class="depth-gauge">
              <div class="gauge-face">
                <div class="gauge-needle" :style="{ transform: `rotate(${depthAngle}deg)` }"></div>
                <div class="gauge-scale">
                  <div v-for="i in 10" :key="`depth-${i}`" class="scale-mark"></div>
                </div>
              </div>
              <div class="instrument-label">深度</div>
            </div>

            <div class="speed-gauge">
              <div class="gauge-face">
                <div class="gauge-needle" :style="{ transform: `rotate(${speedAngle}deg)` }"></div>
                <div class="gauge-scale">
                  <div v-for="i in 8" :key="`speed-${i}`" class="scale-mark"></div>
                </div>
              </div>
              <div class="instrument-label">航速</div>
            </div>
          </div>

          <!-- 控制按钮 -->
          <div class="control-buttons">
            <button class="cabin-button" @click="openLog">
              <el-icon><Document /></el-icon>
              <span>航海日志</span>
            </button>
            <button class="cabin-button" @click="openMap">
              <el-icon><Location /></el-icon>
              <span>海图</span>
            </button>
            <button class="cabin-button" @click="openInventory">
              <el-icon><Box /></el-icon>
              <span>储物箱</span>
            </button>
          </div>
        </div>

        <!-- 船舱物品 -->
        <div class="cabin-items">
          <!-- 桌子 -->
          <div class="table" @click="interactWithTable">
            <div class="table-surface">
              <div class="map-scroll" v-if="showMapOnTable"></div>
              <div class="quill-pen"></div>
              <div class="ink-bottle"></div>
            </div>
            <div class="table-legs"></div>
          </div>

          <!-- 书架 -->
          <div class="bookshelf" @click="openLibrary">
            <div class="shelf-frame"></div>
            <div class="books">
              <div v-for="i in 12" :key="`book-${i}`" class="book" :class="`book-${i % 4 + 1}`"></div>
            </div>
          </div>

          <!-- 望远镜 -->
          <div class="telescope" @click="useTelescope">
            <div class="telescope-body"></div>
            <div class="telescope-lens"></div>
            <div class="telescope-stand"></div>
          </div>

          <!-- 油灯 -->
          <div class="lantern" :class="{ 'lit': isLanternLit }" @click="toggleLantern">
            <div class="lantern-body"></div>
            <div class="lantern-flame" v-if="isLanternLit"></div>
            <div class="lantern-glow" v-if="isLanternLit"></div>
          </div>
        </div>

        <!-- 地板 -->
        <div class="cabin-floor">
          <div class="floor-planks">
            <div v-for="i in 15" :key="`floor-${i}`" class="floor-plank"></div>
          </div>
          <div class="floor-carpet"></div>
        </div>
      </div>

      <!-- 环境光效 -->
      <div class="ambient-lighting" :class="timeOfDay">
        <div class="light-rays" v-if="timeOfDay === 'day'"></div>
        <div class="moonlight" v-if="timeOfDay === 'night'"></div>
      </div>

      <!-- 船只摇摆效果 -->
      <div class="ship-motion" :class="{ 'rough-seas': isStorm }"></div>

      <!-- 雨滴效果（暴风雨时） -->
      <div class="rain-effect" v-if="isStorm">
        <div v-for="i in 50" :key="`rain-${i}`" class="raindrop"></div>
      </div>
    </div>

    <!-- 交互提示 -->
    <div class="interaction-hint" v-if="hoverHint" :style="hintPosition">
      {{ hoverHint }}
    </div>

    <!-- 望远镜视图模态框 -->
    <el-dialog
      v-model="telescopeView"
      title="望远镜视野"
      width="80%"
      class="telescope-dialog"
    >
      <div class="telescope-viewport">
        <div class="telescope-circle">
          <div class="distant-view">
            <div class="horizon-line"></div>
            <div class="distant-islands" v-if="Math.random() > 0.7">
              <div class="island"></div>
            </div>
            <div class="seabirds">
              <div v-for="i in 3" :key="`bird-${i}`" class="bird"></div>
            </div>
            <div class="weather-effects" :class="weatherCondition"></div>
          </div>
        </div>
        <div class="telescope-info">
          <p>通过望远镜，你可以观察远方的海域...</p>
          <p v-if="Math.random() > 0.8" class="discovery">你发现了什么！</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { Document, Location, Box } from '@element-plus/icons-vue'

const gameStore = useGameStore()

// 响应式数据
const heading = ref(0) // 罗盘方向
const depth = ref(50) // 深度
const speed = ref(3) // 航速
const isStorm = ref(false)
const isLanternLit = ref(true)
const showMapOnTable = ref(false)
const telescopeView = ref(false)
const hoverHint = ref('')
const hintPosition = ref({ left: '0px', top: '0px' })

// 计算属性
const timeOfDay = computed(() => {
  const hour = gameStore.timeInfo?.currentHour || 12
  if (hour >= 6 && hour < 18) return 'day'
  if (hour >= 18 && hour < 20) return 'sunset'
  return 'night'
})

const depthAngle = computed(() => (depth.value / 100) * 180 - 90)
const speedAngle = computed(() => (speed.value / 10) * 180 - 90)
const weatherCondition = computed(() => isStorm.value ? 'storm' : 'clear')

// 船只摇摆动画
let motionInterval = null

const startShipMotion = () => {
  motionInterval = setInterval(() => {
    // 随机改变航向
    heading.value += (Math.random() - 0.5) * 2
    
    // 模拟深度变化
    depth.value += (Math.random() - 0.5) * 5
    depth.value = Math.max(0, Math.min(100, depth.value))
    
    // 模拟速度变化
    speed.value += (Math.random() - 0.5) * 0.5
    speed.value = Math.max(0, Math.min(10, speed.value))
    
    // 随机天气变化
    if (Math.random() > 0.98) {
      isStorm.value = !isStorm.value
    }
  }, 2000)
}

// 交互方法
const lookOutside = (side) => {
  hoverHint.value = `从${side === 'left' ? '左' : '右'}舷窗望向大海...`
  setTimeout(() => hoverHint.value = '', 2000)
}

const openMap = () => {
  showMapOnTable.value = !showMapOnTable.value
  // 触发地图面板
  document.dispatchEvent(new CustomEvent('openGamePanel', { detail: 'map' }))
}

const openLog = () => {
  document.dispatchEvent(new CustomEvent('openGamePanel', { detail: 'log' }))
}

const openInventory = () => {
  document.dispatchEvent(new CustomEvent('openGamePanel', { detail: 'inventory' }))
}

const openLibrary = () => {
  hoverHint.value = '这些古老的海洋传说书籍记录着深海的秘密...'
  setTimeout(() => hoverHint.value = '', 3000)
}

const useTelescope = () => {
  telescopeView.value = true
}

const toggleLantern = () => {
  isLanternLit.value = !isLanternLit.value
}

const interactWithTable = () => {
  showMapOnTable.value = !showMapOnTable.value
  hoverHint.value = showMapOnTable.value ? '展开了海图' : '收起了海图'
  setTimeout(() => hoverHint.value = '', 2000)
}

// 生命周期
onMounted(() => {
  startShipMotion()
})

onUnmounted(() => {
  if (motionInterval) {
    clearInterval(motionInterval)
  }
})

// 暴露给父组件的方法
defineExpose({
  setWeather: (weather) => {
    isStorm.value = weather === 'storm'
  },
  setTimeOfDay: (time) => {
    // 时间由gameStore控制
  }
})
</script>

<style lang="scss" scoped>
.ship-cabin {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  perspective: 1000px;
  background: linear-gradient(
    to bottom,
    #1a2332 0%,
    #2d3748 50%,
    #1a202c 100%
  );
}

.cabin-background {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  animation: gentle-sway 8s ease-in-out infinite;
}

.storm-mode .cabin-background {
  animation: rough-sway 3s ease-in-out infinite;
}

.cabin-structure {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

// 墙壁
.wall {
  position: absolute;
  height: 70%;
  width: 200px;
  top: 15%;
  
  &.wall-left {
    left: 0;
    transform: rotateY(15deg) translateZ(-50px);
  }
  
  &.wall-right {
    right: 0;
    transform: rotateY(-15deg) translateZ(-50px);
  }
}

.wood-planks {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    #8B4513 0%,
    #A0522D 50%,
    #654321 100%
  );
  position: relative;
  
  .plank {
    height: 12.5%;
    border-bottom: 2px solid #654321;
    background: linear-gradient(
      to right,
      #8B4513 0%,
      #A0522D 20%,
      #8B4513 40%,
      #A0522D 60%,
      #8B4513 80%,
      #A0522D 100%
    );
    
    &:nth-child(odd) {
      filter: brightness(0.9);
    }
  }
}

// 舷窗
.porthole {
  position: absolute;
  width: 120px;
  height: 120px;
  top: 30%;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateX(-50%) scale(1.05);
  }
}

.porthole-frame {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 8px solid #4A5568;
  background: radial-gradient(circle, #2D3748 0%, #1A202C 100%);
  box-shadow: 
    inset 0 0 20px rgba(0,0,0,0.5),
    0 0 30px rgba(102, 255, 204, 0.3);
}

.porthole-glass {
  position: absolute;
  width: 80%;
  height: 80%;
  top: 10%;
  left: 10%;
  border-radius: 50%;
  overflow: hidden;
  background: rgba(102, 255, 204, 0.1);
}

.ocean-view {
  width: 100%;
  height: 100%;
  position: relative;
  
  .waves {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 60%;
    background: linear-gradient(
      to top,
      #1a365d 0%,
      #2c5282 50%,
      #3182ce 100%
    );
    animation: wave-motion 4s ease-in-out infinite;
  }
  
  .horizon {
    position: absolute;
    top: 40%;
    width: 100%;
    height: 2px;
    background: rgba(102, 255, 204, 0.5);
  }
  
  .sky {
    position: absolute;
    top: 0;
    width: 100%;
    height: 40%;
    
    &.day {
      background: linear-gradient(to bottom, #87CEEB 0%, #B0E0E6 100%);
    }
    
    &.sunset {
      background: linear-gradient(to bottom, #FF6B35 0%, #F7931E 50%, #FFD700 100%);
    }
    
    &.night {
      background: linear-gradient(to bottom, #0F0F23 0%, #1a1a2e 100%);
    }
  }
}

// 控制台
.control-panel {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 200px;
  background: linear-gradient(
    to top,
    #2D3748 0%,
    #4A5568 50%,
    #2D3748 100%
  );
  border-radius: 20px 20px 0 0;
  border: 3px solid #4A5568;
  box-shadow: 0 -10px 30px rgba(0,0,0,0.5);
}

.instruments {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 60%;
  padding: 20px;
}

.compass, .depth-gauge, .speed-gauge {
  position: relative;
  width: 80px;
  height: 80px;
  cursor: pointer;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.1);
  }
}

.compass-face, .gauge-face {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, #1A202C 0%, #2D3748 100%);
  border: 3px solid #66ffcc;
  position: relative;
  box-shadow: 
    inset 0 0 10px rgba(0,0,0,0.5),
    0 0 15px rgba(102, 255, 204, 0.3);
}

.compass-needle, .gauge-needle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 2px;
  height: 35px;
  background: #FFD700;
  transform-origin: bottom center;
  transform: translate(-50%, -100%);
  transition: transform 0.5s ease;
  box-shadow: 0 0 5px rgba(255, 215, 0, 0.8);
}

.compass-directions {
  position: absolute;
  width: 100%;
  height: 100%;
  
  .direction {
    position: absolute;
    color: #66ffcc;
    font-weight: bold;
    font-size: 12px;
    
    &.north { top: 5px; left: 50%; transform: translateX(-50%); }
    &.east { right: 5px; top: 50%; transform: translateY(-50%); }
    &.south { bottom: 5px; left: 50%; transform: translateX(-50%); }
    &.west { left: 5px; top: 50%; transform: translateY(-50%); }
  }
}

.instrument-label {
  text-align: center;
  color: #66ffcc;
  font-size: 10px;
  margin-top: 5px;
}

.control-buttons {
  display: flex;
  justify-content: space-around;
  padding: 10px 20px;
}

.cabin-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 10px 15px;
  background: rgba(102, 255, 204, 0.1);
  border: 2px solid #66ffcc;
  border-radius: 8px;
  color: #66ffcc;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(102, 255, 204, 0.2);
    box-shadow: 0 0 15px rgba(102, 255, 204, 0.5);
    transform: translateY(-2px);
  }
  
  span {
    font-size: 10px;
  }
}

// 船舱物品
.cabin-items {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  
  > * {
    pointer-events: auto;
  }
}

.table {
  position: absolute;
  bottom: 200px;
  left: 20%;
  width: 150px;
  height: 100px;
  cursor: pointer;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.05);
  }
}

.table-surface {
  width: 100%;
  height: 20px;
  background: #8B4513;
  border-radius: 10px;
  position: relative;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.bookshelf {
  position: absolute;
  top: 20%;
  right: 10%;
  width: 100px;
  height: 150px;
  cursor: pointer;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.05);
  }
}

.telescope {
  position: absolute;
  top: 30%;
  left: 10%;
  width: 80px;
  height: 60px;
  cursor: pointer;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.1);
  }
}

.lantern {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 60px;
  cursor: pointer;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateX(-50%) scale(1.1);
  }
  
  &.lit .lantern-glow {
    animation: lantern-flicker 2s ease-in-out infinite;
  }
}

// 地板
.cabin-floor {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 30%;
  transform: rotateX(60deg) translateZ(-100px);
  transform-origin: bottom center;
}

.floor-planks {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to right,
    #654321 0%,
    #8B4513 50%,
    #654321 100%
  );
}

.floor-plank {
  height: 100%;
  width: 6.67%;
  float: left;
  border-right: 1px solid #4A4A4A;
  
  &:nth-child(odd) {
    filter: brightness(0.9);
  }
}

// 环境光效
.ambient-lighting {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  
  &.day {
    background: radial-gradient(
      ellipse at center top,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 70%
    );
  }
  
  &.night {
    background: radial-gradient(
      ellipse at center top,
      rgba(102, 255, 204, 0.05) 0%,
      transparent 70%
    );
  }
}

// 动画
@keyframes gentle-sway {
  0%, 100% { transform: rotateZ(0deg) rotateX(0deg); }
  25% { transform: rotateZ(0.5deg) rotateX(0.2deg); }
  50% { transform: rotateZ(0deg) rotateX(0deg); }
  75% { transform: rotateZ(-0.5deg) rotateX(-0.2deg); }
}

@keyframes rough-sway {
  0%, 100% { transform: rotateZ(0deg) rotateX(0deg); }
  25% { transform: rotateZ(2deg) rotateX(1deg); }
  50% { transform: rotateZ(0deg) rotateX(0deg); }
  75% { transform: rotateZ(-2deg) rotateX(-1deg); }
}

@keyframes wave-motion {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

@keyframes lantern-flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

// 交互提示
.interaction-hint {
  position: fixed;
  background: rgba(0, 20, 40, 0.9);
  color: #66ffcc;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #66ffcc;
  font-size: 12px;
  z-index: 1000;
  pointer-events: none;
}

// 望远镜对话框
.telescope-dialog {
  :deep(.el-dialog) {
    background: rgba(0, 0, 0, 0.9);
    border: 3px solid #66ffcc;
  }
}

.telescope-viewport {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.telescope-circle {
  width: 400px;
  height: 400px;
  border-radius: 50%;
  border: 20px solid #2D3748;
  overflow: hidden;
  background: #000;
  position: relative;
}

.distant-view {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    #87CEEB 0%,
    #4682B4 50%,
    #1e3a8a 100%
  );
  position: relative;
}

.telescope-info {
  color: #66ffcc;
  text-align: center;
  
  .discovery {
    color: #FFD700;
    font-weight: bold;
    animation: glow 2s ease-in-out infinite;
  }
}

@keyframes glow {
  0%, 100% { text-shadow: 0 0 5px rgba(255, 215, 0, 0.5); }
  50% { text-shadow: 0 0 20px rgba(255, 215, 0, 0.8); }
}
</style>
