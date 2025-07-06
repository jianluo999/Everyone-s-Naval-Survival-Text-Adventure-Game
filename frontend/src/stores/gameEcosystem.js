import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useGameEcosystemStore = defineStore('gameEcosystem', () => {
  // ==================== 核心游戏状态 ====================
  
  // 玩家基础状态
  const player = ref({
    name: '杨逸',
    level: 15,
    experience: 2450,
    experienceToNext: 3000,
    health: 76,
    maxHealth: 100,
    sanity: 93,
    maxSanity: 100,
    energy: 35,
    maxEnergy: 100,
    location: '起源之海',
    coordinates: { x: 125, y: 89 }
  })
  
  // 船只状态
  const ship = ref({
    name: '梦魇号',
    type: '探索船',
    durability: 85,
    maxDurability: 100,
    speed: 12,
    capacity: 500,
    usedCapacity: 287,
    skills: ['深海探测', '风暴预警', '快速修复']
  })
  
  // 资源系统
  const resources = ref({
    gold: 500,
    wood: 125,
    cloth: 98,
    food: 67,
    water: 89,
    medicine: 23,
    ammunition: 45,
    rare_materials: 12
  })
  
  // 物品库存
  const inventory = ref([
    { id: 1, name: '燧发枪', type: 'weapon', quality: 'rare', durability: 78, equipped: true },
    { id: 2, name: '海盗长弓', type: 'weapon', quality: 'common', durability: 92, equipped: false },
    { id: 3, name: '圣水', type: 'consumable', quality: 'legendary', quantity: 3 },
    { id: 4, name: '医疗绷带', type: 'consumable', quality: 'common', quantity: 15 },
    { id: 5, name: '椰子', type: 'food', quality: 'common', quantity: 28 }
  ])
  
  // ==================== 功能模块状态 ====================
  
  // 探索系统状态
  const exploration = ref({
    currentIsland: null,
    discoveredIslands: [
      { id: 1, name: '椰林岛', type: 'resource', discovered: true, resources: ['椰子', '木料'] },
      { id: 2, name: '神秘岛', type: 'treasure', discovered: true, hasChest: true },
      { id: 3, name: '废船岛', type: 'danger', discovered: false, threat: 'undead' }
    ],
    tools: [
      { id: 1, name: '石斧', durability: 67, maxDurability: 100, efficiency: 1.2 }
    ],
    dailyExplorationCount: 2,
    maxDailyExplorations: 5
  })
  
  // 交易系统状态
  const trading = ref({
    marketItems: [
      { id: 1, sellerId: 'npc_zhou', item: '圣水', price: 150, quantity: 2 },
      { id: 2, sellerId: 'player_123', item: '燧发枪', price: 300, quantity: 1 },
      { id: 3, sellerId: 'npc_merchant', item: '船只图纸', price: 500, quantity: 1 }
    ],
    friends: [
      { id: 'player_123', name: '李明', online: true, lastSeen: new Date() },
      { id: 'player_456', name: '王芳', online: false, lastSeen: new Date(Date.now() - 3600000) }
    ],
    tradeHistory: [],
    reputation: 85
  })
  
  // 战斗系统状态
  const combat = ref({
    inCombat: false,
    combatLog: [],
    weapons: computed(() => inventory.value.filter(item => item.type === 'weapon')),
    equippedWeapon: computed(() => inventory.value.find(item => item.type === 'weapon' && item.equipped)),
    combatStats: {
      wins: 12,
      losses: 3,
      escapes: 5,
      totalDamageDealt: 2450,
      totalDamageTaken: 890
    }
  })
  
  // 占星系统状态
  const astrology = ref({
    dailyPredictions: [
      { type: 'storm', message: '3天后将有强风暴来袭', severity: 'high', timeLeft: 259200 },
      { type: 'treasure', message: '东北方向可能有宝藏', confidence: 0.7 },
      { type: 'danger', message: '附近有敌对船只活动', threat: 'medium' }
    ],
    scryingUsed: false,
    maxDailyScrying: 1,
    nearbyShips: [
      { id: 'ship_001', name: '黑珍珠号', distance: 45, hostility: 'hostile', captain: '巴博萨' },
      { id: 'ship_002', name: '商船', distance: 78, hostility: 'neutral', captain: '商人老李' }
    ],
    starAlignment: 'favorable'
  })
  
  // 天赋系统状态
  const talents = ref({
    unlockedTalents: [
      { id: 'fishing_master', name: '钓鱼大师', level: 2, effect: '钓鱼效率+40%' },
      { id: 'deep_sea_adaptation', name: '深海适应', level: 1, effect: '水下活动时间+50%' }
    ],
    availablePoints: 3,
    conditions: {
      fishing_catches: 156,
      combat_wins: 12,
      islands_explored: 8,
      trades_completed: 23
    }
  })
  
  // ==================== 生态系统逻辑 ====================
  
  // 计算属性 - 展示系统间的关联
  const playerPowerLevel = computed(() => {
    const baseLevel = player.value.level
    const equipmentBonus = inventory.value
      .filter(item => item.equipped)
      .reduce((sum, item) => sum + (item.quality === 'legendary' ? 10 : item.quality === 'rare' ? 5 : 2), 0)
    const talentBonus = talents.value.unlockedTalents.length * 3
    return baseLevel + equipmentBonus + talentBonus
  })
  
  const shipEfficiency = computed(() => {
    const baseEfficiency = ship.value.durability / ship.value.maxDurability
    const skillBonus = ship.value.skills.length * 0.1
    const cargoWeight = ship.value.usedCapacity / ship.value.capacity
    return Math.max(0.1, baseEfficiency + skillBonus - cargoWeight * 0.3)
  })
  
  const survivalRating = computed(() => {
    const healthRatio = player.value.health / player.value.maxHealth
    const sanityRatio = player.value.sanity / player.value.maxSanity
    const resourceSecurity = Math.min(1, (resources.value.food + resources.value.water) / 100)
    const equipmentQuality = inventory.value.filter(item => item.equipped).length / 3
    
    return Math.floor((healthRatio + sanityRatio + resourceSecurity + equipmentQuality) * 25)
  })
  
  // ==================== 系统间交互方法 ====================
  
  // 探索影响其他系统
  const completeExploration = (islandId, resourcesGained, experienceGained) => {
    // 更新资源
    Object.keys(resourcesGained).forEach(resource => {
      if (resources.value[resource] !== undefined) {
        resources.value[resource] += resourcesGained[resource]
      }
    })
    
    // 更新经验
    player.value.experience += experienceGained
    if (player.value.experience >= player.value.experienceToNext) {
      levelUp()
    }
    
    // 消耗精力
    player.value.energy = Math.max(0, player.value.energy - 15)
    
    // 更新探索计数
    exploration.value.dailyExplorationCount++
    
    // 更新天赋条件
    talents.value.conditions.islands_explored++
    
    // 检查天赋解锁
    checkTalentUnlocks()
  }
  
  // 交易影响其他系统
  const completeTrade = (itemId, price, isBuying) => {
    if (isBuying) {
      resources.value.gold -= price
      // 添加物品到库存的逻辑
    } else {
      resources.value.gold += price
      // 从库存移除物品的逻辑
    }
    
    // 更新交易声誉
    trading.value.reputation += isBuying ? 1 : 2
    
    // 更新天赋条件
    talents.value.conditions.trades_completed++
    
    // 检查天赋解锁
    checkTalentUnlocks()
  }
  
  // 战斗影响其他系统
  const completeCombat = (result, damageDealt, damageTaken) => {
    // 更新战斗统计
    combat.value.combatStats[result]++
    combat.value.combatStats.totalDamageDealt += damageDealt
    combat.value.combatStats.totalDamageTaken += damageTaken
    
    // 影响玩家状态
    player.value.health = Math.max(0, player.value.health - damageTaken)
    if (result === 'losses') {
      player.value.sanity = Math.max(0, player.value.sanity - 10)
    }
    
    // 武器耐久度损失
    const weapon = combat.value.equippedWeapon.value
    if (weapon) {
      weapon.durability = Math.max(0, weapon.durability - 5)
    }
    
    // 更新天赋条件
    if (result === 'wins') {
      talents.value.conditions.combat_wins++
    }
    
    // 检查天赋解锁
    checkTalentUnlocks()
  }
  
  // 占星预测影响其他系统
  const useAstrologyPrediction = (predictionType) => {
    astrology.value.scryingUsed = true
    
    // 根据预测类型给予不同的信息优势
    switch (predictionType) {
      case 'storm':
        // 提前准备风暴，减少损失
        break
      case 'treasure':
        // 增加探索成功率
        break
      case 'danger':
        // 提高战斗准备度
        break
    }
    
    // 消耗精力
    player.value.energy = Math.max(0, player.value.energy - 10)
  }
  
  // 天赋系统影响其他系统
  const unlockTalent = (talentId) => {
    const talent = {
      id: talentId,
      name: getTalentName(talentId),
      level: 1,
      effect: getTalentEffect(talentId)
    }
    
    talents.value.unlockedTalents.push(talent)
    talents.value.availablePoints--
    
    // 天赋效果立即生效
    applyTalentEffects()
  }
  
  // ==================== 辅助方法 ====================
  
  const levelUp = () => {
    player.value.level++
    player.value.experience = 0
    player.value.experienceToNext = player.value.level * 200
    player.value.maxHealth += 5
    player.value.maxSanity += 3
    player.value.maxEnergy += 10
    talents.value.availablePoints++
  }
  
  const checkTalentUnlocks = () => {
    // 检查是否满足天赋解锁条件
    const conditions = talents.value.conditions
    
    if (conditions.fishing_catches >= 100 && !hasTalent('fishing_master')) {
      // 解锁钓鱼大师天赋
    }
    
    if (conditions.combat_wins >= 10 && !hasTalent('combat_veteran')) {
      // 解锁战斗老兵天赋
    }
  }
  
  const hasTalent = (talentId) => {
    return talents.value.unlockedTalents.some(talent => talent.id === talentId)
  }
  
  const getTalentName = (talentId) => {
    const names = {
      fishing_master: '钓鱼大师',
      combat_veteran: '战斗老兵',
      deep_sea_adaptation: '深海适应',
      trade_expert: '贸易专家'
    }
    return names[talentId] || talentId
  }
  
  const getTalentEffect = (talentId) => {
    const effects = {
      fishing_master: '钓鱼效率+40%',
      combat_veteran: '战斗伤害+25%',
      deep_sea_adaptation: '水下活动时间+50%',
      trade_expert: '交易价格优化15%'
    }
    return effects[talentId] || '未知效果'
  }
  
  const applyTalentEffects = () => {
    // 应用所有已解锁天赋的效果
    talents.value.unlockedTalents.forEach(talent => {
      // 根据天赋类型应用不同效果
    })
  }
  
  // ==================== 监听器 - 系统间自动反应 ====================
  
  // 监听健康状态，自动影响其他系统
  watch(() => player.value.health, (newHealth) => {
    if (newHealth < 20) {
      // 低血量时影响战斗效率
      player.value.sanity = Math.max(0, player.value.sanity - 1)
    }
  })
  
  // 监听理智状态，自动影响其他系统
  watch(() => player.value.sanity, (newSanity) => {
    if (newSanity < 30) {
      // 低理智时影响所有行动效率
      ship.value.speed = Math.max(5, ship.value.speed * 0.8)
    }
  })
  
  // 监听船只耐久度，自动影响航行
  watch(() => ship.value.durability, (newDurability) => {
    if (newDurability < 30) {
      // 低耐久度时降低航行速度
      ship.value.speed = Math.max(3, ship.value.speed * 0.6)
    }
  })
  
  return {
    // 状态
    player,
    ship,
    resources,
    inventory,
    exploration,
    trading,
    combat,
    astrology,
    talents,
    
    // 计算属性
    playerPowerLevel,
    shipEfficiency,
    survivalRating,
    
    // 方法
    completeExploration,
    completeTrade,
    completeCombat,
    useAstrologyPrediction,
    unlockTalent,
    levelUp,
    checkTalentUnlocks
  }
})
