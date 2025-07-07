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
      <!-- 有选择时显示选择列表 -->
      <div v-if="availableChoices && availableChoices.length > 0">
        <h3 class="choices-title">你的选择：<span class="choice-hint">（单击选中，双击执行）</span></h3>

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
            @dblclick="executeChoice(choice)"
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
                <el-icon><Money /></el-icon>
                -{{ choice.goldCost }}
              </el-tag>

              <el-tag
                v-if="choice.goldReward > 0"
                type="success"
                size="small"
                effect="dark"
              >
                <el-icon><Money /></el-icon>
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
      </div>

      <!-- 死路处理：没有选择时显示结束冒险选项 -->
      <div v-else class="dead-end-section">
        <div class="dead-end-content">
          <el-icon class="dead-end-icon"><Warning /></el-icon>
          <h3 class="dead-end-title">冒险陷入困境</h3>
          <p class="dead-end-description">
            你发现自己陷入了困境，无法继续前进。<br>
            也许是时候结束这次冒险，重新开始了。
          </p>

          <div class="dead-end-actions">
            <el-button
              type="danger"
              size="large"
              @click="endAdventure"
              :loading="makingChoice"
            >
              结束冒险
            </el-button>
            <el-button
              size="large"
              @click="$router.push('/')"
            >
              返回主页
            </el-button>
          </div>
        </div>
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
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Star, Lock, Check, Money, Warning, InfoFilled, Trophy, InfoFilled as Heart } from '@element-plus/icons-vue'

const router = useRouter()
const gameStore = useGameStore()

// 定义emit
const emit = defineEmits(['choice-made'])

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

