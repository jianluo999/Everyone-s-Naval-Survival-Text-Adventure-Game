// 音效管理器
class AudioManager {
  constructor() {
    this.sounds = new Map()
    this.enabled = true
    this.volume = 0.5
    this.loadSounds()
  }

  // 加载音效文件
  loadSounds() {
    const soundFiles = {
      click: '/sounds/click.mp3',
      choice: '/sounds/choice.mp3',
      battle: '/sounds/battle.mp3',
      sanityLoss: '/sounds/sanity-loss.mp3',
      ambient: '/sounds/deep-sea-ambient.mp3',
      notification: '/sounds/notification.mp3'
    }

    Object.entries(soundFiles).forEach(([key, path]) => {
      const audio = new Audio(path)
      audio.volume = this.volume
      audio.preload = 'auto'
      this.sounds.set(key, audio)
    })
  }

  // 播放音效
  play(soundName, volume = 1) {
    if (!this.enabled) return

    const sound = this.sounds.get(soundName)
    if (sound) {
      sound.volume = this.volume * volume
      sound.currentTime = 0
      sound.play().catch(e => console.log('Audio play failed:', e))
    }
  }

  // 设置音量
  setVolume(volume) {
    this.volume = Math.max(0, Math.min(1, volume))
    this.sounds.forEach(sound => {
      sound.volume = this.volume
    })
  }

  // 启用/禁用音效
  setEnabled(enabled) {
    this.enabled = enabled
    if (!enabled) {
      this.sounds.forEach(sound => sound.pause())
    }
  }

  // 播放环境音
  playAmbient() {
    const ambient = this.sounds.get('ambient')
    if (ambient && this.enabled) {
      ambient.loop = true
      ambient.volume = this.volume * 0.3
      ambient.play().catch(e => console.log('Ambient play failed:', e))
    }
  }

  // 停止环境音
  stopAmbient() {
    const ambient = this.sounds.get('ambient')
    if (ambient) {
      ambient.pause()
      ambient.currentTime = 0
    }
  }
}

export const audioManager = new AudioManager()
export default audioManager
