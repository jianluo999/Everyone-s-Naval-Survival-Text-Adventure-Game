<template>
  <div class="story-display">
    <!-- 故事头部 -->
    <div class="story-header">
      <div class="story-info">
        <h2 class="story-title">{{ currentStory?.title || '加载中...' }}</h2>
        <div class="story-meta">
          <el-tag size="small" type="info">
            第{{ currentStory?.chapter || 1 }}章
          </el-tag>
          <el-tag size="small" type="primary">
            场景{{ currentStory?.scene || 1 }}
          </el-tag>
          <el-tag size="small" :type="storyTypeTag">
            {{ storyTypeText }}
          </el-tag>
        </div>
      </div>
      
      <!-- 黑雾警告 -->
      <div class="fog-warning">
        <el-icon class="fog-icon"><Warning /></el-icon>
        <span>黑雾速度：10节</span>
      </div>
    </div>

    <!-- 故事内容 -->
    <div class="story-content">
      <div v-if="loading" class="loading-story">
        <el-skeleton :rows="5" animated />
      </div>
      
      <div v-else-if="currentStory" class="story-text">
        <!-- 故事文本 -->
        <div class="story-paragraphs">
          <p 
            v-for="(paragraph, index) in storyParagraphs" 
            :key="index"
            class="story-paragraph"
            :class="{ 'animated': showAnimation }"
            :style="{ animationDelay: `${index * 0.5}s` }"
          >
            {{ paragraph }}
          </p>
        </div>

        <!-- 结局标记 -->
        <div v-if="currentStory.isEnding" class="ending-mark">
          <el-icon class="ending-icon"><Trophy /></el-icon>
          <span>故事结局</span>
        </div>
      </div>
      
      <div v-else class="no-story">
        <el-empty description="暂无故事内容" />
      </div>
    </div>

    <!-- 选择区域 -->
    <div class="choices-section" v-if="currentStory && !currentStory.isEnding">
      <h3 class="choices-title">你的选择：</h3>
      
      <div class="choices-list">
        <div 
          v-for="(choice, index) in availableChoices" 
          :key="choice.id"
          class="choice-item"
          :class="{ 
            'disabled': !canMakeChoice(choice),
            'selected': selectedChoice === choice.id 
          }"
          @click="selectChoice(choice)"
        >
          <div class="choice-content">
            <div class="choice-text">
              {{ choice.text }}
            </div>
            
            <!-- 选择效果 -->
            <div class="choice-effects" v-if="hasEffects(choice)">
              <el-tag 
                v-if="choice.goldCost > 0" 
                type="warning" 
                size="small"
                effect="dark"
              >
                <el-icon><Coin /></el-icon>
                -{{ choice.goldCost }}
              </el-tag>
              
              <el-tag 
                v-if="choice.goldReward > 0" 
                type="success" 
                size="small"
                effect="dark"
              >
                <el-icon><Coin /></el-icon>
                +{{ choice.goldReward }}
              </el-tag>
              
              <el-tag 
                v-if="choice.healthCost > 0" 
                type="danger" 
                size="small"
                effect="dark"
              >
                <el-icon><Heart /></el-icon>
                -{{ choice.healthCost }}
              </el-tag>
              
              <el-tag 
                v-if="choice.healthReward > 0" 
                type="success" 
                size="small"
                effect="dark"
              >
                <el-icon><Heart /></el-icon>
                +{{ choice.healthReward }}
              </el-tag>
              
              <el-tag 
                v-if="choice.experienceReward > 0" 
                type="primary" 
                size="small"
                effect="dark"
              >
                <el-icon><Star /></el-icon>
                +{{ choice.experienceReward }}
              </el-tag>
            </div>
            
            <!-- 需求条件 -->
            <div class="choice-requirements" v-if="choice.requirements">
              <el-icon class="req-icon"><Lock /></el-icon>
              <span class="req-text">需要条件</span>
            </div>
          </div>
          
          <div class="choice-index">
            {{ index + 1 }}
          </div>
        </div>
      </div>

      <!-- 确认按钮 -->
      <div class="choice-actions">
        <el-button 
          type="primary" 
          size="large"
          :disabled="!selectedChoice || makingChoice"
          :loading="makingChoice"
          @click="confirmChoice"
          class="confirm-btn"
        >
          <el-icon><Check /></el-icon>
          确认选择
        </el-button>
        
        <el-button 
          size="large"
          :disabled="makingChoice"
          @click="clearSelection"
          class="clear-btn"
        >
          重新选择
        </el-button>
      </div>
    </div>

    <!-- 游戏结束界面 -->
    <div v-else-if="currentStory?.isEnding" class="game-ending">
      <div class="ending-content">
        <el-icon class="ending-celebration"><Trophy /></el-icon>
        <h3>恭喜完成冒险！</h3>
        <p>你的航海传奇已经载入史册</p>
        
        <div class="ending-actions">
          <el-button type="primary" size="large" @click="startNewAdventure">
            开始新的冒险
          </el-button>
          <el-button size="large" @click="$router.push('/')">
            返回主页
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'

