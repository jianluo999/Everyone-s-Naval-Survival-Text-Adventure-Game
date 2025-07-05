<template>
  <el-card class="player-status-card">
    <template #header>
      <div class="card-header">
        <el-icon><User /></el-icon>
        <span>船长 {{ player.name }}</span>
        <el-tag type="success">Lv.{{ player.level }}</el-tag>
      </div>
    </template>

    <div class="status-content">
      <!-- 核心状态 -->
      <div class="core-stats">
        <div class="stat-row">
          <div class="stat-item">
            <span class="stat-label">理智</span>
            <el-progress 
              :percentage="sanityPercent" 
              :color="sanityColor"
              :show-text="false"
              :stroke-width="8"
            />
            <span class="stat-value">{{ player.sanity }}/{{ player.maxSanity }}</span>
          </div>
        </div>

        <div class="stat-row">
          <div class="stat-item">
            <span class="stat-label">精力</span>
            <el-progress 
              :percentage="energyPercent" 
              color="#409EFF"
              :show-text="false"
              :stroke-width="8"
            />
            <span class="stat-value">{{ player.energy }}/{{ player.maxEnergy }}</span>
          </div>
        </div>

        <div class="stat-row">
          <div class="stat-item">
            <span class="stat-label">气血</span>
            <el-progress 
              :percentage="healthPercent" 
              color="#F56C6C"
              :show-text="false"
              :stroke-width="8"
            />
            <span class="stat-value">{{ player.health }}/{{ player.maxHealth }}</span>
          </div>
        </div>

        <div class="stat-row">
          <div class="stat-item">
            <span class="stat-label">饥饿</span>
            <el-progress 
              :percentage="hungerPercent" 
              color="#FF9800"
              :show-text="false"
              :stroke-width="8"
            />
            <span class="stat-value">{{ player.hunger || 100 }}/100</span>
          </div>
        </div>

        <div class="stat-row">
          <div class="stat-item">
            <span class="stat-label">口渴</span>
            <el-progress 
              :percentage="thirstPercent" 
              color="#2196F3"
              :show-text="false"
              :stroke-width="8"
            />
            <span class="stat-value">{{ player.thirst || 100 }}/100</span>
          </div>
        </div>
      </div>

      <!-- 属性面板 -->
      <div class="attributes">
        <h4>角色属性</h4>
        <div class="attr-grid">
          <div class="attr-item">
            <el-icon><Sword /></el-icon>
            <span class="attr-name">力量</span>
            <span class="attr-value">{{ player.strength }}</span>
          </div>
          <div class="attr-item">
            <el-icon><Star /></el-icon>
            <span class="attr-name">精神</span>
            <span class="attr-value">{{ player.spirit }}</span>
          </div>
          <div class="attr-item">
            <el-icon><Lightning /></el-icon>
            <span class="attr-name">敏捷</span>
            <span class="attr-value">{{ player.agility }}</span>
          </div>
          <div class="attr-item">
            <el-icon><Shield /></el-icon>
            <span class="attr-name">体质</span>
            <span class="attr-value">{{ player.constitution }}</span>
          </div>
          <div class="attr-item">
            <el-icon><View /></el-icon>
            <span class="attr-name">感知</span>
            <span class="attr-value">{{ player.perception }}</span>
          </div>
        </div>
      </div>

      <!-- 经验和金币 -->
      <div class="resources">
        <div class="resource-item">
          <el-icon><Coin /></el-icon>
          <span>金币：{{ player.gold }}</span>
        </div>
        <div class="resource-item">
          <el-icon><TrophyBase /></el-icon>
          <span>经验：{{ player.experience }}</span>
        </div>
      </div>

      <!-- 天赋 -->
      <div class="talents" v-if="player.talents">
        <h4>天赋</h4>
        <el-tag type="warning" size="small">{{ player.talents }}</el-tag>
        <p class="talent-desc">你永不服输，理智至少会保留1点，且不会自杀</p>
      </div>

      <!-- 状态 -->
      <div class="player-status">
        <h4>当前状态</h4>
        <el-tag :type="statusType" size="large">{{ player.status }}</el-tag>
        <p class="location">位置：{{ player.currentLocation }}</p>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()
const player = computed(() => gameStore.player)

// 计算百分比
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

// 理智值颜色
const sanityColor = computed(() => {
  const percent = sanityPercent.value
  if (percent > 70) return '#67C23A'
  if (percent > 50) return '#E6A23C'
  if (percent > 30) return '#F56C6C'
  return '#909399'
})

// 状态类型
const statusType = computed(() => {
  if (player.value.health <= 0 || player.value.sanity <= 0) return 'danger'
  if (player.value.health < 50 || player.value.sanity < 50) return 'warning'
  return 'success'
})
</script>

<style lang="scss" scoped>
.player-status-card {
  height: 100%;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
  color: #333;

  .el-icon {
    font-size: 1.2rem;
    color: #409EFF;
  }
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.core-stats {
  .stat-row {
    margin-bottom: 1rem;
    
    &:last-child {
      margin-bottom: 0;
    }
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;

    .stat-label {
      min-width: 40px;
      font-weight: 500;
      color: #666;
    }

    .el-progress {
      flex: 1;
    }

    .stat-value {
      min-width: 60px;
      text-align: right;
      font-size: 0.9rem;
      color: #333;
      font-weight: 500;
    }
  }
}

.attributes {
  h4 {
    margin: 0 0 1rem 0;
    color: #333;
    font-size: 1rem;
  }

  .attr-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: 0.8rem;
  }

  .attr-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.8rem;
    background: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;

    &:hover {
      background: #e9ecef;
      transform: translateY(-2px);
    }

    .el-icon {
      font-size: 1.5rem;
      margin-bottom: 0.3rem;
      color: #409EFF;
    }

    .attr-name {
      font-size: 0.8rem;
      color: #666;
      margin-bottom: 0.2rem;
    }

    .attr-value {
      font-weight: bold;
      font-size: 1.1rem;
      color: #333;
    }
  }
}

.resources {
  display: flex;
  gap: 1rem;

  .resource-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    background: #f0f9ff;
    border-radius: 20px;
    border: 1px solid #e0f2fe;

    .el-icon {
      color: #0ea5e9;
    }

    span {
      font-weight: 500;
      color: #0c4a6e;
    }
  }
}

.talents {
  h4 {
    margin: 0 0 0.8rem 0;
    color: #333;
    font-size: 1rem;
  }

  .talent-desc {
    margin: 0.5rem 0 0 0;
    font-size: 0.8rem;
    color: #666;
    line-height: 1.4;
  }
}

.player-status {
  h4 {
    margin: 0 0 0.8rem 0;
    color: #333;
    font-size: 1rem;
  }

  .location {
    margin: 0.5rem 0 0 0;
    font-size: 0.9rem;
    color: #666;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .resources {
    flex-direction: column;
  }

  .attr-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style> 