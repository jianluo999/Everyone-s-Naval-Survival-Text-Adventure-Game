<template>
  <div class="status-effects">
    <h4>🩹 状态效果</h4>
    
    <!-- 状态效果列表 -->
    <div class="effects-list" v-if="activeEffects.length > 0">
      <div 
        v-for="effect in activeEffects" 
        :key="effect.id"
        class="effect-item"
        :class="[effect.type, effect.severity]"
        @mouseenter="showTooltip(effect, $event)"
        @mouseleave="hideTooltip"
      >
        <div class="effect-icon">{{ getEffectIcon(effect.type) }}</div>
        <div class="effect-info">
          <div class="effect-name">{{ getEffectName(effect.type) }}</div>
          <div class="effect-severity">{{ getSeverityText(effect.severity) }}</div>
          <div class="effect-duration" v-if="effect.duration > 0">
            {{ formatDuration(effect.duration) }}
          </div>
        </div>
        <div class="effect-progress" v-if="effect.maxDuration > 0">
          <div 
            class="progress-bar" 
            :style="{ width: (effect.duration / effect.maxDuration) * 100 + '%' }"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- 无状态效果时的显示 -->
    <div v-else class="no-effects">
      <span class="healthy-status">✨ 状态良好</span>
    </div>
    
    <!-- 状态效果详情提示框 -->
    <div 
      v-if="tooltipVisible" 
      class="effect-tooltip"
      :style="tooltipStyle"
    >
      <div class="tooltip-header">
        <span class="tooltip-icon">{{ getEffectIcon(tooltipEffect.type) }}</span>
        <span class="tooltip-title">{{ getEffectName(tooltipEffect.type) }}</span>
        <span class="tooltip-severity" :class="tooltipEffect.severity">
          {{ getSeverityText(tooltipEffect.severity) }}
        </span>
      </div>
      <div class="tooltip-description">
        {{ getEffectDescription(tooltipEffect) }}
      </div>
      <div class="tooltip-effects" v-if="tooltipEffect.effects">
        <div class="effects-title">影响：</div>
        <div 
          v-for="(value, key) in tooltipEffect.effects" 
          :key="key"
          class="effect-modifier"
          :class="{ positive: value > 0, negative: value < 0 }"
        >
          {{ getAttributeName(key) }}: {{ value > 0 ? '+' : '' }}{{ value }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()

// 响应式数据
const tooltipVisible = ref(false)
const tooltipEffect = ref(null)
const tooltipStyle = ref({})

// 模拟状态效果数据（实际应该从游戏商店获取）
const statusEffects = ref([
  {
    id: 'infection_001',
    type: 'infection',
    severity: 'severe',
    duration: 3600, // 秒
    maxDuration: 7200,
    effects: {
      health: -2,
      strength: -2,
      agility: -1
    },
    source: '尸毒感染'
  },
  {
    id: 'fever_001',
    type: 'fever',
    severity: 'moderate',
    duration: 1800,
    maxDuration: 3600,
    effects: {
      energy: -1,
      perception: -1
    },
    source: '感染引起的发烧'
  },
  {
    id: 'food_poisoning_001',
    type: 'poisoning',
    severity: 'mild',
    duration: 900,
    maxDuration: 1800,
    effects: {
      health: -1,
      thirst: -2
    },
    source: '食物中毒'
  }
])

// 计算属性
const activeEffects = computed(() => {
  return statusEffects.value.filter(effect => effect.duration > 0)
})

// 方法
const getEffectIcon = (type) => {
  const icons = {
    infection: '🦠',
    fever: '🌡️',
    poisoning: '☠️',
    bleeding: '🩸',
    exhaustion: '😴',
    madness: '🌀',
    curse: '👻',
    blessing: '✨',
    regeneration: '💚',
    strength: '💪',
    weakness: '😵',
    paralysis: '🥶'
  }
  return icons[type] || '❓'
}

const getEffectName = (type) => {
  const names = {
    infection: '感染',
    fever: '发烧',
    poisoning: '中毒',
    bleeding: '流血',
    exhaustion: '疲惫',
    madness: '疯狂',
    curse: '诅咒',
    blessing: '祝福',
    regeneration: '再生',
    strength: '力量增强',
    weakness: '虚弱',
    paralysis: '麻痹'
  }
  return names[type] || '未知状态'
}

const getSeverityText = (severity) => {
  const texts = {
    mild: '轻微',
    moderate: '中度',
    severe: '严重',
    critical: '危急'
  }
  return texts[severity] || severity
}

const getEffectDescription = (effect) => {
  const descriptions = {
    infection: '伤口感染，需要医疗处理。持续损失生命值和属性。',
    fever: '体温升高，影响精力和感知能力。',
    poisoning: '食物中毒，导致腹泻和脱水。',
    bleeding: '持续失血，需要包扎伤口。',
    exhaustion: '极度疲劳，所有行动效率降低。',
    madness: '精神错乱，理智值持续下降。',
    curse: '被诅咒，各种负面效果随机出现。',
    blessing: '受到祝福，获得正面效果加成。',
    regeneration: '快速恢复生命值。',
    strength: '力量得到增强。',
    weakness: '身体虚弱，各项能力下降。',
    paralysis: '身体麻痹，无法正常行动。'
  }
  return descriptions[effect.type] || '未知效果'
}

const getAttributeName = (key) => {
  const names = {
    health: '生命',
    energy: '精力',
    sanity: '理智',
    strength: '力量',
    agility: '敏捷',
    perception: '感知',
    thirst: '水分',
    hunger: '饥饿'
  }
  return names[key] || key
}

const formatDuration = (seconds) => {
  if (seconds < 60) {
    return `${seconds}秒`
  } else if (seconds < 3600) {
    return `${Math.floor(seconds / 60)}分钟`
  } else {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}小时${minutes > 0 ? minutes + '分钟' : ''}`
  }
}

const showTooltip = (effect, event) => {
  tooltipEffect.value = effect
  tooltipVisible.value = true
  
  const rect = event.target.getBoundingClientRect()
  tooltipStyle.value = {
    position: 'fixed',
    left: rect.right + 10 + 'px',
    top: rect.top + 'px',
    zIndex: 1000
  }
}

const hideTooltip = () => {
  tooltipVisible.value = false
  tooltipEffect.value = null
}

// 状态效果更新定时器
let effectTimer = null

const updateEffects = () => {
  statusEffects.value.forEach(effect => {
    if (effect.duration > 0) {
      effect.duration = Math.max(0, effect.duration - 1)
      
      // 应用效果
      if (effect.effects) {
        // 这里应该调用游戏商店的方法来应用效果
        // gameStore.applyStatusEffect(effect)
      }
    }
  })
  
  // 移除已过期的效果
  statusEffects.value = statusEffects.value.filter(effect => effect.duration > 0)
}

// 生命周期
onMounted(() => {
  // 每秒更新一次状态效果
  effectTimer = setInterval(updateEffects, 1000)
})

onUnmounted(() => {
  if (effectTimer) {
    clearInterval(effectTimer)
  }
})

// 暴露方法供外部调用
const addStatusEffect = (effectData) => {
  const existingEffect = statusEffects.value.find(e => e.type === effectData.type)
  
  if (existingEffect) {
    // 如果已存在相同类型的效果，更新持续时间和严重程度
    existingEffect.duration = Math.max(existingEffect.duration, effectData.duration)
    if (getSeverityLevel(effectData.severity) > getSeverityLevel(existingEffect.severity)) {
      existingEffect.severity = effectData.severity
      existingEffect.effects = effectData.effects
    }
  } else {
    // 添加新的状态效果
    statusEffects.value.push({
      id: Date.now().toString(),
      ...effectData
    })
  }
}

const removeStatusEffect = (effectId) => {
  const index = statusEffects.value.findIndex(e => e.id === effectId)
  if (index !== -1) {
    statusEffects.value.splice(index, 1)
  }
}

const getSeverityLevel = (severity) => {
  const levels = { mild: 1, moderate: 2, severe: 3, critical: 4 }
  return levels[severity] || 0
}

defineExpose({
  addStatusEffect,
  removeStatusEffect,
  activeEffects
})
</script>

<style lang="scss" scoped>
.status-effects {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0.5rem 0;
  border: 1px solid rgba(255, 255, 255, 0.1);
  
  h4 {
    margin: 0 0 0.5rem 0;
    color: #fff;
    font-size: 0.9rem;
  }
}

.effects-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.effect-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.3rem;
  border-left: 3px solid;
  background: rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateX(2px);
  }
  
  &.infection {
    border-left-color: #e74c3c;
    &.severe { background: rgba(231, 76, 60, 0.1); }
    &.moderate { background: rgba(231, 76, 60, 0.05); }
    &.mild { background: rgba(231, 76, 60, 0.03); }
  }
  
  &.fever {
    border-left-color: #f39c12;
    &.severe { background: rgba(243, 156, 18, 0.1); }
    &.moderate { background: rgba(243, 156, 18, 0.05); }
    &.mild { background: rgba(243, 156, 18, 0.03); }
  }
  
  &.poisoning {
    border-left-color: #8e44ad;
    &.severe { background: rgba(142, 68, 173, 0.1); }
    &.moderate { background: rgba(142, 68, 173, 0.05); }
    &.mild { background: rgba(142, 68, 173, 0.03); }
  }
  
  &.blessing {
    border-left-color: #2ecc71;
    background: rgba(46, 204, 113, 0.1);
  }
}

.effect-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.effect-info {
  flex: 1;
  min-width: 0;
}

.effect-name {
  font-weight: bold;
  color: #fff;
  font-size: 0.8rem;
}

.effect-severity {
  font-size: 0.7rem;
  opacity: 0.8;
  color: #bbb;
}

.effect-duration {
  font-size: 0.7rem;
  color: #3498db;
  margin-top: 0.1rem;
}

.effect-progress {
  width: 40px;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  margin-left: 0.5rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2980b9);
  border-radius: 2px;
  transition: width 1s ease;
}

.no-effects {
  text-align: center;
  padding: 1rem;
  color: #2ecc71;
  font-size: 0.9rem;
}

.healthy-status {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

.effect-tooltip {
  background: rgba(0, 0, 0, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  padding: 0.8rem;
  max-width: 250px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
}

.tooltip-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tooltip-icon {
  font-size: 1.1rem;
}

.tooltip-title {
  font-weight: bold;
  color: #fff;
  flex: 1;
}

.tooltip-severity {
  font-size: 0.7rem;
  padding: 0.1rem 0.3rem;
  border-radius: 0.2rem;
  
  &.mild { background: rgba(46, 204, 113, 0.3); color: #2ecc71; }
  &.moderate { background: rgba(243, 156, 18, 0.3); color: #f39c12; }
  &.severe { background: rgba(231, 76, 60, 0.3); color: #e74c3c; }
  &.critical { background: rgba(192, 57, 43, 0.3); color: #c0392b; }
}

.tooltip-description {
  color: #bbb;
  font-size: 0.8rem;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.tooltip-effects {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 0.5rem;
}

.effects-title {
  font-size: 0.7rem;
  color: #3498db;
  margin-bottom: 0.3rem;
  font-weight: bold;
}

.effect-modifier {
  font-size: 0.7rem;
  margin: 0.1rem 0;
  
  &.positive { color: #2ecc71; }
  &.negative { color: #e74c3c; }
}
</style>
