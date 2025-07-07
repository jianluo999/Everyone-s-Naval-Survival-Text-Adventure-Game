#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的数据导入脚本
"""

import os
import subprocess
import time

def run_mysql_command(sql_file):
    """执行MySQL命令"""
    cmd = f'mysql -u root -pmgsincos30 sailing_game < "{sql_file}"'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def import_all_data():
    """导入所有数据"""
    sql_dir = "novel_texts/sql_batches"
    
    print("🚀 开始批量导入数据...")
    
    # 导入场景数据
    print("📖 导入场景数据...")
    scene_files = [f for f in os.listdir(sql_dir) if f.startswith('scenes_batch_')]
    scene_files.sort()
    
    success_scenes = 0
    for i, file in enumerate(scene_files, 1):
        file_path = os.path.join(sql_dir, file)
        print(f"导入场景批次 {i}/{len(scene_files)}: {file}")
        
        success, error = run_mysql_command(file_path)
        if success:
            success_scenes += 1
            print(f"✅ 成功")
        else:
            print(f"❌ 失败: {error}")
        
        time.sleep(0.1)  # 短暂延迟
    
    # 导入选择数据
    print("\n🎯 导入选择数据...")
    choice_files = [f for f in os.listdir(sql_dir) if f.startswith('choices_batch_')]
    choice_files.sort()
    
    success_choices = 0
    for i, file in enumerate(choice_files, 1):
        file_path = os.path.join(sql_dir, file)
        print(f"导入选择批次 {i}/{len(choice_files)}: {file}")
        
        success, error = run_mysql_command(file_path)
        if success:
            success_choices += 1
            print(f"✅ 成功")
        else:
            print(f"❌ 失败: {error}")
        
        time.sleep(0.1)  # 短暂延迟
    
    print(f"\n🎉 导入完成！")
    print(f"📊 场景批次：{success_scenes}/{len(scene_files)} 成功")
    print(f"📊 选择批次：{success_choices}/{len(choice_files)} 成功")
    
    # 检查最终结果
    print("\n📊 检查导入结果...")
    success, result = run_mysql_command_output('SELECT COUNT(*) FROM stories WHERE chapter >= 1')
    if success:
        print(f"✅ 总场景数：{result.strip()}")
    
    success, result = run_mysql_command_output('SELECT COUNT(*) FROM choices')
    if success:
        print(f"✅ 总选择数：{result.strip()}")

def run_mysql_command_output(sql):
    """执行MySQL命令并返回输出"""
    cmd = f'mysql -u root -pmgsincos30 sailing_game -e "{sql}" -s -N'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    import_all_data()
