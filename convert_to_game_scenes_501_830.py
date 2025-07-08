#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将501-830章节转换为游戏场景
添加选择分支和互动元素，使用第二人称叙述
"""

import json
import os
import re
from typing import List, Dict

class GameSceneConverter:
    def __init__(self):
        self.input_file = "novel_texts/chapters/chapters_501_830.json"
        self.output_dir = "novel_texts/game_scenes"
        
    def load_chapters(self) -> List[Dict]:
        """加载章节数据"""
        print("=== 加载章节数据 ===")
        
        if not os.path.exists(self.input_file):
            print(f"❌ 文件不存在: {self.input_file}")
            return []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
        
        print(f"✅ 加载了{len(chapters)}章节")
        return chapters
    
    def convert_to_second_person(self, text: str) -> str:
        """转换为第二人称"""
        if not text:
            return text
        
        # 保护引号内的对话
        protected_parts = []
        quote_pattern = r'"[^"]*"'
        quotes = re.findall(quote_pattern, text)
        converted_text = text
        
        for i, quote in enumerate(quotes):
            placeholder = f"__QUOTE_{i}__"
            converted_text = converted_text.replace(quote, placeholder, 1)
            protected_parts.append((placeholder, quote))
        
        # 转换规则
        conversion_rules = [
            (r'杨逸', '你'),
            (r'我们的', '你们的'),
            (r'我们', '你们'),
            (r'我的', '你的'),
            (r'其我', '其他'),
            (r'我(?![的们])', '你'),
            (r'咱们', '你们'),
            (r'咱', '你'),
            (r'本人', '你'),
        ]
        
        for pattern, replacement in conversion_rules:
            converted_text = re.sub(pattern, replacement, converted_text)
        
        # 恢复引号内容
        for placeholder, original in protected_parts:
            converted_text = converted_text.replace(placeholder, original)
        
        return converted_text
    
    def split_into_scenes(self, chapter: Dict) -> List[Dict]:
        """将章节分割为多个场景"""
        content = chapter['content']
        chapter_num = chapter['chapter_number']
        title = chapter['title']
        
        # 按段落分割
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        
        scenes = []
        current_scene_content = []
        scene_count = 1
        
        for i, paragraph in enumerate(paragraphs):
            current_scene_content.append(paragraph)
            
            # 每3-4段或遇到明显的场景转换创建一个新场景
            if (len(current_scene_content) >= 3 and 
                (i == len(paragraphs) - 1 or  # 最后一段
                 len('\n'.join(current_scene_content)) > 400 or  # 内容足够长
                 self.is_scene_break(paragraph))):  # 场景转换点
                
                scene_content = '\n'.join(current_scene_content)
                scene_content = self.convert_to_second_person(scene_content)
                
                scene = {
                    'story_id': f'story_{chapter_num}_{scene_count}',
                    'title': f'第{chapter_num}章：{title} - {scene_count}',
                    'content': scene_content,
                    'chapter_number': chapter_num,
                    'scene_number': scene_count
                }
                
                scenes.append(scene)
                current_scene_content = []
                scene_count += 1
        
        # 处理剩余内容
        if current_scene_content:
            scene_content = '\n'.join(current_scene_content)
            scene_content = self.convert_to_second_person(scene_content)
            
            scene = {
                'story_id': f'story_{chapter_num}_{scene_count}',
                'title': f'第{chapter_num}章：{title} - {scene_count}',
                'content': scene_content,
                'chapter_number': chapter_num,
                'scene_number': scene_count
            }
            scenes.append(scene)
        
        return scenes
    
    def is_scene_break(self, paragraph: str) -> bool:
        """判断是否是场景转换点"""
        scene_break_indicators = [
            '时间', '地点', '另一边', '与此同时', '数小时后', '数天后',
            '夜晚', '清晨', '下午', '傍晚', '第二天', '次日',
            '突然', '忽然', '就在这时', '正在此时'
        ]
        
        return any(indicator in paragraph for indicator in scene_break_indicators)
    
    def add_choices(self, scenes: List[Dict]) -> List[Dict]:
        """为场景添加选择分支"""
        print(f"=== 为{len(scenes)}个场景添加选择 ===")
        
        for i, scene in enumerate(scenes):
            choices = []
            
            # 为每个场景添加基本选择
            if i < len(scenes) - 1:  # 不是最后一个场景
                next_scene = scenes[i + 1]
                choices.append({
                    'text': '继续',
                    'nextStoryId': next_scene['story_id']
                })
                
                # 添加额外的互动选择
                choices.extend(self.generate_interactive_choices(scene, scenes, i))
            else:
                # 最后一个场景，连接到下一章第一个场景
                next_chapter = scene['chapter_number'] + 1
                if next_chapter <= 830:  # 确保不超出范围
                    choices.append({
                        'text': '继续',
                        'nextStoryId': f'story_{next_chapter}_1'
                    })
            
            scene['choices'] = choices
        
        return scenes
    
    def generate_interactive_choices(self, scene: Dict, all_scenes: List[Dict], current_index: int) -> List[Dict]:
        """生成互动选择"""
        choices = []
        content = scene['content'].lower()
        
        # 根据内容生成不同类型的选择
        if '战斗' in content or '攻击' in content or '敌人' in content:
            choices.extend([
                {'text': '仔细观察敌人', 'nextStoryId': scene['story_id']},
                {'text': '准备战斗', 'nextStoryId': scene['story_id']},
                {'text': '寻找掩护', 'nextStoryId': scene['story_id']}
            ])
        elif '探索' in content or '发现' in content or '寻找' in content:
            choices.extend([
                {'text': '仔细搜索', 'nextStoryId': scene['story_id']},
                {'text': '小心前进', 'nextStoryId': scene['story_id']},
                {'text': '观察周围', 'nextStoryId': scene['story_id']}
            ])
        elif '对话' in content or '说话' in content or '交谈' in content:
            choices.extend([
                {'text': '继续倾听', 'nextStoryId': scene['story_id']},
                {'text': '询问详情', 'nextStoryId': scene['story_id']},
                {'text': '表达看法', 'nextStoryId': scene['story_id']}
            ])
        else:
            # 通用选择
            choices.extend([
                {'text': '仔细思考', 'nextStoryId': scene['story_id']},
                {'text': '观察环境', 'nextStoryId': scene['story_id']},
                {'text': '做出决定', 'nextStoryId': scene['story_id']}
            ])
        
        # 限制选择数量，避免过多
        return choices[:2]  # 最多2个额外选择
    
    def convert_chapters_to_scenes(self, chapters: List[Dict]) -> List[Dict]:
        """转换所有章节为场景"""
        print("=== 转换章节为游戏场景 ===")
        
        all_scenes = []
        
        for chapter in chapters:
            print(f"转换第{chapter['chapter_number']}章: {chapter['title']}")
            
            # 分割为场景
            scenes = self.split_into_scenes(chapter)
            
            # 添加选择
            scenes = self.add_choices(scenes)
            
            all_scenes.extend(scenes)
            
            print(f"  生成{len(scenes)}个场景")
        
        print(f"✅ 总共生成{len(all_scenes)}个游戏场景")
        return all_scenes
    
    def save_scenes(self, scenes: List[Dict]):
        """保存游戏场景"""
        print("=== 保存游戏场景 ===")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(self.output_dir, "game_scenes_501_830.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scenes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 游戏场景已保存到: {output_file}")
        
        # 统计信息
        total_choices = sum(len(scene.get('choices', [])) for scene in scenes)
        avg_choices = total_choices / len(scenes) if scenes else 0
        
        print(f"统计信息:")
        print(f"  场景数量: {len(scenes)}")
        print(f"  选择总数: {total_choices}")
        print(f"  平均每场景选择数: {avg_choices:.1f}")
        
        # 显示前几个场景
        print(f"\n前3个场景预览:")
        for scene in scenes[:3]:
            print(f"  {scene['story_id']}: {scene['title']}")
            print(f"    内容长度: {len(scene['content'])} 字符")
            print(f"    选择数量: {len(scene.get('choices', []))}")
            print(f"    内容预览: {scene['content'][:50]}...")
            print()
    
    def run(self):
        """运行完整转换流程"""
        print("游戏场景转换器 - 501-830章")
        print("=" * 50)
        
        # 1. 加载章节
        chapters = self.load_chapters()
        if not chapters:
            print("❌ 加载章节失败")
            return False
        
        # 2. 转换为游戏场景
        scenes = self.convert_chapters_to_scenes(chapters)
        
        # 3. 保存场景
        self.save_scenes(scenes)
        
        print("\n🎉 游戏场景转换完成!")
        return True

def main():
    converter = GameSceneConverter()
    converter.run()

if __name__ == "__main__":
    main()
