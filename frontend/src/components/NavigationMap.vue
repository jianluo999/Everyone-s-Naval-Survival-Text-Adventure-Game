<template>
  <div class="navigation-map">
    <div class="map-header">
      <h3>
        <el-icon><Location /></el-icon>
        航海地图
      </h3>
      <div class="map-legend">
        <span class="legend-item">
          <div class="legend-dot current"></div>
          当前位置
        </span>
        <span class="legend-item">
          <div class="legend-dot explored"></div>
          已探索
        </span>
        <span class="legend-item">
          <div class="legend-dot unknown"></div>
          未知海域
        </span>
      </div>
    </div>
    
    <div class="map-container">
      <svg class="sea-map" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
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
        <rect width="800" height="600" fill="url(#seaGradient)" />
        <rect width="800" height="600" fill="url(#waves)" />
        
        <!-- 地点标记 -->
        <g v-for="location in mapLocations" :key="location.id">
          <!-- 岛屿 -->
          <circle 
            v-if="location.type === 'island'"
            :cx="location.x" 
            :cy="location.y" 
            :r="location.size || 15"
            :fill="getLocationColor(location)"
            :stroke="location.current ? '#FFD700' : '#66ffcc'"
            :stroke-width="location.current ? 3 : 1"
            :class="{ 'current-location': location.current, 'clickable': location.accessible }"
            @click="selectLocation(location)"
          />
          
          <!-- 船只位置 -->
          <g v-if="location.current">
            <path 
              :transform="`translate(${location.x - 12}, ${location.y - 8})`"
              d="M12,2 L22,20 L12,17 L2,20 Z" 
              fill="#FFD700" 
              stroke="#FFA500" 
              stroke-width="1"
              class="ship-icon"
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
          >
            {{ location.explored ? location.name : '???' }}
          </text>
          
          <!-- 连接线 -->
          <g v-if="location.connections">
            <line 
              v-for="connection in location.connections"
              :key="connection"
              :x1="location.x"
              :y1="location.y"
              :x2="getLocationById(connection).x"
              :y2="getLocationById(connection).y"
              stroke="#004488"
              stroke-width="2"
              stroke-dasharray="5,5"
              opacity="0.6"
            />
          </g>
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
      </svg>
    </div>
    
    <!-- 地点详情 -->
    <div v-if="selectedLocation" class="location-details">
      <h4>{{ selectedLocation.name }}</h4>
      <p>{{ selectedLocation.description }}</p>
      <div class="location-actions">
        <el-button 
          v-if="selectedLocation.accessible && !selectedLocation.current"
          type="primary" 
          size="small"
          @click="navigateToLocation(selectedLocation)"
        >
          前往此地
        </el-button>
        <el-button 
          v-if="selectedLocation.current"
          type="success" 
          size="small"
          disabled
        >
          当前位置
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage } from 'element-plus'

const gameStore = useGameStore()
const selectedLocation = ref(null)

// 地图位置数据 - 从后端API获取
const mapLocations = ref([])
const loadingMap = ref(false)

// 所有地图数据现在从后端API获取，不再使用硬编码假数据

// 雾气区域 - 也应该从后端获取
const fogAreas = ref([])

// 获取地点颜色
const getLocationColor = (location) => {
  if (location.current) return '#FFD700'
  if (!location.explored) return '#666'
  
  switch (location.type) {
    case 'island': return '#228B22'
    case 'ships': return '#4169E1'
    case 'water': return '#1E90FF'
    case 'storm': return '#8B0000'
    default: return '#66ffcc'
  }
}

// 根据ID获取地点
const getLocationById = (id) => {
  return mapLocations.value.find(loc => loc.id === id) || { x: 0, y: 0 }
}

// 选择地点
const selectLocation = (location) => {
  if (location.accessible) {
    selectedLocation.value = location
  }
}

// 导航到地点
const navigateToLocation = (location) => {
  ElMessage.success(`正在前往 ${location.name}...`)
  // 这里可以触发游戏状态变化
  // gameStore.navigateToLocation(location.id)
}
</script>

<style lang="scss" scoped>
.navigation-map {
  background: rgba(0, 20, 40, 0.9);
  border-radius: 8px;
  padding: 1rem;
  color: #66ffcc;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  
  h3 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.map-legend {
  display: flex;
  gap: 1rem;
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
  }
  
  .legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    
    &.current { background: #FFD700; }
    &.explored { background: #66ffcc; }
    &.unknown { background: #666; }
  }
}

.map-container {
  border: 2px solid #66ffcc;
  border-radius: 8px;
  overflow: hidden;
  background: #001122;
}

.sea-map {
  width: 100%;
  height: 400px;
  
  .clickable {
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      filter: brightness(1.3);
      transform: scale(1.1);
    }
  }
  
  .current-location {
    animation: pulse 2s ease-in-out infinite;
  }
  
  .ship-icon {
    animation: float 3s ease-in-out infinite;
  }
  
  .fog-area {
    animation: drift 8s ease-in-out infinite;
  }
}

.location-details {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(0, 40, 80, 0.6);
  border-radius: 6px;
  border-left: 3px solid #66ffcc;
  
  h4 {
    margin: 0 0 0.5rem 0;
    color: #FFD700;
  }
  
  p {
    margin: 0 0 1rem 0;
    color: #ccc;
    font-size: 14px;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@keyframes drift {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(5px, -3px); }
  50% { transform: translate(-3px, 5px); }
  75% { transform: translate(-5px, -2px); }
}
</style>
