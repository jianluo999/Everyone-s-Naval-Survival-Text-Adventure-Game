<template>
  <div class="attribute-radar">
    <div class="radar-container">
      <svg class="radar-chart" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <!-- 背景网格 -->
        <defs>
          <radialGradient id="radarGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#001122;stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:#003366;stop-opacity:0.3" />
          </radialGradient>
          
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge> 
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        
        <!-- 背景圆 -->
        <circle cx="200" cy="200" r="180" fill="url(#radarGradient)" stroke="#66ffcc" stroke-width="1" opacity="0.3"/>

        <!-- 网格线 -->
        <g class="grid-lines">
          <!-- 同心圆 -->
          <circle v-for="i in 5" :key="`circle-${i}`"
                  cx="200" cy="200"
                  :r="i * 36"
                  fill="none"
                  stroke="#66ffcc"
                  stroke-width="1"
                  opacity="0.3"/>

          <!-- 五条射线 -->
          <g v-for="(attr, index) in attributes" :key="`line-${index}`">
            <line
              x1="200" y1="200"
              :x2="200 + 180 * Math.cos(getAngle(index))"
              :y2="200 + 180 * Math.sin(getAngle(index))"
              stroke="#66ffcc"
              stroke-width="1"
              opacity="0.4"
            />
          </g>
        </g>
        
        <!-- 数据区域 -->
        <polygon 
          :points="getPolygonPoints()"
          fill="rgba(102, 255, 204, 0.2)"
          stroke="#66ffcc"
          stroke-width="2"
          filter="url(#glow)"
          class="data-polygon"
        />
        
        <!-- 数据点 -->
        <g class="data-points">
          <circle
            v-for="(attr, index) in attributes"
            :key="`point-${index}`"
            :cx="200 + (attr.value / 100) * 180 * Math.cos(getAngle(index))"
            :cy="200 + (attr.value / 100) * 180 * Math.sin(getAngle(index))"
            r="10"
            :fill="getAttributeColor(attr.key)"
            stroke="#fff"
            stroke-width="2"
            class="data-point"
            @mouseover="showTooltip(attr, $event)"
            @mouseout="hideTooltip"
            @click="showDetailModal(attr)"
          />
          <!-- 数据点发光效果 -->
          <circle
            v-for="(attr, index) in attributes"
            :key="`glow-${index}`"
            :cx="200 + (attr.value / 100) * 180 * Math.cos(getAngle(index))"
            :cy="200 + (attr.value / 100) * 180 * Math.sin(getAngle(index))"
            r="15"
            :fill="getAttributeColor(attr.key)"
            opacity="0.3"
            class="data-point-glow"
          />
        </g>

        <!-- 属性标签 -->
        <g class="attribute-labels">
          <g v-for="(attr, index) in attributes" :key="`label-${index}`">
            <text
              :x="200 + 210 * Math.cos(getAngle(index))"
              :y="200 + 210 * Math.sin(getAngle(index))"
              :text-anchor="getLabelAnchor(index)"
              :dominant-baseline="getLabelBaseline(index)"
              fill="#66ffcc"
              font-size="16"
              font-weight="bold"
              class="attribute-label"
            >
              {{ attr.name }}
            </text>
            <text
              :x="200 + 210 * Math.cos(getAngle(index))"
              :y="200 + 210 * Math.sin(getAngle(index)) + 18"
              :text-anchor="getLabelAnchor(index)"
              :dominant-baseline="getLabelBaseline(index)"
              :fill="getAttributeColor(attr.key)"
              font-size="14"
              font-weight="bold"
            >
              {{ attr.value }}
            </text>
          </g>
        </g>
      </svg>
      
      <!-- 悬浮提示 -->
      <div
        v-if="tooltip.show"
        class="radar-tooltip"
        :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
      >
        <div class="tooltip-title">{{ tooltip.attr.name }}</div>
        <div class="tooltip-value">{{ tooltip.attr.value }}/100</div>
        <div class="tooltip-hint">点击查看详情</div>
      </div>
    </div>

    <!-- 自定义属性详情弹窗 -->
    <div v-if="modal.show" class="custom-modal-overlay" @click="closeModal">
      <div class="custom-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <div
              class="title-icon"
              :style="{ backgroundColor: getAttributeColor(modal.attr.key) }"
            ></div>
            <span>{{ modal.attr.name }}属性详情</span>
          </div>
          <button class="modal-close" @click="closeModal">
            <span>×</span>
          </button>
        </div>

        <div class="modal-body">
          <div class="attr-value-display">
            <div class="value-circle" :style="{ borderColor: getAttributeColor(modal.attr.key) }">
              <span class="value-number">{{ modal.attr.value }}</span>
              <span class="value-max">/100</span>
            </div>
          </div>

          <div class="attr-description">
            <h4>属性说明</h4>
            <p>{{ getAttributeDescription(modal.attr.key) }}</p>
          </div>

          <div class="attr-effects">
            <h4>当前效果</h4>
            <div class="effect-list">
              <div
                v-for="effect in getAttributeEffects(modal.attr.key, modal.attr.value)"
                :key="effect.name"
                class="effect-item"
              >
                <span class="effect-name">{{ effect.name }}：</span>
                <span class="effect-value" :class="effect.type">{{ effect.value }}</span>
              </div>
            </div>
          </div>

          <div class="attr-level">
            <h4>等级评价</h4>
            <div class="level-bar">
              <div
                class="level-fill"
                :style="{
                  width: modal.attr.value + '%',
                  backgroundColor: getAttributeColor(modal.attr.key)
                }"
              ></div>
            </div>
            <div class="level-text">{{ getAttributeLevel(modal.attr.value) }}</div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="modal-btn" @click="closeModal">确定</button>
        </div>
      </div>
    </div>
    
    <!-- 属性说明 -->
    <div class="attribute-legend">
      <div 
        v-for="attr in attributes" 
        :key="`legend-${attr.key}`"
        class="legend-item"
      >
        <div 
          class="legend-color" 
          :style="{ backgroundColor: getAttributeColor(attr.key) }"
        ></div>
        <span class="legend-name">{{ attr.name }}</span>
        <span class="legend-value">{{ attr.value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  playerData: {
    type: Object,
    required: true
  }
})

