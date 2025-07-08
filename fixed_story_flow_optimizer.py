#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版故事流优化器 - 处理大量场景和选择的连接问题
确保所有故事分支都有合理的连接，避免死路和不可达故事
"""

import json
import os
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

class FixedStoryFlowOptimizer:
    def __init__(self):
        self.scenes_file = "novel_texts/game_scenes/converted_scenes.json"
        self.choices_file = "novel_texts/game_scenes/converted_choices.json"
        self.output_dir = "novel_texts/optimized_scenes"
        
        self.scenes = {}  # story_id -> scene_data
        self.choices = defaultdict(list)  # story_id -> [choices]
        self.story_graph = defaultdict(set)  # story_id -> {next_story_ids}
        self.reverse_graph = defaultdict(set)  # story_id -> {prev_story_ids}
        
        self.dead_ends = set()
        self.unreachable = set()
        self.fixed_choices = []
        
    def load_data(self):
        """加载场景和选择数据"""
        print("📚 加载转换后的场景和选择数据...")
        
        # 加载场景数据
        if os.path.exists(self.scenes_file):
            with open(self.scenes_file, 'r', encoding='utf-8') as f:
                scenes_list = json.load(f)
                for scene in scenes_list:
                    self.scenes[scene['story_id']] = scene
            print(f"✅ 加载了 {len(self.scenes)} 个场景")
        else:
            print(f"❌ 找不到场景文件: {self.scenes_file}")
            return False
        
        # 加载选择数据
        if os.path.exists(self.choices_file):
            with open(self.choices_file, 'r', encoding='utf-8') as f:
                choices_list = json.load(f)
                for choice in choices_list:
                    story_id = choice['story_id']
                    self.choices[story_id].append(choice)
                    
                    # 构建故事图
                    next_story_id = choice['next_story_id']
                    self.story_graph[story_id].add(next_story_id)
                    self.reverse_graph[next_story_id].add(story_id)
                    
            print(f"✅ 加载了 {len(choices_list)} 个选择")
        else:
            print(f"❌ 找不到选择文件: {self.choices_file}")
            return False
        
        return True
    
    def analyze_story_flow(self):
        """分析故事流，找出问题"""
        print("🔍 分析故事流...")
        
        # 找出死路（没有出路的故事）
        for story_id in self.scenes:
            if story_id not in self.story_graph or not self.story_graph[story_id]:
                self.dead_ends.add(story_id)
        
        # 找出不可达的故事（没有入路的故事，除了起始故事）
        start_stories = {f"story_1_1"}  # 起始故事
        for story_id in self.scenes:
            if story_id not in start_stories and story_id not in self.reverse_graph:
                self.unreachable.add(story_id)
        
        print(f"🚫 发现 {len(self.dead_ends)} 个死路故事")
        print(f"🔒 发现 {len(self.unreachable)} 个不可达故事")
        
        return len(self.dead_ends), len(self.unreachable)
    
    def fix_dead_ends(self):
        """修复死路问题"""
        print("🔧 修复死路问题...")
        
        fixed_count = 0
        for story_id in self.dead_ends:
            # 为死路故事创建选择
            new_choices = self.create_choices_for_dead_end(story_id)
            
            for choice in new_choices:
                self.choices[story_id].append(choice)
                self.fixed_choices.append(choice)
                
                # 更新故事图
                next_story_id = choice['next_story_id']
                self.story_graph[story_id].add(next_story_id)
                self.reverse_graph[next_story_id].add(story_id)
                
                fixed_count += 1
        
        print(f"✅ 修复了 {fixed_count} 个死路选择")
        return fixed_count
    
    def create_choices_for_dead_end(self, story_id: str) -> List[Dict]:
        """为死路故事创建选择"""
        choices = []
        
        # 解析故事ID
        parts = story_id.split('_')
        if len(parts) >= 3:
            chapter = int(parts[1])
            scene = int(parts[2])
        else:
            return choices
        
        # 创建3个选择，指向不同的下一个故事
        choice_templates = [
            {"text": "继续前进", "experience_reward": 5},
            {"text": "仔细观察", "experience_reward": 6},
            {"text": "准备行动", "experience_reward": 4}
        ]
        
        for i, template in enumerate(choice_templates):
            next_story_id = self.find_suitable_next_story(chapter, scene, i + 1)
            
            choice = {
                "story_id": story_id,
                "text": template["text"],
                "next_story_id": next_story_id,
                "requirements": "",
                "is_available": True,
                "health_cost": 0,
                "health_reward": 0,
                "gold_cost": 0,
                "gold_reward": 0,
                "experience_reward": template["experience_reward"],
                "fixed": True
            }
            choices.append(choice)
        
        return choices
    
    def find_suitable_next_story(self, chapter: int, scene: int, choice_num: int) -> str:
        """找到合适的下一个故事ID"""
        # 优先选择同章节的下一个场景
        next_scene = scene + choice_num
        candidate = f"story_{chapter}_{next_scene}"
        
        if candidate in self.scenes:
            return candidate
        
        # 如果同章节没有，尝试下一章的开始
        next_chapter = chapter + 1
        candidate = f"story_{next_chapter}_1"
        
        if candidate in self.scenes:
            return candidate
        
        # 如果都没有，找最近的可用故事
        for test_chapter in range(chapter + 1, chapter + 10):
            for test_scene in range(1, 6):
                candidate = f"story_{test_chapter}_{test_scene}"
                if candidate in self.scenes:
                    return candidate
        
        # 最后的备选：回到第一章
        return "story_1_1"
    
    def fix_unreachable_stories(self):
        """修复不可达故事问题"""
        print("🔧 修复不可达故事问题...")
        
        fixed_count = 0
        for story_id in self.unreachable:
            # 为不可达故事创建入路
            source_stories = self.find_suitable_source_stories(story_id)
            
            for source_story_id in source_stories[:2]:  # 最多创建2个入路
                new_choice = self.create_choice_to_unreachable(source_story_id, story_id)
                
                self.choices[source_story_id].append(new_choice)
                self.fixed_choices.append(new_choice)
                
                # 更新故事图
                self.story_graph[source_story_id].add(story_id)
                self.reverse_graph[story_id].add(source_story_id)
                
                fixed_count += 1
        
        print(f"✅ 为 {fixed_count} 个不可达故事创建了入路")
        return fixed_count
    
    def find_suitable_source_stories(self, target_story_id: str) -> List[str]:
        """找到合适的源故事来连接到目标故事"""
        # 解析目标故事ID
        parts = target_story_id.split('_')
        if len(parts) >= 3:
            chapter = int(parts[1])
            scene = int(parts[2])
        else:
            return []
        
        source_stories = []
        
        # 优先选择同章节的前面场景
        for prev_scene in range(max(1, scene - 3), scene):
            candidate = f"story_{chapter}_{prev_scene}"
            if candidate in self.scenes and len(self.choices[candidate]) < 4:
                source_stories.append(candidate)
        
        # 如果同章节没有，选择前一章的场景
        if not source_stories and chapter > 1:
            prev_chapter = chapter - 1
            for test_scene in range(1, 11):
                candidate = f"story_{prev_chapter}_{test_scene}"
                if candidate in self.scenes and len(self.choices[candidate]) < 4:
                    source_stories.append(candidate)
                    if len(source_stories) >= 2:
                        break
        
        return source_stories
    
    def create_choice_to_unreachable(self, source_story_id: str, target_story_id: str) -> Dict:
        """创建指向不可达故事的选择"""
        return {
            "story_id": source_story_id,
            "text": "探索新的方向",
            "next_story_id": target_story_id,
            "requirements": "",
            "is_available": True,
            "health_cost": 0,
            "health_reward": 0,
            "gold_cost": 0,
            "gold_reward": 0,
            "experience_reward": 7,
            "fixed": True
        }
    
    def optimize_story_flow(self):
        """优化故事流"""
        print("🚀 开始优化故事流...")
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 加载数据
        if not self.load_data():
            return False
        
        # 分析问题
        dead_count, unreachable_count = self.analyze_story_flow()
        
        # 修复问题
        fixed_dead = self.fix_dead_ends()
        fixed_unreachable = self.fix_unreachable_stories()
        
        # 重新分析验证
        self.dead_ends.clear()
        self.unreachable.clear()
        final_dead, final_unreachable = self.analyze_story_flow()
        
        # 保存结果
        self.save_optimized_data()
        
        # 生成报告
        self.generate_optimization_report(dead_count, unreachable_count, 
                                        fixed_dead, fixed_unreachable,
                                        final_dead, final_unreachable)
        
        print("🎉 故事流优化完成！")
        return True

    def save_optimized_data(self):
        """保存优化后的数据"""
        print("💾 保存优化后的数据...")

        # 保存优化后的场景
        scenes_output = os.path.join(self.output_dir, "optimized_scenes.json")
        scenes_list = list(self.scenes.values())
        with open(scenes_output, 'w', encoding='utf-8') as f:
            json.dump(scenes_list, f, ensure_ascii=False, indent=2)

        # 保存优化后的选择
        choices_output = os.path.join(self.output_dir, "optimized_choices.json")
        all_choices = []
        for story_id, choices in self.choices.items():
            all_choices.extend(choices)

        with open(choices_output, 'w', encoding='utf-8') as f:
            json.dump(all_choices, f, ensure_ascii=False, indent=2)

        # 保存修复的选择
        fixed_output = os.path.join(self.output_dir, "fixed_choices.json")
        with open(fixed_output, 'w', encoding='utf-8') as f:
            json.dump(self.fixed_choices, f, ensure_ascii=False, indent=2)

        print(f"✅ 优化数据已保存到 {self.output_dir}")

    def generate_optimization_report(self, initial_dead: int, initial_unreachable: int,
                                   fixed_dead: int, fixed_unreachable: int,
                                   final_dead: int, final_unreachable: int):
        """生成优化报告"""
        report_file = os.path.join(self.output_dir, "optimization_report.md")

        total_scenes = len(self.scenes)
        total_choices = sum(len(choices) for choices in self.choices.values())
        fixed_choices_count = len(self.fixed_choices)

        # 统计故事类型
        type_stats = defaultdict(int)
        for scene in self.scenes.values():
            type_stats[scene['story_type']] += 1

        # 统计章节覆盖
        chapters = set()
        for story_id in self.scenes:
            parts = story_id.split('_')
            if len(parts) >= 2:
                chapters.add(int(parts[1]))

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 故事流优化报告\n\n")

            f.write("## 总体统计\n")
            f.write(f"- 总场景数: {total_scenes}\n")
            f.write(f"- 总选择数: {total_choices}\n")
            f.write(f"- 修复选择数: {fixed_choices_count}\n")
            f.write(f"- 覆盖章节数: {len(chapters)}\n")
            f.write(f"- 平均每场景选择数: {total_choices/total_scenes:.1f}\n\n")

            f.write("## 问题修复统计\n")
            f.write(f"- 初始死路故事: {initial_dead}\n")
            f.write(f"- 初始不可达故事: {initial_unreachable}\n")
            f.write(f"- 修复死路选择: {fixed_dead}\n")
            f.write(f"- 修复不可达入路: {fixed_unreachable}\n")
            f.write(f"- 最终死路故事: {final_dead}\n")
            f.write(f"- 最终不可达故事: {final_unreachable}\n\n")

            f.write("## 故事类型分布\n")
            for story_type, count in sorted(type_stats.items()):
                f.write(f"- {story_type}: {count} 个场景\n")
            f.write("\n")

            f.write("## 章节覆盖范围\n")
            sorted_chapters = sorted(chapters)
            f.write(f"- 起始章节: 第{sorted_chapters[0]}章\n")
            f.write(f"- 结束章节: 第{sorted_chapters[-1]}章\n")
            f.write(f"- 章节范围: {sorted_chapters[0]}-{sorted_chapters[-1]}\n")

            # 检查缺失的章节
            missing_chapters = []
            for i in range(sorted_chapters[0], sorted_chapters[-1] + 1):
                if i not in chapters:
                    missing_chapters.append(i)

            if missing_chapters:
                f.write(f"- 缺失章节: {missing_chapters[:10]}")
                if len(missing_chapters) > 10:
                    f.write(f" (还有{len(missing_chapters)-10}个)")
                f.write("\n")
            else:
                f.write("- 章节完整性: 完整\n")

        print(f"📊 优化报告已生成: {report_file}")

def main():
    """主函数"""
    print("修复版故事流优化器")
    print("=" * 50)
    
    optimizer = FixedStoryFlowOptimizer()
    
    try:
        success = optimizer.optimize_story_flow()
        if success:
            print("\n✅ 优化成功完成！")
        else:
            print("\n❌ 优化过程中出现问题")
            
    except Exception as e:
        print(f"❌ 优化过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
