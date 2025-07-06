<template>
  <div class="enhanced-trading">
    <div class="trading-header">
      <h3>🏪 交易中心</h3>
      <div class="trading-tabs">
        <el-tabs v-model="activeTab" class="trading-tabs-inner">
          <el-tab-pane label="交易大厅" name="market">
            <template #label>
              <span class="tab-label">
                <el-icon><Shop /></el-icon>
                交易大厅
              </span>
            </template>
          </el-tab-pane>

          <el-tab-pane label="私人交易" name="private">
            <template #label>
              <span class="tab-label">
                <el-icon><ChatDotRound /></el-icon>
                私人交易
                <el-badge v-if="privateTrades.length > 0" :value="privateTrades.length" class="trade-badge" />
              </span>
            </template>
          </el-tab-pane>

          <el-tab-pane label="好友列表" name="friends">
            <template #label>
              <span class="tab-label">
                <el-icon><User /></el-icon>
                好友
                <el-badge v-if="onlineFriends.length > 0" :value="onlineFriends.length" class="friend-badge" />
              </span>
            </template>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>

    <!-- 交易大厅 -->
    <div v-if="activeTab === 'market'" class="market-panel">
      <div class="market-filters">
        <el-select v-model="selectedCategory" placeholder="选择分类" size="small">
          <el-option label="全部" value="all" />
          <el-option label="武器" value="weapons" />
          <el-option label="消耗品" value="consumables" />
          <el-option label="材料" value="materials" />
          <el-option label="遗物" value="relics" />
        </el-select>

        <el-select v-model="selectedQuality" placeholder="选择品质" size="small">
          <el-option label="全部品质" value="all" />
          <el-option label="普通" value="common" />
          <el-option label="良品" value="good" />
          <el-option label="精品" value="excellent" />
          <el-option label="史诗" value="epic" />
        </el-select>

        <el-button type="primary" size="small" @click="showCreateTrade">
          发布交易
        </el-button>
      </div>

      <div class="market-listings">
        <div
          v-for="listing in filteredListings"
          :key="listing.id"
          class="listing-item"
          :class="listing.quality"
        >
          <div class="listing-header">
            <div class="seller-info">
              <span class="seller-name">{{ listing.sellerName }}</span>
              <span class="seller-ship">{{ listing.sellerShip }}</span>
            </div>
            <div class="listing-time">{{ formatTime(listing.createdAt) }}</div>
          </div>

          <div class="listing-content">
            <div class="offering-section">
              <h5>🏪 出售</h5>
              <div class="items-grid">
                <div
                  v-for="item in listing.offering"
                  :key="item.id"
                  class="item-card"
                  @click="showItemDetails(item)"
                >
                  <div class="item-icon">{{ item.icon }}</div>
                  <div class="item-info">
                    <div class="item-name">{{ item.name }}</div>
                    <div class="item-amount">x{{ item.amount }}</div>
                  </div>
                  <div class="item-quality" :class="item.quality">
                    {{ getQualityText(item.quality) }}
                  </div>
                </div>
              </div>
            </div>

            <div class="wanting-section" v-if="listing.wanting.length > 0">
              <h5>🛒 求购</h5>
              <div class="wanted-items">
                <span
                  v-for="wanted in listing.wanting"
                  :key="wanted"
                  class="wanted-item"
                >
                  {{ wanted }}
                </span>
              </div>
            </div>

            <div class="listing-actions">
              <el-button
                type="primary"
                size="small"
                @click="contactSeller(listing)"
                :disabled="listing.sellerName === currentPlayer"
              >
                联系交易
              </el-button>
              <el-button
                type="success"
                size="small"
                @click="quickTrade(listing)"
                v-if="canQuickTrade(listing)"
              >
                快速交易
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 私人交易 -->
    <div v-else-if="activeTab === 'private'" class="private-panel">
      <div class="private-trades-list">
        <div
          v-for="trade in privateTrades"
          :key="trade.id"
          class="private-trade-item"
          :class="{ 'unread': !trade.read }"
        >
          <div class="trade-header">
            <div class="trader-info">
              <span class="trader-name">{{ trade.traderName }}</span>
              <span class="trade-status" :class="trade.status">
                {{ getTradeStatusText(trade.status) }}
              </span>
            </div>
            <div class="trade-time">{{ formatTime(trade.lastUpdate) }}</div>
          </div>

          <div class="trade-preview">
            <div class="trade-offer">
              <span class="offer-label">对方提供:</span>
              <span class="offer-items">{{ trade.theirOffer.map(i => i.name).join(', ') }}</span>
            </div>
            <div class="trade-request">
              <span class="request-label">对方需要:</span>
              <span class="request-items">{{ trade.theirRequest.join(', ') }}</span>
            </div>
          </div>

          <div class="trade-actions">
            <el-button size="small" @click="openPrivateTrade(trade)">
              查看详情
            </el-button>
            <el-button
              v-if="trade.status === 'pending'"
              type="success"
              size="small"
              @click="acceptTrade(trade)"
            >
              接受
            </el-button>
            <el-button
              v-if="trade.status === 'pending'"
              type="danger"
              size="small"
              @click="rejectTrade(trade)"
            >
              拒绝
            </el-button>
          </div>
        </div>

        <div v-if="privateTrades.length === 0" class="no-trades">
          <el-icon class="empty-icon"><ChatDotRound /></el-icon>
          <p>暂无私人交易</p>
          <p class="tip">在交易大厅联系其他玩家开始交易</p>
        </div>
      </div>
    </div>

    <!-- 好友列表 -->
    <div v-else-if="activeTab === 'friends'" class="friends-panel">
      <div class="friends-header">
        <el-input
          v-model="friendSearchQuery"
          placeholder="搜索玩家名称或船只名称"
          size="small"
          class="friend-search"
        >
          <template #prepend>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-button type="primary" size="small" @click="showAddFriend">
          添加好友
        </el-button>
      </div>

      <div class="friends-list">
        <div class="online-friends" v-if="onlineFriends.length > 0">
          <h4>🟢 在线好友 ({{ onlineFriends.length }})</h4>
          <div
            v-for="friend in onlineFriends"
            :key="friend.id"
            class="friend-item online"
          >
            <div class="friend-avatar">{{ friend.avatar }}</div>
            <div class="friend-info">
              <div class="friend-name">{{ friend.name }}</div>
              <div class="friend-ship">{{ friend.shipName }}</div>
              <div class="friend-status">{{ friend.status }}</div>
            </div>
            <div class="friend-actions">
              <el-button size="small" @click="startPrivateChat(friend)">
                私聊
              </el-button>
              <el-button size="small" @click="inviteToTrade(friend)">
                交易
              </el-button>
            </div>
          </div>
        </div>

        <div class="offline-friends" v-if="offlineFriends.length > 0">
          <h4>⚫ 离线好友 ({{ offlineFriends.length }})</h4>
          <div
            v-for="friend in offlineFriends"
            :key="friend.id"
            class="friend-item offline"
          >
            <div class="friend-avatar">{{ friend.avatar }}</div>
            <div class="friend-info">
              <div class="friend-name">{{ friend.name }}</div>
              <div class="friend-ship">{{ friend.shipName }}</div>
              <div class="last-seen">{{ formatLastSeen(friend.lastSeen) }}</div>
            </div>
          </div>
        </div>

        <div v-if="friends.length === 0" class="no-friends">
          <el-icon class="empty-icon"><User /></el-icon>
          <p>暂无好友</p>
          <p class="tip">添加好友开始交易和聊天</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Shop, ChatDotRound, User, Search } from '@element-plus/icons-vue'

