#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试批量加载功能
验证转换后的剧情文件是否能被正确加载
"""

import os
import re
from pathlib import Path

def test_batch_loading():
    """测试批量加载功能"""
    print("🧪 开始测试批量加载功能...")
    
    # 检查处理后的文件目录
    processed_dir = Path("novel_texts/processed")
    if not processed_dir.exists():
        print("❌ 处理后的文件目录不存在")
        return False
    
    # 查找所有游戏文件
    game_files = list(processed_dir.glob("*_game.md"))
    if not game_files:
        print("❌ 没有找到游戏文件")
        return False
    
    print(f"📁 找到 {len(game_files)} 个游戏文件")
    
    total_scenes = 0
    total_choices = 0
    
    for file_path in sorted(game_files):
        print(f"\n📄 测试文件: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 测试场景解析
            scenes = test_scene_parsing(content)
            choices = test_choice_parsing(content)
            
            total_scenes += scenes
            total_choices += choices
            
            print(f"  ✅ 场景: {scenes}, 选择: {choices}")
            
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
            return False
    
    print(f"\n📊 测试结果:")
    print(f"  总场景数: {total_scenes}")
    print(f"  总选择数: {total_choices}")
    print(f"  文件数量: {len(game_files)}")
    
    if total_scenes > 0:
        print("✅ 批量加载功能测试通过！")
        return True
    else:
        print("❌ 批量加载功能测试失败！")
        return False

def test_scene_parsing(content):
    """测试场景解析"""
    # 使用与DataInitializer相同的正则表达式
    scene_pattern = re.compile(
        r"## 场景 (\d+)\s*\n\s*\*\*场景ID\*\*: (scene_\d+_\d+)\s*\n\s*(.*?)(?=\n### 选择分支|\n---|\n## 场景|\Z)", 
        re.DOTALL
    )
    
    matches = scene_pattern.findall(content)
    
    for match in matches:
        scene_number, scene_id, scene_content = match
        
        # 验证场景ID格式
        if not re.match(r'scene_\d+_\d+', scene_id):
            raise ValueError(f"场景ID格式错误: {scene_id}")
        
        # 验证内容不为空
        if not scene_content.strip():
            raise ValueError(f"场景内容为空: {scene_id}")
    
    return len(matches)

def test_choice_parsing(content):
    """测试选择解析"""
    # 查找选择分支
    choice_sections = re.findall(r'### 选择分支\n\n(.*?)(?=\n---|\n##|\Z)', content, re.DOTALL)
    
    total_choices = 0
    for section in choice_sections:
        choices = re.findall(r'\d+\. (.+)', section)
        total_choices += len(choices)
    
    return total_choices

def generate_test_report():
    """生成测试报告"""
    print("\n📋 生成测试报告...")
    
    processed_dir = Path("novel_texts/processed")
    game_files = list(processed_dir.glob("*_game.md"))
    
    report = []
    report.append("# 批量加载测试报告\n")
    report.append(f"**测试时间**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**文件数量**: {len(game_files)}\n")
    
    total_scenes = 0
    total_choices = 0
    
    report.append("\n## 文件详情\n")
    report.append("| 文件名 | 场景数 | 选择数 | 状态 |\n")
    report.append("|--------|--------|--------|------|\n")
    
    for file_path in sorted(game_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            scenes = test_scene_parsing(content)
            choices = test_choice_parsing(content)
            
            total_scenes += scenes
            total_choices += choices
            
            report.append(f"| {file_path.name} | {scenes} | {choices} | ✅ |\n")
            
        except Exception as e:
            report.append(f"| {file_path.name} | - | - | ❌ {str(e)} |\n")
    
    report.append(f"\n## 总计\n")
    report.append(f"- **总场景数**: {total_scenes}\n")
    report.append(f"- **总选择数**: {total_choices}\n")
    report.append(f"- **平均每文件场景数**: {total_scenes / len(game_files) if game_files else 0:.1f}\n")
    
    # 保存报告
    report_path = Path("novel_texts/BATCH_LOADING_TEST_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(''.join(report))
    
    print(f"✅ 测试报告已保存到: {report_path}")

def main():
    """主函数"""
    success = test_batch_loading()
    
    if success:
        generate_test_report()
        print("\n🎉 所有测试通过！批量加载功能正常工作。")
    else:
        print("\n💥 测试失败！需要检查批量加载功能。")
    
    return success

if __name__ == "__main__":
    main()
