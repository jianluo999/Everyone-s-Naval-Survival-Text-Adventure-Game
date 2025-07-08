#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理并重新导入501-830章节数据
"""

import mysql.connector
import os

class CleanAndReimporter:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        self.sql_file = "novel_texts/optimized_sql/combined_501_830.sql"
        
    def connect_db(self):
        """连接数据库"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
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
    
    def import_new_data(self):
        """导入新的501-830章节数据"""
        print("=== 导入新的501-830章节数据 ===")
        
        if not os.path.exists(self.sql_file):
            print(f"❌ SQL文件不存在: {self.sql_file}")
            return False
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 读取并执行SQL文件
            with open(self.sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 分割SQL语句并执行
            sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            executed_count = 0
            for statement in sql_statements:
                if statement.upper().startswith('INSERT'):
                    try:
                        cursor.execute(statement)
                        executed_count += 1
                        
                        if executed_count % 500 == 0:
                            conn.commit()
                            print(f"  已执行 {executed_count} 条插入语句")
                    except Exception as e:
                        print(f"  执行语句失败: {str(e)[:100]}...")
                        continue
                elif statement.upper() in ['START TRANSACTION', 'COMMIT']:
                    cursor.execute(statement)
            
            conn.commit()
            print(f"✅ 成功执行 {executed_count} 条插入语句")
            return True
            
        except Exception as e:
            print(f"导入数据错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def verify_final_result(self):
        """验证最终结果"""
        print("=== 验证最终结果 ===")
        
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
            
            print(f"最终验证结果:")
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
            
            return new_stories >= 2000  # 期望至少2000个故事
            
        except Exception as e:
            print(f"验证错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def run(self):
        """运行完整流程"""
        print("清理并重新导入501-830章节")
        print("=" * 50)
        
        # 1. 清理现有数据
        if not self.clean_existing_data():
            print("❌ 清理数据失败")
            return False
        
        # 2. 导入新数据
        if not self.import_new_data():
            print("❌ 导入新数据失败")
            return False
        
        # 3. 验证结果
        if self.verify_final_result():
            print("\n🎉 清理并重新导入完成且验证通过!")
            return True
        else:
            print("\n⚠️ 导入完成但验证发现问题")
            return False

def main():
    reimporter = CleanAndReimporter()
    reimporter.run()

if __name__ == "__main__":
    main()
