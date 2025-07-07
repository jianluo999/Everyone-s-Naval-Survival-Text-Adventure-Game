#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版批量导入脚本 - 生成SQL文件分批导入
"""

import json
import os

def generate_batch_sql_files():
    """生成分批SQL导入文件"""
    print("🚀 开始生成批量SQL导入文件...")
    
    # 加载数据
    print("📂 加载数据文件...")
    with open('novel_texts/game_scenes/all_scenes.json', 'r', encoding='utf-8') as f:
        scenes_data = json.load(f)
    
    with open('novel_texts/game_scenes/all_choices.json', 'r', encoding='utf-8') as f:
        choices_data = json.load(f)
    
    print(f"✅ 数据加载完成：{len(scenes_data)} 个场景，{len(choices_data)} 个选择")
    
    # 创建输出目录
    output_dir = "novel_texts/sql_batches"
    os.makedirs(output_dir, exist_ok=True)
    
    # 分批大小
    batch_size = 500
    
    # 生成场景SQL文件
    print("📖 生成场景SQL文件...")
    scenes_batches = (len(scenes_data) + batch_size - 1) // batch_size
    
    for i in range(0, len(scenes_data), batch_size):
        batch_num = i // batch_size + 1
        batch = scenes_data[i:i + batch_size]
        
        sql_file = os.path.join(output_dir, f"scenes_batch_{batch_num:03d}.sql")
        
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("USE sailing_game;\n")
            f.write("SET NAMES utf8mb4;\n\n")
            f.write(f"-- 场景批次 {batch_num}/{scenes_batches}\n")
            f.write(f"-- 包含 {len(batch)} 个场景\n\n")
            
            for scene in batch:
                # 转义单引号
                title = scene['title'].replace("'", "''")
                content = scene['content'].replace("'", "''")
                
                f.write(f"INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) VALUES ")
                f.write(f"('{scene['story_id']}', '{title}', '{content}', ")
                f.write(f"{scene['chapter']}, {scene['scene']}, '{scene['story_type']}', {1 if scene['is_ending'] else 0});\n")
        
        print(f"✅ 生成场景批次 {batch_num}/{scenes_batches}")
    
    # 生成选择SQL文件
    print("🎯 生成选择SQL文件...")
    choices_batches = (len(choices_data) + batch_size - 1) // batch_size
    
    for i in range(0, len(choices_data), batch_size):
        batch_num = i // batch_size + 1
        batch = choices_data[i:i + batch_size]
        
        sql_file = os.path.join(output_dir, f"choices_batch_{batch_num:03d}.sql")
        
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("USE sailing_game;\n")
            f.write("SET NAMES utf8mb4;\n\n")
            f.write(f"-- 选择批次 {batch_num}/{choices_batches}\n")
            f.write(f"-- 包含 {len(batch)} 个选择\n\n")
            
            for choice in batch:
                # 转义单引号
                text = choice['text'].replace("'", "''")
                
                f.write(f"INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, ")
                f.write(f"health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES ")
                f.write(f"('{choice['story_id']}', '{text}', '{choice['next_story_id']}', ")
                f.write(f"'{choice['requirements']}', {1 if choice['is_available'] else 0}, ")
                f.write(f"{choice['health_cost']}, {choice['health_reward']}, {choice['gold_cost']}, ")
                f.write(f"{choice['gold_reward']}, {choice['experience_reward']});\n")
        
        print(f"✅ 生成选择批次 {batch_num}/{choices_batches}")
    
    # 生成导入脚本
    import_script = os.path.join(output_dir, "import_all.bat")
    with open(import_script, 'w', encoding='utf-8') as f:
        f.write("@echo off\n")
        f.write("echo 开始批量导入数据...\n\n")
        
        # 导入场景
        for i in range(1, scenes_batches + 1):
            f.write(f"echo 导入场景批次 {i}/{scenes_batches}...\n")
            f.write(f"mysql -u root -pmgsincos30 < scenes_batch_{i:03d}.sql\n")
            f.write("if %errorlevel% neq 0 (\n")
            f.write(f"    echo 场景批次 {i} 导入失败！\n")
            f.write("    pause\n")
            f.write("    exit /b 1\n")
            f.write(")\n\n")
        
        # 导入选择
        for i in range(1, choices_batches + 1):
            f.write(f"echo 导入选择批次 {i}/{choices_batches}...\n")
            f.write(f"mysql -u root -pmgsincos30 < choices_batch_{i:03d}.sql\n")
            f.write("if %errorlevel% neq 0 (\n")
            f.write(f"    echo 选择批次 {i} 导入失败！\n")
            f.write("    pause\n")
            f.write("    exit /b 1\n")
            f.write(")\n\n")
        
        f.write("echo 所有数据导入完成！\n")
        f.write("pause\n")
    
    print(f"\n🎉 SQL文件生成完成！")
    print(f"📁 输出目录: {output_dir}")
    print(f"📊 场景文件: {scenes_batches} 个")
    print(f"📊 选择文件: {choices_batches} 个")
    print(f"🚀 运行 {import_script} 开始导入")

if __name__ == "__main__":
    generate_batch_sql_files()
