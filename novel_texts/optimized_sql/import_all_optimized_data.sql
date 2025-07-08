-- 优化数据主导入脚本
-- 自动生成，用于导入所有优化后的场景和选择数据

-- 设置MySQL参数
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- 导入场景数据
SOURCE optimized_scenes_batch_001.sql;
SOURCE optimized_scenes_batch_002.sql;
SOURCE optimized_scenes_batch_003.sql;
SOURCE optimized_scenes_batch_004.sql;
SOURCE optimized_scenes_batch_005.sql;
SOURCE optimized_scenes_batch_006.sql;
SOURCE optimized_scenes_batch_007.sql;
SOURCE optimized_scenes_batch_008.sql;
SOURCE optimized_scenes_batch_009.sql;
SOURCE optimized_scenes_batch_010.sql;
SOURCE optimized_scenes_batch_011.sql;
SOURCE optimized_scenes_batch_012.sql;

-- 导入选择数据
SOURCE optimized_choices_batch_001.sql;
SOURCE optimized_choices_batch_002.sql;
SOURCE optimized_choices_batch_003.sql;
SOURCE optimized_choices_batch_004.sql;
SOURCE optimized_choices_batch_005.sql;
SOURCE optimized_choices_batch_006.sql;
SOURCE optimized_choices_batch_007.sql;
SOURCE optimized_choices_batch_008.sql;
SOURCE optimized_choices_batch_009.sql;
SOURCE optimized_choices_batch_010.sql;
SOURCE optimized_choices_batch_011.sql;
SOURCE optimized_choices_batch_012.sql;
SOURCE optimized_choices_batch_013.sql;
SOURCE optimized_choices_batch_014.sql;
SOURCE optimized_choices_batch_015.sql;
SOURCE optimized_choices_batch_016.sql;
SOURCE optimized_choices_batch_017.sql;
SOURCE optimized_choices_batch_018.sql;
SOURCE optimized_choices_batch_019.sql;
SOURCE optimized_choices_batch_020.sql;
SOURCE optimized_choices_batch_021.sql;
SOURCE optimized_choices_batch_022.sql;
SOURCE optimized_choices_batch_023.sql;
SOURCE optimized_choices_batch_024.sql;
SOURCE optimized_choices_batch_025.sql;
SOURCE optimized_choices_batch_026.sql;
SOURCE optimized_choices_batch_027.sql;
SOURCE optimized_choices_batch_028.sql;
SOURCE optimized_choices_batch_029.sql;
SOURCE optimized_choices_batch_030.sql;
SOURCE optimized_choices_batch_031.sql;
SOURCE optimized_choices_batch_032.sql;
SOURCE optimized_choices_batch_033.sql;
SOURCE optimized_choices_batch_034.sql;
SOURCE optimized_choices_batch_035.sql;
SOURCE optimized_choices_batch_036.sql;
SOURCE optimized_choices_batch_037.sql;

-- 提交事务
COMMIT;

-- 恢复MySQL参数
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
SET AUTOCOMMIT = 1;

-- 验证导入结果
SELECT COUNT(*) as total_stories FROM stories;
SELECT COUNT(*) as total_choices FROM choices;
SELECT story_type, COUNT(*) as count FROM stories GROUP BY story_type;
