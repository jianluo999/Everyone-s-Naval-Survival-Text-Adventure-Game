n<template>
  <div class="comprehensive-status">
    <!-- 综合状态头部 -->
    <div class="status-header">
      <div class="player-info">
        <el-icon class="captain-icon"><User /></el-icon>
        <span class="captain-name">{{ player.name }}</span>
        <el-tag type="success" size="small">Lv.{{ player.level }}</el-tag>
      </div>
      <div class="ship-info">
        <el-icon class="ship-icon"><Ship /></el-icon>
        <span class="ship-name">{{ ship.name }}</span>
        <el-tag :type="statusTagType" size="small">{{ statusText }}</el-tag>
      </div>
    </div>

    <!-- 核心状态条 -->
    <div class="core-status">
      <div class="status-grid">
        <!-- 玩家状态 -->
        <div class="status-group player-group">
          <h4 class="group-title">船长状态</h4>
          <div class="status-bars">
            <div class="status-item">
              <span class="status-label">理智</span>
              <el-progress 
                :percentage="sanityPercent" 
                :color="sanityColor"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ player.sanity }}/{{ player.maxSanity }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">精力</span>
              <el-progress 
                :percentage="energyPercent" 
                color="#409EFF"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ player.energy }}/{{ player.maxEnergy }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">气血</span>
              <el-progress 
                :percentage="healthPercent" 
                color="#F56C6C"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ player.health }}/{{ player.maxHealth }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">饥饿</span>
              <el-progress 
                :percentage="hungerPercent" 
                color="#FF9800"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ player.hunger || 100 }}/100</span>
            </div>
            <div class="status-item">
              <span class="status-label">口渴</span>
              <el-progress 
                :percentage="thirstPercent" 
                color="#2196F3"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ player.thirst || 100 }}/100</span>
            </div>
          </div>
        </div>

        <!-- 船只状态 -->
        <div class="status-group ship-group">
          <h4 class="group-title">船只状态</h4>
          <div class="status-bars">
            <div class="status-item">
              <span class="status-label">耐久</span>
              <el-progress 
                :percentage="durabilityPercent" 
                :color="durabilityColor"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ ship.durability }}/{{ ship.maxDurability }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">燃料</span>
              <el-progress 
                :percentage="fuelPercent" 
                color="#E6A23C"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ ship.fuel }}/{{ ship.maxFuel }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">食物</span>
              <el-progress 
                :percentage="foodPercent" 
                color="#67C23A"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ ship.food }}/{{ ship.maxFood }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">淡水</span>
              <el-progress 
                :percentage="waterPercent" 
                color="#409EFF"
                :show-text="false"
                :stroke-width="6"
              />
              <span class="status-value">{{ ship.water }}/{{ ship.maxWater }}</span>
            </div>
          </div>
        </div>

        <!-- 钓鱼系统 -->
        <div class="status-group fishing-group">
          <h4 class="group-title">钓鱼系统</h4>
          <div class="fishing-controls">
                         <el-button 
               type="primary" 
               size="small"
               @click="startFishing"
               :loading="fishingState.fishing"
               :disabled="!canFish"
               class="fishing-btn"
             >
               <el-icon><Operation /></el-icon>
               {{ fishingState.fishing ? '钓鱼中...' : '开始钓鱼' }}
             </el-button>
            <div class="fishing-status">
              <span class="fishing-label">状态：</span>
              <span class="fishing-text">{{ fishingStatusText }}</span>
            </div>
          </div>
          
          <!-- 钓鱼结果 -->
          <div v-if="fishingState.lastResult" class="fishing-result">
            <div class="result-fish">
              <span class="fish-name">{{ fishingState.lastResult.fishName }}</span>
              <el-tag :type="getFishRarityType(fishingState.lastResult.rarity)" size="small">
                {{ fishingState.lastResult.rarity }}
              </el-tag>
            </div>
            <div class="result-actions">
              <el-button 
                size="small" 
                type="success" 
                @click="eatFish(fishingState.lastResult)"
                v-if="fishingState.lastResult.canEat"
              >
                食用
              </el-button>
              <el-button 
                size="small" 
                @click="discardFish"
              >
                丢弃
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部信息栏 -->
      <div class="bottom-info">
        <div class="resource-info">
          <span class="resource-item">
            <el-icon><Coin /></el-icon>
            {{ player.gold }}金币
          </span>
          <span class="resource-item">
            <el-icon><TrophyBase /></el-icon>
            {{ player.experience }}经验
          </span>
          <span class="resource-item">
            <el-icon><Timer /></el-icon>
            {{ ship.speed }}节速度
          </span>
          <span class="resource-item">
            <el-icon><Box /></el-icon>
            {{ ship.currentCargo }}/{{ ship.cargoCapacity }}载货
          </span>
        </div>
        
        <div class="attributes-info">
          <span class="attr-item">力量{{ player.strength }}</span>
          <span class="attr-item">精神{{ player.spirit }}</span>
          <span class="attr-item">敏捷{{ player.agility }}</span>
          <span class="attr-item">体质{{ player.constitution }}</span>
          <span class="attr-item">感知{{ player.perception }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'
import { User, Ship, Coin, TrophyBase, Timer, Box, Operation } from '@element-plus/icons-vue'

const gameStore = useGameStore()

// 响应式数据
const fishingState = ref({
  fishing: false,
  lastResult: null,
  status: 'ready'
})

// 计算属性
const player = computed(() => gameStore.player)
const ship = computed(() => gameStore.player?.ship)

// 玩家状态百分比
const sanityPercent = computed(() => 
  Math.round((player.value.sanity / player.value.maxSanity) * 100)
)
const energyPercent = computed(() => 
  Math.round((player.value.energy / player.value.maxEnergy) * 100)
)
const healthPercent = computed(() => 
  Math.round((player.value.health / player.value.maxHealth) * 100)
)
const hungerPercent = computed(() => 
  Math.round((player.value.hunger || 100))
)
const thirstPercent = computed(() => 
  Math.round((player.value.thirst || 100))
)

// 船只状态百分比
const durabilityPercent = computed(() => 
  Math.round((ship.value.durability / ship.value.maxDurability) * 100)
)
const fuelPercent = computed(() => 
  Math.round((ship.value.fuel / ship.value.maxFuel) * 100)
)
const foodPercent = computed(() => 
  Math.round((ship.value.food / ship.value.maxFood) * 100)
)
const waterPercent = computed(() => 
  Math.round((ship.value.water / ship.value.maxWater) * 100)
)

// 颜色计算
const sanityColor = computed(() => {
  const percent = sanityPercent.value
  if (percent > 70) return '#67C23A'
  if (percent > 50) return '#E6A23C'
  if (percent > 30) return '#F56C6C'
  return '#909399'
})

const durabilityColor = computed(() => {
  const percent = durabilityPercent.value
  if (percent > 70) return '#67C23A'
  if (percent > 40) return '#E6A23C'
  return '#F56C6C'
})

// 船只状态
const statusText = computed(() => {
  const percent = durabilityPercent.value
  if (percent > 80) return '完好'
  if (percent > 60) return '良好'
  if (percent > 40) return '一般'
  if (percent > 20) return '损坏'
  return '危险'
})

const statusTagType = computed(() => {
  const percent = durabilityPercent.value
  if (percent > 60) return 'success'
  if (percent > 30) return 'warning'
  return 'danger'
})

// 钓鱼相关
const canFish = computed(() => {
  return player.value && player.value.energy > 10 && !fishingState.value.fishing
})

const fishingStatusText = computed(() => {
  if (fishingState.value.fishing) return '钓鱼中'
  if (!canFish.value) return '精力不足'
  return '可以钓鱼'
})

// 方法
const startFishing = async () => {
  if (!canFish.value) return
  
  fishingState.value.fishing = true
  fishingState.value.status = 'fishing'
  
  try {
    // 模拟钓鱼过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 模拟钓鱼结果
    const fishResults = [
      { fishName: '长腿沙丁鱼', rarity: '奇异', canEat: true },
      { fishName: '海鲈鱼', rarity: '普通', canEat: true },
      { fishName: '囊肿刺豚', rarity: '危险', canEat: false },
      { fishName: '人头章鱼', rarity: '稀有', canEat: true }
    ]
    
    const result = fishResults[Math.floor(Math.random() * fishResults.length)]
    fishingState.value.lastResult = result
    
    ElMessage.success(`钓到了${result.fishName}！`)
    
  } catch (err) {
    ElMessage.error('钓鱼失败')
  } finally {
    fishingState.value.fishing = false
    fishingState.value.status = 'ready'
  }
}

const eatFish = (fish) => {
  ElMessage.success(`食用了${fish.fishName}，获得营养补充`)
  fishingState.value.lastResult = null
}

const discardFish = () => {
  ElMessage.info('已丢弃鱼类')
  fishingState.value.lastResult = null
}

const getFishRarityType = (rarity) => {
  const typeMap = {
    '普通': '',
    '奇异': 'warning',
    '稀有': 'primary',
    '危险': 'danger',
    '传说': 'success'
  }
  return typeMap[rarity] || ''
}
</script>

<style lang="scss" scoped>
.comprehensive-status {
  height: 100%;
  background: rgba(0, 25, 20, 0.95);
  border-radius: 15px;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
  backdrop-filter: blur(15px);
  font-family: 'Consolas', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
  box-shadow: 0 0 20px rgba(0, 80, 60, 0.3);
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(102, 255, 204, 0.2);
  
  .player-info, .ship-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    
    .captain-icon, .ship-icon {
      color: #ffffff;
    }
    
    .captain-name, .ship-name {
      font-weight: bold;
      color: #ffffff;
      text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
    }
  }
}

.core-status {
  .status-grid {
    display: flex;
    justify-content: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    
    .status-group {
      flex: 0 0 auto;
      min-width: 120px;
      max-width: 150px;
      
      .group-title {
        font-size: 0.8rem;
        margin: 0 0 0.5rem 0;
        color: #ffffff;
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
        letter-spacing: 0.5px;
      }
      
      .status-bars {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
        
        .status-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.7rem;
          
          .status-label {
            min-width: 28px;
            color: #ffffff;
            font-weight: 500;
            text-shadow: 0 0 3px rgba(255, 255, 255, 0.8);
          }
          
          .status-value {
            min-width: 45px;
            font-size: 0.65rem;
            color: #ffffff;
            text-align: right;
            font-weight: 600;
            text-shadow: 0 0 3px rgba(255, 255, 255, 0.8);
          }
          
          .el-progress {
            flex: 1;
          }
        }
      }
    }
    
    .fishing-group {
      flex: 0 0 auto;
      min-width: 140px;
      max-width: 180px;
      
      .fishing-controls {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        
        .fishing-btn {
          font-size: 0.75rem;
          padding: 0.3rem 0.6rem;
          height: auto;
        }
        
        .fishing-status {
          font-size: 0.7rem;
          
          .fishing-label {
            color: #00ff88;
            font-weight: 500;
          }
          
          .fishing-text {
            color: #00ffc8;
            font-weight: 600;
            text-shadow: 0 0 3px rgba(0, 255, 200, 0.6);
          }
        }
      }
      
      .fishing-result {
        background: rgba(5, 25, 35, 0.8);
        border-radius: 8px;
        padding: 0.5rem;
        border: 1px solid rgba(0, 255, 136, 0.3);
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.1);
        
        .result-fish {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
          font-size: 0.7rem;
          
          .fish-name {
            color: #00ffc8;
            font-weight: bold;
            text-shadow: 0 0 3px rgba(0, 255, 200, 0.8);
          }
        }
        
        .result-actions {
          display: flex;
          gap: 0.3rem;
          
          .el-button {
            font-size: 0.65rem;
            padding: 0.2rem 0.5rem;
            height: auto;
          }
        }
      }
    }
  }
}

.bottom-info {
  display: flex;
  justify-content: space-between;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(102, 255, 204, 0.2);
  font-size: 0.7rem;
  
  .resource-info {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    
    .resource-item {
      display: flex;
      align-items: center;
      gap: 0.2rem;
      color: #00ff88;
      font-weight: 500;
      text-shadow: 0 0 3px rgba(0, 255, 136, 0.5);
      
      .el-icon {
        font-size: 0.8rem;
        color: #00ffc8;
      }
    }
  }
  
  .attributes-info {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    
    .attr-item {
      color: #00ffc8;
      font-size: 0.65rem;
      font-weight: 600;
      text-shadow: 0 0 3px rgba(0, 255, 200, 0.6);
    }
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .status-grid {
    grid-template-columns: 1fr 1fr !important;
    
    .fishing-group {
      grid-column: 1 / -1;
    }
  }
}

@media (max-width: 768px) {
  .comprehensive-status {
    padding: 0.8rem;
  }
  
  .status-grid {
    grid-template-columns: 1fr !important;
    gap: 0.8rem !important;
  }
  
  .status-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .bottom-info {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style> 