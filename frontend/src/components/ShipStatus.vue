<template>
  <el-card class="ship-status-card">
    <template #header>
      <div class="card-header">
        <el-icon><Ship /></el-icon>
        <span>{{ ship.name }}</span>
        <el-tag :type="statusTagType">{{ statusText }}</el-tag>
      </div>
    </template>

    <div class="ship-content">
      <!-- 船只基本信息 -->
      <div class="ship-info">
        <div class="ship-type">
          <el-icon><Flag /></el-icon>
          <span>类型：{{ ship.type }}</span>
        </div>
        <p class="ship-desc">{{ ship.description }}</p>
      </div>

      <!-- 船只状态 -->
      <div class="ship-stats">
        <h4>船只状态</h4>
        
        <div class="stat-item">
          <span class="stat-label">耐久度</span>
          <el-progress 
            :percentage="durabilityPercent" 
            :color="durabilityColor"
            :show-text="false"
            :stroke-width="8"
          />
          <span class="stat-value">{{ ship.durability }}/{{ ship.maxDurability }}</span>
        </div>

        <div class="stat-item">
          <span class="stat-label">燃料</span>
          <el-progress 
            :percentage="fuelPercent" 
            color="#E6A23C"
            :show-text="false"
            :stroke-width="8"
          />
          <span class="stat-value">{{ ship.fuel }}/{{ ship.maxFuel }}</span>
        </div>

        <div class="stat-item">
          <span class="stat-label">食物</span>
          <el-progress 
            :percentage="foodPercent" 
            color="#67C23A"
            :show-text="false"
            :stroke-width="8"
          />
          <span class="stat-value">{{ ship.food }}/{{ ship.maxFood }}</span>
        </div>

        <div class="stat-item">
          <span class="stat-label">淡水</span>
          <el-progress 
            :percentage="waterPercent" 
            color="#409EFF"
            :show-text="false"
            :stroke-width="8"
          />
          <span class="stat-value">{{ ship.water }}/{{ ship.maxWater }}</span>
        </div>
      </div>

      <!-- 船只属性 -->
      <div class="ship-attributes">
        <h4>船只属性</h4>
        <div class="attr-grid">
          <div class="attr-item">
            <el-icon><Timer /></el-icon>
            <span class="attr-name">速度</span>
            <span class="attr-value">{{ ship.speed }}节</span>
          </div>
          <div class="attr-item">
            <el-icon><Box /></el-icon>
            <span class="attr-name">载货</span>
            <span class="attr-value">{{ ship.currentCargo }}/{{ ship.cargoCapacity }}</span>
          </div>
          <div class="attr-item">
            <el-icon><Sword /></el-icon>
            <span class="attr-name">攻击</span>
            <span class="attr-value">{{ ship.attackPower }}</span>
          </div>
          <div class="attr-item">
            <el-icon><Shield /></el-icon>
            <span class="attr-name">防御</span>
            <span class="attr-value">{{ ship.defense }}</span>
          </div>
        </div>
      </div>

      <!-- 特殊装备 -->
      <div class="ship-equipment">
        <h4>特殊装备</h4>
        <div class="equipment-list">
          <el-tag 
            v-if="ship.hasGrappleHook" 
            type="success" 
            size="small"
            effect="dark"
          >
            <el-icon><Connection /></el-icon>
            爪钩（无限耐久）
          </el-tag>
          
          <!-- 如果有其他装备，可以在这里添加 -->
          <div v-if="!ship.hasGrappleHook" class="no-equipment">
            暂无特殊装备
          </div>
        </div>
      </div>

      <!-- 警告信息 -->
      <div class="warnings" v-if="warnings.length > 0">
        <h4>⚠️ 警告</h4>
        <div class="warning-list">
          <el-alert
            v-for="warning in warnings"
            :key="warning.type"
            :title="warning.message"
            :type="warning.level"
            :closable="false"
            show-icon
            size="small"
          />
        </div>
      </div>

      <!-- 升级建议 -->
      <div class="upgrade-tips">
        <h4>💡 升级建议</h4>
        <div class="tips-list">
          <p v-if="durabilityPercent < 50">
            <el-icon><Warning /></el-icon>
            船只耐久度过低，考虑修理或升级船体
          </p>
          <p v-if="ship.attackPower === 0">
            <el-icon><Sword /></el-icon>
            安装武器系统以应对海上威胁
          </p>
          <p v-if="ship.cargoCapacity < 50">
            <el-icon><Box /></el-icon>
            扩展货舱容量以装载更多物资
          </p>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()