const gameStore = useGameStore()

// 响应式数据
const activeTab = ref('market')
const selectedCategory = ref('all')
const selectedQuality = ref('all')
const friendSearchQuery = ref('')
const currentPlayer = ref('杨逸') // 当前玩家名称

// 交易列表数据
const marketListings = ref([
  {
    id: 1,
    sellerName: '周黛',
    sellerShip: '光辉女神号',
    createdAt: new Date(Date.now() - 300000),
    quality: 'excellent',
    offering: [
      {
        id: 'holy_water',
        name: '圣水',
        icon: '💧',
        amount: 2,
        quality: 'excellent',
        description: '受祝福的水，可治愈多种毒素和诅咒'
      }
    ],
    wanting: ['溺亡者之怨', '布料', '海螺币'],
    status: 'active'
  },
  {
    id: 2,
    sellerName: '钢铁雄心号',
    sellerShip: '钢铁战舰',
    createdAt: new Date(Date.now() - 600000),
    quality: 'good',
    offering: [
      {
        id: 'steel',
        name: '钢铁',
        icon: '⚙️',
        amount: 50,
        quality: 'good',
        description: '高质量的钢铁材料'
      }
    ],
    wanting: ['医疗绷带', '眼球果'],
    status: 'active'
  },
  {
    id: 3,
    sellerName: '深海探险家',
    sellerShip: '探索者号',
    createdAt: new Date(Date.now() - 900000),
    quality: 'good',
    offering: [
      {
        id: 'bone_token',
        name: '白骨令牌',
        icon: '🦴',
        amount: 1,
        quality: 'excellent',
        description: '可以召唤骷髅战士的神秘令牌'
      },
      {
        id: 'serrated_dagger',
        name: '锯齿匕首',
        icon: '🗡️',
        amount: 1,
        quality: 'excellent',
        description: '锋利但短小的武器'
      }
    ],
    wanting: ['淡水', '食物', '海螺币'],
    status: 'active'
  }
])

