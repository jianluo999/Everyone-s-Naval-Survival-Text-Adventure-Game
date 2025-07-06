<template>
  <div class="gachapon-container">
    <!-- 扭蛋机外观 -->
    <div class="gachapon-machine" :class="{ 'active': isOperating }">
      <div class="machine-body">
        <!-- 扭蛋机头部 - 根据类型显示不同造型 -->
        <div class="machine-head" :class="machineType">
          <div class="machine-eyes" :class="{ 'glowing': isOperating }"></div>
          <div class="machine-mouth">
            <div class="mouth-opening" :class="{ 'eating': isOperating }"></div>
            <div class="tentacles" v-if="machineType === 'octopus'">
              <div v-for="i in 6" :key="i" class="tentacle" :style="{ animationDelay: i * 0.1 + 's' }"></div>
            </div>
          </div>
        </div>
        
        <!-- 投入口 -->
        <div class="input-slot" @drop="handleDrop" @dragover.prevent @dragenter.prevent>
          <div class="slot-glow" :class="{ 'active': isDragOver }"></div>
          <span class="slot-text">投入怪物尸体</span>
        </div>
        
        <!-- 转盘 -->
        <div class="control-dial" @click="operateGachapon" :class="{ 'spinning': isOperating }">
          <div class="dial-handle"></div>
          <div class="dial-center"></div>
        </div>
        
        <!-- 出货口 -->
        <div class="output-slot">
          <div class="reward-glow" v-if="currentReward"></div>
          <div class="reward-item" v-if="currentReward" @click="collectReward">
            <div class="reward-orb" :class="currentReward.quality">
              <div class="orb-shine"></div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 机器底座 -->
      <div class="machine-base">
        <div class="base-decoration"></div>
      </div>
    </div>
    
    <!-- 操作面板 -->
    <div class="control-panel">
      <h3>🎰 怪物扭蛋机</h3>
      <div class="machine-info">
        <p>类型：{{ getMachineTypeName() }}</p>
        <p>状态：{{ getStatusText() }}</p>
      </div>
      
      <!-- 投入的材料显示 -->
      <div class="input-materials" v-if="inputMaterial">
        <h4>已投入材料：</h4>
        <div class="material-item">
          <span class="material-name">{{ inputMaterial.name }}</span>
          <span class="material-type">{{ inputMaterial.type }}</span>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button 
          type="primary" 
          :disabled="!canOperate" 
          @click="operateGachapon"
          :loading="isOperating"
        >
          {{ isOperating ? '扭蛋中...' : '开始扭蛋' }}
        </el-button>
        
        <el-button 
          v-if="currentReward" 
          type="success" 
          @click="collectReward"
        >
          收取奖励
        </el-button>
      </div>
      
      <!-- 奖励历史 -->
      <div class="reward-history" v-if="rewardHistory.length > 0">
        <h4>最近获得：</h4>
        <div class="history-list">
          <div 
            v-for="reward in rewardHistory.slice(-3)" 
            :key="reward.id"
            class="history-item"
            :class="reward.quality"
          >
            <span class="reward-name">{{ reward.name }}</span>
            <span class="reward-quality">{{ getQualityText(reward.quality) }}</span>
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
const machineType = ref('octopus') // octopus, robot, clown, cat
const isOperating = ref(false)
const isDragOver = ref(false)
const inputMaterial = ref(null)
const currentReward = ref(null)
const rewardHistory = ref([])

// 计算属性
const canOperate = computed(() => {
  return inputMaterial.value && !isOperating.value && !currentReward.value
})

// 方法
const getMachineTypeName = () => {
  const types = {
    octopus: '章鱼怪人',
    robot: '机械战士',
    clown: '诡异小丑',
    cat: '大脸猫咪'
  }
  return types[machineType.value] || '未知类型'
}

const getStatusText = () => {
  if (isOperating.value) return '运转中'
  if (currentReward.value) return '有奖励待收取'
  if (inputMaterial.value) return '准备就绪'
  return '等待投料'
}

const getQualityText = (quality) => {
  const qualities = {
    common: '普通',
    good: '良品',
    excellent: '精品',
    epic: '史诗',
    legendary: '传说'
  }
  return qualities[quality] || quality
}

// 拖拽处理
const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  
  // 这里应该处理拖拽的怪物材料
  // 暂时模拟一个材料
  inputMaterial.value = {
    id: 'monster_part_001',
    name: '溺亡者断手',
    type: '怪物肢体',
    quality: 'common'
  }
  
  ElMessage.success('材料投入成功！')
}

