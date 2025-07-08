#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API连接测试脚本 - 测试前后端集成是否正常工作
"""

import requests
import json

def test_backend_api():
    """测试后端API连接"""
    base_url = "http://localhost:8080/api"
    
    print("🔌 测试后端API连接...")
    
    # 测试获取故事
    try:
        print("📖 测试获取故事 story_1_1...")
        response = requests.get(f"{base_url}/stories/story_1_1", timeout=5)
        
        if response.status_code == 200:
            story_data = response.json()
            print("✅ 故事获取成功:")
            print(f"   - 故事ID: {story_data.get('storyId')}")
            print(f"   - 标题: {story_data.get('title')}")
            print(f"   - 内容长度: {len(story_data.get('content', ''))}")
            print(f"   - 故事类型: {story_data.get('storyType')}")
        else:
            print(f"❌ 故事获取失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 故事获取异常: {e}")
    
    # 测试获取选择
    try:
        print("\n🎯 测试获取选择 story_1_1...")
        response = requests.get(f"{base_url}/choices/story_1_1", timeout=5)
        
        if response.status_code == 200:
            choices_data = response.json()
            print("✅ 选择获取成功:")
            print(f"   - 选择数量: {len(choices_data)}")
            
            for i, choice in enumerate(choices_data[:3]):  # 只显示前3个
                print(f"   - 选择{i+1}: {choice.get('text')}")
                print(f"     下一个故事: {choice.get('nextStoryId')}")
        else:
            print(f"❌ 选择获取失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 选择获取异常: {e}")
    
    # 测试获取玩家状态
    try:
        print("\n👤 测试获取玩家状态...")
        response = requests.get(f"{base_url}/players/1", timeout=5)
        
        if response.status_code == 200:
            player_data = response.json()
            print("✅ 玩家状态获取成功:")
            print(f"   - 玩家名: {player_data.get('name')}")
            print(f"   - 当前故事: {player_data.get('currentStoryId')}")
            print(f"   - 生命值: {player_data.get('health')}")
            print(f"   - 金币: {player_data.get('gold')}")
        else:
            print(f"❌ 玩家状态获取失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 玩家状态获取异常: {e}")
    
    # 测试数据库统计
    try:
        print("\n📊 测试数据库统计...")
        
        # 测试故事总数
        response = requests.get(f"{base_url}/stories", timeout=5)
        if response.status_code == 200:
            stories = response.json()
            print(f"✅ 故事总数: {len(stories)}")
        
        # 测试选择总数（通过获取多个故事的选择来估算）
        total_choices = 0
        test_stories = ["story_1_1", "story_1_2", "story_1_3", "story_2_1", "story_2_2"]
        
        for story_id in test_stories:
            try:
                response = requests.get(f"{base_url}/choices/{story_id}", timeout=2)
                if response.status_code == 200:
                    choices = response.json()
                    total_choices += len(choices)
            except:
                continue
        
        print(f"✅ 测试故事的选择总数: {total_choices}")
        
    except Exception as e:
        print(f"❌ 数据库统计异常: {e}")

def test_cors_headers():
    """测试CORS配置"""
    print("\n🌐 测试CORS配置...")
    
    try:
        response = requests.options("http://localhost:8080/api/stories/story_1_1", 
                                  headers={
                                      'Origin': 'http://localhost:3000',
                                      'Access-Control-Request-Method': 'GET'
                                  }, timeout=5)
        
        if response.status_code in [200, 204]:
            print("✅ CORS预检请求成功")
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            for header, value in cors_headers.items():
                if value:
                    print(f"   - {header}: {value}")
        else:
            print(f"❌ CORS预检失败: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ CORS测试异常: {e}")

def main():
    """主函数"""
    print("🎮 前后端集成测试")
    print("=" * 50)
    
    # 测试后端API
    test_backend_api()
    
    # 测试CORS
    test_cors_headers()
    
    print("\n" + "=" * 50)
    print("🎉 API连接测试完成！")

if __name__ == "__main__":
    main()
