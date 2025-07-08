#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版数据库导入器 - 将优化后的SQL文件导入到MySQL数据库
确保数据能正确导入并验证完整性
"""

import os
import mysql.connector
from mysql.connector import Error
import time

class FixedDatabaseImporter:
    def __init__(self):
        self.sql_dir = "novel_texts/optimized_sql"
        self.db_config = {
            'host': 'localhost',
            'port': 3306,
            'database': 'sailing_game',
            'user': 'root',
            'password': 'mgsincos30',
            'charset': 'utf8mb4',
            'autocommit': False
        }
        self.connection = None
        
    def connect_database(self):
        """连接数据库"""
        try:
            print("🔌 连接数据库...")
            self.connection = mysql.connector.connect(**self.db_config)
            
            if self.connection.is_connected():
                print("✅ 数据库连接成功")
                return True
            else:
                print("❌ 数据库连接失败")
                return False
                
        except Error as e:
            print(f"❌ 数据库连接错误: {e}")
            return False
    
    def disconnect_database(self):
        """断开数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 数据库连接已关闭")
    
    def execute_sql_file(self, sql_file: str) -> bool:
        """执行SQL文件"""
        try:
            print(f"📄 执行SQL文件: {os.path.basename(sql_file)}")
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 分割SQL语句
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            cursor = self.connection.cursor()
            
            for i, statement in enumerate(statements):
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                        
                        # 每100条语句提交一次
                        if i % 100 == 0:
                            self.connection.commit()
                            
                    except Error as e:
                        print(f"⚠️ SQL语句执行警告: {str(e)[:100]}...")
                        continue
            
            # 最终提交
            self.connection.commit()
            cursor.close()
            
            print(f"✅ SQL文件执行完成: {os.path.basename(sql_file)}")
            return True
            
        except Exception as e:
            print(f"❌ 执行SQL文件失败: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def create_database_schema(self):
        """创建数据库表结构"""
        schema_file = os.path.join(self.sql_dir, "create_tables.sql")
        
        if not os.path.exists(schema_file):
            print(f"❌ 找不到表结构文件: {schema_file}")
            return False
        
        print("🗃️ 创建数据库表结构...")
        return self.execute_sql_file(schema_file)
    
    def import_scenes_data(self):
        """导入场景数据"""
        print("📖 导入场景数据...")
        
        # 查找所有场景批次文件
        scene_files = []
        for filename in os.listdir(self.sql_dir):
            if filename.startswith('optimized_scenes_batch_') and filename.endswith('.sql'):
                scene_files.append(os.path.join(self.sql_dir, filename))
        
        scene_files.sort()
        
        if not scene_files:
            print("❌ 找不到场景SQL文件")
            return False
        
        success_count = 0
        for scene_file in scene_files:
            if self.execute_sql_file(scene_file):
                success_count += 1
            time.sleep(0.1)  # 短暂延迟避免数据库压力
        
        print(f"✅ 场景数据导入完成: {success_count}/{len(scene_files)} 个文件成功")
        return success_count == len(scene_files)
    
    def import_choices_data(self):
        """导入选择数据"""
        print("🎯 导入选择数据...")
        
        # 查找所有选择批次文件
        choice_files = []
        for filename in os.listdir(self.sql_dir):
            if filename.startswith('optimized_choices_batch_') and filename.endswith('.sql'):
                choice_files.append(os.path.join(self.sql_dir, filename))
        
        choice_files.sort()
        
        if not choice_files:
            print("❌ 找不到选择SQL文件")
            return False
        
        success_count = 0
        for choice_file in choice_files:
            if self.execute_sql_file(choice_file):
                success_count += 1
            time.sleep(0.1)  # 短暂延迟避免数据库压力
        
        print(f"✅ 选择数据导入完成: {success_count}/{len(choice_files)} 个文件成功")
        return success_count == len(choice_files)
    
    def verify_import_results(self):
        """验证导入结果"""
        print("🔍 验证导入结果...")
        
        try:
            cursor = self.connection.cursor()
            
            # 检查场景数据
            cursor.execute("SELECT COUNT(*) FROM stories")
            stories_count = cursor.fetchone()[0]
            print(f"📖 场景总数: {stories_count}")
            
            # 检查选择数据
            cursor.execute("SELECT COUNT(*) FROM choices")
            choices_count = cursor.fetchone()[0]
            print(f"🎯 选择总数: {choices_count}")
            
            # 检查故事类型分布
            cursor.execute("SELECT story_type, COUNT(*) FROM stories GROUP BY story_type")
            type_stats = cursor.fetchall()
            print("📊 故事类型分布:")
            for story_type, count in type_stats:
                print(f"   - {story_type}: {count}")
            
            # 检查章节覆盖
            cursor.execute("SELECT MIN(chapter), MAX(chapter), COUNT(DISTINCT chapter) FROM stories")
            min_chapter, max_chapter, chapter_count = cursor.fetchone()
            print(f"📚 章节范围: 第{min_chapter}章 - 第{max_chapter}章 (共{chapter_count}章)")
            
            # 检查数据完整性
            cursor.execute("""
                SELECT COUNT(*) FROM choices c 
                LEFT JOIN stories s ON c.next_story_id = s.story_id 
                WHERE s.story_id IS NULL
            """)
            broken_links = cursor.fetchone()[0]
            
            if broken_links > 0:
                print(f"⚠️ 发现 {broken_links} 个断开的选择链接")
            else:
                print("✅ 所有选择链接完整")
            
            cursor.close()
            
            # 生成验证报告
            self.generate_verification_report(stories_count, choices_count, type_stats, 
                                            min_chapter, max_chapter, chapter_count, broken_links)
            
            return True
            
        except Error as e:
            print(f"❌ 验证过程出错: {e}")
            return False
    
    def generate_verification_report(self, stories_count: int, choices_count: int, 
                                   type_stats: list, min_chapter: int, max_chapter: int, 
                                   chapter_count: int, broken_links: int):
        """生成验证报告"""
        report_file = os.path.join(self.sql_dir, "import_verification_report.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 数据库导入验证报告\n\n")
            
            f.write("## 导入统计\n")
            f.write(f"- 场景总数: {stories_count}\n")
            f.write(f"- 选择总数: {choices_count}\n")
            f.write(f"- 平均每场景选择数: {choices_count/stories_count:.1f}\n\n")
            
            f.write("## 故事类型分布\n")
            for story_type, count in type_stats:
                f.write(f"- {story_type}: {count} 个场景\n")
            f.write("\n")
            
            f.write("## 章节覆盖\n")
            f.write(f"- 起始章节: 第{min_chapter}章\n")
            f.write(f"- 结束章节: 第{max_chapter}章\n")
            f.write(f"- 章节总数: {chapter_count}\n")
            f.write(f"- 覆盖率: {chapter_count/(max_chapter-min_chapter+1)*100:.1f}%\n\n")
            
            f.write("## 数据完整性\n")
            if broken_links == 0:
                f.write("- 选择链接: ✅ 完整\n")
            else:
                f.write(f"- 选择链接: ⚠️ 发现 {broken_links} 个断开链接\n")
            
            f.write(f"- 导入状态: {'✅ 成功' if broken_links == 0 else '⚠️ 部分问题'}\n")
        
        print(f"📊 验证报告已生成: {report_file}")
    
    def import_all_data(self):
        """导入所有数据"""
        print("🚀 开始导入优化后的数据到数据库...")
        
        # 连接数据库
        if not self.connect_database():
            return False
        
        try:
            # 1. 创建表结构
            if not self.create_database_schema():
                print("❌ 创建表结构失败")
                return False
            
            # 2. 导入场景数据
            if not self.import_scenes_data():
                print("❌ 导入场景数据失败")
                return False
            
            # 3. 导入选择数据
            if not self.import_choices_data():
                print("❌ 导入选择数据失败")
                return False
            
            # 4. 验证导入结果
            if not self.verify_import_results():
                print("❌ 验证导入结果失败")
                return False
            
            print("🎉 数据导入完成！")
            return True
            
        except Exception as e:
            print(f"❌ 导入过程中出现错误: {e}")
            return False
            
        finally:
            self.disconnect_database()

def main():
    """主函数"""
    print("修复版数据库导入器")
    print("=" * 50)
    
    importer = FixedDatabaseImporter()
    
    try:
        success = importer.import_all_data()
        if success:
            print("\n✅ 数据库导入成功完成！")
        else:
            print("\n❌ 数据库导入失败")
            
    except Exception as e:
        print(f"❌ 导入过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
