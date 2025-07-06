#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大规模替换故事内容脚本
直接替换DataInitializer.java中的createGameStories方法
"""

import re
from pathlib import Path

def replace_create_game_stories():
    """替换DataInitializer.java中的createGameStories方法"""
    
    # 读取批量生成的Java代码
    batch_file = Path("../batch_generated_java.txt")
    with open(batch_file, 'r', encoding='utf-8') as f:
        batch_content = f.read()
    
    # 提取故事创建部分
    story_pattern = r'// ==================== 批量生成的故事内容 ====================(.*?)// ==================== 批量生成的选择内容 ===================='
    story_match = re.search(story_pattern, batch_content, re.DOTALL)
    
    if not story_match:
        print("❌ 未找到故事内容部分")
        return False
    
    story_content = story_match.group(1).strip()
    
    # 读取DataInitializer.java
    java_file = Path("../../backend/src/main/java/com/adventure/config/DataInitializer.java")
    with open(java_file, 'r', encoding='utf-8') as f:
        java_content = f.read()
    
    # 找到createGameStories方法并替换
    method_pattern = r'(private void createGameStories\(\) \{)(.*?)(\n    \})'
    
    new_method_content = f"""private void createGameStories() {{
        System.out.println("📚 开始加载大量故事内容...");
        
{story_content}
        
        System.out.println("✅ 大量故事内容加载完成！");
    }}"""
    
    # 替换方法内容
    new_java_content = re.sub(method_pattern, new_method_content, java_content, flags=re.DOTALL)
    
    if new_java_content == java_content:
        print("❌ 未找到createGameStories方法或替换失败")
        return False
    
    # 写回文件
    with open(java_file, 'w', encoding='utf-8') as f:
        f.write(new_java_content)
    
    print("✅ createGameStories方法替换成功！")
    return True

def replace_create_game_choices():
    """替换DataInitializer.java中的createGameChoices方法"""
    
    # 读取批量生成的Java代码
    batch_file = Path("../batch_generated_java.txt")
    with open(batch_file, 'r', encoding='utf-8') as f:
        batch_content = f.read()
    
    # 提取选择创建部分
    choice_pattern = r'// ==================== 批量生成的选择内容 ====================(.*?)$'
    choice_match = re.search(choice_pattern, batch_content, re.DOTALL)
    
    if not choice_match:
        print("❌ 未找到选择内容部分")
        return False
    
    choice_content = choice_match.group(1).strip()
    
    # 读取DataInitializer.java
    java_file = Path("../../backend/src/main/java/com/adventure/config/DataInitializer.java")
    with open(java_file, 'r', encoding='utf-8') as f:
        java_content = f.read()
    
    # 找到createGameChoices方法并替换
    method_pattern = r'(private void createGameChoices\(\) \{)(.*?)(\n    \})'
    
    new_method_content = f"""private void createGameChoices() {{
        System.out.println("🎯 开始加载大量选择内容...");
        
{choice_content}
        
        System.out.println("✅ 大量选择内容加载完成！");
    }}"""
    
    # 替换方法内容
    new_java_content = re.sub(method_pattern, new_method_content, java_content, flags=re.DOTALL)
    
    if new_java_content == java_content:
        print("❌ 未找到createGameChoices方法或替换失败")
        return False
    
    # 写回文件
    with open(java_file, 'w', encoding='utf-8') as f:
        f.write(new_java_content)
    
    print("✅ createGameChoices方法替换成功！")
    return True

def main():
    print("🚀 开始大规模替换故事和选择内容...")
    
    # 替换故事内容
    if replace_create_game_stories():
        print("✅ 故事内容替换完成")
    else:
        print("❌ 故事内容替换失败")
        return
    
    # 替换选择内容
    if replace_create_game_choices():
        print("✅ 选择内容替换完成")
    else:
        print("❌ 选择内容替换失败")
        return
    
    print("🎉 大规模替换完成！现在游戏中应该有大量的故事内容了！")

if __name__ == "__main__":
    main()
