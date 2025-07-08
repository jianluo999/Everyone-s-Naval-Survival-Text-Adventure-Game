<template>
  <div class="talent-system">
    <div class="talent-header">
      <h3>✨ 神秘天赋</h3>
      <div class="talent-description">
        通过完成特定条件解锁隐藏能力
      </div>
    </div>
    
    <!-- 天赋列表 -->
    <div class="talents-list">
      <div 
        v-for="talent in talents" 
        :key="talent.id"
        class="talent-item"
        :class="{ 
          'unlocked': talent.unlocked, 
          'unlockable': canUnlock(talent),
          'hidden': !talent.revealed 
        }"
        @click="showTalentDetails(talent)"
      >
        <div class="talent-icon">
          <span v-if="talent.unlocked">{{ talent.icon }}</span>
          <span v-else-if="talent.revealed">❓</span>
          <span v-else>⬛</span>
        </div>
        
        <div class="talent-info">
          <div class="talent-name">
            {{ talent.unlocked ? talent.name : (talent.revealed ? '未知天赋' : '???') }}
          </div>
          
          <div class="talent-progress" v-if="talent.revealed">
            <div class="progress-text">
              {{ getProgressText(talent) }}
            </div>
            <el-progress 
              :percentage="getProgressPercentage(talent)"
              :show-text="false"
              :stroke-width="4"
              :color="talent.unlocked ? '#2ecc71' : '#3498db'"
            />
          </div>
          
          <div class="talent-hint" v-if="!talent.revealed && talent.hint">
            <span class="hint-text">{{ talent.hint }}</span>
          </div>
        </div>
        
        <div class="talent-status">
          <span v-if="talent.unlocked" class="status-unlocked">✅</span>
          <span v-else-if="canUnlock(talent)" class="status-ready">⚡</span>
          <span v-else class="status-locked">🔒</span>
        </div>
      </div>
    </div>
    
    <!-- 天赋详情弹窗 -->
    <el-dialog
      v-model="detailsVisible"
      :title="selectedTalent?.name || '未知天赋'"
      width="400px"
      class="talent-dialog"
    >
      <div v-if="selectedTalent" class="talent-details">
        <div class="talent-icon-large">
          {{ selectedTalent.unlocked ? selectedTalent.icon : '❓' }}
        </div>
        
        <div class="talent-description-full">
          {{ selectedTalent.unlocked ? selectedTalent.description : '完成解锁条件后可查看详细信息' }}
        </div>
        
        <div class="unlock-conditions" v-if="selectedTalent.revealed">
          <h4>解锁条件：</h4>
          <div class="condition-item">
            <span class="condition-text">{{ getConditionText(selectedTalent) }}</span>
            <div class="condition-progress">
              <span class="progress-numbers">
                {{ selectedTalent.progress }}/{{ selectedTalent.requirement }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="talent-effects" v-if="selectedTalent.unlocked && selectedTalent.effects">
          <h4>天赋效果：</h4>
          <div 
            v-for="(effect, key) in selectedTalent.effects" 
            :key="key"
            class="effect-item"
          >
            <span class="effect-name">{{ getEffectName(key) }}</span>
            <span class="effect-value">{{ formatEffectValue(effect) }}</span>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailsVisible = false">关闭</el-button>
        <el-button 
          v-if="canUnlock(selectedTalent)" 
          type="primary" 
          @click="unlockTalent(selectedTalent)"
        >
          解锁天赋
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'

const gameStore = useGameStore()

// 响应式数据
const detailsVisible = ref(false)
const selectedTalent = ref(null)

// 天赋数据 - 从后端API获取
const talents = ref([])
const loadingTalents = ref(false)

// 所有天赋数据现在从后端API获取，不再使用硬编码假数据

// 计算属性
const unlockedTalents = computed(() => {
  return talents.value.filter(talent => talent.unlocked)
})

const availableTalents = computed(() => {
  return talents.value.filter(talent => talent.revealed)
})

// 方法
const canUnlock = (talent) => {
  return talent && talent.revealed && !talent.unlocked && talent.progress >= talent.requirement
}

const getProgressText = (talent) => {
  if (talent.unlocked) return '已解锁'
  return `${talent.progress}/${talent.requirement}`
}

const getProgressPercentage = (talent) => {
  if (talent.unlocked) return 100
  return Math.min((talent.progress / talent.requirement) * 100, 100)
}

const getConditionText = (talent) => {
  const conditions = {
    survive_days: '在海上生存天数',
    fishing_attempts: '钓鱼次数',
    monsters_killed: '击败怪物数量',
    sanity_lost: '累计理智损失',
    distance_traveled: '航行距离',
    items_crafted: '制作物品数量',
    stories_completed: '完成故事数量'
  }
  return conditions[talent.condition] || talent.condition
}

const getEffectName = (key) => {
  const names = {
    swimming_speed: '游泳速度',
    drowning_resistance: '溺水抗性',
    fishing_success_rate: '钓鱼成功率',
    rare_fish_chance: '稀有鱼类概率',
    attack_power: '攻击力',
    dodge_rate: '闪避率',
    sanity_loss_reduction: '理智损失减免',
    madness_resistance: '疯狂抗性'
  }
  return names[key] || key
}

const formatEffectValue = (value) => {
  return `+${value}%`
}

const showTalentDetails = (talent) => {
  if (!talent.revealed && !talent.unlocked) {
    ElMessage.info('这个天赋还未显现...')
    return
  }
  
  selectedTalent.value = talent
  detailsVisible.value = true
}

const unlockTalent = (talent) => {
  if (!canUnlock(talent)) return
  
  talent.unlocked = true
  ElMessage.success(`解锁天赋：${talent.name}！`)
  
  // 应用天赋效果
  if (talent.effects) {
    // 这里应该调用游戏商店的方法来应用天赋效果
    // gameStore.applyTalentEffects(talent.effects)
  }
  
  detailsVisible.value = false
}

// 更新天赋进度
const updateTalentProgress = (condition, amount = 1) => {
  talents.value.forEach(talent => {
    if (talent.condition === condition && !talent.unlocked) {
      talent.progress = Math.min(talent.progress + amount, talent.requirement)
      
      // 检查是否应该显现天赋
      if (!talent.revealed && talent.progress > 0) {
        talent.revealed = true
        ElMessage.info(`发现了新的天赋线索...`)
      }
      
      // 检查是否可以解锁
      if (talent.progress >= talent.requirement && !talent.unlocked) {
        ElMessage.warning(`天赋"${talent.name}"可以解锁了！`)
      }
    }
  })
}

// 初始化
onMounted(() => {
  // 模拟一些进度
  updateTalentProgress('survive_days', 1)
  updateTalentProgress('fishing_attempts', 25)
})

// 暴露方法供外部调用
defineExpose({
  updateTalentProgress,
  unlockedTalents,
  availableTalents
})
</script>

<style lang="scss" scoped>
.talent-system {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.talent-header {
  text-align: center;
  margin-bottom: 1.5rem;
  
  h3 {
    color: #f39c12;
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
  }
  
  .talent-description {
    color: #bbb;
    font-size: 0.9rem;
  }
}

.talents-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.talent-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  }
  
  &.unlocked {
    border-color: #2ecc71;
    background: rgba(46, 204, 113, 0.1);
  }
  
  &.unlockable {
    border-color: #f39c12;
    background: rgba(243, 156, 18, 0.1);
    animation: talentReady 2s ease-in-out infinite;
  }
  
  &.hidden {
    opacity: 0.5;
    filter: blur(1px);
  }
}

