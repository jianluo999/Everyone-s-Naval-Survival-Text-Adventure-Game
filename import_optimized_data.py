#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入优化后的场景和选择数据
"""

import json
import pymysql
from typing import List, Dict

class OptimizedDataImporter:
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
        return pymysql.connect(**self.db_config)

    def clear_existing_data(self):
        """清空现有数据"""
        print("🗑️ 清空现有数据...")
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # 清空选择表
            cursor.execute("DELETE FROM choices WHERE story_id LIKE 'story_%'")
            print(f"✅ 清空选择数据: {cursor.rowcount} 条")
            
            # 清空场景表
            cursor.execute("DELETE FROM stories WHERE story_id LIKE 'story_%'")
            print(f"✅ 清空场景数据: {cursor.rowcount} 条")
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ 清空数据失败: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def import_scenes_batch(self, scenes: List[Dict], batch_size: int = 500):
        """批量导入场景数据"""
        print(f"📖 开始导入 {len(scenes)} 个优化场景...")
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        insert_sql = """
        INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            total_batches = (len(scenes) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(scenes))
                batch_scenes = scenes[start_idx:end_idx]
                
                # 准备批量数据
                batch_data = []
                for scene in batch_scenes:
                    batch_data.append((
                        scene['story_id'],
                        scene['title'],
                        scene['content'],
                        scene['chapter'],
                        scene['scene'],
                        scene['story_type'],
                        scene['is_ending']
                    ))
                
                # 执行批量插入
                cursor.executemany(insert_sql, batch_data)
                conn.commit()
                
                print(f"✅ 场景批次 {batch_num + 1}/{total_batches}: {len(batch_data)} 个场景")
            
            print(f"🎉 场景导入完成: {len(scenes)} 个")
            
        except Exception as e:
            print(f"❌ 场景导入失败: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def import_choices_batch(self, choices: List[Dict], batch_size: int = 500):
        """批量导入选择数据"""
        print(f"🎯 开始导入 {len(choices)} 个优化选择...")
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        insert_sql = """
        INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, 
                           health_cost, health_reward, gold_cost, gold_reward, experience_reward)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            total_batches = (len(choices) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(choices))
                batch_choices = choices[start_idx:end_idx]
                
                # 准备批量数据
                batch_data = []
                for choice in batch_choices:
                    batch_data.append((
                        choice['story_id'],
                        choice['text'],
                        choice['next_story_id'],
                        choice['requirements'],
                        choice['is_available'],
                        choice['health_cost'],
                        choice['health_reward'],
                        choice['gold_cost'],
                        choice['gold_reward'],
                        choice['experience_reward']
                    ))
                
                # 执行批量插入
                cursor.executemany(insert_sql, batch_data)
                conn.commit()
                
                print(f"✅ 选择批次 {batch_num + 1}/{total_batches}: {len(batch_data)} 个选择")
            
            print(f"🎉 选择导入完成: {len(choices)} 个")
            
        except Exception as e:
            print(f"❌ 选择导入失败: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def verify_import(self):
        """验证导入结果"""
        print("📊 验证导入结果...")
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        try:
            # 检查场景数量
            cursor.execute("SELECT COUNT(*) FROM stories WHERE story_id LIKE 'story_%'")
            scene_count = cursor.fetchone()[0]
            print(f"✅ 场景总数: {scene_count}")
            
            # 检查选择数量
            cursor.execute("SELECT COUNT(*) FROM choices WHERE story_id LIKE 'story_%'")
            choice_count = cursor.fetchone()[0]
            print(f"✅ 选择总数: {choice_count}")
            
            # 检查章节范围
            cursor.execute("SELECT MIN(chapter), MAX(chapter), COUNT(DISTINCT chapter) FROM stories WHERE story_id LIKE 'story_%'")
            min_ch, max_ch, total_ch = cursor.fetchone()
            print(f"✅ 章节范围: 第{min_ch}章 - 第{max_ch}章 (共{total_ch}章)")
            
            # 检查优化效果 - 第一人称转换
            cursor.execute("SELECT COUNT(*) FROM stories WHERE content LIKE '%我%' AND story_id LIKE 'story_%'")
            first_person_count = cursor.fetchone()[0]
            print(f"✅ 第一人称场景: {first_person_count} 个")
            
            # 检查智能标题
            cursor.execute("SELECT COUNT(*) FROM stories WHERE title LIKE '%：%' AND story_id LIKE 'story_%'")
            smart_title_count = cursor.fetchone()[0]
            print(f"✅ 智能标题场景: {smart_title_count} 个")
            
            # 检查选择多样性
            cursor.execute("SELECT COUNT(DISTINCT text) FROM choices WHERE story_id LIKE 'story_%'")
            unique_choices = cursor.fetchone()[0]
            print(f"✅ 独特选择类型: {unique_choices} 种")
            
        except Exception as e:
            print(f"❌ 验证失败: {e}")
        finally:
            cursor.close()
            conn.close()

    def import_optimized_data(self, scenes_file: str, choices_file: str):
        """导入优化后的数据"""
        print("🚀 开始导入优化后的游戏数据...")
        
        # 加载优化后的数据
        print("📂 加载优化数据...")
        with open(scenes_file, 'r', encoding='utf-8') as f:
            scenes = json.load(f)
        
        with open(choices_file, 'r', encoding='utf-8') as f:
            choices = json.load(f)
        
        print(f"📖 加载场景: {len(scenes)} 个")
        print(f"🎯 加载选择: {len(choices)} 个")
        
        # 清空现有数据
        self.clear_existing_data()
        
        # 导入优化后的数据
        self.import_scenes_batch(scenes)
        self.import_choices_batch(choices)
        
        # 验证导入结果
        self.verify_import()
        
        print("🎉 优化数据导入完成！")

def main():
    importer = OptimizedDataImporter()
    
    # 配置文件路径
    scenes_file = "novel_texts/optimized_scenes/optimized_scenes.json"
    choices_file = "novel_texts/optimized_scenes/optimized_choices.json"
    
    # 执行导入
    importer.import_optimized_data(scenes_file, choices_file)

if __name__ == "__main__":
    main()
