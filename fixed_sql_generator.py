#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版SQL生成器 - 将优化后的场景和选择数据转换为SQL导入脚本
确保数据能正确导入到MySQL数据库
"""

import json
import os
from typing import List, Dict

class FixedSQLGenerator:
    def __init__(self):
        self.scenes_file = "novel_texts/optimized_scenes/optimized_scenes.json"
        self.choices_file = "novel_texts/optimized_scenes/optimized_choices.json"
        self.output_dir = "novel_texts/optimized_sql"
        self.batch_size = 500
        
    def escape_sql_string(self, text: str) -> str:
        """转义SQL字符串"""
        if text is None:
            return 'NULL'
        
        # 转义单引号、反斜杠和换行符
        text = str(text).replace('\\', '\\\\')
        text = text.replace("'", "\\'")
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\r')
        text = text.replace('\t', '\\t')
        
        return f"'{text}'"
    
    def generate_scenes_sql(self, scenes: List[Dict]):
        """生成场景SQL文件"""
        print("📖 生成优化场景SQL文件...")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        total_batches = (len(scenes) + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(scenes))
            batch_scenes = scenes[start_idx:end_idx]
            
            filename = f"{self.output_dir}/optimized_scenes_batch_{batch_num + 1:03d}.sql"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("-- 优化场景数据批次 {}\n".format(batch_num + 1))
                f.write("-- 清理现有数据（仅第一批次）\n")
                if batch_num == 0:
                    f.write("DELETE FROM stories;\n")
                    f.write("ALTER TABLE stories AUTO_INCREMENT = 1;\n\n")
                
                f.write("INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) VALUES\n")
                
                values = []
                for scene in batch_scenes:
                    value = "({}, {}, {}, {}, {}, {}, {})".format(
                        self.escape_sql_string(scene['story_id']),
                        self.escape_sql_string(scene['title']),
                        self.escape_sql_string(scene['content']),
                        scene['chapter'],
                        scene['scene'],
                        self.escape_sql_string(scene['story_type']),
                        1 if scene.get('is_ending', False) else 0
                    )
                    values.append(value)
                
                f.write(',\n'.join(values))
                f.write(';\n\n')
                
                f.write("-- 批次统计\n")
                f.write(f"-- 本批次场景数: {len(batch_scenes)}\n")
                f.write(f"-- 批次范围: {start_idx + 1} - {end_idx}\n")
            
            print(f"✅ 生成场景批次 {batch_num + 1}/{total_batches}: {filename}")
    
    def generate_choices_sql(self, choices: List[Dict]):
        """生成选择SQL文件"""
        print("🎯 生成优化选择SQL文件...")
        
        total_batches = (len(choices) + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(choices))
            batch_choices = choices[start_idx:end_idx]
            
            filename = f"{self.output_dir}/optimized_choices_batch_{batch_num + 1:03d}.sql"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("-- 优化选择数据批次 {}\n".format(batch_num + 1))
                f.write("-- 清理现有数据（仅第一批次）\n")
                if batch_num == 0:
                    f.write("DELETE FROM choices;\n")
                    f.write("ALTER TABLE choices AUTO_INCREMENT = 1;\n\n")
                
                f.write("INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES\n")
                
                values = []
                for choice in batch_choices:
                    value = "({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
                        self.escape_sql_string(choice['story_id']),
                        self.escape_sql_string(choice['text']),
                        self.escape_sql_string(choice['next_story_id']),
                        self.escape_sql_string(choice.get('requirements', '')),
                        1 if choice.get('is_available', True) else 0,
                        choice.get('health_cost', 0),
                        choice.get('health_reward', 0),
                        choice.get('gold_cost', 0),
                        choice.get('gold_reward', 0),
                        choice.get('experience_reward', 0)
                    )
                    values.append(value)
                
                f.write(',\n'.join(values))
                f.write(';\n\n')
                
                f.write("-- 批次统计\n")
                f.write(f"-- 本批次选择数: {len(batch_choices)}\n")
                f.write(f"-- 批次范围: {start_idx + 1} - {end_idx}\n")
            
            print(f"✅ 生成选择批次 {batch_num + 1}/{total_batches}: {filename}")
    
    def generate_master_import_script(self, scenes_batches: int, choices_batches: int):
        """生成主导入脚本"""
        script_file = f"{self.output_dir}/import_all_optimized_data.sql"
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write("-- 优化数据主导入脚本\n")
            f.write("-- 自动生成，用于导入所有优化后的场景和选择数据\n\n")
            
            f.write("-- 设置MySQL参数\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
            f.write("SET UNIQUE_CHECKS = 0;\n")
            f.write("SET AUTOCOMMIT = 0;\n\n")
            
            f.write("-- 导入场景数据\n")
            for i in range(1, scenes_batches + 1):
                f.write(f"SOURCE optimized_scenes_batch_{i:03d}.sql;\n")
            f.write("\n")
            
            f.write("-- 导入选择数据\n")
            for i in range(1, choices_batches + 1):
                f.write(f"SOURCE optimized_choices_batch_{i:03d}.sql;\n")
            f.write("\n")
            
            f.write("-- 提交事务\n")
            f.write("COMMIT;\n\n")
            
            f.write("-- 恢复MySQL参数\n")
            f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
            f.write("SET UNIQUE_CHECKS = 1;\n")
            f.write("SET AUTOCOMMIT = 1;\n\n")
            
            f.write("-- 验证导入结果\n")
            f.write("SELECT COUNT(*) as total_stories FROM stories;\n")
            f.write("SELECT COUNT(*) as total_choices FROM choices;\n")
            f.write("SELECT story_type, COUNT(*) as count FROM stories GROUP BY story_type;\n")
        
        print(f"📜 生成主导入脚本: {script_file}")
    
    def generate_database_schema(self):
        """生成数据库表结构"""
        schema_file = f"{self.output_dir}/create_tables.sql"
        
        with open(schema_file, 'w', encoding='utf-8') as f:
            f.write("-- 数据库表结构创建脚本\n")
            f.write("-- 确保数据库表结构正确\n\n")
            
            f.write("-- 创建stories表\n")
            f.write("""CREATE TABLE IF NOT EXISTS stories (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    story_id VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    chapter INT NOT NULL,
    scene INT NOT NULL,
    story_type VARCHAR(50) DEFAULT 'general',
    is_ending BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_story_id (story_id),
    INDEX idx_chapter (chapter),
    INDEX idx_story_type (story_type)
);\n\n""")
            
            f.write("-- 创建choices表\n")
            f.write("""CREATE TABLE IF NOT EXISTS choices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    story_id VARCHAR(50) NOT NULL,
    text VARCHAR(500) NOT NULL,
    next_story_id VARCHAR(50) NOT NULL,
    requirements VARCHAR(200) DEFAULT '',
    is_available BOOLEAN DEFAULT TRUE,
    health_cost INT DEFAULT 0,
    health_reward INT DEFAULT 0,
    gold_cost INT DEFAULT 0,
    gold_reward INT DEFAULT 0,
    experience_reward INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_story_id (story_id),
    INDEX idx_next_story_id (next_story_id),
    FOREIGN KEY (story_id) REFERENCES stories(story_id) ON DELETE CASCADE
);\n\n""")
        
        print(f"🗃️ 生成数据库表结构: {schema_file}")
    
    def generate_sql_files(self):
        """生成所有SQL文件"""
        print("🚀 开始生成SQL导入文件...")
        
        # 检查输入文件
        if not os.path.exists(self.scenes_file):
            print(f"❌ 找不到场景文件: {self.scenes_file}")
            return False
        
        if not os.path.exists(self.choices_file):
            print(f"❌ 找不到选择文件: {self.choices_file}")
            return False
        
        # 加载数据
        with open(self.scenes_file, 'r', encoding='utf-8') as f:
            scenes = json.load(f)
        
        with open(self.choices_file, 'r', encoding='utf-8') as f:
            choices = json.load(f)
        
        print(f"📚 加载了 {len(scenes)} 个场景")
        print(f"🎯 加载了 {len(choices)} 个选择")
        
        # 生成数据库表结构
        self.generate_database_schema()
        
        # 生成场景SQL
        self.generate_scenes_sql(scenes)
        scenes_batches = (len(scenes) + self.batch_size - 1) // self.batch_size
        
        # 生成选择SQL
        self.generate_choices_sql(choices)
        choices_batches = (len(choices) + self.batch_size - 1) // self.batch_size
        
        # 生成主导入脚本
        self.generate_master_import_script(scenes_batches, choices_batches)
        
        # 生成统计报告
        self.generate_sql_report(len(scenes), len(choices), scenes_batches, choices_batches)
        
        print("🎉 SQL文件生成完成！")
        return True
    
    def generate_sql_report(self, scenes_count: int, choices_count: int, 
                           scenes_batches: int, choices_batches: int):
        """生成SQL生成报告"""
        report_file = f"{self.output_dir}/sql_generation_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# SQL生成报告\n\n")
            
            f.write("## 数据统计\n")
            f.write(f"- 场景数量: {scenes_count}\n")
            f.write(f"- 选择数量: {choices_count}\n")
            f.write(f"- 场景批次: {scenes_batches}\n")
            f.write(f"- 选择批次: {choices_batches}\n")
            f.write(f"- 批次大小: {self.batch_size}\n\n")
            
            f.write("## 生成文件\n")
            f.write("- create_tables.sql - 数据库表结构\n")
            f.write("- import_all_optimized_data.sql - 主导入脚本\n")
            f.write(f"- optimized_scenes_batch_001.sql 到 optimized_scenes_batch_{scenes_batches:03d}.sql\n")
            f.write(f"- optimized_choices_batch_001.sql 到 optimized_choices_batch_{choices_batches:03d}.sql\n\n")
            
            f.write("## 导入说明\n")
            f.write("1. 首先运行 create_tables.sql 创建表结构\n")
            f.write("2. 然后运行 import_all_optimized_data.sql 导入所有数据\n")
            f.write("3. 或者手动按顺序运行各个批次文件\n\n")
        
        print(f"📊 SQL生成报告: {report_file}")

def main():
    """主函数"""
    print("修复版SQL生成器")
    print("=" * 50)
    
    generator = FixedSQLGenerator()
    
    try:
        success = generator.generate_sql_files()
        if success:
            print(f"\n✅ SQL文件生成成功！")
            print(f"📁 输出目录: {generator.output_dir}")
        else:
            print("\n❌ SQL文件生成失败")
            
    except Exception as e:
        print(f"❌ 生成过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
