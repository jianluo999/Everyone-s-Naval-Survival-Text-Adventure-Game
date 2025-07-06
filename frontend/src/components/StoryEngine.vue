<template>
  <div class="story-engine">
    <!-- 主剧情显示区域 -->
    <div class="story-display">
      <div class="chapter-header">
        <h2 class="chapter-title">{{ currentChapter.title }}</h2>
        <div class="chapter-progress">
          <span class="current-page">{{ currentPage }}</span>
          <span class="separator">/</span>
          <span class="total-pages">{{ currentChapter.totalPages }}</span>
        </div>
      </div>
      
      <!-- 剧情内容 -->
      <div class="story-content" ref="storyContent">
        <div 
          v-for="(paragraph, index) in currentPageContent" 
          :key="index"
          class="story-paragraph"
          :class="paragraph.type"
          v-html="formatParagraph(paragraph.text)"
        ></div>
      </div>
      
      <!-- 物品获得提示 -->
      <div v-if="itemsGained.length > 0" class="items-gained">
        <h4>📦 获得物品：</h4>
        <div class="items-list">
          <div 
            v-for="item in itemsGained" 
            :key="item.id"
            class="item-card"
            :class="item.quality"
          >
            <div class="item-icon">{{ item.icon }}</div>
            <div class="item-info">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-description">{{ item.description }}</div>
              <div class="item-effect" v-if="item.effect">{{ item.effect }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 状态变化提示 -->
      <div v-if="statusChanges.length > 0" class="status-changes">
        <div 
          v-for="change in statusChanges" 
          :key="change.id"
          class="status-change"
          :class="change.type"
        >
          <span class="change-icon">{{ change.icon }}</span>
          <span class="change-text">{{ change.text }}</span>
          <span class="change-value">{{ change.value }}</span>
        </div>
      </div>
    </div>
    
    <!-- 选择系统 -->
    <div v-if="currentChoices.length > 0" class="choice-system">
      <h4>🤔 你的选择：</h4>
      <div class="choices-list">
        <div 
          v-for="(choice, index) in currentChoices" 
          :key="index"
          class="choice-option"
          :class="{ 'disabled': choice.disabled, 'dangerous': choice.risk > 70 }"
          @click="makeChoice(choice)"
        >
          <div class="choice-text">{{ choice.text }}</div>
          <div class="choice-info">
            <span v-if="choice.requirement" class="requirement">
              需要：{{ choice.requirement }}
            </span>
            <span v-if="choice.risk > 0" class="risk-level">
              风险：{{ getRiskText(choice.risk) }}
            </span>
            <span v-if="choice.energyCost > 0" class="energy-cost">
              精力：-{{ choice.energyCost }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 剧情控制 -->
    <div class="story-controls">
      <el-button-group>
        <el-button 
          @click="previousPage" 
          :disabled="currentPage <= 1"
          icon="ArrowLeft"
        >
          上一页
        </el-button>
        
        <el-button 
          @click="nextPage" 
          :disabled="currentPage >= currentChapter.totalPages && currentChoices.length === 0"
          type="primary"
        >
          {{ currentChoices.length > 0 ? '等待选择' : '下一页' }}
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </el-button-group>
      
      <div class="auto-play-controls">
        <el-switch
          v-model="autoPlay"
          active-text="自动播放"
          @change="toggleAutoPlay"
        />
        <el-slider
          v-if="autoPlay"
          v-model="autoPlaySpeed"
          :min="1"
          :max="10"
          :step="1"
          style="width: 100px; margin-left: 10px;"
        />
      </div>
    </div>
    
    <!-- 剧情历史 -->
    <div class="story-history" v-if="showHistory">
      <h4>📚 剧情回顾</h4>
      <div class="history-list">
        <div 
          v-for="entry in storyHistory" 
          :key="entry.id"
          class="history-entry"
          @click="jumpToHistory(entry)"
        >
          <div class="history-chapter">{{ entry.chapter }}</div>
          <div class="history-content">{{ entry.summary }}</div>
          <div class="history-time">{{ formatTime(entry.timestamp) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

const gameStore = useGameStore()

// 响应式数据
const currentStoryId = ref(gameStore.gameState?.currentStoryId || 'chapter_01_start');
const currentChapter = ref({ title: '加载中...', totalPages: 1, content: {} });
const currentChoices = ref([]);
const currentPage = ref(1);
const autoPlay = ref(false);
const autoPlaySpeed = ref(3);
const showHistory = ref(false);
const storyContent = ref(null);
const itemsGained = ref([]);
const statusChanges = ref([]);
const storyHistory = ref([]);


// 计算属性
const currentPageContent = computed(() => {
  const content = currentChapter.value.content;
  if (content && content[currentPage.value]) {
    return content[currentPage.value];
  }
  return [];
});


// 方法
const loadStory = async (storyId) => {
  if (!storyId) {
    ElMessage.error('无效的故事ID');
    return;
  }
  try {
    const response = await fetch(`http://localhost:8080/api/game/story/${storyId}`);
    if (!response.ok) {
      throw new Error('故事加载失败');
    }
    const data = await response.json();
    if (data.success) {
      const story = data.story;
      // 后端返回的content是JSON字符串，需要解析
      const parsedContent = JSON.parse(story.content);

      currentChapter.value = {
        id: story.storyId,
        title: story.title,
        content: parsedContent.pages, // 假设后端返回的content中有pages
        totalPages: Object.keys(parsedContent.pages).length,
      };
      
      // 后端直接返回choices数组
      currentChoices.value = story.choices || []; 
      
      currentPage.value = 1;
      gameStore.updateGameState({ currentStoryId: storyId });
    } else {
      ElMessage.error(data.error || '未知错误');
    }
  } catch (error) {
    console.error('加载故事时出错:', error);
    ElMessage.error('无法连接到服务器或加载故事失败');
  }
};


const formatParagraph = (text) => {
  text = text.replace(/【([^】]+)】/g, '<span class="item-tag">【$1】</span>');
  text = text.replace(/(\d+)点/g, '<span class="number-value">$1点</span>');
  text = text.replace(/(buff|debuff)/gi, '<span class="status-effect">$1</span>');
  return text;
};

const nextPage = () => {
  if (currentChoices.value.length > 0 && currentPage.value >= currentChapter.value.totalPages) {
    ElMessage.warning('请先做出选择');
    return;
  }
  
  if (currentPage.value < currentChapter.value.totalPages) {
    currentPage.value++;
    scrollToTop();
    addToHistory();
  } else {
    ElMessage.info('本章已结束，请做出选择或等待剧情自动推进。');
  }
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    scrollToTop();
  }
};

const makeChoice = async (choice) => {
  if (choice.disabled) {
    ElMessage.error('不满足选择条件');
    return;
  }

  try {
    const response = await fetch('http://localhost:8080/api/game/choice', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        playerName: gameStore.player.name,
        choiceId: choice.id,
        nextStoryId: choice.nextStoryId,
      }),
    });

    const data = await response.json();

    if (data.success) {
      ElMessage.success('选择成功');
      gameStore.updatePlayer(data.player);
      // 加载下一个故事片段
      loadStory(choice.nextStoryId);
    } else {
      ElMessage.error(data.error || '选择失败');
    }
  } catch (error) {
    console.error('做出选择时出错:', error);
    ElMessage.error('无法连接到服务器或处理选择失败');
  }
};


