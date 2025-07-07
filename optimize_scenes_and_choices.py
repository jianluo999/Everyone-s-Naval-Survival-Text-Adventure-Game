#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精细优化场景和选择脚本
- 将第三人称转换为第一人称
- 优化选择分支的逻辑性和沉浸感
- 改进场景标题和内容
"""

import json
import re
import random
from typing import List, Dict

class SceneOptimizer:
    def __init__(self):
        # 第三人称到第一人称的转换规则
        self.person_conversions = {
            '杨逸': '我',
            '他': '我',
            '他的': '我的',
            '他们': '我们',
            '他们的': '我们的',
            '杨逸的': '我的',
            '这个年轻人': '我',
            '这个男人': '我',
            '这个人': '我',
        }
        
        # 场景类型对应的选择模板
        self.choice_templates = {
            'NORMAL': {
                'exploration': ['仔细观察周围环境', '继续向前探索', '停下来思考', '检查身上的物品'],
                'action': ['立即行动', '谨慎前进', '等待时机', '寻找其他路径'],
                'decision': ['接受这个现实', '质疑眼前的一切', '尝试理解情况', '保持冷静分析']
            },
            'DIALOGUE': {
                'response': ['认真倾听', '提出疑问', '表示赞同', '保持沉默'],
                'inquiry': ['询问更多细节', '请求解释', '表达困惑', '寻求帮助'],
                'social': ['友善回应', '保持警惕', '展现自信', '谦逊应对']
            },
            'BATTLE': {
                'combat': ['准备战斗', '寻找掩护', '观察敌情', '制定策略'],
                'tactical': ['正面攻击', '迂回包抄', '防守反击', '寻找弱点'],
                'survival': ['全力一搏', '保存实力', '寻找逃路', '呼叫支援']
            },
            'EXPLORATION': {
                'investigate': ['仔细搜查', '快速浏览', '重点检查', '全面探索'],
                'navigate': ['选择安全路线', '冒险走捷径', '跟随标记', '自己开路'],
                'discover': ['深入调查', '记录发现', '收集证据', '继续寻找']
            },
            'NIGHTMARE': {
                'psychological': ['努力保持清醒', '接受梦境现实', '寻找逃脱方法', '面对内心恐惧'],
                'survival': ['拼命逃跑', '勇敢面对', '寻找庇护', '呼唤帮助'],
                'mystery': ['解开谜团', '忽视异象', '寻找线索', '相信直觉']
            }
        }
        
        # 场景标题优化模板
        self.title_templates = {
            'awakening': '苏醒时刻',
            'discovery': '重要发现',
            'exploration': '探索未知',
            'encounter': '意外遭遇',
            'decision': '关键抉择',
            'battle': '激烈战斗',
            'mystery': '神秘事件',
            'revelation': '真相揭露',
            'journey': '航海征程',
            'danger': '危险降临'
        }

    def convert_to_first_person(self, text: str) -> str:
        """将第三人称转换为第一人称"""
        # 处理基本的人称转换
        for third, first in self.person_conversions.items():
            text = text.replace(third, first)
        
        # 处理动词时态调整
        text = re.sub(r'我(\w+)道', r'我\1着说', text)  # "我说道" -> "我说着"
        text = re.sub(r'我(\w+)起来', r'我开始\1', text)  # "我站起来" -> "我开始站立"
        
        # 处理特殊句式
        text = re.sub(r'我发现自己', '我发现我', text)
        text = re.sub(r'我看向自己', '我看向我', text)
        
        return text

    def enhance_scene_content(self, content: str, story_type: str) -> str:
        """增强场景内容的沉浸感"""
        # 转换为第一人称
        enhanced = self.convert_to_first_person(content)
        
        # 根据场景类型添加感官描述
        if story_type == 'NORMAL':
            if '海' in enhanced or '船' in enhanced:
                enhanced = self.add_maritime_atmosphere(enhanced)
        elif story_type == 'BATTLE':
            enhanced = self.add_tension_atmosphere(enhanced)
        elif story_type == 'NIGHTMARE':
            enhanced = self.add_mysterious_atmosphere(enhanced)
        
        return enhanced

    def add_maritime_atmosphere(self, text: str) -> str:
        """添加海洋氛围描述"""
        atmospheric_additions = [
            "海风轻抚着我的脸庞，带来咸腥的味道。",
            "船只在波浪中轻微摇摆，发出吱呀的声响。",
            "远处传来海鸥的叫声，回荡在无垠的海面上。",
            "阳光透过云层洒在海面上，波光粼粼。"
        ]
        
        if '海' in text and len(text) < 200:
            addition = random.choice(atmospheric_additions)
            text = f"{text}\n\n{addition}"
        
        return text

    def add_tension_atmosphere(self, text: str) -> str:
        """添加紧张氛围描述"""
        if '战斗' in text or '攻击' in text:
            tension_additions = [
                "我的心跳加速，肾上腺素开始分泌。",
                "空气中弥漫着紧张的气息。",
                "我握紧了手中的武器，准备迎接挑战。"
            ]
            if len(text) < 200:
                addition = random.choice(tension_additions)
                text = f"{text}\n\n{addition}"
        
        return text

    def add_mysterious_atmosphere(self, text: str) -> str:
        """添加神秘氛围描述"""
        mystery_additions = [
            "一种不祥的预感涌上心头。",
            "周围的空气似乎变得沉重起来。",
            "我感到有什么东西在暗中观察着我。"
        ]
        
        if len(text) < 200:
            addition = random.choice(mystery_additions)
            text = f"{text}\n\n{addition}"
        
        return text

    def generate_smart_title(self, content: str, chapter: int, scene: int) -> str:
        """生成智能化的场景标题"""
        content_lower = content.lower()
        
        # 关键词匹配生成标题
        if any(word in content_lower for word in ['苏醒', '醒来', '起身']):
            return f"第{chapter}章：苏醒时刻"
        elif any(word in content_lower for word in ['发现', '看到', '注意到']):
            return f"第{chapter}章：重要发现"
        elif any(word in content_lower for word in ['战斗', '攻击', '战争', '敌人']):
            return f"第{chapter}章：激烈战斗"
        elif any(word in content_lower for word in ['对话', '说道', '回答', '询问']):
            return f"第{chapter}章：重要对话"
        elif any(word in content_lower for word in ['探索', '寻找', '搜索', '调查']):
            return f"第{chapter}章：探索未知"
        elif any(word in content_lower for word in ['决定', '选择', '考虑', '抉择']):
            return f"第{chapter}章：关键抉择"
        elif any(word in content_lower for word in ['魔药', '装备', '道具', '物品']):
            return f"第{chapter}章：物品获得"
        elif any(word in content_lower for word in ['翠西雅', '苏娜', '船员']):
            return f"第{chapter}章：人物互动"
        elif any(word in content_lower for word in ['危险', '威胁', '恐惧']):
            return f"第{chapter}章：危险降临"
        elif any(word in content_lower for word in ['秘密', '谜团', '神秘']):
            return f"第{chapter}章：神秘事件"
        else:
            return f"第{chapter}章：航海征程 - {scene}"

    def generate_contextual_choices(self, scene: Dict) -> List[Dict]:
        """根据场景内容生成上下文相关的选择"""
        content = scene['content'].lower()
        story_type = scene['story_type']
        story_id = scene['story_id']
        
        choices = []
        
        # 根据内容关键词生成选择
        if '发现' in content or '看到' in content:
            choices.extend([
                {
                    'story_id': story_id,
                    'text': '仔细观察这个发现',
                    'next_story_id': self.get_next_scene_id(story_id),
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 0,
                    'experience_reward': 8
                },
                {
                    'story_id': story_id,
                    'text': '谨慎地接近查看',
                    'next_story_id': f"{story_id}_careful",
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 0,
                    'experience_reward': 6
                }
            ])
        
        if '对话' in content or '说' in content:
            choices.extend([
                {
                    'story_id': story_id,
                    'text': '认真倾听对方的话',
                    'next_story_id': self.get_next_scene_id(story_id),
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 0,
                    'experience_reward': 7
                },
                {
                    'story_id': story_id,
                    'text': '提出我的疑问',
                    'next_story_id': f"{story_id}_question",
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 0,
                    'experience_reward': 5
                }
            ])
        
        if '战斗' in content or '攻击' in content:
            choices.extend([
                {
                    'story_id': story_id,
                    'text': '准备迎战',
                    'next_story_id': self.get_next_scene_id(story_id),
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 5, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 10,
                    'experience_reward': 15
                },
                {
                    'story_id': story_id,
                    'text': '寻找战术优势',
                    'next_story_id': f"{story_id}_tactical",
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 5,
                    'experience_reward': 10
                }
            ])
        
        # 如果没有特定内容匹配，使用通用选择
        if not choices:
            choices = self.generate_generic_choices(scene)
        
        # 确保至少有2个选择，最多4个
        while len(choices) < 2:
            choices.append(self.generate_generic_choice(scene, len(choices)))
        
        return choices[:4]  # 限制最多4个选择

    def generate_generic_choices(self, scene: Dict) -> List[Dict]:
        """生成通用选择"""
        story_id = scene['story_id']
        story_type = scene['story_type']
        
        if story_type in self.choice_templates:
            template_category = list(self.choice_templates[story_type].keys())[0]
            choice_texts = self.choice_templates[story_type][template_category]
        else:
            choice_texts = self.choice_templates['NORMAL']['action']
        
        choices = []
        for i, text in enumerate(choice_texts[:4]):
            choices.append({
                'story_id': story_id,
                'text': text,
                'next_story_id': self.get_next_scene_id(story_id) if i == 0 else f"{story_id}_alt_{i}",
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 0,
                'experience_reward': 8 if i == 0 else 5
            })
        
        return choices

    def generate_generic_choice(self, scene: Dict, index: int) -> Dict:
        """生成单个通用选择"""
        generic_choices = ['继续前进', '仔细思考', '保持警惕', '寻找线索']
        
        return {
            'story_id': scene['story_id'],
            'text': generic_choices[index % len(generic_choices)],
            'next_story_id': f"{scene['story_id']}_generic_{index}",
            'requirements': '',
            'is_available': True,
            'health_cost': 0, 'health_reward': 0,
            'gold_cost': 0, 'gold_reward': 0,
            'experience_reward': 3
        }

    def get_next_scene_id(self, current_story_id: str) -> str:
        """获取下一个场景ID"""
        # 解析当前场景ID
        parts = current_story_id.split('_')
        if len(parts) >= 3:
            chapter = int(parts[1])
            scene = int(parts[2])
            return f"story_{chapter}_{scene + 1}"
        return f"{current_story_id}_next"

    def optimize_scenes_and_choices(self, scenes_file: str, choices_file: str, output_dir: str):
        """优化场景和选择"""
        print("🎨 开始精细优化场景和选择...")
        
        # 加载数据
        with open(scenes_file, 'r', encoding='utf-8') as f:
            scenes = json.load(f)
        
        print(f"📖 加载了 {len(scenes)} 个场景")
        
        optimized_scenes = []
        optimized_choices = []
        
        # 逐个优化场景
        for i, scene in enumerate(scenes):
            if i % 100 == 0:
                print(f"🔄 优化进度: {i}/{len(scenes)}")
            
            # 优化场景内容
            optimized_scene = scene.copy()
            optimized_scene['content'] = self.enhance_scene_content(scene['content'], scene['story_type'])
            optimized_scene['title'] = self.generate_smart_title(scene['content'], scene['chapter'], scene['scene'])
            
            optimized_scenes.append(optimized_scene)
            
            # 生成优化的选择
            scene_choices = self.generate_contextual_choices(optimized_scene)
            optimized_choices.extend(scene_choices)
        
        # 保存优化结果
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f"{output_dir}/optimized_scenes.json", 'w', encoding='utf-8') as f:
            json.dump(optimized_scenes, f, ensure_ascii=False, indent=2)
        
        with open(f"{output_dir}/optimized_choices.json", 'w', encoding='utf-8') as f:
            json.dump(optimized_choices, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 优化完成！")
        print(f"📊 优化场景: {len(optimized_scenes)} 个")
        print(f"📊 优化选择: {len(optimized_choices)} 个")
        print(f"💾 保存到: {output_dir}")

def main():
    optimizer = SceneOptimizer()
    
    # 配置文件路径
    scenes_file = "novel_texts/game_scenes/all_scenes.json"
    choices_file = "novel_texts/game_scenes/all_choices.json"
    output_dir = "novel_texts/optimized_scenes"
    
    # 执行优化
    optimizer.optimize_scenes_and_choices(scenes_file, choices_file, output_dir)

if __name__ == "__main__":
    main()
