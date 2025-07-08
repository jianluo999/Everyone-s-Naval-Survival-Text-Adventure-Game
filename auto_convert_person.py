#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动执行故事人称转换
"""

import mysql.connector
import re

class AutoStoryPersonConverter:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        
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
    
    def convert_all_stories(self):
        """转换所有故事"""
        print("=== 开始批量转换所有故事 ===")
        
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
            
            # 获取所有需要转换的故事
            cursor.execute("""
                SELECT id, story_id, content 
                FROM stories 
                WHERE content LIKE '%我%' OR content LIKE '%我的%' OR content LIKE '%我们%'
                ORDER BY id
            """)
            
            stories = cursor.fetchall()
            converted_count = 0
            batch_size = 100
            
            for i, story in enumerate(stories):
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
                
                # 每100个故事提交一次
                if (i + 1) % batch_size == 0:
                    conn.commit()
                    print(f"已处理: {i + 1}/{len(stories)} 故事，已转换: {converted_count}")
            
            # 最终提交
            conn.commit()
            print(f"✅ 转换完成! 总共转换了 {converted_count} 个故事")
            return True
            
        except Exception as e:
            print(f"批量转换错误: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def verify_conversion(self):
        """验证转换效果"""
        print("=== 验证转换效果 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 检查是否还有第一人称
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM stories 
                WHERE content REGEXP '我(?![的们])'
            """)
            first_person_count = cursor.fetchone()['count']
            
            # 检查第二人称数量
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM stories 
                WHERE content LIKE '%你%'
            """)
            second_person_count = cursor.fetchone()['count']
            
            # 总故事数
            cursor.execute("SELECT COUNT(*) as count FROM stories")
            total_count = cursor.fetchone()['count']
            
            print(f"验证结果:")
            print(f"  总故事数: {total_count}")
            print(f"  包含第二人称的故事: {second_person_count}")
            print(f"  仍含第一人称的故事: {first_person_count}")
            print(f"  转换覆盖率: {second_person_count / total_count * 100:.1f}%")
            
            # 随机采样检查
            cursor.execute("""
                SELECT story_id, title, content 
                FROM stories 
                ORDER BY RAND()
                LIMIT 5
            """)
            samples = cursor.fetchall()
            
            print(f"\n随机采样检查:")
            for sample in samples:
                content = sample['content'][:100] + "..." if len(sample['content']) > 100 else sample['content']
                print(f"  {sample['story_id']}: {content}")
            
            return first_person_count < 100  # 允许少量第一人称（可能在引号内）
            
        except Exception as e:
            print(f"验证错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def main():
    converter = AutoStoryPersonConverter()
    
    print("自动故事人称转换")
    print("=" * 50)
    
    # 执行转换
    if converter.convert_all_stories():
        # 验证转换效果
        if converter.verify_conversion():
            print("\n🎉 人称转换完成且验证通过!")
        else:
            print("\n⚠️ 转换完成但验证发现问题")
    else:
        print("\n❌ 转换失败")

if __name__ == "__main__":
    main()
