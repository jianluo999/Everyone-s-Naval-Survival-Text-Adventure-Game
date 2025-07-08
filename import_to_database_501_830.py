#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入501-830章节数据到数据库
执行SQL插入语句
"""

import mysql.connector
import os
import time

class DatabaseImporter:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        self.sql_dir = "novel_texts/optimized_sql"
        
    def connect_db(self):
        """连接数据库"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
    def check_existing_data(self):
        """检查现有数据"""
        print("=== 检查现有数据 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 检查501-830章节的故事是否已存在
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM stories 
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
            """)
            existing_stories = cursor.fetchone()[0]
            
            # 检查总故事数
            cursor.execute("SELECT COUNT(*) as count FROM stories")
            total_stories = cursor.fetchone()[0]
            
            # 检查总选择数
            cursor.execute("SELECT COUNT(*) as count FROM choices")
            total_choices = cursor.fetchone()[0]
            
            print(f"现有数据统计:")
            print(f"  501-830章节故事: {existing_stories}")
            print(f"  总故事数: {total_stories}")
            print(f"  总选择数: {total_choices}")
            
            if existing_stories > 0:
                print(f"⚠️ 发现{existing_stories}个501-830章节的故事已存在")
                return True
            
            return False
            
        except Exception as e:
            print(f"检查数据错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def backup_database(self):
        """备份数据库"""
        print("=== 备份数据库 ===")
        
        try:
            backup_file = f"backup_before_501_830_{int(time.time())}.sql"
            backup_path = os.path.join(self.sql_dir, backup_file)
            
            # 使用mysqldump备份
            cmd = f'mysqldump -h localhost -u root -pmgsincos30 sailing_game > "{backup_path}"'
            os.system(cmd)
            
            if os.path.exists(backup_path):
                print(f"✅ 数据库已备份到: {backup_path}")
                return True
            else:
                print("❌ 备份失败")
                return False
                
        except Exception as e:
            print(f"备份错误: {e}")
            return False
    
    def execute_sql_file(self, sql_file: str) -> bool:
        """执行SQL文件"""
        print(f"=== 执行SQL文件: {sql_file} ===")
        
        if not os.path.exists(sql_file):
            print(f"❌ SQL文件不存在: {sql_file}")
            return False
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 读取SQL文件
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 分割SQL语句
            sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            executed_count = 0
            for i, statement in enumerate(sql_statements):
                if statement.upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER')):
                    try:
                        cursor.execute(statement)
                        executed_count += 1
                        
                        # 每100条语句提交一次
                        if executed_count % 100 == 0:
                            conn.commit()
                            print(f"  已执行 {executed_count}/{len(sql_statements)} 条语句")
                    except Exception as e:
                        print(f"  执行语句失败 {i+1}: {str(e)[:100]}...")
                        continue
            
            # 最终提交
            conn.commit()
            print(f"✅ 成功执行 {executed_count} 条SQL语句")
            return True
            
        except Exception as e:
            print(f"执行SQL文件错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def import_stories(self) -> bool:
        """导入stories数据"""
        stories_file = os.path.join(self.sql_dir, "stories_501_830.sql")
        return self.execute_sql_file(stories_file)
    
    def import_choices(self) -> bool:
        """导入choices数据"""
        choices_file = os.path.join(self.sql_dir, "choices_501_830.sql")
        return self.execute_sql_file(choices_file)
    
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
            print(f"  新增501-830章节故事: {new_stories}")
            print(f"  新增501-830章节选择: {new_choices}")
            print(f"  数据库总故事数: {total_stories}")
            print(f"  数据库总选择数: {total_choices}")
            
            # 测试几个关键故事
            test_stories = ['story_501_1', 'story_600_1', 'story_700_1', 'story_830_1']
            for story_id in test_stories:
                cursor.execute("SELECT title FROM stories WHERE story_id = %s", (story_id,))
                result = cursor.fetchone()
                if result:
                    print(f"  ✅ {story_id}: {result[0]}")
                else:
                    print(f"  ❌ {story_id}: 不存在")
            
            # 检查断裂选择
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM choices c
                LEFT JOIN stories s ON c.next_story_id = s.story_id
                WHERE s.story_id IS NULL
            """)
            broken_choices = cursor.fetchone()[0]
            print(f"  断裂选择数: {broken_choices}")
            
            return new_stories > 0 and new_choices > 0
            
        except Exception as e:
            print(f"验证错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def run(self):
        """运行完整导入流程"""
        print("数据库导入器 - 501-830章")
        print("=" * 50)
        
        # 1. 检查现有数据
        has_existing = self.check_existing_data()
        
        if has_existing:
            confirm = input("发现现有数据，是否继续导入？(y/N): ")
            if confirm.lower() != 'y':
                print("导入已取消")
                return False
        
        # 2. 备份数据库
        if not self.backup_database():
            print("❌ 备份失败，导入终止")
            return False
        
        # 3. 导入stories
        print("\n开始导入stories数据...")
        if not self.import_stories():
            print("❌ Stories导入失败")
            return False
        
        # 4. 导入choices
        print("\n开始导入choices数据...")
        if not self.import_choices():
            print("❌ Choices导入失败")
            return False
        
        # 5. 验证导入结果
        if self.verify_import():
            print("\n🎉 数据导入完成且验证通过!")
            return True
        else:
            print("\n⚠️ 数据导入完成但验证发现问题")
            return False

def main():
    importer = DatabaseImporter()
    importer.run()

if __name__ == "__main__":
    main()
