#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节分割脚本 - 将500章小说分割成单独的章节文件
"""

import re
import os
from pathlib import Path

def split_novel_chapters(input_file, output_dir):
    """
    分割小说章节
    
    Args:
        input_file: 输入的完整小说文件路径
        output_dir: 输出目录路径
    """
    
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 读取原始文件
    print(f"📖 正在读取文件: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(input_file, 'r', encoding='gbk') as f:
            content = f.read()
    
    print(f"✅ 文件读取完成，总字符数: {len(content)}")
    
    # 章节分割正则表达式 - 匹配各种可能的章节标题格式
    chapter_patterns = [
        r'第([一二三四五六七八九十百千万\d]+)章[：:\s]*([^\n]*)',  # 第X章：标题
        r'第([一二三四五六七八九十百千万\d]+)节[：:\s]*([^\n]*)',  # 第X节：标题
        r'Chapter\s*(\d+)[：:\s]*([^\n]*)',  # Chapter X: 标题
        r'(\d+)[\.、]\s*([^\n]*)',  # 1. 标题 或 1、标题
    ]
    
    chapters = []
    current_chapter = None
    current_content = []
    
    lines = content.split('\n')
    chapter_num = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_content:
                current_content.append('')
            continue
            
        # 检查是否是章节标题
        is_chapter_title = False
        for pattern in chapter_patterns:
            match = re.match(pattern, line)
            if match:
                # 保存上一章
                if current_chapter and current_content:
                    chapters.append({
                        'number': current_chapter,
                        'title': current_title,
                        'content': '\n'.join(current_content).strip()
                    })
                
                # 开始新章
                chapter_num += 1
                current_chapter = chapter_num
                current_title = line
                current_content = []
                is_chapter_title = True
                print(f"📝 发现章节 {chapter_num}: {line[:50]}...")
                break
        
        if not is_chapter_title and current_chapter:
            current_content.append(line)
    
    # 保存最后一章
    if current_chapter and current_content:
        chapters.append({
            'number': current_chapter,
            'title': current_title,
            'content': '\n'.join(current_content).strip()
        })
    
    print(f"🎯 总共发现 {len(chapters)} 个章节")
    
    # 写入单独的章节文件
    for chapter in chapters:
        filename = f"chapter_{chapter['number']:03d}_data.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter['title']}\n\n")
            f.write(chapter['content'])
        
        print(f"💾 已保存: {filename} ({len(chapter['content'])} 字符)")
    
    print(f"✅ 章节分割完成！共生成 {len(chapters)} 个文件")
    return len(chapters)

def main():
    # 配置文件路径
    input_file = "novel_texts/raw/全民大航海，我开局一条幽灵船(1-500章).txt"
    output_dir = "novel_texts/chapters"
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 错误: 找不到输入文件 {input_file}")
        print("请确保文件在当前目录下")
        return
    
    # 执行分割
    try:
        chapter_count = split_novel_chapters(input_file, output_dir)
        print(f"\n🎉 分割完成！")
        print(f"📁 输出目录: {output_dir}")
        print(f"📚 章节数量: {chapter_count}")
        
    except Exception as e:
        print(f"❌ 分割过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
