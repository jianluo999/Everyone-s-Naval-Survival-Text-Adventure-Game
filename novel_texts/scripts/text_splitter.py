#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说文本分割脚本
将大的txt文件按章节分割成小文件
"""

import os
import re
from pathlib import Path

def split_novel_by_chapters(input_file, output_dir):
    """
    按章节分割小说文本
    
    Args:
        input_file: 输入的txt文件路径
        output_dir: 输出目录
    """
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 章节分割正则表达式
    # 匹配：第X章、第X回、Chapter X等格式
    chapter_pattern = r'第\s*[0-9一二三四五六七八九十百千万]+\s*[章回].*?(?=\n|$)'
    
    # 分割章节
    chapters = re.split(f'({chapter_pattern})', content, flags=re.MULTILINE)
    
    current_chapter = 1
    current_title = ""
    current_content = ""
    
    for i, part in enumerate(chapters):
        if re.match(chapter_pattern, part.strip()):
            # 保存上一章
            if current_content.strip():
                save_chapter(output_dir, current_chapter, current_title, current_content)
                current_chapter += 1
            
            # 开始新章节
            current_title = part.strip()
            current_content = ""
        else:
            current_content += part
    
    # 保存最后一章
    if current_content.strip():
        save_chapter(output_dir, current_chapter, current_title, current_content)
    
    print(f"分割完成！共分割出 {current_chapter} 章")

def save_chapter(output_dir, chapter_num, title, content):
    """保存单个章节"""
    filename = f"chapter_{chapter_num:02d}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        if title:
            f.write(f"{title}\n\n")
        f.write(content.strip())
    
    print(f"保存章节：{filename} - {title}")

def split_by_size(input_file, output_dir, max_size_kb=50):
    """
    按文件大小分割
    
    Args:
        input_file: 输入文件
        output_dir: 输出目录
        max_size_kb: 最大文件大小（KB）
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    max_chars = max_size_kb * 1024 // 3  # 估算字符数（UTF-8中文约3字节）
    
    parts = []
    current_part = ""
    
    paragraphs = content.split('\n\n')
    
    for paragraph in paragraphs:
        if len(current_part) + len(paragraph) > max_chars:
            if current_part:
                parts.append(current_part.strip())
                current_part = paragraph
            else:
                # 单个段落太长，强制分割
                parts.append(paragraph[:max_chars])
                current_part = paragraph[max_chars:]
        else:
            current_part += "\n\n" + paragraph if current_part else paragraph
    
    if current_part:
        parts.append(current_part.strip())
    
    # 保存分割后的文件
    for i, part in enumerate(parts, 1):
        filename = f"part_{i:02d}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(part)
        
        print(f"保存部分：{filename} ({len(part)} 字符)")

if __name__ == "__main__":
    # 使用示例
    input_file = "../raw/全民大航海，我开局一条幽灵船(1-500章).txt"  # 输入文件
    output_dir = "../raw/chapters"   # 输出目录

    if os.path.exists(input_file):
        print("开始分割小说...")
        split_novel_by_chapters(input_file, output_dir)
    else:
        print(f"文件不存在: {input_file}")
        print("请将小说txt文件放在 novel_texts/raw/ 目录下")
