# SQL生成报告

## 数据统计
- 场景数量: 5781
- 选择数量: 18093
- 场景批次: 12
- 选择批次: 37
- 批次大小: 500

## 生成文件
- create_tables.sql - 数据库表结构
- import_all_optimized_data.sql - 主导入脚本
- optimized_scenes_batch_001.sql 到 optimized_scenes_batch_012.sql
- optimized_choices_batch_001.sql 到 optimized_choices_batch_037.sql

## 导入说明
1. 首先运行 create_tables.sql 创建表结构
2. 然后运行 import_all_optimized_data.sql 导入所有数据
3. 或者手动按顺序运行各个批次文件

