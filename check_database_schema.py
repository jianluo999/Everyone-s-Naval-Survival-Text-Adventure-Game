#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库表结构
"""

import mysql.connector

def check_database_schema():
    """检查数据库表结构"""
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
        
        # 显示所有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("数据库中的表:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # 检查每个表的结构
        for table in tables:
            table_name = table[0]
            print(f"\n=== 表 {table_name} 的结构 ===")
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[0]} - {col[1]} - {col[2]} - {col[3]} - {col[4]} - {col[5]}")
            
            # 显示前几行数据
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            print(f"  前3行数据:")
            for row in rows:
                print(f"    {row}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_database_schema()
