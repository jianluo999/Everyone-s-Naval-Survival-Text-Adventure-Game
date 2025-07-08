<template>
  <div class="fishing-panel">
    <div class="panel-header">
      <h3>🎣 钓鱼系统</h3>
      <div class="fishing-status">
        <span class="status-label">状态:</span>
        <span :class="['status-value', statusClass]">{{ statusText }}</span>
      </div>
    </div>

    <div class="fishing-controls">
      <button
        class="fishing-btn"
        :disabled="!canFish || loading || showSpotSelector || showFishingProgress"
        @click="showSpotSelection"
      >
        <span v-if="loading || showFishingProgress">🔄 钓鱼中...</span>
        <span v-else-if="!canFish">❌ 无法钓鱼</span>
        <span v-else>🎣 选择钓点</span>
      </button>
      
      <div class="fishing-requirements" v-if="!canFish">
        <p>钓鱼需要：</p>
        <ul>
          <li>精力 ≥ 10 (当前: {{ player?.energy || 0 }})</li>
          <li>理智 ≥ 20 (当前: {{ player?.sanity || 0 }})</li>
        </ul>
      </div>
    </div>

    <!-- 钓鱼结果 -->
    <div class="fishing-result" v-if="fishingResult">
      <div class="result-header">
        <h4>🎯 钓鱼结果</h4>
      </div>
      
      <div class="result-content">
        <div class="message">{{ fishingResult.message }}</div>
        
        <div class="experience" v-if="fishingResult.experienceGained">
          <span class="exp-label">经验值:</span>
          <span class="exp-value">+{{ fishingResult.experienceGained }}</span>
        </div>

        <div class="level-up" v-if="fishingResult.levelUp">
          🎉 恭喜升级！现在是 {{ fishingResult.newLevel }} 级！
        </div>

        <!-- 这里不再直接显示鱼，而是通过弹窗 -->
      </div>
    </div>

    <!-- 生存状态 -->
    <div class="survival-status">
      <div class="status-bar">
        <div class="status-item">
          <span class="status-label">🍖 饥饿:</span>
          <div class="progress-bar">
            <div 
              class="progress-fill hunger"
              :style="{ width: `${hungerPercent}%` }"
            ></div>
            <span class="progress-text">{{ player?.hunger || 100 }}/100</span>
          </div>
        </div>
        
        <div class="status-item">
          <span class="status-label">💧 口渴:</span>
          <div class="progress-bar">
            <div 
              class="progress-fill thirst"
              :style="{ width: `${thirstPercent}%` }"
            ></div>
            <span class="progress-text">{{ player?.thirst || 100 }}/100</span>
          </div>
        </div>
      </div>
    </div>
    <!-- 钓点选择器 -->
    <FishingSpotSelector
      :visible="showSpotSelector"
      :player-level="player?.level || 1"
      :ship-type="player?.ship?.type || 'BASIC'"
      @close="closeSpotSelector"
      @spot-selected="handleSpotSelected"
    />

    <!-- 钓鱼进度 -->
    <FishingProgress
      :visible="showFishingProgress"
      :selected-spot="selectedSpot"
      :fishing-duration="fishingDuration"
      @fishing-complete="handleFishingComplete"
      @fishing-cancelled="handleFishingCancelled"
    />

    <!-- 钓鱼结果弹窗 -->
    <FishCaughtModal
      :visible="isModalVisible"
      :fish="caughtFish"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useGameStore } from '@/stores/game';
import FishCaughtModal from './FishCaughtModal.vue';
import FishingSpotSelector from './FishingSpotSelector.vue';
import FishingProgress from './FishingProgress.vue';

const gameStore = useGameStore();

// 使用 toRefs 或者分开引用以保持响应性
const player = computed(() => gameStore.player);
const loading = computed(() => gameStore.loading);
const fishingResult = computed(() => gameStore.fishingResult);
const canFish = computed(() => gameStore.canFish);
const caughtFish = computed(() => gameStore.caughtFish);

// 钓鱼流程状态
const showSpotSelector = ref(false);
const showFishingProgress = ref(false);
const selectedSpot = ref('');
const fishingDuration = ref(15);
const isModalVisible = ref(false);

// 显示钓点选择
const showSpotSelection = () => {
  if (!canFish.value || loading.value) return;
  showSpotSelector.value = true;
};

// 关闭钓点选择器
const closeSpotSelector = () => {
  showSpotSelector.value = false;
};

// 处理钓点选择
const handleSpotSelected = (spot) => {
  selectedSpot.value = spot;
  showSpotSelector.value = false;

  // 生成随机钓鱼时间（5-20秒）
  fishingDuration.value = Math.floor(Math.random() * 16) + 5;

  // 显示钓鱼进度
  showFishingProgress.value = true;
};

// 处理钓鱼完成
const handleFishingComplete = async (fishingData) => {
  showFishingProgress.value = false;

  try {
    // 调用后端钓鱼API
    const result = await gameStore.goFishingWithSpot(selectedSpot.value);

    if (result && result.success && result.fish) {
      // 显示钓鱼结果弹窗
      isModalVisible.value = true;
    }
  } catch (error) {
    console.error('钓鱼失败:', error);
  }
};