const getRiskText = (risk) => {
  if (risk < 30) return '低';
  if (risk < 60) return '中';
  if (risk < 80) return '高';
  return '极高';
};

const toggleAutoPlay = (enabled) => {
  if (enabled) {
    startAutoPlay();
  } else {
    stopAutoPlay();
  }
};

let autoPlayTimer = null;

const startAutoPlay = () => {
  autoPlayTimer = setInterval(() => {
    if (currentChoices.value.length === 0) {
      nextPage();
    }
  }, (11 - autoPlaySpeed.value) * 1000);
};

const stopAutoPlay = () => {
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer);
    autoPlayTimer = null;
  }
};

const scrollToTop = () => {
  nextTick(() => {
    if (storyContent.value) {
      storyContent.value.scrollTop = 0;
    }
  });
};

const addToHistory = () => {
  const entry = {
    id: Date.now(),
    chapter: currentChapter.value.title,
    summary: currentPageContent.value[0]?.text.substring(0, 30) + '...',
    timestamp: new Date(),
  };
  
  storyHistory.value.unshift(entry);
  
  if (storyHistory.value.length > 20) {
    storyHistory.value = storyHistory.value.slice(0, 20);
  }
};

const jumpToHistory = (entry) => {
  ElMessage.info(`跳转到：${entry.chapter}`);
};