// 私人交易数据
const privateTrades = ref([
  {
    id: 1,
    traderName: '周黛',
    status: 'pending',
    read: false,
    lastUpdate: new Date(Date.now() - 180000),
    theirOffer: [
      { name: '圣水', amount: 1 }
    ],
    theirRequest: ['溺亡者之怨', '400海螺币'],
    myOffer: [],
    myRequest: []
  }
])

// 好友数据
const friends = ref([
  {
    id: 1,
    name: '周黛',
    shipName: '光辉女神号',
    avatar: '👩‍🦳',
    status: '在交易中心',
    online: true,
    lastSeen: null
  },
  {
    id: 2,
    name: '钢铁雄心号',
    shipName: '钢铁战舰',
    avatar: '👨‍🔧',
    status: '正在航行',
    online: true,
    lastSeen: null
  },
  {
    id: 3,
    name: '深海探险家',
    shipName: '探索者号',
    avatar: '🧭',
    status: '离线',
    online: false,
    lastSeen: new Date(Date.now() - 3600000)
  }
])

// 计算属性
const filteredListings = computed(() => {
  return marketListings.value.filter(listing => {
    if (selectedCategory.value !== 'all') {
      // 这里可以根据物品类型过滤
    }
    if (selectedQuality.value !== 'all') {
      return listing.quality === selectedQuality.value
    }
    return true
  })
})

const onlineFriends = computed(() => {
  return friends.value.filter(friend => friend.online)
})

const offlineFriends = computed(() => {
  return friends.value.filter(friend => !friend.online)
})

// 方法
const getQualityText = (quality) => {
  const texts = {
    common: '普通',
    good: '良品',
    excellent: '精品',
    epic: '史诗',
    legendary: '传说'
  }
  return texts[quality] || quality
}

