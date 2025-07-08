#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库表结构
"""

import mysql.connector

def check_tables():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'mgsincos30',
        'database': 'sailing_game',
        'charset': 'utf8mb4'
    }
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # 检查stories表结构
        print("=== Stories表结构 ===")
        cursor.execute("DESCRIBE stories")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} {row[2]} {row[3]} {row[4]} {row[5]}")
        
        # 检查choices表结构
        print("\n=== Choices表结构 ===")
        cursor.execute("DESCRIBE choices")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} {row[2]} {row[3]} {row[4]} {row[5]}")
        
        # 检查现有数据样本
        print("\n=== Stories表数据样本 ===")
        cursor.execute("SELECT story_id, title, chapter FROM stories LIMIT 3")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} (章节: {row[2]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_tables()
