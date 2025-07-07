#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量小说章节转游戏场景脚本
将500个章节批量转换为游戏场景，包含选择选项
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

class NovelToGameConverter:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.scene_counter = 1
        
        # 场景分割关键词
        self.scene_break_keywords = [
            '半小时后', '一小时后', '两小时后', '几小时后', '时间来到',
            '与此同时', '就在这时', '突然', '这时候', '接下来',
            '然而', '但是', '不过', '可是', '只是', '只见',
            '杨逸', '你', '他', '她', '苏娜', '翠西雅',
            '............', '----------', '———————'
        ]
        
        # 选择类型模板
        self.choice_templates = {
            'action': [
                '继续观察', '立即行动', '谨慎前进', '快速撤退',
                '仔细检查', '保持警惕', '尝试沟通', '准备战斗'
            ],
            'dialogue': [
                '询问详情', '表示同意', '提出质疑', '保持沉默',
                '友善回应', '严肃对待', '开玩笑', '转移话题'
            ],
            'exploration': [
                '探索周围', '搜查物品', '查看装备', '检查状态',
                '继续前进', '原路返回', '寻找线索', '休息片刻'
            ],
            'decision': [
                '接受提议', '拒绝请求', '考虑一下', '提出条件',
                '寻求帮助', '独自行动', '制定计划', '随机应变'
            ]
        }

    def split_chapter_to_scenes(self, chapter_content: str, chapter_num: int) -> List[Dict]:
        """将章节内容分割为多个场景"""
        lines = chapter_content.split('\n')
        scenes = []
        current_scene = []
        scene_num = 1
        
        # 移除章节标题
        if lines and lines[0].startswith('#'):
            lines = lines[1:]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检查是否是场景分割点
            is_scene_break = False
            for keyword in self.scene_break_keywords:
                if keyword in line and len(current_scene) > 3:  # 确保场景有足够内容
                    is_scene_break = True
                    break
            
            if is_scene_break and current_scene:
                # 保存当前场景
                scene_content = '\n'.join(current_scene).strip()
                if len(scene_content) > 50:  # 过滤太短的场景
                    scenes.append({
                        'story_id': f'story_{chapter_num}_{scene_num}',
                        'title': self.generate_scene_title(scene_content, chapter_num, scene_num),
                        'content': scene_content,
                        'chapter': chapter_num,
                        'scene': scene_num,
                        'story_type': self.determine_story_type(scene_content),
                        'is_ending': False
                    })
                    scene_num += 1
                
                # 开始新场景
                current_scene = [line]
            else:
                current_scene.append(line)
        
        # 保存最后一个场景
        if current_scene:
            scene_content = '\n'.join(current_scene).strip()
            if len(scene_content) > 50:
                scenes.append({
                    'story_id': f'story_{chapter_num}_{scene_num}',
                    'title': self.generate_scene_title(scene_content, chapter_num, scene_num),
                    'content': scene_content,
                    'chapter': chapter_num,
                    'scene': scene_num,
                    'story_type': self.determine_story_type(scene_content),
                    'is_ending': False
                })
        
        return scenes

    def generate_scene_title(self, content: str, chapter: int, scene: int) -> str:
        """根据场景内容生成标题"""
        # 提取关键词生成标题
        content_lower = content.lower()
        
        if '战斗' in content or '攻击' in content or '战争' in content:
            return f'第{chapter}章 - 激烈战斗'
        elif '对话' in content or '说道' in content or '回答' in content:
            return f'第{chapter}章 - 重要对话'
        elif '发现' in content or '找到' in content or '看到' in content:
            return f'第{chapter}章 - 重要发现'
        elif '决定' in content or '选择' in content or '考虑' in content:
            return f'第{chapter}章 - 关键决策'
        elif '魔药' in content or '装备' in content or '道具' in content:
            return f'第{chapter}章 - 物品获得'
        elif '翠西雅' in content:
            return f'第{chapter}章 - 翠西雅相关'
        elif '苏娜' in content:
            return f'第{chapter}章 - 苏娜相关'
        else:
            return f'第{chapter}章 - 场景{scene}'

    def determine_story_type(self, content: str) -> str:
        """根据内容确定故事类型"""
        content_lower = content.lower()
        
        if '战斗' in content_lower or '攻击' in content_lower or '战争' in content_lower:
            return 'BATTLE'
        elif '对话' in content_lower or '"' in content or '"' in content:
            return 'DIALOGUE'
        elif '探索' in content_lower or '寻找' in content_lower or '搜索' in content_lower:
            return 'EXPLORATION'
        elif '噩梦' in content_lower or '梦境' in content_lower:
            return 'NIGHTMARE'
        elif '交易' in content_lower or '购买' in content_lower or '出售' in content_lower:
            return 'TRADE'
        else:
            return 'NORMAL'

    def generate_choices_for_scene(self, scene: Dict, next_scene_id: str = None) -> List[Dict]:
        """为场景生成选择选项"""
        choices = []
        story_type = scene['story_type']
        content = scene['content']
        
        # 根据故事类型选择合适的选择模板
        if story_type == 'BATTLE':
            choice_texts = ['继续战斗', '寻找掩护', '使用道具', '尝试逃跑']
        elif story_type == 'DIALOGUE':
            choice_texts = ['继续对话', '询问详情', '表示同意', '保持沉默']
        elif story_type == 'EXPLORATION':
            choice_texts = ['继续探索', '仔细搜查', '谨慎前进', '原路返回']
        elif story_type == 'TRADE':
            choice_texts = ['进行交易', '讨价还价', '查看商品', '离开商店']
        else:
            choice_texts = ['继续前进', '仔细观察', '做出决定', '等待时机']
        
        # 生成选择数据
        for i, text in enumerate(choice_texts):
            next_story = next_scene_id if i == 0 else f"{scene['story_id']}_alt_{i}"
            
            choices.append({
                'story_id': scene['story_id'],
                'text': text,
                'next_story_id': next_story,
                'requirements': '',
                'is_available': True,
                'health_cost': 0,
                'health_reward': 0,
                'gold_cost': 0,
                'gold_reward': 0,
                'experience_reward': 5 if i == 0 else 3  # 主线选择给更多经验
            })
        
        return choices

    def process_single_chapter(self, chapter_file: str, actual_chapter_num: int) -> Tuple[List[Dict], List[Dict]]:
        """处理单个章节文件"""
        file_chapter_num = int(re.search(r'chapter_(\d+)', chapter_file).group(1))

        print(f"📖 处理第{actual_chapter_num}章 (文件: {chapter_file})...")

        # 读取章节内容
        with open(os.path.join(self.input_dir, chapter_file), 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割为场景，使用实际章节号
        scenes = self.split_chapter_to_scenes(content, actual_chapter_num)
        
        # 生成选择
        all_choices = []
        for i, scene in enumerate(scenes):
            next_scene_id = scenes[i + 1]['story_id'] if i + 1 < len(scenes) else f'story_{actual_chapter_num + 1}_1'
            choices = self.generate_choices_for_scene(scene, next_scene_id)
            all_choices.extend(choices)

        print(f"✅ 第{actual_chapter_num}章完成：{len(scenes)}个场景，{len(all_choices)}个选择")
        return scenes, all_choices

    def batch_convert_all_chapters(self):
        """批量转换所有章节"""
        print("🚀 开始批量转换500个章节...")
        
        # 确保输出目录存在
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        all_scenes = []
        all_choices = []
        
        # 获取所有章节文件
        chapter_files = [f for f in os.listdir(self.input_dir) if f.startswith('chapter_') and f.endswith('.txt')]
        chapter_files.sort(key=lambda x: int(re.search(r'chapter_(\d+)', x).group(1)))
        
        print(f"📚 找到 {len(chapter_files)} 个章节文件")
        
        # 批量处理，使用连续的章节号
        for i, chapter_file in enumerate(chapter_files, 1):
            try:
                scenes, choices = self.process_single_chapter(chapter_file, i)
                all_scenes.extend(scenes)
                all_choices.extend(choices)
            except Exception as e:
                print(f"❌ 处理 {chapter_file} 时出错: {str(e)}")
                continue
        
        # 保存结果
        self.save_results(all_scenes, all_choices)
        
        print(f"🎉 批量转换完成！")
        print(f"📊 总计：{len(all_scenes)} 个场景，{len(all_choices)} 个选择")

    def save_results(self, scenes: List[Dict], choices: List[Dict]):
        """保存转换结果"""
        # 保存场景数据
        scenes_file = os.path.join(self.output_dir, 'all_scenes.json')
        with open(scenes_file, 'w', encoding='utf-8') as f:
            json.dump(scenes, f, ensure_ascii=False, indent=2)
        
        # 保存选择数据
        choices_file = os.path.join(self.output_dir, 'all_choices.json')
        with open(choices_file, 'w', encoding='utf-8') as f:
            json.dump(choices, f, ensure_ascii=False, indent=2)
        
        # 生成SQL导入脚本
        self.generate_sql_import_script(scenes, choices)
        
        print(f"💾 数据已保存到 {self.output_dir}")

    def generate_sql_import_script(self, scenes: List[Dict], choices: List[Dict]):
        """生成SQL导入脚本"""
        sql_file = os.path.join(self.output_dir, 'batch_import.sql')
        
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("USE sailing_game;\n\n")
            f.write("-- 批量导入场景数据\n")
            
            # 场景数据
            for scene in scenes:
                f.write(f"INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) VALUES ")
                f.write(f"('{scene['story_id']}', '{scene['title']}', '{scene['content'].replace(chr(39), chr(39)+chr(39))}', ")
                f.write(f"{scene['chapter']}, {scene['scene']}, '{scene['story_type']}', {1 if scene['is_ending'] else 0});\n")
            
            f.write("\n-- 批量导入选择数据\n")
            
            # 选择数据
            for choice in choices:
                f.write(f"INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, ")
                f.write(f"health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES ")
                f.write(f"('{choice['story_id']}', '{choice['text']}', '{choice['next_story_id']}', ")
                f.write(f"'{choice['requirements']}', {1 if choice['is_available'] else 0}, ")
                f.write(f"{choice['health_cost']}, {choice['health_reward']}, {choice['gold_cost']}, ")
                f.write(f"{choice['gold_reward']}, {choice['experience_reward']});\n")

def main():
    # 配置路径
    input_dir = "novel_texts/chapters"
    output_dir = "novel_texts/game_scenes"
    
    # 创建转换器
    converter = NovelToGameConverter(input_dir, output_dir)
    
    # 执行批量转换
    converter.batch_convert_all_chapters()

if __name__ == "__main__":
    main()