const router = useRouter()
const gameStore = useGameStore()

// 响应式数据
const selectedChoice = ref(null)
const makingChoice = ref(false)
const showAnimation = ref(false)

// 计算属性
const currentStory = computed(() => gameStore.currentStory)
const loading = computed(() => gameStore.loading)

const storyParagraphs = computed(() => {
  if (!currentStory.value?.content) return []
  return currentStory.value.content.split('\n\n').filter(p => p.trim())
})

const availableChoices = computed(() => {
  return currentStory.value?.choices?.filter(choice => choice.isAvailable) || []
})

const storyTypeText = computed(() => {
  const type = currentStory.value?.storyType
  const typeMap = {
    'AWAKENING': '觉醒',
    'TUTORIAL': '教程',
    'NORMAL': '普通',
    'BATTLE': '战斗',
    'TRADE': '贸易',
    'ENDING': '结局'
  }
  return typeMap[type] || '未知'
})

const storyTypeTag = computed(() => {
  const type = currentStory.value?.storyType
  const tagMap = {
    'AWAKENING': 'warning',
    'TUTORIAL': 'info',
    'NORMAL': '',
    'BATTLE': 'danger',
    'TRADE': 'success',
    'ENDING': 'primary'
  }
  return tagMap[type] || ''
})

// 监听故事变化，重置选择和动画
watch(currentStory, () => {
  selectedChoice.value = null
  showAnimation.value = false
  
  nextTick(() => {
    showAnimation.value = true
  })
}, { immediate: true })

// 方法
const selectChoice = (choice) => {
  if (!canMakeChoice(choice)) {
    ElMessage.warning('不满足选择条件')
    return
  }
  
  selectedChoice.value = choice.id
}

const canMakeChoice = (choice) => {
  if (!gameStore.player) return false
  
  // 检查金币需求
  if (choice.goldCost > gameStore.player.gold) {
    return false
  }
  
  // 检查生命值需求
  if (choice.healthCost > gameStore.player.health) {
    return false
  }
  
  // 这里可以添加更多条件检查
  return true
}

const hasEffects = (choice) => {
  return choice.goldCost > 0 || 
         choice.goldReward > 0 || 
         choice.healthCost > 0 || 
         choice.healthReward > 0 || 
         choice.experienceReward > 0
}

const confirmChoice = async () => {
  if (!selectedChoice.value) return
  
  const choice = availableChoices.value.find(c => c.id === selectedChoice.value)
  if (!choice) return
  
  makingChoice.value = true
  
  try {
    // 先更新玩家状态（如果有立即效果）
    const statusChanges = {}
    if (choice.goldCost > 0) statusChanges.gold = -choice.goldCost
    if (choice.goldReward > 0) statusChanges.gold = (statusChanges.gold || 0) + choice.goldReward
    if (choice.healthCost > 0) statusChanges.health = -choice.healthCost
    if (choice.healthReward > 0) statusChanges.health = (statusChanges.health || 0) + choice.healthReward
    if (choice.experienceReward > 0) statusChanges.experience = choice.experienceReward
    
    if (Object.keys(statusChanges).length > 0) {
      await gameStore.updatePlayerStats(statusChanges)
    }
    
    // 执行选择
    await gameStore.makeChoice(choice.id, choice.nextStoryId)
    
    ElMessage.success('选择已执行')
    selectedChoice.value = null
    
  } catch (err) {
    ElMessage.error(err.message)
  } finally {
    makingChoice.value = false
  }
}

const clearSelection = () => {
  selectedChoice.value = null
}

const startNewAdventure = () => {
  gameStore.resetGame()
  router.push('/')
}
</script>

<style lang="scss" scoped>
.story-display {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  overflow: hidden;
}

