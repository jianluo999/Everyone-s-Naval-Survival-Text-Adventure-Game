#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查重复的story_id
"""

import json
from collections import Counter

def check_duplicates():
    scenes_file = "novel_texts/game_scenes/game_scenes_501_830.json"
    
    with open(scenes_file, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    # 统计story_id
    story_ids = [scene['story_id'] for scene in scenes]
    counter = Counter(story_ids)
    
    # 找出重复的
    duplicates = {story_id: count for story_id, count in counter.items() if count > 1}
    
    print(f"总场景数: {len(scenes)}")
    print(f"唯一story_id数: {len(counter)}")
    print(f"重复的story_id: {len(duplicates)}")
    
    if duplicates:
        print("\n重复的story_id:")
        for story_id, count in duplicates.items():
            print(f"  {story_id}: {count}次")
            
        # 显示重复场景的详情
        print("\n重复场景详情:")
        for story_id in list(duplicates.keys())[:5]:  # 只显示前5个
            matching_scenes = [s for s in scenes if s['story_id'] == story_id]
            print(f"\n{story_id}:")
            for i, scene in enumerate(matching_scenes):
                print(f"  场景{i+1}: {scene['title']}")
                print(f"    内容: {scene['content'][:50]}...")

if __name__ == "__main__":
    check_duplicates()