// 双击直接执行选择
const executeChoice = async (choice) => {
  if (!canMakeChoice(choice)) {
    ElMessage.warning('不满足选择条件')
    return
  }

  if (makingChoice.value) {
    return // 防止重复点击
  }

  selectedChoice.value = choice.id
  await confirmChoice()
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
    // 记录选择到航海日志
    emit('choice-made', {
      choice: choice,
      storyTitle: currentStory.value?.title || '未知故事'
    })
    
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

const endAdventure = async () => {
  try {
    makingChoice.value = true

    // 显示确认对话框
    await ElMessageBox.confirm(
      '确定要结束当前冒险吗？你的进度将会丢失。',
      '结束冒险',
      {
        confirmButtonText: '确定结束',
        cancelButtonText: '继续冒险',
        type: 'warning'
      }
    )

    // 重置游戏并返回主页
    gameStore.resetGame()
    ElMessage.success('冒险已结束')
    router.push('/')

  } catch {
    // 用户取消了操作
  } finally {
    makingChoice.value = false
  }
}

// 组件挂载时添加额外的文本选择保护
onMounted(() => {
  // 禁用文本选择的额外保护
  const preventSelection = (e) => {
    if (e.target.closest('.story-display')) {
      e.preventDefault()
      return false
    }
  }

  const preventDrag = (e) => {
    if (e.target.closest('.story-display')) {
      e.preventDefault()
      return false
    }
  }

  const preventContextMenu = (e) => {
    if (e.target.closest('.story-text')) {
      e.preventDefault()
      return false
    }
  }

  // 添加事件监听器
  document.addEventListener('selectstart', preventSelection)
  document.addEventListener('dragstart', preventDrag)
  document.addEventListener('contextmenu', preventContextMenu)

  // 禁用键盘选择快捷键
  document.addEventListener('keydown', (e) => {
    if (e.target.closest('.story-display')) {
      // 禁用 Ctrl+A (全选)
      if (e.ctrlKey && e.key === 'a') {
        e.preventDefault()
        return false
      }
      // 禁用 Ctrl+C (复制)
      if (e.ctrlKey && e.key === 'c') {
        e.preventDefault()
        return false
      }
    }
  })
})
</script>

<style lang="scss" scoped>
.story-display {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  overflow: hidden;

  // 彻底禁用整个组件的文本选择和各种高亮效果
  user-select: none !important;
  -webkit-user-select: none !important;
  -moz-user-select: none !important;
  -ms-user-select: none !important;

  // 禁用点击高亮
  -webkit-tap-highlight-color: transparent !important;
  -webkit-touch-callout: none !important;

  // 禁用outline
  outline: none !important;

  // 禁用所有可能的选择效果
  &::selection {
    background: transparent !important;
    color: transparent !important;
  }

  &::-moz-selection {
    background: transparent !important;
    color: transparent !important;
  }

  // 确保所有子元素也不会有选择效果
  * {
    user-select: none !important;
    -webkit-user-select: none !important;
    -moz-user-select: none !important;
    -ms-user-select: none !important;
    -webkit-tap-highlight-color: transparent !important;
    outline: none !important;

    &::selection {
      background: transparent !important;
      color: transparent !important;
    }

    &::-moz-selection {
      background: transparent !important;
      color: transparent !important;
    }

    &::selection {
      background: transparent;
    }

    &::-moz-selection {
      background: transparent;
    }
  }
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
    // 彻底禁用故事内容的文本选择
    user-select: none !important;
    -webkit-user-select: none !important;
    -moz-user-select: none !important;
    -ms-user-select: none !important;

    // 禁用点击高亮和各种交互效果
    -webkit-tap-highlight-color: transparent !important;
    -webkit-touch-callout: none !important;

    // 禁用右键菜单
    pointer-events: none;

    // 禁用outline和focus
    outline: none !important;

    // 禁用所有选择效果
    &::selection {
      background: transparent !important;
    }

    &::-moz-selection {
      background: transparent !important;
    }

    .story-paragraphs {
      // 禁用整个段落容器的选择
      user-select: none !important;
      -webkit-user-select: none !important;
      -moz-user-select: none !important;
      -ms-user-select: none !important;
      pointer-events: none;

      .story-paragraph {
        margin-bottom: 1.2rem;
        line-height: 1.8;
        color: #ffffff;
        font-size: 1rem;
        text-align: justify;
        opacity: 0;
        transform: translateY(20px);
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
        font-family: 'Consolas', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
        font-weight: 400;
        letter-spacing: 0.3px;

        // 彻底禁用段落的选择和交互
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        -webkit-tap-highlight-color: transparent !important;
        pointer-events: none;

        // 禁用所有选择效果
        &::selection {
          background: transparent !important;
        }

        &::-moz-selection {
          background: transparent !important;
        }
        
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

    .choice-hint {
      font-size: 0.8rem;
      color: #666;
      font-weight: normal;
      margin-left: 8px;
    }
  }
  
  .choices-list {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
    max-height: 300px;
    overflow-y: auto;

    // 禁用整个选择列表的文本选择
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;

    // 禁用点击高亮
    -webkit-tap-highlight-color: transparent;
    
    .choice-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1rem;
      border: 2px solid rgba(30, 144, 255, 0.4);
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s ease;
      background: rgba(0, 40, 80, 0.8);
      position: relative;

      // 彻底禁用文本选择和各种高亮效果
      user-select: none;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;

      // 禁用点击高亮
      -webkit-tap-highlight-color: transparent;
      -webkit-touch-callout: none;
      -webkit-appearance: none;

      // 禁用outline
      outline: none !important;

      // 禁用focus样式
      &:focus {
        outline: none !important;
        box-shadow: none !important;
      }

      // 禁用所有可能的选择效果
      &::selection {
        background: transparent;
      }

      &::-moz-selection {
        background: transparent;
      }

      // 双击提示
      &::after {
        content: '双击执行';
        position: absolute;
        top: 4px;
        right: 8px;
        font-size: 10px;
        color: rgba(102, 255, 204, 0.6);
        opacity: 0;
        transition: opacity 0.3s ease;
      }
      
      &:hover:not(.disabled) {
        border-color: #1E90FF;
        background: rgba(30, 144, 255, 0.15);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3);

        &::after {
          opacity: 1;
        }
      }

      // 双击时的反馈效果
      &:active {
        transform: translateY(0px) scale(0.98);
        transition: transform 0.1s ease;
      }
      
      &.selected {
        border-color: #1E90FF;
        background: rgba(30, 144, 255, 0.25);
        box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.2);
      }
      
      &.disabled {
        opacity: 0.5;
        cursor: not-allowed;
        background: rgba(0, 20, 40, 0.6);
      }
      
      .choice-content {
        flex: 1;
        
        .choice-text {
          margin-bottom: 0.5rem;
          color: #ffffff;
          font-weight: 500;
          line-height: 1.5;
          text-shadow: 0 0 5px rgba(255, 255, 255, 0.6);

          // 彻底确保选择文本不会被选中
          user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;

          // 禁用点击高亮
          -webkit-tap-highlight-color: transparent;

          // 禁用选择效果
          &::selection {
            background: transparent;
          }

          &::-moz-selection {
            background: transparent;
          }
        }
        
        .choice-effects {
          display: flex;
          gap: 0.3rem;
          flex-wrap: wrap;
          margin-bottom: 0.5rem;

          // 禁用选择
          user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;
        }

        .choice-requirements {
          display: flex;
          align-items: center;
          gap: 0.3rem;
          color: #f56c6c;
          font-size: 0.8rem;

          // 禁用选择
          user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;

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
        background: #1E90FF;
        color: white;
        border-radius: 50%;
        font-weight: bold;
        font-size: 0.9rem;
        margin-left: 1rem;
        flex-shrink: 0;
        box-shadow: 0 0 8px rgba(30, 144, 255, 0.4);
      }
    }
  }

  .choice-hint {
    text-align: center;
    color: #66ffcc;
    font-size: 0.85rem;
    margin: 1rem 0;
    padding: 0.5rem;
    background: rgba(102, 255, 204, 0.1);
    border: 1px solid rgba(102, 255, 204, 0.3);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;

    .el-icon {
      font-size: 1rem;
    }
  }


}

.dead-end-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;

  .dead-end-content {
    text-align: center;
    padding: 2.5rem;
    background: linear-gradient(135deg, #ff6b6b, #ee5a52);
    border-radius: 15px;
    color: white;
    box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
    max-width: 500px;

    .dead-end-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      color: #ffeb3b;
      animation: pulse 2s infinite;
    }

    .dead-end-title {
      margin: 0 0 1rem 0;
      font-size: 1.8rem;
      font-weight: bold;
    }

    .dead-end-description {
      margin: 0 0 2rem 0;
      font-size: 1rem;
      line-height: 1.6;
      opacity: 0.9;
    }

    .dead-end-actions {
      display: flex;
      gap: 1rem;
      justify-content: center;
      flex-wrap: wrap;
    }
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
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
  

  
  .ending-content {
    padding: 2rem;
    
    .ending-actions {
      flex-direction: column;
    }
  }
}
</style> 