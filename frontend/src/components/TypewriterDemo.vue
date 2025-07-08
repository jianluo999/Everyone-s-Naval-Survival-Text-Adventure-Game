<template>
  <div class="typewriter-demo">
    <h2>打字机效果演示</h2>
    
    <div class="speed-controls">
      <label>打字速度：</label>
      <el-select v-model="speed" @change="restartDemo" style="width: 100px">
        <el-option label="慢" :value="80" />
        <el-option label="中" :value="40" />
        <el-option label="快" :value="25" />
        <el-option label="极快" :value="10" />
        <el-option label="瞬间" :value="1" />
      </el-select>
      <el-button @click="restartDemo" type="primary" size="small">重新开始</el-button>
    </div>
    
    <div class="demo-content">
      <div class="story-paragraph">
        <span
          v-for="(char, index) in demoText"
          :key="index"
          class="typewriter-char"
          :class="{ 'visible': index < currentCharIndex }"
        >{{ char }}</span>
        <span v-if="isActive" class="typewriter-cursor"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const speed = ref(25)
const currentCharIndex = ref(0)
const isActive = ref(false)
const timer = ref(null)

const demoText = "你立刻打开舱门，想要看清楚外面的情况。海风轻抚着你的脸庞，带来咸腥的味道。远处的海平线上，似乎有什么东西在移动..."

const startTypewriter = () => {
  if (timer.value) {
    clearInterval(timer.value)
  }
  
  currentCharIndex.value = 0
  isActive.value = true
  
  timer.value = setInterval(() => {
    currentCharIndex.value++
    
    if (currentCharIndex.value >= demoText.length) {
      clearInterval(timer.value)
      isActive.value = false
    }
  }, speed.value)
}

const restartDemo = () => {
  startTypewriter()
}

onMounted(() => {
  startTypewriter()
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<style lang="scss" scoped>
.typewriter-demo {
  padding: 2rem;
  background: linear-gradient(135deg, #0c1445 0%, #1a2b5c 100%);
  min-height: 100vh;
  color: white;
  
  h2 {
    color: #66ffcc;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 0 0 10px rgba(102, 255, 204, 0.5);
  }
  
  .speed-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
    
    label {
      color: #66ffcc;
    }
  }
  
  .demo-content {
    max-width: 800px;
    margin: 0 auto;
    
    .story-paragraph {
      font-size: 1.2rem;
      line-height: 1.8;
      color: #ffffff;
      text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
      font-family: 'Consolas', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
      
      .typewriter-char {
        opacity: 0;
        display: inline;
        transition: none;
        
        &.visible {
          opacity: 1;
          animation: typewriter-appear 0.05s ease-out forwards;
        }
      }
      
      .typewriter-cursor {
        display: inline-block;
        width: 2px;
        height: 1.2em;
        background-color: #66ffcc;
        animation: typewriter-blink 0.6s infinite;
        margin-left: 2px;
        box-shadow: 0 0 5px #66ffcc;
      }
    }
  }
}

@keyframes typewriter-appear {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes typewriter-blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}
</style>