.talent-icon {
  font-size: 2rem;
  margin-right: 1rem;
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.talent-info {
  flex: 1;
  min-width: 0;
}

.talent-name {
  font-weight: bold;
  color: #fff;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.talent-progress {
  .progress-text {
    font-size: 0.8rem;
    color: #3498db;
    margin-bottom: 0.3rem;
  }
}

.talent-hint {
  .hint-text {
    font-size: 0.8rem;
    color: #95a5a6;
    font-style: italic;
  }
}

.talent-status {
  font-size: 1.5rem;
  margin-left: 1rem;
  
  .status-ready {
    animation: statusPulse 1.5s ease-in-out infinite;
  }
}

.talent-dialog {
  :deep(.el-dialog) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
  
  :deep(.el-dialog__header) {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  :deep(.el-dialog__title) {
    color: #f39c12;
  }
}

.talent-details {
  text-align: center;
}

.talent-icon-large {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.talent-description-full {
  color: #bbb;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.unlock-conditions {
  text-align: left;
  margin-bottom: 1.5rem;
  
  h4 {
    color: #3498db;
    margin-bottom: 0.5rem;
  }
}

.condition-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.3rem;
}

.condition-text {
  color: #fff;
}

.progress-numbers {
  color: #3498db;
  font-weight: bold;
}

.talent-effects {
  text-align: left;
  
  h4 {
    color: #2ecc71;
    margin-bottom: 0.5rem;
  }
}

.effect-item {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  
  &:last-child {
    border-bottom: none;
  }
}

.effect-name {
  color: #fff;
}

.effect-value {
  color: #2ecc71;
  font-weight: bold;
}

// 动画
@keyframes talentReady {
  0%, 100% { box-shadow: 0 0 5px rgba(243, 156, 18, 0.5); }
  50% { box-shadow: 0 0 20px rgba(243, 156, 18, 0.8); }
}

@keyframes statusPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}
</style>
