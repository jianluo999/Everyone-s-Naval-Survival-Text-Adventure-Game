#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复故事推进问题
基于实际数据库表结构分析和修复故事连接断裂
"""

import mysql.connector
import json

class StoryProgressionFixer:
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
    
    def analyze_story_22_issue(self):
        """分析故事22的具体问题"""
        print("=== 分析故事22推进问题 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 查找story_1_22
            cursor.execute("SELECT * FROM stories WHERE story_id = 'story_1_22'")
            story_22 = cursor.fetchone()
            
            if story_22:
                print(f"找到story_1_22:")
                print(f"  标题: {story_22['title']}")
                print(f"  内容: {story_22['content'][:100]}...")
                
                # 查找从story_1_22出发的选择
                cursor.execute("SELECT * FROM choices WHERE story_id = 'story_1_22'")
                choices = cursor.fetchall()
                
                print(f"\n从story_1_22出发的选择 ({len(choices)}个):")
                for choice in choices:
                    print(f"  - 选择ID: {choice['id']}")
                    print(f"    文本: {choice['text']}")
                    print(f"    目标: {choice['next_story_id']}")
                    
                    # 检查目标故事是否存在
                    cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (choice['next_story_id'],))
                    target_exists = cursor.fetchone()
                    if target_exists:
                        print(f"    状态: ✅ 目标故事存在")
                    else:
                        print(f"    状态: ❌ 目标故事不存在!")
                    print()
                
                if len(choices) == 0:
                    print("  ❌ 没有找到任何选择！这就是问题所在！")
            else:
                print("❌ 没有找到story_1_22")
            
        except Exception as e:
            print(f"分析错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def find_broken_story_chains(self):
        """查找断裂的故事链"""
        print("\n=== 查找断裂的故事链 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 查找指向不存在故事的选择
            query = """
            SELECT c.id, c.story_id, c.next_story_id, c.text
            FROM choices c
            LEFT JOIN stories s ON c.next_story_id = s.story_id
            WHERE s.story_id IS NULL
            """
            
            cursor.execute(query)
            broken_choices = cursor.fetchall()
            
            print(f"发现 {len(broken_choices)} 个断裂的选择:")
            for choice in broken_choices:
                print(f"  - 选择ID: {choice['id']}")
                print(f"    从: {choice['story_id']}")
                print(f"    到: {choice['next_story_id']} (不存在)")
                print(f"    文本: {choice['text']}")
                print()
            
            # 查找没有选择的故事
            query = """
            SELECT s.story_id, s.title
            FROM stories s
            LEFT JOIN choices c ON s.story_id = c.story_id
            WHERE c.story_id IS NULL
            AND s.is_ending = 0
            ORDER BY s.story_id
            """
            
            cursor.execute(query)
            dead_end_stories = cursor.fetchall()
            
            print(f"发现 {len(dead_end_stories)} 个没有选择的故事:")
            for story in dead_end_stories[:20]:  # 只显示前20个
                print(f"  - {story['story_id']}: {story['title']}")
            
            if len(dead_end_stories) > 20:
                print(f"  ... 还有 {len(dead_end_stories) - 20} 个")
            
            return broken_choices, dead_end_stories
            
        except Exception as e:
            print(f"查找错误: {e}")
            return [], []
        finally:
            cursor.close()
            conn.close()
    
    def fix_story_22_specifically(self):
        """专门修复story_1_22的问题"""
        print("\n=== 修复story_1_22 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 检查story_1_22是否有选择
            cursor.execute("SELECT COUNT(*) as count FROM choices WHERE story_id = 'story_1_22'")
            result = cursor.fetchone()
            
            if result['count'] == 0:
                print("story_1_22没有选择，需要添加选择")
                
                # 查找story_1_23是否存在
                cursor.execute("SELECT story_id FROM stories WHERE story_id = 'story_1_23'")
                story_23_exists = cursor.fetchone()
                
                if story_23_exists:
                    # 添加选择指向story_1_23
                    insert_query = """
                    INSERT INTO choices (story_id, text, next_story_id, gold_cost, gold_reward, 
                                       health_cost, health_reward, experience_reward, is_available, requirements)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    choices_to_add = [
                        ('story_1_22', '继续前进', 'story_1_23', 0, 0, 0, 0, 5, 1, ''),
                        ('story_1_22', '仔细观察周围', 'story_1_23', 0, 0, 0, 0, 5, 1, ''),
                        ('story_1_22', '思考下一步行动', 'story_1_23', 0, 0, 0, 0, 5, 1, '')
                    ]
                    
                    for choice_data in choices_to_add:
                        cursor.execute(insert_query, choice_data)
                    
                    conn.commit()
                    print(f"✅ 为story_1_22添加了 {len(choices_to_add)} 个选择")
                    return True
                else:
                    print("❌ story_1_23不存在，无法修复")
                    return False
            else:
                print(f"story_1_22已有 {result['count']} 个选择")
                return True
                
        except Exception as e:
            print(f"修复错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def fix_all_dead_end_stories(self):
        """修复所有没有选择的故事"""
        print("\n=== 修复所有死路故事 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 查找所有没有选择的非结局故事
            query = """
            SELECT s.story_id, s.title, s.chapter, s.scene
            FROM stories s
            LEFT JOIN choices c ON s.story_id = c.story_id
            WHERE c.story_id IS NULL
            AND s.is_ending = 0
            ORDER BY s.chapter, s.scene
            """
            
            cursor.execute(query)
            dead_end_stories = cursor.fetchall()
            
            print(f"找到 {len(dead_end_stories)} 个需要修复的故事")
            
            fixed_count = 0
            for story in dead_end_stories:
                story_id = story['story_id']
                chapter = story['chapter']
                scene = story['scene']
                
                # 尝试找到下一个故事
                next_scene = scene + 1
                next_story_id = f"story_{chapter}_{next_scene}"
                
                # 检查下一个故事是否存在
                cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (next_story_id,))
                next_exists = cursor.fetchone()
                
                if next_exists:
                    # 添加选择
                    insert_query = """
                    INSERT INTO choices (story_id, text, next_story_id, gold_cost, gold_reward, 
                                       health_cost, health_reward, experience_reward, is_available, requirements)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    choice_data = (story_id, '继续', next_story_id, 0, 0, 0, 0, 5, 1, '')
                    cursor.execute(insert_query, choice_data)
                    fixed_count += 1
                    
                    if fixed_count % 100 == 0:
                        print(f"已修复 {fixed_count} 个故事...")
                        conn.commit()
            
            conn.commit()
            print(f"✅ 总共修复了 {fixed_count} 个故事")
            
        except Exception as e:
            print(f"批量修复错误: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    
    def verify_story_progression(self, start_story="story_1_1", max_steps=30):
        """验证故事推进是否正常"""
        print(f"\n=== 验证故事推进 (从{start_story}开始) ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        current_story = start_story
        path = []
        
        try:
            for step in range(max_steps):
                # 获取当前故事
                cursor.execute("SELECT * FROM stories WHERE story_id = %s", (current_story,))
                story = cursor.fetchone()
                
                if not story:
                    print(f"步骤 {step}: ❌ 故事不存在 - {current_story}")
                    break
                
                path.append(current_story)
                print(f"步骤 {step}: ✅ {current_story} - {story['title']}")
                
                # 获取选择
                cursor.execute("SELECT * FROM choices WHERE story_id = %s", (current_story,))
                choices = cursor.fetchall()
                
                if not choices:
                    print(f"  ❌ 没有选择可以继续!")
                    break
                
                print(f"  有 {len(choices)} 个选择:")
                for i, choice in enumerate(choices):
                    print(f"    {i+1}. {choice['text']} -> {choice['next_story_id']}")
                
                # 选择第一个选择继续
                next_story = choices[0]['next_story_id']
                current_story = next_story
                
                # 如果到达story_1_22，暂停让用户确认
                if current_story == 'story_1_22':
                    print(f"  到达关键点: {current_story}")
                    break
            
            print(f"\n验证路径: {' -> '.join(path)}")
            
        except Exception as e:
            print(f"验证错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def run_complete_fix(self):
        """运行完整修复"""
        print("故事推进问题修复")
        print("=" * 50)
        
        # 1. 分析问题
        self.analyze_story_22_issue()
        
        # 2. 查找断裂链
        broken_choices, dead_end_stories = self.find_broken_story_chains()
        
        # 3. 修复story_1_22
        if self.fix_story_22_specifically():
            print("✅ story_1_22修复成功")
        
        # 4. 修复所有死路故事
        if len(dead_end_stories) > 0:
            self.fix_all_dead_end_stories()
        
        # 5. 验证修复效果
        self.verify_story_progression()
        
        print("\n修复完成!")

def main():
    fixer = StoryProgressionFixer()
    fixer.run_complete_fix()

if __name__ == "__main__":
    main()
