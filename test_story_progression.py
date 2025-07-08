#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试故事推进功能
验证修复后的游戏是否能正常推进
"""

import mysql.connector
import requests
import time
import os

# 禁用代理
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

class StoryProgressionTester:
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
    
    def test_database_integrity(self):
        """测试数据库完整性"""
        print("=== 测试数据库完整性 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 检查故事总数
            cursor.execute("SELECT COUNT(*) as count FROM stories")
            story_count = cursor.fetchone()['count']
            print(f"故事总数: {story_count}")
            
            # 检查选择总数
            cursor.execute("SELECT COUNT(*) as count FROM choices")
            choice_count = cursor.fetchone()['count']
            print(f"选择总数: {choice_count}")
            
            # 检查断裂选择
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM choices c
                LEFT JOIN stories s ON c.next_story_id = s.story_id
                WHERE s.story_id IS NULL
            """)
            broken_count = cursor.fetchone()['count']
            print(f"断裂选择: {broken_count}")
            
            # 检查没有选择的故事
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM stories s
                LEFT JOIN choices c ON s.story_id = c.story_id
                WHERE c.story_id IS NULL AND s.is_ending = 0
            """)
            no_choice_count = cursor.fetchone()['count']
            print(f"没有选择的故事: {no_choice_count}")
            
            # 检查story_1_22的选择
            cursor.execute("SELECT * FROM choices WHERE story_id = 'story_1_22'")
            story_22_choices = cursor.fetchall()
            print(f"story_1_22的选择数: {len(story_22_choices)}")
            for choice in story_22_choices:
                print(f"  - {choice['text']} -> {choice['next_story_id']}")
            
            success = broken_count == 0 and no_choice_count <= 1 and len(story_22_choices) > 0
            print(f"数据库完整性: {'✅ 通过' if success else '❌ 失败'}")
            return success
            
        except Exception as e:
            print(f"数据库测试错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def test_backend_api(self):
        """测试后端API"""
        print("\n=== 测试后端API ===")
        
        try:
            # 测试获取story_1_1
            response = requests.get(f"{self.backend_url}/game/story/story_1_1", timeout=5)
            if response.status_code == 200:
                story_data = response.json()
                print(f"✅ story_1_1 API正常: {story_data.get('title', 'N/A')}")
            else:
                print(f"❌ story_1_1 API失败: {response.status_code}")
                return False
            
            # 测试获取story_1_22
            response = requests.get(f"{self.backend_url}/game/story/story_1_22", timeout=5)
            if response.status_code == 200:
                story_data = response.json()
                print(f"✅ story_1_22 API正常: {story_data.get('title', 'N/A')}")
            else:
                print(f"❌ story_1_22 API失败: {response.status_code}")
                return False
            
            # 测试获取story_1_22的选择（包含在故事API中）
            if response.status_code == 200:
                story_data = response.json()
                if story_data.get('success') and 'story' in story_data:
                    story = story_data['story']
                    choices = story.get('choices', [])
                    print(f"✅ story_1_22选择API正常: {len(choices)}个选择")
                    for choice in choices:
                        print(f"  - {choice.get('text', 'N/A')} -> {choice.get('nextStoryId', 'N/A')}")
                else:
                    print(f"❌ story_1_22选择数据格式错误")
                    return False
            else:
                print(f"❌ story_1_22选择API失败: {response.status_code}")
                return False
            
            # 测试获取story_2_1（story_1_22指向的下一个故事）
            response = requests.get(f"{self.backend_url}/game/story/story_2_1", timeout=5)
            if response.status_code == 200:
                story_data = response.json()
                if story_data.get('success') and 'story' in story_data:
                    story = story_data['story']
                    print(f"✅ story_2_1 API正常: {story.get('title', 'N/A')}")
                else:
                    print(f"❌ story_2_1数据格式错误")
                    return False
            else:
                print(f"❌ story_2_1 API失败: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            print(f"API测试错误: {e}")
            return False
    
    def test_story_progression_path(self):
        """测试故事推进路径"""
        print("\n=== 测试故事推进路径 ===")
        
        try:
            current_story = "story_1_1"
            path = []
            
            for step in range(25):
                path.append(current_story)
                
                # 获取当前故事
                response = requests.get(f"{self.backend_url}/game/story/{current_story}", timeout=5)
                if response.status_code != 200:
                    print(f"❌ 步骤 {step}: 无法获取故事 {current_story}")
                    return False

                story_response = response.json()
                if not story_response.get('success') or 'story' not in story_response:
                    print(f"❌ 步骤 {step}: 故事数据格式错误 {current_story}")
                    return False

                story_data = story_response['story']
                print(f"步骤 {step}: ✅ {current_story} - {story_data.get('title', 'N/A')}")

                # 获取选择（包含在故事数据中）
                choices_data = story_data.get('choices', [])
                if not choices_data:
                    print(f"❌ 步骤 {step}: 没有选择可以继续")
                    return False

                print(f"  有 {len(choices_data)} 个选择")

                # 选择第一个选择继续
                next_story = choices_data[0].get('nextStoryId')
                if not next_story:
                    print(f"❌ 步骤 {step}: 选择没有目标故事")
                    return False
                
                current_story = next_story
                
                # 如果到达story_1_22，检查是否能继续
                if current_story == "story_1_22":
                    print(f"🎯 到达关键点: story_1_22")
                    
                    # 获取story_1_22的选择
                    response = requests.get(f"{self.backend_url}/game/story/story_1_22", timeout=5)
                    if response.status_code == 200:
                        story_response = response.json()
                        if story_response.get('success') and 'story' in story_response:
                            story_data = story_response['story']
                            choices_22 = story_data.get('choices', [])
                            if choices_22:
                                next_from_22 = choices_22[0].get('nextStoryId')
                                print(f"✅ story_1_22可以继续到: {next_from_22}")

                                # 验证下一个故事存在
                                response = requests.get(f"{self.backend_url}/game/story/{next_from_22}", timeout=5)
                                if response.status_code == 200:
                                    target_response = response.json()
                                    if target_response.get('success'):
                                        print(f"✅ 目标故事 {next_from_22} 存在")
                                        return True
                                    else:
                                        print(f"❌ 目标故事 {next_from_22} 数据格式错误")
                                        return False
                                else:
                                    print(f"❌ 目标故事 {next_from_22} 不存在")
                                    return False
                            else:
                                print(f"❌ story_1_22没有选择")
                                return False
                        else:
                            print(f"❌ story_1_22数据格式错误")
                            return False
                    else:
                        print(f"❌ 无法获取story_1_22的选择")
                        return False
            
            print(f"✅ 成功测试了 {len(path)} 步故事推进")
            return True
            
        except Exception as e:
            print(f"路径测试错误: {e}")
            return False
    
    def run_complete_test(self):
        """运行完整测试"""
        print("故事推进功能测试")
        print("=" * 50)
        
        # 1. 测试数据库完整性
        if not self.test_database_integrity():
            print("❌ 数据库完整性测试失败")
            return False
        
        # 2. 测试后端API
        if not self.test_backend_api():
            print("❌ 后端API测试失败")
            return False
        
        # 3. 测试故事推进路径
        if not self.test_story_progression_path():
            print("❌ 故事推进路径测试失败")
            return False
        
        print("\n🎉 所有测试通过！故事推进功能已修复！")
        return True

def main():
    tester = StoryProgressionTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n✅ 修复验证成功！")
        print("🎮 现在可以正常游玩，故事推进不会再卡在22了！")
    else:
        print("\n❌ 验证失败，需要进一步检查")

if __name__ == "__main__":
    main()
