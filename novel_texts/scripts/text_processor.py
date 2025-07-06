#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说文本处理器 - 将原始文本转换为结构化数据
解决硬编码问题，实现数据驱动的内容管理
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

class NovelTextProcessor:
    """小说文本处理器"""
    
    def __init__(self):
        self.chapters = {}
        self.scenes = {}
        self.choices = {}
    
    def process_raw_text(self, text_file: str) -> Dict:
        """处理原始小说文本"""
        print(f"📖 开始处理原始文本: {text_file}")
        
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按章节分割
        chapters = self.split_by_chapters(content)
        
        # 按场景分割
        for chapter_num, chapter_content in chapters.items():
            scenes = self.split_by_scenes(chapter_content)
            self.chapters[chapter_num] = scenes
        
        return self.chapters
    
    def split_by_chapters(self, content: str) -> Dict[int, str]:
        """按章节分割文本"""
        chapters = {}
        
        # 匹配章节标题的正则表达式
        chapter_pattern = r'第(\d+)章[^\n]*\n'
        
        # 找到所有章节位置
        chapter_matches = list(re.finditer(chapter_pattern, content))
        
        for i, match in enumerate(chapter_matches):
            chapter_num = int(match.group(1))
            start_pos = match.end()
            
            # 确定章节结束位置
            if i + 1 < len(chapter_matches):
                end_pos = chapter_matches[i + 1].start()
            else:
                end_pos = len(content)
            
            chapter_content = content[start_pos:end_pos].strip()
            chapters[chapter_num] = chapter_content
            
        print(f"✅ 分割出 {len(chapters)} 个章节")
        return chapters
    
    def split_by_scenes(self, chapter_content: str) -> List[Dict]:
        """按场景分割章节内容"""
        scenes = []
        
        # 按段落分割，每个段落作为一个场景
        paragraphs = [p.strip() for p in chapter_content.split('\n\n') if p.strip()]
        
        # 合并短段落，避免场景过于碎片化
        merged_scenes = self.merge_short_paragraphs(paragraphs)
        
        for i, scene_content in enumerate(merged_scenes, 1):
            scene = {
                'scene_id': i,
                'title': self.generate_scene_title(scene_content, i),
                'content': scene_content,
                'type': self.determine_scene_type(scene_content),
                'is_ending': self.is_ending_scene(scene_content)
            }
            scenes.append(scene)
        
        return scenes
    
    def merge_short_paragraphs(self, paragraphs: List[str], min_length: int = 100) -> List[str]:
        """合并过短的段落"""
        merged = []
        current_scene = ""
        
        for paragraph in paragraphs:
            current_scene += paragraph + "\n\n"
            
            # 如果当前场景足够长，或者是对话场景，就结束当前场景
            if (len(current_scene) >= min_length or 
                self.is_dialogue_heavy(paragraph) or
                self.is_action_scene(paragraph)):
                merged.append(current_scene.strip())
                current_scene = ""
        
        # 处理最后一个场景
        if current_scene.strip():
            if merged:
                merged[-1] += "\n\n" + current_scene.strip()
            else:
                merged.append(current_scene.strip())
        
        return merged
    
    def generate_scene_title(self, content: str, scene_num: int) -> str:
        """生成场景标题"""
        # 提取内容的关键词作为标题
        first_sentence = content.split('。')[0][:50]
        
        # 移除特殊字符
        title = re.sub(r'["\n\r\t]', '', first_sentence)
        
        if not title:
            title = f"场景{scene_num}"
        
        return title
    
    def determine_scene_type(self, content: str) -> str:
        """判断场景类型"""
        if '【' in content and '】' in content:
            return "TUTORIAL"
        elif '"' in content or '"' in content:
            return "DIALOGUE"
        elif any(word in content for word in ['战斗', '攻击', '血', '死亡']):
            return "COMBAT"
        else:
            return "NORMAL"
    
    def is_ending_scene(self, content: str) -> bool:
        """判断是否为结局场景"""
        ending_keywords = ['结束', '完结', '终章', '死亡', '游戏结束']
        return any(keyword in content for keyword in ending_keywords)
    
    def is_dialogue_heavy(self, content: str) -> bool:
        """判断是否为对话密集场景"""
        dialogue_count = content.count('"') + content.count('"')
        return dialogue_count >= 4
    
    def is_action_scene(self, content: str) -> bool:
        """判断是否为动作场景"""
        action_keywords = ['突然', '立即', '迅速', '冲向', '抓住', '跑', '逃']
        return any(keyword in content for keyword in action_keywords)
    
    def generate_choices(self, scenes: List[Dict]) -> List[Dict]:
        """为场景生成选择分支"""
        choices = []
        
        for i, scene in enumerate(scenes):
            scene_choices = []
            
            # 为每个场景生成2-3个选择
            if i < len(scenes) - 1:  # 不是最后一个场景
                # 主要选择：继续剧情
                main_choice = {
                    'text': '继续',
                    'next_scene': i + 2,  # 下一个场景
                    'experience_reward': 10
                }
                scene_choices.append(main_choice)
                
                # 可选选择：探索或其他行动
                if scene['type'] == 'NORMAL':
                    alt_choice = {
                        'text': '仔细观察周围',
                        'next_scene': i + 2,
                        'experience_reward': 15
                    }
                    scene_choices.append(alt_choice)
            
            choices.append({
                'scene_id': scene['scene_id'],
                'choices': scene_choices
            })
        
        return choices
    
    def export_to_json(self, output_file: str):
        """导出为JSON格式"""
        data = {
            'chapters': self.chapters,
            'metadata': {
                'total_chapters': len(self.chapters),
                'total_scenes': sum(len(scenes) for scenes in self.chapters.values()),
                'processed_at': str(Path().cwd())
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 数据已导出到: {output_file}")
    
    def export_to_java_data(self, output_file: str):
        """导出为Java数据格式"""
        java_code = []
        java_code.append("// 自动生成的故事数据")
        java_code.append("private void loadProcessedStories() {")
        
        for chapter_num, scenes in self.chapters.items():
            for scene in scenes:
                java_code.append(f"    createStoryFromData({chapter_num}, {scene['scene_id']}, ")
                java_code.append(f"        \"{scene['title']}\",")
                java_code.append(f"        \"{scene['content']}\",")
                java_code.append(f"        \"{scene['type']}\", {str(scene['is_ending']).lower()});")
                java_code.append("")
        
        java_code.append("}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(java_code))
        
        print(f"✅ Java代码已导出到: {output_file}")

def main():
    """主函数"""
    processor = NovelTextProcessor()
    
    # 处理原始文本（如果有的话）
    raw_text_file = "../raw_novel.txt"
    if Path(raw_text_file).exists():
        processor.process_raw_text(raw_text_file)
        
        # 导出结果
        processor.export_to_json("../processed_novel.json")
        processor.export_to_java_data("../generated_stories.java")
    else:
        print(f"❌ 原始文本文件不存在: {raw_text_file}")
        print("💡 请将小说文本保存为 raw_novel.txt")

if __name__ == "__main__":
    main()