// 处理钓鱼取消
const handleFishingCancelled = () => {
  showFishingProgress.value = false;
  selectedSpot.value = '';
};

const closeModal = () => {
  isModalVisible.value = false;
  gameStore.clearCaughtFish();
};

// 监听 store 中 caughtFish 的变化
watch(() => gameStore.caughtFish, (newFish) => {
  if (newFish) {
    isModalVisible.value = true;
  }
});

const statusClass = computed(() => { // 改回 computed
  if (!canFish.value) return 'disabled';
  return gameStore.survivalStatus;
});

const statusText = computed(() => { // 改回 computed
  if (!canFish.value) return '无法钓鱼';
  switch(gameStore.survivalStatus) {
    case 'critical': return '危险';
    case 'poor': return '较差';
    case 'fair': return '一般';
    case 'good': return '良好';
    default: return '未知';
  }
});

const hungerPercent = computed(() => {
  return Math.max(0, player.value?.hunger || 0); // 注意访问 .value
});

const thirstPercent = computed(() => {
  return Math.max(0, player.value?.thirst || 0); // 注意访问 .value
});

const getRarityText = (rarity) => {
  const rarityMap = {
    'COMMON': '普通',
    'UNCOMMON': '非凡',
    'RARE': '稀有',
    'EPIC': '史诗',
    'LEGENDARY': '传说'
  };
  return rarityMap[rarity] || rarity;
};

const getFishImage = (fishName) => {
  // 根据鱼类名称返回对应图片
  const fishImages = {
    '长腿沙丁鱼': '/src/assets/images/fish/long-legged-sardine.svg',
    '囊肿刺豚': '/src/assets/images/fish/cystic-pufferfish.svg',
    '人头章鱼': '/src/assets/images/fish/human-headed-octopus.svg',
    '海鲈鱼': '/src/assets/images/fish/sea-bass.svg',
    '深海怪鱼': '/src/assets/images/fish/deep-sea-monster.svg'
  }
  return fishImages[fishName] || '/src/assets/images/fish/sea-bass.svg'
}
</script>

<style scoped>
.fishing-panel {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  border-radius: 15px;
  padding: 20px;
  color: white;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.4em;
}

.fishing-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-label {
  font-weight: bold;
}

.status-value {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.status-value.good {
  background: #4caf50;
}

.status-value.fair {
  background: #ff9800;
}

.status-value.poor {
  background: #f44336;
}

.status-value.critical {
  background: #d32f2f;
  animation: pulse 1s infinite;
}

.status-value.disabled {
  background: #666;
}

.fishing-controls {
  text-align: center;
  margin-bottom: 20px;
}

.fishing-btn {
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
  border: none;
  border-radius: 25px;
  padding: 12px 24px;
  color: white;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.fishing-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.fishing-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.fishing-requirements {
  margin-top: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.fishing-requirements ul {
  list-style: none;
  padding: 0;
  margin: 10px 0 0 0;
}

.fishing-requirements li {
  padding: 5px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.fishing-result {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
}

.result-header h4 {
  margin: 0 0 15px 0;
  color: #ffd700;
}

.message {
  font-size: 1.1em;
  margin-bottom: 15px;
}

.experience {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.exp-value {
  background: #4caf50;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.level-up {
  background: #ffd700;
  color: #333;
  padding: 10px;
  border-radius: 8px;
  font-weight: bold;
  text-align: center;
  margin: 10px 0;
}

.caught-fish {
  margin-top: 20px;
}

.fish-card {
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.fish-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.fish-header h5 {
  margin: 0;
  color: #2c3e50;
}

.fish-rarity {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: bold;
}

.fish-rarity.common {
  background: #95a5a6;
  color: white;
}

.fish-rarity.uncommon {
  background: #27ae60;
  color: white;
}

.fish-rarity.rare {
  background: #3498db;
  color: white;
}

.fish-rarity.epic {
  background: #9b59b6;
  color: white;
}

.fish-rarity.legendary {
  background: #f39c12;
  color: white;
}

.fish-image {
  text-align: center;
  margin: 15px 0;
}

.fish-image img {
  max-width: 150px;
  max-height: 150px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.fish-description {
  margin: 15px 0;
  font-style: italic;
  color: #555;
}

.fish-effects {
  margin: 15px 0;
}

.fish-effects h6 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.fish-effects ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.fish-effects li {
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}

.fish-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.eat-btn {
  background: linear-gradient(45deg, #4caf50, #66bb6a);
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.eat-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

.discard-btn {
  background: linear-gradient(45deg, #f44336, #ef5350);
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.discard-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}

.survival-status {
  margin-top: 20px;
}

.status-bar {
  display: flex;
  gap: 20px;
}

.status-item {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  flex: 1;
  height: 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
}

.progress-fill.hunger {
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
}

.progress-fill.thirst {
  background: linear-gradient(45deg, #4fc3f7, #81d4fa);
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.9em;
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

@media (max-width: 768px) {
  .status-bar {
    flex-direction: column;
    gap: 10px;
  }
  
  .fish-actions {
    flex-direction: column;
  }
}
</style> 