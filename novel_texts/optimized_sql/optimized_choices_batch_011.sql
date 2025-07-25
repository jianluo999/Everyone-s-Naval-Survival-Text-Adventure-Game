-- 优化选择数据批次 11
-- 清理现有数据（仅第一批次）
INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES
('story_133_5', '观察周围情况', 'story_133_8', '', 1, 0, 0, 0, 0, 6),
('story_133_6', '继续前进', 'story_133_7', '', 1, 0, 0, 0, 0, 5),
('story_133_6', '停下来思考', 'story_133_8', '', 1, 0, 0, 0, 0, 4),
('story_133_6', '观察周围情况', 'story_133_9', '', 1, 0, 0, 0, 0, 6),
('story_133_7', '继续前进', 'story_133_8', '', 1, 0, 0, 0, 0, 5),
('story_133_7', '停下来思考', 'story_133_9', '', 1, 0, 0, 0, 0, 4),
('story_133_7', '观察周围情况', 'story_133_10', '', 1, 0, 0, 0, 0, 6),
('story_133_8', '检查获得的物品', 'story_133_9', '', 1, 0, 0, 0, 0, 7),
('story_133_8', '继续探索', 'story_133_10', '', 1, 0, 0, 0, 0, 5),
('story_133_8', '探索新的方向', 'story_133_11', '', 1, 0, 0, 0, 0, 7),
('story_133_9', '检查获得的物品', 'story_133_10', '', 1, 0, 0, 0, 0, 7),
('story_133_9', '继续探索', 'story_134_1', '', 1, 0, 0, 0, 0, 5),
('story_133_9', '探索新的方向', 'story_133_11', '', 1, 0, 0, 0, 0, 7),
('story_133_10', '继续前进', 'story_134_1', '', 1, 0, 0, 0, 0, 5),
('story_133_10', '停下来思考', 'story_134_1', '', 1, 0, 0, 0, 0, 4),
('story_133_10', '观察周围情况', 'story_134_1', '', 1, 0, 0, 0, 0, 6),
('story_133_11', '继续前进', 'story_134_1', '', 1, 0, 0, 0, 0, 5),
('story_133_11', '停下来思考', 'story_134_1', '', 1, 0, 0, 0, 0, 4),
('story_133_11', '观察周围情况', 'story_134_1', '', 1, 0, 0, 0, 0, 6),
('story_134_1', '检查获得的物品', 'story_134_2', '', 1, 0, 0, 0, 0, 7),
('story_134_1', '继续探索', 'story_134_3', '', 1, 0, 0, 0, 0, 5),
('story_134_2', '继续前进', 'story_134_3', '', 1, 0, 0, 0, 0, 5),
('story_134_2', '停下来思考', 'story_134_4', '', 1, 0, 0, 0, 0, 4),
('story_134_2', '观察周围情况', 'story_134_5', '', 1, 0, 0, 0, 0, 6),
('story_134_3', '继续前进', 'story_134_4', '', 1, 0, 0, 0, 0, 5),
('story_134_3', '停下来思考', 'story_134_5', '', 1, 0, 0, 0, 0, 4),
('story_134_3', '观察周围情况', 'story_134_6', '', 1, 0, 0, 0, 0, 6),
('story_134_4', '检查获得的物品', 'story_134_5', '', 1, 0, 0, 0, 0, 7),
('story_134_4', '继续探索', 'story_134_6', '', 1, 0, 0, 0, 0, 5),
('story_134_5', '继续前进', 'story_134_6', '', 1, 0, 0, 0, 0, 5),
('story_134_5', '停下来思考', 'story_134_7', '', 1, 0, 0, 0, 0, 4),
('story_134_5', '观察周围情况', 'story_134_8', '', 1, 0, 0, 0, 0, 6),
('story_134_6', '检查获得的物品', 'story_134_7', '', 1, 0, 0, 0, 0, 7),
('story_134_6', '继续探索', 'story_134_8', '', 1, 0, 0, 0, 0, 5),
('story_134_7', '继续前进', 'story_134_8', '', 1, 0, 0, 0, 0, 5),
('story_134_7', '停下来思考', 'story_134_9', '', 1, 0, 0, 0, 0, 4),
('story_134_7', '观察周围情况', 'story_134_10', '', 1, 0, 0, 0, 0, 6),
('story_134_8', '检查获得的物品', 'story_134_9', '', 1, 0, 0, 0, 0, 7),
('story_134_8', '继续探索', 'story_134_10', '', 1, 0, 0, 0, 0, 5),
('story_134_8', '探索新的方向', 'story_134_11', '', 1, 0, 0, 0, 0, 7),
('story_134_9', '继续前进', 'story_134_10', '', 1, 0, 0, 0, 0, 5),
('story_134_9', '停下来思考', 'story_135_1', '', 1, 0, 0, 0, 0, 4),
('story_134_9', '观察周围情况', 'story_135_1', '', 1, 0, 0, 0, 0, 6),
('story_134_9', '探索新的方向', 'story_134_11', '', 1, 0, 0, 0, 0, 7),
('story_134_10', '检查获得的物品', 'story_135_1', '', 1, 0, 0, 0, 0, 7),
('story_134_10', '继续探索', 'story_135_1', '', 1, 0, 0, 0, 0, 5),
('story_134_11', '检查获得的物品', 'story_135_1', '', 1, 0, 0, 0, 0, 7),
('story_134_11', '继续探索', 'story_135_1', '', 1, 0, 0, 0, 0, 5),
('story_135_1', '检查获得的物品', 'story_135_2', '', 1, 0, 0, 0, 0, 7),
('story_135_1', '继续探索', 'story_135_3', '', 1, 0, 0, 0, 0, 5),
('story_135_2', '继续前进', 'story_135_3', '', 1, 0, 0, 0, 0, 5),
('story_135_2', '停下来思考', 'story_135_4', '', 1, 0, 0, 0, 0, 4),
('story_135_2', '观察周围情况', 'story_135_5', '', 1, 0, 0, 0, 0, 6),
('story_135_3', '检查获得的物品', 'story_135_4', '', 1, 0, 0, 0, 0, 7),
('story_135_3', '继续探索', 'story_135_5', '', 1, 0, 0, 0, 0, 5),
('story_135_4', '检查获得的物品', 'story_135_5', '', 1, 0, 0, 0, 0, 7),
('story_135_4', '继续探索', 'story_135_6', '', 1, 0, 0, 0, 0, 5),
('story_135_5', '与其他人交流', 'story_135_6', '', 1, 0, 0, 0, 0, 6),
('story_135_5', '继续探索', 'story_135_7', '', 1, 0, 0, 0, 0, 5),
('story_135_6', '继续前进', 'story_135_7', '', 1, 0, 0, 0, 0, 5),
('story_135_6', '停下来思考', 'story_135_8', '', 1, 0, 0, 0, 0, 4),
('story_135_6', '观察周围情况', 'story_135_9', '', 1, 0, 0, 0, 0, 6),
('story_135_7', '检查获得的物品', 'story_135_8', '', 1, 0, 0, 0, 0, 7),
('story_135_7', '继续探索', 'story_135_9', '', 1, 0, 0, 0, 0, 5),
('story_135_8', '继续前进', 'story_135_9', '', 1, 0, 0, 0, 0, 5),
('story_135_8', '停下来思考', 'story_135_10', '', 1, 0, 0, 0, 0, 4),
('story_135_8', '观察周围情况', 'story_136_1', '', 1, 0, 0, 0, 0, 6),
('story_135_9', '继续前进', 'story_135_10', '', 1, 0, 0, 0, 0, 5),
('story_135_9', '停下来思考', 'story_136_1', '', 1, 0, 0, 0, 0, 4),
('story_135_9', '观察周围情况', 'story_136_1', '', 1, 0, 0, 0, 0, 6),
('story_135_10', '继续前进', 'story_136_1', '', 1, 0, 0, 0, 0, 5),
('story_135_10', '停下来思考', 'story_136_1', '', 1, 0, 0, 0, 0, 4),
('story_135_10', '观察周围情况', 'story_136_1', '', 1, 0, 0, 0, 0, 6),
('story_136_1', '检查获得的物品', 'story_136_2', '', 1, 0, 0, 0, 0, 7),
('story_136_1', '继续探索', 'story_136_3', '', 1, 0, 0, 0, 0, 5),
('story_136_2', '继续前进', 'story_136_3', '', 1, 0, 0, 0, 0, 5),
('story_136_2', '停下来思考', 'story_136_4', '', 1, 0, 0, 0, 0, 4),
('story_136_2', '观察周围情况', 'story_136_5', '', 1, 0, 0, 0, 0, 6),
('story_136_3', '继续前进', 'story_136_4', '', 1, 0, 0, 0, 0, 5),
('story_136_3', '停下来思考', 'story_136_5', '', 1, 0, 0, 0, 0, 4),
('story_136_3', '观察周围情况', 'story_136_6', '', 1, 0, 0, 0, 0, 6),
('story_136_4', '继续前进', 'story_136_5', '', 1, 0, 0, 0, 0, 5),
('story_136_4', '停下来思考', 'story_136_6', '', 1, 0, 0, 0, 0, 4),
('story_136_4', '观察周围情况', 'story_136_7', '', 1, 0, 0, 0, 0, 6),
('story_136_5', '继续前进', 'story_136_6', '', 1, 0, 0, 0, 0, 5),
('story_136_5', '停下来思考', 'story_136_7', '', 1, 0, 0, 0, 0, 4),
('story_136_5', '观察周围情况', 'story_136_8', '', 1, 0, 0, 0, 0, 6),
('story_136_6', '检查获得的物品', 'story_136_7', '', 1, 0, 0, 0, 0, 7),
('story_136_6', '继续探索', 'story_136_8', '', 1, 0, 0, 0, 0, 5),
('story_136_7', '继续前进', 'story_136_8', '', 1, 0, 0, 0, 0, 5),
('story_136_7', '停下来思考', 'story_136_9', '', 1, 0, 0, 0, 0, 4),
('story_136_7', '观察周围情况', 'story_136_10', '', 1, 0, 0, 0, 0, 6),
('story_136_8', '继续前进', 'story_136_9', '', 1, 0, 0, 0, 0, 5),
('story_136_8', '停下来思考', 'story_136_10', '', 1, 0, 0, 0, 0, 4),
('story_136_8', '观察周围情况', 'story_137_1', '', 1, 0, 0, 0, 0, 6),
('story_136_8', '探索新的方向', 'story_136_11', '', 1, 0, 0, 0, 0, 7),
('story_136_9', '检查获得的物品', 'story_136_10', '', 1, 0, 0, 0, 0, 7),
('story_136_9', '继续探索', 'story_137_1', '', 1, 0, 0, 0, 0, 5),
('story_136_9', '探索新的方向', 'story_136_11', '', 1, 0, 0, 0, 0, 7),
('story_136_9', '探索新的方向', 'story_136_12', '', 1, 0, 0, 0, 0, 7),
('story_136_10', '检查获得的物品', 'story_137_1', '', 1, 0, 0, 0, 0, 7),
('story_136_10', '继续探索', 'story_137_1', '', 1, 0, 0, 0, 0, 5),
('story_136_10', '探索新的方向', 'story_136_12', '', 1, 0, 0, 0, 0, 7),
('story_136_11', '检查获得的物品', 'story_137_1', '', 1, 0, 0, 0, 0, 7),
('story_136_11', '继续探索', 'story_137_1', '', 1, 0, 0, 0, 0, 5),
('story_136_12', '检查获得的物品', 'story_137_1', '', 1, 0, 0, 0, 0, 7),
('story_136_12', '继续探索', 'story_137_1', '', 1, 0, 0, 0, 0, 5),
('story_137_1', '继续前进', 'story_137_2', '', 1, 0, 0, 0, 0, 5),
('story_137_1', '停下来思考', 'story_137_3', '', 1, 0, 0, 0, 0, 4),
('story_137_1', '观察周围情况', 'story_137_4', '', 1, 0, 0, 0, 0, 6),
('story_137_2', '继续前进', 'story_137_3', '', 1, 0, 0, 0, 0, 5),
('story_137_2', '停下来思考', 'story_137_4', '', 1, 0, 0, 0, 0, 4),
('story_137_2', '观察周围情况', 'story_137_5', '', 1, 0, 0, 0, 0, 6),
('story_137_3', '继续前进', 'story_137_4', '', 1, 0, 0, 0, 0, 5),
('story_137_3', '停下来思考', 'story_137_5', '', 1, 0, 0, 0, 0, 4),
('story_137_3', '观察周围情况', 'story_137_6', '', 1, 0, 0, 0, 0, 6),
('story_137_4', '继续前进', 'story_137_5', '', 1, 0, 0, 0, 0, 5),
('story_137_4', '停下来思考', 'story_137_6', '', 1, 0, 0, 0, 0, 4),
('story_137_4', '观察周围情况', 'story_137_7', '', 1, 0, 0, 0, 0, 6),
('story_137_5', '检查获得的物品', 'story_137_6', '', 1, 0, 0, 0, 0, 7),
('story_137_5', '继续探索', 'story_137_7', '', 1, 0, 0, 0, 0, 5),
('story_137_6', '检查获得的物品', 'story_137_7', '', 1, 0, 0, 0, 0, 7),
('story_137_6', '继续探索', 'story_137_8', '', 1, 0, 0, 0, 0, 5),
('story_137_7', '继续前进', 'story_137_8', '', 1, 0, 0, 0, 0, 5),
('story_137_7', '停下来思考', 'story_137_9', '', 1, 0, 0, 0, 0, 4),
('story_137_7', '观察周围情况', 'story_137_10', '', 1, 0, 0, 0, 0, 6),
('story_137_8', '继续前进', 'story_137_9', '', 1, 0, 0, 0, 0, 5),
('story_137_8', '停下来思考', 'story_137_10', '', 1, 0, 0, 0, 0, 4),
('story_137_8', '观察周围情况', 'story_138_1', '', 1, 0, 0, 0, 0, 6),
('story_137_8', '探索新的方向', 'story_137_11', '', 1, 0, 0, 0, 0, 7),
('story_137_9', '检查获得的物品', 'story_137_10', '', 1, 0, 0, 0, 0, 7),
('story_137_9', '继续探索', 'story_138_1', '', 1, 0, 0, 0, 0, 5),
('story_137_9', '探索新的方向', 'story_137_11', '', 1, 0, 0, 0, 0, 7),
('story_137_9', '探索新的方向', 'story_137_12', '', 1, 0, 0, 0, 0, 7),
('story_137_10', '继续前进', 'story_138_1', '', 1, 0, 0, 0, 0, 5),
('story_137_10', '停下来思考', 'story_138_1', '', 1, 0, 0, 0, 0, 4),
('story_137_10', '观察周围情况', 'story_138_1', '', 1, 0, 0, 0, 0, 6),
('story_137_10', '探索新的方向', 'story_137_13', '', 1, 0, 0, 0, 0, 7),
('story_137_11', '继续前进', 'story_138_1', '', 1, 0, 0, 0, 0, 5),
('story_137_11', '停下来思考', 'story_138_1', '', 1, 0, 0, 0, 0, 4),
('story_137_11', '观察周围情况', 'story_138_1', '', 1, 0, 0, 0, 0, 6),
('story_137_11', '探索新的方向', 'story_137_13', '', 1, 0, 0, 0, 0, 7),
('story_137_12', '继续前进', 'story_138_1', '', 1, 0, 0, 0, 0, 5),
('story_137_12', '停下来思考', 'story_138_1', '', 1, 0, 0, 0, 0, 4),
('story_137_12', '观察周围情况', 'story_138_1', '', 1, 0, 0, 0, 0, 6),
('story_137_13', '继续前进', 'story_138_1', '', 1, 0, 0, 0, 0, 5),
('story_137_13', '停下来思考', 'story_138_1', '', 1, 0, 0, 0, 0, 4),
('story_137_13', '观察周围情况', 'story_138_1', '', 1, 0, 0, 0, 0, 6),
('story_138_1', '检查获得的物品', 'story_138_2', '', 1, 0, 0, 0, 0, 7),
('story_138_1', '继续探索', 'story_138_3', '', 1, 0, 0, 0, 0, 5),
('story_138_2', '继续前进', 'story_138_3', '', 1, 0, 0, 0, 0, 5),
('story_138_2', '停下来思考', 'story_138_4', '', 1, 0, 0, 0, 0, 4),
('story_138_2', '观察周围情况', 'story_138_5', '', 1, 0, 0, 0, 0, 6),
('story_138_3', '继续前进', 'story_138_4', '', 1, 0, 0, 0, 0, 5),
('story_138_3', '停下来思考', 'story_138_5', '', 1, 0, 0, 0, 0, 4),
('story_138_3', '观察周围情况', 'story_138_6', '', 1, 0, 0, 0, 0, 6),
('story_138_4', '继续前进', 'story_138_5', '', 1, 0, 0, 0, 0, 5),
('story_138_4', '停下来思考', 'story_138_6', '', 1, 0, 0, 0, 0, 4),
('story_138_4', '观察周围情况', 'story_138_7', '', 1, 0, 0, 0, 0, 6),
('story_138_5', '继续前进', 'story_138_6', '', 1, 0, 0, 0, 0, 5),
('story_138_5', '停下来思考', 'story_138_7', '', 1, 0, 0, 0, 0, 4),
('story_138_5', '观察周围情况', 'story_138_8', '', 1, 0, 0, 0, 0, 6),
('story_138_6', '继续前进', 'story_138_7', '', 1, 0, 0, 0, 0, 5),
('story_138_6', '停下来思考', 'story_138_8', '', 1, 0, 0, 0, 0, 4),
('story_138_6', '观察周围情况', 'story_138_9', '', 1, 0, 0, 0, 0, 6),
('story_138_7', '检查获得的物品', 'story_138_8', '', 1, 0, 0, 0, 0, 7),
('story_138_7', '继续探索', 'story_138_9', '', 1, 0, 0, 0, 0, 5),
('story_138_8', '继续前进', 'story_138_9', '', 1, 0, 0, 0, 0, 5),
('story_138_8', '停下来思考', 'story_138_10', '', 1, 0, 0, 0, 0, 4),
('story_138_8', '观察周围情况', 'story_139_1', '', 1, 0, 0, 0, 0, 6),
('story_138_8', '探索新的方向', 'story_138_11', '', 1, 0, 0, 0, 0, 7),
('story_138_9', '与其他人交流', 'story_138_10', '', 1, 0, 0, 0, 0, 6),
('story_138_9', '继续探索', 'story_139_1', '', 1, 0, 0, 0, 0, 5),
('story_138_9', '探索新的方向', 'story_138_11', '', 1, 0, 0, 0, 0, 7),
('story_138_9', '探索新的方向', 'story_138_12', '', 1, 0, 0, 0, 0, 7),
('story_138_10', '检查获得的物品', 'story_139_1', '', 1, 0, 0, 0, 0, 7),
('story_138_10', '继续探索', 'story_139_1', '', 1, 0, 0, 0, 0, 5),
('story_138_10', '探索新的方向', 'story_138_12', '', 1, 0, 0, 0, 0, 7),
('story_138_11', '继续前进', 'story_139_1', '', 1, 0, 0, 0, 0, 5),
('story_138_11', '停下来思考', 'story_139_1', '', 1, 0, 0, 0, 0, 4),
('story_138_11', '观察周围情况', 'story_139_1', '', 1, 0, 0, 0, 0, 6),
('story_138_12', '继续前进', 'story_139_1', '', 1, 0, 0, 0, 0, 5),
('story_138_12', '停下来思考', 'story_139_1', '', 1, 0, 0, 0, 0, 4),
('story_138_12', '观察周围情况', 'story_139_1', '', 1, 0, 0, 0, 0, 6),
('story_139_1', '与其他人交流', 'story_139_2', '', 1, 0, 0, 0, 0, 6),
('story_139_1', '继续探索', 'story_139_3', '', 1, 0, 0, 0, 0, 5),
('story_139_2', '继续前进', 'story_139_3', '', 1, 0, 0, 0, 0, 5),
('story_139_2', '停下来思考', 'story_139_4', '', 1, 0, 0, 0, 0, 4),
('story_139_2', '观察周围情况', 'story_139_5', '', 1, 0, 0, 0, 0, 6),
('story_139_3', '检查获得的物品', 'story_139_4', '', 1, 0, 0, 0, 0, 7),
('story_139_3', '继续探索', 'story_139_5', '', 1, 0, 0, 0, 0, 5),
('story_139_4', '继续前进', 'story_139_5', '', 1, 0, 0, 0, 0, 5),
('story_139_4', '停下来思考', 'story_139_6', '', 1, 0, 0, 0, 0, 4),
('story_139_4', '观察周围情况', 'story_139_7', '', 1, 0, 0, 0, 0, 6),
('story_139_5', '继续前进', 'story_139_6', '', 1, 0, 0, 0, 0, 5),
('story_139_5', '停下来思考', 'story_139_7', '', 1, 0, 0, 0, 0, 4),
('story_139_5', '观察周围情况', 'story_139_8', '', 1, 0, 0, 0, 0, 6),
('story_139_6', '检查获得的物品', 'story_139_7', '', 1, 0, 0, 0, 0, 7),
('story_139_6', '继续探索', 'story_139_8', '', 1, 0, 0, 0, 0, 5),
('story_139_7', '继续前进', 'story_139_8', '', 1, 0, 0, 0, 0, 5),
('story_139_7', '停下来思考', 'story_139_9', '', 1, 0, 0, 0, 0, 4),
('story_139_7', '观察周围情况', 'story_139_10', '', 1, 0, 0, 0, 0, 6),
('story_139_8', '继续前进', 'story_139_9', '', 1, 0, 0, 0, 0, 5),
('story_139_8', '停下来思考', 'story_139_10', '', 1, 0, 0, 0, 0, 4),
('story_139_8', '观察周围情况', 'story_140_1', '', 1, 0, 0, 0, 0, 6),
('story_139_9', '继续前进', 'story_139_10', '', 1, 0, 0, 0, 0, 5),
('story_139_9', '停下来思考', 'story_140_1', '', 1, 0, 0, 0, 0, 4),
('story_139_9', '观察周围情况', 'story_140_1', '', 1, 0, 0, 0, 0, 6),
('story_139_10', '继续前进', 'story_140_1', '', 1, 0, 0, 0, 0, 5),
('story_139_10', '停下来思考', 'story_140_1', '', 1, 0, 0, 0, 0, 4),
('story_139_10', '观察周围情况', 'story_140_1', '', 1, 0, 0, 0, 0, 6),
('story_140_1', '检查获得的物品', 'story_140_2', '', 1, 0, 0, 0, 0, 7),
('story_140_1', '继续探索', 'story_140_3', '', 1, 0, 0, 0, 0, 5),
('story_140_2', '继续前进', 'story_140_3', '', 1, 0, 0, 0, 0, 5),
('story_140_2', '停下来思考', 'story_140_4', '', 1, 0, 0, 0, 0, 4),
('story_140_2', '观察周围情况', 'story_140_5', '', 1, 0, 0, 0, 0, 6),
('story_140_3', '继续前进', 'story_140_4', '', 1, 0, 0, 0, 0, 5),
('story_140_3', '停下来思考', 'story_140_5', '', 1, 0, 0, 0, 0, 4),
('story_140_3', '观察周围情况', 'story_140_6', '', 1, 0, 0, 0, 0, 6),
('story_140_4', '继续前进', 'story_140_5', '', 1, 0, 0, 0, 0, 5),
('story_140_4', '停下来思考', 'story_140_6', '', 1, 0, 0, 0, 0, 4),
('story_140_4', '观察周围情况', 'story_140_7', '', 1, 0, 0, 0, 0, 6),
('story_140_5', '检查获得的物品', 'story_140_6', '', 1, 0, 0, 0, 0, 7),
('story_140_5', '继续探索', 'story_140_7', '', 1, 0, 0, 0, 0, 5),
('story_140_6', '继续前进', 'story_140_7', '', 1, 0, 0, 0, 0, 5),
('story_140_6', '停下来思考', 'story_140_8', '', 1, 0, 0, 0, 0, 4),
('story_140_6', '观察周围情况', 'story_140_9', '', 1, 0, 0, 0, 0, 6),
('story_140_7', '继续前进', 'story_140_8', '', 1, 0, 0, 0, 0, 5),
('story_140_7', '停下来思考', 'story_140_9', '', 1, 0, 0, 0, 0, 4),
('story_140_7', '观察周围情况', 'story_140_10', '', 1, 0, 0, 0, 0, 6),
('story_140_8', '继续前进', 'story_140_9', '', 1, 0, 0, 0, 0, 5),
('story_140_8', '停下来思考', 'story_140_10', '', 1, 0, 0, 0, 0, 4),
('story_140_8', '观察周围情况', 'story_141_1', '', 1, 0, 0, 0, 0, 6),
('story_140_9', '继续前进', 'story_140_10', '', 1, 0, 0, 0, 0, 5),
('story_140_9', '停下来思考', 'story_141_1', '', 1, 0, 0, 0, 0, 4),
('story_140_9', '观察周围情况', 'story_141_1', '', 1, 0, 0, 0, 0, 6),
('story_140_10', '继续前进', 'story_141_1', '', 1, 0, 0, 0, 0, 5),
('story_140_10', '停下来思考', 'story_141_1', '', 1, 0, 0, 0, 0, 4),
('story_140_10', '观察周围情况', 'story_141_1', '', 1, 0, 0, 0, 0, 6),
('story_141_1', '继续前进', 'story_141_2', '', 1, 0, 0, 0, 0, 5),
('story_141_1', '停下来思考', 'story_141_3', '', 1, 0, 0, 0, 0, 4),
('story_141_1', '观察周围情况', 'story_141_4', '', 1, 0, 0, 0, 0, 6),
('story_141_2', '与其他人交流', 'story_141_3', '', 1, 0, 0, 0, 0, 6),
('story_141_2', '继续探索', 'story_141_4', '', 1, 0, 0, 0, 0, 5),
('story_141_3', '与其他人交流', 'story_141_4', '', 1, 0, 0, 0, 0, 6),
('story_141_3', '继续探索', 'story_141_5', '', 1, 0, 0, 0, 0, 5),
('story_141_4', '继续前进', 'story_141_5', '', 1, 0, 0, 0, 0, 5),
('story_141_4', '停下来思考', 'story_141_6', '', 1, 0, 0, 0, 0, 4),
('story_141_4', '观察周围情况', 'story_141_7', '', 1, 0, 0, 0, 0, 6),
('story_141_5', '与其他人交流', 'story_141_6', '', 1, 0, 0, 0, 0, 6),
('story_141_5', '继续探索', 'story_141_7', '', 1, 0, 0, 0, 0, 5),
('story_141_6', '检查获得的物品', 'story_141_7', '', 1, 0, 0, 0, 0, 7),
('story_141_6', '继续探索', 'story_141_8', '', 1, 0, 0, 0, 0, 5),
('story_141_7', '继续前进', 'story_141_8', '', 1, 0, 0, 0, 0, 5),
('story_141_7', '停下来思考', 'story_141_9', '', 1, 0, 0, 0, 0, 4),
('story_141_7', '观察周围情况', 'story_141_10', '', 1, 0, 0, 0, 0, 6),
('story_141_8', '与其他人交流', 'story_141_9', '', 1, 0, 0, 0, 0, 6),
('story_141_8', '检查获得的物品', 'story_141_10', '', 1, 0, 0, 0, 0, 7),
('story_141_8', '探索新的方向', 'story_141_11', '', 1, 0, 0, 0, 0, 7),
('story_141_9', '检查获得的物品', 'story_141_10', '', 1, 0, 0, 0, 0, 7),
('story_141_9', '继续探索', 'story_142_1', '', 1, 0, 0, 0, 0, 5),
('story_141_9', '探索新的方向', 'story_141_11', '', 1, 0, 0, 0, 0, 7),
('story_141_10', '继续前进', 'story_142_1', '', 1, 0, 0, 0, 0, 5),
('story_141_10', '停下来思考', 'story_142_1', '', 1, 0, 0, 0, 0, 4),
('story_141_10', '观察周围情况', 'story_142_1', '', 1, 0, 0, 0, 0, 6),
('story_141_11', '继续前进', 'story_142_1', '', 1, 0, 0, 0, 0, 5),
('story_141_11', '停下来思考', 'story_142_1', '', 1, 0, 0, 0, 0, 4),
('story_141_11', '观察周围情况', 'story_142_1', '', 1, 0, 0, 0, 0, 6),
('story_142_1', '继续前进', 'story_142_2', '', 1, 0, 0, 0, 0, 5),
('story_142_1', '停下来思考', 'story_142_3', '', 1, 0, 0, 0, 0, 4),
('story_142_1', '观察周围情况', 'story_142_4', '', 1, 0, 0, 0, 0, 6),
('story_142_2', '继续前进', 'story_142_3', '', 1, 0, 0, 0, 0, 5),
('story_142_2', '停下来思考', 'story_142_4', '', 1, 0, 0, 0, 0, 4),
('story_142_2', '观察周围情况', 'story_142_5', '', 1, 0, 0, 0, 0, 6),
('story_142_3', '检查获得的物品', 'story_142_4', '', 1, 0, 0, 0, 0, 7),
('story_142_3', '继续探索', 'story_142_5', '', 1, 0, 0, 0, 0, 5),
('story_142_4', '检查获得的物品', 'story_142_5', '', 1, 0, 0, 0, 0, 7),
('story_142_4', '继续探索', 'story_142_6', '', 1, 0, 0, 0, 0, 5),
('story_142_5', '检查获得的物品', 'story_142_6', '', 1, 0, 0, 0, 0, 7),
('story_142_5', '继续探索', 'story_142_7', '', 1, 0, 0, 0, 0, 5),
('story_142_6', '检查获得的物品', 'story_142_7', '', 1, 0, 0, 0, 0, 7),
('story_142_6', '继续探索', 'story_142_8', '', 1, 0, 0, 0, 0, 5),
('story_142_7', '继续前进', 'story_142_8', '', 1, 0, 0, 0, 0, 5),
('story_142_7', '停下来思考', 'story_142_9', '', 1, 0, 0, 0, 0, 4),
('story_142_7', '观察周围情况', 'story_142_10', '', 1, 0, 0, 0, 0, 6),
('story_142_8', '继续前进', 'story_142_9', '', 1, 0, 0, 0, 0, 5),
('story_142_8', '停下来思考', 'story_142_10', '', 1, 0, 0, 0, 0, 4),
('story_142_8', '观察周围情况', 'story_143_1', '', 1, 0, 0, 0, 0, 6),
('story_142_8', '探索新的方向', 'story_142_11', '', 1, 0, 0, 0, 0, 7),
('story_142_9', '检查获得的物品', 'story_142_10', '', 1, 0, 0, 0, 0, 7),
('story_142_9', '继续探索', 'story_143_1', '', 1, 0, 0, 0, 0, 5),
('story_142_9', '探索新的方向', 'story_142_12', '', 1, 0, 0, 0, 0, 7),
('story_142_9', '探索新的方向', 'story_142_11', '', 1, 0, 0, 0, 0, 7),
('story_142_10', '检查获得的物品', 'story_143_1', '', 1, 0, 0, 0, 0, 7),
('story_142_10', '继续探索', 'story_143_1', '', 1, 0, 0, 0, 0, 5),
('story_142_10', '探索新的方向', 'story_142_12', '', 1, 0, 0, 0, 0, 7),
('story_142_11', '继续前进', 'story_143_1', '', 1, 0, 0, 0, 0, 5),
('story_142_11', '停下来思考', 'story_143_1', '', 1, 0, 0, 0, 0, 4),
('story_142_11', '观察周围情况', 'story_143_1', '', 1, 0, 0, 0, 0, 6),
('story_142_12', '检查获得的物品', 'story_143_1', '', 1, 0, 0, 0, 0, 7),
('story_142_12', '继续探索', 'story_143_1', '', 1, 0, 0, 0, 0, 5),
('story_143_1', '检查获得的物品', 'story_143_2', '', 1, 0, 0, 0, 0, 7),
('story_143_1', '继续探索', 'story_143_3', '', 1, 0, 0, 0, 0, 5),
('story_143_2', '继续前进', 'story_143_3', '', 1, 0, 0, 0, 0, 5),
('story_143_2', '停下来思考', 'story_143_4', '', 1, 0, 0, 0, 0, 4),
('story_143_2', '观察周围情况', 'story_143_5', '', 1, 0, 0, 0, 0, 6),
('story_143_3', '继续前进', 'story_143_4', '', 1, 0, 0, 0, 0, 5),
('story_143_3', '停下来思考', 'story_143_5', '', 1, 0, 0, 0, 0, 4),
('story_143_3', '观察周围情况', 'story_143_6', '', 1, 0, 0, 0, 0, 6),
('story_143_4', '继续前进', 'story_143_5', '', 1, 0, 0, 0, 0, 5),
('story_143_4', '停下来思考', 'story_143_6', '', 1, 0, 0, 0, 0, 4),
('story_143_4', '观察周围情况', 'story_143_7', '', 1, 0, 0, 0, 0, 6),
('story_143_5', '继续前进', 'story_143_6', '', 1, 0, 0, 0, 0, 5),
('story_143_5', '停下来思考', 'story_143_7', '', 1, 0, 0, 0, 0, 4),
('story_143_5', '观察周围情况', 'story_143_8', '', 1, 0, 0, 0, 0, 6),
('story_143_6', '继续前进', 'story_143_7', '', 1, 0, 0, 0, 0, 5),
('story_143_6', '停下来思考', 'story_143_8', '', 1, 0, 0, 0, 0, 4),
('story_143_6', '观察周围情况', 'story_143_9', '', 1, 0, 0, 0, 0, 6),
('story_143_7', '继续前进', 'story_143_8', '', 1, 0, 0, 0, 0, 5),
('story_143_7', '停下来思考', 'story_143_9', '', 1, 0, 0, 0, 0, 4),
('story_143_7', '观察周围情况', 'story_143_10', '', 1, 0, 0, 0, 0, 6),
('story_143_8', '继续前进', 'story_143_9', '', 1, 0, 0, 0, 0, 5),
('story_143_8', '停下来思考', 'story_143_10', '', 1, 0, 0, 0, 0, 4),
('story_143_8', '观察周围情况', 'story_144_1', '', 1, 0, 0, 0, 0, 6),
('story_143_9', '与其他人交流', 'story_143_10', '', 1, 0, 0, 0, 0, 6),
('story_143_9', '继续探索', 'story_144_1', '', 1, 0, 0, 0, 0, 5),
('story_143_10', '继续前进', 'story_144_1', '', 1, 0, 0, 0, 0, 5),
('story_143_10', '停下来思考', 'story_144_1', '', 1, 0, 0, 0, 0, 4),
('story_143_10', '观察周围情况', 'story_144_1', '', 1, 0, 0, 0, 0, 6),
('story_144_1', '继续前进', 'story_144_2', '', 1, 0, 0, 0, 0, 5),
('story_144_1', '停下来思考', 'story_144_3', '', 1, 0, 0, 0, 0, 4),
('story_144_1', '观察周围情况', 'story_144_4', '', 1, 0, 0, 0, 0, 6),
('story_144_2', '继续前进', 'story_144_3', '', 1, 0, 0, 0, 0, 5),
('story_144_2', '停下来思考', 'story_144_4', '', 1, 0, 0, 0, 0, 4),
('story_144_2', '观察周围情况', 'story_144_5', '', 1, 0, 0, 0, 0, 6),
('story_144_3', '继续前进', 'story_144_4', '', 1, 0, 0, 0, 0, 5),
('story_144_3', '停下来思考', 'story_144_5', '', 1, 0, 0, 0, 0, 4),
('story_144_3', '观察周围情况', 'story_144_6', '', 1, 0, 0, 0, 0, 6),
('story_144_4', '继续前进', 'story_144_5', '', 1, 0, 0, 0, 0, 5),
('story_144_4', '停下来思考', 'story_144_6', '', 1, 0, 0, 0, 0, 4),
('story_144_4', '观察周围情况', 'story_144_7', '', 1, 0, 0, 0, 0, 6),
('story_144_5', '继续前进', 'story_144_6', '', 1, 0, 0, 0, 0, 5),
('story_144_5', '停下来思考', 'story_144_7', '', 1, 0, 0, 0, 0, 4),
('story_144_5', '观察周围情况', 'story_144_8', '', 1, 0, 0, 0, 0, 6),
('story_144_6', '继续前进', 'story_144_7', '', 1, 0, 0, 0, 0, 5),
('story_144_6', '停下来思考', 'story_144_8', '', 1, 0, 0, 0, 0, 4),
('story_144_6', '观察周围情况', 'story_144_9', '', 1, 0, 0, 0, 0, 6),
('story_144_7', '继续前进', 'story_144_8', '', 1, 0, 0, 0, 0, 5),
('story_144_7', '停下来思考', 'story_144_9', '', 1, 0, 0, 0, 0, 4),
('story_144_7', '观察周围情况', 'story_144_10', '', 1, 0, 0, 0, 0, 6),
('story_144_8', '继续前进', 'story_144_9', '', 1, 0, 0, 0, 0, 5),
('story_144_8', '停下来思考', 'story_144_10', '', 1, 0, 0, 0, 0, 4),
('story_144_8', '观察周围情况', 'story_145_1', '', 1, 0, 0, 0, 0, 6),
('story_144_8', '探索新的方向', 'story_144_11', '', 1, 0, 0, 0, 0, 7),
('story_144_9', '继续前进', 'story_144_10', '', 1, 0, 0, 0, 0, 5),
('story_144_9', '停下来思考', 'story_145_1', '', 1, 0, 0, 0, 0, 4),
('story_144_9', '观察周围情况', 'story_145_1', '', 1, 0, 0, 0, 0, 6),
('story_144_9', '探索新的方向', 'story_144_12', '', 1, 0, 0, 0, 0, 7),
('story_144_10', '继续前进', 'story_145_1', '', 1, 0, 0, 0, 0, 5),
('story_144_10', '停下来思考', 'story_145_1', '', 1, 0, 0, 0, 0, 4),
('story_144_10', '观察周围情况', 'story_145_1', '', 1, 0, 0, 0, 0, 6),
('story_144_10', '探索新的方向', 'story_144_12', '', 1, 0, 0, 0, 0, 7),
('story_144_11', '继续前进', 'story_145_1', '', 1, 0, 0, 0, 0, 5),
('story_144_11', '停下来思考', 'story_145_1', '', 1, 0, 0, 0, 0, 4),
('story_144_11', '观察周围情况', 'story_145_1', '', 1, 0, 0, 0, 0, 6),
('story_144_12', '继续前进', 'story_145_1', '', 1, 0, 0, 0, 0, 5),
('story_144_12', '停下来思考', 'story_145_1', '', 1, 0, 0, 0, 0, 4),
('story_144_12', '观察周围情况', 'story_145_1', '', 1, 0, 0, 0, 0, 6),
('story_145_1', '检查获得的物品', 'story_145_2', '', 1, 0, 0, 0, 0, 7),
('story_145_1', '继续探索', 'story_145_3', '', 1, 0, 0, 0, 0, 5),
('story_145_2', '与其他人交流', 'story_145_3', '', 1, 0, 0, 0, 0, 6),
('story_145_2', '继续探索', 'story_145_4', '', 1, 0, 0, 0, 0, 5),
('story_145_3', '继续前进', 'story_145_4', '', 1, 0, 0, 0, 0, 5),
('story_145_3', '停下来思考', 'story_145_5', '', 1, 0, 0, 0, 0, 4),
('story_145_3', '观察周围情况', 'story_145_6', '', 1, 0, 0, 0, 0, 6),
('story_145_4', '继续前进', 'story_145_5', '', 1, 0, 0, 0, 0, 5),
('story_145_4', '停下来思考', 'story_145_6', '', 1, 0, 0, 0, 0, 4),
('story_145_4', '观察周围情况', 'story_145_7', '', 1, 0, 0, 0, 0, 6),
('story_145_5', '继续前进', 'story_145_6', '', 1, 0, 0, 0, 0, 5),
('story_145_5', '停下来思考', 'story_145_7', '', 1, 0, 0, 0, 0, 4),
('story_145_5', '观察周围情况', 'story_145_8', '', 1, 0, 0, 0, 0, 6),
('story_145_6', '与其他人交流', 'story_145_7', '', 1, 0, 0, 0, 0, 6),
('story_145_6', '继续探索', 'story_145_8', '', 1, 0, 0, 0, 0, 5),
('story_145_7', '继续前进', 'story_145_8', '', 1, 0, 0, 0, 0, 5),
('story_145_7', '停下来思考', 'story_145_9', '', 1, 0, 0, 0, 0, 4),
('story_145_7', '观察周围情况', 'story_145_10', '', 1, 0, 0, 0, 0, 6),
('story_145_8', '与其他人交流', 'story_145_9', '', 1, 0, 0, 0, 0, 6),
('story_145_8', '继续探索', 'story_145_10', '', 1, 0, 0, 0, 0, 5),
('story_145_8', '探索新的方向', 'story_145_11', '', 1, 0, 0, 0, 0, 7),
('story_145_9', '继续前进', 'story_145_10', '', 1, 0, 0, 0, 0, 5),
('story_145_9', '停下来思考', 'story_146_1', '', 1, 0, 0, 0, 0, 4),
('story_145_9', '观察周围情况', 'story_146_1', '', 1, 0, 0, 0, 0, 6),
('story_145_9', '探索新的方向', 'story_145_11', '', 1, 0, 0, 0, 0, 7),
('story_145_10', '继续前进', 'story_146_1', '', 1, 0, 0, 0, 0, 5),
('story_145_10', '停下来思考', 'story_146_1', '', 1, 0, 0, 0, 0, 4),
('story_145_10', '观察周围情况', 'story_146_1', '', 1, 0, 0, 0, 0, 6),
('story_145_11', '继续前进', 'story_146_1', '', 1, 0, 0, 0, 0, 5),
('story_145_11', '停下来思考', 'story_146_1', '', 1, 0, 0, 0, 0, 4),
('story_145_11', '观察周围情况', 'story_146_1', '', 1, 0, 0, 0, 0, 6),
('story_146_1', '与其他人交流', 'story_146_2', '', 1, 0, 0, 0, 0, 6),
('story_146_1', '继续探索', 'story_146_3', '', 1, 0, 0, 0, 0, 5),
('story_146_2', '继续前进', 'story_146_3', '', 1, 0, 0, 0, 0, 5),
('story_146_2', '停下来思考', 'story_146_4', '', 1, 0, 0, 0, 0, 4),
('story_146_2', '观察周围情况', 'story_146_5', '', 1, 0, 0, 0, 0, 6),
('story_146_3', '与其他人交流', 'story_146_4', '', 1, 0, 0, 0, 0, 6),
('story_146_3', '继续探索', 'story_146_5', '', 1, 0, 0, 0, 0, 5),
('story_146_4', '继续前进', 'story_146_5', '', 1, 0, 0, 0, 0, 5),
('story_146_4', '停下来思考', 'story_146_6', '', 1, 0, 0, 0, 0, 4),
('story_146_4', '观察周围情况', 'story_146_7', '', 1, 0, 0, 0, 0, 6),
('story_146_5', '继续前进', 'story_146_6', '', 1, 0, 0, 0, 0, 5),
('story_146_5', '停下来思考', 'story_146_7', '', 1, 0, 0, 0, 0, 4),
('story_146_5', '观察周围情况', 'story_146_8', '', 1, 0, 0, 0, 0, 6),
('story_146_6', '继续前进', 'story_146_7', '', 1, 0, 0, 0, 0, 5),
('story_146_6', '停下来思考', 'story_146_8', '', 1, 0, 0, 0, 0, 4),
('story_146_6', '观察周围情况', 'story_146_9', '', 1, 0, 0, 0, 0, 6),
('story_146_7', '继续前进', 'story_146_8', '', 1, 0, 0, 0, 0, 5),
('story_146_7', '停下来思考', 'story_146_9', '', 1, 0, 0, 0, 0, 4),
('story_146_7', '观察周围情况', 'story_146_10', '', 1, 0, 0, 0, 0, 6),
('story_146_8', '继续前进', 'story_146_9', '', 1, 0, 0, 0, 0, 5),
('story_146_8', '停下来思考', 'story_146_10', '', 1, 0, 0, 0, 0, 4),
('story_146_8', '观察周围情况', 'story_147_1', '', 1, 0, 0, 0, 0, 6),
('story_146_9', '继续前进', 'story_146_10', '', 1, 0, 0, 0, 0, 5),
('story_146_9', '停下来思考', 'story_147_1', '', 1, 0, 0, 0, 0, 4),
('story_146_9', '观察周围情况', 'story_147_1', '', 1, 0, 0, 0, 0, 6),
('story_146_10', '继续前进', 'story_147_1', '', 1, 0, 0, 0, 0, 5),
('story_146_10', '停下来思考', 'story_147_1', '', 1, 0, 0, 0, 0, 4),
('story_146_10', '观察周围情况', 'story_147_1', '', 1, 0, 0, 0, 0, 6),
('story_147_1', '继续前进', 'story_147_2', '', 1, 0, 0, 0, 0, 5),
('story_147_1', '停下来思考', 'story_147_3', '', 1, 0, 0, 0, 0, 4),
('story_147_1', '观察周围情况', 'story_147_4', '', 1, 0, 0, 0, 0, 6),
('story_147_2', '继续前进', 'story_147_3', '', 1, 0, 0, 0, 0, 5),
('story_147_2', '停下来思考', 'story_147_4', '', 1, 0, 0, 0, 0, 4),
('story_147_2', '观察周围情况', 'story_147_5', '', 1, 0, 0, 0, 0, 6),
('story_147_3', '继续前进', 'story_147_4', '', 1, 0, 0, 0, 0, 5),
('story_147_3', '停下来思考', 'story_147_5', '', 1, 0, 0, 0, 0, 4),
('story_147_3', '观察周围情况', 'story_147_6', '', 1, 0, 0, 0, 0, 6),
('story_147_4', '与其他人交流', 'story_147_5', '', 1, 0, 0, 0, 0, 6),
('story_147_4', '检查获得的物品', 'story_147_6', '', 1, 0, 0, 0, 0, 7),
('story_147_5', '继续前进', 'story_147_6', '', 1, 0, 0, 0, 0, 5),
('story_147_5', '停下来思考', 'story_147_7', '', 1, 0, 0, 0, 0, 4),
('story_147_5', '观察周围情况', 'story_147_8', '', 1, 0, 0, 0, 0, 6),
('story_147_6', '继续前进', 'story_147_7', '', 1, 0, 0, 0, 0, 5),
('story_147_6', '停下来思考', 'story_147_8', '', 1, 0, 0, 0, 0, 4),
('story_147_6', '观察周围情况', 'story_147_9', '', 1, 0, 0, 0, 0, 6),
('story_147_7', '继续前进', 'story_147_8', '', 1, 0, 0, 0, 0, 5),
('story_147_7', '停下来思考', 'story_147_9', '', 1, 0, 0, 0, 0, 4),
('story_147_7', '观察周围情况', 'story_147_10', '', 1, 0, 0, 0, 0, 6),
('story_147_8', '继续前进', 'story_147_9', '', 1, 0, 0, 0, 0, 5),
('story_147_8', '停下来思考', 'story_147_10', '', 1, 0, 0, 0, 0, 4),
('story_147_8', '观察周围情况', 'story_148_1', '', 1, 0, 0, 0, 0, 6),
('story_147_9', '继续前进', 'story_147_10', '', 1, 0, 0, 0, 0, 5),
('story_147_9', '停下来思考', 'story_148_1', '', 1, 0, 0, 0, 0, 4),
('story_147_9', '观察周围情况', 'story_148_1', '', 1, 0, 0, 0, 0, 6),
('story_147_10', '继续前进', 'story_148_1', '', 1, 0, 0, 0, 0, 5),
('story_147_10', '停下来思考', 'story_148_1', '', 1, 0, 0, 0, 0, 4),
('story_147_10', '观察周围情况', 'story_148_1', '', 1, 0, 0, 0, 0, 6),
('story_148_1', '继续前进', 'story_148_2', '', 1, 0, 0, 0, 0, 5),
('story_148_1', '停下来思考', 'story_148_3', '', 1, 0, 0, 0, 0, 4),
('story_148_1', '观察周围情况', 'story_148_4', '', 1, 0, 0, 0, 0, 6),
('story_148_2', '仔细探索周围环境', 'story_148_3', '', 1, 0, 0, 0, 0, 8),
('story_148_2', '继续探索', 'story_148_4', '', 1, 0, 0, 0, 0, 5),
('story_148_3', '继续前进', 'story_148_4', '', 1, 0, 0, 0, 0, 5),
('story_148_3', '停下来思考', 'story_148_5', '', 1, 0, 0, 0, 0, 4),
('story_148_3', '观察周围情况', 'story_148_6', '', 1, 0, 0, 0, 0, 6),
('story_148_4', '继续前进', 'story_148_5', '', 1, 0, 0, 0, 0, 5),
('story_148_4', '停下来思考', 'story_148_6', '', 1, 0, 0, 0, 0, 4),
('story_148_4', '观察周围情况', 'story_148_7', '', 1, 0, 0, 0, 0, 6),
('story_148_5', '与其他人交流', 'story_148_6', '', 1, 0, 0, 0, 0, 6),
('story_148_5', '继续探索', 'story_148_7', '', 1, 0, 0, 0, 0, 5),
('story_148_6', '与其他人交流', 'story_148_7', '', 1, 0, 0, 0, 0, 6),
('story_148_6', '继续探索', 'story_148_8', '', 1, 0, 0, 0, 0, 5),
('story_148_7', '继续前进', 'story_148_8', '', 1, 0, 0, 0, 0, 5),
('story_148_7', '停下来思考', 'story_148_9', '', 1, 0, 0, 0, 0, 4),
('story_148_7', '观察周围情况', 'story_148_10', '', 1, 0, 0, 0, 0, 6),
('story_148_8', '与其他人交流', 'story_148_9', '', 1, 0, 0, 0, 0, 6),
('story_148_8', '继续探索', 'story_148_10', '', 1, 0, 0, 0, 0, 5),
('story_148_9', '继续前进', 'story_148_10', '', 1, 0, 0, 0, 0, 5),
('story_148_9', '停下来思考', 'story_149_1', '', 1, 0, 0, 0, 0, 4),
('story_148_9', '观察周围情况', 'story_149_1', '', 1, 0, 0, 0, 0, 6),
('story_148_10', '继续前进', 'story_149_1', '', 1, 0, 0, 0, 0, 5),
('story_148_10', '停下来思考', 'story_149_1', '', 1, 0, 0, 0, 0, 4),
('story_148_10', '观察周围情况', 'story_149_1', '', 1, 0, 0, 0, 0, 6),
('story_149_1', '继续前进', 'story_149_2', '', 1, 0, 0, 0, 0, 5),
('story_149_1', '停下来思考', 'story_149_3', '', 1, 0, 0, 0, 0, 4),
('story_149_1', '观察周围情况', 'story_149_4', '', 1, 0, 0, 0, 0, 6),
('story_149_1', '探索新的方向', 'story_150_12', '', 1, 0, 0, 0, 0, 7),
('story_149_2', '继续前进', 'story_149_3', '', 1, 0, 0, 0, 0, 5),
('story_149_2', '停下来思考', 'story_149_4', '', 1, 0, 0, 0, 0, 4),
('story_149_2', '观察周围情况', 'story_149_5', '', 1, 0, 0, 0, 0, 6),
('story_149_2', '探索新的方向', 'story_150_12', '', 1, 0, 0, 0, 0, 7),
('story_149_3', '继续前进', 'story_149_4', '', 1, 0, 0, 0, 0, 5),
('story_149_3', '停下来思考', 'story_149_5', '', 1, 0, 0, 0, 0, 4),
('story_149_3', '观察周围情况', 'story_149_6', '', 1, 0, 0, 0, 0, 6),
('story_149_4', '继续前进', 'story_149_5', '', 1, 0, 0, 0, 0, 5),
('story_149_4', '停下来思考', 'story_149_6', '', 1, 0, 0, 0, 0, 4),
('story_149_4', '观察周围情况', 'story_149_7', '', 1, 0, 0, 0, 0, 6),
('story_149_5', '继续前进', 'story_149_6', '', 1, 0, 0, 0, 0, 5),
('story_149_5', '停下来思考', 'story_149_7', '', 1, 0, 0, 0, 0, 4),
('story_149_5', '观察周围情况', 'story_149_8', '', 1, 0, 0, 0, 0, 6),
('story_149_6', '继续前进', 'story_149_7', '', 1, 0, 0, 0, 0, 5);

-- 批次统计
-- 本批次选择数: 500
-- 批次范围: 5001 - 5500
