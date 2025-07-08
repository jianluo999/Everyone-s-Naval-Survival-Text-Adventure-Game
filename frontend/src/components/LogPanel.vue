<template>
  <div class="log-panel">
    <div class="log-header">
      <h3>
        <el-icon><Document /></el-icon>
        航海日志
      </h3>
      <div class="log-controls">
        <el-button size="small" @click="clearLogs" type="danger" plain>
          <el-icon><Delete /></el-icon>
          清空日志
        </el-button>
        <el-button size="small" @click="exportLogs" type="primary" plain>
          <el-icon><Download /></el-icon>
          导出日志
        </el-button>
      </div>
    </div>

    <div class="log-content">
      <div class="log-filters">
        <el-select v-model="selectedType" placeholder="筛选类型" size="small" style="width: 120px">
          <el-option label="全部" value="all" />
          <el-option label="航行" value="navigation" />
          <el-option label="战斗" value="combat" />
          <el-option label="交易" value="trade" />
          <el-option label="探索" value="exploration" />
          <el-option label="事件" value="event" />
        </el-select>
        
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          size="small"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 240px"
        />
      </div>

      <div class="log-entries">
        <div 
          v-for="entry in filteredLogs" 
          :key="entry.id"
          class="log-entry"
          :class="entry.type"
        >
          <div class="entry-header">
            <span class="entry-time">{{ formatTime(entry.timestamp) }}</span>
            <span class="entry-type">{{ getTypeLabel(entry.type) }}</span>
            <span class="entry-location" v-if="entry.location">{{ entry.location }}</span>
          </div>
          <div class="entry-content">
            {{ entry.content }}
          </div>
          <div class="entry-details" v-if="entry.details">
            <div class="detail-item" v-for="detail in entry.details" :key="detail.key">
              <span class="detail-key">{{ detail.key }}:</span>
              <span class="detail-value">{{ detail.value }}</span>
            </div>
          </div>
        </div>

        <div v-if="filteredLogs.length === 0" class="empty-log">
          <el-icon><Document /></el-icon>
          <p>暂无日志记录</p>
          <p class="hint">开始你的冒险，记录将自动添加到这里</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'
import { Document, Delete, Download } from '@element-plus/icons-vue'

const gameStore = useGameStore()

// 响应式数据
const selectedType = ref('all')
const dateRange = ref([])
const logs = ref([
  {
    id: 1,
    timestamp: new Date(),
    type: 'navigation',
    location: '起始港口',
    content: '开始了新的航海冒险',
    details: [
      { key: '船只状态', value: '良好' },
      { key: '补给', value: '充足' }
    ]
  }
])

// 计算属性
const filteredLogs = computed(() => {
  let filtered = logs.value

  // 按类型筛选
  if (selectedType.value !== 'all') {
    filtered = filtered.filter(log => log.type === selectedType.value)
  }

  // 按日期筛选
  if (dateRange.value && dateRange.value.length === 2) {
    const [start, end] = dateRange.value
    filtered = filtered.filter(log => {
      const logDate = new Date(log.timestamp)
      return logDate >= start && logDate <= end
    })
  }

  return filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
})

// 方法
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

const getTypeLabel = (type) => {
  const labels = {
    navigation: '🧭 航行',
    combat: '⚔️ 战斗',
    trade: '💰 交易',
    exploration: '🗺️ 探索',
    event: '📜 事件'
  }
  return labels[type] || '📝 记录'
}

const clearLogs = () => {
  ElMessage.confirm('确定要清空所有日志吗？', '确认操作', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    logs.value = []
    ElMessage.success('日志已清空')
  }).catch(() => {
    // 用户取消
  })
}

const exportLogs = () => {
  const logText = filteredLogs.value.map(log => {
    return `[${formatTime(log.timestamp)}] ${getTypeLabel(log.type)} - ${log.content}`
  }).join('\n')
  
  const blob = new Blob([logText], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `航海日志_${new Date().toISOString().split('T')[0]}.txt`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('日志导出成功')
}

// 添加新日志条目的方法
const addLogEntry = (type, content, location = null, details = null) => {
  const newEntry = {
    id: Date.now(),
    timestamp: new Date(),
    type,
    location,
    content,
    details
  }
  logs.value.unshift(newEntry)
}

// 暴露方法给父组件
defineExpose({
  addLogEntry
})

onMounted(() => {
  // 可以从gameStore加载历史日志
  // logs.value = gameStore.logs || []
})
</script>

<style scoped>
.log-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(0, 20, 40, 0.95);
  color: #e0e6ed;
  border-radius: 8px;
  overflow: hidden;
}

.log-header {
  padding: 16px;
  background: rgba(0, 30, 60, 0.8);
  border-bottom: 1px solid rgba(102, 255, 204, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #66ffcc;
}

.log-controls {
  display: flex;
  gap: 8px;
}

.log-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.log-filters {
  padding: 12px 16px;
  background: rgba(0, 25, 50, 0.6);
  border-bottom: 1px solid rgba(102, 255, 204, 0.2);
  display: flex;
  gap: 12px;
  align-items: center;
}

.log-entries {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.log-entry {
  background: rgba(0, 30, 60, 0.4);
  border: 1px solid rgba(102, 255, 204, 0.2);
  border-radius: 6px;
  margin-bottom: 8px;
  padding: 12px;
  transition: all 0.3s ease;
}

.log-entry:hover {
  background: rgba(0, 40, 80, 0.6);
  border-color: rgba(102, 255, 204, 0.4);
}

.entry-header {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 8px;
  font-size: 12px;
}

.entry-time {
  color: #888;
}

.entry-type {
  background: rgba(102, 255, 204, 0.2);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
}

.entry-location {
  color: #66ffcc;
  font-weight: bold;
}

.entry-content {
  color: #e0e6ed;
  line-height: 1.5;
  margin-bottom: 8px;
}

.entry-details {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 12px;
}

.detail-item {
  background: rgba(0, 20, 40, 0.6);
  padding: 4px 8px;
  border-radius: 4px;
}

.detail-key {
  color: #888;
}

.detail-value {
  color: #66ffcc;
  margin-left: 4px;
}

.empty-log {
  text-align: center;
  padding: 40px 20px;
  color: #888;
}

.empty-log .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.hint {
  font-size: 12px;
  margin-top: 8px;
  opacity: 0.7;
}

/* 日志类型样式 */
.log-entry.navigation {
  border-left: 4px solid #409eff;
}

.log-entry.combat {
  border-left: 4px solid #f56c6c;
}

.log-entry.trade {
  border-left: 4px solid #e6a23c;
}

.log-entry.exploration {
  border-left: 4px solid #67c23a;
}

.log-entry.event {
  border-left: 4px solid #909399;
}
</style>
