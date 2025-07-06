<template>
  <div class="ship-capture">
    <div class="capture-header">
      <h3>🚢 船只占领</h3>
      <div class="capture-status">
        发现无主船只：{{ targetShip.name }}
      </div>
    </div>
    
    <!-- 船只信息 -->
    <div class="ship-info">
      <div class="ship-visual">
        <div class="ship-icon" :class="targetShip.type">
          {{ getShipIcon(targetShip.type) }}
        </div>
        <div class="ship-flag" v-if="targetShip.flag">
          {{ targetShip.flag }}
        </div>
      </div>
      
      <div class="ship-details">
        <h4>{{ targetShip.name }}</h4>
        <div class="ship-stats">
          <div class="stat-item">
            <span class="stat-label">等级:</span>
            <span class="stat-value">{{ targetShip.level }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">耐久:</span>
            <span class="stat-value">{{ targetShip.durability }}/{{ targetShip.maxDurability }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">容量:</span>
            <span class="stat-value">{{ targetShip.capacity }}单位</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">航速:</span>
            <span class="stat-value">{{ targetShip.speed }}节</span>
          </div>
        </div>
        
        <!-- 特殊技能 -->
        <div class="ship-abilities" v-if="targetShip.abilities.length > 0">
          <h5>船体技能：</h5>
          <div class="abilities-list">
            <div 
              v-for="ability in targetShip.abilities" 
              :key="ability.id"
              class="ability-item"
            >
              <span class="ability-icon">{{ ability.icon }}</span>
              <div class="ability-info">
                <div class="ability-name">{{ ability.name }}</div>
                <div class="ability-description">{{ ability.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 船只货物 -->
    <div class="ship-cargo">
      <h4>🎒 船只货物</h4>
      <div class="cargo-grid">
        <div 
          v-for="item in targetShip.cargo" 
          :key="item.id"
          class="cargo-item"
          :class="item.quality"
        >
          <div class="item-icon">{{ item.icon }}</div>
          <div class="item-info">
            <div class="item-name">{{ item.name }}</div>
            <div class="item-amount">x{{ item.amount }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 操作选项 -->
    <div class="capture-options">
      <div class="option-card capture-option" @click="showCaptureDetails">
        <div class="option-icon">🏴‍☠️</div>
        <div class="option-info">
          <h4>占领船只</h4>
          <p>将此船只加入你的舰队，可以切换使用</p>
          <div class="option-benefits">
            <span class="benefit">+ 获得船只及其技能</span>
            <span class="benefit">+ 保留所有货物</span>
            <span class="benefit">+ 可随时切换船只</span>
          </div>
        </div>
      </div>
      
      <div class="option-card dismantle-option" @click="showDismantleDetails">
        <div class="option-icon">🔨</div>
        <div class="option-info">
          <h4>分解船只</h4>
          <p>将船只拆解获得大量资源和图纸</p>
          <div class="option-benefits">
            <span class="benefit">+ 获得基础资源</span>
            <span class="benefit">+ 获得船只图纸</span>
            <span class="benefit">+ 立即可用于升级</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailsVisible"
      :title="dialogTitle"
      width="500px"
      class="capture-dialog"
    >
      <!-- 占领详情 -->
      <div v-if="dialogType === 'capture'" class="capture-details">
        <div class="warning-notice">
          <el-icon><Warning /></el-icon>
          <span>占领船只后，你的当前船只将被存储，可以随时切换</span>
        </div>
        
        <div class="capacity-check">
          <h4>容量检查：</h4>
          <div class="capacity-comparison">
            <div class="current-ship">
              <span class="ship-name">当前船只</span>
              <span class="capacity">{{ currentShip.usedCapacity }}/{{ currentShip.capacity }}</span>
            </div>
            <div class="arrow">→</div>
            <div class="target-ship">
              <span class="ship-name">目标船只</span>
              <span class="capacity">{{ targetShip.usedCapacity }}/{{ targetShip.capacity }}</span>
            </div>
          </div>
          
          <div v-if="capacityOverflow > 0" class="overflow-warning">
            <el-icon><Warning /></el-icon>
            <span>超出容量 {{ capacityOverflow }} 单位，部分物品将被丢弃</span>
          </div>
        </div>
      </div>
      
      <!-- 分解详情 -->
      <div v-else-if="dialogType === 'dismantle'" class="dismantle-details">
        <div class="dismantle-preview">
          <h4>分解预览：</h4>
          <div class="rewards-list">
            <div 
              v-for="reward in dismantleRewards" 
              :key="reward.id"
              class="reward-item"
            >
              <span class="reward-icon">{{ reward.icon }}</span>
              <span class="reward-name">{{ reward.name }}</span>
              <span class="reward-amount">+{{ reward.amount }}</span>
            </div>
          </div>
        </div>
        
        <div class="blueprint-info">
          <h4>📜 获得图纸：</h4>
          <div class="blueprint-item">
            <span class="blueprint-icon">📋</span>
            <div class="blueprint-details">
              <div class="blueprint-name">{{ targetShip.name }}图纸</div>
              <div class="blueprint-description">
                可用于改造你的船只，每艘船只只能改造一次
              </div>
            </div>
          </div>
        </div>
        
        <div class="capacity-warning" v-if="totalRewards > currentShip.remainingCapacity">
          <el-icon><Warning /></el-icon>
          <span>
            获得的资源超出船只容量，建议先清理背包或升级船只
          </span>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailsVisible = false">取消</el-button>
        <el-button 
          v-if="dialogType === 'capture'"
          type="primary" 
          @click="confirmCapture"
          :disabled="!canCapture"
        >
          确认占领
        </el-button>
        <el-button 
          v-else-if="dialogType === 'dismantle'"
          type="warning" 
          @click="confirmDismantle"
          :disabled="!canDismantle"
        >
          确认分解
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'

const gameStore = useGameStore()

// Props
const props = defineProps({
  targetShip: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['capture-complete', 'dismantle-complete', 'cancel'])

// 响应式数据
const detailsVisible = ref(false)
const dialogType = ref('') // 'capture' or 'dismantle'

// 模拟当前船只数据
const currentShip = ref({
  name: '梦魇号',
  capacity: 400,
  usedCapacity: 125,
  remainingCapacity: 275
})

// 计算属性
const dialogTitle = computed(() => {
  return dialogType.value === 'capture' ? '占领船只' : '分解船只'
})

const capacityOverflow = computed(() => {
  if (dialogType.value !== 'capture') return 0
  const totalItems = currentShip.value.usedCapacity + props.targetShip.usedCapacity
  return Math.max(0, totalItems - props.targetShip.capacity)
})

const dismantleRewards = computed(() => {
  const ship = props.targetShip
  return [
    {
      id: 'wood',
      name: '木料',
      icon: '🪵',
      amount: Math.floor(ship.level * 100 + ship.capacity * 0.2)
    },
    {
      id: 'cloth',
      name: '布料',
      icon: '🧵',
      amount: Math.floor(ship.level * 50 + ship.capacity * 0.1)
    },
    {
      id: 'iron',
      name: '钢铁',
      icon: '⚙️',
      amount: Math.floor(ship.level * 25)
    },
    {
      id: 'gold',
      name: '海螺币',
      icon: '🪙',
      amount: Math.floor(ship.level * 200 + ship.speed * 10)
    }
  ]
})

const totalRewards = computed(() => {
  return dismantleRewards.value.reduce((total, reward) => {
    if (['wood', 'cloth', 'iron'].includes(reward.id)) {
      return total + reward.amount
    }
    return total
  }, 0)
})

const canCapture = computed(() => {
  return capacityOverflow.value === 0 || capacityOverflow.value <= 50 // 允许少量溢出
})

const canDismantle = computed(() => {
  return totalRewards.value <= currentShip.value.remainingCapacity + 100 // 允许少量超出
})

// 方法
const getShipIcon = (type) => {
  const icons = {
    pirate: '🏴‍☠️',
    merchant: '🚢',
    warship: '⚓',
    ghost: '👻',
    special: '✨'
  }
  return icons[type] || '🚢'
}

const showCaptureDetails = () => {
  dialogType.value = 'capture'
  detailsVisible.value = true
}

const showDismantleDetails = () => {
  dialogType.value = 'dismantle'
  detailsVisible.value = true
}

const confirmCapture = async () => {
  try {
    if (capacityOverflow.value > 0) {
      await ElMessageBox.confirm(
        `占领后将丢失 ${capacityOverflow.value} 单位物品，确定继续吗？`,
        '容量不足警告',
        {
          confirmButtonText: '确定占领',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
    }
    
    // 执行占领逻辑
    ElMessage.success(`成功占领了${props.targetShip.name}！`)
    
    // 这里应该调用游戏商店的方法
    // gameStore.captureShip(props.targetShip)
    
    emit('capture-complete', {
      ship: props.targetShip,
      overflow: capacityOverflow.value
    })
    
    detailsVisible.value = false
    
  } catch {
    // 用户取消
  }
}

const confirmDismantle = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要分解${props.targetShip.name}吗？此操作不可逆转。`,
      '确认分解',
      {
        confirmButtonText: '确定分解',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 执行分解逻辑
    ElMessage.success(`成功分解了${props.targetShip.name}！`)
    
    // 这里应该调用游戏商店的方法
    // gameStore.dismantleShip(props.targetShip, dismantleRewards.value)
    
    emit('dismantle-complete', {
      ship: props.targetShip,
      rewards: dismantleRewards.value
    })
    
    detailsVisible.value = false
    
  } catch {
    // 用户取消
  }
}
</script>

<style lang="scss" scoped>
.ship-capture {
  background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(52, 152, 219, 0.3);
}

.capture-header {
  text-align: center;
  margin-bottom: 1.5rem;
  
  h3 {
    color: #3498db;
    margin: 0 0 0.5rem 0;
  }
  
  .capture-status {
    color: #bbb;
    font-size: 0.9rem;
  }
}

.ship-info {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
}

.ship-visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.ship-icon {
  font-size: 4rem;
  
  &.pirate { filter: hue-rotate(0deg); }
  &.merchant { filter: hue-rotate(120deg); }
  &.warship { filter: hue-rotate(240deg); }
  &.ghost { filter: grayscale(100%); }
}

.ship-flag {
  font-size: 1.5rem;
}

.ship-details {
  flex: 1;
  
  h4 {
    color: #3498db;
    margin: 0 0 1rem 0;
  }
}

.ship-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.3rem;
}

.stat-label {
  color: #bbb;
}

.stat-value {
  color: #fff;
  font-weight: bold;
}

.ship-abilities {
  h5 {
    color: #f39c12;
    margin: 0 0 0.5rem 0;
  }
}

.abilities-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.ability-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem;
  background: rgba(243, 156, 18, 0.1);
  border-radius: 0.3rem;
}

.ability-icon {
  font-size: 1.2rem;
}

.ability-name {
  font-weight: bold;
  color: #f39c12;
  font-size: 0.8rem;
}

.ability-description {
  color: #bbb;
  font-size: 0.7rem;
}

.ship-cargo {
  margin-bottom: 1.5rem;
  
  h4 {
    color: #e67e22;
    margin-bottom: 0.5rem;
  }
}

.cargo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
}

.cargo-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.5rem;
  border-radius: 0.3rem;
  border-left: 3px solid;
  
  &.common { 
    background: rgba(149, 165, 166, 0.1);
    border-left-color: #95a5a6;
  }
  &.good { 
    background: rgba(52, 152, 219, 0.1);
    border-left-color: #3498db;
  }
  &.excellent { 
    background: rgba(155, 89, 182, 0.1);
    border-left-color: #9b59b6;
  }
}

.item-icon {
  font-size: 1.2rem;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 0.8rem;
  color: #fff;
  font-weight: bold;
}

.item-amount {
  font-size: 0.7rem;
  color: #bbb;
}

.capture-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.option-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  }
}

.capture-option {
  background: rgba(46, 204, 113, 0.1);
  border-color: rgba(46, 204, 113, 0.3);
  
  &:hover {
    background: rgba(46, 204, 113, 0.2);
    border-color: rgba(46, 204, 113, 0.5);
  }
}

.dismantle-option {
  background: rgba(230, 126, 34, 0.1);
  border-color: rgba(230, 126, 34, 0.3);
  
  &:hover {
    background: rgba(230, 126, 34, 0.2);
    border-color: rgba(230, 126, 34, 0.5);
  }
}

.option-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.option-info {
  flex: 1;
  
  h4 {
    margin: 0 0 0.5rem 0;
    color: #fff;
  }
  
  p {
    margin: 0 0 0.5rem 0;
    color: #bbb;
    font-size: 0.9rem;
  }
}

.option-benefits {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.benefit {
  font-size: 0.8rem;
  color: #2ecc71;
}

.capture-dialog {
  :deep(.el-dialog) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid rgba(52, 152, 219, 0.3);
  }
  
  :deep(.el-dialog__title) {
    color: #3498db;
  }
}

.warning-notice {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem;
  background: rgba(243, 156, 18, 0.1);
  border: 1px solid rgba(243, 156, 18, 0.3);
  border-radius: 0.3rem;
  margin-bottom: 1rem;
  color: #f39c12;
  font-size: 0.9rem;
}

.capacity-check {
  h4 {
    color: #3498db;
    margin-bottom: 0.5rem;
  }
}

.capacity-comparison {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.current-ship,
.target-ship {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.3rem;
  flex: 1;
}

.ship-name {
  font-size: 0.8rem;
  color: #bbb;
}

.capacity {
  font-weight: bold;
  color: #fff;
}

.arrow {
  font-size: 1.5rem;
  color: #3498db;
}

.overflow-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e74c3c;
  font-size: 0.9rem;
}

.dismantle-preview {
  margin-bottom: 1rem;
  
  h4 {
    color: #e67e22;
    margin-bottom: 0.5rem;
  }
}

.rewards-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.reward-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem;
  background: rgba(46, 204, 113, 0.1);
  border-radius: 0.3rem;
}

.reward-icon {
  font-size: 1.2rem;
}

.reward-name {
  flex: 1;
  color: #fff;
}

.reward-amount {
  color: #2ecc71;
  font-weight: bold;
}

.blueprint-info {
  margin-bottom: 1rem;
  
  h4 {
    color: #9b59b6;
    margin-bottom: 0.5rem;
  }
}

.blueprint-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem;
  background: rgba(155, 89, 182, 0.1);
  border: 1px solid rgba(155, 89, 182, 0.3);
  border-radius: 0.3rem;
}

.blueprint-icon {
  font-size: 1.5rem;
}

.blueprint-name {
  font-weight: bold;
  color: #9b59b6;
}

.blueprint-description {
  font-size: 0.8rem;
  color: #bbb;
}

.capacity-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e74c3c;
  font-size: 0.9rem;
}
</style>
