#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将processed目录中的markdown文件转换为数据文件格式
格式: 场景号|标题|内容|类型|是否结局
"""

import os
import re
import sys

def parse_markdown_file(file_path):
    """解析markdown文件，提取场景信息"""
    scenes = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取章节标题
    chapter_match = re.search(r'# 第(\d+)章\s+(.+)', content)
    if not chapter_match:
        print(f"⚠️ 无法找到章节标题: {file_path}")
        return scenes
    
    chapter_num = int(chapter_match.group(1))
    chapter_title = chapter_match.group(2).strip()
    
    # 分割场景
    scene_sections = re.split(r'## 场景 (\d+)', content)[1:]  # 跳过第一个空元素
    
    for i in range(0, len(scene_sections), 2):
        if i + 1 >= len(scene_sections):
            break
            
        scene_num = int(scene_sections[i])
        scene_content = scene_sections[i + 1]
        
        # 提取场景内容（去掉选择分支部分）
        content_parts = scene_content.split('### 选择分支')[0]
        content_parts = content_parts.split('---')[0]
        
        # 清理内容
        clean_content = []
        lines = content_parts.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('**场景ID**'):
                # 移除markdown格式
                line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # 粗体
                line = re.sub(r'\*(.*?)\*', r'\1', line)      # 斜体
                clean_content.append(line)
        
        # 合并内容
        final_content = '\n\n'.join(clean_content).strip()
        
        if final_content:
            # 确定故事类型
            story_type = determine_story_type(final_content, scene_num)
            
            # 确定是否为结局
            is_ending = scene_num > 15 or '结束' in final_content or '完成' in final_content
            
            scenes.append({
                'scene': scene_num,
                'title': f"{chapter_title} - 场景{scene_num}",
                'content': final_content,
                'type': story_type,
                'is_ending': is_ending
            })
    
    return scenes

def determine_story_type(content, scene_num):
    """根据内容确定故事类型"""
    content_lower = content.lower()
    
    if scene_num <= 3:
        return "AWAKENING"
    elif '对话' in content or '聊天' in content or '"' in content:
        return "DIALOGUE"
    elif '教程' in content or '规则' in content or '手册' in content:
        return "TUTORIAL"
    elif '战斗' in content or '攻击' in content or '怪物' in content:
        return "COMBAT"
    elif '探索' in content or '发现' in content or '寻找' in content:
        return "EXPLORATION"
    elif '交易' in content or '商人' in content or '购买' in content:
        return "TRADE"
    elif '宝藏' in content or '财宝' in content:
        return "TREASURE"
    elif '恐怖' in content or '惊悚' in content or '害怕' in content:
        return "HORROR"
    elif '胜利' in content or '成功' in content:
        return "VICTORY"
    elif '结束' in content or '完成' in content:
        return "CHAPTER_END"
    else:
        return "NORMAL"

def convert_to_data_file(scenes, output_file, chapter_num):
    """将场景数据转换为数据文件格式"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 第{chapter_num}章数据文件\n")
        f.write("# 格式: 场景号|标题|内容|类型|是否结局\n")
        f.write("# 用 | 分隔字段，用 \\n\\n 表示段落分隔\n\n")
        
        for scene in scenes:
            # 转义内容中的换行符
            content = scene['content'].replace('\n\n', '\\n\\n')
            content = content.replace('\n', ' ')  # 单个换行符替换为空格
            
            line = f"{scene['scene']}|{scene['title']}|{content}|{scene['type']}|{str(scene['is_ending']).lower()}\n"
            f.write(line)
            f.write("\n")  # 空行分隔

def main():
    """主函数"""
    processed_dir = "../processed"
    output_dir = ".."
    
    if not os.path.exists(processed_dir):
        print(f"❌ 目录不存在: {processed_dir}")
        return
    
    # 获取所有markdown文件
    md_files = [f for f in os.listdir(processed_dir) if f.endswith('.md') and 'chapter_' in f]
    md_files.sort()
    
    print(f"📚 找到 {len(md_files)} 个章节文件")
    
    for md_file in md_files:
        # 提取章节号
        chapter_match = re.search(r'chapter_(\d+)', md_file)
        if not chapter_match:
            continue
            
        chapter_num = int(chapter_match.group(1))
        
        input_file = os.path.join(processed_dir, md_file)
        output_file = os.path.join(output_dir, f"chapter_{chapter_num}_data.txt")
        
        print(f"🔄 处理: {md_file} -> chapter_{chapter_num}_data.txt")
        
        try:
            scenes = parse_markdown_file(input_file)
            if scenes:
                convert_to_data_file(scenes, output_file, chapter_num)
                print(f"✅ 成功转换第{chapter_num}章，共{len(scenes)}个场景")
            else:
                print(f"⚠️ 第{chapter_num}章没有找到有效场景")
        except Exception as e:
            print(f"❌ 转换第{chapter_num}章失败: {e}")
    
    print("🎉 转换完成！")

if __name__ == "__main__":
    main()
