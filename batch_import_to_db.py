#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量导入游戏数据到数据库
分批导入8000+场景和33000+选择数据
"""

import json
import mysql.connector
from mysql.connector import Error
import time

class BatchImporter:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'sailing_game',
            'user': 'root',
            'password': 'mgsincos30',
            'charset': 'utf8mb4',
            'use_unicode': True
        }
        self.batch_size = 100  # 每批处理100条记录
    
    def connect_database(self):
        """连接数据库"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                print("✅ 数据库连接成功")
                return connection
        except Error as e:
            print(f"❌ 数据库连接失败: {e}")
            return None
    
    def clear_existing_data(self, connection):
        """清空现有数据（可选）"""
        try:
            cursor = connection.cursor()
            
            # 询问是否清空现有数据
            response = input("是否清空现有的stories和choices数据？(y/N): ")
            if response.lower() == 'y':
                print("🗑️ 清空现有数据...")
                cursor.execute("DELETE FROM choices")
                cursor.execute("DELETE FROM stories WHERE chapter > 0")
                connection.commit()
                print("✅ 现有数据已清空")
            else:
                print("⚠️ 保留现有数据，可能会有重复")
                
        except Error as e:
            print(f"❌ 清空数据失败: {e}")
    
    def import_stories_batch(self, connection, scenes_data):
        """批量导入场景数据"""
        print(f"📖 开始导入 {len(scenes_data)} 个场景...")
        
        cursor = connection.cursor()
        
        # 准备SQL语句
        insert_sql = """
        INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title = VALUES(title),
        content = VALUES(content),
        story_type = VALUES(story_type)
        """
        
        # 分批处理
        total_batches = (len(scenes_data) + self.batch_size - 1) // self.batch_size
        success_count = 0
        
        for i in range(0, len(scenes_data), self.batch_size):
            batch = scenes_data[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            
            try:
                # 准备批量数据
                batch_data = []
                for scene in batch:
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
                connection.commit()
                
                success_count += len(batch)
                print(f"✅ 批次 {batch_num}/{total_batches} 完成，已导入 {success_count}/{len(scenes_data)} 个场景")
                
            except Error as e:
                print(f"❌ 批次 {batch_num} 导入失败: {e}")
                connection.rollback()
        
        cursor.close()
        print(f"🎉 场景导入完成！成功导入 {success_count} 个场景")
        return success_count
    
    def import_choices_batch(self, connection, choices_data):
        """批量导入选择数据"""
        print(f"🎯 开始导入 {len(choices_data)} 个选择...")
        
        cursor = connection.cursor()
        
        # 准备SQL语句
        insert_sql = """
        INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, 
                           health_cost, health_reward, gold_cost, gold_reward, experience_reward) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        text = VALUES(text),
        next_story_id = VALUES(next_story_id)
        """
        
        # 分批处理
        total_batches = (len(choices_data) + self.batch_size - 1) // self.batch_size
        success_count = 0
        
        for i in range(0, len(choices_data), self.batch_size):
            batch = choices_data[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            
            try:
                # 准备批量数据
                batch_data = []
                for choice in batch:
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
                connection.commit()
                
                success_count += len(batch)
                print(f"✅ 批次 {batch_num}/{total_batches} 完成，已导入 {success_count}/{len(choices_data)} 个选择")
                
            except Error as e:
                print(f"❌ 批次 {batch_num} 导入失败: {e}")
                connection.rollback()
        
        cursor.close()
        print(f"🎉 选择导入完成！成功导入 {success_count} 个选择")
        return success_count
    
    def load_json_data(self, scenes_file, choices_file):
        """加载JSON数据"""
        print("📂 加载数据文件...")
        
        try:
            with open(scenes_file, 'r', encoding='utf-8') as f:
                scenes_data = json.load(f)
            
            with open(choices_file, 'r', encoding='utf-8') as f:
                choices_data = json.load(f)
            
            print(f"✅ 数据加载完成：{len(scenes_data)} 个场景，{len(choices_data)} 个选择")
            return scenes_data, choices_data
            
        except Exception as e:
            print(f"❌ 数据加载失败: {e}")
            return None, None
    
    def run_import(self):
        """执行完整的导入流程"""
        print("🚀 开始批量导入游戏数据...")
        
        # 加载数据
        scenes_data, choices_data = self.load_json_data(
            'novel_texts/game_scenes/all_scenes.json',
            'novel_texts/game_scenes/all_choices.json'
        )
        
        if not scenes_data or not choices_data:
            return
        
        # 连接数据库
        connection = self.connect_database()
        if not connection:
            return
        
        try:
            # 清空现有数据（可选）
            self.clear_existing_data(connection)
            
            # 导入场景数据
            start_time = time.time()
            scenes_imported = self.import_stories_batch(connection, scenes_data)
            scenes_time = time.time() - start_time
            
            # 导入选择数据
            start_time = time.time()
            choices_imported = self.import_choices_batch(connection, choices_data)
            choices_time = time.time() - start_time
            
            print(f"\n🎉 批量导入完成！")
            print(f"📊 场景导入：{scenes_imported} 个，耗时 {scenes_time:.2f} 秒")
            print(f"📊 选择导入：{choices_imported} 个，耗时 {choices_time:.2f} 秒")
            print(f"📊 总耗时：{scenes_time + choices_time:.2f} 秒")
            
        except Exception as e:
            print(f"❌ 导入过程中出现错误: {e}")
        
        finally:
            if connection.is_connected():
                connection.close()
                print("🔌 数据库连接已关闭")

def main():
    importer = BatchImporter()
    importer.run_import()

if __name__ == "__main__":
    main()
