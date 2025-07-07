#!/usr/bin/env python3
"""
选择分支分析器 - 检查并修复死路问题
确保每个故事都有合理的选择分支和结尾
"""

import json
import os
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

class ChoiceBranchAnalyzer:
    def __init__(self):
        self.stories = {}  # story_id -> story_data
        self.choices = defaultdict(list)  # story_id -> [choices]
        self.story_graph = defaultdict(set)  # story_id -> {next_story_ids}
        self.reverse_graph = defaultdict(set)  # story_id -> {prev_story_ids}
        self.dead_ends = set()
        self.unreachable = set()
        
    def load_data(self):
        """加载故事和选择数据"""
        print("📚 加载故事和选择数据...")
        
        # 加载故事数据
        story_files = [
            'novel_texts/optimized_scenes/optimized_stories.json',
            'backend/src/main/resources/novel_texts/chapter_1_data.txt'
        ]
        
        for file_path in story_files:
            if os.path.exists(file_path):
                if file_path.endswith('.json'):
                    self.load_json_stories(file_path)
                else:
                    self.load_txt_stories(file_path)
        
        # 加载选择数据
        choice_files = [
            'novel_texts/optimized_scenes/optimized_choices.json',
            'backend/src/main/resources/novel_texts/chapter_1_choices.txt'
        ]
        
        for file_path in choice_files:
            if os.path.exists(file_path):
                if file_path.endswith('.json'):
                    self.load_json_choices(file_path)
                else:
                    self.load_txt_choices(file_path)
    
    def load_json_stories(self, file_path):
        """加载JSON格式的故事数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                stories = json.load(f)
                for story in stories:
                    self.stories[story['story_id']] = story
                print(f"✅ 加载JSON故事: {len(stories)}个 - {file_path}")
        except Exception as e:
            print(f"❌ 加载JSON故事失败: {file_path} - {e}")
    
    def load_txt_stories(self, file_path):
        """加载TXT格式的故事数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                story_count = 0
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('|')
                        if len(parts) >= 5:
                            scene_num = parts[0]
                            title = parts[1]
                            content = parts[2].replace('\\n\\n', '\n\n')
                            story_type = parts[3]
                            is_ending = parts[4].lower() == 'true'

                            # 构造story_id
                            story_id = f"story_1_{scene_num}"

                            story = {
                                'story_id': story_id,
                                'title': title,
                                'content': content,
                                'chapter': 1,
                                'scene': int(scene_num),
                                'story_type': story_type,
                                'is_ending': is_ending
                            }
                            self.stories[story_id] = story
                            story_count += 1
                print(f"✅ 加载TXT故事: {story_count}个 - {file_path}")
        except Exception as e:
            print(f"❌ 加载TXT故事失败: {file_path} - {e}")
    
    def load_json_choices(self, file_path):
        """加载JSON格式的选择数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                choices = json.load(f)
                for choice in choices:
                    story_id = choice['story_id']
                    self.choices[story_id].append(choice)
                    # 构建图
                    next_story_id = choice['next_story_id']
                    self.story_graph[story_id].add(next_story_id)
                    self.reverse_graph[next_story_id].add(story_id)
                print(f"✅ 加载JSON选择: {len(choices)}个 - {file_path}")
        except Exception as e:
            print(f"❌ 加载JSON选择失败: {file_path} - {e}")
    
    def load_txt_choices(self, file_path):
        """加载TXT格式的选择数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('|')
                        if len(parts) >= 10:
                            story_id = parts[0]
                            choice = {
                                'story_id': story_id,
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
                            self.choices[story_id].append(choice)
                            # 构建图
                            next_story_id = choice['next_story_id']
                            self.story_graph[story_id].add(next_story_id)
                            self.reverse_graph[next_story_id].add(story_id)
                print(f"✅ 加载TXT选择: {file_path}")
        except Exception as e:
            print(f"❌ 加载TXT选择失败: {file_path} - {e}")
    
    def analyze_branches(self):
        """分析分支结构"""
        print("\n🔍 分析分支结构...")
        
        # 找出死路（没有选择的故事）
        for story_id in self.stories:
            if story_id not in self.choices or len(self.choices[story_id]) == 0:
                # 检查是否是结局故事
                story = self.stories[story_id]
                if not story.get('is_ending', False):
                    self.dead_ends.add(story_id)
        
        # 找出不可达的故事（没有前置故事的）
        start_stories = {'story_1_1'}  # 起始故事
        for story_id in self.stories:
            if story_id not in start_stories and story_id not in self.reverse_graph:
                self.unreachable.add(story_id)
        
        print(f"📊 分析结果:")
        print(f"   总故事数: {len(self.stories)}")
        print(f"   有选择的故事: {len(self.choices)}")
        print(f"   死路故事: {len(self.dead_ends)}")
        print(f"   不可达故事: {len(self.unreachable)}")
        
        return self.dead_ends, self.unreachable
    
    def fix_dead_ends(self):
        """修复死路问题"""
        print("\n🔧 修复死路问题...")
        
        fixed_choices = []
        
        for story_id in self.dead_ends:
            print(f"   修复死路: {story_id}")
            
            # 为死路故事添加选择
            new_choices = self.generate_choices_for_story(story_id)
            fixed_choices.extend(new_choices)
            
            # 更新内部数据结构
            for choice in new_choices:
                self.choices[story_id].append(choice)
                next_story_id = choice['next_story_id']
                self.story_graph[story_id].add(next_story_id)
                self.reverse_graph[next_story_id].add(story_id)
        
        return fixed_choices
    
    def generate_choices_for_story(self, story_id: str) -> List[Dict]:
        """为指定故事生成选择"""
        story = self.stories.get(story_id, {})
        content = story.get('content', '')
        
        choices = []
        
        # 根据故事内容生成不同类型的选择
        if '战斗' in content or '攻击' in content or '敌人' in content:
            choices.extend(self.generate_combat_choices(story_id))
        elif '探索' in content or '搜索' in content or '寻找' in content:
            choices.extend(self.generate_exploration_choices(story_id))
        elif '对话' in content or '交谈' in content or '询问' in content:
            choices.extend(self.generate_dialogue_choices(story_id))
        else:
            choices.extend(self.generate_generic_choices(story_id))
        
        # 确保至少有2个选择
        while len(choices) < 2:
            choices.append(self.generate_fallback_choice(story_id, len(choices)))
        
        return choices[:4]  # 最多4个选择
    
    def generate_combat_choices(self, story_id: str) -> List[Dict]:
        """生成战斗相关选择"""
        return [
            {
                'story_id': story_id,
                'text': '准备迎战',
                'next_story_id': self.get_next_story_id(story_id, 'combat'),
                'requirements': '',
                'is_available': True,
                'health_cost': 5, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 15,
                'experience_reward': 20
            },
            {
                'story_id': story_id,
                'text': '寻找战术优势',
                'next_story_id': self.get_next_story_id(story_id, 'tactical'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 8,
                'experience_reward': 15
            },
            {
                'story_id': story_id,
                'text': '尝试避开冲突',
                'next_story_id': self.get_next_story_id(story_id, 'avoid'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 0,
                'experience_reward': 10
            }
        ]
    
    def generate_exploration_choices(self, story_id: str) -> List[Dict]:
        """生成探索相关选择"""
        return [
            {
                'story_id': story_id,
                'text': '仔细搜索周围',
                'next_story_id': self.get_next_story_id(story_id, 'search'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 5,
                'experience_reward': 12
            },
            {
                'story_id': story_id,
                'text': '继续前进',
                'next_story_id': self.get_next_story_id(story_id, 'forward'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 0,
                'experience_reward': 8
            },
            {
                'story_id': story_id,
                'text': '保持警惕观察',
                'next_story_id': self.get_next_story_id(story_id, 'observe'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 0,
                'experience_reward': 10
            }
        ]
    
    def generate_dialogue_choices(self, story_id: str) -> List[Dict]:
        """生成对话相关选择"""
        return [
            {
                'story_id': story_id,
                'text': '友善地交谈',
                'next_story_id': self.get_next_story_id(story_id, 'friendly'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 10,
                'experience_reward': 15
            },
            {
                'story_id': story_id,
                'text': '谨慎地询问',
                'next_story_id': self.get_next_story_id(story_id, 'cautious'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 5,
                'experience_reward': 12
            },
            {
                'story_id': story_id,
                'text': '保持沉默观察',
                'next_story_id': self.get_next_story_id(story_id, 'silent'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 0,
                'experience_reward': 8
            }
        ]
    
    def generate_generic_choices(self, story_id: str) -> List[Dict]:
        """生成通用选择"""
        return [
            {
                'story_id': story_id,
                'text': '继续前进',
                'next_story_id': self.get_next_story_id(story_id, 'continue'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 0,
                'experience_reward': 8
            },
            {
                'story_id': story_id,
                'text': '仔细思考',
                'next_story_id': self.get_next_story_id(story_id, 'think'),
                'requirements': '',
                'is_available': True,
                'health_cost': 0, 'health_reward': 0,
                'gold_cost': 0, 'gold_reward': 0,
                'experience_reward': 10
            }
        ]
    
    def generate_fallback_choice(self, story_id: str, index: int) -> Dict:
        """生成备用选择"""
        fallback_texts = ['寻找线索', '保持警惕', '休息片刻', '回顾情况']
        
        return {
            'story_id': story_id,
            'text': fallback_texts[index % len(fallback_texts)],
            'next_story_id': self.get_next_story_id(story_id, f'fallback_{index}'),
            'requirements': '',
            'is_available': True,
            'health_cost': 0, 'health_reward': 0,
            'gold_cost': 0, 'gold_reward': 0,
            'experience_reward': 5
        }
    
    def get_next_story_id(self, current_story_id: str, choice_type: str) -> str:
        """获取下一个故事ID"""
        # 解析当前故事ID
        parts = current_story_id.split('_')
        if len(parts) >= 3:
            try:
                chapter = int(parts[1])
                scene = int(parts[2])
                
                # 根据选择类型生成不同的下一个故事ID
                if choice_type == 'continue':
                    return f"story_{chapter}_{scene + 1}"
                else:
                    return f"story_{chapter}_{scene}_{choice_type}"
            except ValueError:
                pass
        
        # 备用方案
        return f"{current_story_id}_{choice_type}"
    
    def save_fixed_choices(self, fixed_choices: List[Dict]):
        """保存修复后的选择"""
        if not fixed_choices:
            print("✅ 没有需要修复的选择")
            return
        
        output_file = 'novel_texts/fixed_choices.json'
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(fixed_choices, f, ensure_ascii=False, indent=2)
            print(f"✅ 保存修复选择: {len(fixed_choices)}个 -> {output_file}")
        except Exception as e:
            print(f"❌ 保存修复选择失败: {e}")
    
    def generate_report(self):
        """生成分析报告"""
        report = []
        report.append("# 选择分支分析报告\n")
        
        report.append(f"## 总体统计")
        report.append(f"- 总故事数: {len(self.stories)}")
        report.append(f"- 有选择的故事: {len(self.choices)}")
        report.append(f"- 死路故事: {len(self.dead_ends)}")
        report.append(f"- 不可达故事: {len(self.unreachable)}\n")
        
        if self.dead_ends:
            report.append("## 死路故事列表")
            for story_id in sorted(self.dead_ends):
                story = self.stories.get(story_id, {})
                title = story.get('title', '未知标题')
                report.append(f"- {story_id}: {title}")
            report.append("")
        
        if self.unreachable:
            report.append("## 不可达故事列表")
            for story_id in sorted(self.unreachable):
                story = self.stories.get(story_id, {})
                title = story.get('title', '未知标题')
                report.append(f"- {story_id}: {title}")
            report.append("")
        
        # 保存报告
        with open('choice_branch_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✅ 生成分析报告: choice_branch_analysis_report.md")

def main():
    analyzer = ChoiceBranchAnalyzer()
    
    # 加载数据
    analyzer.load_data()
    
    # 分析分支
    dead_ends, unreachable = analyzer.analyze_branches()
    
    # 修复死路
    fixed_choices = analyzer.fix_dead_ends()
    
    # 保存修复结果
    analyzer.save_fixed_choices(fixed_choices)
    
    # 生成报告
    analyzer.generate_report()
    
    print(f"\n🎉 分析完成!")
    print(f"   修复了 {len(fixed_choices)} 个选择")
    print(f"   解决了 {len(dead_ends)} 个死路问题")

if __name__ == "__main__":
    main()
