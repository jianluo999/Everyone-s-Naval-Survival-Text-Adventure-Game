<template>
  <div class="astrology-system">
    <div class="astrology-header">
      <h3>🔮 神秘占星</h3>
      <div class="astrology-description">
        通过观察星象预测未来，获得神秘力量
      </div>
    </div>

    <div class="astrology-content">
      <!-- 星盘区域 -->
      <div class="star-chart">
        <div class="chart-container">
          <svg class="star-map" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
            <!-- 星盘背景 -->
            <defs>
              <radialGradient id="starGradient" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#001122;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#000011;stop-opacity:1" />
              </radialGradient>
            </defs>
            
            <circle cx="150" cy="150" r="140" fill="url(#starGradient)" stroke="#66ffcc" stroke-width="2"/>
            
            <!-- 星座线条 -->
            <g class="constellation-lines">
              <path 
                v-for="constellation in constellations" 
                :key="constellation.id"
                :d="constellation.path"
                stroke="#66ffcc"
                stroke-width="1"
                fill="none"
                opacity="0.6"
              />
            </g>
            
            <!-- 星星 -->
            <g class="stars">
              <circle 
                v-for="star in stars" 
                :key="star.id"
                :cx="star.x" 
                :cy="star.y" 
                :r="star.size"
                :fill="star.color"
                :class="{ 'active-star': star.active }"
                @click="selectStar(star)"
              />
            </g>
            
            <!-- 月相 -->
            <g class="moon-phase" transform="translate(150, 150)">
              <circle cx="0" cy="0" r="20" fill="#f0f0f0" opacity="0.8"/>
              <path 
                :d="getMoonPhasePath()"
                fill="#001122"
                opacity="0.6"
              />
            </g>
          </svg>
        </div>
        
        <div class="chart-info">
          <div class="current-phase">
            <h4>当前月相</h4>
            <div class="phase-display">
              <span class="phase-icon">{{ currentMoonPhase.icon }}</span>
              <span class="phase-name">{{ currentMoonPhase.name }}</span>
            </div>
            <p class="phase-effect">{{ currentMoonPhase.effect }}</p>
          </div>
        </div>
      </div>

      <!-- 占卜功能 -->
      <div class="divination-panel">
        <div class="divination-header">
          <h4>🎴 星象占卜</h4>
          <div class="divination-cost">
            消耗: 10 理智值
          </div>
        </div>
        
        <div class="divination-content">
          <div class="divination-types">
            <button 
              v-for="type in divinationTypes" 
              :key="type.id"
              class="divination-btn"
              :class="{ active: selectedDivination === type.id }"
              @click="selectedDivination = type.id"
              :disabled="!canPerformDivination"
            >
              <span class="btn-icon">{{ type.icon }}</span>
              <span class="btn-text">{{ type.name }}</span>
            </button>
          </div>
          
          <div class="divination-action">
            <button 
              class="perform-divination-btn"
              @click="performDivination"
              :disabled="!canPerformDivination || !selectedDivination"
            >
              <span v-if="isPerformingDivination">🔮 占卜中...</span>
              <span v-else>✨ 开始占卜</span>
            </button>
          </div>
          
          <div v-if="lastDivination" class="divination-result">
            <h5>占卜结果</h5>
            <div class="result-content">
              <div class="result-icon">{{ lastDivination.icon }}</div>
              <div class="result-text">
                <h6>{{ lastDivination.title }}</h6>
                <p>{{ lastDivination.description }}</p>
                <div class="result-effects">
                  <span 
                    v-for="effect in lastDivination.effects" 
                    :key="effect.type"
                    class="effect-tag"
                    :class="effect.type"
                  >
                    {{ effect.text }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 星象预测 -->
      <div class="predictions-panel">
        <div class="predictions-header">
          <h4>📜 星象预测</h4>
          <div class="predictions-refresh">
            <button @click="refreshPredictions" class="refresh-btn">
              <span>🔄</span>
            </button>
          </div>
        </div>
        
        <div class="predictions-list">
          <div 
            v-for="prediction in predictions" 
            :key="prediction.id"
            class="prediction-item"
            :class="prediction.type"
          >
            <div class="prediction-icon">{{ prediction.icon }}</div>
            <div class="prediction-content">
              <h6>{{ prediction.title }}</h6>
              <p>{{ prediction.description }}</p>
              <div class="prediction-time">
                有效期: {{ prediction.duration }}
              </div>
            </div>
          </div>
          
          <div v-if="predictions.length === 0" class="no-predictions">
            <p>暂无星象预测</p>
            <p class="hint">进行占卜可能会获得新的预测</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'

const gameStore = useGameStore()

// 响应式数据
const selectedDivination = ref(null)
const isPerformingDivination = ref(false)
const lastDivination = ref(null)

// 星盘数据
const stars = ref([
  { id: 1, x: 80, y: 60, size: 2, color: '#66ffcc', active: false },
  { id: 2, x: 120, y: 80, size: 3, color: '#ffcc66', active: true },
  { id: 3, x: 180, y: 70, size: 2, color: '#cc66ff', active: false },
  { id: 4, x: 220, y: 100, size: 4, color: '#66ccff', active: false },
  { id: 5, x: 200, y: 150, size: 2, color: '#ffcc66', active: false },
  { id: 6, x: 160, y: 200, size: 3, color: '#66ffcc', active: false },
  { id: 7, x: 100, y: 180, size: 2, color: '#cc66ff', active: false },
  { id: 8, x: 70, y: 120, size: 3, color: '#66ccff', active: false }
])

const constellations = ref([
  {
    id: 1,
    path: 'M80,60 L120,80 L180,70 L220,100'
  },
  {
    id: 2,
    path: 'M220,100 L200,150 L160,200 L100,180 L70,120 L80,60'
  }
])

const currentMoonPhase = ref({
  icon: '🌕',
  name: '满月',
  effect: '占卜成功率提升，理智消耗减少'
})

// 占卜类型
const divinationTypes = ref([
  {
    id: 'fortune',
    name: '运势占卜',
    icon: '🍀',
    description: '预测未来的运气变化'
  },
  {
    id: 'weather',
    name: '天象占卜',
    icon: '🌤️',
    description: '预测天气和海况变化'
  },
  {
    id: 'encounter',
    name: '遭遇占卜',
    icon: '👁️',
    description: '预测可能遇到的事件'
  },
  {
    id: 'treasure',
    name: '宝藏占卜',
    icon: '💎',
    description: '寻找隐藏的宝藏线索'
  }
])

// 预测列表
const predictions = ref([
  {
    id: 1,
    type: 'positive',
    icon: '🍀',
    title: '幸运之星',
    description: '接下来的航行将会遇到好运，获得额外奖励的几率提升',
    duration: '2小时'
  },
  {
    id: 2,
    type: 'warning',
    icon: '⚠️',
    title: '风暴预警',
    description: '东南方向可能出现风暴，建议避开该区域',
    duration: '6小时'
  }
])

// 计算属性
const canPerformDivination = computed(() => {
  // 检查玩家是否有足够的理智值
  return gameStore.player?.sanity >= 10
})

// 方法
const selectStar = (star) => {
  // 重置所有星星状态
  stars.value.forEach(s => s.active = false)
  // 激活选中的星星
  star.active = true
  
  ElMessage.info(`选中了 ${star.id} 号星`)
}

const getMoonPhasePath = () => {
  // 根据当前月相返回SVG路径
  return 'M-20,0 A20,20 0 0,1 20,0 A10,10 0 0,0 -20,0'
}

const performDivination = async () => {
  if (!canPerformDivination.value || !selectedDivination.value) return
  
  isPerformingDivination.value = true
  
  try {
    // 模拟占卜过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 消耗理智值
    // gameStore.consumeSanity(10)
    
    // 生成占卜结果
    const divination = generateDivinationResult(selectedDivination.value)
    lastDivination.value = divination
    
    // 可能生成新的预测
    if (Math.random() > 0.5) {
      const newPrediction = generatePrediction()
      predictions.value.unshift(newPrediction)
    }
    
    ElMessage.success('占卜完成！')
    
  } catch (error) {
    ElMessage.error('占卜失败，请稍后再试')
  } finally {
    isPerformingDivination.value = false
  }
}

const generateDivinationResult = (type) => {
  const results = {
    fortune: [
      {
        icon: '🍀',
        title: '大吉',
        description: '星象显示你将迎来一段幸运的时光，所有行动都会得到额外的祝福。',
        effects: [
          { type: 'positive', text: '幸运值 +20' },
          { type: 'positive', text: '经验获得 +50%' }
        ]
      },
      {
        icon: '⚡',
        title: '凶兆',
        description: '星象预示着危险正在逼近，需要格外小心谨慎。',
        effects: [
          { type: 'negative', text: '遭遇危险几率 +30%' },
          { type: 'warning', text: '建议暂缓冒险行动' }
        ]
      }
    ],
    weather: [
      {
        icon: '🌊',
        title: '风平浪静',
        description: '未来几天海况良好，适合长途航行。',
        effects: [
          { type: 'positive', text: '航行速度 +25%' },
          { type: 'positive', text: '船只损耗 -50%' }
        ]
      }
    ],
    encounter: [
      {
        icon: '🏴‍☠️',
        title: '海盗出没',
        description: '星象显示附近海域有海盗活动，小心应对。',
        effects: [
          { type: 'warning', text: '遭遇海盗几率 +40%' },
          { type: 'info', text: '战斗准备建议' }
        ]
      }
    ],
    treasure: [
      {
        icon: '💎',
        title: '宝藏线索',
        description: '星象指引你发现了一个神秘的宝藏位置。',
        effects: [
          { type: 'positive', text: '获得宝藏地图' },
          { type: 'info', text: '坐标已记录' }
        ]
      }
    ]
  }
  
  const typeResults = results[type] || results.fortune
  return typeResults[Math.floor(Math.random() * typeResults.length)]
}

const generatePrediction = () => {
  const predictionTemplates = [
    {
      type: 'positive',
      icon: '✨',
      title: '神秘恩赐',
      description: '星象显示你将获得意外的帮助',
      duration: '4小时'
    },
    {
      type: 'warning',
      icon: '🌪️',
      title: '海域异常',
      description: '某个区域出现了不寻常的现象',
      duration: '8小时'
    },
    {
      type: 'info',
      icon: '🗺️',
      title: '新发现',
      description: '有新的地点等待你去探索',
      duration: '12小时'
    }
  ]
  
  const template = predictionTemplates[Math.floor(Math.random() * predictionTemplates.length)]
  return {
    ...template,
    id: Date.now()
  }
}

const refreshPredictions = () => {
  // 清除过期预测，生成新预测
  predictions.value = predictions.value.filter(() => Math.random() > 0.3)
  
  if (Math.random() > 0.4) {
    predictions.value.push(generatePrediction())
  }
  
  ElMessage.info('星象预测已更新')
}

onMounted(() => {
  // 初始化星象系统
  console.log('占星系统已初始化')
})
</script>

<style scoped>
.astrology-system {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(0, 10, 30, 0.95);
  color: #e0e6ed;
  border-radius: 8px;
  overflow: hidden;
}

.astrology-header {
  padding: 16px;
  background: rgba(0, 20, 50, 0.8);
  border-bottom: 1px solid rgba(102, 255, 204, 0.3);
  text-align: center;
}

.astrology-header h3 {
  margin: 0 0 8px 0;
  color: #66ffcc;
}

.astrology-description {
  font-size: 14px;
  color: #888;
}

.astrology-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 16px;
  padding: 16px;
  overflow: auto;
}

