#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进选择分支脚本
为现有的游戏剧情文件生成更多样化的选择分支
"""

import os
import re
import random
from pathlib import Path

class ChoiceImprover:
    def __init__(self):
        self.choice_templates = {
            'exploration': [
                "仔细搜索周围",
                "快速查看一遍", 
                "保持警惕观察",
                "寻找隐藏线索",
                "检查可疑之处"
            ],
            'interaction': [
                "友好地交流",
                "保持谨慎态度",
                "直接询问情况",
                "先观察再决定",
                "尝试建立信任"
            ],
            'action': [
                "立即采取行动",
                "先制定计划",
                "寻求更多信息",
                "谨慎地尝试",
                "果断地执行"
            ],
            'navigation': [
                "继续向前探索",
                "改变航行方向",
                "停下来休整",
                "加快前进速度",
                "寻找安全地点"
            ],
            'resource': [
                "立即收集资源",
                "先评估风险",
                "寻找更多物品",
                "谨慎地拿取",
                "暂时观察情况"
            ],
            'communication': [
                "发送友善信息",
                "保持沉默观察",
                "询问重要信息",
                "分享自己情况",
                "寻找可靠盟友"
            ],
            'danger': [
                "准备迎战",
                "尝试逃避",
                "寻找掩护",
                "制定应对策略",
                "保持冷静应对"
            ]
        }
    
    def improve_file(self, file_path):
        """改进单个文件的选择分支"""
        print(f"🔧 改进文件: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到所有选择分支部分
        pattern = r'(### 选择分支\n\n)(.*?)(\n---)'
        
        def replace_choices(match):
            header = match.group(1)
            choices_text = match.group(2)
            footer = match.group(3)
            
            # 提取当前选择
            current_choices = re.findall(r'\d+\. (.+)', choices_text)
            
            # 检查是否是重复的通用选择
            generic_choices = ['继续前进', '停下思考', '查看状态']
            if all(choice in generic_choices for choice in current_choices):
                # 生成新的选择
                new_choices = self.generate_contextual_choices(content, match.start())
                
                # 格式化新选择
                formatted_choices = []
                for i, choice in enumerate(new_choices, 1):
                    formatted_choices.append(f"{i}. {choice}")
                
                return header + '\n'.join(formatted_choices) + '\n' + footer
            
            return match.group(0)  # 保持原样
        
        improved_content = re.sub(pattern, replace_choices, content, flags=re.DOTALL)
        
        # 保存改进后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(improved_content)
        
        print(f"✅ 完成改进: {file_path.name}")
    
    def generate_contextual_choices(self, content, position):
        """根据上下文生成选择"""
        # 获取当前场景的内容
        scene_start = content.rfind('## 场景', 0, position)
        scene_end = content.find('### 选择分支', position)
        
        if scene_start == -1 or scene_end == -1:
            return random.sample(self.choice_templates['action'], 3)
        
        scene_content = content[scene_start:scene_end].lower()
        
        # 根据场景内容选择合适的选择类型
        if any(word in scene_content for word in ['发现', '看到', '观察', '搜索']):
            return random.sample(self.choice_templates['exploration'], 3)
        elif any(word in scene_content for word in ['说话', '对话', '交流', '回应']):
            return random.sample(self.choice_templates['interaction'], 3)
        elif any(word in scene_content for word in ['船', '航行', '前进', '方向']):
            return random.sample(self.choice_templates['navigation'], 3)
        elif any(word in scene_content for word in ['物品', '装备', '拿取', '收集']):
            return random.sample(self.choice_templates['resource'], 3)
        elif any(word in scene_content for word in ['聊天', '信息', '频道', '消息']):
            return random.sample(self.choice_templates['communication'], 3)
        elif any(word in scene_content for word in ['危险', '怪物', '攻击', '战斗']):
            return random.sample(self.choice_templates['danger'], 3)
        else:
            return random.sample(self.choice_templates['action'], 3)
    
    def improve_all_files(self, processed_dir="novel_texts/processed"):
        """改进所有文件"""
        print("🚀 开始改进所有剧情文件的选择分支...")
        
        processed_path = Path(processed_dir)
        if not processed_path.exists():
            print(f"❌ 目录不存在: {processed_dir}")
            return
        
        improved_count = 0
        for file_path in processed_path.glob("*_game.md"):
            self.improve_file(file_path)
            improved_count += 1
        
        print(f"\n🎉 改进完成！共处理 {improved_count} 个文件")

def main():
    improver = ChoiceImprover()
    improver.improve_all_files()

if __name__ == "__main__":
    main()
