#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情质量检查脚本
检查转换后的游戏剧情文件中的问题
"""

import os
import re
from pathlib import Path
from collections import Counter

class StoryQualityChecker:
    def __init__(self):
        self.issues = []
        self.stats = {
            'total_scenes': 0,
            'total_choices': 0,
            'repeated_choices': 0,
            'text_errors': 0
        }
    
    def check_all_files(self, processed_dir="novel_texts/processed"):
        """检查所有处理后的文件"""
        print("🔍 开始检查剧情质量...")
        
        processed_path = Path(processed_dir)
        if not processed_path.exists():
            print(f"❌ 目录不存在: {processed_dir}")
            return
        
        # 检查所有游戏文件
        for file_path in processed_path.glob("*_game.md"):
            self.check_file(file_path)
        
        self.print_report()
    
    def check_file(self, file_path):
        """检查单个文件"""
        print(f"📄 检查文件: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文本错误
        self.check_text_errors(content, file_path.name)
        
        # 检查场景结构
        self.check_scene_structure(content, file_path.name)
        
        # 检查选择分支
        self.check_choices(content, file_path.name)
    
    def check_text_errors(self, content, filename):
        """检查文本错误"""
        errors = []
        
        # 检查常见的替换错误
        error_patterns = [
            (r'其你', '其他'),
            (r'你们你', '你们他'),
            (r'你的你', '你的他'),
            (r'你说你', '你说他'),
            (r'你看你', '你看他'),
        ]
        
        for pattern, correct in error_patterns:
            matches = re.findall(pattern, content)
            if matches:
                errors.append(f"发现错误替换: '{pattern}' 应为 '{correct}', 出现 {len(matches)} 次")
                self.stats['text_errors'] += len(matches)
        
        if errors:
            self.issues.append({
                'file': filename,
                'type': 'text_error',
                'details': errors
            })
    
    def check_scene_structure(self, content, filename):
        """检查场景结构"""
        # 统计场景数量
        scenes = re.findall(r'## 场景 \d+', content)
        self.stats['total_scenes'] += len(scenes)
        
        # 检查场景ID格式
        scene_ids = re.findall(r'\*\*场景ID\*\*: (scene_\d+_\d+)', content)
        
        issues = []
        for i, scene_id in enumerate(scene_ids, 1):
            expected_pattern = r'scene_\d+_\d+'
            if not re.match(expected_pattern, scene_id):
                issues.append(f"场景 {i} ID格式错误: {scene_id}")
        
        if issues:
            self.issues.append({
                'file': filename,
                'type': 'scene_structure',
                'details': issues
            })
    
    def check_choices(self, content, filename):
        """检查选择分支"""
        # 提取所有选择
        choice_sections = re.findall(r'### 选择分支\n\n(.*?)(?=\n---|\n##|\Z)', content, re.DOTALL)
        
        all_choices = []
        for section in choice_sections:
            choices = re.findall(r'\d+\. (.+)', section)
            all_choices.extend(choices)
            self.stats['total_choices'] += len(choices)
        
        # 检查重复选择
        choice_counter = Counter(all_choices)
        repeated = [(choice, count) for choice, count in choice_counter.items() if count > 3]
        
        if repeated:
            self.stats['repeated_choices'] += len(repeated)
            self.issues.append({
                'file': filename,
                'type': 'repeated_choices',
                'details': [f"'{choice}' 重复 {count} 次" for choice, count in repeated]
            })
    
    def print_report(self):
        """打印检查报告"""
        print("\n" + "="*50)
        print("📊 剧情质量检查报告")
        print("="*50)
        
        print(f"📈 统计信息:")
        print(f"  总场景数: {self.stats['total_scenes']}")
        print(f"  总选择数: {self.stats['total_choices']}")
        print(f"  文本错误: {self.stats['text_errors']}")
        print(f"  重复选择: {self.stats['repeated_choices']}")
        
        if not self.issues:
            print("\n✅ 恭喜！没有发现质量问题。")
            return
        
        print(f"\n⚠️ 发现 {len(self.issues)} 个问题:")
        
        for issue in self.issues:
            print(f"\n📁 文件: {issue['file']}")
            print(f"🔍 问题类型: {issue['type']}")
            for detail in issue['details']:
                print(f"  - {detail}")
    
    def fix_text_errors(self, processed_dir="novel_texts/processed"):
        """自动修复文本错误"""
        print("\n🔧 开始自动修复文本错误...")
        
        processed_path = Path(processed_dir)
        fixed_files = 0
        
        for file_path in processed_path.glob("*_game.md"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 修复常见错误
            fixes = [
                (r'其你', '其他'),
                (r'你们你', '你们他'),
                (r'你的你', '你的他'),
                (r'你说你', '你说他'),
                (r'你看你', '你看他'),
            ]
            
            for pattern, replacement in fixes:
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files += 1
                print(f"✅ 修复文件: {file_path.name}")
        
        print(f"\n🎉 修复完成！共修复 {fixed_files} 个文件")

def main():
    checker = StoryQualityChecker()
    
    # 检查质量
    checker.check_all_files()
    
    # 询问是否自动修复
    if checker.stats['text_errors'] > 0:
        response = input("\n是否自动修复文本错误？(y/n): ")
        if response.lower() == 'y':
            checker.fix_text_errors()
            print("\n重新检查修复结果...")
            checker = StoryQualityChecker()
            checker.check_all_files()

if __name__ == "__main__":
    main()
