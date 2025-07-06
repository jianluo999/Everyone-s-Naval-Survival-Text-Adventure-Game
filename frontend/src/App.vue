<template>
  <div id="app" class="deep-sea-app">
    <div class="tentacle-decoration left-tentacle"></div>
    <div class="tentacle-decoration right-tentacle"></div>
    <div class="deep-sea-bubbles">
      <div class="bubble" v-for="i in 10" :key="i"></div>
    </div>
    <router-view class="app-content" />
  </div>
</template>

<script setup>
// 深海恐怖风格主应用组件
import { onMounted, onUnmounted } from 'vue'

// 深海环境音效（如果需要的话）
let ambientSounds = null

onMounted(() => {
  // 添加深海环境效果
  document.body.classList.add('deep-sea-mode')
  
  // 可以在这里添加深海音效
  // ambientSounds = new Audio('/sounds/deep-sea-ambient.mp3')
  // ambientSounds.loop = true
  // ambientSounds.volume = 0.3
  // ambientSounds.play()
})

onUnmounted(() => {
  document.body.classList.remove('deep-sea-mode')
  
  // 清理音效
  if (ambientSounds) {
    ambientSounds.pause()
    ambientSounds = null
  }
})
</script>

<style lang="scss">
#app {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.deep-sea-app {
  position: relative;
  min-height: 100vh;
  
  // 深海触手装饰
  .tentacle-decoration {
    position: fixed;
    width: 100px;
    height: 100vh;
    background: linear-gradient(45deg, 
      rgba(0, 20, 40, 0.7) 0%, 
      rgba(0, 40, 80, 0.5) 25%, 
      rgba(0, 60, 120, 0.3) 50%, 
      rgba(0, 40, 80, 0.5) 75%, 
      rgba(0, 20, 40, 0.7) 100%);
    z-index: 0;
    opacity: 0.6;
    animation: tentacle-wave 8s ease-in-out infinite;
    
    &.left-tentacle {
      left: -50px;
      transform: rotate(-15deg);
      animation-delay: -2s;
    }
    
    &.right-tentacle {
      right: -50px;
      transform: rotate(15deg);
      animation-delay: -4s;
    }
    
    &::before {
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      background: repeating-linear-gradient(
        90deg,
        transparent,
        transparent 10px,
        rgba(102, 255, 204, 0.1) 10px,
        rgba(102, 255, 204, 0.1) 12px
      );
      animation: waveEffect 6s ease-in-out infinite;
    }
  }
  
  // 深海气泡效果
  .deep-sea-bubbles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
    
    .bubble {
      position: absolute;
      width: 20px;
      height: 20px;
      background: radial-gradient(circle, rgba(102, 255, 204, 0.3) 0%, transparent 70%);
      border-radius: 50%;
      animation: bubble-float 10s linear infinite;
      
      &:nth-child(1) {
        left: 10%;
        animation-delay: 0s;
        animation-duration: 8s;
      }
      
      &:nth-child(2) {
        left: 20%;
        animation-delay: 2s;
        animation-duration: 12s;
        width: 15px;
        height: 15px;
      }
      
      &:nth-child(3) {
        left: 30%;
        animation-delay: 4s;
        animation-duration: 10s;
      }
      
      &:nth-child(4) {
        left: 40%;
        animation-delay: 6s;
        animation-duration: 9s;
        width: 25px;
        height: 25px;
      }
      
      &:nth-child(5) {
        left: 50%;
        animation-delay: 8s;
        animation-duration: 11s;
      }
      
      &:nth-child(6) {
        left: 60%;
        animation-delay: 1s;
        animation-duration: 13s;
        width: 18px;
        height: 18px;
      }
      
      &:nth-child(7) {
        left: 70%;
        animation-delay: 3s;
        animation-duration: 8s;
      }
      
      &:nth-child(8) {
        left: 80%;
        animation-delay: 5s;
        animation-duration: 10s;
        width: 12px;
        height: 12px;
      }
      
      &:nth-child(9) {
        left: 90%;
        animation-delay: 7s;
        animation-duration: 9s;
      }
      
      &:nth-child(10) {
        left: 85%;
        animation-delay: 9s;
        animation-duration: 14s;
        width: 22px;
        height: 22px;
      }
    }
  }
  
  // 主要内容区域
  .app-content {
    position: relative;
    z-index: 2;
    min-height: calc(100vh - 80px);
  }
}

// 深海模式下的body样式
body.deep-sea-mode {
  // 深海光标
  cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="2" fill="%2366ffcc" opacity="0.8"/><circle cx="12" cy="12" r="8" fill="none" stroke="%2366ffcc" stroke-width="1" opacity="0.3"/></svg>'), auto;
  
  // 防止文本选择时的默认蓝色
  ::selection {
    background: rgba(102, 255, 204, 0.3);
    color: #66ffcc;
  }
  
  ::-moz-selection {
    background: rgba(102, 255, 204, 0.3);
    color: #66ffcc;
  }
}

// 深海气泡动画
@keyframes bubble-float {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) scale(1);
    opacity: 0;
  }
}

// 深海触手波动
@keyframes tentacle-wave {
  0%, 100% { 
    transform: rotateZ(0deg) scaleY(1);
  }
  25% { 
    transform: rotateZ(2deg) scaleY(1.05);
  }
  50% { 
    transform: rotateZ(0deg) scaleY(1.1);
  }
  75% { 
    transform: rotateZ(-2deg) scaleY(1.05);
  }
}

// 深海发光效果
@keyframes eldritch-glow {
  0%, 100% { 
    text-shadow: 0 0 10px rgba(102, 255, 204, 0.8);
    opacity: 0.8;
  }
  50% { 
    text-shadow: 
      0 0 20px rgba(102, 255, 204, 1), 
      0 0 30px rgba(0, 255, 127, 0.8),
      0 0 40px rgba(102, 255, 204, 0.6);
    opacity: 1;
  }
}

// 深海恐怖文本效果
.eldritch-text {
  font-family: 'Creepster', 'Chiller', cursive;
  animation: eldritch-glow 3s ease-in-out infinite;
  letter-spacing: 1px;
}

// 响应式适配
@media (max-width: 768px) {
  .deep-sea-app {
    .tentacle-decoration {
      width: 50px;
      
      &.left-tentacle {
        left: -25px;
      }
      
      &.right-tentacle {
        right: -25px;
      }
    }
  }
}
</style> 