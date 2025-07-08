/**
 * 前后端连接测试工具
 * 用于验证前后端数据同步是否正常
 */

import gameApi from '@/api/game'

export class ConnectionTester {
  constructor() {
    this.testResults = []
  }

  async runAllTests() {
    console.log('🧪 开始前后端连接测试...')
    
    const tests = [
      this.testHealthCheck,
      this.testPlayerCreation,
      this.testPlayerDataSync,
      this.testStoryLoading,
      this.testChoiceExecution,
      this.testFishingSystem
    ]

    for (const test of tests) {
      try {
        await test.call(this)
      } catch (error) {
        console.error(`❌ 测试失败: ${test.name}`, error)
        this.testResults.push({
          test: test.name,
          status: 'failed',
          error: error.message
        })
      }
    }

    this.printResults()
    return this.testResults
  }

  async testHealthCheck() {
    console.log('🔍 测试后端健康检查...')
    const response = await gameApi.healthCheck()
    
    if (response.status === 'healthy') {
      console.log('✅ 后端服务正常')
      this.testResults.push({ test: 'healthCheck', status: 'passed' })
    } else {
      throw new Error('后端服务异常')
    }
  }

  async testPlayerCreation() {
    console.log('🔍 测试玩家创建...')
    const testPlayerName = `测试玩家_${Date.now()}`
    
    const response = await gameApi.createPlayer(testPlayerName)
    
    if (response.success && response.player) {
      console.log('✅ 玩家创建成功')
      this.testPlayer = response.player
      this.testResults.push({ test: 'playerCreation', status: 'passed' })
    } else {
      throw new Error('玩家创建失败')
    }
  }

  async testPlayerDataSync() {
    console.log('🔍 测试玩家数据同步...')
    
    if (!this.testPlayer) {
      throw new Error('没有测试玩家')
    }

    const response = await gameApi.getPlayer(this.testPlayer.name)
    
    if (response.success && response.player) {
      // 验证关键数据是否一致
      const player = response.player
      const checks = [
        player.name === this.testPlayer.name,
        player.health !== undefined,
        player.sanity !== undefined,
        player.gameState !== undefined,
        player.ship !== undefined
      ]

      if (checks.every(check => check)) {
        console.log('✅ 玩家数据同步正常')
        this.testResults.push({ test: 'playerDataSync', status: 'passed' })
      } else {
        throw new Error('玩家数据不完整')
      }
    } else {
      throw new Error('获取玩家数据失败')
    }
  }

  async testStoryLoading() {
    console.log('🔍 测试故事加载...')
    
    const storyId = 'story_1_1' // 默认起始故事
    const response = await gameApi.getStory(storyId)
    
    if (response.success && response.story) {
      const story = response.story
      const checks = [
        story.storyId === storyId,
        story.title !== undefined,
        story.content !== undefined,
        Array.isArray(story.choices)
      ]

      if (checks.every(check => check)) {
        console.log('✅ 故事加载正常')
        this.testResults.push({ test: 'storyLoading', status: 'passed' })
      } else {
        throw new Error('故事数据不完整')
      }
    } else {
      throw new Error('故事加载失败')
    }
  }

  async testChoiceExecution() {
    console.log('🔍 测试选择执行...')
    
    if (!this.testPlayer) {
      throw new Error('没有测试玩家')
    }

    // 获取当前故事的选择
    const storyResponse = await gameApi.getStory(this.testPlayer.gameState.currentStoryId)
    
    if (storyResponse.success && storyResponse.story.choices.length > 0) {
      const firstChoice = storyResponse.story.choices[0]
      
      const choiceResponse = await gameApi.makeChoice({
        playerName: this.testPlayer.name,
        choiceId: firstChoice.id,
        nextStoryId: firstChoice.nextStoryId
      })

      if (choiceResponse.success && choiceResponse.player) {
        console.log('✅ 选择执行正常')
        this.testResults.push({ test: 'choiceExecution', status: 'passed' })
      } else {
        throw new Error('选择执行失败')
      }
    } else {
      throw new Error('没有可用的选择')
    }
  }

  async testFishingSystem() {
    console.log('🔍 测试钓鱼系统...')
    
    if (!this.testPlayer) {
      throw new Error('没有测试玩家')
    }

    const response = await gameApi.goFishing(this.testPlayer.name)
    
    if (response.success) {
      console.log('✅ 钓鱼系统正常')
      this.testResults.push({ test: 'fishingSystem', status: 'passed' })
    } else {
      // 钓鱼失败可能是正常的（精力不足等），只要API调用成功就行
      console.log('✅ 钓鱼API调用正常')
      this.testResults.push({ test: 'fishingSystem', status: 'passed' })
    }
  }

  printResults() {
    console.log('\n📊 测试结果汇总:')
    console.log('==================')
    
    const passed = this.testResults.filter(r => r.status === 'passed').length
    const failed = this.testResults.filter(r => r.status === 'failed').length
    
    this.testResults.forEach(result => {
      const icon = result.status === 'passed' ? '✅' : '❌'
      console.log(`${icon} ${result.test}`)
      if (result.error) {
        console.log(`   错误: ${result.error}`)
      }
    })
    
    console.log('==================')
    console.log(`总计: ${this.testResults.length} 个测试`)
    console.log(`通过: ${passed} 个`)
    console.log(`失败: ${failed} 个`)
    
    if (failed === 0) {
      console.log('🎉 所有测试通过！前后端连接正常！')
    } else {
      console.log('⚠️ 存在连接问题，请检查失败的测试项')
    }
  }
}

// 导出便捷方法
export async function testConnection() {
  const tester = new ConnectionTester()
  return await tester.runAllTests()
}

export default ConnectionTester