.story-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  flex-shrink: 0;
  
  .story-info {
    .story-title {
      margin: 0 0 0.8rem 0;
      color: #333;
      font-size: 1.5rem;
      font-weight: bold;
    }
    
    .story-meta {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
  }
  
  .fog-warning {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.5rem 1rem;
    background: linear-gradient(45deg, #f56c6c, #ff8a8a);
    color: white;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(245, 108, 108, 0.3);
    
    .fog-icon {
      animation: pulse 2s infinite;
    }
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.story-content {
  flex: 1;
  margin-bottom: 1.5rem;
  overflow-y: auto;
  
  .story-text {
          .story-paragraphs {
        .story-paragraph {
          margin-bottom: 1.2rem;
          line-height: 1.8;
          color: #00ff7f;
          font-size: 1rem;
          text-align: justify;
          opacity: 0;
          transform: translateY(20px);
          text-shadow: 0 0 5px rgba(0, 255, 127, 0.5);
        
        &.animated {
          animation: fadeInUp 1s ease forwards;
        }
        
        &:last-child {
          margin-bottom: 0;
        }
      }
    }
    
    .ending-mark {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      margin-top: 2rem;
      padding: 1rem;
      background: linear-gradient(45deg, #ffd700, #ffed4e);
      border-radius: 10px;
      color: #b8860b;
      font-weight: bold;
      
      .ending-icon {
        font-size: 1.5rem;
        animation: bounce 2s infinite;
      }
    }
  }
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.choices-section {
  flex-shrink: 0;
  
  .choices-title {
    margin: 0 0 1rem 0;
    color: #333;
    font-size: 1.2rem;
    font-weight: bold;
  }
  
  .choices-list {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
    max-height: 300px;
    overflow-y: auto;
    
    .choice-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1rem;
      border: 2px solid #e0e0e0;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s ease;
      background: #f9f9f9;
      
      &:hover:not(.disabled) {
        border-color: #409EFF;
        background: #f0f9ff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
      }
      
      &.selected {
        border-color: #409EFF;
        background: #ecf5ff;
        box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
      }
      
      &.disabled {
        opacity: 0.5;
        cursor: not-allowed;
        background: #f5f5f5;
      }
      
      .choice-content {
        flex: 1;
        
        .choice-text {
          margin-bottom: 0.5rem;
          color: #333;
          font-weight: 500;
          line-height: 1.5;
        }
        
        .choice-effects {
          display: flex;
          gap: 0.3rem;
          flex-wrap: wrap;
          margin-bottom: 0.5rem;
        }
        
        .choice-requirements {
          display: flex;
          align-items: center;
          gap: 0.3rem;
          color: #f56c6c;
          font-size: 0.8rem;
          
          .req-icon {
            font-size: 0.7rem;
          }
        }
      }
      
      .choice-index {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #409EFF;
        color: white;
        border-radius: 50%;
        font-weight: bold;
        font-size: 0.9rem;
        margin-left: 1rem;
        flex-shrink: 0;
      }
    }
  }
  
  .choice-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    
    .confirm-btn {
      background: linear-gradient(45deg, #67C23A, #85CE61);
      border: none;
      border-radius: 25px;
      padding: 0.8rem 2rem;
      
      &:hover:not(:disabled) {
        background: linear-gradient(45deg, #5daf34, #7bc952);
        transform: translateY(-2px);
      }
    }
    
    .clear-btn {
      border-radius: 25px;
      padding: 0.8rem 2rem;
    }
  }
}

.game-ending {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  
  .ending-content {
    text-align: center;
    padding: 3rem;
    background: linear-gradient(135deg, #ffd700, #ffed4e);
    border-radius: 20px;
    color: #b8860b;
    box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
    
    .ending-celebration {
      font-size: 4rem;
      margin-bottom: 1rem;
      animation: bounce 2s infinite;
    }
    
    h3 {
      margin: 0 0 1rem 0;
      font-size: 2rem;
    }
    
    p {
      margin: 0 0 2rem 0;
      font-size: 1.1rem;
    }
    
    .ending-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
      flex-wrap: wrap;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .story-display {
    padding: 1rem;
  }
  
  .story-header {
    flex-direction: column;
    gap: 1rem;
    
    .fog-warning {
      align-self: flex-end;
    }
  }
  
  .choice-actions {
    flex-direction: column;
  }
  
  .ending-content {
    padding: 2rem;
    
    .ending-actions {
      flex-direction: column;
    }
  }
}
</style> 