.star-chart {
  background: rgba(0, 15, 35, 0.6);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(102, 255, 204, 0.2);
}

.chart-container {
  margin-bottom: 16px;
}

.star-map {
  width: 100%;
  height: 200px;
}

.stars circle {
  cursor: pointer;
  transition: all 0.3s ease;
}

.stars circle:hover,
.stars circle.active-star {
  filter: brightness(1.5);
  transform: scale(1.2);
}

.current-phase {
  text-align: center;
}

.phase-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 8px 0;
}

.phase-icon {
  font-size: 24px;
}

.phase-effect {
  font-size: 12px;
  color: #888;
  margin: 0;
}

.divination-panel {
  background: rgba(0, 15, 35, 0.6);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(102, 255, 204, 0.2);
}

.divination-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.divination-cost {
  font-size: 12px;
  color: #888;
}

.divination-types {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 16px;
}

.divination-btn {
  background: rgba(0, 30, 60, 0.6);
  border: 1px solid rgba(102, 255, 204, 0.3);
  border-radius: 6px;
  padding: 8px;
  color: #e0e6ed;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.divination-btn:hover {
  background: rgba(0, 40, 80, 0.8);
  border-color: rgba(102, 255, 204, 0.5);
}

.divination-btn.active {
  background: rgba(102, 255, 204, 0.2);
  border-color: #66ffcc;
}

