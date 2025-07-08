<template>
  <div class="fishing-spot-selector" v-if="visible">
    <div class="modal-overlay" @click="$emit('close')">
      <div class="ship-view-container" @click.stop>
        <div class="ship-header">
          <h3>🚢 选择钓鱼位置</h3>
          <button class="close-btn" @click="$emit('close')">✕</button>
        </div>
        
        <div class="ship-view">
          <!-- 船只俯视图 -->
          <div class="ship-body">
            <!-- 船头钓点 -->
            <div 
              class="fishing-spot bow-spot"
              :class="{ active: selectedSpot === 'bow', disabled: !canFishAtSpot('bow') }"
              @click="selectSpot('bow')"
            >
              <div class="spot-icon">🎣</div>
              <div class="spot-label">船头</div>
              <div class="spot-info">
                <div class="fish-types">🐟 常见鱼类</div>
                <div class="success-rate">成功率: 70%</div>
              </div>
            </div>
            
            <!-- 左舷钓点 -->
            <div 
              class="fishing-spot port-spot"
              :class="{ active: selectedSpot === 'port', disabled: !canFishAtSpot('port') }"
              @click="selectSpot('port')"
            >
              <div class="spot-icon">🎣</div>
              <div class="spot-label">左舷</div>
              <div class="spot-info">
                <div class="fish-types">🦈 深海鱼类</div>
                <div class="success-rate">成功率: 50%</div>
              </div>
            </div>
            
            <!-- 右舷钓点 -->
            <div 
              class="fishing-spot starboard-spot"
              :class="{ active: selectedSpot === 'starboard', disabled: !canFishAtSpot('starboard') }"
              @click="selectSpot('starboard')"
            >
              <div class="spot-icon">🎣</div>
              <div class="spot-label">右舷</div>
              <div class="spot-info">
                <div class="fish-types">🐠 热带鱼类</div>
                <div class="success-rate">成功率: 60%</div>
              </div>
            </div>
            
            <!-- 船尾钓点 -->
            <div 
              class="fishing-spot stern-spot"
              :class="{ active: selectedSpot === 'stern', disabled: !canFishAtSpot('stern') }"
              @click="selectSpot('stern')"
            >
              <div class="spot-icon">🎣</div>
              <div class="spot-label">船尾</div>
              <div class="spot-info">
                <div class="fish-types">🦑 奇异生物</div>
                <div class="success-rate">成功率: 30%</div>
              </div>
            </div>
            
            <!-- 特殊钓点（船长室附近） -->
            <div 
              class="fishing-spot captain-spot"
              :class="{ active: selectedSpot === 'captain', disabled: !canFishAtSpot('captain') }"
              @click="selectSpot('captain')"
              v-if="hasSpecialSpot"
            >
              <div class="spot-icon">⭐</div>
              <div class="spot-label">船长专用</div>
              <div class="spot-info">
                <div class="fish-types">👑 传说鱼类</div>
                <div class="success-rate">成功率: 10%</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="spot-details" v-if="selectedSpot">
          <h4>{{ getSpotName(selectedSpot) }} 详情</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">鱼类类型:</span>
              <span class="value">{{ getSpotFishTypes(selectedSpot) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">成功率:</span>
              <span class="value">{{ getSpotSuccessRate(selectedSpot) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">特殊效果:</span>
              <span class="value">{{ getSpotSpecialEffect(selectedSpot) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">推荐技能:</span>
              <span class="value">{{ getSpotRecommendedSkill(selectedSpot) }}</span>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <button 
            class="confirm-btn"
            :disabled="!selectedSpot"
            @click="confirmSpot"
          >
            开始钓鱼
          </button>
          <button class="cancel-btn" @click="$emit('close')">
            取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  playerLevel: {
    type: Number,
    default: 1
  },
  shipType: {
    type: String,
    default: 'BASIC'
  }
})

const emit = defineEmits(['close', 'spot-selected'])

const selectedSpot = ref('')

// 是否有特殊钓点（根据船只类型和玩家等级）
const hasSpecialSpot = computed(() => {
  return props.playerLevel >= 10 || props.shipType !== 'BASIC'
})

// 检查是否可以在某个钓点钓鱼
const canFishAtSpot = (spot) => {
  switch (spot) {
    case 'bow':
    case 'port':
    case 'starboard':
      return true
    case 'stern':
      return props.playerLevel >= 5
    case 'captain':
      return props.playerLevel >= 10 && props.shipType !== 'BASIC'
    default:
      return false
  }
}

// 选择钓点
const selectSpot = (spot) => {
  if (!canFishAtSpot(spot)) return
  selectedSpot.value = spot
}

// 确认钓点选择
const confirmSpot = () => {
  if (selectedSpot.value) {
    emit('spot-selected', selectedSpot.value)
  }
}

// 获取钓点信息的辅助函数
const getSpotName = (spot) => {
  const names = {
    bow: '船头',
    port: '左舷',
    starboard: '右舷',
    stern: '船尾',
    captain: '船长专用钓点'
  }
  return names[spot] || '未知'
}

const getSpotFishTypes = (spot) => {
  const types = {
    bow: '常见海鱼、小型鱼类',
    port: '深海鱼类、中型鱼类',
    starboard: '热带鱼类、彩色鱼类',
    stern: '奇异生物、稀有鱼类',
    captain: '传说鱼类、神秘生物'
  }
  return types[spot] || '未知'
}

const getSpotSuccessRate = (spot) => {
  const rates = {
    bow: '70%',
    port: '50%',
    starboard: '60%',
    stern: '30%',
    captain: '10%'
  }
  return rates[spot] || '未知'
}

const getSpotSpecialEffect = (spot) => {
  const effects = {
    bow: '钓鱼时间较短',
    port: '可能钓到大型鱼类',
    starboard: '鱼类品质较好',
    stern: '可能触发特殊事件',
    captain: '极低概率钓到传说鱼类'
  }
  return effects[spot] || '无'
}

const getSpotRecommendedSkill = (spot) => {
  const skills = {
    bow: '感知 ≥ 3',
    port: '力量 ≥ 5',
    starboard: '敏捷 ≥ 4',
    stern: '理智 ≥ 30',
    captain: '等级 ≥ 10'
  }
  return skills[spot] || '无要求'
}
</script>

<style scoped>
.fishing-spot-selector {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2000;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.ship-view-container {
  background: linear-gradient(135deg, #1a4b5c 0%, #2d5a6b 100%);
  border: 3px solid #4a9eff;
  border-radius: 15px;
  padding: 20px;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.ship-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  color: white;
}

.ship-header h3 {
  margin: 0;
  font-size: 1.5em;
}

.close-btn {
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  font-size: 16px;
}

.ship-view {
  position: relative;
  width: 100%;
  height: 400px;
  background: url('/src/assets/images/ship-top-view.png') no-repeat center center;
  background-size: contain;
  margin: 20px 0;
}

.ship-body {
  position: relative;
  width: 300px;
  height: 400px;
  margin: 0 auto;
  background: linear-gradient(180deg, #8B4513 0%, #A0522D 50%, #8B4513 100%);
  border-radius: 50px 50px 20px 20px;
  border: 3px solid #654321;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
}

.fishing-spot {
  position: absolute;
  width: 80px;
  height: 80px;
  background: rgba(74, 158, 255, 0.2);
  border: 2px solid #4a9eff;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  font-size: 12px;
}

.fishing-spot:hover:not(.disabled) {
  background: rgba(74, 158, 255, 0.4);
  transform: scale(1.1);
}

.fishing-spot.active {
  background: rgba(255, 215, 0, 0.3);
  border-color: #ffd700;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
}

.fishing-spot.disabled {
  background: rgba(128, 128, 128, 0.2);
  border-color: #808080;
  cursor: not-allowed;
  opacity: 0.5;
}

.bow-spot {
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
}

.port-spot {
  top: 50%;
  left: -40px;
  transform: translateY(-50%);
}

.starboard-spot {
  top: 50%;
  right: -40px;
  transform: translateY(-50%);
}

.stern-spot {
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
}

.captain-spot {
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 215, 0, 0.2);
  border-color: #ffd700;
}

.spot-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.spot-label {
  font-size: 10px;
  font-weight: bold;
  text-align: center;
}

.spot-info {
  display: none;
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.9);
  padding: 8px;
  border-radius: 5px;
  white-space: nowrap;
  font-size: 10px;
  z-index: 10;
}

.fishing-spot:hover .spot-info {
  display: block;
}

.spot-details {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 15px;
  margin: 20px 0;
  color: white;
}

.spot-details h4 {
  margin: 0 0 15px 0;
  color: #ffd700;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
}

.detail-item .label {
  font-weight: bold;
  color: #4a9eff;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
}

.confirm-btn, .cancel-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-btn {
  background: linear-gradient(135deg, #4a9eff, #0066cc);
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #0066cc, #004499);
  transform: translateY(-2px);
}

.confirm-btn:disabled {
  background: #666;
  cursor: not-allowed;
}

.cancel-btn {
  background: linear-gradient(135deg, #ff4757, #cc3644);
  color: white;
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #cc3644, #992733);
  transform: translateY(-2px);
}
</style>
