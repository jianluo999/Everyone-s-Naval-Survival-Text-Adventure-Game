<template>
  <transition name="modal-fade">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <div class="modal-header">
          <h2>获得新鱼种！</h2>
          <button class="close-button" @click="close">&times;</button>
        </div>
        <div class="modal-body" v-if="fish">
          <div class="fish-image-container">
            <img
              :src="imagePath"
              :alt="fish.name"
              class="fish-image"
              @error="handleImageError"
              @load="handleImageLoad"
            />
            <div v-if="imageError" class="image-error">
              <p>图片加载失败</p>
              <p>{{ fish.imageName }}</p>
            </div>
          </div>
          <div class="fish-details">
            <h3 class="fish-name">{{ fish.name }}</h3>
            <p class="fish-rarity" :class="rarityClass">{{ fish.rarity }}</p>
            <p class="fish-description">{{ fish.description }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="action-button" @click="close">收入囊中</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed, ref } from 'vue';

const imageError = ref(false);

const props = defineProps({
  fish: {
    type: Object,
    default: null,
  },
  visible: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};

const imagePath = computed(() => {
  console.log('Fish data:', props.fish); // 调试日志

  if (props.fish && props.fish.imageName) {
    console.log('Loading image:', props.fish.imageName); // 调试日志

    // 使用动态导入的方式加载图片
    const imageName = props.fish.imageName;
    try {
      // 直接使用相对路径，Vite 会处理资源
      return `/src/assets/images/fish/generated/${imageName}`;
    } catch (error) {
      console.warn('无法加载鱼类图片:', imageName, error);
    }
  }

  // 返回默认的占位符 SVG
  return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImZpc2hHcmFkaWVudCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+PHN0b3Agb2Zmc2V0PSIwJSIgc3R5bGU9InN0b3AtY29sb3I6IzRhOTBlMjtzdG9wLW9wYWNpdHk6MSIgLz48c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiMyYzVhYTA7c3RvcC1vcGFjaXR5OjEiIC8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PGVsbGlwc2UgY3g9IjEwMCIgY3k9Ijc1IiByeD0iNjAiIHJ5PSIzMCIgZmlsbD0idXJsKCNmaXNoR3JhZGllbnQpIiBzdHJva2U9IiMxZTNhOGEiIHN0cm9rZS13aWR0aD0iMiIvPjxwb2x5Z29uIHBvaW50cz0iNDAsNzUgMTAsNTUgMTAsOTUiIGZpbGw9InVybCgjZmlzaEdyYWRpZW50KSIgc3Ryb2tlPSIjMWUzYThhIiBzdHJva2Utd2lkdGg9IjIiLz48Y2lyY2xlIGN4PSIxMzAiIGN5PSI2NSIgcj0iOCIgZmlsbD0id2hpdGUiIHN0cm9rZT0iIzFlM2E4YSIgc3Ryb2tlLXdpZHRoPSIxIi8+PGNpcmNsZSBjeD0iMTMyIiBjeT0iNjMiIHI9IjQiIGZpbGw9ImJsYWNrIi8+PC9zdmc+';
});

const rarityClass = computed(() => {
  if (!props.fish || !props.fish.rarity) return 'common';
  return props.fish.rarity.toLowerCase();
});

const handleImageError = (event) => {
  console.error('图片加载失败:', event.target.src);
  imageError.value = true;
};

const handleImageLoad = (event) => {
  console.log('图片加载成功:', event.target.src);
  imageError.value = false;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.4s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  font-family: 'ZCOOL KuaiLe', cursive;
  background: url('/src/assets/images/background/parchment.jpg') no-repeat center center;
  background-size: cover;
  color: #4a2c0b;
  border: 10px solid transparent;
  border-image: url('/src/assets/images/background/wood-frame.png') 30 round;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  width: 90%;
  max-width: 500px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 15px 25px;
  border-bottom: 2px solid #7a5c3b;
  text-align: center;
  position: relative;
}

.modal-header h2 {
  margin: 0;
  font-size: 2em;
  color: #5a3c1b;
  text-shadow: 1px 1px 0px #c5a98a;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 2.5em;
  color: #7a5c3b;
  cursor: pointer;
  transition: transform 0.2s;
}

.close-button:hover {
  transform: scale(1.2);
  color: #5a3c1b;
}

.modal-body {
  padding: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.fish-image-container {
  width: 100%;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid #c5a98a;
  margin-bottom: 20px;
  box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
}

.fish-image {
  width: 100%;
  height: auto;
  display: block;
}

.fish-details {
  text-align: center;
}

.fish-name {
  font-size: 2.2em;
  margin: 0 0 10px 0;
  color: #3a1c0b;
}

.fish-rarity {
  font-size: 1.2em;
  font-weight: bold;
  margin: 0 0 15px 0;
  padding: 5px 15px;
  display: inline-block;
  border-radius: 15px;
  color: white;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.fish-rarity.common { background-color: #6c757d; }
.fish-rarity.uncommon { background-color: #28a745; }
.fish-rarity.rare { background-color: #007bff; }
.fish-rarity.legendary { background-color: #9333ea; }


.fish-description {
  font-size: 1.1em;
  line-height: 1.6;
  text-align: justify;
  color: #4a2c0b;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 2px solid #7a5c3b;
  display: flex;
  justify-content: center;
}

.action-button {
  font-family: 'ZCOOL KuaiLe', cursive;
  background-color: #8B4513;
  color: #f0e6d2;
  border: 2px solid #5a3c1b;
  padding: 12px 28px;
  font-size: 1.5em;
  cursor: pointer;
  border-radius: 5px;
  transition: all 0.3s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}

.action-button:hover {
  background-color: #A0522D;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0,0,0,0.3);
}
</style> 