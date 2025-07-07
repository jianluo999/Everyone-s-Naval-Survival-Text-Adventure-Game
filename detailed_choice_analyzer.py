#!/usr/bin/env python3
"""
详细选择分析器 - 深度分析选择分支，确保没有死路
"""

import json
import os
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

class DetailedChoiceAnalyzer:
    def __init__(self):
        self.choices = defaultdict(list)  # story_id -> [choices]
        self.story_graph = defaultdict(set)  # story_id -> {next_story_ids}
        self.reverse_graph = defaultdict(set)  # story_id -> {prev_story_ids}
        self.all_story_ids = set()
        self.dead_ends = set()
        self.unreachable = set()
        self.circular_paths = []
        
    def load_choices(self):
        """加载选择数据"""
        print("📚 加载选择数据...")
        
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
    
    def load_json_choices(self, file_path):
        """加载JSON格式的选择数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                choices = json.load(f)
                for choice in choices:
                    story_id = choice['story_id']
                    next_story_id = choice['next_story_id']
                    
                    self.choices[story_id].append(choice)
                    self.story_graph[story_id].add(next_story_id)
                    self.reverse_graph[next_story_id].add(story_id)
                    self.all_story_ids.add(story_id)
                    self.all_story_ids.add(next_story_id)
                    
                print(f"✅ 加载JSON选择: {len(choices)}个 - {file_path}")
        except Exception as e:
            print(f"❌ 加载JSON选择失败: {file_path} - {e}")
    
    def load_txt_choices(self, file_path):
        """加载TXT格式的选择数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                choice_count = 0
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('|')
                        if len(parts) >= 10:
                            story_id = parts[0]
                            next_story_id = parts[2]
                            
                            choice = {
                                'story_id': story_id,
                                'text': parts[1],
                                'next_story_id': next_story_id,
                                'gold_cost': int(parts[3]),
                                'gold_reward': int(parts[4]),
                                'health_cost': int(parts[5]),
                                'health_reward': int(parts[6]),
                                'experience_reward': int(parts[7]),
                                'requirements': parts[8],
                                'is_available': parts[9].lower() == 'true'
                            }
                            
                            self.choices[story_id].append(choice)
                            self.story_graph[story_id].add(next_story_id)
                            self.reverse_graph[next_story_id].add(story_id)
                            self.all_story_ids.add(story_id)
                            self.all_story_ids.add(next_story_id)
                            choice_count += 1
                            
                print(f"✅ 加载TXT选择: {choice_count}个 - {file_path}")
        except Exception as e:
            print(f"❌ 加载TXT选择失败: {file_path} - {e}")
    
    def analyze_dead_ends(self):
        """分析死路"""
        print("\n🔍 分析死路...")
        
        for story_id in self.all_story_ids:
            # 如果一个故事没有任何选择，且不是明确的结局，就是死路
            if story_id not in self.choices or len(self.choices[story_id]) == 0:
                # 检查是否是结局故事（通常包含"结局"、"ending"等关键词）
                if not self.is_ending_story(story_id):
                    self.dead_ends.add(story_id)
        
        print(f"   发现死路: {len(self.dead_ends)}个")
        return self.dead_ends
    
    def analyze_unreachable(self):
        """分析不可达故事"""
        print("\n🔍 分析不可达故事...")
        
        # 从起始故事开始BFS
        start_stories = {'story_1_1', 'story_1_2', 'story_1_3'}  # 可能的起始故事
        reachable = set()
        queue = deque(start_stories)
        
        while queue:
            current = queue.popleft()
            if current in reachable:
                continue
            reachable.add(current)
            
            # 添加所有可达的下一个故事
            for next_story in self.story_graph.get(current, set()):
                if next_story not in reachable:
                    queue.append(next_story)
        
        # 找出不可达的故事
        self.unreachable = self.all_story_ids - reachable
        
        print(f"   可达故事: {len(reachable)}个")
        print(f"   不可达故事: {len(self.unreachable)}个")
        return self.unreachable
    
    def analyze_circular_paths(self):
        """分析循环路径"""
        print("\n🔍 分析循环路径...")
        
        visited = set()
        rec_stack = set()
        
        def dfs(story_id, path):
            if story_id in rec_stack:
                # 找到循环
                cycle_start = path.index(story_id)
                cycle = path[cycle_start:] + [story_id]
                self.circular_paths.append(cycle)
                return
            
            if story_id in visited:
                return
            
            visited.add(story_id)
            rec_stack.add(story_id)
            
            for next_story in self.story_graph.get(story_id, set()):
                dfs(next_story, path + [story_id])
            
            rec_stack.remove(story_id)
        
        # 从所有故事开始检查循环
        for story_id in self.all_story_ids:
            if story_id not in visited:
                dfs(story_id, [])
        
        print(f"   发现循环路径: {len(self.circular_paths)}个")
        return self.circular_paths
    
    def is_ending_story(self, story_id):
        """判断是否是结局故事"""
        # 简单的启发式判断
        ending_keywords = ['ending', '结局', 'end', 'final', '完结', '终章']
        story_id_lower = story_id.lower()
        
        for keyword in ending_keywords:
            if keyword in story_id_lower:
                return True
        
        # 检查是否有特定的结局模式
        if story_id.endswith('_ending') or story_id.endswith('_end'):
            return True
            
        return False
    
    def generate_fixes(self):
        """生成修复方案"""
        print("\n🔧 生成修复方案...")
        
        fixes = []
        
        # 为死路故事生成选择
        for story_id in self.dead_ends:
            print(f"   为死路故事生成选择: {story_id}")
            
            # 生成2-3个选择
            new_choices = [
                {
                    'story_id': story_id,
                    'text': '继续探索',
                    'next_story_id': self.generate_next_story_id(story_id, 'explore'),
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 0,
                    'experience_reward': 8
                },
                {
                    'story_id': story_id,
                    'text': '仔细思考',
                    'next_story_id': self.generate_next_story_id(story_id, 'think'),
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 0,
                    'experience_reward': 10
                },
                {
                    'story_id': story_id,
                    'text': '寻找出路',
                    'next_story_id': self.generate_next_story_id(story_id, 'escape'),
                    'requirements': '',
                    'is_available': True,
                    'health_cost': 0, 'health_reward': 0,
                    'gold_cost': 0, 'gold_reward': 5,
                    'experience_reward': 12
                }
            ]
            
            fixes.extend(new_choices)
        
        return fixes
    
    def generate_next_story_id(self, current_story_id, action_type):
        """生成下一个故事ID"""
        # 尝试解析当前故事ID
        parts = current_story_id.split('_')
        
        if len(parts) >= 3 and parts[0] == 'story':
            try:
                chapter = int(parts[1])
                scene = int(parts[2])
                
                # 根据动作类型生成不同的下一个故事
                if action_type == 'explore':
                    return f"story_{chapter}_{scene + 1}"
                elif action_type == 'think':
                    return f"story_{chapter}_{scene}_think"
                elif action_type == 'escape':
                    return f"story_{chapter}_{scene}_escape"
                else:
                    return f"story_{chapter}_{scene}_{action_type}"
            except ValueError:
                pass
        
        # 备用方案
        return f"{current_story_id}_{action_type}"
    
    def save_fixes(self, fixes):
        """保存修复方案"""
        if not fixes:
            print("✅ 没有需要修复的选择")
            return
        
        output_file = 'novel_texts/dead_end_fixes.json'
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(fixes, f, ensure_ascii=False, indent=2)
            print(f"✅ 保存修复方案: {len(fixes)}个选择 -> {output_file}")
        except Exception as e:
            print(f"❌ 保存修复方案失败: {e}")
    
    def generate_detailed_report(self):
        """生成详细报告"""
        report = []
        report.append("# 详细选择分支分析报告\n")
        
        report.append(f"## 总体统计")
        report.append(f"- 总故事数: {len(self.all_story_ids)}")
        report.append(f"- 有选择的故事: {len(self.choices)}")
        report.append(f"- 死路故事: {len(self.dead_ends)}")
        report.append(f"- 不可达故事: {len(self.unreachable)}")
        report.append(f"- 循环路径: {len(self.circular_paths)}\n")
        
        if self.dead_ends:
            report.append("## 死路故事详情")
            for story_id in sorted(self.dead_ends):
                report.append(f"- {story_id}")
            report.append("")
        
        if self.unreachable:
            report.append("## 不可达故事详情")
            for story_id in sorted(self.unreachable):
                report.append(f"- {story_id}")
            report.append("")
        
        if self.circular_paths:
            report.append("## 循环路径详情")
            for i, path in enumerate(self.circular_paths[:10]):  # 只显示前10个
                report.append(f"### 循环路径 {i+1}")
                report.append(f"路径: {' -> '.join(path)}")
                report.append("")
        
        # 选择分布统计
        report.append("## 选择分布统计")
        choice_counts = {}
        for story_id, choices in self.choices.items():
            count = len(choices)
            choice_counts[count] = choice_counts.get(count, 0) + 1
        
        for count in sorted(choice_counts.keys()):
            report.append(f"- {count}个选择的故事: {choice_counts[count]}个")
        report.append("")
        
        # 保存报告
        with open('detailed_choice_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✅ 生成详细分析报告: detailed_choice_analysis_report.md")

def main():
    analyzer = DetailedChoiceAnalyzer()
    
    # 加载数据
    analyzer.load_choices()
    
    # 分析各种问题
    dead_ends = analyzer.analyze_dead_ends()
    unreachable = analyzer.analyze_unreachable()
    circular_paths = analyzer.analyze_circular_paths()
    
    # 生成修复方案
    fixes = analyzer.generate_fixes()
    
    # 保存修复方案
    analyzer.save_fixes(fixes)
    
    # 生成详细报告
    analyzer.generate_detailed_report()
    
    print(f"\n🎉 详细分析完成!")
    print(f"   死路故事: {len(dead_ends)}个")
    print(f"   不可达故事: {len(unreachable)}个")
    print(f"   循环路径: {len(circular_paths)}个")
    print(f"   生成修复方案: {len(fixes)}个选择")

if __name__ == "__main__":
    main()
