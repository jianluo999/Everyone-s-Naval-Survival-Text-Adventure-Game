#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紧急故事修复脚本
删除所有断裂的选择，重新生成正确的选择
"""

import mysql.connector
import re

class EmergencyStoryFixer:
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
    
    def clean_broken_choices(self):
        """删除所有断裂的选择"""
        print("=== 清理断裂的选择 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 删除指向不存在故事的选择
            delete_query = """
            DELETE c FROM choices c
            LEFT JOIN stories s ON c.next_story_id = s.story_id
            WHERE s.story_id IS NULL
            """
            
            cursor.execute(delete_query)
            deleted_count = cursor.rowcount
            conn.commit()
            
            print(f"✅ 删除了 {deleted_count} 个断裂的选择")
            return True
            
        except Exception as e:
            print(f"清理错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def generate_sequential_choices(self):
        """为每个故事生成顺序选择"""
        print("=== 生成顺序选择 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 获取所有故事，按章节和场景排序
            cursor.execute("""
                SELECT story_id, chapter, scene, title
                FROM stories 
                WHERE is_ending = 0
                ORDER BY chapter, scene
            """)
            stories = cursor.fetchall()
            
            print(f"找到 {len(stories)} 个非结局故事")
            
            choices_added = 0
            
            for i, story in enumerate(stories):
                story_id = story['story_id']
                chapter = story['chapter']
                scene = story['scene']
                
                # 检查是否已有选择
                cursor.execute("SELECT COUNT(*) as count FROM choices WHERE story_id = %s", (story_id,))
                existing_choices = cursor.fetchone()['count']
                
                if existing_choices > 0:
                    continue  # 跳过已有选择的故事
                
                # 寻找下一个故事
                next_story_id = None
                
                # 方法1: 同章节下一个场景
                next_scene = scene + 1
                potential_next = f"story_{chapter}_{next_scene}"
                cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (potential_next,))
                if cursor.fetchone():
                    next_story_id = potential_next
                else:
                    # 方法2: 下一章第一个场景
                    next_chapter = chapter + 1
                    potential_next = f"story_{next_chapter}_1"
                    cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (potential_next,))
                    if cursor.fetchone():
                        next_story_id = potential_next
                    else:
                        # 方法3: 找下一个可用的故事
                        if i + 1 < len(stories):
                            next_story_id = stories[i + 1]['story_id']
                
                if next_story_id:
                    # 添加选择
                    insert_query = """
                    INSERT INTO choices (story_id, text, next_story_id, gold_cost, gold_reward, 
                                       health_cost, health_reward, experience_reward, is_available, requirements)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    choice_data = (story_id, '继续', next_story_id, 0, 0, 0, 0, 5, 1, '')
                    cursor.execute(insert_query, choice_data)
                    choices_added += 1
                    
                    if choices_added % 100 == 0:
                        print(f"已添加 {choices_added} 个选择...")
                        conn.commit()
            
            conn.commit()
            print(f"✅ 总共添加了 {choices_added} 个选择")
            return True
            
        except Exception as e:
            print(f"生成选择错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def add_multiple_choices_for_key_stories(self):
        """为关键故事添加多个选择"""
        print("=== 为关键故事添加多个选择 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 为每个章节的前几个故事添加多个选择
            cursor.execute("""
                SELECT story_id, chapter, scene
                FROM stories 
                WHERE scene <= 5 AND is_ending = 0
                ORDER BY chapter, scene
            """)
            key_stories = cursor.fetchall()
            
            choices_added = 0
            
            for story in key_stories:
                story_id = story['story_id']
                chapter = story['chapter']
                scene = story['scene']
                
                # 检查现有选择数量
                cursor.execute("SELECT COUNT(*) as count FROM choices WHERE story_id = %s", (story_id,))
                existing_count = cursor.fetchone()['count']
                
                if existing_count >= 3:
                    continue  # 已有足够选择
                
                # 寻找可能的目标故事
                targets = []
                
                # 添加同章节的几个后续故事
                for offset in range(1, 4):
                    target_scene = scene + offset
                    target_id = f"story_{chapter}_{target_scene}"
                    cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (target_id,))
                    if cursor.fetchone():
                        targets.append(target_id)
                
                # 如果目标不够，添加下一章的故事
                if len(targets) < 2:
                    next_chapter = chapter + 1
                    for scene_num in range(1, 4):
                        target_id = f"story_{next_chapter}_{scene_num}"
                        cursor.execute("SELECT story_id FROM stories WHERE story_id = %s", (target_id,))
                        if cursor.fetchone():
                            targets.append(target_id)
                
                # 添加选择
                choice_texts = [
                    "继续前进",
                    "仔细观察",
                    "谨慎行动"
                ]
                
                for i, target in enumerate(targets[:3]):
                    if i >= len(choice_texts):
                        break
                    
                    # 检查是否已存在指向该目标的选择
                    cursor.execute("""
                        SELECT COUNT(*) as count 
                        FROM choices 
                        WHERE story_id = %s AND next_story_id = %s
                    """, (story_id, target))
                    
                    if cursor.fetchone()['count'] == 0:
                        insert_query = """
                        INSERT INTO choices (story_id, text, next_story_id, gold_cost, gold_reward, 
                                           health_cost, health_reward, experience_reward, is_available, requirements)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        
                        choice_data = (story_id, choice_texts[i], target, 0, 0, 0, 0, 5, 1, '')
                        cursor.execute(insert_query, choice_data)
                        choices_added += 1
            
            conn.commit()
            print(f"✅ 为关键故事添加了 {choices_added} 个额外选择")
            return True
            
        except Exception as e:
            print(f"添加多选择错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def verify_story_flow(self):
        """验证故事流是否正常"""
        print("=== 验证故事流 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 检查没有选择的故事数量
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM stories s
                LEFT JOIN choices c ON s.story_id = c.story_id
                WHERE c.story_id IS NULL AND s.is_ending = 0
            """)
            no_choice_count = cursor.fetchone()['count']
            
            # 检查断裂选择数量
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM choices c
                LEFT JOIN stories s ON c.next_story_id = s.story_id
                WHERE s.story_id IS NULL
            """)
            broken_choice_count = cursor.fetchone()['count']
            
            # 检查总选择数量
            cursor.execute("SELECT COUNT(*) as count FROM choices")
            total_choices = cursor.fetchone()['count']
            
            print(f"验证结果:")
            print(f"  - 没有选择的故事: {no_choice_count}")
            print(f"  - 断裂的选择: {broken_choice_count}")
            print(f"  - 总选择数量: {total_choices}")
            
            # 测试从story_1_1开始的路径
            current_story = "story_1_1"
            path_length = 0
            max_path = 25
            
            print(f"\n测试从 {current_story} 开始的路径:")
            
            for step in range(max_path):
                cursor.execute("SELECT * FROM choices WHERE story_id = %s LIMIT 1", (current_story,))
                choice = cursor.fetchone()
                
                if not choice:
                    print(f"  步骤 {step}: ❌ {current_story} 没有选择")
                    break
                
                print(f"  步骤 {step}: ✅ {current_story} -> {choice['next_story_id']}")
                current_story = choice['next_story_id']
                path_length += 1
                
                if current_story == "story_1_22":
                    print(f"  🎯 成功到达 story_1_22!")
                    break
            
            success = no_choice_count < 100 and broken_choice_count == 0 and path_length >= 20
            print(f"\n验证结果: {'✅ 通过' if success else '❌ 失败'}")
            return success
            
        except Exception as e:
            print(f"验证错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def run_emergency_fix(self):
        """运行紧急修复"""
        print("紧急故事修复")
        print("=" * 50)
        
        # 1. 清理断裂选择
        if not self.clean_broken_choices():
            print("❌ 清理断裂选择失败")
            return False
        
        # 2. 生成顺序选择
        if not self.generate_sequential_choices():
            print("❌ 生成顺序选择失败")
            return False
        
        # 3. 为关键故事添加多个选择
        if not self.add_multiple_choices_for_key_stories():
            print("❌ 添加多选择失败")
            return False
        
        # 4. 验证修复效果
        if self.verify_story_flow():
            print("✅ 紧急修复成功!")
            return True
        else:
            print("❌ 修复验证失败")
            return False

def main():
    fixer = EmergencyStoryFixer()
    success = fixer.run_emergency_fix()
    
    if success:
        print("\n🎉 故事推进问题已修复!")
        print("现在可以重新启动游戏测试故事推进功能")
    else:
        print("\n💥 修复失败，需要进一步调查")

if __name__ == "__main__":
    main()
