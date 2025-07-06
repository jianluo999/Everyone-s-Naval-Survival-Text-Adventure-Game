<template>
  <el-dialog
    v-model="visible"
    title="游戏设置"
    width="500px"
    :before-close="handleClose"
    class="game-settings-dialog"
  >
    <div class="settings-content">
      <!-- 音效设置 -->
      <div class="setting-section">
        <h4>
          <el-icon><Headphones /></el-icon>
          音效设置
        </h4>
        <div class="setting-item">
          <span>启用音效</span>
          <el-switch 
            v-model="settings.audio.enabled"
            @change="updateAudioEnabled"
          />
        </div>
        <div class="setting-item">
          <span>音效音量</span>
          <el-slider 
            v-model="settings.audio.volume"
            :min="0"
            :max="100"
            :disabled="!settings.audio.enabled"
            @change="updateAudioVolume"
            style="width: 200px;"
          />
        </div>
        <div class="setting-item">
          <span>环境音</span>
          <el-switch 
            v-model="settings.audio.ambient"
            :disabled="!settings.audio.enabled"
            @change="updateAmbientAudio"
          />
        </div>
      </div>

      <!-- 快捷键设置 -->
      <div class="setting-section">
        <h4>
          <el-icon><Keyboard /></el-icon>
          快捷键设置
        </h4>
        <div class="setting-item">
          <span>启用快捷键</span>
          <el-switch 
            v-model="settings.keyboard.enabled"
            @change="updateKeyboardEnabled"
          />
        </div>
        <div class="setting-item">
          <el-button 
            size="small" 
            @click="showKeyboardHelp"
            :disabled="!settings.keyboard.enabled"
          >
            查看快捷键
          </el-button>
        </div>
      </div>

      <!-- 自动保存设置 -->
      <div class="setting-section">
        <h4>
          <el-icon><Document /></el-icon>
          自动保存设置
        </h4>
        <div class="setting-item">
          <span>启用自动保存</span>
          <el-switch 
            v-model="settings.autoSave.enabled"
            @change="updateAutoSaveEnabled"
          />
        </div>
        <div class="setting-item">
          <span>保存间隔</span>
          <el-select 
            v-model="settings.autoSave.interval"
            :disabled="!settings.autoSave.enabled"
            @change="updateAutoSaveInterval"
            style="width: 120px;"
          >
            <el-option label="15秒" :value="15000" />
            <el-option label="30秒" :value="30000" />
            <el-option label="1分钟" :value="60000" />
            <el-option label="2分钟" :value="120000" />
            <el-option label="5分钟" :value="300000" />
          </el-select>
        </div>
        <div class="setting-item">
          <span>保存记录数</span>
          <el-input-number 
            v-model="settings.autoSave.maxSaves"
            :min="5"
            :max="20"
            :disabled="!settings.autoSave.enabled"
            @change="updateMaxSaves"
            size="small"
            style="width: 120px;"
          />
        </div>
      </div>

      <!-- 界面设置 -->
      <div class="setting-section">
        <h4>
          <el-icon><Monitor /></el-icon>
          界面设置
        </h4>
        <div class="setting-item">
          <span>显示FPS</span>
          <el-switch v-model="settings.ui.showFPS" />
        </div>
        <div class="setting-item">
          <span>动画效果</span>
          <el-switch v-model="settings.ui.animations" />
        </div>
        <div class="setting-item">
          <span>粒子效果</span>
          <el-switch v-model="settings.ui.particles" />
        </div>
      </div>

      <!-- 保存统计 -->
      <div class="setting-section" v-if="saveStats">
        <h4>
          <el-icon><DataAnalysis /></el-icon>
          保存统计
        </h4>
        <div class="stats-grid">
          <div class="stat-item">
            <span>自动保存次数</span>
            <span class="stat-value">{{ saveStats.totalSaves }}</span>
          </div>
          <div class="stat-item">
            <span>最后保存时间</span>
            <span class="stat-value">{{ formatTime(saveStats.lastSaveTime) }}</span>
          </div>
          <div class="stat-item">
            <span>存储大小</span>
            <span class="stat-value">{{ formatSize(saveStats.totalSize) }}</span>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="resetSettings">重置设置</el-button>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Headphones, Keyboard, Document, Monitor, DataAnalysis } from '@element-plus/icons-vue'
import { audioManager } from '@/utils/audioManager'
import { keyboardManager } from '@/utils/keyboardManager'
import { autoSaveManager } from '@/utils/autoSaveManager'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = ref(props.modelValue)
const saveStats = ref(null)

