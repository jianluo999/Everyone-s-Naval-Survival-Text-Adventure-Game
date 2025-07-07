#!/usr/bin/env python3
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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for i in range(1, 18):
        sql_file = os.path.join(base_dir, f"optimized_scenes_batch_{i:03d}.sql")
        success, error = run_mysql_command(sql_file)
        if success:
            print(f"✅ 场景批次 {i}/17")
        else:
            print(f"❌ 场景批次 {i} 失败: {error}")

    # 导入选择数据
    print("🎯 导入优化选择数据...")
    for i in range(1, 57):
        sql_file = os.path.join(base_dir, f"optimized_choices_batch_{i:03d}.sql")
        success, error = run_mysql_command(sql_file)
        if success:
            print(f"✅ 选择批次 {i}/56")
        else:
            print(f"❌ 选择批次 {i} 失败: {error}")
    
    print("🎉 优化数据导入完成！")

if __name__ == "__main__":
    main()
