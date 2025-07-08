#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故事推进问题诊断脚本
分析为什么游戏在故事22后无法继续
"""

import mysql.connector
import json
from pathlib import Path

class StoryProgressionDebugger:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        
    def connect_db(self):
        """连接数据库"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
    def analyze_story_22(self):
        """分析故事22的详细信息"""
        print("=== 分析故事22 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 查找故事22
            cursor.execute("SELECT * FROM stories WHERE story_id LIKE '%_22' OR story_id LIKE '%_22_%'")
            stories_22 = cursor.fetchall()
            
            print(f"找到 {len(stories_22)} 个包含'22'的故事:")
            for story in stories_22:
                print(f"  - {story['story_id']}: {story['title'][:50]}...")
            
            # 查找story_1_22的选择
            cursor.execute("SELECT * FROM choices WHERE from_story_id = 'story_1_22'")
            choices_from_22 = cursor.fetchall()
            
            print(f"\n从story_1_22出发的选择 ({len(choices_from_22)}个):")
            for choice in choices_from_22:
                print(f"  - 选择ID: {choice['choice_id']}")
                print(f"    文本: {choice['choice_text'][:50]}...")
                print(f"    目标: {choice['to_story_id']}")
                
                # 检查目标故事是否存在
                cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (choice['to_story_id'],))
                target_exists = cursor.fetchone()
                if target_exists:
                    print(f"    状态: ✅ 目标故事存在")
                else:
                    print(f"    状态: ❌ 目标故事不存在!")
                print()
            
            # 查找指向story_1_22的选择
            cursor.execute("SELECT * FROM choices WHERE to_story_id = 'story_1_22'")
            choices_to_22 = cursor.fetchall()
            
            print(f"指向story_1_22的选择 ({len(choices_to_22)}个):")
            for choice in choices_to_22:
                print(f"  - 来源: {choice['from_story_id']} -> story_1_22")
                print(f"    选择: {choice['choice_text'][:50]}...")
            
        except Exception as e:
            print(f"查询错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def check_story_sequence(self, start_story="story_1_1", max_depth=30):
        """检查故事序列的连续性"""
        print(f"\n=== 检查故事序列连续性 (从{start_story}开始) ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        visited = set()
        current_story = start_story
        path = []
        
        try:
            for step in range(max_depth):
                if current_story in visited:
                    print(f"步骤 {step}: 检测到循环 - {current_story}")
                    break
                
                visited.add(current_story)
                path.append(current_story)
                
                # 获取当前故事信息
                cursor.execute("SELECT * FROM stories WHERE story_id = %s", (current_story,))
                story = cursor.fetchone()
                
                if not story:
                    print(f"步骤 {step}: ❌ 故事不存在 - {current_story}")
                    break
                
                print(f"步骤 {step}: ✅ {current_story} - {story['title'][:30]}...")
                
                # 获取选择
                cursor.execute("SELECT * FROM choices WHERE from_story_id = %s", (current_story,))
                choices = cursor.fetchall()
                
                if not choices:
                    print(f"  ❌ 没有选择可以继续!")
                    break
                
                print(f"  有 {len(choices)} 个选择:")
                for i, choice in enumerate(choices):
                    print(f"    {i+1}. {choice['choice_text'][:40]}... -> {choice['to_story_id']}")
                
                # 选择第一个选择继续
                next_story = choices[0]['to_story_id']
                
                # 检查下一个故事是否存在
                cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (next_story,))
                if not cursor.fetchone():
                    print(f"  ❌ 下一个故事不存在: {next_story}")
                    break
                
                current_story = next_story
                
                if step >= 25:  # 重点关注22附近
                    input("按Enter继续...")
            
            print(f"\n路径总结: {' -> '.join(path)}")
            
        except Exception as e:
            print(f"检查错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def find_broken_connections(self):
        """查找断裂的连接"""
        print("\n=== 查找断裂的连接 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 查找指向不存在故事的选择
            query = """
            SELECT c.choice_id, c.from_story_id, c.to_story_id, c.choice_text
            FROM choices c
            LEFT JOIN stories s ON c.to_story_id = s.story_id
            WHERE s.story_id IS NULL
            """
            
            cursor.execute(query)
            broken_choices = cursor.fetchall()
            
            print(f"发现 {len(broken_choices)} 个断裂的连接:")
            for choice in broken_choices:
                print(f"  - 选择ID: {choice['choice_id']}")
                print(f"    从: {choice['from_story_id']}")
                print(f"    到: {choice['to_story_id']} (不存在)")
                print(f"    文本: {choice['choice_text'][:50]}...")
                print()
            
            # 查找没有选择的故事
            query = """
            SELECT s.story_id, s.title
            FROM stories s
            LEFT JOIN choices c ON s.story_id = c.from_story_id
            WHERE c.from_story_id IS NULL
            AND s.story_id NOT LIKE '%_end'
            """
            
            cursor.execute(query)
            dead_end_stories = cursor.fetchall()
            
            print(f"发现 {len(dead_end_stories)} 个没有选择的故事:")
            for story in dead_end_stories:
                print(f"  - {story['story_id']}: {story['title'][:50]}...")
            
        except Exception as e:
            print(f"查找错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def check_story_id_patterns(self):
        """检查故事ID模式"""
        print("\n=== 检查故事ID模式 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            # 统计不同模式的故事ID
            cursor.execute("SELECT story_id FROM stories ORDER BY story_id")
            story_ids = [row[0] for row in cursor.fetchall()]
            
            patterns = {}
            for story_id in story_ids:
                parts = story_id.split('_')
                if len(parts) >= 3:
                    pattern = f"{parts[0]}_{parts[1]}_X"
                    if pattern not in patterns:
                        patterns[pattern] = []
                    patterns[pattern].append(int(parts[2]) if parts[2].isdigit() else parts[2])
            
            print("故事ID模式分析:")
            for pattern, numbers in patterns.items():
                if isinstance(numbers[0], int):
                    numbers.sort()
                    missing = []
                    for i in range(min(numbers), max(numbers) + 1):
                        if i not in numbers:
                            missing.append(i)
                    
                    print(f"  {pattern}: {min(numbers)}-{max(numbers)} (缺失: {missing[:10]}{'...' if len(missing) > 10 else ''})")
                else:
                    print(f"  {pattern}: {len(numbers)} 个故事")
            
        except Exception as e:
            print(f"模式检查错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def run_full_diagnosis(self):
        """运行完整诊断"""
        print("故事推进问题诊断")
        print("=" * 50)
        
        self.analyze_story_22()
        self.check_story_sequence()
        self.find_broken_connections()
        self.check_story_id_patterns()
        
        print("\n诊断完成!")

def main():
    debugger = StoryProgressionDebugger()
    debugger.run_full_diagnosis()

if __name__ == "__main__":
    main()
