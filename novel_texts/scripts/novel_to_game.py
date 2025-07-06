#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说转游戏剧情脚本
将小说文本转换为游戏剧情格式
"""

import os
import re
from pathlib import Path

class NovelToGameConverter:
    def __init__(self):
        self.scene_counter = 1
        self.chapter_counter = 1
    
    def convert_chapter(self, input_file, output_file):
        """转换单个章节"""
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取章节标题
        title_match = re.match(r'第\s*[0-9一二三四五六七八九十百千万]+\s*[章回]\s*(.*?)(?=\n|$)', content)
        chapter_title = title_match.group(0) if title_match else f"第{self.chapter_counter}章"
        
        # 处理内容
        processed_content = self.process_content(content, chapter_title)
        
        # 保存处理后的内容
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        print(f"转换完成: {input_file} -> {output_file}")
        self.chapter_counter += 1
    
    def process_content(self, content, chapter_title):
        """处理文本内容"""
        # 移除章节标题行
        content = re.sub(r'^第\s*[0-9一二三四五六七八九十百千万]+\s*[章回].*?\n', '', content, flags=re.MULTILINE)
        
        # 分割段落
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        
        # 转换为游戏格式
        game_content = f"# {chapter_title}\n\n"
        
        current_scene = ""
        scene_length = 0
        max_scene_length = 200  # 每个场景最大字符数
        
        for paragraph in paragraphs:
            # 替换人称
            paragraph = self.convert_to_second_person(paragraph)
            
            # 检查是否需要分割场景
            if scene_length + len(paragraph) > max_scene_length and current_scene:
                # 保存当前场景
                game_content += self.format_scene(current_scene)
                current_scene = paragraph
                scene_length = len(paragraph)
            else:
                current_scene += "\n\n" + paragraph if current_scene else paragraph
                scene_length += len(paragraph)
        
        # 保存最后一个场景
        if current_scene:
            game_content += self.format_scene(current_scene)
        
        return game_content
    
    def convert_to_second_person(self, text):
        """转换为第二人称"""
        # 替换常见的第三人称为第二人称
        replacements = {
            r'杨逸': '你',
            r'他': '你',
            r'她': '你',
            r'主角': '你',
            r'少年': '你',
            r'青年': '你',
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def format_scene(self, scene_content):
        """格式化场景"""
        scene_id = f"scene_{self.chapter_counter}_{self.scene_counter}"
        
        # 添加选择分支（简单示例）
        choices = self.generate_choices(scene_content)
        
        formatted = f"\n## 场景 {self.scene_counter}\n\n"
        formatted += f"**场景ID**: {scene_id}\n\n"
        formatted += f"{scene_content}\n\n"
        
        if choices:
            formatted += "### 选择分支\n\n"
            for i, choice in enumerate(choices, 1):
                formatted += f"{i}. {choice}\n"
            formatted += "\n"
        
        formatted += "---\n"
        
        self.scene_counter += 1
        return formatted
    
    def generate_choices(self, content):
        """生成选择分支"""
        choices = []
        
        # 根据内容关键词生成选择
        if "发现" in content or "看到" in content:
            choices.extend([
                "仔细观察",
                "谨慎接近",
                "保持距离"
            ])
        
        if "说话" in content or "对话" in content:
            choices.extend([
                "友善回应",
                "保持警惕",
                "直接询问"
            ])
        
        if "战斗" in content or "攻击" in content:
            choices.extend([
                "主动攻击",
                "防御反击",
                "尝试逃跑"
            ])
        
        if "物品" in content or "装备" in content:
            choices.extend([
                "拿取物品",
                "检查陷阱",
                "暂时不动"
            ])
        
        # 通用选择
        if not choices:
            choices = [
                "继续前进",
                "停下思考",
                "查看状态"
            ]
        
        return choices[:3]  # 最多3个选择

def batch_convert(input_dir, output_dir):
    """批量转换"""
    converter = NovelToGameConverter()
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 获取所有txt文件
    txt_files = sorted(input_path.glob("*.txt"))
    
    for txt_file in txt_files:
        output_file = output_path / f"{txt_file.stem}_game.md"
        converter.convert_chapter(txt_file, output_file)

if __name__ == "__main__":
    # 使用示例 - 处理前10章作为示例
    input_dir = "../raw/chapters"
    output_dir = "../processed"

    print("开始转换小说为游戏格式...")

    # 先处理前10章作为示例
    converter = NovelToGameConverter()

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 处理前10章
    for i in range(2, 12):  # chapter_02.txt 到 chapter_11.txt
        chapter_file = f"chapter_{i:02d}.txt"
        input_file = input_path / chapter_file
        output_file = output_path / f"chapter_{i:02d}_game.md"

        if input_file.exists():
            converter.convert_chapter(input_file, output_file)
        else:
            print(f"文件不存在: {input_file}")

    print("前10章转换完成！")