.divination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 18px;
}

.btn-text {
  font-size: 12px;
}

.perform-divination-btn {
  width: 100%;
  background: linear-gradient(45deg, #66ffcc, #4a90e2);
  border: none;
  border-radius: 6px;
  padding: 12px;
  color: #001122;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.perform-divination-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 255, 204, 0.3);
}

.perform-divination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.divination-result {
  margin-top: 16px;
  padding: 12px;
  background: rgba(0, 20, 40, 0.8);
  border-radius: 6px;
  border: 1px solid rgba(102, 255, 204, 0.3);
}

.result-content {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.result-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.result-text h6 {
  margin: 0 0 8px 0;
  color: #66ffcc;
}

.result-text p {
  margin: 0 0 8px 0;
  font-size: 14px;
}

.result-effects {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.effect-tag {
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 11px;
}

.effect-tag.positive {
  background: rgba(103, 194, 58, 0.3);
  color: #67c23a;
}

.effect-tag.negative {
  background: rgba(245, 108, 108, 0.3);
  color: #f56c6c;
}

.effect-tag.warning {
  background: rgba(230, 162, 60, 0.3);
  color: #e6a23c;
}

.effect-tag.info {
  background: rgba(64, 158, 255, 0.3);
  color: #409eff;
}

.predictions-panel {
  grid-column: 1 / -1;
  background: rgba(0, 15, 35, 0.6);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(102, 255, 204, 0.2);
}

.predictions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.refresh-btn {
  background: none;
  border: 1px solid rgba(102, 255, 204, 0.3);
  border-radius: 4px;
  padding: 4px 8px;
  color: #66ffcc;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: rgba(102, 255, 204, 0.1);
}

.predictions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.prediction-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: rgba(0, 20, 40, 0.6);
  border-radius: 6px;
  border-left: 4px solid;
}

.prediction-item.positive {
  border-left-color: #67c23a;
}

.prediction-item.warning {
  border-left-color: #e6a23c;
}

.prediction-item.info {
  border-left-color: #409eff;
}

.prediction-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.prediction-content h6 {
  margin: 0 0 4px 0;
  color: #66ffcc;
}

.prediction-content p {
  margin: 0 0 8px 0;
  font-size: 14px;
}

.prediction-time {
  font-size: 12px;
  color: #888;
}

.no-predictions {
  text-align: center;
  padding: 20px;
  color: #888;
}

.hint {
  font-size: 12px;
  margin-top: 8px;
  opacity: 0.7;
}
</style>