// 悬浮提示
const tooltip = ref({
  show: false,
  x: 0,
  y: 0,
  attr: null
})

// 模态框
const modal = ref({
  show: false,
  attr: null
})

// 属性数据
const attributes = computed(() => [
  { 
    key: 'strength', 
    name: '力量', 
    value: props.playerData.strength || 50 
  },
  { 
    key: 'spirit', 
    name: '精神', 
    value: props.playerData.spirit || 50 
  },
  { 
    key: 'agility', 
    name: '敏捷', 
    value: props.playerData.agility || 50 
  },
  { 
    key: 'constitution', 
    name: '体质', 
    value: props.playerData.constitution || 50 
  },
  { 
    key: 'perception', 
    name: '感知', 
    value: props.playerData.perception || 50 
  }
])

// 计算角度（从顶部开始，顺时针）
const getAngle = (index) => {
  return (index * 2 * Math.PI / 5) - Math.PI / 2
}

// 获取多边形点坐标
const getPolygonPoints = () => {
  return attributes.value.map((attr, index) => {
    const angle = getAngle(index)
    const radius = (attr.value / 100) * 180
    const x = 200 + radius * Math.cos(angle)
    const y = 200 + radius * Math.sin(angle)
    return `${x},${y}`
  }).join(' ')
}

// 获取属性颜色
const getAttributeColor = (key) => {
  const colors = {
    strength: '#FF6B6B',    // 红色 - 力量
    spirit: '#4ECDC4',      // 青色 - 精神
    agility: '#45B7D1',     // 蓝色 - 敏捷
    constitution: '#96CEB4', // 绿色 - 体质
    perception: '#FFEAA7'   // 黄色 - 感知
  }
  return colors[key] || '#66ffcc'
}

// 获取标签锚点
const getLabelAnchor = (index) => {
  const angle = getAngle(index)
  const x = Math.cos(angle)
  if (x > 0.1) return 'start'
  if (x < -0.1) return 'end'
  return 'middle'
}

// 获取标签基线
const getLabelBaseline = (index) => {
  const angle = getAngle(index)
  const y = Math.sin(angle)
  if (y > 0.1) return 'hanging'
  if (y < -0.1) return 'baseline'
  return 'middle'
}

