#!/usr/bin/env python3
"""
故事流程优化器 - 构建合理的故事分支网络
支流汇入主流，确保所有路径都有意义且最终收敛
"""

import json
import os
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

class StoryFlowOptimizer:
    def __init__(self):
        self.existing_stories = {}  # story_id -> story_data
        self.choices = defaultdict(list)  # story_id -> [choices]
        self.story_graph = defaultdict(set)  # story_id -> {next_story_ids}
        self.reverse_graph = defaultdict(set)  # story_id -> {prev_story_ids}
        
        # 定义故事主线和关键节点（基于实际存在的故事）
        self.main_storyline = [
            'story_1_18',  # 航海日志详细规则
            'story_1_19',  # 属性详情
            'story_1_20',  # 理智与天赋
            'story_1_21',  # 世界聊天
            'story_1_22',  # 情报收集
            'story_1_23',  # 装备发现
            'story_1_24',  # 船只差异
            'story_1_25',  # 公平性质疑
            'story_1_26',  # 准备出海
            'story_1_27',  # 开始航行
            'story_1_28',  # 海上遭遇
            'story_1_29',  # 危机处理
            'story_1_30'   # 第一章结局
        ]
        
        # 定义支线汇入点（基于实际存在的故事）
        self.convergence_points = {
            'exploration': 'story_1_19',   # 探索支线汇入属性详情
            'dialogue': 'story_1_21',      # 对话支线汇入世界聊天
            'combat': 'story_1_23',        # 战斗支线汇入装备发现
            'fishing': 'story_1_22',       # 钓鱼支线汇入情报收集
            'discovery': 'story_1_26',     # 发现支线汇入准备出海
            'tutorial': 'story_1_18',      # 教程支线汇入航海日志
        }
        
        # 定义故事类型和主题
        self.story_themes = {
            'exploration': ['探索', '搜索', '寻找', '发现', '调查'],
            'combat': ['战斗', '攻击', '防御', '怪物', '敌人'],
            'dialogue': ['对话', '交谈', '询问', '交流', '沟通'],
            'fishing': ['钓鱼', '捕鱼', '鱼竿', '鱼饵', '海钓'],
            'mystery': ['神秘', '谜题', '线索', '秘密', '真相'],
            'survival': ['生存', '食物', '水源', '休息', '恢复']
        }
    
    def load_data(self):
        """加载故事和选择数据"""
        print("📚 加载故事数据...")
        
        # 加载故事数据
        story_file = 'backend/src/main/resources/novel_texts/chapter_1_data.txt'
        if os.path.exists(story_file):
            with open(story_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('|')
                        if len(parts) >= 5:
                            scene_num = parts[0]
                            story_id = f"story_1_{scene_num}"
                            story = {
                                'story_id': story_id,
                                'title': parts[1],
                                'content': parts[2].replace('\\n\\n', '\n\n'),
                                'story_type': parts[3],
                                'is_ending': parts[4].lower() == 'true',
                                'theme': self.classify_story_theme(parts[1] + ' ' + parts[2])
                            }
                            self.existing_stories[story_id] = story
        
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
        
        print(f"✅ 加载完成: {len(self.existing_stories)}个故事, {sum(len(choices) for choices in self.choices.values())}个选择")
    
    def classify_story_theme(self, text: str) -> str:
        """根据文本内容分类故事主题"""
        text_lower = text.lower()
        theme_scores = {}
        
        for theme, keywords in self.story_themes.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                theme_scores[theme] = score
        
        if theme_scores:
            return max(theme_scores, key=theme_scores.get)
        return 'general'
    
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
        except Exception as e:
            print(f"❌ 加载TXT选择失败: {file_path} - {e}")
    
    def analyze_story_flow(self):
        """分析故事流程"""
        print("\n🔍 分析故事流程...")
        
        # 找出死路故事
        dead_ends = []
        for story_id in self.existing_stories:
            if story_id not in self.choices or len(self.choices[story_id]) == 0:
                if not self.existing_stories[story_id].get('is_ending', False):
                    dead_ends.append(story_id)
        
        # 找出指向不存在故事的选择
        broken_choices = []
        for story_id, choices in self.choices.items():
            for choice in choices:
                if choice['next_story_id'] not in self.existing_stories:
                    broken_choices.append(choice)
        
        print(f"   死路故事: {len(dead_ends)}个")
        print(f"   断链选择: {len(broken_choices)}个")
        
        return dead_ends, broken_choices
    
    def optimize_story_flow(self):
        """优化故事流程"""
        print("\n🔧 优化故事流程...")
        
        dead_ends, broken_choices = self.analyze_story_flow()
        optimized_choices = []
        
        # 修复断链选择
        for choice in broken_choices:
            new_target = self.find_optimal_target(choice)
            if new_target:
                choice['next_story_id'] = new_target
                choice['fixed'] = True
                optimized_choices.append(choice)
        
        # 为死路故事添加选择
        for story_id in dead_ends:
            new_choices = self.create_meaningful_choices(story_id)
            optimized_choices.extend(new_choices)
        
        # 确保主线连通性
        self.ensure_main_storyline_connectivity(optimized_choices)
        
        print(f"✅ 优化完成: 修复了{len(optimized_choices)}个选择")
        return optimized_choices
    
    def find_optimal_target(self, choice):
        """为选择找到最优目标故事"""
        current_story_id = choice['story_id']
        choice_text = choice['text'].lower()
        
        # 获取当前故事的主题
        current_story = self.existing_stories.get(current_story_id, {})
        current_theme = current_story.get('theme', 'general')
        
        # 根据选择文本确定目标主题
        target_theme = self.classify_story_theme(choice_text)
        
        # 寻找合适的汇入点
        if target_theme in self.convergence_points:
            convergence_point = self.convergence_points[target_theme]
            if convergence_point in self.existing_stories:
                return convergence_point
        
        # 寻找同主题的故事
        theme_stories = [
            story_id for story_id, story in self.existing_stories.items()
            if story.get('theme') == target_theme
        ]
        
        if theme_stories:
            # 选择最接近主线的故事
            for main_story in self.main_storyline:
                if main_story in theme_stories:
                    return main_story
            return theme_stories[0]
        
        # 回退到主线故事
        current_index = self.get_main_storyline_position(current_story_id)
        if current_index >= 0 and current_index < len(self.main_storyline) - 1:
            return self.main_storyline[current_index + 1]
        
        # 最后的备选
        return 'story_1_19'  # 默认汇入属性详情节点
    
    def create_meaningful_choices(self, story_id):
        """为故事创建有意义的选择"""
        story = self.existing_stories.get(story_id, {})
        story_theme = story.get('theme', 'general')
        
        choices = []
        
        # 根据故事主题创建不同类型的选择
        if story_theme == 'exploration':
            choices = [
                {
                    'story_id': story_id,
                    'text': '继续深入探索',
                    'next_story_id': self.convergence_points['exploration'],
                    'theme': 'exploration'
                },
                {
                    'story_id': story_id,
                    'text': '寻找其他线索',
                    'next_story_id': self.convergence_points['discovery'],
                    'theme': 'mystery'
                }
            ]
        elif story_theme == 'combat':
            choices = [
                {
                    'story_id': story_id,
                    'text': '准备战斗',
                    'next_story_id': self.convergence_points['combat'],
                    'theme': 'combat'
                },
                {
                    'story_id': story_id,
                    'text': '寻找战术优势',
                    'next_story_id': 'story_1_18',
                    'theme': 'exploration'
                }
            ]
        elif story_theme == 'dialogue':
            choices = [
                {
                    'story_id': story_id,
                    'text': '继续对话',
                    'next_story_id': self.convergence_points['dialogue'],
                    'theme': 'dialogue'
                },
                {
                    'story_id': story_id,
                    'text': '结束对话',
                    'next_story_id': self.get_next_main_story(story_id),
                    'theme': 'general'
                }
            ]
        else:
            # 通用选择
            choices = [
                {
                    'story_id': story_id,
                    'text': '继续前进',
                    'next_story_id': self.get_next_main_story(story_id),
                    'theme': 'general'
                },
                {
                    'story_id': story_id,
                    'text': '仔细观察',
                    'next_story_id': self.convergence_points['exploration'],
                    'theme': 'exploration'
                }
            ]
        
        # 添加标准字段
        for choice in choices:
            choice.update({
                'gold_cost': 0,
                'gold_reward': 0,
                'health_cost': 0,
                'health_reward': 0,
                'experience_reward': 10,
                'requirements': '',
                'is_available': True,
                'generated': True
            })
        
        return choices
    
    def get_main_storyline_position(self, story_id):
        """获取故事在主线中的位置"""
        try:
            return self.main_storyline.index(story_id)
        except ValueError:
            return -1
    
    def get_next_main_story(self, story_id):
        """获取下一个主线故事"""
        current_index = self.get_main_storyline_position(story_id)
        if current_index >= 0 and current_index < len(self.main_storyline) - 1:
            return self.main_storyline[current_index + 1]
        
        # 如果不在主线中，找到最近的主线故事
        story_num = int(story_id.split('_')[2]) if '_' in story_id else 1
        for main_story in self.main_storyline:
            main_num = int(main_story.split('_')[2])
            if main_num > story_num:
                return main_story
        
        return self.main_storyline[-1]  # 返回最后一个主线故事
    
    def ensure_main_storyline_connectivity(self, optimized_choices):
        """确保主线故事的连通性"""
        print("🔗 确保主线连通性...")
        
        for i in range(len(self.main_storyline) - 1):
            current_story = self.main_storyline[i]
            next_story = self.main_storyline[i + 1]
            
            # 检查是否有连接到下一个主线故事的选择
            has_connection = False
            for choice in self.choices.get(current_story, []):
                if choice['next_story_id'] == next_story:
                    has_connection = True
                    break
            
            # 如果没有连接，添加一个
            if not has_connection and current_story in self.existing_stories:
                main_choice = {
                    'story_id': current_story,
                    'text': '继续主线剧情',
                    'next_story_id': next_story,
                    'gold_cost': 0,
                    'gold_reward': 0,
                    'health_cost': 0,
                    'health_reward': 0,
                    'experience_reward': 15,
                    'requirements': '',
                    'is_available': True,
                    'main_storyline': True
                }
                optimized_choices.append(main_choice)
                self.choices[current_story].append(main_choice)
    
    def save_optimized_choices(self, optimized_choices):
        """保存优化后的选择"""
        if not optimized_choices:
            print("✅ 没有需要保存的优化选择")
            return
        
        # 合并所有有效选择
        all_valid_choices = []
        
        # 添加现有的有效选择
        for story_id, choices in self.choices.items():
            for choice in choices:
                if choice['next_story_id'] in self.existing_stories:
                    all_valid_choices.append(choice)
        
        # 添加优化后的选择
        all_valid_choices.extend(optimized_choices)
        
        # 保存为JSON格式
        output_file = 'novel_texts/optimized_story_flow.json'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_valid_choices, f, ensure_ascii=False, indent=2)
            print(f"✅ 保存优化选择: {len(all_valid_choices)}个 -> {output_file}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
        
        # 同时保存为TXT格式，便于导入后端
        txt_output_file = 'novel_texts/optimized_story_flow.txt'
        try:
            with open(txt_output_file, 'w', encoding='utf-8') as f:
                f.write("# 优化后的故事流程选择文件\n")
                f.write("# 支流汇入主流，确保故事连贯性\n\n")
                
                for choice in all_valid_choices:
                    line = f"{choice['story_id']}|{choice['text']}|{choice['next_story_id']}|{choice['gold_cost']}|{choice['gold_reward']}|{choice['health_cost']}|{choice['health_reward']}|{choice['experience_reward']}|{choice['requirements']}|{str(choice['is_available']).lower()}\n"
                    f.write(line)
            
            print(f"✅ 保存TXT格式: {len(all_valid_choices)}个 -> {txt_output_file}")
        except Exception as e:
            print(f"❌ 保存TXT失败: {e}")
    
    def generate_flow_report(self):
        """生成流程优化报告"""
        report = []
        report.append("# 故事流程优化报告\n")
        
        report.append("## 主线故事")
        for i, story_id in enumerate(self.main_storyline):
            if story_id in self.existing_stories:
                story = self.existing_stories[story_id]
                report.append(f"{i+1}. {story_id}: {story['title']}")
            else:
                report.append(f"{i+1}. {story_id}: [不存在]")
        report.append("")
        
        report.append("## 汇入点设计")
        for theme, convergence_point in self.convergence_points.items():
            report.append(f"- {theme} -> {convergence_point}")
        report.append("")
        
        report.append("## 故事主题分布")
        theme_count = {}
        for story in self.existing_stories.values():
            theme = story.get('theme', 'general')
            theme_count[theme] = theme_count.get(theme, 0) + 1
        
        for theme, count in sorted(theme_count.items()):
            report.append(f"- {theme}: {count}个故事")
        
        # 保存报告
        with open('story_flow_optimization_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✅ 生成流程报告: story_flow_optimization_report.md")

def main():
    optimizer = StoryFlowOptimizer()
    
    # 加载数据
    optimizer.load_data()
    
    # 分析故事流程
    optimizer.analyze_story_flow()
    
    # 优化故事流程
    optimized_choices = optimizer.optimize_story_flow()
    
    # 保存优化结果
    optimizer.save_optimized_choices(optimized_choices)
    
    # 生成报告
    optimizer.generate_flow_report()
    
    print(f"\n🎉 故事流程优化完成!")
    print("   支流已合理汇入主流")
    print("   确保了故事的连贯性和逻辑性")

if __name__ == "__main__":
    main()
