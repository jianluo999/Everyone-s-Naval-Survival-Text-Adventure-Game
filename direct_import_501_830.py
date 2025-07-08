#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接导入501-830章节数据
"""

import mysql.connector
import json
import os

class DirectImporter:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        self.scenes_file = "novel_texts/game_scenes/game_scenes_501_830_fixed.json"
        
    def connect_db(self):
        """连接数据库"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
    def load_scenes(self):
        """加载场景数据"""
        print("=== 加载场景数据 ===")
        
        if not os.path.exists(self.scenes_file):
            print(f"❌ 文件不存在: {self.scenes_file}")
            return []
        
        with open(self.scenes_file, 'r', encoding='utf-8') as f:
            scenes = json.load(f)
        
        print(f"✅ 加载了{len(scenes)}个场景")
        return scenes
    
    def import_stories(self, scenes):
        """导入stories数据"""
        print("=== 导入stories数据 ===")

        conn = self.connect_db()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            # 准备批量插入，包含所有必需字段
            insert_sql = """
                INSERT INTO stories (story_id, title, content, chapter, scene, is_ending, story_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            story_data = []
            for scene in scenes:
                # 从story_id中提取章节和场景号
                story_id = scene['story_id']
                parts = story_id.split('_')
                chapter = int(parts[1]) if len(parts) >= 2 else 1
                scene_num = int(parts[2]) if len(parts) >= 3 else 1

                # 判断是否是结局场景（最后一个场景且没有选择）
                choices = scene.get('choices', [])
                is_ending = len(choices) == 0

                story_data.append((
                    scene['story_id'],
                    scene['title'],
                    scene['content'],
                    chapter,
                    scene_num,
                    is_ending,
                    'adventure'  # 默认故事类型
                ))

            # 批量插入
            cursor.executemany(insert_sql, story_data)
            conn.commit()

            print(f"✅ 成功插入{len(story_data)}个故事")
            return True

        except Exception as e:
            print(f"导入stories错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def import_choices(self, scenes):
        """导入choices数据"""
        print("=== 导入choices数据 ===")

        conn = self.connect_db()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            # 准备批量插入，包含所有必需字段
            insert_sql = """
                INSERT INTO choices (story_id, text, next_story_id, is_available,
                                   gold_cost, gold_reward, health_cost, health_reward, experience_reward, requirements)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            choice_data = []
            for scene in scenes:
                story_id = scene['story_id']
                choices = scene.get('choices', [])

                for choice in choices:
                    choice_text = choice.get('text', '')
                    next_story_id = choice.get('nextStoryId', '')

                    if choice_text and next_story_id:
                        choice_data.append((
                            story_id,
                            choice_text,
                            next_story_id,
                            True,  # is_available
                            0,     # gold_cost
                            0,     # gold_reward
                            0,     # health_cost
                            0,     # health_reward
                            0,     # experience_reward
                            ''     # requirements
                        ))

            # 批量插入
            cursor.executemany(insert_sql, choice_data)
            conn.commit()

            print(f"✅ 成功插入{len(choice_data)}个选择")
            return True

        except Exception as e:
            print(f"导入choices错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def verify_import(self):
        """验证导入结果"""
        print("=== 验证导入结果 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 检查501-830章节的故事
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM stories 
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
            """)
            new_stories = cursor.fetchone()[0]
            
            # 检查对应的选择
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM choices 
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
            """)
            new_choices = cursor.fetchone()[0]
            
            # 检查总数
            cursor.execute("SELECT COUNT(*) as count FROM stories")
            total_stories = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as count FROM choices")
            total_choices = cursor.fetchone()[0]
            
            print(f"导入验证结果:")
            print(f"  501-830章节故事: {new_stories}")
            print(f"  501-830章节选择: {new_choices}")
            print(f"  数据库总故事数: {total_stories}")
            print(f"  数据库总选择数: {total_choices}")
            
            # 测试关键故事
            test_stories = ['story_501_1', 'story_550_1', 'story_600_1', 'story_700_1', 'story_800_1', 'story_830_5']
            for story_id in test_stories:
                cursor.execute("SELECT title FROM stories WHERE story_id = %s", (story_id,))
                result = cursor.fetchone()
                if result:
                    print(f"  ✅ {story_id}: {result[0]}")
                else:
                    print(f"  ❌ {story_id}: 不存在")
            
            # 检查章节范围
            cursor.execute("""
                SELECT 
                    MIN(CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(story_id, '_', 2), '_', -1) AS UNSIGNED)) as min_chapter,
                    MAX(CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(story_id, '_', 2), '_', -1) AS UNSIGNED)) as max_chapter
                FROM stories 
                WHERE story_id REGEXP '^story_[0-9]+_[0-9]+$'
            """)
            result = cursor.fetchone()
            if result:
                print(f"  章节范围: {result[0]} - {result[1]}")
            
            return new_stories >= 2000
            
        except Exception as e:
            print(f"验证错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def clean_existing_data(self):
        """清理现有的501-830章节数据"""
        print("=== 清理现有501-830章节数据 ===")

        conn = self.connect_db()
        if not conn:
            return False

        cursor = conn.cursor()

        try:
            # 删除501-830章节的选择
            cursor.execute("""
                DELETE FROM choices
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
            """)
            deleted_choices = cursor.rowcount

            # 删除501-830章节的故事
            cursor.execute("""
                DELETE FROM stories
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
            """)
            deleted_stories = cursor.rowcount

            conn.commit()

            print(f"✅ 清理完成:")
            print(f"  删除故事: {deleted_stories}")
            print(f"  删除选择: {deleted_choices}")

            return True

        except Exception as e:
            print(f"清理数据错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def run(self):
        """运行导入流程"""
        print("直接导入501-830章节数据")
        print("=" * 50)

        # 0. 清理现有数据
        if not self.clean_existing_data():
            print("❌ 清理现有数据失败")
            return False

        # 1. 加载场景数据
        scenes = self.load_scenes()
        if not scenes:
            print("❌ 加载场景数据失败")
            return False

        # 2. 导入stories
        if not self.import_stories(scenes):
            print("❌ 导入stories失败")
            return False

        # 3. 导入choices
        if not self.import_choices(scenes):
            print("❌ 导入choices失败")
            return False

        # 4. 验证结果
        if self.verify_import():
            print("\n🎉 数据导入完成且验证通过!")
            return True
        else:
            print("\n⚠️ 数据导入完成但验证发现问题")
            return False

def main():
    importer = DirectImporter()
    importer.run()

if __name__ == "__main__":
    main()
