#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故事人称转换脚本
将第一人称（我、我的）转换为第二人称（你、你的）
"""

import mysql.connector
import re
from typing import Dict, List, Tuple

class StoryPersonConverter:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        
        # 人称转换规则
        self.conversion_rules = [
            # 基本人称转换
            (r'\b我\b', '你'),
            (r'\b我的\b', '你的'),
            (r'\b我们\b', '你们'),
            (r'\b我们的\b', '你们的'),
            (r'\b咱\b', '你'),
            (r'\b咱们\b', '你们'),
            (r'\b本人\b', '你'),
            
            # 动词搭配调整
            (r'你是', '你是'),  # 保持不变
            (r'你有', '你有'),  # 保持不变
            (r'你在', '你在'),  # 保持不变
            (r'你会', '你会'),  # 保持不变
            (r'你能', '你能'),  # 保持不变
            (r'你要', '你要'),  # 保持不变
            (r'你想', '你想'),  # 保持不变
            (r'你看', '你看'),  # 保持不变
            (r'你听', '你听'),  # 保持不变
            (r'你感', '你感'),  # 保持不变
            (r'你觉得', '你觉得'),  # 保持不变
            (r'你认为', '你认为'),  # 保持不变
            (r'你发现', '你发现'),  # 保持不变
            (r'你注意到', '你注意到'),  # 保持不变
            (r'你意识到', '你意识到'),  # 保持不变
        ]
        
        # 特殊情况处理
        self.special_cases = [
            # 避免转换引号内的对话
            (r'"[^"]*我[^"]*"', lambda m: m.group(0)),  # 保持引号内的"我"不变
            (r'"[^"]*我的[^"]*"', lambda m: m.group(0)),  # 保持引号内的"我的"不变
        ]
        
    def connect_db(self):
        """连接数据库"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
    def convert_text(self, text: str) -> str:
        """转换文本中的人称"""
        if not text:
            return text

        converted_text = text

        # 先处理特殊情况（引号内的对话保持不变）
        protected_parts = []

        # 找到所有引号内的内容并保护
        quote_pattern = r'"[^"]*"'
        quotes = re.findall(quote_pattern, text)
        for i, quote in enumerate(quotes):
            placeholder = f"__QUOTE_{i}__"
            converted_text = converted_text.replace(quote, placeholder, 1)
            protected_parts.append((placeholder, quote))

        # 应用基本转换规则（中文环境下的正确匹配）
        basic_rules = [
            (r'我们的', '你们的'),  # 先处理复合词
            (r'我们', '你们'),
            (r'我的', '你的'),
            (r'其我', '其他'),  # 修复错误的"其我"
            (r'我(?![的们])', '你'),  # 匹配"我"但不是"我的"或"我们"
            (r'咱们', '你们'),
            (r'咱', '你'),
            (r'本人', '你'),
        ]

        for pattern, replacement in basic_rules:
            converted_text = re.sub(pattern, replacement, converted_text)

        # 恢复保护的引号内容
        for placeholder, original in protected_parts:
            converted_text = converted_text.replace(placeholder, original)

        return converted_text
    
    def preview_conversion(self, limit: int = 10) -> List[Dict]:
        """预览转换效果"""
        print(f"=== 预览转换效果 (前{limit}个故事) ===")
        
        conn = self.connect_db()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        previews = []
        
        try:
            cursor.execute("""
                SELECT story_id, title, content 
                FROM stories 
                WHERE content LIKE '%我%' OR content LIKE '%我的%' OR content LIKE '%我们%'
                LIMIT %s
            """, (limit,))
            stories = cursor.fetchall()
            
            for story in stories:
                original = story['content']
                converted = self.convert_text(original)
                
                preview = {
                    'story_id': story['story_id'],
                    'title': story['title'],
                    'original': original,
                    'converted': converted,
                    'changed': original != converted
                }
                previews.append(preview)
                
                print(f"\n故事ID: {story['story_id']}")
                print(f"标题: {story['title']}")
                print(f"原文: {original[:100]}...")
                print(f"转换: {converted[:100]}...")
                print(f"是否改变: {'是' if preview['changed'] else '否'}")
                print("-" * 50)
            
            return previews
            
        except Exception as e:
            print(f"预览错误: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def convert_batch(self, batch_size: int = 100) -> bool:
        """批量转换故事"""
        print(f"=== 开始批量转换 (批次大小: {batch_size}) ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 获取需要转换的故事总数
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM stories 
                WHERE content LIKE '%我%' OR content LIKE '%我的%' OR content LIKE '%我们%'
            """)
            total_stories = cursor.fetchone()['total']
            print(f"需要转换的故事总数: {total_stories}")
            
            converted_count = 0
            offset = 0
            
            while offset < total_stories:
                # 获取一批故事
                cursor.execute("""
                    SELECT id, story_id, content 
                    FROM stories 
                    WHERE content LIKE '%我%' OR content LIKE '%我的%' OR content LIKE '%我们%'
                    LIMIT %s OFFSET %s
                """, (batch_size, offset))
                
                stories = cursor.fetchall()
                if not stories:
                    break
                
                # 转换这批故事
                for story in stories:
                    original_content = story['content']
                    converted_content = self.convert_text(original_content)
                    
                    if original_content != converted_content:
                        # 更新数据库
                        update_cursor = conn.cursor()
                        update_cursor.execute("""
                            UPDATE stories 
                            SET content = %s 
                            WHERE id = %s
                        """, (converted_content, story['id']))
                        update_cursor.close()
                        converted_count += 1
                
                # 提交这批更改
                conn.commit()
                offset += batch_size
                
                print(f"已处理: {min(offset, total_stories)}/{total_stories} 故事")
            
            print(f"✅ 转换完成! 总共转换了 {converted_count} 个故事")
            return True
            
        except Exception as e:
            print(f"批量转换错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def verify_conversion(self, sample_size: int = 20) -> bool:
        """验证转换效果"""
        print(f"=== 验证转换效果 (采样{sample_size}个故事) ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 随机采样一些故事检查
            cursor.execute("""
                SELECT story_id, title, content 
                FROM stories 
                ORDER BY RAND()
                LIMIT %s
            """, (sample_size,))
            stories = cursor.fetchall()
            
            first_person_count = 0
            second_person_count = 0
            
            for story in stories:
                content = story['content']
                
                # 检查是否还有第一人称（排除引号内）
                # 简单检查：如果引号外还有"我"，则认为转换不完整
                content_without_quotes = re.sub(r'"[^"]*"', '', content)
                if re.search(r'\b我\b', content_without_quotes):
                    first_person_count += 1
                    print(f"⚠️  {story['story_id']}: 仍包含第一人称")
                    print(f"   内容: {content[:80]}...")
                
                # 检查第二人称
                if re.search(r'\b你\b', content):
                    second_person_count += 1
            
            print(f"\n验证结果:")
            print(f"  采样故事数: {len(stories)}")
            print(f"  仍含第一人称: {first_person_count}")
            print(f"  包含第二人称: {second_person_count}")
            print(f"  转换成功率: {(len(stories) - first_person_count) / len(stories) * 100:.1f}%")
            
            return first_person_count == 0
            
        except Exception as e:
            print(f"验证错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def run_conversion(self, preview_only: bool = False):
        """运行完整转换流程"""
        print("故事人称转换")
        print("=" * 50)
        
        # 1. 预览转换效果
        previews = self.preview_conversion(10)
        
        if preview_only:
            print("\n仅预览模式，不执行实际转换")
            return
        
        # 2. 确认转换
        print(f"\n发现 {len([p for p in previews if p['changed']])} 个故事需要转换")
        confirm = input("是否继续执行批量转换？(y/N): ")
        
        if confirm.lower() != 'y':
            print("转换已取消")
            return
        
        # 3. 执行批量转换
        if self.convert_batch():
            # 4. 验证转换效果
            self.verify_conversion()
            print("\n🎉 人称转换完成!")
        else:
            print("\n❌ 转换失败")

def main():
    converter = StoryPersonConverter()
    
    # 先预览效果
    print("选择操作模式:")
    print("1. 仅预览转换效果")
    print("2. 执行完整转换")
    
    choice = input("请选择 (1/2): ")
    
    if choice == "1":
        converter.run_conversion(preview_only=True)
    elif choice == "2":
        converter.run_conversion(preview_only=False)
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
