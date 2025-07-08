#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复重复的场景
"""

import json
from collections import defaultdict

def fix_duplicates():
    scenes_file = "novel_texts/game_scenes/game_scenes_501_830.json"
    
    with open(scenes_file, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    print(f"原始场景数: {len(scenes)}")
    
    # 按story_id分组
    grouped_scenes = defaultdict(list)
    for scene in scenes:
        grouped_scenes[scene['story_id']].append(scene)
    
    # 去重：对于重复的story_id，只保留第一个
    unique_scenes = []
    duplicates_removed = 0
    
    for story_id, scene_list in grouped_scenes.items():
        if len(scene_list) > 1:
            print(f"发现重复: {story_id} ({len(scene_list)}个)")
            # 选择内容更长的场景
            best_scene = max(scene_list, key=lambda s: len(s.get('content', '')))
            unique_scenes.append(best_scene)
            duplicates_removed += len(scene_list) - 1
        else:
            unique_scenes.append(scene_list[0])
    
    print(f"去重后场景数: {len(unique_scenes)}")
    print(f"移除重复场景: {duplicates_removed}")
    
    # 按story_id排序
    unique_scenes.sort(key=lambda s: s['story_id'])
    
    # 保存修复后的数据
    output_file = "novel_texts/game_scenes/game_scenes_501_830_fixed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_scenes, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 修复后的数据已保存到: {output_file}")
    
    # 验证修复结果
    story_ids = [scene['story_id'] for scene in unique_scenes]
    if len(story_ids) == len(set(story_ids)):
        print("✅ 验证通过：没有重复的story_id")
    else:
        print("❌ 验证失败：仍有重复的story_id")
    
    return unique_scenes

if __name__ == "__main__":
    fix_duplicates()
