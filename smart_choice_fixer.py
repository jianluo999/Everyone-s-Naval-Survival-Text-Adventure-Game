#!/usr/bin/env python3
"""
智能选择修复器 - 修复死路选择，将它们重新连接到现有故事
"""

import json
import os
import random
from collections import defaultdict
from typing import Dict, List, Set

class SmartChoiceFixer:
    def __init__(self):
        self.existing_stories = set()  # 现有的故事ID
        self.choices = defaultdict(list)  # story_id -> [choices]
        self.dead_end_choices = []  # 指向死路的选择
        self.fixed_choices = []  # 修复后的选择
        
    def load_existing_stories(self):
        """加载现有的故事ID"""
        print("📚 加载现有故事...")
        
        # 从故事数据文件加载
        story_files = [
            'backend/src/main/resources/novel_texts/chapter_1_data.txt'
        ]
        
        for file_path in story_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split('|')
                            if len(parts) >= 5:
                                scene_num = parts[0]
                                story_id = f"story_1_{scene_num}"
                                self.existing_stories.add(story_id)
        
        print(f"✅ 加载现有故事: {len(self.existing_stories)}个")
    
    def load_choices(self):
        """加载选择数据"""
        print("📚 加载选择数据...")
        
        choice_files = [
            'novel_texts/optimized_scenes/optimized_choices.json',
            'backend/src/main/resources/novel_texts/chapter_1_choices.txt'
        ]
        
        total_choices = 0
        
        for file_path in choice_files:
            if os.path.exists(file_path):
                if file_path.endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        choices = json.load(f)
                        for choice in choices:
                            story_id = choice['story_id']
                            self.choices[story_id].append(choice)
                            total_choices += 1
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                parts = line.split('|')
                                if len(parts) >= 10:
                                    choice = {
                                        'story_id': parts[0],
                                        'text': parts[1],
                                        'next_story_id': parts[2],
                                        'gold_cost': int(parts[3]),
                                        'gold_reward': int(parts[4]),
                                        'health_cost': int(parts[5]),
                                        'health_reward': int(parts[6]),
                                        'experience_reward': int(parts[7]),
                                        'requirements': parts[8],
                                        'is_available': parts[9].lower() == 'true'
                                    }
                                    self.choices[choice['story_id']].append(choice)
                                    total_choices += 1
        
        print(f"✅ 加载选择: {total_choices}个")
    
    def find_dead_end_choices(self):
        """找出指向死路的选择"""
        print("🔍 查找死路选择...")
        
        dead_count = 0
        
        for story_id, choices in self.choices.items():
            for choice in choices:
                next_story_id = choice['next_story_id']
                # 如果下一个故事不存在，就是死路选择
                if next_story_id not in self.existing_stories:
                    self.dead_end_choices.append(choice)
                    dead_count += 1
        
        print(f"   发现死路选择: {dead_count}个")
        return self.dead_end_choices
    
    def fix_dead_end_choices(self):
        """修复死路选择"""
        print("🔧 修复死路选择...")
        
        # 将现有故事转换为列表，便于随机选择
        existing_story_list = list(self.existing_stories)
        
        # 为每个死路选择找到合适的目标故事
        for choice in self.dead_end_choices:
            original_next_id = choice['next_story_id']
            
            # 尝试找到合适的替代故事
            new_next_id = self.find_suitable_replacement(choice, existing_story_list)
            
            # 创建修复后的选择
            fixed_choice = choice.copy()
            fixed_choice['next_story_id'] = new_next_id
            fixed_choice['original_next_story_id'] = original_next_id  # 保留原始信息
            
            self.fixed_choices.append(fixed_choice)
        
        print(f"✅ 修复选择: {len(self.fixed_choices)}个")
        return self.fixed_choices
    
    def find_suitable_replacement(self, choice, existing_stories):
        """为选择找到合适的替代故事"""
        current_story_id = choice['story_id']
        original_next_id = choice['next_story_id']
        
        # 解析当前故事ID
        try:
            parts = current_story_id.split('_')
            if len(parts) >= 3 and parts[0] == 'story':
                chapter = int(parts[1])
                scene = int(parts[2])
                
                # 优先选择：同章节的下一个场景
                next_scene_id = f"story_{chapter}_{scene + 1}"
                if next_scene_id in existing_stories:
                    return next_scene_id
                
                # 次优选择：同章节的其他场景
                chapter_stories = [s for s in existing_stories if s.startswith(f"story_{chapter}_")]
                if chapter_stories:
                    # 选择场景号最接近的
                    chapter_stories.sort(key=lambda x: abs(int(x.split('_')[2]) - scene))
                    return chapter_stories[0]
        except (ValueError, IndexError):
            pass
        
        # 备用选择：根据选择类型选择合适的故事
        choice_text = choice['text'].lower()
        
        if '探索' in choice_text or '搜索' in choice_text:
            # 探索类选择，选择探索相关的故事
            exploration_stories = [s for s in existing_stories if any(keyword in s for keyword in ['explore', 'search', '6', '26'])]
            if exploration_stories:
                return random.choice(exploration_stories)
        
        elif '战斗' in choice_text or '攻击' in choice_text:
            # 战斗类选择，选择战斗相关的故事
            combat_stories = [s for s in existing_stories if any(keyword in s for keyword in ['combat', 'fight', '15', '16'])]
            if combat_stories:
                return random.choice(combat_stories)
        
        elif '对话' in choice_text or '交谈' in choice_text:
            # 对话类选择，选择对话相关的故事
            dialogue_stories = [s for s in existing_stories if any(keyword in s for keyword in ['talk', 'dialogue', '21', '22'])]
            if dialogue_stories:
                return random.choice(dialogue_stories)
        
        # 最后的备用选择：随机选择一个现有故事
        return random.choice(existing_stories)
    
    def save_fixed_choices(self):
        """保存修复后的选择"""
        if not self.fixed_choices:
            print("✅ 没有需要修复的选择")
            return
        
        # 保存为TXT格式，便于导入
        output_file = 'novel_texts/fixed_choices.txt'
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# 修复后的选择数据文件\n")
                f.write("# 格式: 故事ID|选择文本|下一个故事ID|金币消耗|金币奖励|生命消耗|生命奖励|经验奖励|要求|是否可用\n\n")
                
                for choice in self.fixed_choices:
                    line = f"{choice['story_id']}|{choice['text']}|{choice['next_story_id']}|{choice['gold_cost']}|{choice['gold_reward']}|{choice['health_cost']}|{choice['health_reward']}|{choice['experience_reward']}|{choice['requirements']}|{str(choice['is_available']).lower()}\n"
                    f.write(line)
            
            print(f"✅ 保存修复选择: {len(self.fixed_choices)}个 -> {output_file}")
        except Exception as e:
            print(f"❌ 保存修复选择失败: {e}")
    
    def generate_optimized_choices(self):
        """生成优化后的完整选择文件"""
        print("🔧 生成优化选择文件...")
        
        # 收集所有有效的选择
        valid_choices = []
        
        # 添加现有的有效选择
        for story_id, choices in self.choices.items():
            for choice in choices:
                if choice['next_story_id'] in self.existing_stories:
                    valid_choices.append(choice)
        
        # 添加修复后的选择
        valid_choices.extend(self.fixed_choices)
        
        # 确保每个现有故事都有至少2个选择
        story_choice_count = defaultdict(int)
        for choice in valid_choices:
            story_choice_count[choice['story_id']] += 1
        
        # 为选择不足的故事添加选择
        for story_id in self.existing_stories:
            if story_choice_count[story_id] < 2:
                needed = 2 - story_choice_count[story_id]
                for i in range(needed):
                    new_choice = self.generate_generic_choice(story_id, i)
                    valid_choices.append(new_choice)
        
        # 保存优化后的选择
        output_file = 'novel_texts/optimized_complete_choices.json'
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(valid_choices, f, ensure_ascii=False, indent=2)
            print(f"✅ 保存优化选择: {len(valid_choices)}个 -> {output_file}")
        except Exception as e:
            print(f"❌ 保存优化选择失败: {e}")
    
    def generate_generic_choice(self, story_id, index):
        """为故事生成通用选择"""
        generic_texts = ['继续前进', '仔细思考', '保持警惕', '寻找线索']
        
        # 选择一个现有的故事作为目标
        existing_story_list = list(self.existing_stories)
        target_story = random.choice(existing_story_list)
        
        return {
            'story_id': story_id,
            'text': generic_texts[index % len(generic_texts)],
            'next_story_id': target_story,
            'gold_cost': 0,
            'gold_reward': 0,
            'health_cost': 0,
            'health_reward': 0,
            'experience_reward': 5,
            'requirements': '',
            'is_available': True
        }
    
    def generate_report(self):
        """生成修复报告"""
        report = []
        report.append("# 智能选择修复报告\n")
        
        report.append(f"## 修复统计")
        report.append(f"- 现有故事数: {len(self.existing_stories)}")
        report.append(f"- 死路选择数: {len(self.dead_end_choices)}")
        report.append(f"- 修复选择数: {len(self.fixed_choices)}")
        report.append(f"- 修复成功率: {len(self.fixed_choices) / max(1, len(self.dead_end_choices)) * 100:.1f}%\n")
        
        # 现有故事列表
        report.append("## 现有故事列表")
        for story_id in sorted(self.existing_stories):
            report.append(f"- {story_id}")
        report.append("")
        
        # 保存报告
        with open('smart_choice_fix_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✅ 生成修复报告: smart_choice_fix_report.md")

def main():
    fixer = SmartChoiceFixer()
    
    # 加载现有故事
    fixer.load_existing_stories()
    
    # 加载选择数据
    fixer.load_choices()
    
    # 查找死路选择
    fixer.find_dead_end_choices()
    
    # 修复死路选择
    fixer.fix_dead_end_choices()
    
    # 保存修复结果
    fixer.save_fixed_choices()
    
    # 生成优化的完整选择文件
    fixer.generate_optimized_choices()
    
    # 生成报告
    fixer.generate_report()
    
    print(f"\n🎉 智能修复完成!")
    print(f"   现有故事: {len(fixer.existing_stories)}个")
    print(f"   死路选择: {len(fixer.dead_end_choices)}个")
    print(f"   修复选择: {len(fixer.fixed_choices)}个")

if __name__ == "__main__":
    main()
