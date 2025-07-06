<template>
  <div class="cabin-demo">
    <div class="demo-header">
      <h1>🚢 第一视角船舱环境演示</h1>
      <div class="demo-controls">
        <el-button @click="$router.push('/game')" type="primary">
          <el-icon><ArrowLeft /></el-icon>
          返回游戏
        </el-button>
        <el-button @click="toggleWeather" :type="weatherType">
          {{ weatherLabels[currentWeather] }}
        </el-button>
        <el-button @click="toggleTime" :type="timeType">
          {{ timeLabels[currentTime] }}
        </el-button>
        <el-button disabled type="info">
          🎵 音效暂未启用
        </el-button>
      </div>
    </div>

    <!-- 船舱环境 -->
    <div class="demo-cabin">
      <div class="cabin-placeholder">
        <div class="cabin-frame">
          <h2>🚢 船舱环境演示</h2>
          <p>3D船舱环境已简化，避免组件冲突</p>
          <div class="cabin-preview">
            <div class="preview-item">🪟 舷窗视野</div>
            <div class="preview-item">🧭 导航仪表</div>
            <div class="preview-item">📚 船舱物品</div>
            <div class="preview-item">⚓ 环境效果</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 环境信息面板 -->
    <div class="environment-panel">
      <div class="panel-section">
        <h3>🌊 环境状态</h3>
        <div class="status-grid">
          <div class="status-item">
            <span class="label">天气:</span>
            <span class="value">{{ weatherLabels[currentWeather] }}</span>
          </div>
          <div class="status-item">
            <span class="label">时间:</span>
            <span class="value">{{ timeLabels[currentTime] }}</span>
          </div>
          <div class="status-item">
            <span class="label">海况:</span>
            <span class="value">{{ seaConditions[currentWeather] }}</span>
          </div>
        </div>
      </div>

      <div class="panel-section">
        <h3>🎮 交互提示</h3>
        <div class="interaction-tips">
          <div class="tip">
            <el-icon><View /></el-icon>
            <span>点击舷窗观察海面</span>
          </div>
          <div class="tip">
            <el-icon><Compass /></el-icon>
            <span>点击罗盘查看方向</span>
          </div>
          <div class="tip">
            <el-icon><Search /></el-icon>
            <span>点击望远镜远眺</span>
          </div>
          <div class="tip">
            <el-icon><Reading /></el-icon>
            <span>点击书架阅读</span>
          </div>
          <div class="tip">
            <el-icon><Sunny /></el-icon>
            <span>点击油灯控制照明</span>
          </div>
        </div>
      </div>

      <div class="panel-section">
        <h3>🔧 技术特性</h3>
        <div class="features-list">
          <div class="feature">✨ CSS 3D变换构建立体空间</div>
          <div class="feature">🌊 动态海浪和天空效果</div>
          <div class="feature">⚡ 实时船只摇摆动画</div>
          <div class="feature">🎵 Web Audio API环境音效</div>
          <div class="feature">🖱️ 丰富的交互元素</div>
          <div class="feature">📱 响应式设计适配</div>
        </div>
      </div>
    </div>

    <!-- 音效说明面板 -->
    <div class="sound-panel">
      <h4>🎵 音效系统</h4>
      <div class="sound-info">
        <p>音效系统暂时禁用，避免兼容性问题</p>
        <p>未来版本将支持：</p>
        <ul>
          <li>🌊 海浪声</li>
          <li>💨 风声</li>
          <li>🌧️ 雨声</li>
          <li>🐦 海鸥叫声</li>
          <li>⚓ 船只吱嘎声</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, View, Compass, Search, Reading, Sunny } from '@element-plus/icons-vue'
// import ShipCabin from '@/components/ShipCabin.vue' // 暂时注释避免冲突
// import { ambientSounds } from '@/utils/ambientSounds' // 暂时注释避免冲突

const router = useRouter()
const cabinRef = ref(null)

// 环境状态
const currentWeather = ref('calm')
const currentTime = ref('day')
const soundEnabled = ref(true)
const volume = ref(30)

// 标签映射
const weatherLabels = {
  calm: '🌅 平静',
  windy: '💨 多风',
  storm: '⛈️ 暴风雨',
  foggy: '🌫️ 多雾'
}

const timeLabels = {
  dawn: '🌅 黎明',
  day: '☀️ 白天',
  dusk: '🌇 黄昏',
  night: '🌙 夜晚'
}

const seaConditions = {
  calm: '风平浪静',
  windy: '中等海浪',
  storm: '巨浪滔天',
  foggy: '能见度低'
}

// 计算属性
const weatherType = ref('primary')
const timeType = ref('success')

// 切换天气
const toggleWeather = () => {
  const weathers = ['calm', 'windy', 'storm', 'foggy']
  const currentIndex = weathers.indexOf(currentWeather.value)
  currentWeather.value = weathers[(currentIndex + 1) % weathers.length]
  console.log('天气切换到:', currentWeather.value)
}