const getTradeStatusText = (status) => {
  const texts = {
    pending: '待处理',
    accepted: '已接受',
    rejected: '已拒绝',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const formatTime = (date) => {
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return `${Math.floor(diff / 86400000)}天前`
}

const formatLastSeen = (date) => {
  if (!date) return '从未在线'
  return `最后在线: ${formatTime(date)}`
}

const showItemDetails = (item) => {
  ElMessageBox.alert(item.description, item.name, {
    confirmButtonText: '确定'
  })
}

const contactSeller = (listing) => {
  ElMessage.info(`正在联系 ${listing.sellerName}...`)

  // 创建私人交易请求
  const newTrade = {
    id: Date.now(),
    traderName: listing.sellerName,
    status: 'draft',
    read: true,
    lastUpdate: new Date(),
    theirOffer: listing.offering,
    theirRequest: listing.wanting,
    myOffer: [],
    myRequest: []
  }

  privateTrades.value.push(newTrade)
  activeTab.value = 'private'
}

const canQuickTrade = (listing) => {
  // 检查是否有对方需要的物品
  return listing.wanting.some(wanted => {
    // 这里应该检查玩家背包
    return true // 简化处理
  })
}

const quickTrade = (listing) => {
  ElMessageBox.confirm(
    `确定要与 ${listing.sellerName} 进行快速交易吗？`,
    '快速交易',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    ElMessage.success('交易成功！')
    // 这里应该执行实际的交易逻辑
  }).catch(() => {
    // 用户取消
  })
}

const showCreateTrade = () => {
  ElMessage.info('发布交易功能开发中...')
}

const openPrivateTrade = (trade) => {
  ElMessage.info(`打开与 ${trade.traderName} 的交易窗口`)
  trade.read = true
}

const acceptTrade = (trade) => {
  trade.status = 'accepted'
  trade.lastUpdate = new Date()
  ElMessage.success(`接受了与 ${trade.traderName} 的交易`)
}

const rejectTrade = (trade) => {
  trade.status = 'rejected'
  trade.lastUpdate = new Date()
  ElMessage.info(`拒绝了与 ${trade.traderName} 的交易`)
}

const startPrivateChat = (friend) => {
  ElMessage.info(`开始与 ${friend.name} 的私聊`)
}

const inviteToTrade = (friend) => {
  ElMessage.info(`邀请 ${friend.name} 进行交易`)
}

const showAddFriend = () => {
  ElMessageBox.prompt('请输入要添加的玩家名称', '添加好友', {
    confirmButtonText: '添加',
    cancelButtonText: '取消',
    inputPattern: /^.{1,20}$/,
    inputErrorMessage: '玩家名称长度应为1-20个字符'
  }).then(({ value }) => {
    ElMessage.success(`已发送好友请求给 ${value}`)
  }).catch(() => {
    // 用户取消
  })
}

// 初始化
onMounted(() => {
  // 模拟接收新的交易请求
  setTimeout(() => {
    if (privateTrades.value.length > 0) {
      ElMessage.info('收到新的交易请求')
    }
  }, 3000)
})
</script>

<style lang="scss" scoped>
.enhanced-trading {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(243, 156, 18, 0.3);
  min-height: 600px;
}

.trading-header {
  margin-bottom: 1.5rem;

  h3 {
    color: #f39c12;
    margin: 0 0 1rem 0;
    text-align: center;
  }
}

.trading-tabs-inner {
  :deep(.el-tabs__header) {
    margin: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  :deep(.el-tabs__nav-wrap) {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 0.5rem;
    padding: 0.3rem;
  }

  :deep(.el-tabs__item) {
    color: #bbb;
    border: none;
    border-radius: 0.3rem;
    margin: 0 0.2rem;

    &.is-active {
      background: rgba(243, 156, 18, 0.2);
      color: #f39c12;
    }

    &:hover {
      color: #f39c12;
    }
  }
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.trade-badge,
.friend-badge {
  :deep(.el-badge__content) {
    background: #e74c3c;
    border: none;
  }
}

// 交易大厅样式
.market-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.market-filters {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.market-listings {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 500px;
  overflow-y: auto;
}

.listing-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
  border-left: 4px solid;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateX(2px);
  }

  &.common { border-left-color: #95a5a6; }
  &.good { border-left-color: #3498db; }
  &.excellent { border-left-color: #9b59b6; }
  &.epic { border-left-color: #e67e22; }
  &.legendary { border-left-color: #f1c40f; }
}

.listing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.seller-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.seller-name {
  font-weight: bold;
  color: #3498db;
}

.seller-ship {
  font-size: 0.8rem;
  color: #bbb;
}

.listing-time {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.listing-content {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.offering-section,
.wanting-section {
  h5 {
    margin: 0 0 0.5rem 0;
    color: #f39c12;
    font-size: 0.9rem;
  }
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.5rem;
}

.item-card {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.3rem;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(0, 0, 0, 0.4);
    transform: scale(1.02);
  }
}

.item-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-weight: bold;
  color: #fff;
  font-size: 0.8rem;
}

.item-amount {
  font-size: 0.7rem;
  color: #bbb;
}

.item-quality {
  font-size: 0.7rem;
  padding: 0.1rem 0.3rem;
  border-radius: 0.2rem;

  &.common { background: rgba(149, 165, 166, 0.3); color: #95a5a6; }
  &.good { background: rgba(52, 152, 219, 0.3); color: #3498db; }
  &.excellent { background: rgba(155, 89, 182, 0.3); color: #9b59b6; }
  &.epic { background: rgba(230, 126, 34, 0.3); color: #e67e22; }
  &.legendary { background: rgba(241, 196, 15, 0.3); color: #f1c40f; }
}

.wanted-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.wanted-item {
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
  font-size: 0.8rem;
}

.listing-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

// 私人交易样式
.private-panel {
  max-height: 500px;
  overflow-y: auto;
}

.private-trades-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.private-trade-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;

  &.unread {
    border-color: #e74c3c;
    background: rgba(231, 76, 60, 0.1);
  }

  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
}

.trade-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.trader-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.trader-name {
  font-weight: bold;
  color: #3498db;
}

.trade-status {
  font-size: 0.7rem;
  padding: 0.1rem 0.3rem;
  border-radius: 0.2rem;

  &.pending { background: rgba(243, 156, 18, 0.3); color: #f39c12; }
  &.accepted { background: rgba(46, 204, 113, 0.3); color: #2ecc71; }
  &.rejected { background: rgba(231, 76, 60, 0.3); color: #e74c3c; }
  &.completed { background: rgba(52, 152, 219, 0.3); color: #3498db; }
}

.trade-time {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.trade-preview {
  margin-bottom: 0.8rem;
}

.trade-offer,
.trade-request {
  display: flex;
  gap: 0.5rem;
  margin: 0.3rem 0;
  font-size: 0.8rem;
}

.offer-label,
.request-label {
  color: #bbb;
  min-width: 70px;
}

.offer-items,
.request-items {
  color: #fff;
}

.trade-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

// 好友列表样式
.friends-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.friends-header {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.friend-search {
  flex: 1;
}

.friends-list {
  max-height: 450px;
  overflow-y: auto;
}

.online-friends,
.offline-friends {
  margin-bottom: 1.5rem;

  h4 {
    color: #3498db;
    margin: 0 0 0.8rem 0;
    font-size: 0.9rem;
  }
}

.friend-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  margin: 0.5rem 0;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  &.online {
    border-left: 3px solid #2ecc71;
  }

  &.offline {
    border-left: 3px solid #95a5a6;
    opacity: 0.7;
  }
}

.friend-avatar {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.friend-info {
  flex: 1;
  min-width: 0;
}

.friend-name {
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.2rem;
}

.friend-ship {
  font-size: 0.8rem;
  color: #bbb;
  margin-bottom: 0.2rem;
}

.friend-status {
  font-size: 0.7rem;
  color: #2ecc71;
}

.last-seen {
  font-size: 0.7rem;
  color: #95a5a6;
}

.friend-actions {
  display: flex;
  gap: 0.5rem;
}

// 空状态样式
.no-trades,
.no-friends {
  text-align: center;
  padding: 2rem;
  color: #bbb;

  .empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
  }

  p {
    margin: 0.5rem 0;
  }

  .tip {
    font-size: 0.8rem;
    color: #7f8c8d;
  }
}
</style>