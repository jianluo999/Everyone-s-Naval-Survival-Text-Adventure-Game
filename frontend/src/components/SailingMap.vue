<template>
  <div class="sailing-map">
    <div class="map-header">
      <h3>
        <el-icon><Location /></el-icon>
        航海地图
      </h3>
      <div class="map-controls">
        <el-button-group>
          <el-button 
            :type="viewMode === 'overview' ? 'primary' : ''"
            size="small"
            @click="viewMode = 'overview'"
          >
            <el-icon><View /></el-icon>
            总览
          </el-button>
          <el-button 
            :type="viewMode === 'detailed' ? 'primary' : ''"
            size="small"
            @click="viewMode = 'detailed'"
          >
            <el-icon><ZoomIn /></el-icon>
            详细
          </el-button>
        </el-button-group>
        
        <el-button size="small" @click="centerOnShip" type="info" plain>
          <el-icon><Aim /></el-icon>
          定位船只
        </el-button>
      </div>
    </div>

    <div class="map-container">
      <div class="map-legend">
        <div class="legend-item">
          <div class="legend-dot current"></div>
          <span>当前位置</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot explored"></div>
          <span>已探索</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot unknown"></div>
          <span>未知海域</span>
        </div>
        <div class="legend-item">
          <div class="legend-dot danger"></div>
          <span>危险区域</span>
        </div>
      </div>

      <div class="map-viewport" ref="mapViewport">
        <svg 
          class="sea-map" 
          :viewBox="`${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`"
          @mousedown="startPan"
          @mousemove="handlePan"
          @mouseup="endPan"
          @wheel="handleZoom"
        >
          <!-- 海洋背景 -->
          <defs>
            <radialGradient id="seaGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" style="stop-color:#001122;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#003366;stop-opacity:1" />
            </radialGradient>
            <pattern id="waves" patternUnits="userSpaceOnUse" width="40" height="20">
              <path d="M0,10 Q10,0 20,10 T40,10" stroke="#004488" stroke-width="1" fill="none" opacity="0.3"/>
            </pattern>
          </defs>
          
          <!-- 海洋背景 -->
          <rect width="2000" height="1500" fill="url(#seaGradient)" />
          <rect width="2000" height="1500" fill="url(#waves)" />
          
          <!-- 航行路径 -->
          <g class="sailing-paths">
            <path 
              v-for="path in sailingPaths" 
              :key="path.id"
              :d="path.d"
              stroke="#66ffcc"
              stroke-width="2"
              stroke-dasharray="5,5"
              fill="none"
              opacity="0.6"
            />
          </g>
          
          <!-- 地点标记 -->
          <g v-for="location in mapLocations" :key="location.id">
            <!-- 岛屿 -->
            <circle 
              v-if="location.type === 'island'"
              :cx="location.x" 
              :cy="location.y" 
              :r="location.size || 15"
              :fill="getLocationColor(location)"
              :stroke="location.current ? '#FFD700' : getLocationBorderColor(location)"
              :stroke-width="location.current ? 3 : 1"
              :class="{ 'current-location': location.current, 'clickable': location.accessible }"
              @click="selectLocation(location)"
            />
            
            <!-- 港口 -->
            <rect 
              v-if="location.type === 'port'"
              :x="location.x - 10" 
              :y="location.y - 10" 
              width="20" 
              height="20"
              :fill="getLocationColor(location)"
              :stroke="location.current ? '#FFD700' : getLocationBorderColor(location)"
              :stroke-width="location.current ? 3 : 1"
              :class="{ 'current-location': location.current, 'clickable': location.accessible }"
              @click="selectLocation(location)"
            />
            
            <!-- 危险区域 -->
            <polygon 
              v-if="location.type === 'danger'"
              :points="getDangerZonePoints(location)"
              fill="rgba(255, 0, 0, 0.2)"
              stroke="#ff4444"
              stroke-width="2"
              stroke-dasharray="3,3"
            />
            
            <!-- 船只位置 -->
            <g v-if="location.current">
              <path 
                :transform="`translate(${location.x - 12}, ${location.y - 8}) rotate(${shipRotation})`"
                d="M12,2 L22,20 L12,17 L2,20 Z" 
                fill="#FFD700" 
                stroke="#FFA500" 
                stroke-width="1"
                class="ship-icon"
              />
              <!-- 船只航迹 -->
              <circle 
                :cx="location.x" 
                :cy="location.y" 
                r="30"
                fill="none"
                stroke="#FFD700"
                stroke-width="1"
                stroke-dasharray="2,2"
                opacity="0.5"
                class="ship-wake"
              />
            </g>
            
            <!-- 地点名称 -->
            <text 
              :x="location.x" 
              :y="location.y + (location.size || 15) + 20"
              text-anchor="middle"
              :fill="location.explored ? '#66ffcc' : '#888'"
              font-size="12"
              font-family="Arial, sans-serif"
              class="location-name"
            >
              {{ location.explored ? location.name : '???' }}
            </text>
            
            <!-- 距离显示 -->
            <text 
              v-if="location.distance && viewMode === 'detailed'"
              :x="location.x" 
              :y="location.y + (location.size || 15) + 35"
              text-anchor="middle"
              fill="#888"
              font-size="10"
              font-family="Arial, sans-serif"
            >
              {{ location.distance }} 海里
            </text>
          </g>
          
          <!-- 雾气效果 -->
          <g class="fog-overlay">
            <circle 
              v-for="fog in fogAreas" 
              :key="fog.id"
              :cx="fog.x" 
              :cy="fog.y" 
              :r="fog.radius"
              fill="rgba(200, 200, 200, 0.3)"
              class="fog-area"
            />
          </g>
          
          <!-- 风向指示 -->
          <g class="wind-indicator" transform="translate(50, 50)">
            <circle cx="0" cy="0" r="25" fill="rgba(0, 50, 100, 0.8)" stroke="#66ffcc" stroke-width="1"/>
            <path 
              :transform="`rotate(${windDirection})`"
              d="M0,-20 L5,-10 L0,-5 L-5,-10 Z" 
              fill="#66ffcc"
            />
            <text x="0" y="40" text-anchor="middle" fill="#66ffcc" font-size="10">
              风向
            </text>
          </g>
        </svg>
      </div>
    </div>

    <!-- 位置信息面板 -->
    <div v-if="selectedLocation" class="location-info">
      <div class="info-header">
        <h4>{{ selectedLocation.name }}</h4>
        <el-button size="small" @click="selectedLocation = null" type="info" circle>
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
      <div class="info-content">
        <p><strong>类型:</strong> {{ getLocationTypeLabel(selectedLocation.type) }}</p>
        <p><strong>状态:</strong> {{ selectedLocation.explored ? '已探索' : '未探索' }}</p>
        <p v-if="selectedLocation.distance"><strong>距离:</strong> {{ selectedLocation.distance }} 海里</p>
        <p v-if="selectedLocation.description">{{ selectedLocation.description }}</p>
        
        <div class="location-actions" v-if="selectedLocation.accessible">
          <el-button 
            size="small" 
            type="primary"
            @click="navigateToLocation(selectedLocation)"
            :disabled="selectedLocation.current"
          >
            <el-icon><Position /></el-icon>
            {{ selectedLocation.current ? '当前位置' : '前往此地' }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'
import { 
  Location, View, ZoomIn, Aim, Close, Position 
} from '@element-plus/icons-vue'

const gameStore = useGameStore()

// 响应式数据
const viewMode = ref('overview')
const selectedLocation = ref(null)
const mapViewport = ref(null)
const isPanning = ref(false)
const lastPanPoint = ref({ x: 0, y: 0 })

const viewBox = ref({
  x: 0,
  y: 0,
  width: 800,
  height: 600
})

const shipRotation = ref(0)
const windDirection = ref(45)

// 地图数据
const mapLocations = ref([
  {
    id: 1,
    name: '起始港口',
    type: 'port',
    x: 400,
    y: 300,
    explored: true,
    accessible: true,
    current: true,
    description: '你的冒险起点，一个繁忙的贸易港口。'
  },
  {
    id: 2,
    name: '神秘岛屿',
    type: 'island',
    x: 600,
    y: 200,
    size: 20,
    explored: false,
    accessible: true,
    distance: 25,
    description: '被迷雾笼罩的神秘岛屿，传说中藏有宝藏。'
  },
  {
    id: 3,
    name: '风暴海域',
    type: 'danger',
    x: 300,
    y: 150,
    size: 40,
    explored: true,
    accessible: false,
    description: '危险的风暴区域，船只需要足够的耐久度才能通过。'
  }
])

const sailingPaths = ref([
  {
    id: 1,
    d: 'M400,300 Q500,250 600,200'
  }
])

const fogAreas = ref([
  {
    id: 1,
    x: 600,
    y: 200,
    radius: 50
  }
])

// 方法
const getLocationColor = (location) => {
  if (!location.explored) return '#444'
  
  switch (location.type) {
    case 'port': return '#66ffcc'
    case 'island': return '#90EE90'
    case 'danger': return '#ff6b6b'
    default: return '#888'
  }
}

const getLocationBorderColor = (location) => {
  if (!location.accessible) return '#666'
  return location.explored ? '#66ffcc' : '#888'
}

const getLocationTypeLabel = (type) => {
  const labels = {
    port: '港口',
    island: '岛屿',
    danger: '危险区域'
  }
  return labels[type] || '未知'
}

const getDangerZonePoints = (location) => {
  const size = location.size || 30
  const x = location.x
  const y = location.y
  return `${x-size},${y-size} ${x+size},${y-size} ${x+size},${y+size} ${x-size},${y+size}`
}

const selectLocation = (location) => {
  if (location.accessible) {
    selectedLocation.value = location
  }
}

const centerOnShip = () => {
  const currentLocation = mapLocations.value.find(loc => loc.current)
  if (currentLocation) {
    viewBox.value.x = currentLocation.x - viewBox.value.width / 2
    viewBox.value.y = currentLocation.y - viewBox.value.height / 2
  }
}

const navigateToLocation = (location) => {
  ElMessage.info(`开始前往 ${location.name}...`)
  // 这里可以调用gameStore的导航方法
  // gameStore.navigateToLocation(location.id)
}

const startPan = (event) => {
  isPanning.value = true
  lastPanPoint.value = { x: event.clientX, y: event.clientY }
}

const handlePan = (event) => {
  if (!isPanning.value) return
  
  const deltaX = event.clientX - lastPanPoint.value.x
  const deltaY = event.clientY - lastPanPoint.value.y
  
  viewBox.value.x -= deltaX
  viewBox.value.y -= deltaY
  
  lastPanPoint.value = { x: event.clientX, y: event.clientY }
}

const endPan = () => {
  isPanning.value = false
}

const handleZoom = (event) => {
  event.preventDefault()
  const zoomFactor = event.deltaY > 0 ? 1.1 : 0.9
  const newWidth = viewBox.value.width * zoomFactor
  const newHeight = viewBox.value.height * zoomFactor
  
  // 限制缩放范围
  if (newWidth > 200 && newWidth < 2000) {
    viewBox.value.width = newWidth
    viewBox.value.height = newHeight
  }
}

onMounted(() => {
  // 初始化地图位置
  centerOnShip()
  
  // 模拟风向变化
  setInterval(() => {
    windDirection.value = (windDirection.value + 1) % 360
  }, 5000)
})
</script>

<style scoped>
.sailing-map {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(0, 20, 40, 0.95);
  color: #e0e6ed;
  border-radius: 8px;
  overflow: hidden;
}

.map-header {
  padding: 16px;
  background: rgba(0, 30, 60, 0.8);
  border-bottom: 1px solid rgba(102, 255, 204, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.map-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #66ffcc;
}

.map-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.map-container {
  flex: 1;
  display: flex;
  position: relative;
  overflow: hidden;
}

.map-legend {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(0, 30, 60, 0.9);
  padding: 12px;
  border-radius: 6px;
  border: 1px solid rgba(102, 255, 204, 0.3);
  z-index: 10;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 12px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 1px solid #66ffcc;
}

.legend-dot.current {
  background: #FFD700;
  border-color: #FFA500;
}

.legend-dot.explored {
  background: #66ffcc;
}

.legend-dot.unknown {
  background: #444;
}

.legend-dot.danger {
  background: #ff6b6b;
  border-color: #ff4444;
}

.map-viewport {
  flex: 1;
  cursor: grab;
}

.map-viewport:active {
  cursor: grabbing;
}

.sea-map {
  width: 100%;
  height: 100%;
}

.clickable {
  cursor: pointer;
  transition: all 0.3s ease;
}

.clickable:hover {
  filter: brightness(1.2);
}

.ship-icon {
  animation: float 3s ease-in-out infinite;
}

.ship-wake {
  animation: pulse 2s ease-in-out infinite;
}

.location-name {
  pointer-events: none;
}

.wind-indicator {
  pointer-events: none;
}

.location-info {
  position: absolute;
  bottom: 16px;
  right: 16px;
  width: 280px;
  background: rgba(0, 30, 60, 0.95);
  border: 1px solid rgba(102, 255, 204, 0.3);
  border-radius: 8px;
  padding: 16px;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.info-header h4 {
  margin: 0;
  color: #66ffcc;
}

.info-content p {
  margin: 6px 0;
  font-size: 14px;
}

.location-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.8; }
}
</style>
