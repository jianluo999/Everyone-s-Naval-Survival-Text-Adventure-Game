#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证501-830章节数据
测试游戏功能和数据完整性
"""

import mysql.connector
import requests
import os

# 禁用代理
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

class FinalVerifier:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mgsincos30',
            'database': 'sailing_game',
            'charset': 'utf8mb4'
        }
        self.backend_url = "http://localhost:8080/api"
        
    def connect_db(self):
        """连接数据库"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return None
    
    def verify_database_integrity(self):
        """验证数据库完整性"""
        print("=== 验证数据库完整性 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 检查总体数据
            cursor.execute("SELECT COUNT(*) FROM stories")
            total_stories = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM choices")
            total_choices = cursor.fetchone()[0]
            
            # 检查501-830章节数据
            cursor.execute("""
                SELECT COUNT(*) FROM stories 
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
            """)
            new_stories = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM choices 
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
            """)
            new_choices = cursor.fetchone()[0]
            
            # 检查章节覆盖
            cursor.execute("""
                SELECT 
                    MIN(chapter) as min_chapter,
                    MAX(chapter) as max_chapter,
                    COUNT(DISTINCT chapter) as chapter_count
                FROM stories
            """)
            result = cursor.fetchone()
            min_chapter, max_chapter, chapter_count = result
            
            # 检查断裂选择
            cursor.execute("""
                SELECT COUNT(*) FROM choices c
                LEFT JOIN stories s ON c.next_story_id = s.story_id
                WHERE s.story_id IS NULL
            """)
            broken_choices = cursor.fetchone()[0]
            
            print(f"数据库完整性报告:")
            print(f"  总故事数: {total_stories}")
            print(f"  总选择数: {total_choices}")
            print(f"  501-830章节故事: {new_stories}")
            print(f"  501-830章节选择: {new_choices}")
            print(f"  章节范围: {min_chapter} - {max_chapter}")
            print(f"  章节总数: {chapter_count}")
            print(f"  断裂选择: {broken_choices}")
            
            return broken_choices < 10 and new_stories >= 2500
            
        except Exception as e:
            print(f"验证错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def test_api_functionality(self):
        """测试API功能"""
        print("\n=== 测试API功能 ===")
        
        try:
            # 测试关键故事的API
            test_stories = [
                'story_501_1',  # 第501章开始
                'story_550_1',  # 中间章节
                'story_600_1',  # 中间章节
                'story_700_1',  # 中间章节
                'story_800_1',  # 后期章节
                'story_830_5'   # 最后章节
            ]
            
            success_count = 0
            for story_id in test_stories:
                response = requests.get(f"{self.backend_url}/game/story/{story_id}", timeout=10)
                
                if response.status_code == 200:
                    story_data = response.json()
                    if story_data.get('success') and 'story' in story_data:
                        story = story_data['story']
                        content = story.get('content', '')
                        choices = story.get('choices', [])
                        
                        print(f"  ✅ {story_id}: {story.get('title', 'N/A')}")
                        print(f"    内容长度: {len(content)} 字符")
                        print(f"    选择数量: {len(choices)}")
                        print(f"    第二人称检查: {'你' in content}")
                        
                        success_count += 1
                    else:
                        print(f"  ❌ {story_id}: 数据格式错误")
                else:
                    print(f"  ❌ {story_id}: API请求失败 ({response.status_code})")
            
            print(f"\nAPI测试结果: {success_count}/{len(test_stories)} 成功")
            return success_count == len(test_stories)
            
        except Exception as e:
            print(f"API测试错误: {e}")
            return False
    
    def test_story_progression(self):
        """测试故事推进"""
        print("\n=== 测试故事推进 ===")
        
        try:
            # 测试从第500章到第501章的连接
            response = requests.get(f"{self.backend_url}/game/story/story_500_22", timeout=10)
            if response.status_code == 200:
                story_data = response.json()
                if story_data.get('success'):
                    story = story_data['story']
                    choices = story.get('choices', [])
                    
                    # 检查是否有指向501章的选择
                    has_501_connection = any(
                        choice.get('nextStoryId', '').startswith('story_501_')
                        for choice in choices
                    )
                    
                    print(f"  第500章最后场景选择数: {len(choices)}")
                    print(f"  连接到第501章: {'✅' if has_501_connection else '❌'}")
                    
                    if has_501_connection:
                        # 测试实际跳转
                        next_story_id = next(
                            choice.get('nextStoryId')
                            for choice in choices
                            if choice.get('nextStoryId', '').startswith('story_501_')
                        )
                        
                        response = requests.get(f"{self.backend_url}/game/story/{next_story_id}", timeout=10)
                        if response.status_code == 200:
                            print(f"  ✅ 成功跳转到: {next_story_id}")
                            return True
                        else:
                            print(f"  ❌ 跳转失败: {next_story_id}")
                            return False
                    else:
                        print("  ❌ 没有找到连接到501章的选择")
                        return False
            else:
                print("  ❌ 无法获取第500章数据")
                return False
                
        except Exception as e:
            print(f"故事推进测试错误: {e}")
            return False
    
    def test_content_quality(self):
        """测试内容质量"""
        print("\n=== 测试内容质量 ===")
        
        conn = self.connect_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # 随机采样检查内容质量
            cursor.execute("""
                SELECT story_id, title, content 
                FROM stories 
                WHERE story_id REGEXP '^story_(50[1-9]|5[1-9][0-9]|[6-7][0-9][0-9]|8[0-2][0-9]|830)_'
                ORDER BY RAND()
                LIMIT 10
            """)
            
            samples = cursor.fetchall()
            
            quality_issues = 0
            for story_id, title, content in samples:
                issues = []
                
                # 检查内容长度
                if len(content) < 50:
                    issues.append("内容过短")
                
                # 检查第二人称转换
                if '我' in content and '"' not in content:  # 排除对话中的"我"
                    issues.append("可能存在未转换的第一人称")
                
                # 检查标题格式
                if not title.startswith('第') or '章' not in title:
                    issues.append("标题格式异常")
                
                if issues:
                    print(f"  ⚠️ {story_id}: {', '.join(issues)}")
                    quality_issues += 1
                else:
                    print(f"  ✅ {story_id}: 质量良好")
            
            print(f"\n内容质量检查: {len(samples) - quality_issues}/{len(samples)} 通过")
            return quality_issues <= 2  # 允许少量问题
            
        except Exception as e:
            print(f"内容质量测试错误: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def run_verification(self):
        """运行完整验证"""
        print("501-830章节最终验证")
        print("=" * 50)
        
        # 1. 数据库完整性验证
        db_ok = self.verify_database_integrity()
        
        # 2. API功能测试
        api_ok = self.test_api_functionality()
        
        # 3. 故事推进测试
        progression_ok = self.test_story_progression()
        
        # 4. 内容质量测试
        quality_ok = self.test_content_quality()
        
        # 总结
        print("\n" + "=" * 50)
        print("最终验证结果:")
        print(f"  数据库完整性: {'✅ 通过' if db_ok else '❌ 失败'}")
        print(f"  API功能: {'✅ 通过' if api_ok else '❌ 失败'}")
        print(f"  故事推进: {'✅ 通过' if progression_ok else '❌ 失败'}")
        print(f"  内容质量: {'✅ 通过' if quality_ok else '❌ 失败'}")
        
        all_passed = db_ok and api_ok and progression_ok and quality_ok
        
        if all_passed:
            print("\n🎉 所有验证通过！501-830章节成功集成到游戏中！")
        else:
            print("\n⚠️ 部分验证失败，需要进一步检查")
        
        return all_passed

def main():
    verifier = FinalVerifier()
    verifier.run_verification()

if __name__ == "__main__":
    main()
