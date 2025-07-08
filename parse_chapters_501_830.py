#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析501-830章节内容
将txt文件转换为结构化的章节数据
"""

import re
import json
import os
from typing import List, Dict

class ChapterParser:
    def __init__(self):
        self.input_file = "novel_texts/raw/全民大航海，我开局一条幽灵船(501-830章).txt"
        self.output_dir = "novel_texts/chapters"
        
    def parse_chapters(self) -> List[Dict]:
        """解析章节内容"""
        print("=== 开始解析501-830章节 ===")
        
        if not os.path.exists(self.input_file):
            print(f"❌ 文件不存在: {self.input_file}")
            return []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按章节分割
        chapter_pattern = r'^第(\d+)章\s+(.+?)$'
        lines = content.split('\n')
        
        chapters = []
        current_chapter = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检查是否是章节标题
            match = re.match(chapter_pattern, line)
            if match:
                # 保存上一章
                if current_chapter:
                    current_chapter['content'] = '\n'.join(current_content).strip()
                    chapters.append(current_chapter)
                
                # 开始新章
                chapter_num = int(match.group(1))
                chapter_title = match.group(2).strip()
                
                current_chapter = {
                    'chapter_number': chapter_num,
                    'title': chapter_title,
                    'content': ''
                }
                current_content = []
                
                print(f"解析第{chapter_num}章: {chapter_title}")
                
            elif current_chapter:
                # 添加到当前章节内容
                if not line.startswith('《') and not line.startswith('作者：') and not line.startswith('来源：') and not line.startswith('网址：'):
                    current_content.append(line)
        
        # 保存最后一章
        if current_chapter:
            current_chapter['content'] = '\n'.join(current_content).strip()
            chapters.append(current_chapter)
        
        print(f"✅ 解析完成，共{len(chapters)}章")
        return chapters
    
    def save_chapters(self, chapters: List[Dict]):
        """保存章节数据"""
        print("=== 保存章节数据 ===")
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 保存为JSON文件
        output_file = os.path.join(self.output_dir, "chapters_501_830.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 章节数据已保存到: {output_file}")
        
        # 统计信息
        total_chars = sum(len(ch['content']) for ch in chapters)
        avg_chars = total_chars / len(chapters) if chapters else 0
        
        print(f"统计信息:")
        print(f"  章节数量: {len(chapters)}")
        print(f"  总字符数: {total_chars:,}")
        print(f"  平均每章字符数: {avg_chars:.0f}")
        
        # 显示前几章的信息
        print(f"\n前5章预览:")
        for i, chapter in enumerate(chapters[:5]):
            print(f"  第{chapter['chapter_number']}章: {chapter['title']}")
            print(f"    内容长度: {len(chapter['content'])} 字符")
            print(f"    内容预览: {chapter['content'][:50]}...")
            print()
    
    def validate_chapters(self, chapters: List[Dict]) -> bool:
        """验证章节数据"""
        print("=== 验证章节数据 ===")
        
        if not chapters:
            print("❌ 没有解析到任何章节")
            return False
        
        # 检查章节连续性
        expected_start = 501
        expected_end = 830
        
        chapter_numbers = [ch['chapter_number'] for ch in chapters]
        chapter_numbers.sort()
        
        missing_chapters = []
        for i in range(expected_start, expected_end + 1):
            if i not in chapter_numbers:
                missing_chapters.append(i)
        
        if missing_chapters:
            print(f"⚠️ 缺失章节: {missing_chapters[:10]}{'...' if len(missing_chapters) > 10 else ''}")
        
        # 检查内容质量
        empty_chapters = [ch for ch in chapters if not ch['content'].strip()]
        if empty_chapters:
            print(f"⚠️ 空内容章节: {len(empty_chapters)}个")
        
        # 检查标题
        no_title_chapters = [ch for ch in chapters if not ch['title'].strip()]
        if no_title_chapters:
            print(f"⚠️ 无标题章节: {len(no_title_chapters)}个")
        
        print(f"✅ 验证完成")
        print(f"  有效章节: {len(chapters) - len(empty_chapters)}")
        print(f"  章节范围: {min(chapter_numbers)} - {max(chapter_numbers)}")
        
        return len(empty_chapters) == 0 and len(no_title_chapters) == 0
    
    def run(self):
        """运行完整解析流程"""
        print("章节解析器 - 501-830章")
        print("=" * 50)
        
        # 1. 解析章节
        chapters = self.parse_chapters()
        
        if not chapters:
            print("❌ 解析失败")
            return False
        
        # 2. 验证数据
        is_valid = self.validate_chapters(chapters)
        
        # 3. 保存数据
        self.save_chapters(chapters)
        
        if is_valid:
            print("\n🎉 章节解析完成且验证通过!")
        else:
            print("\n⚠️ 章节解析完成但存在问题")
        
        return True

def main():
    parser = ChapterParser()
    parser.run()

if __name__ == "__main__":
    main()
