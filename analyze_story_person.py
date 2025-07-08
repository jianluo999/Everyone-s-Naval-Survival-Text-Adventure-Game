#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析故事内容的人称使用情况
检查需要转换的第一人称模式
"""

import mysql.connector
import re
from collections import Counter

class StoryPersonAnalyzer:
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
    
    def analyze_first_person_patterns(self):
        """分析第一人称使用模式"""
        print("=== 分析第一人称使用模式 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 获取所有故事内容
            cursor.execute("SELECT story_id, title, content FROM stories LIMIT 100")
            stories = cursor.fetchall()
            
            # 第一人称模式
            first_person_patterns = [
                r'我',
                r'我的',
                r'我们',
                r'我们的',
                r'咱',
                r'咱们',
                r'本人'
            ]
            
            pattern_counts = Counter()
            story_examples = {}
            
            for story in stories:
                content = story['content']
                story_id = story['story_id']
                
                for pattern in first_person_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        pattern_counts[pattern] += len(matches)
                        if pattern not in story_examples:
                            story_examples[pattern] = []
                        if len(story_examples[pattern]) < 3:
                            # 找到包含该模式的句子
                            sentences = re.split(r'[。！？]', content)
                            for sentence in sentences:
                                if pattern in sentence and len(sentence.strip()) > 0:
                                    story_examples[pattern].append({
                                        'story_id': story_id,
                                        'sentence': sentence.strip()[:50] + '...' if len(sentence.strip()) > 50 else sentence.strip()
                                    })
                                    break
            
            print("第一人称使用统计:")
            for pattern, count in pattern_counts.most_common():
                print(f"  '{pattern}': {count} 次")
                if pattern in story_examples:
                    print("    示例:")
                    for example in story_examples[pattern][:2]:
                        print(f"      {example['story_id']}: {example['sentence']}")
                print()
            
        except Exception as e:
            print(f"分析错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def sample_story_content(self):
        """采样故事内容"""
        print("\n=== 故事内容采样 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # 获取几个示例故事
            cursor.execute("""
                SELECT story_id, title, content 
                FROM stories 
                WHERE story_id IN ('story_1_1', 'story_1_2', 'story_1_22', 'story_2_1')
                ORDER BY story_id
            """)
            stories = cursor.fetchall()
            
            for story in stories:
                print(f"\n故事ID: {story['story_id']}")
                print(f"标题: {story['title']}")
                print(f"内容: {story['content'][:200]}...")
                print("-" * 50)
            
        except Exception as e:
            print(f"采样错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def check_conversion_complexity(self):
        """检查转换复杂度"""
        print("\n=== 转换复杂度分析 ===")
        
        conn = self.connect_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            # 统计包含第一人称的故事数量
            cursor.execute("""
                SELECT COUNT(*) as total_stories
                FROM stories
            """)
            total_stories = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) as first_person_stories
                FROM stories
                WHERE content LIKE '%我%' OR content LIKE '%我的%' OR content LIKE '%我们%'
            """)
            first_person_stories = cursor.fetchone()[0]
            
            print(f"总故事数: {total_stories}")
            print(f"包含第一人称的故事: {first_person_stories}")
            print(f"需要转换的比例: {first_person_stories/total_stories*100:.1f}%")
            
            # 检查故事长度分布
            cursor.execute("""
                SELECT 
                    AVG(CHAR_LENGTH(content)) as avg_length,
                    MIN(CHAR_LENGTH(content)) as min_length,
                    MAX(CHAR_LENGTH(content)) as max_length
                FROM stories
            """)
            length_stats = cursor.fetchone()
            
            print(f"\n故事长度统计:")
            print(f"  平均长度: {length_stats[0]:.0f} 字符")
            print(f"  最短长度: {length_stats[1]} 字符")
            print(f"  最长长度: {length_stats[2]} 字符")
            
        except Exception as e:
            print(f"复杂度分析错误: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def run_analysis(self):
        """运行完整分析"""
        print("故事人称使用分析")
        print("=" * 50)
        
        self.sample_story_content()
        self.analyze_first_person_patterns()
        self.check_conversion_complexity()
        
        print("\n分析完成!")

def main():
    analyzer = StoryPersonAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