// 获取属性描述
const getAttributeDescription = (key) => {
  const descriptions = {
    strength: '影响物理攻击力和负重能力',
    spirit: '影响理智值和魔法抗性',
    agility: '影响闪避率和行动速度',
    constitution: '影响生命值和抗毒能力',
    perception: '影响发现隐藏物品和危险感知'
  }
  return descriptions[key] || ''
}

// 显示提示
const showTooltip = (attr, event) => {
  const rect = event.target.getBoundingClientRect()
  tooltip.value = {
    show: true,
    x: rect.left + rect.width / 2,
    y: rect.top - 10,
    attr
  }
}

// 隐藏提示
const hideTooltip = () => {
  tooltip.value.show = false
}

// 显示详情模态框
const showDetailModal = (attr) => {
  modal.value = {
    show: true,
    attr
  }
  hideTooltip()
}

// 关闭模态框
const closeModal = () => {
  modal.value.show = false
}

// 获取属性效果
const getAttributeEffects = (key, value) => {
  const effects = {
    strength: [
      { name: '物理攻击力', value: `+${Math.floor(value * 0.5)}`, type: 'positive' },
      { name: '负重能力', value: `+${Math.floor(value * 0.3)}kg`, type: 'positive' },
      { name: '破坏力', value: `+${Math.floor(value * 0.2)}%`, type: 'positive' }
    ],
    spirit: [
      { name: '理智上限', value: `+${Math.floor(value * 0.8)}`, type: 'positive' },
      { name: '魔法抗性', value: `+${Math.floor(value * 0.4)}%`, type: 'positive' },
      { name: '恐惧抗性', value: `+${Math.floor(value * 0.3)}%`, type: 'positive' }
    ],
    agility: [
      { name: '闪避率', value: `+${Math.floor(value * 0.3)}%`, type: 'positive' },
      { name: '行动速度', value: `+${Math.floor(value * 0.2)}%`, type: 'positive' },
      { name: '暴击率', value: `+${Math.floor(value * 0.1)}%`, type: 'positive' }
    ],
    constitution: [
      { name: '生命值上限', value: `+${Math.floor(value * 1.2)}`, type: 'positive' },
      { name: '抗毒能力', value: `+${Math.floor(value * 0.5)}%`, type: 'positive' },
      { name: '恢复速度', value: `+${Math.floor(value * 0.3)}%`, type: 'positive' }
    ],
    perception: [
      { name: '发现概率', value: `+${Math.floor(value * 0.4)}%`, type: 'positive' },
      { name: '危险感知', value: `+${Math.floor(value * 0.3)}%`, type: 'positive' },
      { name: '远程精度', value: `+${Math.floor(value * 0.2)}%`, type: 'positive' }
    ]
  }
  return effects[key] || []
}

// 获取属性等级
const getAttributeLevel = (value) => {
  if (value >= 90) return '传奇 (90-100)'
  if (value >= 80) return '卓越 (80-89)'
  if (value >= 70) return '优秀 (70-79)'
  if (value >= 60) return '良好 (60-69)'
  if (value >= 50) return '普通 (50-59)'
  if (value >= 40) return '较差 (40-49)'
  if (value >= 30) return '糟糕 (30-39)'
  return '极差 (0-29)'
}
</script>

<style lang="scss" scoped>
.attribute-radar {
  background: rgba(0, 20, 40, 0.9);
  border-radius: 12px;
  padding: 1rem;
  border: 2px solid #66ffcc;
}

.radar-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.radar-chart {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 0 10px rgba(102, 255, 204, 0.3));
}

.data-polygon {
  transition: all 0.3s ease;
  
  &:hover {
    fill: rgba(102, 255, 204, 0.3);
  }
}

.data-point {
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    r: 10;
    filter: drop-shadow(0 0 12px currentColor);
  }
}

.data-point-glow {
  pointer-events: none;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

.attribute-label {
  cursor: default;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
}

.radar-tooltip {
  position: fixed;
  background: rgba(0, 20, 40, 0.95);
  border: 1px solid #66ffcc;
  border-radius: 6px;
  padding: 8px 12px;
  color: #66ffcc;
  font-size: 12px;
  z-index: 1000;
  pointer-events: none;
  transform: translateX(-50%) translateY(-100%);
  
  .tooltip-title {
    font-weight: bold;
    margin-bottom: 4px;
  }
  
  .tooltip-value {
    color: #FFD700;
    font-weight: bold;
    margin-bottom: 4px;
  }
  
  .tooltip-hint {
    color: #66ffcc;
    font-size: 10px;
    font-style: italic;
    margin-top: 4px;
  }
}

// 自定义模态框样式
.custom-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
}

