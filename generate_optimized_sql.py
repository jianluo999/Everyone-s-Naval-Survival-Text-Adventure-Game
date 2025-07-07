#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成优化后数据的SQL导入文件
"""

import json
import os
from typing import List, Dict

class OptimizedSQLGenerator:
    def __init__(self):
        self.batch_size = 500
        self.output_dir = "novel_texts/optimized_sql"

    def escape_sql_string(self, text: str) -> str:
        """转义SQL字符串"""
        if text is None:
            return 'NULL'
        
        # 转义单引号和反斜杠
        text = str(text).replace('\\', '\\\\').replace("'", "\\'")
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
                        1 if scene['is_ending'] else 0
                    )
                    values.append(value)
                
                f.write(',\n'.join(values))
                f.write(';\n')
            
            print(f"✅ 生成场景批次 {batch_num + 1}/{total_batches}")

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
                f.write("INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES\n")
                
                values = []
                for choice in batch_choices:
                    value = "({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
                        self.escape_sql_string(choice['story_id']),
                        self.escape_sql_string(choice['text']),
                        self.escape_sql_string(choice['next_story_id']),
                        self.escape_sql_string(choice['requirements']),
                        1 if choice['is_available'] else 0,
                        choice['health_cost'],
                        choice['health_reward'],
                        choice['gold_cost'],
                        choice['gold_reward'],
                        choice['experience_reward']
                    )
                    values.append(value)
                
                f.write(',\n'.join(values))
                f.write(';\n')
            
            print(f"✅ 生成选择批次 {batch_num + 1}/{total_batches}")

    def generate_import_script(self, scene_batches: int, choice_batches: int):
        """生成导入脚本"""
        script_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os

def run_mysql_command(sql_file):
    cmd = [
        'mysql', 
        '-u', 'root', 
        '-pmgsincos30',
        'sailing_game'
    ]
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            result = subprocess.run(cmd, input=f.read(), text=True, capture_output=True)
        
        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("🚀 开始导入优化后的游戏数据...")
    
    # 清空现有数据
    print("🗑️ 清空现有数据...")
    clear_sql = '''
    DELETE FROM choices WHERE story_id LIKE 'story_%';
    DELETE FROM stories WHERE story_id LIKE 'story_%';
    '''
    
    cmd = ['mysql', '-u', 'root', '-pmgsincos30', 'sailing_game']
    subprocess.run(cmd, input=clear_sql, text=True)
    print("✅ 数据清空完成")
    
    # 导入场景数据
    print("📖 导入优化场景数据...")
    for i in range(1, {scene_batches + 1}):
        sql_file = f"optimized_scenes_batch_{{i:03d}}.sql"
        success, error = run_mysql_command(sql_file)
        if success:
            print(f"✅ 场景批次 {{i}}/{scene_batches}")
        else:
            print(f"❌ 场景批次 {{i}} 失败: {{error}}")
    
    # 导入选择数据
    print("🎯 导入优化选择数据...")
    for i in range(1, {choice_batches + 1}):
        sql_file = f"optimized_choices_batch_{{i:03d}}.sql"
        success, error = run_mysql_command(sql_file)
        if success:
            print(f"✅ 选择批次 {{i}}/{choice_batches}")
        else:
            print(f"❌ 选择批次 {{i}} 失败: {{error}}")
    
    print("🎉 优化数据导入完成！")

if __name__ == "__main__":
    main()
"""
        
        with open(f"{self.output_dir}/import_optimized.py", 'w', encoding='utf-8') as f:
            f.write(script_content)

    def generate_optimized_sql(self, scenes_file: str, choices_file: str):
        """生成优化后的SQL文件"""
        print("🚀 开始生成优化后的SQL导入文件...")
        
        # 加载优化数据
        with open(scenes_file, 'r', encoding='utf-8') as f:
            scenes = json.load(f)
        
        with open(choices_file, 'r', encoding='utf-8') as f:
            choices = json.load(f)
        
        print(f"📖 加载场景: {len(scenes)} 个")
        print(f"🎯 加载选择: {len(choices)} 个")
        
        # 生成SQL文件
        self.generate_scenes_sql(scenes)
        self.generate_choices_sql(choices)
        
        # 计算批次数量
        scene_batches = (len(scenes) + self.batch_size - 1) // self.batch_size
        choice_batches = (len(choices) + self.batch_size - 1) // self.batch_size
        
        # 生成导入脚本
        self.generate_import_script(scene_batches, choice_batches)
        
        print(f"🎉 SQL文件生成完成！")
        print(f"📁 输出目录: {self.output_dir}")
        print(f"📊 场景文件: {scene_batches} 个")
        print(f"📊 选择文件: {choice_batches} 个")
        print(f"🚀 运行 {self.output_dir}/import_optimized.py 开始导入")

def main():
    generator = OptimizedSQLGenerator()
    
    # 配置文件路径
    scenes_file = "novel_texts/optimized_scenes/optimized_scenes.json"
    choices_file = "novel_texts/optimized_scenes/optimized_choices.json"
    
    # 生成SQL文件
    generator.generate_optimized_sql(scenes_file, choices_file)

if __name__ == "__main__":
    main()
