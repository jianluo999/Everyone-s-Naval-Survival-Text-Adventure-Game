#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版小说转游戏脚本 - 将500+章节文件正确转换为游戏场景和选择
解决原有工作流中数据解析问题
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

class FixedNovelToGameConverter:
    def __init__(self):
        self.chapters_dir = "novel_texts/chapters"
        self.output_dir = "novel_texts/game_scenes"
        self.scenes = []
        self.choices = []
        self.processed_chapters = 0
        
    def convert_all_chapters(self):
        """转换所有章节文件"""
        print("🚀 开始批量转换章节文件为游戏场景...")
        
        # 确保输出目录存在
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # 获取所有章节文件
        chapter_files = sorted([f for f in os.listdir(self.chapters_dir) 
                               if f.startswith('chapter_') and f.endswith('_data.txt')])
        
        print(f"📚 发现 {len(chapter_files)} 个章节文件")
        
        for chapter_file in chapter_files:
            chapter_path = os.path.join(self.chapters_dir, chapter_file)
            try:
                scenes = self.convert_chapter_to_scenes(chapter_path)
                self.scenes.extend(scenes)
                self.processed_chapters += 1
                
                if self.processed_chapters % 50 == 0:
                    print(f"✅ 已处理 {self.processed_chapters}/{len(chapter_files)} 个章节")
                    
            except Exception as e:
                print(f"❌ 处理章节 {chapter_file} 时出错: {str(e)}")
                continue
        
        print(f"🎯 转换完成！共生成 {len(self.scenes)} 个场景，{len(self.choices)} 个选择")
        
        # 保存结果
        self.save_results()
        
    def convert_chapter_to_scenes(self, chapter_file: str) -> List[Dict]:
        """将单个章节文件转换为多个游戏场景"""
        
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取章节编号
        filename = os.path.basename(chapter_file)
        file_match = re.search(r'chapter_(\d+)_data\.txt', filename)
        if not file_match:
            return []
            
        chapter_num = int(file_match.group(1))
        
        # 提取章节标题
        lines = content.split('\n')
        title_line = lines[0] if lines else ""
        chapter_match = re.search(r'第(\d+)章\s*(.+)', title_line)
        
        if chapter_match:
            chapter_title = chapter_match.group(2).strip()
        else:
            chapter_title = f"第{chapter_num}章"
        
        # 分析章节内容，创建场景
        scenes = self.analyze_and_create_scenes(content, chapter_num, chapter_title)
        
        return scenes
    
    def analyze_and_create_scenes(self, content: str, chapter_num: int, chapter_title: str) -> List[Dict]:
        """分析章节内容并创建游戏场景"""
        scenes = []
        
        # 将内容按段落分割，过滤空行和标题
        paragraphs = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                paragraphs.append(line)
        
        if not paragraphs:
            return scenes
        
        # 智能分割场景：根据内容长度和语义分割
        scene_groups = self.smart_split_paragraphs(paragraphs)
        
        for i, scene_paragraphs in enumerate(scene_groups):
            if scene_paragraphs:
                scene_text = '\n'.join(scene_paragraphs)
                scene = self.create_scene(scene_text, chapter_num, chapter_title, i + 1)
                scenes.append(scene)
        
        return scenes
    
    def smart_split_paragraphs(self, paragraphs: List[str]) -> List[List[str]]:
        """智能分割段落为场景组"""
        scene_groups = []
        current_group = []
        current_length = 0
        
        for paragraph in paragraphs:
            current_group.append(paragraph)
            current_length += len(paragraph)
            
            # 场景分割条件：
            # 1. 累积长度超过400字符
            # 2. 遇到场景转换标志
            # 3. 对话结束
            should_split = (
                current_length > 400 or
                self.is_scene_break(paragraph) or
                (len(current_group) >= 4 and current_length > 200)
            )
            
            if should_split:
                scene_groups.append(current_group.copy())
                current_group = []
                current_length = 0
        
        # 添加最后一组
        if current_group:
            scene_groups.append(current_group)
        
        return scene_groups
    
    def is_scene_break(self, paragraph: str) -> bool:
        """判断是否应该在此处分割场景"""
        scene_break_indicators = [
            '......',
            '。。。。。。',
            '这时候',
            '突然',
            '接下来',
            '然后',
            '过了一会',
            '不久后',
            '与此同时',
            '正在这时',
            '就在这时',
            '半小时后',
            '一小时后',
            '几小时后'
        ]
        
        return any(indicator in paragraph for indicator in scene_break_indicators)
    
    def create_scene(self, text: str, chapter_num: int, chapter_title: str, scene_num: int) -> Dict:
        """创建单个游戏场景"""
        story_id = f"story_{chapter_num}_{scene_num}"
        
        # 生成场景标题
        scene_title = f"{chapter_title} - 场景{scene_num}"
        
        # 转换为第二人称视角
        converted_text = self.convert_to_second_person(text)
        
        # 确保文本长度适中
        if len(converted_text) > 800:
            converted_text = converted_text[:800] + "..."
        
        scene = {
            "story_id": story_id,
            "title": scene_title,
            "content": converted_text,
            "chapter": chapter_num,
            "scene": scene_num,
            "story_type": self.determine_story_type(text),
            "is_ending": False
        }
        
        # 为场景创建选择
        choices = self.create_choices_for_scene(story_id, text, chapter_num, scene_num)
        self.choices.extend(choices)
        
        return scene
    
    def convert_to_second_person(self, text: str) -> str:
        """将文本转换为第二人称视角"""
        # 替换主角名字和第三人称为第二人称
        replacements = [
            (r'杨逸', '你'),
            (r'他(?!们|人|的船|的话|说|们的)', '你'),
            (r'他的', '你的'),
            (r'他在', '你在'),
            (r'他看', '你看'),
            (r'他想', '你想'),
            (r'他说', '你说'),
            (r'他发现', '你发现'),
            (r'他感到', '你感到'),
            (r'他觉得', '你觉得'),
            (r'他决定', '你决定'),
            (r'他开始', '你开始'),
            (r'他继续', '你继续'),
            (r'他试着', '你试着'),
            (r'他拿起', '你拿起'),
            (r'他走', '你走'),
            (r'他来到', '你来到'),
            (r'他进入', '你进入'),
            (r'他离开', '你离开'),
            (r'他打开', '你打开'),
            (r'他合上', '你合上'),
            (r'他推开', '你推开'),
            (r'他起身', '你起身'),
            (r'他抬头', '你抬头'),
            (r'他低头', '你低头')
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def determine_story_type(self, text: str) -> str:
        """根据文本内容确定故事类型"""
        if any(word in text for word in ['探索', '发现', '寻找', '搜索']):
            return 'exploration'
        elif any(word in text for word in ['对话', '聊天', '说话', '交流']):
            return 'dialogue'
        elif any(word in text for word in ['战斗', '攻击', '武器', '敌人']):
            return 'combat'
        elif any(word in text for word in ['钓鱼', '捕鱼', '鱼']):
            return 'fishing'
        elif any(word in text for word in ['生存', '食物', '水', '补给']):
            return 'survival'
        else:
            return 'general'
    
    def create_choices_for_scene(self, story_id: str, text: str, chapter_num: int, scene_num: int) -> List[Dict]:
        """为场景创建选择"""
        choices = []
        
        # 根据文本内容生成相关的选择
        choice_templates = self.get_choice_templates(text)
        
        for i, template in enumerate(choice_templates[:3]):  # 最多3个选择
            next_story_id = self.determine_next_story_id(chapter_num, scene_num, i + 1)
            
            choice = {
                "story_id": story_id,
                "text": template["text"],
                "next_story_id": next_story_id,
                "requirements": template.get("requirements", ""),
                "is_available": True,
                "health_cost": template.get("health_cost", 0),
                "health_reward": template.get("health_reward", 0),
                "gold_cost": template.get("gold_cost", 0),
                "gold_reward": template.get("gold_reward", 0),
                "experience_reward": template.get("experience_reward", 5)
            }
            choices.append(choice)
        
        return choices
    
    def get_choice_templates(self, text: str) -> List[Dict]:
        """根据文本内容获取选择模板"""
        templates = []
        
        # 基础选择模板
        if '探索' in text or '寻找' in text:
            templates.append({
                "text": "仔细探索周围环境",
                "experience_reward": 8
            })
        
        if '对话' in text or '聊天' in text:
            templates.append({
                "text": "与其他人交流",
                "experience_reward": 6
            })
        
        if '装备' in text or '物品' in text:
            templates.append({
                "text": "检查获得的物品",
                "experience_reward": 7
            })
        
        # 如果没有特定模板，使用通用模板
        if not templates:
            templates = [
                {"text": "继续前进", "experience_reward": 5},
                {"text": "停下来思考", "experience_reward": 4},
                {"text": "观察周围情况", "experience_reward": 6}
            ]
        
        # 确保至少有2个选择
        while len(templates) < 2:
            templates.append({"text": "继续探索", "experience_reward": 5})
        
        return templates
    
    def determine_next_story_id(self, chapter_num: int, scene_num: int, choice_num: int) -> str:
        """确定下一个故事ID"""
        # 简单的线性推进逻辑
        next_scene = scene_num + choice_num
        
        # 如果超出当前章节，进入下一章
        if next_scene > 10:  # 假设每章最多10个场景
            next_chapter = chapter_num + 1
            next_scene = 1
        else:
            next_chapter = chapter_num
        
        return f"story_{next_chapter}_{next_scene}"

    def save_results(self):
        """保存转换结果"""
        print("💾 保存转换结果...")

        # 保存场景数据
        scenes_file = os.path.join(self.output_dir, "converted_scenes.json")
        with open(scenes_file, 'w', encoding='utf-8') as f:
            json.dump(self.scenes, f, ensure_ascii=False, indent=2)

        # 保存选择数据
        choices_file = os.path.join(self.output_dir, "converted_choices.json")
        with open(choices_file, 'w', encoding='utf-8') as f:
            json.dump(self.choices, f, ensure_ascii=False, indent=2)

        # 生成统计报告
        self.generate_conversion_report()

        print(f"✅ 结果已保存到 {self.output_dir}")
        print(f"📖 场景文件: {scenes_file}")
        print(f"🎯 选择文件: {choices_file}")

    def generate_conversion_report(self):
        """生成转换报告"""
        report_file = os.path.join(self.output_dir, "conversion_report.md")

        # 统计数据
        total_scenes = len(self.scenes)
        total_choices = len(self.choices)
        chapters_processed = self.processed_chapters

        # 按章节统计
        chapter_stats = {}
        for scene in self.scenes:
            chapter = scene['chapter']
            if chapter not in chapter_stats:
                chapter_stats[chapter] = {'scenes': 0, 'choices': 0}
            chapter_stats[chapter]['scenes'] += 1

        for choice in self.choices:
            story_id = choice['story_id']
            chapter = int(story_id.split('_')[1])
            if chapter in chapter_stats:
                chapter_stats[chapter]['choices'] += 1

        # 按故事类型统计
        type_stats = {}
        for scene in self.scenes:
            story_type = scene['story_type']
            type_stats[story_type] = type_stats.get(story_type, 0) + 1

        # 生成报告
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 小说转游戏转换报告\n\n")
            f.write("## 总体统计\n")
            f.write(f"- 处理章节数: {chapters_processed}\n")
            f.write(f"- 生成场景数: {total_scenes}\n")
            f.write(f"- 生成选择数: {total_choices}\n")
            f.write(f"- 平均每章场景数: {total_scenes/chapters_processed:.1f}\n")
            f.write(f"- 平均每场景选择数: {total_choices/total_scenes:.1f}\n\n")

            f.write("## 故事类型分布\n")
            for story_type, count in sorted(type_stats.items()):
                f.write(f"- {story_type}: {count} 个场景\n")
            f.write("\n")

            f.write("## 章节统计（前20章）\n")
            for chapter in sorted(chapter_stats.keys())[:20]:
                stats = chapter_stats[chapter]
                f.write(f"- 第{chapter}章: {stats['scenes']} 个场景, {stats['choices']} 个选择\n")

            if len(chapter_stats) > 20:
                f.write(f"- ... 还有 {len(chapter_stats) - 20} 个章节\n")

        print(f"📊 转换报告已生成: {report_file}")

def main():
    """主函数"""
    print("修复版小说转游戏转换器")
    print("=" * 50)

    converter = FixedNovelToGameConverter()

    # 检查输入目录
    if not os.path.exists(converter.chapters_dir):
        print(f"❌ 错误: 找不到章节目录 {converter.chapters_dir}")
        return

    # 开始转换
    try:
        converter.convert_all_chapters()
        print("\n🎉 转换完成！")

    except Exception as e:
        print(f"❌ 转换过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
