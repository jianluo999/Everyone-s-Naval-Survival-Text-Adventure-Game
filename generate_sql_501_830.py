#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成501-830章节的SQL插入语句
创建stories和choices表的数据
"""

import json
import os
from typing import List, Dict

class SQLGenerator:
    def __init__(self):
        self.input_file = "novel_texts/game_scenes/game_scenes_501_830.json"
        self.output_dir = "novel_texts/optimized_sql"
        
    def load_scenes(self) -> List[Dict]:
        """加载游戏场景数据"""
        print("=== 加载游戏场景数据 ===")
        
        if not os.path.exists(self.input_file):
            print(f"❌ 文件不存在: {self.input_file}")
            return []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            scenes = json.load(f)
        
        print(f"✅ 加载了{len(scenes)}个游戏场景")
        return scenes
    
    def escape_sql_string(self, text: str) -> str:
        """转义SQL字符串"""
        if not text:
            return ""
        
        # 转义单引号和反斜杠
        text = text.replace("\\", "\\\\")
        text = text.replace("'", "\\'")
        text = text.replace('"', '\\"')
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\r')
        text = text.replace('\t', '\\t')
        
        return text
    
    def generate_stories_sql(self, scenes: List[Dict]) -> str:
        """生成stories表的SQL"""
        print("=== 生成stories表SQL ===")
        
        sql_lines = [
            "-- Stories表插入语句 (501-830章)",
            "-- 总共 {} 个故事场景".format(len(scenes)),
            "",
            "INSERT INTO stories (story_id, title, content) VALUES"
        ]
        
        story_values = []
        for scene in scenes:
            story_id = self.escape_sql_string(scene['story_id'])
            title = self.escape_sql_string(scene['title'])
            content = self.escape_sql_string(scene['content'])
            
            value = f"('{story_id}', '{title}', '{content}')"
            story_values.append(value)
        
        # 分批插入，每1000条一批
        batch_size = 1000
        all_sql = []
        
        for i in range(0, len(story_values), batch_size):
            batch = story_values[i:i + batch_size]
            batch_sql = sql_lines.copy()
            batch_sql.append(",\n".join(batch) + ";")
            batch_sql.append("")
            all_sql.extend(batch_sql)
        
        print(f"✅ 生成了{len(scenes)}个故事的SQL插入语句")
        return "\n".join(all_sql)
    
    def generate_choices_sql(self, scenes: List[Dict]) -> str:
        """生成choices表的SQL"""
        print("=== 生成choices表SQL ===")
        
        sql_lines = [
            "-- Choices表插入语句 (501-830章)",
            "",
            "INSERT INTO choices (story_id, choice_text, next_story_id) VALUES"
        ]
        
        choice_values = []
        total_choices = 0
        
        for scene in scenes:
            story_id = scene['story_id']
            choices = scene.get('choices', [])
            
            for choice in choices:
                choice_text = self.escape_sql_string(choice.get('text', ''))
                next_story_id = self.escape_sql_string(choice.get('nextStoryId', ''))
                
                if choice_text and next_story_id:
                    value = f"('{story_id}', '{choice_text}', '{next_story_id}')"
                    choice_values.append(value)
                    total_choices += 1
        
        # 分批插入
        batch_size = 1000
        all_sql = []
        
        for i in range(0, len(choice_values), batch_size):
            batch = choice_values[i:i + batch_size]
            batch_sql = sql_lines.copy()
            batch_sql.append(",\n".join(batch) + ";")
            batch_sql.append("")
            all_sql.extend(batch_sql)
        
        print(f"✅ 生成了{total_choices}个选择的SQL插入语句")
        return "\n".join(all_sql)
    
    def save_sql_files(self, stories_sql: str, choices_sql: str):
        """保存SQL文件"""
        print("=== 保存SQL文件 ===")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 保存stories SQL
        stories_file = os.path.join(self.output_dir, "stories_501_830.sql")
        with open(stories_file, 'w', encoding='utf-8') as f:
            f.write(stories_sql)
        print(f"✅ Stories SQL已保存到: {stories_file}")
        
        # 保存choices SQL
        choices_file = os.path.join(self.output_dir, "choices_501_830.sql")
        with open(choices_file, 'w', encoding='utf-8') as f:
            f.write(choices_sql)
        print(f"✅ Choices SQL已保存到: {choices_file}")
        
        # 生成合并的SQL文件
        combined_file = os.path.join(self.output_dir, "combined_501_830.sql")
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write("-- 501-830章节完整SQL数据\n")
            f.write("-- 包含stories和choices表的插入语句\n\n")
            f.write("-- 开始事务\n")
            f.write("START TRANSACTION;\n\n")
            f.write(stories_sql)
            f.write("\n\n")
            f.write(choices_sql)
            f.write("\n\n-- 提交事务\n")
            f.write("COMMIT;\n")
        print(f"✅ 合并SQL已保存到: {combined_file}")
    
    def validate_data(self, scenes: List[Dict]):
        """验证数据质量"""
        print("=== 验证数据质量 ===")
        
        # 统计信息
        total_scenes = len(scenes)
        total_choices = sum(len(scene.get('choices', [])) for scene in scenes)
        
        # 检查空内容
        empty_content_scenes = [s for s in scenes if not s.get('content', '').strip()]
        empty_title_scenes = [s for s in scenes if not s.get('title', '').strip()]
        
        # 检查选择连接
        all_story_ids = {scene['story_id'] for scene in scenes}
        broken_choices = []
        
        for scene in scenes:
            for choice in scene.get('choices', []):
                next_story_id = choice.get('nextStoryId', '')
                if next_story_id and next_story_id not in all_story_ids:
                    # 检查是否指向其他章节
                    if not (next_story_id.startswith('story_') and 
                           (int(next_story_id.split('_')[1]) < 501 or 
                            int(next_story_id.split('_')[1]) > 830)):
                        broken_choices.append({
                            'from': scene['story_id'],
                            'to': next_story_id,
                            'choice': choice.get('text', '')
                        })
        
        print(f"数据质量报告:")
        print(f"  总场景数: {total_scenes}")
        print(f"  总选择数: {total_choices}")
        print(f"  平均每场景选择数: {total_choices/total_scenes:.1f}")
        print(f"  空内容场景: {len(empty_content_scenes)}")
        print(f"  空标题场景: {len(empty_title_scenes)}")
        print(f"  断裂选择: {len(broken_choices)}")
        
        if broken_choices:
            print(f"  前5个断裂选择:")
            for choice in broken_choices[:5]:
                print(f"    {choice['from']} -> {choice['to']}: {choice['choice']}")
        
        # 章节覆盖范围
        chapter_numbers = set()
        for scene in scenes:
            story_id = scene['story_id']
            if story_id.startswith('story_'):
                parts = story_id.split('_')
                if len(parts) >= 2:
                    try:
                        chapter_num = int(parts[1])
                        chapter_numbers.add(chapter_num)
                    except ValueError:
                        pass
        
        if chapter_numbers:
            min_chapter = min(chapter_numbers)
            max_chapter = max(chapter_numbers)
            print(f"  章节范围: {min_chapter} - {max_chapter}")
            print(f"  章节数量: {len(chapter_numbers)}")
        
        return len(empty_content_scenes) == 0 and len(empty_title_scenes) == 0
    
    def run(self):
        """运行完整SQL生成流程"""
        print("SQL生成器 - 501-830章")
        print("=" * 50)
        
        # 1. 加载场景数据
        scenes = self.load_scenes()
        if not scenes:
            print("❌ 加载场景数据失败")
            return False
        
        # 2. 验证数据质量
        is_valid = self.validate_data(scenes)
        
        # 3. 生成SQL
        stories_sql = self.generate_stories_sql(scenes)
        choices_sql = self.generate_choices_sql(scenes)
        
        # 4. 保存SQL文件
        self.save_sql_files(stories_sql, choices_sql)
        
        if is_valid:
            print("\n🎉 SQL生成完成且数据验证通过!")
        else:
            print("\n⚠️ SQL生成完成但数据存在问题")
        
        return True

def main():
    generator = SQLGenerator()
    generator.run()

if __name__ == "__main__":
    main()
