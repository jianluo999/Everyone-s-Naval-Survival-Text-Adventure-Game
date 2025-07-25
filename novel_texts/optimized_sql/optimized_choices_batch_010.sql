-- 优化选择数据批次 10
-- 清理现有数据（仅第一批次）
INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES
('story_119_6', '继续前进', 'story_119_7', '', 1, 0, 0, 0, 0, 5),
('story_119_6', '停下来思考', 'story_119_8', '', 1, 0, 0, 0, 0, 4),
('story_119_6', '观察周围情况', 'story_119_9', '', 1, 0, 0, 0, 0, 6),
('story_119_7', '继续前进', 'story_119_8', '', 1, 0, 0, 0, 0, 5),
('story_119_7', '停下来思考', 'story_119_9', '', 1, 0, 0, 0, 0, 4),
('story_119_7', '观察周围情况', 'story_119_10', '', 1, 0, 0, 0, 0, 6),
('story_119_8', '继续前进', 'story_119_9', '', 1, 0, 0, 0, 0, 5),
('story_119_8', '停下来思考', 'story_119_10', '', 1, 0, 0, 0, 0, 4),
('story_119_8', '观察周围情况', 'story_120_1', '', 1, 0, 0, 0, 0, 6),
('story_119_8', '探索新的方向', 'story_119_11', '', 1, 0, 0, 0, 0, 7),
('story_119_9', '继续前进', 'story_119_10', '', 1, 0, 0, 0, 0, 5),
('story_119_9', '停下来思考', 'story_120_1', '', 1, 0, 0, 0, 0, 4),
('story_119_9', '观察周围情况', 'story_120_1', '', 1, 0, 0, 0, 0, 6),
('story_119_9', '探索新的方向', 'story_119_12', '', 1, 0, 0, 0, 0, 7),
('story_119_10', '继续前进', 'story_120_1', '', 1, 0, 0, 0, 0, 5),
('story_119_10', '停下来思考', 'story_120_1', '', 1, 0, 0, 0, 0, 4),
('story_119_10', '观察周围情况', 'story_120_1', '', 1, 0, 0, 0, 0, 6),
('story_119_10', '探索新的方向', 'story_119_12', '', 1, 0, 0, 0, 0, 7),
('story_119_11', '继续前进', 'story_120_1', '', 1, 0, 0, 0, 0, 5),
('story_119_11', '停下来思考', 'story_120_1', '', 1, 0, 0, 0, 0, 4),
('story_119_11', '观察周围情况', 'story_120_1', '', 1, 0, 0, 0, 0, 6),
('story_119_12', '继续前进', 'story_120_1', '', 1, 0, 0, 0, 0, 5),
('story_119_12', '停下来思考', 'story_120_1', '', 1, 0, 0, 0, 0, 4),
('story_119_12', '观察周围情况', 'story_120_1', '', 1, 0, 0, 0, 0, 6),
('story_120_1', '继续前进', 'story_120_2', '', 1, 0, 0, 0, 0, 5),
('story_120_1', '停下来思考', 'story_120_3', '', 1, 0, 0, 0, 0, 4),
('story_120_1', '观察周围情况', 'story_120_4', '', 1, 0, 0, 0, 0, 6),
('story_120_2', '继续前进', 'story_120_3', '', 1, 0, 0, 0, 0, 5),
('story_120_2', '停下来思考', 'story_120_4', '', 1, 0, 0, 0, 0, 4),
('story_120_2', '观察周围情况', 'story_120_5', '', 1, 0, 0, 0, 0, 6),
('story_120_3', '继续前进', 'story_120_4', '', 1, 0, 0, 0, 0, 5),
('story_120_3', '停下来思考', 'story_120_5', '', 1, 0, 0, 0, 0, 4),
('story_120_3', '观察周围情况', 'story_120_6', '', 1, 0, 0, 0, 0, 6),
('story_120_4', '继续前进', 'story_120_5', '', 1, 0, 0, 0, 0, 5),
('story_120_4', '停下来思考', 'story_120_6', '', 1, 0, 0, 0, 0, 4),
('story_120_4', '观察周围情况', 'story_120_7', '', 1, 0, 0, 0, 0, 6),
('story_120_5', '继续前进', 'story_120_6', '', 1, 0, 0, 0, 0, 5),
('story_120_5', '停下来思考', 'story_120_7', '', 1, 0, 0, 0, 0, 4),
('story_120_5', '观察周围情况', 'story_120_8', '', 1, 0, 0, 0, 0, 6),
('story_120_6', '继续前进', 'story_120_7', '', 1, 0, 0, 0, 0, 5),
('story_120_6', '停下来思考', 'story_120_8', '', 1, 0, 0, 0, 0, 4),
('story_120_6', '观察周围情况', 'story_120_9', '', 1, 0, 0, 0, 0, 6),
('story_120_7', '继续前进', 'story_120_8', '', 1, 0, 0, 0, 0, 5),
('story_120_7', '停下来思考', 'story_120_9', '', 1, 0, 0, 0, 0, 4),
('story_120_7', '观察周围情况', 'story_120_10', '', 1, 0, 0, 0, 0, 6),
('story_120_8', '继续前进', 'story_120_9', '', 1, 0, 0, 0, 0, 5),
('story_120_8', '停下来思考', 'story_120_10', '', 1, 0, 0, 0, 0, 4),
('story_120_8', '观察周围情况', 'story_121_1', '', 1, 0, 0, 0, 0, 6),
('story_120_8', '探索新的方向', 'story_120_11', '', 1, 0, 0, 0, 0, 7),
('story_120_9', '继续前进', 'story_120_10', '', 1, 0, 0, 0, 0, 5),
('story_120_9', '停下来思考', 'story_121_1', '', 1, 0, 0, 0, 0, 4),
('story_120_9', '观察周围情况', 'story_121_1', '', 1, 0, 0, 0, 0, 6),
('story_120_9', '探索新的方向', 'story_120_12', '', 1, 0, 0, 0, 0, 7),
('story_120_10', '继续前进', 'story_121_1', '', 1, 0, 0, 0, 0, 5),
('story_120_10', '停下来思考', 'story_121_1', '', 1, 0, 0, 0, 0, 4),
('story_120_10', '观察周围情况', 'story_121_1', '', 1, 0, 0, 0, 0, 6),
('story_120_10', '探索新的方向', 'story_120_12', '', 1, 0, 0, 0, 0, 7),
('story_120_11', '继续前进', 'story_121_1', '', 1, 0, 0, 0, 0, 5),
('story_120_11', '停下来思考', 'story_121_1', '', 1, 0, 0, 0, 0, 4),
('story_120_11', '观察周围情况', 'story_121_1', '', 1, 0, 0, 0, 0, 6),
('story_120_12', '继续前进', 'story_121_1', '', 1, 0, 0, 0, 0, 5),
('story_120_12', '停下来思考', 'story_121_1', '', 1, 0, 0, 0, 0, 4),
('story_120_12', '观察周围情况', 'story_121_1', '', 1, 0, 0, 0, 0, 6),
('story_121_1', '继续前进', 'story_121_2', '', 1, 0, 0, 0, 0, 5),
('story_121_1', '停下来思考', 'story_121_3', '', 1, 0, 0, 0, 0, 4),
('story_121_1', '观察周围情况', 'story_121_4', '', 1, 0, 0, 0, 0, 6),
('story_121_1', '探索新的方向', 'story_122_12', '', 1, 0, 0, 0, 0, 7),
('story_121_2', '继续前进', 'story_121_3', '', 1, 0, 0, 0, 0, 5),
('story_121_2', '停下来思考', 'story_121_4', '', 1, 0, 0, 0, 0, 4),
('story_121_2', '观察周围情况', 'story_121_5', '', 1, 0, 0, 0, 0, 6),
('story_121_2', '探索新的方向', 'story_122_12', '', 1, 0, 0, 0, 0, 7),
('story_121_3', '继续前进', 'story_121_4', '', 1, 0, 0, 0, 0, 5),
('story_121_3', '停下来思考', 'story_121_5', '', 1, 0, 0, 0, 0, 4),
('story_121_3', '观察周围情况', 'story_121_6', '', 1, 0, 0, 0, 0, 6),
('story_121_4', '继续前进', 'story_121_5', '', 1, 0, 0, 0, 0, 5),
('story_121_4', '停下来思考', 'story_121_6', '', 1, 0, 0, 0, 0, 4),
('story_121_4', '观察周围情况', 'story_121_7', '', 1, 0, 0, 0, 0, 6),
('story_121_5', '检查获得的物品', 'story_121_6', '', 1, 0, 0, 0, 0, 7),
('story_121_5', '继续探索', 'story_121_7', '', 1, 0, 0, 0, 0, 5),
('story_121_6', '继续前进', 'story_121_7', '', 1, 0, 0, 0, 0, 5),
('story_121_6', '停下来思考', 'story_121_8', '', 1, 0, 0, 0, 0, 4),
('story_121_6', '观察周围情况', 'story_121_9', '', 1, 0, 0, 0, 0, 6),
('story_121_7', '继续前进', 'story_121_8', '', 1, 0, 0, 0, 0, 5),
('story_121_7', '停下来思考', 'story_121_9', '', 1, 0, 0, 0, 0, 4),
('story_121_7', '观察周围情况', 'story_121_10', '', 1, 0, 0, 0, 0, 6),
('story_121_8', '继续前进', 'story_121_9', '', 1, 0, 0, 0, 0, 5),
('story_121_8', '停下来思考', 'story_121_10', '', 1, 0, 0, 0, 0, 4),
('story_121_8', '观察周围情况', 'story_122_1', '', 1, 0, 0, 0, 0, 6),
('story_121_8', '探索新的方向', 'story_121_11', '', 1, 0, 0, 0, 0, 7),
('story_121_9', '继续前进', 'story_121_10', '', 1, 0, 0, 0, 0, 5),
('story_121_9', '停下来思考', 'story_122_1', '', 1, 0, 0, 0, 0, 4),
('story_121_9', '观察周围情况', 'story_122_1', '', 1, 0, 0, 0, 0, 6),
('story_121_9', '探索新的方向', 'story_121_11', '', 1, 0, 0, 0, 0, 7),
('story_121_10', '继续前进', 'story_122_1', '', 1, 0, 0, 0, 0, 5),
('story_121_10', '停下来思考', 'story_122_1', '', 1, 0, 0, 0, 0, 4),
('story_121_10', '观察周围情况', 'story_122_1', '', 1, 0, 0, 0, 0, 6),
('story_121_11', '继续前进', 'story_122_1', '', 1, 0, 0, 0, 0, 5),
('story_121_11', '停下来思考', 'story_122_1', '', 1, 0, 0, 0, 0, 4),
('story_121_11', '观察周围情况', 'story_122_1', '', 1, 0, 0, 0, 0, 6),
('story_122_1', '继续前进', 'story_122_2', '', 1, 0, 0, 0, 0, 5),
('story_122_1', '停下来思考', 'story_122_3', '', 1, 0, 0, 0, 0, 4),
('story_122_1', '观察周围情况', 'story_122_4', '', 1, 0, 0, 0, 0, 6),
('story_122_2', '继续前进', 'story_122_3', '', 1, 0, 0, 0, 0, 5),
('story_122_2', '停下来思考', 'story_122_4', '', 1, 0, 0, 0, 0, 4),
('story_122_2', '观察周围情况', 'story_122_5', '', 1, 0, 0, 0, 0, 6),
('story_122_3', '继续前进', 'story_122_4', '', 1, 0, 0, 0, 0, 5),
('story_122_3', '停下来思考', 'story_122_5', '', 1, 0, 0, 0, 0, 4),
('story_122_3', '观察周围情况', 'story_122_6', '', 1, 0, 0, 0, 0, 6),
('story_122_4', '继续前进', 'story_122_5', '', 1, 0, 0, 0, 0, 5),
('story_122_4', '停下来思考', 'story_122_6', '', 1, 0, 0, 0, 0, 4),
('story_122_4', '观察周围情况', 'story_122_7', '', 1, 0, 0, 0, 0, 6),
('story_122_5', '继续前进', 'story_122_6', '', 1, 0, 0, 0, 0, 5),
('story_122_5', '停下来思考', 'story_122_7', '', 1, 0, 0, 0, 0, 4),
('story_122_5', '观察周围情况', 'story_122_8', '', 1, 0, 0, 0, 0, 6),
('story_122_6', '继续前进', 'story_122_7', '', 1, 0, 0, 0, 0, 5),
('story_122_6', '停下来思考', 'story_122_8', '', 1, 0, 0, 0, 0, 4),
('story_122_6', '观察周围情况', 'story_122_9', '', 1, 0, 0, 0, 0, 6),
('story_122_7', '继续前进', 'story_122_8', '', 1, 0, 0, 0, 0, 5),
('story_122_7', '停下来思考', 'story_122_9', '', 1, 0, 0, 0, 0, 4),
('story_122_7', '观察周围情况', 'story_122_10', '', 1, 0, 0, 0, 0, 6),
('story_122_8', '继续前进', 'story_122_9', '', 1, 0, 0, 0, 0, 5),
('story_122_8', '停下来思考', 'story_122_10', '', 1, 0, 0, 0, 0, 4),
('story_122_8', '观察周围情况', 'story_123_1', '', 1, 0, 0, 0, 0, 6),
('story_122_8', '探索新的方向', 'story_122_11', '', 1, 0, 0, 0, 0, 7),
('story_122_9', '继续前进', 'story_122_10', '', 1, 0, 0, 0, 0, 5),
('story_122_9', '停下来思考', 'story_123_1', '', 1, 0, 0, 0, 0, 4),
('story_122_9', '观察周围情况', 'story_123_1', '', 1, 0, 0, 0, 0, 6),
('story_122_9', '探索新的方向', 'story_122_11', '', 1, 0, 0, 0, 0, 7),
('story_122_10', '继续前进', 'story_123_1', '', 1, 0, 0, 0, 0, 5),
('story_122_10', '停下来思考', 'story_123_1', '', 1, 0, 0, 0, 0, 4),
('story_122_10', '观察周围情况', 'story_123_1', '', 1, 0, 0, 0, 0, 6),
('story_122_10', '探索新的方向', 'story_122_13', '', 1, 0, 0, 0, 0, 7),
('story_122_11', '继续前进', 'story_123_1', '', 1, 0, 0, 0, 0, 5),
('story_122_11', '停下来思考', 'story_123_1', '', 1, 0, 0, 0, 0, 4),
('story_122_11', '观察周围情况', 'story_123_1', '', 1, 0, 0, 0, 0, 6),
('story_122_11', '探索新的方向', 'story_122_13', '', 1, 0, 0, 0, 0, 7),
('story_122_12', '继续前进', 'story_123_1', '', 1, 0, 0, 0, 0, 5),
('story_122_12', '停下来思考', 'story_123_1', '', 1, 0, 0, 0, 0, 4),
('story_122_12', '观察周围情况', 'story_123_1', '', 1, 0, 0, 0, 0, 6),
('story_122_13', '继续前进', 'story_123_1', '', 1, 0, 0, 0, 0, 5),
('story_122_13', '停下来思考', 'story_123_1', '', 1, 0, 0, 0, 0, 4),
('story_122_13', '观察周围情况', 'story_123_1', '', 1, 0, 0, 0, 0, 6),
('story_123_1', '继续前进', 'story_123_2', '', 1, 0, 0, 0, 0, 5),
('story_123_1', '停下来思考', 'story_123_3', '', 1, 0, 0, 0, 0, 4),
('story_123_1', '观察周围情况', 'story_123_4', '', 1, 0, 0, 0, 0, 6),
('story_123_2', '继续前进', 'story_123_3', '', 1, 0, 0, 0, 0, 5),
('story_123_2', '停下来思考', 'story_123_4', '', 1, 0, 0, 0, 0, 4),
('story_123_2', '观察周围情况', 'story_123_5', '', 1, 0, 0, 0, 0, 6),
('story_123_3', '继续前进', 'story_123_4', '', 1, 0, 0, 0, 0, 5),
('story_123_3', '停下来思考', 'story_123_5', '', 1, 0, 0, 0, 0, 4),
('story_123_3', '观察周围情况', 'story_123_6', '', 1, 0, 0, 0, 0, 6),
('story_123_4', '继续前进', 'story_123_5', '', 1, 0, 0, 0, 0, 5),
('story_123_4', '停下来思考', 'story_123_6', '', 1, 0, 0, 0, 0, 4),
('story_123_4', '观察周围情况', 'story_123_7', '', 1, 0, 0, 0, 0, 6),
('story_123_5', '继续前进', 'story_123_6', '', 1, 0, 0, 0, 0, 5),
('story_123_5', '停下来思考', 'story_123_7', '', 1, 0, 0, 0, 0, 4),
('story_123_5', '观察周围情况', 'story_123_8', '', 1, 0, 0, 0, 0, 6),
('story_123_6', '继续前进', 'story_123_7', '', 1, 0, 0, 0, 0, 5),
('story_123_6', '停下来思考', 'story_123_8', '', 1, 0, 0, 0, 0, 4),
('story_123_6', '观察周围情况', 'story_123_9', '', 1, 0, 0, 0, 0, 6),
('story_123_7', '继续前进', 'story_123_8', '', 1, 0, 0, 0, 0, 5),
('story_123_7', '停下来思考', 'story_123_9', '', 1, 0, 0, 0, 0, 4),
('story_123_7', '观察周围情况', 'story_123_10', '', 1, 0, 0, 0, 0, 6),
('story_123_8', '继续前进', 'story_123_9', '', 1, 0, 0, 0, 0, 5),
('story_123_8', '停下来思考', 'story_123_10', '', 1, 0, 0, 0, 0, 4),
('story_123_8', '观察周围情况', 'story_124_1', '', 1, 0, 0, 0, 0, 6),
('story_123_9', '继续前进', 'story_123_10', '', 1, 0, 0, 0, 0, 5),
('story_123_9', '停下来思考', 'story_124_1', '', 1, 0, 0, 0, 0, 4),
('story_123_9', '观察周围情况', 'story_124_1', '', 1, 0, 0, 0, 0, 6),
('story_123_10', '继续前进', 'story_124_1', '', 1, 0, 0, 0, 0, 5),
('story_123_10', '停下来思考', 'story_124_1', '', 1, 0, 0, 0, 0, 4),
('story_123_10', '观察周围情况', 'story_124_1', '', 1, 0, 0, 0, 0, 6),
('story_124_1', '继续前进', 'story_124_2', '', 1, 0, 0, 0, 0, 5),
('story_124_1', '停下来思考', 'story_124_3', '', 1, 0, 0, 0, 0, 4),
('story_124_1', '观察周围情况', 'story_124_4', '', 1, 0, 0, 0, 0, 6),
('story_124_2', '继续前进', 'story_124_3', '', 1, 0, 0, 0, 0, 5),
('story_124_2', '停下来思考', 'story_124_4', '', 1, 0, 0, 0, 0, 4),
('story_124_2', '观察周围情况', 'story_124_5', '', 1, 0, 0, 0, 0, 6),
('story_124_3', '继续前进', 'story_124_4', '', 1, 0, 0, 0, 0, 5),
('story_124_3', '停下来思考', 'story_124_5', '', 1, 0, 0, 0, 0, 4),
('story_124_3', '观察周围情况', 'story_124_6', '', 1, 0, 0, 0, 0, 6),
('story_124_4', '继续前进', 'story_124_5', '', 1, 0, 0, 0, 0, 5),
('story_124_4', '停下来思考', 'story_124_6', '', 1, 0, 0, 0, 0, 4),
('story_124_4', '观察周围情况', 'story_124_7', '', 1, 0, 0, 0, 0, 6),
('story_124_5', '继续前进', 'story_124_6', '', 1, 0, 0, 0, 0, 5),
('story_124_5', '停下来思考', 'story_124_7', '', 1, 0, 0, 0, 0, 4),
('story_124_5', '观察周围情况', 'story_124_8', '', 1, 0, 0, 0, 0, 6),
('story_124_6', '继续前进', 'story_124_7', '', 1, 0, 0, 0, 0, 5),
('story_124_6', '停下来思考', 'story_124_8', '', 1, 0, 0, 0, 0, 4),
('story_124_6', '观察周围情况', 'story_124_9', '', 1, 0, 0, 0, 0, 6),
('story_124_7', '检查获得的物品', 'story_124_8', '', 1, 0, 0, 0, 0, 7),
('story_124_7', '继续探索', 'story_124_9', '', 1, 0, 0, 0, 0, 5),
('story_124_8', '继续前进', 'story_124_9', '', 1, 0, 0, 0, 0, 5),
('story_124_8', '停下来思考', 'story_124_10', '', 1, 0, 0, 0, 0, 4),
('story_124_8', '观察周围情况', 'story_125_1', '', 1, 0, 0, 0, 0, 6),
('story_124_9', '继续前进', 'story_124_10', '', 1, 0, 0, 0, 0, 5),
('story_124_9', '停下来思考', 'story_125_1', '', 1, 0, 0, 0, 0, 4),
('story_124_9', '观察周围情况', 'story_125_1', '', 1, 0, 0, 0, 0, 6),
('story_125_1', '继续前进', 'story_125_2', '', 1, 0, 0, 0, 0, 5),
('story_125_1', '停下来思考', 'story_125_3', '', 1, 0, 0, 0, 0, 4),
('story_125_1', '观察周围情况', 'story_125_4', '', 1, 0, 0, 0, 0, 6),
('story_125_2', '继续前进', 'story_125_3', '', 1, 0, 0, 0, 0, 5),
('story_125_2', '停下来思考', 'story_125_4', '', 1, 0, 0, 0, 0, 4),
('story_125_2', '观察周围情况', 'story_125_5', '', 1, 0, 0, 0, 0, 6),
('story_125_3', '继续前进', 'story_125_4', '', 1, 0, 0, 0, 0, 5),
('story_125_3', '停下来思考', 'story_125_5', '', 1, 0, 0, 0, 0, 4),
('story_125_3', '观察周围情况', 'story_125_6', '', 1, 0, 0, 0, 0, 6),
('story_125_4', '继续前进', 'story_125_5', '', 1, 0, 0, 0, 0, 5),
('story_125_4', '停下来思考', 'story_125_6', '', 1, 0, 0, 0, 0, 4),
('story_125_4', '观察周围情况', 'story_125_7', '', 1, 0, 0, 0, 0, 6),
('story_125_5', '继续前进', 'story_125_6', '', 1, 0, 0, 0, 0, 5),
('story_125_5', '停下来思考', 'story_125_7', '', 1, 0, 0, 0, 0, 4),
('story_125_5', '观察周围情况', 'story_125_8', '', 1, 0, 0, 0, 0, 6),
('story_125_6', '继续前进', 'story_125_7', '', 1, 0, 0, 0, 0, 5),
('story_125_6', '停下来思考', 'story_125_8', '', 1, 0, 0, 0, 0, 4),
('story_125_6', '观察周围情况', 'story_125_9', '', 1, 0, 0, 0, 0, 6),
('story_125_7', '继续前进', 'story_125_8', '', 1, 0, 0, 0, 0, 5),
('story_125_7', '停下来思考', 'story_125_9', '', 1, 0, 0, 0, 0, 4),
('story_125_7', '观察周围情况', 'story_125_10', '', 1, 0, 0, 0, 0, 6),
('story_125_8', '继续前进', 'story_125_9', '', 1, 0, 0, 0, 0, 5),
('story_125_8', '停下来思考', 'story_125_10', '', 1, 0, 0, 0, 0, 4),
('story_125_8', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_125_8', '探索新的方向', 'story_125_11', '', 1, 0, 0, 0, 0, 7),
('story_125_9', '继续前进', 'story_125_10', '', 1, 0, 0, 0, 0, 5),
('story_125_9', '停下来思考', 'story_126_1', '', 1, 0, 0, 0, 0, 4),
('story_125_9', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_125_9', '探索新的方向', 'story_125_12', '', 1, 0, 0, 0, 0, 7),
('story_125_10', '继续前进', 'story_126_1', '', 1, 0, 0, 0, 0, 5),
('story_125_10', '停下来思考', 'story_126_1', '', 1, 0, 0, 0, 0, 4),
('story_125_10', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_125_10', '探索新的方向', 'story_125_13', '', 1, 0, 0, 0, 0, 7),
('story_125_11', '继续前进', 'story_126_1', '', 1, 0, 0, 0, 0, 5),
('story_125_11', '停下来思考', 'story_126_1', '', 1, 0, 0, 0, 0, 4),
('story_125_11', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_125_11', '探索新的方向', 'story_125_14', '', 1, 0, 0, 0, 0, 7),
('story_125_12', '继续前进', 'story_126_1', '', 1, 0, 0, 0, 0, 5),
('story_125_12', '停下来思考', 'story_126_1', '', 1, 0, 0, 0, 0, 4),
('story_125_12', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_125_12', '探索新的方向', 'story_125_14', '', 1, 0, 0, 0, 0, 7),
('story_125_13', '继续前进', 'story_126_1', '', 1, 0, 0, 0, 0, 5),
('story_125_13', '停下来思考', 'story_126_1', '', 1, 0, 0, 0, 0, 4),
('story_125_13', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_125_13', '探索新的方向', 'story_125_15', '', 1, 0, 0, 0, 0, 7),
('story_125_14', '继续前进', 'story_126_1', '', 1, 0, 0, 0, 0, 5),
('story_125_14', '停下来思考', 'story_126_1', '', 1, 0, 0, 0, 0, 4),
('story_125_14', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_125_14', '探索新的方向', 'story_125_15', '', 1, 0, 0, 0, 0, 7),
('story_125_15', '继续前进', 'story_126_1', '', 1, 0, 0, 0, 0, 5),
('story_125_15', '停下来思考', 'story_126_1', '', 1, 0, 0, 0, 0, 4),
('story_125_15', '观察周围情况', 'story_126_1', '', 1, 0, 0, 0, 0, 6),
('story_126_1', '继续前进', 'story_126_2', '', 1, 0, 0, 0, 0, 5),
('story_126_1', '停下来思考', 'story_126_3', '', 1, 0, 0, 0, 0, 4),
('story_126_1', '观察周围情况', 'story_126_4', '', 1, 0, 0, 0, 0, 6),
('story_126_2', '继续前进', 'story_126_3', '', 1, 0, 0, 0, 0, 5),
('story_126_2', '停下来思考', 'story_126_4', '', 1, 0, 0, 0, 0, 4),
('story_126_2', '观察周围情况', 'story_126_5', '', 1, 0, 0, 0, 0, 6),
('story_126_3', '继续前进', 'story_126_4', '', 1, 0, 0, 0, 0, 5),
('story_126_3', '停下来思考', 'story_126_5', '', 1, 0, 0, 0, 0, 4),
('story_126_3', '观察周围情况', 'story_126_6', '', 1, 0, 0, 0, 0, 6),
('story_126_4', '继续前进', 'story_126_5', '', 1, 0, 0, 0, 0, 5),
('story_126_4', '停下来思考', 'story_126_6', '', 1, 0, 0, 0, 0, 4),
('story_126_4', '观察周围情况', 'story_126_7', '', 1, 0, 0, 0, 0, 6),
('story_126_5', '与其他人交流', 'story_126_6', '', 1, 0, 0, 0, 0, 6),
('story_126_5', '继续探索', 'story_126_7', '', 1, 0, 0, 0, 0, 5),
('story_126_6', '继续前进', 'story_126_7', '', 1, 0, 0, 0, 0, 5),
('story_126_6', '停下来思考', 'story_126_8', '', 1, 0, 0, 0, 0, 4),
('story_126_6', '观察周围情况', 'story_126_9', '', 1, 0, 0, 0, 0, 6),
('story_126_7', '继续前进', 'story_126_8', '', 1, 0, 0, 0, 0, 5),
('story_126_7', '停下来思考', 'story_126_9', '', 1, 0, 0, 0, 0, 4),
('story_126_7', '观察周围情况', 'story_126_10', '', 1, 0, 0, 0, 0, 6),
('story_126_8', '继续前进', 'story_126_9', '', 1, 0, 0, 0, 0, 5),
('story_126_8', '停下来思考', 'story_126_10', '', 1, 0, 0, 0, 0, 4),
('story_126_8', '观察周围情况', 'story_127_1', '', 1, 0, 0, 0, 0, 6),
('story_126_8', '探索新的方向', 'story_126_11', '', 1, 0, 0, 0, 0, 7),
('story_126_9', '继续前进', 'story_126_10', '', 1, 0, 0, 0, 0, 5),
('story_126_9', '停下来思考', 'story_127_1', '', 1, 0, 0, 0, 0, 4),
('story_126_9', '观察周围情况', 'story_127_1', '', 1, 0, 0, 0, 0, 6),
('story_126_9', '探索新的方向', 'story_126_11', '', 1, 0, 0, 0, 0, 7),
('story_126_10', '检查获得的物品', 'story_127_1', '', 1, 0, 0, 0, 0, 7),
('story_126_10', '继续探索', 'story_127_1', '', 1, 0, 0, 0, 0, 5),
('story_126_11', '继续前进', 'story_127_1', '', 1, 0, 0, 0, 0, 5),
('story_126_11', '停下来思考', 'story_127_1', '', 1, 0, 0, 0, 0, 4),
('story_126_11', '观察周围情况', 'story_127_1', '', 1, 0, 0, 0, 0, 6),
('story_127_1', '继续前进', 'story_127_2', '', 1, 0, 0, 0, 0, 5),
('story_127_1', '停下来思考', 'story_127_3', '', 1, 0, 0, 0, 0, 4),
('story_127_1', '观察周围情况', 'story_127_4', '', 1, 0, 0, 0, 0, 6),
('story_127_2', '继续前进', 'story_127_3', '', 1, 0, 0, 0, 0, 5),
('story_127_2', '停下来思考', 'story_127_4', '', 1, 0, 0, 0, 0, 4),
('story_127_2', '观察周围情况', 'story_127_5', '', 1, 0, 0, 0, 0, 6),
('story_127_3', '继续前进', 'story_127_4', '', 1, 0, 0, 0, 0, 5),
('story_127_3', '停下来思考', 'story_127_5', '', 1, 0, 0, 0, 0, 4),
('story_127_3', '观察周围情况', 'story_127_6', '', 1, 0, 0, 0, 0, 6),
('story_127_4', '继续前进', 'story_127_5', '', 1, 0, 0, 0, 0, 5),
('story_127_4', '停下来思考', 'story_127_6', '', 1, 0, 0, 0, 0, 4),
('story_127_4', '观察周围情况', 'story_127_7', '', 1, 0, 0, 0, 0, 6),
('story_127_5', '与其他人交流', 'story_127_6', '', 1, 0, 0, 0, 0, 6),
('story_127_5', '继续探索', 'story_127_7', '', 1, 0, 0, 0, 0, 5),
('story_127_6', '继续前进', 'story_127_7', '', 1, 0, 0, 0, 0, 5),
('story_127_6', '停下来思考', 'story_127_8', '', 1, 0, 0, 0, 0, 4),
('story_127_6', '观察周围情况', 'story_127_9', '', 1, 0, 0, 0, 0, 6),
('story_127_7', '继续前进', 'story_127_8', '', 1, 0, 0, 0, 0, 5),
('story_127_7', '停下来思考', 'story_127_9', '', 1, 0, 0, 0, 0, 4),
('story_127_7', '观察周围情况', 'story_127_10', '', 1, 0, 0, 0, 0, 6),
('story_127_8', '继续前进', 'story_127_9', '', 1, 0, 0, 0, 0, 5),
('story_127_8', '停下来思考', 'story_127_10', '', 1, 0, 0, 0, 0, 4),
('story_127_8', '观察周围情况', 'story_128_1', '', 1, 0, 0, 0, 0, 6),
('story_127_8', '探索新的方向', 'story_127_11', '', 1, 0, 0, 0, 0, 7),
('story_127_9', '继续前进', 'story_127_10', '', 1, 0, 0, 0, 0, 5),
('story_127_9', '停下来思考', 'story_128_1', '', 1, 0, 0, 0, 0, 4),
('story_127_9', '观察周围情况', 'story_128_1', '', 1, 0, 0, 0, 0, 6),
('story_127_9', '探索新的方向', 'story_127_11', '', 1, 0, 0, 0, 0, 7),
('story_127_10', '继续前进', 'story_128_1', '', 1, 0, 0, 0, 0, 5),
('story_127_10', '停下来思考', 'story_128_1', '', 1, 0, 0, 0, 0, 4),
('story_127_10', '观察周围情况', 'story_128_1', '', 1, 0, 0, 0, 0, 6),
('story_127_10', '探索新的方向', 'story_127_12', '', 1, 0, 0, 0, 0, 7),
('story_127_11', '继续前进', 'story_128_1', '', 1, 0, 0, 0, 0, 5),
('story_127_11', '停下来思考', 'story_128_1', '', 1, 0, 0, 0, 0, 4),
('story_127_11', '观察周围情况', 'story_128_1', '', 1, 0, 0, 0, 0, 6),
('story_127_11', '探索新的方向', 'story_127_12', '', 1, 0, 0, 0, 0, 7),
('story_127_12', '继续前进', 'story_128_1', '', 1, 0, 0, 0, 0, 5),
('story_127_12', '停下来思考', 'story_128_1', '', 1, 0, 0, 0, 0, 4),
('story_127_12', '观察周围情况', 'story_128_1', '', 1, 0, 0, 0, 0, 6),
('story_128_1', '继续前进', 'story_128_2', '', 1, 0, 0, 0, 0, 5),
('story_128_1', '停下来思考', 'story_128_3', '', 1, 0, 0, 0, 0, 4),
('story_128_1', '观察周围情况', 'story_128_4', '', 1, 0, 0, 0, 0, 6),
('story_128_2', '继续前进', 'story_128_3', '', 1, 0, 0, 0, 0, 5),
('story_128_2', '停下来思考', 'story_128_4', '', 1, 0, 0, 0, 0, 4),
('story_128_2', '观察周围情况', 'story_128_5', '', 1, 0, 0, 0, 0, 6),
('story_128_3', '继续前进', 'story_128_4', '', 1, 0, 0, 0, 0, 5),
('story_128_3', '停下来思考', 'story_128_5', '', 1, 0, 0, 0, 0, 4),
('story_128_3', '观察周围情况', 'story_128_6', '', 1, 0, 0, 0, 0, 6),
('story_128_4', '继续前进', 'story_128_5', '', 1, 0, 0, 0, 0, 5),
('story_128_4', '停下来思考', 'story_128_6', '', 1, 0, 0, 0, 0, 4),
('story_128_4', '观察周围情况', 'story_128_7', '', 1, 0, 0, 0, 0, 6),
('story_128_5', '继续前进', 'story_128_6', '', 1, 0, 0, 0, 0, 5),
('story_128_5', '停下来思考', 'story_128_7', '', 1, 0, 0, 0, 0, 4),
('story_128_5', '观察周围情况', 'story_128_8', '', 1, 0, 0, 0, 0, 6),
('story_128_6', '继续前进', 'story_128_7', '', 1, 0, 0, 0, 0, 5),
('story_128_6', '停下来思考', 'story_128_8', '', 1, 0, 0, 0, 0, 4),
('story_128_6', '观察周围情况', 'story_128_9', '', 1, 0, 0, 0, 0, 6),
('story_128_7', '继续前进', 'story_128_8', '', 1, 0, 0, 0, 0, 5),
('story_128_7', '停下来思考', 'story_128_9', '', 1, 0, 0, 0, 0, 4),
('story_128_7', '观察周围情况', 'story_128_10', '', 1, 0, 0, 0, 0, 6),
('story_128_8', '继续前进', 'story_128_9', '', 1, 0, 0, 0, 0, 5),
('story_128_8', '停下来思考', 'story_128_10', '', 1, 0, 0, 0, 0, 4),
('story_128_8', '观察周围情况', 'story_129_1', '', 1, 0, 0, 0, 0, 6),
('story_128_8', '探索新的方向', 'story_128_11', '', 1, 0, 0, 0, 0, 7),
('story_128_9', '继续前进', 'story_128_10', '', 1, 0, 0, 0, 0, 5),
('story_128_9', '停下来思考', 'story_129_1', '', 1, 0, 0, 0, 0, 4),
('story_128_9', '观察周围情况', 'story_129_1', '', 1, 0, 0, 0, 0, 6),
('story_128_9', '探索新的方向', 'story_128_11', '', 1, 0, 0, 0, 0, 7),
('story_128_10', '继续前进', 'story_129_1', '', 1, 0, 0, 0, 0, 5),
('story_128_10', '停下来思考', 'story_129_1', '', 1, 0, 0, 0, 0, 4),
('story_128_10', '观察周围情况', 'story_129_1', '', 1, 0, 0, 0, 0, 6),
('story_128_10', '探索新的方向', 'story_128_12', '', 1, 0, 0, 0, 0, 7),
('story_128_11', '继续前进', 'story_129_1', '', 1, 0, 0, 0, 0, 5),
('story_128_11', '停下来思考', 'story_129_1', '', 1, 0, 0, 0, 0, 4),
('story_128_11', '观察周围情况', 'story_129_1', '', 1, 0, 0, 0, 0, 6),
('story_128_11', '探索新的方向', 'story_128_12', '', 1, 0, 0, 0, 0, 7),
('story_128_12', '继续前进', 'story_129_1', '', 1, 0, 0, 0, 0, 5),
('story_128_12', '停下来思考', 'story_129_1', '', 1, 0, 0, 0, 0, 4),
('story_128_12', '观察周围情况', 'story_129_1', '', 1, 0, 0, 0, 0, 6),
('story_129_1', '继续前进', 'story_129_2', '', 1, 0, 0, 0, 0, 5),
('story_129_1', '停下来思考', 'story_129_3', '', 1, 0, 0, 0, 0, 4),
('story_129_1', '观察周围情况', 'story_129_4', '', 1, 0, 0, 0, 0, 6),
('story_129_2', '继续前进', 'story_129_3', '', 1, 0, 0, 0, 0, 5),
('story_129_2', '停下来思考', 'story_129_4', '', 1, 0, 0, 0, 0, 4),
('story_129_2', '观察周围情况', 'story_129_5', '', 1, 0, 0, 0, 0, 6),
('story_129_3', '继续前进', 'story_129_4', '', 1, 0, 0, 0, 0, 5),
('story_129_3', '停下来思考', 'story_129_5', '', 1, 0, 0, 0, 0, 4),
('story_129_3', '观察周围情况', 'story_129_6', '', 1, 0, 0, 0, 0, 6),
('story_129_4', '继续前进', 'story_129_5', '', 1, 0, 0, 0, 0, 5),
('story_129_4', '停下来思考', 'story_129_6', '', 1, 0, 0, 0, 0, 4),
('story_129_4', '观察周围情况', 'story_129_7', '', 1, 0, 0, 0, 0, 6),
('story_129_5', '检查获得的物品', 'story_129_6', '', 1, 0, 0, 0, 0, 7),
('story_129_5', '继续探索', 'story_129_7', '', 1, 0, 0, 0, 0, 5),
('story_129_6', '继续前进', 'story_129_7', '', 1, 0, 0, 0, 0, 5),
('story_129_6', '停下来思考', 'story_129_8', '', 1, 0, 0, 0, 0, 4),
('story_129_6', '观察周围情况', 'story_129_9', '', 1, 0, 0, 0, 0, 6),
('story_129_7', '继续前进', 'story_129_8', '', 1, 0, 0, 0, 0, 5),
('story_129_7', '停下来思考', 'story_129_9', '', 1, 0, 0, 0, 0, 4),
('story_129_7', '观察周围情况', 'story_129_10', '', 1, 0, 0, 0, 0, 6),
('story_129_8', '继续前进', 'story_129_9', '', 1, 0, 0, 0, 0, 5),
('story_129_8', '停下来思考', 'story_129_10', '', 1, 0, 0, 0, 0, 4),
('story_129_8', '观察周围情况', 'story_130_1', '', 1, 0, 0, 0, 0, 6),
('story_129_9', '继续前进', 'story_129_10', '', 1, 0, 0, 0, 0, 5),
('story_129_9', '停下来思考', 'story_130_1', '', 1, 0, 0, 0, 0, 4),
('story_129_9', '观察周围情况', 'story_130_1', '', 1, 0, 0, 0, 0, 6),
('story_129_10', '继续前进', 'story_130_1', '', 1, 0, 0, 0, 0, 5),
('story_129_10', '停下来思考', 'story_130_1', '', 1, 0, 0, 0, 0, 4),
('story_129_10', '观察周围情况', 'story_130_1', '', 1, 0, 0, 0, 0, 6),
('story_130_1', '继续前进', 'story_130_2', '', 1, 0, 0, 0, 0, 5),
('story_130_1', '停下来思考', 'story_130_3', '', 1, 0, 0, 0, 0, 4),
('story_130_1', '观察周围情况', 'story_130_4', '', 1, 0, 0, 0, 0, 6),
('story_130_2', '继续前进', 'story_130_3', '', 1, 0, 0, 0, 0, 5),
('story_130_2', '停下来思考', 'story_130_4', '', 1, 0, 0, 0, 0, 4),
('story_130_2', '观察周围情况', 'story_130_5', '', 1, 0, 0, 0, 0, 6),
('story_130_3', '继续前进', 'story_130_4', '', 1, 0, 0, 0, 0, 5),
('story_130_3', '停下来思考', 'story_130_5', '', 1, 0, 0, 0, 0, 4),
('story_130_3', '观察周围情况', 'story_130_6', '', 1, 0, 0, 0, 0, 6),
('story_130_4', '继续前进', 'story_130_5', '', 1, 0, 0, 0, 0, 5),
('story_130_4', '停下来思考', 'story_130_6', '', 1, 0, 0, 0, 0, 4),
('story_130_4', '观察周围情况', 'story_130_7', '', 1, 0, 0, 0, 0, 6),
('story_130_5', '继续前进', 'story_130_6', '', 1, 0, 0, 0, 0, 5),
('story_130_5', '停下来思考', 'story_130_7', '', 1, 0, 0, 0, 0, 4),
('story_130_5', '观察周围情况', 'story_130_8', '', 1, 0, 0, 0, 0, 6),
('story_130_6', '继续前进', 'story_130_7', '', 1, 0, 0, 0, 0, 5),
('story_130_6', '停下来思考', 'story_130_8', '', 1, 0, 0, 0, 0, 4),
('story_130_6', '观察周围情况', 'story_130_9', '', 1, 0, 0, 0, 0, 6),
('story_130_7', '继续前进', 'story_130_8', '', 1, 0, 0, 0, 0, 5),
('story_130_7', '停下来思考', 'story_130_9', '', 1, 0, 0, 0, 0, 4),
('story_130_7', '观察周围情况', 'story_130_10', '', 1, 0, 0, 0, 0, 6),
('story_130_8', '继续前进', 'story_130_9', '', 1, 0, 0, 0, 0, 5),
('story_130_8', '停下来思考', 'story_130_10', '', 1, 0, 0, 0, 0, 4),
('story_130_8', '观察周围情况', 'story_131_1', '', 1, 0, 0, 0, 0, 6),
('story_130_9', '继续前进', 'story_130_10', '', 1, 0, 0, 0, 0, 5),
('story_130_9', '停下来思考', 'story_131_1', '', 1, 0, 0, 0, 0, 4),
('story_130_9', '观察周围情况', 'story_131_1', '', 1, 0, 0, 0, 0, 6),
('story_130_10', '继续前进', 'story_131_1', '', 1, 0, 0, 0, 0, 5),
('story_130_10', '停下来思考', 'story_131_1', '', 1, 0, 0, 0, 0, 4),
('story_130_10', '观察周围情况', 'story_131_1', '', 1, 0, 0, 0, 0, 6),
('story_131_1', '继续前进', 'story_131_2', '', 1, 0, 0, 0, 0, 5),
('story_131_1', '停下来思考', 'story_131_3', '', 1, 0, 0, 0, 0, 4),
('story_131_1', '观察周围情况', 'story_131_4', '', 1, 0, 0, 0, 0, 6),
('story_131_2', '继续前进', 'story_131_3', '', 1, 0, 0, 0, 0, 5),
('story_131_2', '停下来思考', 'story_131_4', '', 1, 0, 0, 0, 0, 4),
('story_131_2', '观察周围情况', 'story_131_5', '', 1, 0, 0, 0, 0, 6),
('story_131_3', '与其他人交流', 'story_131_4', '', 1, 0, 0, 0, 0, 6),
('story_131_3', '继续探索', 'story_131_5', '', 1, 0, 0, 0, 0, 5),
('story_131_4', '继续前进', 'story_131_5', '', 1, 0, 0, 0, 0, 5),
('story_131_4', '停下来思考', 'story_131_6', '', 1, 0, 0, 0, 0, 4),
('story_131_4', '观察周围情况', 'story_131_7', '', 1, 0, 0, 0, 0, 6),
('story_131_5', '继续前进', 'story_131_6', '', 1, 0, 0, 0, 0, 5),
('story_131_5', '停下来思考', 'story_131_7', '', 1, 0, 0, 0, 0, 4),
('story_131_5', '观察周围情况', 'story_131_8', '', 1, 0, 0, 0, 0, 6),
('story_131_6', '继续前进', 'story_131_7', '', 1, 0, 0, 0, 0, 5),
('story_131_6', '停下来思考', 'story_131_8', '', 1, 0, 0, 0, 0, 4),
('story_131_6', '观察周围情况', 'story_131_9', '', 1, 0, 0, 0, 0, 6),
('story_131_7', '继续前进', 'story_131_8', '', 1, 0, 0, 0, 0, 5),
('story_131_7', '停下来思考', 'story_131_9', '', 1, 0, 0, 0, 0, 4),
('story_131_7', '观察周围情况', 'story_131_10', '', 1, 0, 0, 0, 0, 6),
('story_131_8', '继续前进', 'story_131_9', '', 1, 0, 0, 0, 0, 5),
('story_131_8', '停下来思考', 'story_131_10', '', 1, 0, 0, 0, 0, 4),
('story_131_8', '观察周围情况', 'story_132_1', '', 1, 0, 0, 0, 0, 6),
('story_131_8', '探索新的方向', 'story_131_11', '', 1, 0, 0, 0, 0, 7),
('story_131_9', '继续前进', 'story_131_10', '', 1, 0, 0, 0, 0, 5),
('story_131_9', '停下来思考', 'story_132_1', '', 1, 0, 0, 0, 0, 4),
('story_131_9', '观察周围情况', 'story_132_1', '', 1, 0, 0, 0, 0, 6),
('story_131_9', '探索新的方向', 'story_131_12', '', 1, 0, 0, 0, 0, 7),
('story_131_10', '继续前进', 'story_132_1', '', 1, 0, 0, 0, 0, 5),
('story_131_10', '停下来思考', 'story_132_1', '', 1, 0, 0, 0, 0, 4),
('story_131_10', '观察周围情况', 'story_132_1', '', 1, 0, 0, 0, 0, 6),
('story_131_10', '探索新的方向', 'story_131_12', '', 1, 0, 0, 0, 0, 7),
('story_131_11', '继续前进', 'story_132_1', '', 1, 0, 0, 0, 0, 5),
('story_131_11', '停下来思考', 'story_132_1', '', 1, 0, 0, 0, 0, 4),
('story_131_11', '观察周围情况', 'story_132_1', '', 1, 0, 0, 0, 0, 6),
('story_131_12', '继续前进', 'story_132_1', '', 1, 0, 0, 0, 0, 5),
('story_131_12', '停下来思考', 'story_132_1', '', 1, 0, 0, 0, 0, 4),
('story_131_12', '观察周围情况', 'story_132_1', '', 1, 0, 0, 0, 0, 6),
('story_132_1', '继续前进', 'story_132_2', '', 1, 0, 0, 0, 0, 5),
('story_132_1', '停下来思考', 'story_132_3', '', 1, 0, 0, 0, 0, 4),
('story_132_1', '观察周围情况', 'story_132_4', '', 1, 0, 0, 0, 0, 6),
('story_132_2', '仔细探索周围环境', 'story_132_3', '', 1, 0, 0, 0, 0, 8),
('story_132_2', '继续探索', 'story_132_4', '', 1, 0, 0, 0, 0, 5),
('story_132_3', '继续前进', 'story_132_4', '', 1, 0, 0, 0, 0, 5),
('story_132_3', '停下来思考', 'story_132_5', '', 1, 0, 0, 0, 0, 4),
('story_132_3', '观察周围情况', 'story_132_6', '', 1, 0, 0, 0, 0, 6),
('story_132_4', '继续前进', 'story_132_5', '', 1, 0, 0, 0, 0, 5),
('story_132_4', '停下来思考', 'story_132_6', '', 1, 0, 0, 0, 0, 4),
('story_132_4', '观察周围情况', 'story_132_7', '', 1, 0, 0, 0, 0, 6),
('story_132_5', '继续前进', 'story_132_6', '', 1, 0, 0, 0, 0, 5),
('story_132_5', '停下来思考', 'story_132_7', '', 1, 0, 0, 0, 0, 4),
('story_132_5', '观察周围情况', 'story_132_8', '', 1, 0, 0, 0, 0, 6),
('story_132_6', '与其他人交流', 'story_132_7', '', 1, 0, 0, 0, 0, 6),
('story_132_6', '继续探索', 'story_132_8', '', 1, 0, 0, 0, 0, 5),
('story_132_7', '继续前进', 'story_132_8', '', 1, 0, 0, 0, 0, 5),
('story_132_7', '停下来思考', 'story_132_9', '', 1, 0, 0, 0, 0, 4),
('story_132_7', '观察周围情况', 'story_132_10', '', 1, 0, 0, 0, 0, 6),
('story_132_8', '继续前进', 'story_132_9', '', 1, 0, 0, 0, 0, 5),
('story_132_8', '停下来思考', 'story_132_10', '', 1, 0, 0, 0, 0, 4),
('story_132_8', '观察周围情况', 'story_133_1', '', 1, 0, 0, 0, 0, 6),
('story_132_9', '继续前进', 'story_132_10', '', 1, 0, 0, 0, 0, 5),
('story_132_9', '停下来思考', 'story_133_1', '', 1, 0, 0, 0, 0, 4),
('story_132_9', '观察周围情况', 'story_133_1', '', 1, 0, 0, 0, 0, 6),
('story_132_10', '继续前进', 'story_133_1', '', 1, 0, 0, 0, 0, 5),
('story_132_10', '停下来思考', 'story_133_1', '', 1, 0, 0, 0, 0, 4),
('story_132_10', '观察周围情况', 'story_133_1', '', 1, 0, 0, 0, 0, 6),
('story_133_1', '与其他人交流', 'story_133_2', '', 1, 0, 0, 0, 0, 6),
('story_133_1', '继续探索', 'story_133_3', '', 1, 0, 0, 0, 0, 5),
('story_133_2', '继续前进', 'story_133_3', '', 1, 0, 0, 0, 0, 5),
('story_133_2', '停下来思考', 'story_133_4', '', 1, 0, 0, 0, 0, 4),
('story_133_2', '观察周围情况', 'story_133_5', '', 1, 0, 0, 0, 0, 6),
('story_133_3', '继续前进', 'story_133_4', '', 1, 0, 0, 0, 0, 5),
('story_133_3', '停下来思考', 'story_133_5', '', 1, 0, 0, 0, 0, 4),
('story_133_3', '观察周围情况', 'story_133_6', '', 1, 0, 0, 0, 0, 6),
('story_133_4', '继续前进', 'story_133_5', '', 1, 0, 0, 0, 0, 5),
('story_133_4', '停下来思考', 'story_133_6', '', 1, 0, 0, 0, 0, 4),
('story_133_4', '观察周围情况', 'story_133_7', '', 1, 0, 0, 0, 0, 6),
('story_133_5', '继续前进', 'story_133_6', '', 1, 0, 0, 0, 0, 5),
('story_133_5', '停下来思考', 'story_133_7', '', 1, 0, 0, 0, 0, 4);

-- 批次统计
-- 本批次选择数: 500
-- 批次范围: 4501 - 5000