.custom-modal {
  background: linear-gradient(135deg, rgba(0, 20, 40, 0.95), rgba(0, 30, 60, 0.95));
  border: 2px solid #66ffcc;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.5),
    0 0 30px rgba(102, 255, 204, 0.3);
  animation: modalSlideIn 0.3s ease;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(102, 255, 204, 0.3);
  background: rgba(102, 255, 204, 0.1);

  .modal-title {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #66ffcc;
    font-size: 1.2rem;
    font-weight: bold;

    .title-icon {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 2px solid #fff;
    }
  }

  .modal-close {
    background: none;
    border: none;
    color: #66ffcc;
    font-size: 2rem;
    cursor: pointer;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.3s ease;

    &:hover {
      background: rgba(255, 255, 255, 0.1);
      transform: rotate(90deg);
    }
  }
}

.attribute-legend {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  
  .legend-color {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.3);
  }
  
  .legend-name {
    color: #66ffcc;
    flex: 1;
  }
  
  .legend-value {
    color: #FFD700;
    font-weight: bold;
  }
}

.modal-body {
  padding: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;

  h4 {
    color: #66ffcc;
    margin: 1rem 0 0.5rem 0;
    font-size: 1rem;
    border-bottom: 1px solid rgba(102, 255, 204, 0.3);
    padding-bottom: 0.5rem;

    &:first-child {
      margin-top: 0;
    }
  }
}

.attr-value-display {
  text-align: center;
  margin-bottom: 1.5rem;

  .value-circle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    border: 4px solid;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.3);
    position: relative;

    .value-number {
      font-size: 2.5rem;
      font-weight: bold;
      color: #fff;
    }

    .value-max {
      font-size: 1rem;
      color: #ccc;
      margin-left: 4px;
    }
  }
}

.attr-description {
  p {
    color: #ccc;
    line-height: 1.6;
    margin: 0;
  }
}

.effect-list {
  display: grid;
  gap: 8px;
}

.effect-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  border-left: 3px solid #66ffcc;

  .effect-name {
    color: #ccc;
  }

  .effect-value {
    font-weight: bold;

    &.positive {
      color: #4CAF50;
    }

    &.negative {
      color: #f44336;
    }
  }
}

.attr-level {
  .level-bar {
    width: 100%;
    height: 12px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 6px;
    overflow: hidden;
    margin: 8px 0;

    .level-fill {
      height: 100%;
      transition: width 0.5s ease;
      border-radius: 6px;
    }
  }

  .level-text {
    text-align: center;
    color: #FFD700;
    font-weight: bold;
    font-size: 0.9rem;
  }
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(102, 255, 204, 0.3);
  text-align: center;
  background: rgba(0, 0, 0, 0.2);

  .modal-btn {
    background: linear-gradient(45deg, #66ffcc, #4dd4ac);
    border: none;
    color: #001122;
    padding: 10px 30px;
    border-radius: 25px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(102, 255, 204, 0.4);
    }
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 768px) {
  .attribute-radar {
    padding: 0.5rem;
  }

  .radar-container {
    max-width: 380px; // 移动端增大雷达图
  }

  .attribute-legend {
    grid-template-columns: repeat(2, 1fr);
  }

  .custom-modal {
    width: 95%;
    margin: 1rem;
  }

  .modal-header {
    padding: 1rem;

    .modal-title {
      font-size: 1rem;
    }
  }

  .modal-body {
    padding: 1rem;

    .attr-value-display .value-circle {
      width: 100px;
      height: 100px;

      .value-number {
        font-size: 2rem;
      }
    }
  }
}

@media (max-width: 1200px) {
  .radar-container {
    max-width: 450px; // 中等屏幕适中大小
  }
}

@media (max-width: 480px) {
  .radar-container {
    max-width: 300px; // 小屏幕适当减小
  }

  .attribute-legend {
    grid-template-columns: 1fr; // 单列显示
    gap: 4px;
  }

  .legend-item {
    font-size: 10px;
    gap: 3px;

    .legend-color {
      width: 8px;
      height: 8px;
    }
  }
}
</style>
