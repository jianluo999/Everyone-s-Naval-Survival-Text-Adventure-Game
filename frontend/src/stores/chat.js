import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { Client } from '@stomp/stompjs'
import SockJS from 'sockjs-client'
import gameApi from '@/api/game'
import { ElMessage } from 'element-plus'

export const useChatStore = defineStore('chat', () => {
  // 状态
  const connected = ref(false)
  const connecting = ref(false)
  const stompClient = ref(null)
  const currentPlayer = ref('')
  
  // 消息存储
  const worldMessages = ref([])
  const regionMessages = ref([])
  const systemMessages = ref([])
  const tradeMessages = ref([])
  
  // 活跃玩家列表
  const activePlayers = ref([])
  
  // 连接状态
  const connectionStatus = computed(() => {
    if (connecting.value) return 'connecting'
    if (connected.value) return 'connected'
    return 'disconnected'
  })

  // 获取指定频道的消息
  const getChannelMessages = computed(() => (channel) => {
    switch (channel) {
      case 'world': return worldMessages.value
      case 'region': return regionMessages.value
      case 'system': return systemMessages.value
      case 'trade': return tradeMessages.value
      default: return []
    }
  })

  // 连接WebSocket
  const connect = (playerName) => {
    if (connected.value || connecting.value) {
      console.log('🔗 [CHAT] 已连接或正在连接中')
      return
    }

    connecting.value = true
    currentPlayer.value = playerName

    try {
      // 创建STOMP客户端
      const client = new Client({
        webSocketFactory: () => new SockJS('http://localhost:8080/api/ws'),
        connectHeaders: {
          login: playerName,
        },
        debug: (str) => {
          console.log('🔍 [STOMP]', str)
        },
        reconnectDelay: 5000,
        heartbeatIncoming: 4000,
        heartbeatOutgoing: 4000,
      })

      // 连接成功回调
      client.onConnect = (frame) => {
        console.log('✅ [CHAT] WebSocket连接成功:', frame)
        connected.value = true
        connecting.value = false
        
        // 订阅各个频道
        subscribeToChannels(client)
        
        // 发送用户加入消息
        sendUserJoinMessage(client, playerName)
        
        // 加载聊天历史
        loadChatHistory()
        
        ElMessage.success('聊天系统连接成功')
      }

      // 连接错误回调
      client.onStompError = (frame) => {
        console.error('❌ [CHAT] WebSocket连接错误:', frame.headers['message'])
        console.error('详细信息:', frame.body)
        connected.value = false
        connecting.value = false
        ElMessage.error('聊天系统连接失败')
      }

      // 连接断开回调
      client.onDisconnect = () => {
        console.log('🔌 [CHAT] WebSocket连接断开')
        connected.value = false
        connecting.value = false
      }

      stompClient.value = client
      client.activate()

    } catch (error) {
      console.error('❌ [CHAT] 连接失败:', error)
      connecting.value = false
      ElMessage.error('聊天系统连接失败')
    }
  }

  // 订阅频道
  const subscribeToChannels = (client) => {
    // 订阅世界频道
    client.subscribe('/topic/chat/world', (message) => {
      const chatMessage = JSON.parse(message.body)
      worldMessages.value.push(chatMessage)
      console.log('🌍 [CHAT] 收到世界消息:', chatMessage)
    })

    // 订阅区域频道
    client.subscribe('/topic/chat/region', (message) => {
      const chatMessage = JSON.parse(message.body)
      regionMessages.value.push(chatMessage)
      console.log('🗺️ [CHAT] 收到区域消息:', chatMessage)
    })

    // 订阅系统频道
    client.subscribe('/topic/chat/system', (message) => {
      const chatMessage = JSON.parse(message.body)
      systemMessages.value.push(chatMessage)
      console.log('⚙️ [CHAT] 收到系统消息:', chatMessage)
    })

    // 订阅交易频道
    client.subscribe('/topic/chat/trade', (message) => {
      const chatMessage = JSON.parse(message.body)
      tradeMessages.value.push(chatMessage)
      console.log('💰 [CHAT] 收到交易消息:', chatMessage)
    })

    // 订阅公共频道（用于用户加入/离开通知）
    client.subscribe('/topic/public', (message) => {
      const chatMessage = JSON.parse(message.body)
      if (chatMessage.messageType === 'SYSTEM') {
        systemMessages.value.push(chatMessage)
      }
      console.log('📢 [CHAT] 收到公共消息:', chatMessage)
    })
  }

  // 发送用户加入消息
  const sendUserJoinMessage = (client, playerName) => {
    const joinMessage = {
      playerName: playerName,
      content: '',
      channel: 'SYSTEM',
      messageType: 'SYSTEM'
    }
    
    client.publish({
      destination: '/app/chat.addUser',
      body: JSON.stringify(joinMessage)
    })
  }

  // 发送消息
  const sendMessage = (content, channel = 'WORLD') => {
    if (!connected.value || !stompClient.value) {
      ElMessage.error('聊天系统未连接')
      return false
    }

    if (!content.trim()) {
      ElMessage.warning('消息内容不能为空')
      return false
    }

    const message = {
      playerName: currentPlayer.value,
      content: content.trim(),
      channel: channel.toUpperCase(),
      messageType: 'NORMAL'
    }

    try {
      stompClient.value.publish({
        destination: '/app/chat.sendMessage',
        body: JSON.stringify(message)
      })
      
      console.log('📤 [CHAT] 消息已发送:', message)
      return true
    } catch (error) {
      console.error('❌ [CHAT] 发送消息失败:', error)
      ElMessage.error('发送消息失败')
      return false
    }
  }

  // 加载聊天历史
  const loadChatHistory = async () => {
    try {
      const channels = ['world', 'region', 'system', 'trade']
      
      for (const channel of channels) {
        const response = await gameApi.getChatHistory(channel, 0, 20)
        if (response.data.success) {
          const messages = response.data.messages.reverse() // 按时间正序排列
          
          switch (channel) {
            case 'world':
              worldMessages.value = messages
              break
            case 'region':
              regionMessages.value = messages
              break
            case 'system':
              systemMessages.value = messages
              break
            case 'trade':
              tradeMessages.value = messages
              break
          }
        }
      }
      
      console.log('📚 [CHAT] 聊天历史加载完成')
    } catch (error) {
      console.error('❌ [CHAT] 加载聊天历史失败:', error)
    }
  }

  // 加载活跃玩家
  const loadActivePlayers = async () => {
    try {
      const response = await gameApi.getActivePlayers()
      if (response.data.success) {
        activePlayers.value = response.data.players
      }
    } catch (error) {
      console.error('❌ [CHAT] 加载活跃玩家失败:', error)
    }
  }

  // 断开连接
  const disconnect = () => {
    if (stompClient.value) {
      stompClient.value.deactivate()
      stompClient.value = null
    }
    connected.value = false
    connecting.value = false
    currentPlayer.value = ''
    console.log('🔌 [CHAT] 已断开连接')
  }

  // 清空消息
  const clearMessages = (channel) => {
    switch (channel) {
      case 'world':
        worldMessages.value = []
        break
      case 'region':
        regionMessages.value = []
        break
      case 'system':
        systemMessages.value = []
        break
      case 'trade':
        tradeMessages.value = []
        break
      case 'all':
        worldMessages.value = []
        regionMessages.value = []
        systemMessages.value = []
        tradeMessages.value = []
        break
    }
  }

  return {
    // 状态
    connected,
    connecting,
    connectionStatus,
    currentPlayer,
    activePlayers,
    
    // 消息
    worldMessages,
    regionMessages,
    systemMessages,
    tradeMessages,
    getChannelMessages,
    
    // 方法
    connect,
    disconnect,
    sendMessage,
    loadChatHistory,
    loadActivePlayers,
    clearMessages
  }
})
