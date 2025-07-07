#!/usr/bin/env python3
"""
提取有效选择 - 只保留实际存在的故事的选择
"""

import os

def extract_valid_choices():
    # 实际存在的故事ID
    existing_stories = {
        'story_1_18', 'story_1_19', 'story_1_20', 'story_1_21', 
        'story_1_22', 'story_1_23', 'story_1_24', 'story_1_25', 
        'story_1_26', 'story_1_27', 'story_1_28', 'story_1_29', 'story_1_30'
    }
    
    valid_choices = []
    
    # 读取优化后的选择文件
    if os.path.exists('novel_texts/optimized_story_flow.txt'):
        with open('novel_texts/optimized_story_flow.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 10:
                        story_id = parts[0]
                        next_story_id = parts[2]
                        
                        # 只保留源故事和目标故事都存在的选择
                        if story_id in existing_stories and next_story_id in existing_stories:
                            valid_choices.append(line)
    
    # 为每个现有故事确保至少有2个选择
    story_choice_count = {}
    for choice_line in valid_choices:
        story_id = choice_line.split('|')[0]
        story_choice_count[story_id] = story_choice_count.get(story_id, 0) + 1
    
    # 为选择不足的故事添加基本选择
    additional_choices = []
    for story_id in existing_stories:
        if story_choice_count.get(story_id, 0) < 2:
            needed = 2 - story_choice_count.get(story_id, 0)
            
            # 根据故事ID生成合适的下一个故事
            story_num = int(story_id.split('_')[2])
            
            for i in range(needed):
                if i == 0:
                    # 第一个选择：继续主线
                    next_num = story_num + 1
                    if next_num <= 30:
                        next_story = f"story_1_{next_num}"
                        if next_story in existing_stories:
                            choice_line = f"{story_id}|继续前进|{next_story}|0|0|0|0|10||true"
                            additional_choices.append(choice_line)
                        else:
                            # 如果下一个不存在，选择一个存在的
                            choice_line = f"{story_id}|继续前进|story_1_26|0|0|0|0|10||true"
                            additional_choices.append(choice_line)
                else:
                    # 第二个选择：回顾或思考
                    prev_num = max(18, story_num - 1)
                    prev_story = f"story_1_{prev_num}"
                    if prev_story in existing_stories:
                        choice_line = f"{story_id}|回顾之前的信息|{prev_story}|0|0|0|0|8||true"
                        additional_choices.append(choice_line)
                    else:
                        choice_line = f"{story_id}|仔细思考|story_1_18|0|0|0|0|8||true"
                        additional_choices.append(choice_line)
    
    # 合并所有有效选择
    all_valid_choices = valid_choices + additional_choices
    
    # 保存到新文件
    output_file = 'novel_texts/final_valid_choices.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 最终有效选择文件\n")
        f.write("# 只包含实际存在的故事之间的选择\n")
        f.write("# 格式: 故事ID|选择文本|下一个故事ID|金币消耗|金币奖励|生命消耗|生命奖励|经验奖励|要求|是否可用\n\n")
        
        for choice_line in all_valid_choices:
            f.write(choice_line + '\n')
    
    print(f"✅ 提取有效选择: {len(all_valid_choices)}个")
    print(f"   原始选择: {len(valid_choices)}个")
    print(f"   补充选择: {len(additional_choices)}个")
    print(f"   保存到: {output_file}")
    
    # 统计每个故事的选择数量
    final_count = {}
    for choice_line in all_valid_choices:
        story_id = choice_line.split('|')[0]
        final_count[story_id] = final_count.get(story_id, 0) + 1
    
    print("\n📊 每个故事的选择数量:")
    for story_id in sorted(existing_stories):
        count = final_count.get(story_id, 0)
        print(f"   {story_id}: {count}个选择")

if __name__ == "__main__":
    extract_valid_choices()
