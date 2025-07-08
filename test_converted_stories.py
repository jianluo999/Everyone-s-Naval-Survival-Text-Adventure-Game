#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试转换后的故事内容
验证第二人称转换效果
"""

import mysql.connector
import requests
import os

# 禁用代理
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

class ConvertedStoryTester:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        self.backend_url = "http://localhost:8080/api"
        
    def connect_db(self):
        """连接数据库"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
    def test_database_stories(self):
        """测试数据库中的故事内容"""
        print("=== 测试数据库中的故事内容 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 测试关键故事
            test_stories = ['story_1_1', 'story_1_2', 'story_1_22', 'story_2_1']
            
            for story_id in test_stories:
                cursor.execute("SELECT story_id, title, content FROM stories WHERE story_id = %s", (story_id,))
                story = cursor.fetchone()
                
                if story:
                    print(f"\n故事ID: {story['story_id']}")
                    print(f"标题: {story['title']}")
                    print(f"内容: {story['content'][:150]}...")
                    
                    # 检查人称使用
                    content = story['content']
                    first_person_count = content.count('我') - content.count('"') * content.count('我') // max(content.count('"'), 1)
                    second_person_count = content.count('你')
                    
                    print(f"第一人称('我')出现次数: {first_person_count}")
                    print(f"第二人称('你')出现次数: {second_person_count}")
                    print("-" * 50)
                else:
                    print(f"❌ 故事 {story_id} 不存在")
            
            return True
            
        except Exception as e:
            print(f"数据库测试错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def test_api_stories(self):
        """测试API返回的故事内容"""
        print("\n=== 测试API返回的故事内容 ===")
        
        try:
            # 测试关键故事的API
            test_stories = ['story_1_1', 'story_1_2', 'story_1_22', 'story_2_1']
            
            for story_id in test_stories:
                response = requests.get(f"{self.backend_url}/game/story/{story_id}", timeout=10)
                
                if response.status_code == 200:
                    story_data = response.json()
                    if story_data.get('success') and 'story' in story_data:
                        story = story_data['story']
                        content = story.get('content', '')
                        
                        print(f"\n故事ID: {story_id}")
                        print(f"标题: {story.get('title', 'N/A')}")
                        print(f"内容: {content[:150]}...")
                        
                        # 检查人称使用
                        second_person_count = content.count('你')
                        print(f"第二人称('你')出现次数: {second_person_count}")
                        
                        # 检查选择
                        choices = story.get('choices', [])
                        print(f"选择数量: {len(choices)}")
                        for i, choice in enumerate(choices[:2]):
                            print(f"  选择{i+1}: {choice.get('text', 'N/A')}")
                        
                        print("-" * 50)
                    else:
                        print(f"❌ 故事 {story_id} API数据格式错误")
                else:
                    print(f"❌ 故事 {story_id} API请求失败: {response.status_code}")
            
            return True
            
        except Exception as e:
            print(f"API测试错误: {e}")
            return False
    
    def test_story_flow(self):
        """测试故事流程"""
        print("\n=== 测试故事流程 ===")
        
        try:
            # 测试从story_1_1开始的几个故事
            current_story = "story_1_1"
            
            for step in range(5):
                response = requests.get(f"{self.backend_url}/game/story/{current_story}", timeout=10)
                
                if response.status_code == 200:
                    story_data = response.json()
                    if story_data.get('success') and 'story' in story_data:
                        story = story_data['story']
                        content = story.get('content', '')
                        choices = story.get('choices', [])
                        
                        print(f"步骤 {step}: {current_story}")
                        print(f"  标题: {story.get('title', 'N/A')}")
                        print(f"  内容片段: {content[:80]}...")
                        print(f"  选择数量: {len(choices)}")
                        
                        if choices:
                            next_story = choices[0].get('nextStoryId')
                            print(f"  下一个故事: {next_story}")
                            current_story = next_story
                        else:
                            print("  没有更多选择")
                            break
                    else:
                        print(f"❌ 故事数据格式错误")
                        break
                else:
                    print(f"❌ API请求失败: {response.status_code}")
                    break
            
            return True
            
        except Exception as e:
            print(f"故事流程测试错误: {e}")
            return False
    
    def run_tests(self):
        """运行所有测试"""
        print("转换后故事内容测试")
        print("=" * 50)
        
        # 1. 测试数据库内容
        db_success = self.test_database_stories()
        
        # 2. 测试API内容
        api_success = self.test_api_stories()
        
        # 3. 测试故事流程
        flow_success = self.test_story_flow()
        
        # 总结
        print("\n=== 测试总结 ===")
        print(f"数据库测试: {'✅ 通过' if db_success else '❌ 失败'}")
        print(f"API测试: {'✅ 通过' if api_success else '❌ 失败'}")
        print(f"流程测试: {'✅ 通过' if flow_success else '❌ 失败'}")
        
        if db_success and api_success and flow_success:
            print("\n🎉 所有测试通过！第二人称转换成功！")
            return True
        else:
            print("\n⚠️ 部分测试失败，需要检查")
            return False

def main():
    tester = ConvertedStoryTester()
    tester.run_tests()

if __name__ == "__main__":
    main()
