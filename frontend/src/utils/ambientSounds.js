// 简化的音效管理器 - 无需音频文件，避免兼容性问题
class AmbientSoundManager {
  constructor() {
    this.enabled = false // 默认禁用，避免音频问题
    this.volume = 0.3
    this.currentAmbient = null
    console.log('🎵 音效系统已初始化（静音模式）')
  }

  // 播放环境音 - 静音模式
  playAmbient(soundName, options = {}) {
    console.log(`🎵 播放环境音: ${soundName}`, options)
    return null
  }

  // 停止当前环境音
  stopAmbient() {
    console.log('🔇 停止环境音')
  }

  // 切换环境音
  switchAmbient(soundName, options = {}) {
    console.log(`🔄 切换环境音: ${soundName}`, options)
  }

  // 设置主音量
  setVolume(volume) {
    this.volume = Math.max(0, Math.min(1, volume))
    console.log(`🔊 设置音量: ${Math.round(this.volume * 100)}%`)
  }

  // 启用/禁用音效
  setEnabled(enabled) {
    this.enabled = enabled
    console.log(`🎵 音效${enabled ? '启用' : '禁用'}`)
  }

  // 根据天气设置环境音
  setWeatherAmbient(weather) {
    console.log(`🌊 设置天气音效: ${weather}`)
  }

  // 根据时间设置环境音
  setTimeAmbient(timeOfDay) {
    console.log(`🕐 设置时间音效: ${timeOfDay}`)
  }

  // 播放交互音效
  playInteractionSound(type) {
    console.log(`🎯 播放交互音效: ${type}`)
  }
}

// 创建全局实例
export const ambientSounds = new AmbientSoundManager()
export default ambientSounds