const ship = computed(() => gameStore.player?.ship)

// 计算百分比
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

// 耐久度颜色
const durabilityColor = computed(() => {
  const percent = durabilityPercent.value
  if (percent > 70) return '#67C23A'
  if (percent > 40) return '#E6A23C'
  return '#F56C6C'
})

// 状态文本和标签类型
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

// 警告信息
const warnings = computed(() => {
  const alerts = []
  
  if (ship.value.fuel < 20) {
    alerts.push({
      type: 'fuel',
      level: 'warning',
      message: '燃料不足，请及时补充'
    })
  }
  
  if (ship.value.food < 20) {
    alerts.push({
      type: 'food',
      level: 'warning',
      message: '食物储备不足'
    })
  }
  
  if (ship.value.water < 20) {
    alerts.push({
      type: 'water',
      level: 'error',
      message: '淡水严重不足！'
    })
  }
  
  if (durabilityPercent.value < 30) {
    alerts.push({
      type: 'durability',
      level: 'error',
      message: '船只损坏严重，有沉没风险！'
    })
  }
  
  return alerts
})
</script>

<style lang="scss" scoped>
.ship-status-card {
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

.ship-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.ship-info {
  .ship-type {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
    
    .el-icon {
      color: #409EFF;
    }
    
    span {
      font-weight: 500;
      color: #333;
    }
  }
  
  .ship-desc {
    margin: 0;
    font-size: 0.9rem;
    color: #666;
    line-height: 1.5;
    font-style: italic;
  }
}

.ship-stats {
  h4 {
    margin: 0 0 1rem 0;
    color: #333;
    font-size: 1rem;
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1rem;

    &:last-child {
      margin-bottom: 0;
    }

    .stat-label {
      min-width: 50px;
      font-weight: 500;
      color: #666;
      font-size: 0.9rem;
    }

    .el-progress {
      flex: 1;
    }

    .stat-value {
      min-width: 60px;
      text-align: right;
      font-size: 0.8rem;
      color: #333;
      font-weight: 500;
    }
  }
}

.ship-attributes {
  h4 {
    margin: 0 0 1rem 0;
    color: #333;
    font-size: 1rem;
  }

  .attr-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
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
      font-size: 1.3rem;
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
      font-size: 1rem;
      color: #333;
    }
  }
}

.ship-equipment {
  h4 {
    margin: 0 0 1rem 0;
    color: #333;
    font-size: 1rem;
  }

  .equipment-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;

    .el-tag {
      display: flex;
      align-items: center;
      gap: 0.3rem;
    }

    .no-equipment {
      color: #999;
      font-style: italic;
      font-size: 0.9rem;
    }
  }
}

.warnings {
  h4 {
    margin: 0 0 1rem 0;
    color: #f56c6c;
    font-size: 1rem;
  }

  .warning-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
}

.upgrade-tips {
  h4 {
    margin: 0 0 1rem 0;
    color: #333;
    font-size: 1rem;
  }

  .tips-list {
    p {
      margin: 0.5rem 0;
      font-size: 0.9rem;
      color: #666;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      line-height: 1.4;

      .el-icon {
        color: #e6a23c;
        flex-shrink: 0;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .attr-grid {
    grid-template-columns: 1fr;
  }
}
</style> 