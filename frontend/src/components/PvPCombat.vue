<template>
  <div class="pvp-combat">
    <div class="combat-header">
      <h3>⚔️ 玩家对战</h3>
      <div class="combat-status" :class="combatState">
        {{ getCombatStatusText() }}
      </div>
    </div>
    
    <!-- 战斗界面 -->
    <div v-if="inCombat" class="combat-interface">
      <!-- 敌方信息 -->
      <div class="enemy-info">
        <div class="enemy-header">
          <span class="enemy-name">{{ enemy.name }}</span>
          <span class="enemy-ship">{{ enemy.shipName }}</span>
        </div>
        <div class="enemy-health">
          <div class="health-bar">
            <div 
              class="health-fill" 
              :style="{ width: (enemy.health / enemy.maxHealth) * 100 + '%' }"
            ></div>
          </div>
          <span class="health-text">{{ enemy.health }}/{{ enemy.maxHealth }}</span>
        </div>
        <div class="enemy-status" v-if="enemy.statusEffects.length > 0">
          <span 
            v-for="effect in enemy.statusEffects" 
            :key="effect.id"
            class="status-effect"
            :class="effect.type"
          >
            {{ getStatusIcon(effect.type) }}
          </span>
        </div>
      </div>
      
      <!-- 战斗动作 -->
      <div class="combat-actions">
        <div class="weapon-selection">
          <h4>选择武器：</h4>
          <div class="weapons-grid">
            <div 
              v-for="weapon in availableWeapons" 
              :key="weapon.id"
              class="weapon-item"
              :class="{ 
                'selected': selectedWeapon?.id === weapon.id,
                'disabled': !canUseWeapon(weapon)
              }"
              @click="selectWeapon(weapon)"
            >
              <div class="weapon-icon">{{ weapon.icon }}</div>
              <div class="weapon-info">
                <div class="weapon-name">{{ weapon.name }}</div>
                <div class="weapon-damage">伤害: {{ weapon.damage }}</div>
                <div class="weapon-accuracy">命中: {{ weapon.accuracy }}%</div>
                <div class="weapon-cooldown" v-if="weapon.cooldown > 0">
                  冷却: {{ weapon.cooldown }}秒
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 攻击选项 -->
        <div class="attack-options">
          <el-button 
            type="danger" 
            size="large"
            :disabled="!selectedWeapon || attacking"
            @click="performAttack('normal')"
            :loading="attacking"
          >
            <span v-if="!attacking">🎯 普通攻击</span>
            <span v-else>攻击中...</span>
          </el-button>
          
          <el-button 
            type="warning" 
            size="large"
            :disabled="!selectedWeapon || !canPoisonAttack || attacking"
            @click="performAttack('poison')"
          >
            ☠️ 毒素攻击
          </el-button>
          
          <el-button 
            type="info" 
            size="large"
            :disabled="attacking"
            @click="attemptEscape"
          >
            🏃 尝试逃跑
          </el-button>
        </div>
      </div>
      
      <!-- 战斗日志 -->
      <div class="combat-log">
        <h4>战斗记录：</h4>
        <div class="log-entries">
          <div 
            v-for="entry in combatLog" 
            :key="entry.id"
            class="log-entry"
            :class="entry.type"
          >
            <span class="log-time">{{ formatTime(entry.time) }}</span>
            <span class="log-message">{{ entry.message }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 战斗结果 -->
    <div v-else-if="combatResult" class="combat-result">
      <div class="result-header" :class="combatResult.victory ? 'victory' : 'defeat'">
        <h3>{{ combatResult.victory ? '🏆 胜利！' : '💀 失败...' }}</h3>
      </div>
      
      <div class="result-details">
        <div v-if="combatResult.victory" class="victory-rewards">
          <h4>战利品：</h4>
          <div class="rewards-list">
            <div 
              v-for="reward in combatResult.rewards" 
              :key="reward.id"
              class="reward-item"
            >
              <span class="reward-icon">{{ reward.icon }}</span>
              <span class="reward-name">{{ reward.name }}</span>
              <span class="reward-amount">x{{ reward.amount }}</span>
            </div>
          </div>
          
          <div v-if="combatResult.shipCapture" class="ship-capture">
            <h4>🚢 船只占领：</h4>
            <p>你可以选择占领敌方船只或将其分解获得资源</p>
            <div class="capture-options">
              <el-button type="primary" @click="captureShip">
                占领船只
              </el-button>
              <el-button type="warning" @click="dismantleShip">
                分解船只
              </el-button>
            </div>
          </div>
        </div>
        
        <div v-else class="defeat-consequences">
          <h4>后果：</h4>
          <ul>
            <li v-for="consequence in combatResult.consequences" :key="consequence">
              {{ consequence }}
            </li>
          </ul>
        </div>
      </div>
      
      <el-button type="primary" @click="closeCombat" class="close-btn">
        继续航行
      </el-button>
    </div>
    
    <!-- 非战斗状态 -->
    <div v-else class="no-combat">
      <div class="combat-tips">
        <h4>⚔️ 战斗提示</h4>
        <ul>
          <li>遇到其他玩家时可以选择战斗或逃跑</li>
          <li>使用毒素武器可以造成持续伤害</li>
          <li>击败敌人可以获得其船只和资源</li>
          <li>理智值过低会影响战斗表现</li>
        </ul>
      </div>
      
      <div class="weapon-maintenance">
        <h4>🔧 武器维护</h4>
        <div class="weapons-status">
          <div 
            v-for="weapon in availableWeapons" 
            :key="weapon.id"
            class="weapon-status"
          >
            <span class="weapon-name">{{ weapon.name }}</span>
            <span class="weapon-condition" :class="getConditionClass(weapon.condition)">
              {{ getConditionText(weapon.condition) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage, ElMessageBox } from 'element-plus'

const gameStore = useGameStore()

// 响应式数据
const inCombat = ref(false)
const combatState = ref('idle') // idle, combat, victory, defeat
const attacking = ref(false)
const selectedWeapon = ref(null)
const combatResult = ref(null)
const combatLog = ref([])

// 敌方数据
const enemy = ref({
  name: '海盗船长',
  shipName: '黑珍珠号',
  health: 85,
  maxHealth: 100,
  statusEffects: []
})

// 可用武器
const availableWeapons = ref([
  {
    id: 'flintlock_pistol',
    name: '锈蚀燧发枪',
    icon: '🔫',
    damage: 45,
    accuracy: 70,
    cooldown: 60,
    lastUsed: 0,
    condition: 85,
    special: 'misfire_chance',
    description: '威力巨大但有哑火风险'
  },
  {
    id: 'pirate_bow',
    name: '海盗长弓',
    icon: '🏹',
    damage: 25,
    accuracy: 80,
    cooldown: 5,
    lastUsed: 0,
    condition: 90,
    special: 'poison_compatible',
    description: '可以涂抹毒素'
  },
  {
    id: 'rusty_cutlass',
    name: '生锈弯刀',
    icon: '⚔️',
    damage: 20,
    accuracy: 90,
    cooldown: 3,
    lastUsed: 0,
    condition: 60,
    special: 'melee',
    description: '近战武器，命中率高'
  }
])

// 计算属性
const canPoisonAttack = computed(() => {
  return selectedWeapon.value?.special === 'poison_compatible' && 
         gameStore.hasItem('cyst_pufferfish')
})

// 方法
const getCombatStatusText = () => {
  const texts = {
    idle: '待机中',
    combat: '战斗中',
    victory: '胜利',
    defeat: '失败'
  }
  return texts[combatState.value] || '未知状态'
}

const getStatusIcon = (type) => {
  const icons = {
    poison: '☠️',
    bleeding: '🩸',
    stunned: '😵',
    burning: '🔥',
    frozen: '🧊'
  }
  return icons[type] || '❓'
}

const canUseWeapon = (weapon) => {
  const now = Date.now()
  return (now - weapon.lastUsed) >= (weapon.cooldown * 1000)
}

const selectWeapon = (weapon) => {
  if (!canUseWeapon(weapon)) {
    ElMessage.warning('武器还在冷却中')
    return
  }
  
  selectedWeapon.value = weapon
  addCombatLog('info', `选择了${weapon.name}`)
}

const performAttack = async (attackType) => {
  if (!selectedWeapon.value) {
    ElMessage.warning('请先选择武器')
    return
  }
  
  attacking.value = true
  
  try {
    // 模拟攻击延迟
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const weapon = selectedWeapon.value
    let damage = weapon.damage
    let hitChance = weapon.accuracy
    
    // 检查命中
    const hitRoll = Math.random() * 100
    if (hitRoll > hitChance) {
      addCombatLog('miss', `${weapon.name}攻击未命中！`)
      return
    }
    
    // 特殊武器效果
    if (weapon.special === 'misfire_chance' && Math.random() < 0.3) {
      addCombatLog('misfire', `${weapon.name}哑火了！`)
      return
    }
    
    // 计算伤害
    const finalDamage = Math.floor(damage * (0.8 + Math.random() * 0.4))
    enemy.value.health = Math.max(0, enemy.value.health - finalDamage)
    
    addCombatLog('hit', `${weapon.name}造成了${finalDamage}点伤害`)
    
    // 毒素攻击
    if (attackType === 'poison' && canPoisonAttack.value) {
      enemy.value.statusEffects.push({
        id: Date.now(),
        type: 'poison',
        duration: 30
      })
      addCombatLog('poison', '敌人中毒了！')
      // gameStore.removeItem('cyst_pufferfish', 1)
    }
    
    // 更新武器冷却
    weapon.lastUsed = Date.now()
    
    // 检查敌人是否死亡
    if (enemy.value.health <= 0) {
      victory()
    } else {
      // 敌人反击
      setTimeout(enemyAttack, 1500)
    }
    
  } finally {
    attacking.value = false
  }
}

const enemyAttack = () => {
  const damage = Math.floor(15 + Math.random() * 20)
  // gameStore.takeDamage(damage)
  addCombatLog('enemy', `敌人攻击造成了${damage}点伤害`)
  
  // 检查玩家是否死亡
  if (gameStore.player?.health <= 0) {
    defeat()
  }
}

const attemptEscape = async () => {
  const escapeChance = 60 // 基础逃跑成功率
  const roll = Math.random() * 100
  
  if (roll < escapeChance) {
    addCombatLog('escape', '成功逃脱了战斗！')
    closeCombat()
  } else {
    addCombatLog('escape_fail', '逃跑失败！')
    // 敌人获得额外攻击机会
    setTimeout(enemyAttack, 1000)
  }
}

const victory = () => {
  combatState.value = 'victory'
  inCombat.value = false
  
  // 生成战利品
  const rewards = [
    { id: 'gold', name: '海螺币', icon: '🪙', amount: 400 },
    { id: 'pirate_clothes', name: '海盗服', icon: '👕', amount: 1 },
    { id: 'wood', name: '木料', icon: '🪵', amount: 50 },
    { id: 'cloth', name: '布料', icon: '🧵', amount: 30 }
  ]
  
  combatResult.value = {
    victory: true,
    rewards: rewards,
    shipCapture: true
  }
  
  addCombatLog('victory', '战斗胜利！')
}

const defeat = () => {
  combatState.value = 'defeat'
  inCombat.value = false
  
  combatResult.value = {
    victory: false,
    consequences: [
      '失去部分资源',
      '船只受损',
      '理智值下降'
    ]
  }
  
  addCombatLog('defeat', '战斗失败...')
}

const captureShip = () => {
  ElMessage.success('成功占领了敌方船只！')
  // 这里应该实现船只占领逻辑
  closeCombat()
}

const dismantleShip = () => {
  ElMessage.success('分解船只获得了大量资源和图纸！')
  // 这里应该实现船只分解逻辑
  closeCombat()
}

const closeCombat = () => {
  inCombat.value = false
  combatState.value = 'idle'
  combatResult.value = null
  combatLog.value = []
  selectedWeapon.value = null
  enemy.value.health = enemy.value.maxHealth
  enemy.value.statusEffects = []
}

const addCombatLog = (type, message) => {
  combatLog.value.push({
    id: Date.now(),
    type: type,
    message: message,
    time: new Date()
  })
  
  // 限制日志条数
  if (combatLog.value.length > 20) {
    combatLog.value = combatLog.value.slice(-20)
  }
}

const formatTime = (date) => {
  return date.toLocaleTimeString()
}

const getConditionClass = (condition) => {
  if (condition >= 80) return 'excellent'
  if (condition >= 60) return 'good'
  if (condition >= 40) return 'fair'
  return 'poor'
}

const getConditionText = (condition) => {
  if (condition >= 80) return '优秀'
  if (condition >= 60) return '良好'
  if (condition >= 40) return '一般'
  return '糟糕'
}

// 开始战斗（供外部调用）
const startCombat = (enemyData) => {
  inCombat.value = true
  combatState.value = 'combat'
  enemy.value = { ...enemy.value, ...enemyData }
  addCombatLog('start', `与${enemy.value.name}的战斗开始！`)
}

// 暴露方法
defineExpose({
  startCombat,
  inCombat
})
</script>

<style lang="scss" scoped>
.pvp-combat {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.combat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  
  h3 {
    color: #e74c3c;
    margin: 0;
  }
  
  .combat-status {
    padding: 0.3rem 0.8rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: bold;
    
    &.idle { background: rgba(149, 165, 166, 0.3); color: #95a5a6; }
    &.combat { background: rgba(231, 76, 60, 0.3); color: #e74c3c; }
    &.victory { background: rgba(46, 204, 113, 0.3); color: #2ecc71; }
    &.defeat { background: rgba(192, 57, 43, 0.3); color: #c0392b; }
  }
}

.combat-interface {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.enemy-info {
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.enemy-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.enemy-name {
  font-weight: bold;
  color: #e74c3c;
}

.enemy-ship {
  color: #bbb;
  font-size: 0.9rem;
}

.enemy-health {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.health-bar {
  flex: 1;
  height: 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.health-fill {
  height: 100%;
  background: linear-gradient(90deg, #e74c3c, #c0392b);
  transition: width 0.5s ease;
}

.health-text {
  font-size: 0.8rem;
  color: #fff;
  min-width: 60px;
}

.enemy-status {
  display: flex;
  gap: 0.3rem;
}

.status-effect {
  font-size: 1.2rem;
  
  &.poison { filter: hue-rotate(270deg); }
}

.combat-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.weapon-selection h4 {
  color: #f39c12;
  margin-bottom: 0.5rem;
}

.weapons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.weapon-item {
  display: flex;
  align-items: center;
  padding: 0.8rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover:not(.disabled) {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
  }
  
  &.selected {
    background: rgba(52, 152, 219, 0.2);
    border-color: #3498db;
  }
  
  &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.weapon-icon {
  font-size: 2rem;
  margin-right: 0.8rem;
}

.weapon-info {
  flex: 1;
}

.weapon-name {
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.2rem;
}

.weapon-damage,
.weapon-accuracy,
.weapon-cooldown {
  font-size: 0.7rem;
  color: #bbb;
  margin: 0.1rem 0;
}

.attack-options {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.combat-log {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  max-height: 200px;
  overflow-y: auto;
  
  h4 {
    color: #3498db;
    margin-bottom: 0.5rem;
  }
}

.log-entries {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.log-entry {
  display: flex;
  gap: 0.5rem;
  font-size: 0.8rem;
  
  &.hit { color: #e74c3c; }
  &.miss { color: #95a5a6; }
  &.poison { color: #8e44ad; }
  &.victory { color: #2ecc71; }
  &.defeat { color: #c0392b; }
  &.enemy { color: #e67e22; }
  &.escape { color: #3498db; }
}

.log-time {
  color: #7f8c8d;
  min-width: 60px;
}

.combat-result {
  text-align: center;
}

.result-header {
  margin-bottom: 1.5rem;
  
  &.victory h3 { color: #2ecc71; }
  &.defeat h3 { color: #e74c3c; }
}

.victory-rewards {
  text-align: left;
  margin-bottom: 1rem;
  
  h4 { color: #f39c12; }
}

.rewards-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-bottom: 1rem;
}

.reward-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem;
  background: rgba(46, 204, 113, 0.1);
  border-radius: 0.3rem;
}

.ship-capture {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(52, 152, 219, 0.1);
  border-radius: 0.5rem;
  
  h4 { color: #3498db; }
}

.capture-options {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.no-combat {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.combat-tips,
.weapon-maintenance {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
  
  h4 {
    color: #3498db;
    margin-bottom: 0.5rem;
  }
  
  ul {
    margin: 0;
    padding-left: 1.2rem;
    color: #bbb;
    
    li {
      margin: 0.3rem 0;
      font-size: 0.9rem;
    }
  }
}

.weapons-status {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.weapon-status {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.3rem;
}

.weapon-condition {
  &.excellent { color: #2ecc71; }
  &.good { color: #f39c12; }
  &.fair { color: #e67e22; }
  &.poor { color: #e74c3c; }
}

.close-btn {
  margin-top: 1rem;
}
</style>
