<template>
  <div class="attribute-radar">
    <div class="radar-container">
      <svg class="radar-chart" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
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
        <circle cx="150" cy="150" r="140" fill="url(#radarGradient)" stroke="#66ffcc" stroke-width="1" opacity="0.3"/>
        
        <!-- 网格线 -->
        <g class="grid-lines">
          <!-- 同心圆 -->
          <circle v-for="i in 5" :key="`circle-${i}`" 
                  cx="150" cy="150" 
                  :r="i * 28" 
                  fill="none" 
                  stroke="#66ffcc" 
                  stroke-width="1" 
                  opacity="0.3"/>
          
          <!-- 五条射线 -->
          <g v-for="(attr, index) in attributes" :key="`line-${index}`">
            <line 
              x1="150" y1="150"
              :x2="150 + 140 * Math.cos(getAngle(index))"
              :y2="150 + 140 * Math.sin(getAngle(index))"
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
            :cx="150 + (attr.value / 100) * 140 * Math.cos(getAngle(index))"
            :cy="150 + (attr.value / 100) * 140 * Math.sin(getAngle(index))"
            r="4"
            :fill="getAttributeColor(attr.key)"
            stroke="#fff"
            stroke-width="1"
            class="data-point"
            @mouseover="showTooltip(attr, $event)"
            @mouseout="hideTooltip"
          />
        </g>
        
        <!-- 属性标签 -->
        <g class="attribute-labels">
          <g v-for="(attr, index) in attributes" :key="`label-${index}`">
            <text 
              :x="150 + 160 * Math.cos(getAngle(index))"
              :y="150 + 160 * Math.sin(getAngle(index))"
              :text-anchor="getLabelAnchor(index)"
              :dominant-baseline="getLabelBaseline(index)"
              fill="#66ffcc"
              font-size="14"
              font-weight="bold"
              class="attribute-label"
            >
              {{ attr.name }}
            </text>
            <text 
              :x="150 + 160 * Math.cos(getAngle(index))"
              :y="150 + 160 * Math.sin(getAngle(index)) + 16"
              :text-anchor="getLabelAnchor(index)"
              :dominant-baseline="getLabelBaseline(index)"
              :fill="getAttributeColor(attr.key)"
              font-size="12"
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
        <div class="tooltip-desc">{{ getAttributeDescription(tooltip.attr.key) }}</div>
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
    const radius = (attr.value / 100) * 140
    const x = 150 + radius * Math.cos(angle)
    const y = 150 + radius * Math.sin(angle)
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
  max-width: 300px;
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
    r: 6;
    filter: drop-shadow(0 0 8px currentColor);
  }
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
  
  .tooltip-desc {
    color: #ccc;
    font-size: 11px;
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

@media (max-width: 768px) {
  .attribute-radar {
    padding: 0.5rem;
  }
  
  .radar-container {
    max-width: 250px;
  }
  
  .attribute-legend {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
