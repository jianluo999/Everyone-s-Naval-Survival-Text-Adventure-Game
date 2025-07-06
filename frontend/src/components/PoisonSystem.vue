<template>
  <div class="poison-system">
    <h4>☠️ 毒素与感染</h4>
    
    <!-- 毒素效果列表 -->
    <div class="poison-effects" v-if="activePoisonEffects.length > 0">
      <div 
        v-for="poison in activePoisonEffects" 
        :key="poison.id"
        class="poison-item"
        :class="[poison.type, poison.severity]"
      >
        <div class="poison-icon">{{ getPoisonIcon(poison.type) }}</div>
        <div class="poison-info">
          <div class="poison-name">{{ getPoisonName(poison.type) }}</div>
          <div class="poison-stage">{{ getStageText(poison.stage) }}</div>
          <div class="poison-timer" v-if="poison.duration > 0">
            {{ formatTime(poison.duration) }}
          </div>
        </div>
        <div class="poison-progress">
          <div 
            class="progress-bar" 
            :style="{ 
              width: (poison.progress / poison.maxProgress) * 100 + '%',
              backgroundColor: getPoisonColor(poison.type)
            }"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- 治疗选项 -->
    <div class="treatment-options" v-if="availableTreatments.length > 0">
      <h5>🩹 可用治疗</h5>
      <div class="treatment-list">
        <div 
          v-for="treatment in availableTreatments" 
          :key="treatment.id"
          class="treatment-item"
          @click="applyTreatment(treatment)"
        >
          <div class="treatment-icon">{{ treatment.icon }}</div>
          <div class="treatment-info">
            <div class="treatment-name">{{ treatment.name }}</div>
            <div class="treatment-effect">{{ treatment.description }}</div>
          </div>
          <div class="treatment-cost" v-if="treatment.cost">
            {{ treatment.cost }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- 毒素详情弹窗 -->
    <el-dialog
      v-model="detailsVisible"
      :title="selectedPoison?.name || '毒素详情'"
      width="400px"
      class="poison-dialog"
    >
      <div v-if="selectedPoison" class="poison-details">
        <div class="poison-icon-large">
          {{ getPoisonIcon(selectedPoison.type) }}
        </div>
        
        <div class="poison-description">
          {{ getPoisonDescription(selectedPoison) }}
        </div>
        
        <div class="poison-stages">
          <h4>毒素阶段：</h4>
          <div 
            v-for="(stage, index) in selectedPoison.stages" 
            :key="index"
            class="stage-item"
            :class="{ 'current': index === selectedPoison.stage }"
          >
            <div class="stage-number">{{ index + 1 }}</div>
            <div class="stage-info">
              <div class="stage-name">{{ stage.name }}</div>
              <div class="stage-effects">
                <span 
                  v-for="(value, key) in stage.effects" 
                  :key="key"
                  class="effect-tag"
                  :class="{ negative: value < 0, positive: value > 0 }"
                >
                  {{ getAttributeName(key) }}: {{ value > 0 ? '+' : '' }}{{ value }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailsVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'

const gameStore = useGameStore()

// 响应式数据
const detailsVisible = ref(false)
const selectedPoison = ref(null)

// 毒素效果数据
const poisonEffects = ref([
  {
    id: 'corpse_poison_001',
    type: 'corpse_poison',
    severity: 'severe',
    stage: 2,
    progress: 150,
    maxProgress: 200,
    duration: 7200, // 秒
    source: '溺亡者抓伤',
    stages: [
      {
        name: '轻微感染',
        effects: { health: -1, sanity: -1 }
      },
      {
        name: '中度感染',
        effects: { health: -2, strength: -1, agility: -1 }
      },
      {
        name: '严重感染',
        effects: { health: -3, strength: -2, agility: -2, sanity: -2 }
      },
      {
        name: '尸毒扩散',
        effects: { health: -5, strength: -3, agility: -3, sanity: -5 }
      }
    ]
  },
  {
    id: 'pufferfish_poison_001',
    type: 'pufferfish_poison',
    severity: 'moderate',
    stage: 1,
    progress: 80,
    maxProgress: 120,
    duration: 1800,
    source: '囊肿刺豚毒素',
    stages: [
      {
        name: '轻微中毒',
        effects: { agility: -1, perception: -1 }
      },
      {
        name: '神经麻痹',
        effects: { agility: -3, perception: -2, strength: -1 }
      },
      {
        name: '呼吸困难',
        effects: { health: -2, agility: -5, perception: -3 }
      }
    ]
  }
])

// 可用治疗方案
const availableTreatments = ref([
  {
    id: 'holy_water',
    name: '圣水',
    icon: '💧',
    description: '可治愈多种毒素和诅咒',
    effectiveness: {
      corpse_poison: 80,
      pufferfish_poison: 60,
      curse: 90
    },
    cost: '1瓶圣水'
  },
  {
    id: 'medical_bandage',
    name: '医疗绷带',
    icon: '🩹',
    description: '减缓感染扩散',
    effectiveness: {
      corpse_poison: 30,
      bleeding: 70
    },
    cost: '1个绷带'
  },
  {
    id: 'salt',
    name: '神圣的盐',
    icon: '🧂',
    description: '可解除轻微诅咒和感染',
    effectiveness: {
      corpse_poison: 20,
      curse: 50,
      evil_influence: 80
    },
    cost: '1包盐'
  }
])

// 计算属性
const activePoisonEffects = computed(() => {
  return poisonEffects.value.filter(poison => poison.duration > 0)
})

// 方法
const getPoisonIcon = (type) => {
  const icons = {
    corpse_poison: '🦠',
    pufferfish_poison: '🐡',
    snake_venom: '🐍',
    spider_venom: '🕷️',
    curse: '👻',
    disease: '🤒',
    radiation: '☢️'
  }
  return icons[type] || '☠️'
}

const getPoisonName = (type) => {
  const names = {
    corpse_poison: '尸毒感染',
    pufferfish_poison: '河豚毒素',
    snake_venom: '蛇毒',
    spider_venom: '蛛毒',
    curse: '诅咒',
    disease: '疾病',
    radiation: '辐射'
  }
  return names[type] || '未知毒素'
}

const getStageText = (stage) => {
  const stages = ['I', 'II', 'III', 'IV', 'V']
  return `阶段 ${stages[stage] || stage + 1}`
}

const getPoisonColor = (type) => {
  const colors = {
    corpse_poison: '#8e44ad',
    pufferfish_poison: '#e67e22',
    snake_venom: '#27ae60',
    spider_venom: '#2c3e50',
    curse: '#9b59b6',
    disease: '#e74c3c',
    radiation: '#f1c40f'
  }
  return colors[type] || '#95a5a6'
}

const getPoisonDescription = (poison) => {
  const descriptions = {
    corpse_poison: '由死灵生物传播的恶性感染，会逐渐侵蚀生者的血肉和理智。如不及时治疗，最终会导致死亡或转化为不死生物。',
    pufferfish_poison: '来自深海囊肿刺豚的神经毒素，会导致肌肉麻痹和感知能力下降。虽然致命性较低，但会严重影响战斗能力。',
    snake_venom: '毒蛇分泌的剧毒，会破坏血液循环系统。',
    spider_venom: '巨型蜘蛛的毒液，具有强烈的麻痹效果。',
    curse: '来自邪恶力量的诅咒，会持续削弱受害者。',
    disease: '各种疾病的统称，需要适当的医疗处理。',
    radiation: '神秘能量的辐射，会造成基因层面的损伤。'
  }
  return descriptions[poison.type] || '未知的有害效果'
}

const getAttributeName = (key) => {
  const names = {
    health: '生命',
    sanity: '理智',
    strength: '力量',
    agility: '敏捷',
    perception: '感知',
    energy: '精力'
  }
  return names[key] || key
}

const formatTime = (seconds) => {
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

const applyTreatment = (treatment) => {
  // 检查是否有对应的物品
  // const hasItem = gameStore.hasItem(treatment.id)
  // if (!hasItem) {
  //   ElMessage.error('没有足够的治疗物品')
  //   return
  // }
  
  // 应用治疗效果
  let treatedCount = 0
  poisonEffects.value.forEach(poison => {
    if (treatment.effectiveness[poison.type]) {
      const effectiveness = treatment.effectiveness[poison.type]
      const reduction = Math.floor(poison.progress * (effectiveness / 100))
      poison.progress = Math.max(0, poison.progress - reduction)
      
      // 如果毒素被完全清除
      if (poison.progress === 0) {
        poison.duration = 0
        treatedCount++
      }
    }
  })
  
  if (treatedCount > 0) {
    ElMessage.success(`使用${treatment.name}治疗了${treatedCount}种毒素`)
    // gameStore.removeItem(treatment.id, 1)
  } else {
    ElMessage.warning(`${treatment.name}对当前毒素无效`)
  }
}

const showPoisonDetails = (poison) => {
  selectedPoison.value = poison
  detailsVisible.value = true
}

// 毒素进展定时器
let poisonTimer = null

const updatePoisonEffects = () => {
  poisonEffects.value.forEach(poison => {
    if (poison.duration > 0) {
      poison.duration = Math.max(0, poison.duration - 1)
      
      // 毒素进展
      if (poison.progress < poison.maxProgress) {
        poison.progress += 1
        
        // 检查是否进入下一阶段
        const stageThreshold = poison.maxProgress / poison.stages.length
        const newStage = Math.floor(poison.progress / stageThreshold)
        
        if (newStage > poison.stage && newStage < poison.stages.length) {
          poison.stage = newStage
          ElMessage.warning(`${getPoisonName(poison.type)}进入${getStageText(newStage)}`)
        }
      }
      
      // 应用毒素效果
      const currentStage = poison.stages[poison.stage]
      if (currentStage && currentStage.effects) {
        // 这里应该调用游戏商店的方法来应用效果
        // gameStore.applyPoisonEffects(currentStage.effects)
      }
    }
  })
  
  // 移除已过期的毒素
  poisonEffects.value = poisonEffects.value.filter(poison => poison.duration > 0)
}

// 添加新的毒素效果
const addPoisonEffect = (poisonData) => {
  const existingPoison = poisonEffects.value.find(p => p.type === poisonData.type)
  
  if (existingPoison) {
    // 如果已存在相同类型的毒素，增加持续时间和进度
    existingPoison.duration = Math.max(existingPoison.duration, poisonData.duration)
    existingPoison.progress = Math.min(existingPoison.maxProgress, existingPoison.progress + (poisonData.progress || 50))
  } else {
    // 添加新的毒素效果
    poisonEffects.value.push({
      id: Date.now().toString(),
      ...poisonData
    })
  }
  
  ElMessage.error(`受到${getPoisonName(poisonData.type)}影响！`)
}

// 生命周期
onMounted(() => {
  // 每秒更新一次毒素效果
  poisonTimer = setInterval(updatePoisonEffects, 1000)
})

onUnmounted(() => {
  if (poisonTimer) {
    clearInterval(poisonTimer)
  }
})

// 暴露方法供外部调用
defineExpose({
  addPoisonEffect,
  activePoisonEffects,
  applyTreatment
})
</script>

<style lang="scss" scoped>
.poison-system {
  background: rgba(142, 68, 173, 0.1);
  border: 1px solid rgba(142, 68, 173, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0.5rem 0;
}

h4 {
  margin: 0 0 1rem 0;
  color: #8e44ad;
  font-size: 0.9rem;
}

h5 {
  margin: 1rem 0 0.5rem 0;
  color: #27ae60;
  font-size: 0.8rem;
}

.poison-effects {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.poison-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.3rem;
  background: rgba(0, 0, 0, 0.2);
  border-left: 3px solid;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(0, 0, 0, 0.3);
    transform: translateX(2px);
  }
  
  &.corpse_poison {
    border-left-color: #8e44ad;
  }
  
  &.pufferfish_poison {
    border-left-color: #e67e22;
  }
  
  &.severe {
    animation: poisonPulse 2s ease-in-out infinite;
  }
}

.poison-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.poison-info {
  flex: 1;
  min-width: 0;
}

.poison-name {
  font-weight: bold;
  color: #fff;
  font-size: 0.8rem;
}

.poison-stage {
  font-size: 0.7rem;
  color: #e67e22;
  margin: 0.1rem 0;
}

.poison-timer {
  font-size: 0.7rem;
  color: #3498db;
}

.poison-progress {
  width: 40px;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  margin-left: 0.5rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 2px;
  transition: width 1s ease;
}

.treatment-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.treatment-item {
  display: flex;
  align-items: center;
  padding: 0.4rem;
  border-radius: 0.3rem;
  background: rgba(46, 204, 113, 0.1);
  border: 1px solid rgba(46, 204, 113, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(46, 204, 113, 0.2);
    border-color: rgba(46, 204, 113, 0.5);
  }
}

.treatment-icon {
  font-size: 1rem;
  margin-right: 0.5rem;
}

.treatment-info {
  flex: 1;
}

.treatment-name {
  font-weight: bold;
  color: #2ecc71;
  font-size: 0.8rem;
}

.treatment-effect {
  font-size: 0.7rem;
  color: #bbb;
}

.treatment-cost {
  font-size: 0.7rem;
  color: #f39c12;
}

.poison-dialog {
  :deep(.el-dialog) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid rgba(142, 68, 173, 0.3);
  }
  
  :deep(.el-dialog__title) {
    color: #8e44ad;
  }
}

.poison-details {
  text-align: center;
}

.poison-icon-large {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.poison-description {
  color: #bbb;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  text-align: left;
}

.poison-stages {
  text-align: left;
  
  h4 {
    color: #e67e22;
    margin-bottom: 0.5rem;
  }
}

.stage-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  margin: 0.3rem 0;
  border-radius: 0.3rem;
  background: rgba(255, 255, 255, 0.05);
  
  &.current {
    background: rgba(230, 126, 34, 0.2);
    border: 1px solid rgba(230, 126, 34, 0.5);
  }
}

.stage-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #fff;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.stage-info {
  flex: 1;
}

.stage-name {
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.2rem;
}

.stage-effects {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem;
}

.effect-tag {
  font-size: 0.7rem;
  padding: 0.1rem 0.3rem;
  border-radius: 0.2rem;
  
  &.negative {
    background: rgba(231, 76, 60, 0.3);
    color: #e74c3c;
  }
  
  &.positive {
    background: rgba(46, 204, 113, 0.3);
    color: #2ecc71;
  }
}

// 动画
@keyframes poisonPulse {
  0%, 100% { box-shadow: 0 0 5px rgba(142, 68, 173, 0.5); }
  50% { box-shadow: 0 0 15px rgba(142, 68, 173, 0.8); }
}
</style>