// 切换时间
const toggleTime = () => {
  const times = ['dawn', 'day', 'dusk', 'night']
  const currentIndex = times.indexOf(currentTime.value)
  currentTime.value = times[(currentIndex + 1) % times.length]
  console.log('时间切换到:', currentTime.value)
}

// 音效相关方法（暂时禁用）
const toggleSound = () => {
  console.log('音效切换（暂时禁用）')
}

const updateVolume = (value) => {
  console.log('音量调节（暂时禁用）:', value)
}

const playSound = (soundType) => {
  console.log('播放音效（暂时禁用）:', soundType)
}

// 生命周期
onMounted(() => {
  console.log('船舱演示页面已加载')
})

onUnmounted(() => {
  console.log('船舱演示页面已卸载')
})
</script>

<style lang="scss" scoped>
.cabin-demo {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(
    to bottom,
    #0a1929 0%,
    #1e3a8a 50%,
    #0f172a 100%
  );
}

.demo-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(0, 20, 40, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 2px solid #66ffcc;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h1 {
    color: #66ffcc;
    margin: 0;
    font-size: 1.5rem;
    text-shadow: 0 0 10px rgba(102, 255, 204, 0.5);
  }
}

.demo-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.demo-cabin {
  width: 100%;
  height: 100%;
  margin-top: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cabin-placeholder {
  background: rgba(0, 20, 40, 0.9);
  border: 2px solid #66ffcc;
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  text-align: center;
  max-width: 600px;
}

.cabin-frame {
  h2 {
    color: #66ffcc;
    margin: 0 0 1rem 0;
    text-shadow: 0 0 10px rgba(102, 255, 204, 0.5);
  }

  p {
    color: #ccc;
    margin: 0 0 1.5rem 0;
    line-height: 1.5;
  }
}

.cabin-preview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 1.5rem;
}

.preview-item {
  background: rgba(102, 255, 204, 0.1);
  border: 1px solid #66ffcc;
  border-radius: 8px;
  padding: 1rem;
  color: #66ffcc;
  font-size: 0.9rem;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(102, 255, 204, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 255, 204, 0.3);
  }
}

.environment-panel {
  position: fixed;
  top: 100px;
  right: 20px;
  width: 300px;
  background: rgba(0, 20, 40, 0.9);
  border: 2px solid #66ffcc;
  border-radius: 12px;
  padding: 1rem;
  backdrop-filter: blur(10px);
  z-index: 999;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
}

.panel-section {
  margin-bottom: 1.5rem;
  
  h3 {
    color: #66ffcc;
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    border-bottom: 1px solid rgba(102, 255, 204, 0.3);
    padding-bottom: 0.25rem;
  }
}

.status-grid {
  display: grid;
  gap: 0.5rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  
  .label {
    color: #ccc;
    font-size: 0.9rem;
  }
  
  .value {
    color: #FFD700;
    font-weight: bold;
    font-size: 0.9rem;
  }
}

.interaction-tips {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ccc;
  font-size: 0.85rem;
  
  .el-icon {
    color: #66ffcc;
  }
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.feature {
  color: #ccc;
  font-size: 0.85rem;
  padding: 0.25rem 0;
}

.sound-panel {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background: rgba(0, 20, 40, 0.9);
  border: 2px solid #66ffcc;
  border-radius: 12px;
  padding: 1rem;
  backdrop-filter: blur(10px);
  z-index: 999;
  
  h4 {
    color: #66ffcc;
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
  }
}

.sound-info {
  color: #ccc;
  font-size: 0.85rem;
  line-height: 1.4;

  p {
    margin: 0.5rem 0;
  }

  ul {
    margin: 0.5rem 0;
    padding-left: 1rem;

    li {
      margin: 0.25rem 0;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .demo-header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    
    h1 {
      font-size: 1.2rem;
    }
  }
  
  .demo-controls {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .environment-panel {
    position: relative;
    top: auto;
    right: auto;
    width: calc(100% - 40px);
    margin: 20px;
    max-height: none;
  }
  
  .sound-panel {
    position: relative;
    bottom: auto;
    left: auto;
    margin: 20px;
  }
  
  .demo-cabin {
    margin-top: 140px;
    height: calc(100vh - 140px);
  }
}

// 自定义滚动条
.environment-panel::-webkit-scrollbar {
  width: 6px;
}

.environment-panel::-webkit-scrollbar-track {
  background: rgba(0, 40, 80, 0.3);
  border-radius: 3px;
}

.environment-panel::-webkit-scrollbar-thumb {
  background: #66ffcc;
  border-radius: 3px;
  
  &:hover {
    background: #FFD700;
  }
}
</style>