const formatTime = (timestamp) => {
  return timestamp.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

watch(currentPage, () => {
  itemsGained.value = [];
  statusChanges.value = [];
});

onMounted(() => {
  loadStory(currentStoryId.value);
  addToHistory();
});
</script>

<style lang="scss" scoped>
.story-engine {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #fff;
  padding: 1rem;
  overflow: hidden;
}

.story-display {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(52, 152, 219, 0.3);
}

.chapter-title {
  color: #3498db;
  margin: 0;
  font-size: 1.5rem;
}

.chapter-progress {
  color: #bbb;
  font-size: 0.9rem;
}

.story-content {
  margin-bottom: 2rem;
}

.story-paragraph {
  margin-bottom: 1rem;
  line-height: 1.8;
  padding: 0.8rem;
  border-radius: 0.5rem;
  
  &.narrative {
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid #3498db;
  }
  
  &.action {
    background: rgba(46, 204, 113, 0.1);
    border-left: 3px solid #2ecc71;
  }
  
  &.thought {
    background: rgba(155, 89, 182, 0.1);
    border-left: 3px solid #9b59b6;
    font-style: italic;
  }
  
  &.discovery {
    background: rgba(243, 156, 18, 0.1);
    border-left: 3px solid #f39c12;
  }
  
  &.item {
    background: rgba(231, 76, 60, 0.1);
    border-left: 3px solid #e74c3c;
    font-family: monospace;
  }
  
  &.status {
    background: rgba(52, 152, 219, 0.1);
    border-left: 3px solid #3498db;
  }
  
  &.crafting {
    background: rgba(142, 68, 173, 0.1);
    border-left: 3px solid #8e44ad;
  }
}

:deep(.item-tag) {
  color: #f39c12;
  font-weight: bold;
}

:deep(.number-value) {
  color: #e74c3c;
  font-weight: bold;
}

:deep(.status-effect) {
  color: #2ecc71;
  font-weight: bold;
  text-transform: uppercase;
}

.items-gained {
  background: rgba(46, 204, 113, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  
  h4 {
    color: #2ecc71;
    margin: 0 0 0.5rem 0;
  }
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  
  &.rare {
    border: 1px solid #9b59b6;
    box-shadow: 0 0 10px rgba(155, 89, 182, 0.3);
  }
  
  &.good {
    border: 1px solid #3498db;
    box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
  }
  
  &.common {
    border: 1px solid #95a5a6;
  }
}

.item-icon {
  font-size: 2rem;
  width: 50px;
  text-align: center;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: bold;
  color: #f39c12;
  margin-bottom: 0.2rem;
}

.item-description {
  color: #bbb;
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

.item-effect {
  color: #2ecc71;
  font-size: 0.8rem;
  font-style: italic;
}

.status-changes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.status-change {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.8rem;
  border-radius: 1rem;
  font-size: 0.9rem;
  
  &.positive {
    background: rgba(46, 204, 113, 0.2);
    color: #2ecc71;
  }
  
  &.negative {
    background: rgba(231, 76, 60, 0.2);
    color: #e74c3c;
  }
}

.choice-system {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  
  h4 {
    color: #f39c12;
    margin: 0 0 0.8rem 0;
  }
}

.choices-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.choice-option {
  padding: 1rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover:not(.disabled) {
    background: rgba(52, 152, 219, 0.1);
    border-color: #3498db;
  }
  
  &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  &.dangerous {
    border-color: #e74c3c;
    background: rgba(231, 76, 60, 0.1);
  }
}

.choice-text {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.choice-info {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #bbb;
}

.requirement {
  color: #f39c12;
}

.risk-level {
  color: #e74c3c;
}

.energy-cost {
  color: #3498db;
}

.story-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
}

.auto-play-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.story-history {
  max-height: 200px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-top: 1rem;
  
  h4 {
    color: #3498db;
    margin: 0 0 0.5rem 0;
  }
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.history-entry {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.5rem;
  border-radius: 0.3rem;
  cursor: pointer;
  transition: background 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.05);
  }
}

.history-chapter {
  color: #f39c12;
  font-weight: bold;
  min-width: 80px;
}

.history-content {
  flex: 1;
  color: #bbb;
  font-size: 0.9rem;
}

.history-time {
  color: #666;
  font-size: 0.8rem;
}
</style>