// 扭蛋操作
const operateGachapon = async () => {
  if (!canOperate.value) return
  
  isOperating.value = true
  
  try {
    // 模拟扭蛋过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 生成随机奖励
    const reward = generateRandomReward()
    currentReward.value = reward
    
    // 清空投入材料
    inputMaterial.value = null
    
    ElMessage.success(`获得了${reward.name}！`)
    
  } catch (error) {
    ElMessage.error('扭蛋失败：' + error.message)
  } finally {
    isOperating.value = false
  }
}

// 收取奖励
const collectReward = () => {
  if (!currentReward.value) return
  
  // 添加到历史记录
  rewardHistory.value.push({
    ...currentReward.value,
    timestamp: new Date()
  })
  
  // 添加到玩家背包（这里需要调用游戏商店的方法）
  // gameStore.addItem(currentReward.value)
  
  ElMessage.success(`收取了${currentReward.value.name}`)
  currentReward.value = null
}

// 生成随机奖励
const generateRandomReward = () => {
  const rewards = [
    {
      id: 'potion_001',
      name: '溺亡者之怨',
      type: 'consumable',
      quality: 'good',
      description: '服下后，理智-20，一分钟内将被视作溺亡者，不会受到低等异魔的主动攻击。'
    },
    {
      id: 'token_001',
      name: '白骨令牌',
      type: 'relic',
      quality: 'excellent',
      description: '可以召唤一只骷髅，操控它为你而战，持续15分钟。冷却时间24小时。'
    },
    {
      id: 'weapon_001',
      name: '锯齿匕首',
      type: 'weapon',
      quality: 'excellent',
      description: '一把锋利的匕首，手感舒适，可造成微量伤害。它唯一的缺点，就是短！'
    }
  ]
  
  // 根据品质权重随机选择
  const qualityWeights = {
    common: 50,
    good: 30,
    excellent: 15,
    epic: 4,
    legendary: 1
  }
  
  const randomReward = rewards[Math.floor(Math.random() * rewards.length)]
  return {
    ...randomReward,
    id: Date.now().toString()
  }
}

// 初始化
onMounted(() => {
  // 随机选择扭蛋机类型
  const types = ['octopus', 'robot', 'clown', 'cat']
  machineType.value = types[Math.floor(Math.random() * types.length)]
})
</script>

<style lang="scss" scoped>
.gachapon-container {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 1rem;
  min-height: 400px;
}

.gachapon-machine {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  
  &.active {
    .machine-head {
      animation: machineShake 0.5s ease-in-out infinite;
    }
  }
}