// 设置数据
const settings = reactive({
  audio: {
    enabled: true,
    volume: 50,
    ambient: true
  },
  keyboard: {
    enabled: true
  },
  autoSave: {
    enabled: true,
    interval: 30000,
    maxSaves: 10
  },
  ui: {
    showFPS: false,
    animations: true,
    particles: true
  }
})

// 监听visible变化
watch(() => props.modelValue, (newVal) => {
  visible.value = newVal
})

watch(visible, (newVal) => {
  emit('update:modelValue', newVal)
})

// 加载设置
const loadSettings = () => {
  try {
    const savedSettings = localStorage.getItem('gameSettings')
    if (savedSettings) {
      Object.assign(settings, JSON.parse(savedSettings))
    }
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

// 保存设置
const saveSettings = () => {
  try {
    localStorage.setItem('gameSettings', JSON.stringify(settings))
    ElMessage.success('设置已保存')
    visible.value = false
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  }
}

// 重置设置
const resetSettings = () => {
  settings.audio.enabled = true
  settings.audio.volume = 50
  settings.audio.ambient = true
  settings.keyboard.enabled = true
  settings.autoSave.enabled = true
  settings.autoSave.interval = 30000
  settings.autoSave.maxSaves = 10
  settings.ui.showFPS = false
  settings.ui.animations = true
  settings.ui.particles = true
  
  ElMessage.info('设置已重置')
}

// 更新音效设置
const updateAudioEnabled = (enabled) => {
  audioManager.setEnabled(enabled)
  if (!enabled) {
    audioManager.stopAmbient()
  } else if (settings.audio.ambient) {
    audioManager.playAmbient()
  }
}

const updateAudioVolume = (volume) => {
  audioManager.setVolume(volume / 100)
}

const updateAmbientAudio = (enabled) => {
  if (enabled && settings.audio.enabled) {
    audioManager.playAmbient()
  } else {
    audioManager.stopAmbient()
  }
}

// 更新快捷键设置
const updateKeyboardEnabled = (enabled) => {
  keyboardManager.setEnabled(enabled)
}

const showKeyboardHelp = () => {
  keyboardManager.showHelp()
}

// 更新自动保存设置
const updateAutoSaveEnabled = (enabled) => {
  autoSaveManager.setEnabled(enabled)
}

const updateAutoSaveInterval = (interval) => {
  autoSaveManager.setInterval(interval)
}

const updateMaxSaves = (maxSaves) => {
  autoSaveManager.maxSaves = maxSaves
}

// 格式化时间
const formatTime = (timestamp) => {
  if (!timestamp) return '无'
  return new Date(timestamp).toLocaleString()
}

// 格式化大小
const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 关闭对话框
const handleClose = () => {
  visible.value = false
}

// 更新保存统计
const updateSaveStats = () => {
  saveStats.value = autoSaveManager.getSaveStats()
}

onMounted(() => {
  loadSettings()
  updateSaveStats()
  
  // 应用设置
  updateAudioEnabled(settings.audio.enabled)
  updateAudioVolume(settings.audio.volume)
  updateAmbientAudio(settings.audio.ambient)
  updateKeyboardEnabled(settings.keyboard.enabled)
  updateAutoSaveEnabled(settings.autoSave.enabled)
  updateAutoSaveInterval(settings.autoSave.interval)
  updateMaxSaves(settings.autoSave.maxSaves)
})
</script>

<style lang="scss" scoped>
.game-settings-dialog {
  :deep(.el-dialog) {
    background: rgba(0, 20, 40, 0.95);
    border: 2px solid #66ffcc;
    border-radius: 12px;
  }
  
  :deep(.el-dialog__header) {
    background: rgba(0, 40, 80, 0.8);
    border-bottom: 1px solid #66ffcc;
    color: #66ffcc;
  }
  
  :deep(.el-dialog__body) {
    color: #ccc;
  }
}

.settings-content {
  max-height: 500px;
  overflow-y: auto;
}

.setting-section {
  margin-bottom: 2rem;
  
  h4 {
    color: #66ffcc;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid rgba(102, 255, 204, 0.3);
    padding-bottom: 0.5rem;
  }
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
  
  span {
    color: #ccc;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: rgba(0, 40, 80, 0.3);
  border-radius: 4px;
  
  .stat-value {
    color: #FFD700;
    font-weight: bold;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
