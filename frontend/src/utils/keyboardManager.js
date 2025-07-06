// 快捷键管理器
class KeyboardManager {
  constructor() {
    this.shortcuts = new Map()
    this.enabled = true
    this.setupDefaultShortcuts()
    this.bindEvents()
  }

  // 设置默认快捷键
  setupDefaultShortcuts() {
    this.shortcuts.set('1', { action: 'selectChoice', param: 0, description: '选择第一个选项' })
    this.shortcuts.set('2', { action: 'selectChoice', param: 1, description: '选择第二个选项' })
    this.shortcuts.set('3', { action: 'selectChoice', param: 2, description: '选择第三个选项' })
    this.shortcuts.set('4', { action: 'selectChoice', param: 3, description: '选择第四个选项' })
    this.shortcuts.set('5', { action: 'selectChoice', param: 4, description: '选择第五个选项' })
    
    this.shortcuts.set('s', { action: 'saveGame', description: '保存游戏' })
    this.shortcuts.set('m', { action: 'toggleMap', description: '切换地图' })
    this.shortcuts.set('l', { action: 'toggleLog', description: '切换日志' })
    this.shortcuts.set('c', { action: 'toggleChat', description: '切换聊天' })
    this.shortcuts.set('h', { action: 'showHelp', description: '显示帮助' })
    
    this.shortcuts.set('Escape', { action: 'closeModal', description: '关闭弹窗' })
    this.shortcuts.set('Enter', { action: 'confirmAction', description: '确认操作' })
  }

  // 绑定键盘事件
  bindEvents() {
    document.addEventListener('keydown', (event) => {
      if (!this.enabled) return
      
      // 忽略在输入框中的按键
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return
      }

      const key = event.key
      const shortcut = this.shortcuts.get(key)
      
      if (shortcut) {
        event.preventDefault()
        this.executeAction(shortcut.action, shortcut.param)
      }
    })
  }

  // 执行快捷键动作
  executeAction(action, param) {
    const event = new CustomEvent('keyboardAction', {
      detail: { action, param }
    })
    document.dispatchEvent(event)
  }

  // 添加自定义快捷键
  addShortcut(key, action, param, description) {
    this.shortcuts.set(key, { action, param, description })
  }

  // 移除快捷键
  removeShortcut(key) {
    this.shortcuts.delete(key)
  }

  // 获取所有快捷键
  getAllShortcuts() {
    return Array.from(this.shortcuts.entries()).map(([key, config]) => ({
      key,
      ...config
    }))
  }

  // 启用/禁用快捷键
  setEnabled(enabled) {
    this.enabled = enabled
  }

  // 显示快捷键帮助
  showHelp() {
    const shortcuts = this.getAllShortcuts()
    const helpText = shortcuts.map(s => `${s.key}: ${s.description}`).join('\n')
    
    // 创建帮助弹窗
    const helpModal = document.createElement('div')
    helpModal.className = 'keyboard-help-modal'
    helpModal.innerHTML = `
      <div class="help-content">
        <h3>快捷键帮助</h3>
        <div class="shortcuts-list">
          ${shortcuts.map(s => `
            <div class="shortcut-item">
              <kbd>${s.key}</kbd>
              <span>${s.description}</span>
            </div>
          `).join('')}
        </div>
        <button onclick="this.parentElement.parentElement.remove()">关闭 (ESC)</button>
      </div>
    `
    
    // 添加样式
    helpModal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 10000;
    `
    
    document.body.appendChild(helpModal)
    
    // ESC关闭
    const closeHandler = (e) => {
      if (e.key === 'Escape') {
        helpModal.remove()
        document.removeEventListener('keydown', closeHandler)
      }
    }
    document.addEventListener('keydown', closeHandler)
  }
}

export const keyboardManager = new KeyboardManager()
export default keyboardManager