.machine-body {
  width: 200px;
  height: 300px;
  background: linear-gradient(145deg, #2c3e50, #34495e);
  border-radius: 20px;
  position: relative;
  box-shadow: 
    0 10px 30px rgba(0,0,0,0.3),
    inset 0 2px 10px rgba(255,255,255,0.1);
}

.machine-head {
  width: 120px;
  height: 100px;
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50% 50% 40% 40%;
  
  &.octopus {
    background: linear-gradient(145deg, #8e44ad, #9b59b6);
  }
  
  &.robot {
    background: linear-gradient(145deg, #34495e, #2c3e50);
  }
  
  &.clown {
    background: linear-gradient(145deg, #e74c3c, #c0392b);
  }
  
  &.cat {
    background: linear-gradient(145deg, #f39c12, #e67e22);
  }
}

.machine-eyes {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 20px;
  
  &::before,
  &::after {
    content: '';
    position: absolute;
    width: 12px;
    height: 12px;
    background: #fff;
    border-radius: 50%;
    top: 4px;
  }
  
  &::before { left: 10px; }
  &::after { right: 10px; }
  
  &.glowing {
    &::before,
    &::after {
      background: #ff4757;
      box-shadow: 0 0 10px #ff4757;
      animation: eyeGlow 1s ease-in-out infinite alternate;
    }
  }
}

.machine-mouth {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 20px;
}

.mouth-opening {
  width: 100%;
  height: 100%;
  background: #000;
  border-radius: 50%;
  transition: all 0.3s ease;
  
  &.eating {
    transform: scaleY(1.5);
    animation: mouthChew 0.5s ease-in-out infinite;
  }
}

.tentacles {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 20px;
}

.tentacle {
  position: absolute;
  width: 3px;
  height: 15px;
  background: linear-gradient(to bottom, #8e44ad, #9b59b6);
  border-radius: 2px;
  animation: tentacleWave 2s ease-in-out infinite;
  
  &:nth-child(1) { left: 10px; }
  &:nth-child(2) { left: 20px; }
  &:nth-child(3) { left: 30px; }
  &:nth-child(4) { left: 40px; }
  &:nth-child(5) { left: 50px; }
  &:nth-child(6) { left: 60px; }
}

.input-slot {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 30px;
  background: linear-gradient(145deg, #1a1a2e, #16213e);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px dashed #555;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #3498db;
  }
}

.slot-glow {
  position: absolute;
  inset: -2px;
  border-radius: 15px;
  background: linear-gradient(45deg, transparent, #3498db, transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  
  &.active {
    opacity: 1;
    animation: slotGlow 1s ease-in-out infinite;
  }
}

.slot-text {
  font-size: 10px;
  color: #bbb;
  text-align: center;
  line-height: 1.2;
}

.control-dial {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 60px;
  background: linear-gradient(145deg, #e74c3c, #c0392b);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateX(-50%) scale(1.1);
  }
  
  &.spinning {
    animation: dialSpin 2s linear infinite;
  }
}

.dial-handle {
  width: 20px;
  height: 4px;
  background: #fff;
  border-radius: 2px;
  position: absolute;
}

.dial-center {
  width: 10px;
  height: 10px;
  background: #fff;
  border-radius: 50%;
}

.output-slot {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 40px;
  background: linear-gradient(145deg, #1a1a2e, #16213e);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.reward-glow {
  position: absolute;
  inset: -2px;
  border-radius: 10px;
  background: linear-gradient(45deg, #f39c12, #e67e22, #f39c12);
  animation: rewardGlow 1s ease-in-out infinite;
}

.reward-item {
  cursor: pointer;
  z-index: 1;
}

.reward-orb {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.2);
  }
  
  &.common { background: linear-gradient(145deg, #95a5a6, #7f8c8d); }
  &.good { background: linear-gradient(145deg, #3498db, #2980b9); }
  &.excellent { background: linear-gradient(145deg, #9b59b6, #8e44ad); }
  &.epic { background: linear-gradient(145deg, #e67e22, #d35400); }
  &.legendary { background: linear-gradient(145deg, #f1c40f, #f39c12); }
}

.orb-shine {
  position: absolute;
  top: 5px;
  left: 8px;
  width: 8px;
  height: 8px;
  background: rgba(255,255,255,0.8);
  border-radius: 50%;
  animation: orbShine 2s ease-in-out infinite;
}

.machine-base {
  width: 220px;
  height: 40px;
  background: linear-gradient(145deg, #2c3e50, #34495e);
  border-radius: 20px;
  margin-top: 10px;
  position: relative;
}

.base-decoration {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 180px;
  height: 10px;
  background: linear-gradient(90deg, transparent, #555, transparent);
  border-radius: 5px;
}

.control-panel {
  flex: 1;
  background: rgba(255,255,255,0.05);
  border-radius: 1rem;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.1);
}

.machine-info {
  margin: 1rem 0;
  
  p {
    margin: 0.5rem 0;
    color: #bbb;
    font-size: 0.9rem;
  }
}

.input-materials {
  margin: 1rem 0;
  
  h4 {
    color: #3498db;
    margin-bottom: 0.5rem;
  }
}

.material-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: rgba(255,255,255,0.05);
  border-radius: 0.5rem;
  margin: 0.5rem 0;
}

.material-name {
  color: #fff;
  font-weight: bold;
}

.material-type {
  color: #bbb;
  font-size: 0.8rem;
}

.action-buttons {
  margin: 1.5rem 0;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.reward-history {
  margin-top: 1.5rem;
  
  h4 {
    color: #f39c12;
    margin-bottom: 0.5rem;
  }
}

.history-list {
  max-height: 150px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border-radius: 0.5rem;
  border-left: 3px solid;
  
  &.common { 
    background: rgba(149,165,166,0.1);
    border-left-color: #95a5a6;
  }
  &.good { 
    background: rgba(52,152,219,0.1);
    border-left-color: #3498db;
  }
  &.excellent { 
    background: rgba(155,89,182,0.1);
    border-left-color: #9b59b6;
  }
  &.epic { 
    background: rgba(230,126,34,0.1);
    border-left-color: #e67e22;
  }
  &.legendary { 
    background: rgba(241,196,15,0.1);
    border-left-color: #f1c40f;
  }
}

.reward-name {
  color: #fff;
  font-weight: bold;
}

.reward-quality {
  font-size: 0.8rem;
  opacity: 0.8;
}

// 动画
@keyframes machineShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  75% { transform: translateX(2px); }
}

@keyframes eyeGlow {
  0% { box-shadow: 0 0 5px #ff4757; }
  100% { box-shadow: 0 0 15px #ff4757, 0 0 25px #ff4757; }
}

@keyframes mouthChew {
  0%, 100% { transform: scaleY(1.5); }
  50% { transform: scaleY(1.2); }
}

@keyframes tentacleWave {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(10deg); }
}

@keyframes slotGlow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@keyframes dialSpin {
  from { transform: translateX(-50%) rotate(0deg); }
  to { transform: translateX(-50%) rotate(360deg); }
}

@keyframes rewardGlow {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

@keyframes orbShine {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 0.3; }
}
</style>
