#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量集成脚本
将转换后的游戏剧情快速集成到Java后端
"""

import os
import re
from pathlib import Path

class BatchIntegrator:
    def __init__(self):
        self.story_counter = 1
        self.choice_counter = 1
    
    def parse_game_file(self, file_path):
        """解析游戏格式文件，提取场景和选择"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取章节标题
        title_match = re.search(r'# (.+)', content)
        chapter_title = title_match.group(1) if title_match else "未知章节"
        
        # 提取所有场景
        scenes = []
        scene_pattern = r'## 场景 (\d+)\s*\n\*\*场景ID\*\*: (.+?)\n\n(.*?)(?=### 选择分支|---|\Z)'
        choice_pattern = r'### 选择分支\s*\n((?:\d+\. .+\n?)+)'
        
        scene_matches = re.finditer(scene_pattern, content, re.DOTALL)
        
        for match in scene_matches:
            scene_num = match.group(1)
            scene_id = match.group(2)
            scene_content = match.group(3).strip()
            
            # 查找对应的选择分支
            choices = []
            choice_start = match.end()
            choice_match = re.search(choice_pattern, content[choice_start:choice_start+500])
            if choice_match:
                choice_lines = choice_match.group(1).strip().split('\n')
                for line in choice_lines:
                    choice_text = re.sub(r'^\d+\.\s*', '', line.strip())
                    if choice_text:
                        choices.append(choice_text)
            
            scenes.append({
                'scene_num': scene_num,
                'scene_id': scene_id,
                'content': scene_content,
                'choices': choices
            })
        
        return chapter_title, scenes
    
    def generate_java_stories(self, chapter_title, scenes, chapter_num):
        """生成Java故事代码"""
        java_code = []
        
        for i, scene in enumerate(scenes):
            story_var = f"story{chapter_num}_{i+1}"
            story_id = f"story_{chapter_num}_{i+1}"
            
            # 清理内容，转义引号
            content = scene['content'].replace('"', '\\"').replace('\n', '\\n')
            
            java_code.append(f"""
        // 第{chapter_num}章第{i+1}场景：{scene['scene_id']}
        Story {story_var} = new Story();
        {story_var}.setStoryId("{story_id}");
        {story_var}.setTitle("{chapter_title} - 场景{i+1}");
        {story_var}.setContent("{content}");
        {story_var}.setChapter({chapter_num});
        {story_var}.setScene({i+1});
        {story_var}.setStoryType("NORMAL");
        {story_var}.setIsEnding(false);
        storyRepository.save({story_var});""")
        
        return '\n'.join(java_code)
    
    def generate_java_choices(self, scenes, chapter_num):
        """生成Java选择代码"""
        java_code = []
        
        for i, scene in enumerate(scenes):
            story_id = f"story_{chapter_num}_{i+1}"
            
            for j, choice_text in enumerate(scene['choices']):
                choice_var = f"choice{chapter_num}_{i+1}_{j+1}"
                choice_id = f"choice_{chapter_num}_{i+1}_{j+1}"
                
                # 确定下一个故事ID
                next_story_id = f"story_{chapter_num}_{i+2}" if i+1 < len(scenes) else f"story_{chapter_num+1}_1"
                
                # 清理选择文本
                clean_choice = choice_text.replace('"', '\\"')
                
                java_code.append(f"""
        Choice {choice_var} = new Choice();
        {choice_var}.setChoiceId("{choice_id}");
        {choice_var}.setStoryId("{story_id}");
        {choice_var}.setChoiceText("{clean_choice}");
        {choice_var}.setNextStoryId("{next_story_id}");
        {choice_var}.setAttributeEffects("{{}}");
        choiceRepository.save({choice_var});""")
        
        return '\n'.join(java_code)
    
    def process_all_chapters(self, input_dir, output_file):
        """处理所有章节文件"""
        input_path = Path(input_dir)
        
        all_stories = []
        all_choices = []
        
        # 处理所有游戏文件
        game_files = sorted(input_path.glob("chapter_*_game.md"))
        
        for i, game_file in enumerate(game_files, 1):
            print(f"处理文件: {game_file.name}")
            
            chapter_title, scenes = self.parse_game_file(game_file)
            
            # 生成Java代码
            stories_code = self.generate_java_stories(chapter_title, scenes, i)
            choices_code = self.generate_java_choices(scenes, i)
            
            all_stories.append(stories_code)
            all_choices.append(choices_code)
        
        # 生成完整的Java文件内容
        java_content = f"""
    // ==================== 批量生成的故事内容 ====================
    private void createBatchStories() {{
        {''.join(all_stories)}
    }}
    
    // ==================== 批量生成的选择内容 ====================
    private void createBatchChoices() {{
        {''.join(all_choices)}
    }}
"""
        
        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(java_content)
        
        print(f"批量生成完成！代码已保存到: {output_file}")
        print(f"共处理 {len(game_files)} 个章节文件")
        print(f"生成 {sum(len(self.parse_game_file(f)[1]) for f in game_files)} 个场景")

def main():
    integrator = BatchIntegrator()
    
    input_dir = "../processed"
    output_file = "../batch_generated_java.txt"
    
    print("开始批量集成游戏剧情...")
    integrator.process_all_chapters(input_dir, output_file)
    print("批量集成完成！")

if __name__ == "__main__":
    main()
