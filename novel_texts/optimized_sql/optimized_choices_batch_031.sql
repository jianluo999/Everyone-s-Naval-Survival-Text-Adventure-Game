-- 优化选择数据批次 31
-- 清理现有数据（仅第一批次）
INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES
('story_432_7', '停下来思考', 'story_432_9', '', 1, 0, 0, 0, 0, 4),
('story_432_7', '观察周围情况', 'story_432_10', '', 1, 0, 0, 0, 0, 6),
('story_432_8', '继续前进', 'story_432_9', '', 1, 0, 0, 0, 0, 5),
('story_432_8', '停下来思考', 'story_432_10', '', 1, 0, 0, 0, 0, 4),
('story_432_8', '观察周围情况', 'story_433_1', '', 1, 0, 0, 0, 0, 6),
('story_432_8', '探索新的方向', 'story_432_11', '', 1, 0, 0, 0, 0, 7),
('story_432_9', '继续前进', 'story_432_10', '', 1, 0, 0, 0, 0, 5),
('story_432_9', '停下来思考', 'story_433_1', '', 1, 0, 0, 0, 0, 4),
('story_432_9', '观察周围情况', 'story_433_1', '', 1, 0, 0, 0, 0, 6),
('story_432_9', '探索新的方向', 'story_432_12', '', 1, 0, 0, 0, 0, 7),
('story_432_10', '继续前进', 'story_433_1', '', 1, 0, 0, 0, 0, 5),
('story_432_10', '停下来思考', 'story_433_1', '', 1, 0, 0, 0, 0, 4),
('story_432_10', '观察周围情况', 'story_433_1', '', 1, 0, 0, 0, 0, 6),
('story_432_10', '探索新的方向', 'story_432_12', '', 1, 0, 0, 0, 0, 7),
('story_432_11', '继续前进', 'story_433_1', '', 1, 0, 0, 0, 0, 5),
('story_432_11', '停下来思考', 'story_433_1', '', 1, 0, 0, 0, 0, 4),
('story_432_11', '观察周围情况', 'story_433_1', '', 1, 0, 0, 0, 0, 6),
('story_432_12', '与其他人交流', 'story_433_1', '', 1, 0, 0, 0, 0, 6),
('story_432_12', '继续探索', 'story_433_1', '', 1, 0, 0, 0, 0, 5),
('story_433_1', '继续前进', 'story_433_2', '', 1, 0, 0, 0, 0, 5),
('story_433_1', '停下来思考', 'story_433_3', '', 1, 0, 0, 0, 0, 4),
('story_433_1', '观察周围情况', 'story_433_4', '', 1, 0, 0, 0, 0, 6),
('story_433_2', '继续前进', 'story_433_3', '', 1, 0, 0, 0, 0, 5),
('story_433_2', '停下来思考', 'story_433_4', '', 1, 0, 0, 0, 0, 4),
('story_433_2', '观察周围情况', 'story_433_5', '', 1, 0, 0, 0, 0, 6),
('story_433_3', '继续前进', 'story_433_4', '', 1, 0, 0, 0, 0, 5),
('story_433_3', '停下来思考', 'story_433_5', '', 1, 0, 0, 0, 0, 4),
('story_433_3', '观察周围情况', 'story_433_6', '', 1, 0, 0, 0, 0, 6),
('story_433_4', '继续前进', 'story_433_5', '', 1, 0, 0, 0, 0, 5),
('story_433_4', '停下来思考', 'story_433_6', '', 1, 0, 0, 0, 0, 4),
('story_433_4', '观察周围情况', 'story_433_7', '', 1, 0, 0, 0, 0, 6),
('story_433_5', '继续前进', 'story_433_6', '', 1, 0, 0, 0, 0, 5),
('story_433_5', '停下来思考', 'story_433_7', '', 1, 0, 0, 0, 0, 4),
('story_433_5', '观察周围情况', 'story_433_8', '', 1, 0, 0, 0, 0, 6),
('story_433_6', '继续前进', 'story_433_7', '', 1, 0, 0, 0, 0, 5),
('story_433_6', '停下来思考', 'story_433_8', '', 1, 0, 0, 0, 0, 4),
('story_433_6', '观察周围情况', 'story_433_9', '', 1, 0, 0, 0, 0, 6),
('story_433_7', '继续前进', 'story_433_8', '', 1, 0, 0, 0, 0, 5),
('story_433_7', '停下来思考', 'story_433_9', '', 1, 0, 0, 0, 0, 4),
('story_433_7', '观察周围情况', 'story_433_10', '', 1, 0, 0, 0, 0, 6),
('story_433_8', '继续前进', 'story_433_9', '', 1, 0, 0, 0, 0, 5),
('story_433_8', '停下来思考', 'story_433_10', '', 1, 0, 0, 0, 0, 4),
('story_433_8', '观察周围情况', 'story_434_1', '', 1, 0, 0, 0, 0, 6),
('story_433_9', '继续前进', 'story_433_10', '', 1, 0, 0, 0, 0, 5),
('story_433_9', '停下来思考', 'story_434_1', '', 1, 0, 0, 0, 0, 4),
('story_433_9', '观察周围情况', 'story_434_1', '', 1, 0, 0, 0, 0, 6),
('story_433_10', '继续前进', 'story_434_1', '', 1, 0, 0, 0, 0, 5),
('story_433_10', '停下来思考', 'story_434_1', '', 1, 0, 0, 0, 0, 4),
('story_433_10', '观察周围情况', 'story_434_1', '', 1, 0, 0, 0, 0, 6),
('story_434_1', '继续前进', 'story_434_2', '', 1, 0, 0, 0, 0, 5),
('story_434_1', '停下来思考', 'story_434_3', '', 1, 0, 0, 0, 0, 4),
('story_434_1', '观察周围情况', 'story_434_4', '', 1, 0, 0, 0, 0, 6),
('story_434_2', '继续前进', 'story_434_3', '', 1, 0, 0, 0, 0, 5),
('story_434_2', '停下来思考', 'story_434_4', '', 1, 0, 0, 0, 0, 4),
('story_434_2', '观察周围情况', 'story_434_5', '', 1, 0, 0, 0, 0, 6),
('story_434_3', '继续前进', 'story_434_4', '', 1, 0, 0, 0, 0, 5),
('story_434_3', '停下来思考', 'story_434_5', '', 1, 0, 0, 0, 0, 4),
('story_434_3', '观察周围情况', 'story_434_6', '', 1, 0, 0, 0, 0, 6),
('story_434_4', '继续前进', 'story_434_5', '', 1, 0, 0, 0, 0, 5),
('story_434_4', '停下来思考', 'story_434_6', '', 1, 0, 0, 0, 0, 4),
('story_434_4', '观察周围情况', 'story_434_7', '', 1, 0, 0, 0, 0, 6),
('story_434_5', '继续前进', 'story_434_6', '', 1, 0, 0, 0, 0, 5),
('story_434_5', '停下来思考', 'story_434_7', '', 1, 0, 0, 0, 0, 4),
('story_434_5', '观察周围情况', 'story_434_8', '', 1, 0, 0, 0, 0, 6),
('story_434_6', '继续前进', 'story_434_7', '', 1, 0, 0, 0, 0, 5),
('story_434_6', '停下来思考', 'story_434_8', '', 1, 0, 0, 0, 0, 4),
('story_434_6', '观察周围情况', 'story_434_9', '', 1, 0, 0, 0, 0, 6),
('story_434_7', '继续前进', 'story_434_8', '', 1, 0, 0, 0, 0, 5),
('story_434_7', '停下来思考', 'story_434_9', '', 1, 0, 0, 0, 0, 4),
('story_434_7', '观察周围情况', 'story_434_10', '', 1, 0, 0, 0, 0, 6),
('story_434_8', '继续前进', 'story_434_9', '', 1, 0, 0, 0, 0, 5),
('story_434_8', '停下来思考', 'story_434_10', '', 1, 0, 0, 0, 0, 4),
('story_434_8', '观察周围情况', 'story_435_1', '', 1, 0, 0, 0, 0, 6),
('story_434_8', '探索新的方向', 'story_434_11', '', 1, 0, 0, 0, 0, 7),
('story_434_9', '与其他人交流', 'story_434_10', '', 1, 0, 0, 0, 0, 6),
('story_434_9', '继续探索', 'story_435_1', '', 1, 0, 0, 0, 0, 5),
('story_434_9', '探索新的方向', 'story_434_11', '', 1, 0, 0, 0, 0, 7),
('story_434_9', '探索新的方向', 'story_434_12', '', 1, 0, 0, 0, 0, 7),
('story_434_10', '检查获得的物品', 'story_435_1', '', 1, 0, 0, 0, 0, 7),
('story_434_10', '继续探索', 'story_435_1', '', 1, 0, 0, 0, 0, 5),
('story_434_10', '探索新的方向', 'story_434_12', '', 1, 0, 0, 0, 0, 7),
('story_434_11', '继续前进', 'story_435_1', '', 1, 0, 0, 0, 0, 5),
('story_434_11', '停下来思考', 'story_435_1', '', 1, 0, 0, 0, 0, 4),
('story_434_11', '观察周围情况', 'story_435_1', '', 1, 0, 0, 0, 0, 6),
('story_434_12', '继续前进', 'story_435_1', '', 1, 0, 0, 0, 0, 5),
('story_434_12', '停下来思考', 'story_435_1', '', 1, 0, 0, 0, 0, 4),
('story_434_12', '观察周围情况', 'story_435_1', '', 1, 0, 0, 0, 0, 6),
('story_435_1', '检查获得的物品', 'story_435_2', '', 1, 0, 0, 0, 0, 7),
('story_435_1', '继续探索', 'story_435_3', '', 1, 0, 0, 0, 0, 5),
('story_435_2', '检查获得的物品', 'story_435_3', '', 1, 0, 0, 0, 0, 7),
('story_435_2', '继续探索', 'story_435_4', '', 1, 0, 0, 0, 0, 5),
('story_435_3', '检查获得的物品', 'story_435_4', '', 1, 0, 0, 0, 0, 7),
('story_435_3', '继续探索', 'story_435_5', '', 1, 0, 0, 0, 0, 5),
('story_435_4', '继续前进', 'story_435_5', '', 1, 0, 0, 0, 0, 5),
('story_435_4', '停下来思考', 'story_435_6', '', 1, 0, 0, 0, 0, 4),
('story_435_4', '观察周围情况', 'story_435_7', '', 1, 0, 0, 0, 0, 6),
('story_435_5', '继续前进', 'story_435_6', '', 1, 0, 0, 0, 0, 5),
('story_435_5', '停下来思考', 'story_435_7', '', 1, 0, 0, 0, 0, 4),
('story_435_5', '观察周围情况', 'story_435_8', '', 1, 0, 0, 0, 0, 6),
('story_435_6', '继续前进', 'story_435_7', '', 1, 0, 0, 0, 0, 5),
('story_435_6', '停下来思考', 'story_435_8', '', 1, 0, 0, 0, 0, 4),
('story_435_6', '观察周围情况', 'story_435_9', '', 1, 0, 0, 0, 0, 6),
('story_435_7', '继续前进', 'story_435_8', '', 1, 0, 0, 0, 0, 5),
('story_435_7', '停下来思考', 'story_435_9', '', 1, 0, 0, 0, 0, 4),
('story_435_7', '观察周围情况', 'story_435_10', '', 1, 0, 0, 0, 0, 6),
('story_435_8', '继续前进', 'story_435_9', '', 1, 0, 0, 0, 0, 5),
('story_435_8', '停下来思考', 'story_435_10', '', 1, 0, 0, 0, 0, 4),
('story_435_8', '观察周围情况', 'story_436_1', '', 1, 0, 0, 0, 0, 6),
('story_435_9', '继续前进', 'story_435_10', '', 1, 0, 0, 0, 0, 5),
('story_435_9', '停下来思考', 'story_436_1', '', 1, 0, 0, 0, 0, 4),
('story_435_9', '观察周围情况', 'story_436_1', '', 1, 0, 0, 0, 0, 6),
('story_435_10', '继续前进', 'story_436_1', '', 1, 0, 0, 0, 0, 5),
('story_435_10', '停下来思考', 'story_436_1', '', 1, 0, 0, 0, 0, 4),
('story_435_10', '观察周围情况', 'story_436_1', '', 1, 0, 0, 0, 0, 6),
('story_436_1', '继续前进', 'story_436_2', '', 1, 0, 0, 0, 0, 5),
('story_436_1', '停下来思考', 'story_436_3', '', 1, 0, 0, 0, 0, 4),
('story_436_1', '观察周围情况', 'story_436_4', '', 1, 0, 0, 0, 0, 6),
('story_436_2', '继续前进', 'story_436_3', '', 1, 0, 0, 0, 0, 5),
('story_436_2', '停下来思考', 'story_436_4', '', 1, 0, 0, 0, 0, 4),
('story_436_2', '观察周围情况', 'story_436_5', '', 1, 0, 0, 0, 0, 6),
('story_436_3', '继续前进', 'story_436_4', '', 1, 0, 0, 0, 0, 5),
('story_436_3', '停下来思考', 'story_436_5', '', 1, 0, 0, 0, 0, 4),
('story_436_3', '观察周围情况', 'story_436_6', '', 1, 0, 0, 0, 0, 6),
('story_436_4', '继续前进', 'story_436_5', '', 1, 0, 0, 0, 0, 5),
('story_436_4', '停下来思考', 'story_436_6', '', 1, 0, 0, 0, 0, 4),
('story_436_4', '观察周围情况', 'story_436_7', '', 1, 0, 0, 0, 0, 6),
('story_436_5', '继续前进', 'story_436_6', '', 1, 0, 0, 0, 0, 5),
('story_436_5', '停下来思考', 'story_436_7', '', 1, 0, 0, 0, 0, 4),
('story_436_5', '观察周围情况', 'story_436_8', '', 1, 0, 0, 0, 0, 6),
('story_436_6', '继续前进', 'story_436_7', '', 1, 0, 0, 0, 0, 5),
('story_436_6', '停下来思考', 'story_436_8', '', 1, 0, 0, 0, 0, 4),
('story_436_6', '观察周围情况', 'story_436_9', '', 1, 0, 0, 0, 0, 6),
('story_436_7', '继续前进', 'story_436_8', '', 1, 0, 0, 0, 0, 5),
('story_436_7', '停下来思考', 'story_436_9', '', 1, 0, 0, 0, 0, 4),
('story_436_7', '观察周围情况', 'story_436_10', '', 1, 0, 0, 0, 0, 6),
('story_436_8', '继续前进', 'story_436_9', '', 1, 0, 0, 0, 0, 5),
('story_436_8', '停下来思考', 'story_436_10', '', 1, 0, 0, 0, 0, 4),
('story_436_8', '观察周围情况', 'story_437_1', '', 1, 0, 0, 0, 0, 6),
('story_436_9', '继续前进', 'story_436_10', '', 1, 0, 0, 0, 0, 5),
('story_436_9', '停下来思考', 'story_437_1', '', 1, 0, 0, 0, 0, 4),
('story_436_9', '观察周围情况', 'story_437_1', '', 1, 0, 0, 0, 0, 6),
('story_436_10', '继续前进', 'story_437_1', '', 1, 0, 0, 0, 0, 5),
('story_436_10', '停下来思考', 'story_437_1', '', 1, 0, 0, 0, 0, 4),
('story_436_10', '观察周围情况', 'story_437_1', '', 1, 0, 0, 0, 0, 6),
('story_437_1', '继续前进', 'story_437_2', '', 1, 0, 0, 0, 0, 5),
('story_437_1', '停下来思考', 'story_437_3', '', 1, 0, 0, 0, 0, 4),
('story_437_1', '观察周围情况', 'story_437_4', '', 1, 0, 0, 0, 0, 6),
('story_437_2', '继续前进', 'story_437_3', '', 1, 0, 0, 0, 0, 5),
('story_437_2', '停下来思考', 'story_437_4', '', 1, 0, 0, 0, 0, 4),
('story_437_2', '观察周围情况', 'story_437_5', '', 1, 0, 0, 0, 0, 6),
('story_437_3', '继续前进', 'story_437_4', '', 1, 0, 0, 0, 0, 5),
('story_437_3', '停下来思考', 'story_437_5', '', 1, 0, 0, 0, 0, 4),
('story_437_3', '观察周围情况', 'story_437_6', '', 1, 0, 0, 0, 0, 6),
('story_437_4', '继续前进', 'story_437_5', '', 1, 0, 0, 0, 0, 5),
('story_437_4', '停下来思考', 'story_437_6', '', 1, 0, 0, 0, 0, 4),
('story_437_4', '观察周围情况', 'story_437_7', '', 1, 0, 0, 0, 0, 6),
('story_437_5', '继续前进', 'story_437_6', '', 1, 0, 0, 0, 0, 5),
('story_437_5', '停下来思考', 'story_437_7', '', 1, 0, 0, 0, 0, 4),
('story_437_5', '观察周围情况', 'story_437_8', '', 1, 0, 0, 0, 0, 6),
('story_437_6', '继续前进', 'story_437_7', '', 1, 0, 0, 0, 0, 5),
('story_437_6', '停下来思考', 'story_437_8', '', 1, 0, 0, 0, 0, 4),
('story_437_6', '观察周围情况', 'story_437_9', '', 1, 0, 0, 0, 0, 6),
('story_437_7', '继续前进', 'story_437_8', '', 1, 0, 0, 0, 0, 5),
('story_437_7', '停下来思考', 'story_437_9', '', 1, 0, 0, 0, 0, 4),
('story_437_7', '观察周围情况', 'story_437_10', '', 1, 0, 0, 0, 0, 6),
('story_437_8', '继续前进', 'story_437_9', '', 1, 0, 0, 0, 0, 5),
('story_437_8', '停下来思考', 'story_437_10', '', 1, 0, 0, 0, 0, 4),
('story_437_8', '观察周围情况', 'story_438_1', '', 1, 0, 0, 0, 0, 6),
('story_437_8', '探索新的方向', 'story_437_11', '', 1, 0, 0, 0, 0, 7),
('story_437_9', '继续前进', 'story_437_10', '', 1, 0, 0, 0, 0, 5),
('story_437_9', '停下来思考', 'story_438_1', '', 1, 0, 0, 0, 0, 4),
('story_437_9', '观察周围情况', 'story_438_1', '', 1, 0, 0, 0, 0, 6),
('story_437_9', '探索新的方向', 'story_437_12', '', 1, 0, 0, 0, 0, 7),
('story_437_10', '继续前进', 'story_438_1', '', 1, 0, 0, 0, 0, 5),
('story_437_10', '停下来思考', 'story_438_1', '', 1, 0, 0, 0, 0, 4),
('story_437_10', '观察周围情况', 'story_438_1', '', 1, 0, 0, 0, 0, 6),
('story_437_10', '探索新的方向', 'story_437_12', '', 1, 0, 0, 0, 0, 7),
('story_437_11', '继续前进', 'story_438_1', '', 1, 0, 0, 0, 0, 5),
('story_437_11', '停下来思考', 'story_438_1', '', 1, 0, 0, 0, 0, 4),
('story_437_11', '观察周围情况', 'story_438_1', '', 1, 0, 0, 0, 0, 6),
('story_437_11', '探索新的方向', 'story_437_13', '', 1, 0, 0, 0, 0, 7),
('story_437_12', '继续前进', 'story_438_1', '', 1, 0, 0, 0, 0, 5),
('story_437_12', '停下来思考', 'story_438_1', '', 1, 0, 0, 0, 0, 4),
('story_437_12', '观察周围情况', 'story_438_1', '', 1, 0, 0, 0, 0, 6),
('story_437_12', '探索新的方向', 'story_437_13', '', 1, 0, 0, 0, 0, 7),
('story_437_13', '继续前进', 'story_438_1', '', 1, 0, 0, 0, 0, 5),
('story_437_13', '停下来思考', 'story_438_1', '', 1, 0, 0, 0, 0, 4),
('story_437_13', '观察周围情况', 'story_438_1', '', 1, 0, 0, 0, 0, 6),
('story_438_1', '继续前进', 'story_438_2', '', 1, 0, 0, 0, 0, 5),
('story_438_1', '停下来思考', 'story_438_3', '', 1, 0, 0, 0, 0, 4),
('story_438_1', '观察周围情况', 'story_438_4', '', 1, 0, 0, 0, 0, 6),
('story_438_2', '继续前进', 'story_438_3', '', 1, 0, 0, 0, 0, 5),
('story_438_2', '停下来思考', 'story_438_4', '', 1, 0, 0, 0, 0, 4),
('story_438_2', '观察周围情况', 'story_438_5', '', 1, 0, 0, 0, 0, 6),
('story_438_3', '继续前进', 'story_438_4', '', 1, 0, 0, 0, 0, 5),
('story_438_3', '停下来思考', 'story_438_5', '', 1, 0, 0, 0, 0, 4),
('story_438_3', '观察周围情况', 'story_438_6', '', 1, 0, 0, 0, 0, 6),
('story_438_4', '检查获得的物品', 'story_438_5', '', 1, 0, 0, 0, 0, 7),
('story_438_4', '继续探索', 'story_438_6', '', 1, 0, 0, 0, 0, 5),
('story_438_5', '继续前进', 'story_438_6', '', 1, 0, 0, 0, 0, 5),
('story_438_5', '停下来思考', 'story_438_7', '', 1, 0, 0, 0, 0, 4),
('story_438_5', '观察周围情况', 'story_438_8', '', 1, 0, 0, 0, 0, 6),
('story_438_6', '继续前进', 'story_438_7', '', 1, 0, 0, 0, 0, 5),
('story_438_6', '停下来思考', 'story_438_8', '', 1, 0, 0, 0, 0, 4),
('story_438_6', '观察周围情况', 'story_438_9', '', 1, 0, 0, 0, 0, 6),
('story_438_7', '继续前进', 'story_438_8', '', 1, 0, 0, 0, 0, 5),
('story_438_7', '停下来思考', 'story_438_9', '', 1, 0, 0, 0, 0, 4),
('story_438_7', '观察周围情况', 'story_438_10', '', 1, 0, 0, 0, 0, 6),
('story_438_8', '仔细探索周围环境', 'story_438_9', '', 1, 0, 0, 0, 0, 8),
('story_438_8', '继续探索', 'story_438_10', '', 1, 0, 0, 0, 0, 5),
('story_438_8', '探索新的方向', 'story_438_11', '', 1, 0, 0, 0, 0, 7),
('story_438_9', '继续前进', 'story_438_10', '', 1, 0, 0, 0, 0, 5),
('story_438_9', '停下来思考', 'story_439_1', '', 1, 0, 0, 0, 0, 4),
('story_438_9', '观察周围情况', 'story_439_1', '', 1, 0, 0, 0, 0, 6),
('story_438_9', '探索新的方向', 'story_438_12', '', 1, 0, 0, 0, 0, 7),
('story_438_10', '继续前进', 'story_439_1', '', 1, 0, 0, 0, 0, 5),
('story_438_10', '停下来思考', 'story_439_1', '', 1, 0, 0, 0, 0, 4),
('story_438_10', '观察周围情况', 'story_439_1', '', 1, 0, 0, 0, 0, 6),
('story_438_10', '探索新的方向', 'story_438_12', '', 1, 0, 0, 0, 0, 7),
('story_438_11', '继续前进', 'story_439_1', '', 1, 0, 0, 0, 0, 5),
('story_438_11', '停下来思考', 'story_439_1', '', 1, 0, 0, 0, 0, 4),
('story_438_11', '观察周围情况', 'story_439_1', '', 1, 0, 0, 0, 0, 6),
('story_438_11', '探索新的方向', 'story_438_13', '', 1, 0, 0, 0, 0, 7),
('story_438_12', '继续前进', 'story_439_1', '', 1, 0, 0, 0, 0, 5),
('story_438_12', '停下来思考', 'story_439_1', '', 1, 0, 0, 0, 0, 4),
('story_438_12', '观察周围情况', 'story_439_1', '', 1, 0, 0, 0, 0, 6),
('story_438_12', '探索新的方向', 'story_438_13', '', 1, 0, 0, 0, 0, 7),
('story_438_13', '继续前进', 'story_439_1', '', 1, 0, 0, 0, 0, 5),
('story_438_13', '停下来思考', 'story_439_1', '', 1, 0, 0, 0, 0, 4),
('story_438_13', '观察周围情况', 'story_439_1', '', 1, 0, 0, 0, 0, 6),
('story_438_13', '探索新的方向', 'story_438_14', '', 1, 0, 0, 0, 0, 7),
('story_438_14', '继续前进', 'story_439_1', '', 1, 0, 0, 0, 0, 5),
('story_438_14', '停下来思考', 'story_439_1', '', 1, 0, 0, 0, 0, 4),
('story_438_14', '观察周围情况', 'story_439_1', '', 1, 0, 0, 0, 0, 6),
('story_439_1', '继续前进', 'story_439_2', '', 1, 0, 0, 0, 0, 5),
('story_439_1', '停下来思考', 'story_439_3', '', 1, 0, 0, 0, 0, 4),
('story_439_1', '观察周围情况', 'story_439_4', '', 1, 0, 0, 0, 0, 6),
('story_439_2', '继续前进', 'story_439_3', '', 1, 0, 0, 0, 0, 5),
('story_439_2', '停下来思考', 'story_439_4', '', 1, 0, 0, 0, 0, 4),
('story_439_2', '观察周围情况', 'story_439_5', '', 1, 0, 0, 0, 0, 6),
('story_439_3', '继续前进', 'story_439_4', '', 1, 0, 0, 0, 0, 5),
('story_439_3', '停下来思考', 'story_439_5', '', 1, 0, 0, 0, 0, 4),
('story_439_3', '观察周围情况', 'story_439_6', '', 1, 0, 0, 0, 0, 6),
('story_439_4', '继续前进', 'story_439_5', '', 1, 0, 0, 0, 0, 5),
('story_439_4', '停下来思考', 'story_439_6', '', 1, 0, 0, 0, 0, 4),
('story_439_4', '观察周围情况', 'story_439_7', '', 1, 0, 0, 0, 0, 6),
('story_439_5', '仔细探索周围环境', 'story_439_6', '', 1, 0, 0, 0, 0, 8),
('story_439_5', '继续探索', 'story_439_7', '', 1, 0, 0, 0, 0, 5),
('story_439_6', '仔细探索周围环境', 'story_439_7', '', 1, 0, 0, 0, 0, 8),
('story_439_6', '继续探索', 'story_439_8', '', 1, 0, 0, 0, 0, 5),
('story_439_7', '继续前进', 'story_439_8', '', 1, 0, 0, 0, 0, 5),
('story_439_7', '停下来思考', 'story_439_9', '', 1, 0, 0, 0, 0, 4),
('story_439_7', '观察周围情况', 'story_439_10', '', 1, 0, 0, 0, 0, 6),
('story_439_8', '继续前进', 'story_439_9', '', 1, 0, 0, 0, 0, 5),
('story_439_8', '停下来思考', 'story_439_10', '', 1, 0, 0, 0, 0, 4),
('story_439_8', '观察周围情况', 'story_440_1', '', 1, 0, 0, 0, 0, 6),
('story_439_8', '探索新的方向', 'story_439_11', '', 1, 0, 0, 0, 0, 7),
('story_439_9', '继续前进', 'story_439_10', '', 1, 0, 0, 0, 0, 5),
('story_439_9', '停下来思考', 'story_440_1', '', 1, 0, 0, 0, 0, 4),
('story_439_9', '观察周围情况', 'story_440_1', '', 1, 0, 0, 0, 0, 6),
('story_439_9', '探索新的方向', 'story_439_12', '', 1, 0, 0, 0, 0, 7),
('story_439_10', '继续前进', 'story_440_1', '', 1, 0, 0, 0, 0, 5),
('story_439_10', '停下来思考', 'story_440_1', '', 1, 0, 0, 0, 0, 4),
('story_439_10', '观察周围情况', 'story_440_1', '', 1, 0, 0, 0, 0, 6),
('story_439_10', '探索新的方向', 'story_439_13', '', 1, 0, 0, 0, 0, 7),
('story_439_11', '继续前进', 'story_440_1', '', 1, 0, 0, 0, 0, 5),
('story_439_11', '停下来思考', 'story_440_1', '', 1, 0, 0, 0, 0, 4),
('story_439_11', '观察周围情况', 'story_440_1', '', 1, 0, 0, 0, 0, 6),
('story_439_11', '探索新的方向', 'story_439_13', '', 1, 0, 0, 0, 0, 7),
('story_439_12', '检查获得的物品', 'story_440_1', '', 1, 0, 0, 0, 0, 7),
('story_439_12', '继续探索', 'story_440_1', '', 1, 0, 0, 0, 0, 5),
('story_439_13', '继续前进', 'story_440_1', '', 1, 0, 0, 0, 0, 5),
('story_439_13', '停下来思考', 'story_440_1', '', 1, 0, 0, 0, 0, 4),
('story_439_13', '观察周围情况', 'story_440_1', '', 1, 0, 0, 0, 0, 6),
('story_440_1', '继续前进', 'story_440_2', '', 1, 0, 0, 0, 0, 5),
('story_440_1', '停下来思考', 'story_440_3', '', 1, 0, 0, 0, 0, 4),
('story_440_1', '观察周围情况', 'story_440_4', '', 1, 0, 0, 0, 0, 6),
('story_440_2', '继续前进', 'story_440_3', '', 1, 0, 0, 0, 0, 5),
('story_440_2', '停下来思考', 'story_440_4', '', 1, 0, 0, 0, 0, 4),
('story_440_2', '观察周围情况', 'story_440_5', '', 1, 0, 0, 0, 0, 6),
('story_440_3', '继续前进', 'story_440_4', '', 1, 0, 0, 0, 0, 5),
('story_440_3', '停下来思考', 'story_440_5', '', 1, 0, 0, 0, 0, 4),
('story_440_3', '观察周围情况', 'story_440_6', '', 1, 0, 0, 0, 0, 6),
('story_440_4', '仔细探索周围环境', 'story_440_5', '', 1, 0, 0, 0, 0, 8),
('story_440_4', '继续探索', 'story_440_6', '', 1, 0, 0, 0, 0, 5),
('story_440_5', '继续前进', 'story_440_6', '', 1, 0, 0, 0, 0, 5),
('story_440_5', '停下来思考', 'story_440_7', '', 1, 0, 0, 0, 0, 4),
('story_440_5', '观察周围情况', 'story_440_8', '', 1, 0, 0, 0, 0, 6),
('story_440_6', '继续前进', 'story_440_7', '', 1, 0, 0, 0, 0, 5),
('story_440_6', '停下来思考', 'story_440_8', '', 1, 0, 0, 0, 0, 4),
('story_440_6', '观察周围情况', 'story_440_9', '', 1, 0, 0, 0, 0, 6),
('story_440_7', '继续前进', 'story_440_8', '', 1, 0, 0, 0, 0, 5),
('story_440_7', '停下来思考', 'story_440_9', '', 1, 0, 0, 0, 0, 4),
('story_440_7', '观察周围情况', 'story_440_10', '', 1, 0, 0, 0, 0, 6),
('story_440_8', '检查获得的物品', 'story_440_9', '', 1, 0, 0, 0, 0, 7),
('story_440_8', '继续探索', 'story_440_10', '', 1, 0, 0, 0, 0, 5),
('story_440_8', '探索新的方向', 'story_440_11', '', 1, 0, 0, 0, 0, 7),
('story_440_9', '继续前进', 'story_440_10', '', 1, 0, 0, 0, 0, 5),
('story_440_9', '停下来思考', 'story_441_1', '', 1, 0, 0, 0, 0, 4),
('story_440_9', '观察周围情况', 'story_441_1', '', 1, 0, 0, 0, 0, 6),
('story_440_9', '探索新的方向', 'story_440_11', '', 1, 0, 0, 0, 0, 7),
('story_440_10', '继续前进', 'story_441_1', '', 1, 0, 0, 0, 0, 5),
('story_440_10', '停下来思考', 'story_441_1', '', 1, 0, 0, 0, 0, 4),
('story_440_10', '观察周围情况', 'story_441_1', '', 1, 0, 0, 0, 0, 6),
('story_440_11', '继续前进', 'story_441_1', '', 1, 0, 0, 0, 0, 5),
('story_440_11', '停下来思考', 'story_441_1', '', 1, 0, 0, 0, 0, 4),
('story_440_11', '观察周围情况', 'story_441_1', '', 1, 0, 0, 0, 0, 6),
('story_441_1', '继续前进', 'story_441_2', '', 1, 0, 0, 0, 0, 5),
('story_441_1', '停下来思考', 'story_441_3', '', 1, 0, 0, 0, 0, 4),
('story_441_1', '观察周围情况', 'story_441_4', '', 1, 0, 0, 0, 0, 6),
('story_441_2', '继续前进', 'story_441_3', '', 1, 0, 0, 0, 0, 5),
('story_441_2', '停下来思考', 'story_441_4', '', 1, 0, 0, 0, 0, 4),
('story_441_2', '观察周围情况', 'story_441_5', '', 1, 0, 0, 0, 0, 6),
('story_441_3', '继续前进', 'story_441_4', '', 1, 0, 0, 0, 0, 5),
('story_441_3', '停下来思考', 'story_441_5', '', 1, 0, 0, 0, 0, 4),
('story_441_3', '观察周围情况', 'story_441_6', '', 1, 0, 0, 0, 0, 6),
('story_441_4', '继续前进', 'story_441_5', '', 1, 0, 0, 0, 0, 5),
('story_441_4', '停下来思考', 'story_441_6', '', 1, 0, 0, 0, 0, 4),
('story_441_4', '观察周围情况', 'story_441_7', '', 1, 0, 0, 0, 0, 6),
('story_441_5', '继续前进', 'story_441_6', '', 1, 0, 0, 0, 0, 5),
('story_441_5', '停下来思考', 'story_441_7', '', 1, 0, 0, 0, 0, 4),
('story_441_5', '观察周围情况', 'story_441_8', '', 1, 0, 0, 0, 0, 6),
('story_441_6', '继续前进', 'story_441_7', '', 1, 0, 0, 0, 0, 5),
('story_441_6', '停下来思考', 'story_441_8', '', 1, 0, 0, 0, 0, 4),
('story_441_6', '观察周围情况', 'story_441_9', '', 1, 0, 0, 0, 0, 6),
('story_441_7', '继续前进', 'story_441_8', '', 1, 0, 0, 0, 0, 5),
('story_441_7', '停下来思考', 'story_441_9', '', 1, 0, 0, 0, 0, 4),
('story_441_7', '观察周围情况', 'story_441_10', '', 1, 0, 0, 0, 0, 6),
('story_441_8', '继续前进', 'story_441_9', '', 1, 0, 0, 0, 0, 5),
('story_441_8', '停下来思考', 'story_441_10', '', 1, 0, 0, 0, 0, 4),
('story_441_8', '观察周围情况', 'story_442_1', '', 1, 0, 0, 0, 0, 6),
('story_441_8', '探索新的方向', 'story_441_11', '', 1, 0, 0, 0, 0, 7),
('story_441_9', '继续前进', 'story_441_10', '', 1, 0, 0, 0, 0, 5),
('story_441_9', '停下来思考', 'story_442_1', '', 1, 0, 0, 0, 0, 4),
('story_441_9', '观察周围情况', 'story_442_1', '', 1, 0, 0, 0, 0, 6),
('story_441_9', '探索新的方向', 'story_441_11', '', 1, 0, 0, 0, 0, 7),
('story_441_10', '继续前进', 'story_442_1', '', 1, 0, 0, 0, 0, 5),
('story_441_10', '停下来思考', 'story_442_1', '', 1, 0, 0, 0, 0, 4),
('story_441_10', '观察周围情况', 'story_442_1', '', 1, 0, 0, 0, 0, 6),
('story_441_10', '探索新的方向', 'story_441_12', '', 1, 0, 0, 0, 0, 7),
('story_441_11', '仔细探索周围环境', 'story_442_1', '', 1, 0, 0, 0, 0, 8),
('story_441_11', '继续探索', 'story_442_1', '', 1, 0, 0, 0, 0, 5),
('story_441_11', '探索新的方向', 'story_441_12', '', 1, 0, 0, 0, 0, 7),
('story_441_12', '继续前进', 'story_442_1', '', 1, 0, 0, 0, 0, 5),
('story_441_12', '停下来思考', 'story_442_1', '', 1, 0, 0, 0, 0, 4),
('story_441_12', '观察周围情况', 'story_442_1', '', 1, 0, 0, 0, 0, 6),
('story_442_1', '继续前进', 'story_442_2', '', 1, 0, 0, 0, 0, 5),
('story_442_1', '停下来思考', 'story_442_3', '', 1, 0, 0, 0, 0, 4),
('story_442_1', '观察周围情况', 'story_442_4', '', 1, 0, 0, 0, 0, 6),
('story_442_2', '继续前进', 'story_442_3', '', 1, 0, 0, 0, 0, 5),
('story_442_2', '停下来思考', 'story_442_4', '', 1, 0, 0, 0, 0, 4),
('story_442_2', '观察周围情况', 'story_442_5', '', 1, 0, 0, 0, 0, 6),
('story_442_3', '继续前进', 'story_442_4', '', 1, 0, 0, 0, 0, 5),
('story_442_3', '停下来思考', 'story_442_5', '', 1, 0, 0, 0, 0, 4),
('story_442_3', '观察周围情况', 'story_442_6', '', 1, 0, 0, 0, 0, 6),
('story_442_4', '继续前进', 'story_442_5', '', 1, 0, 0, 0, 0, 5),
('story_442_4', '停下来思考', 'story_442_6', '', 1, 0, 0, 0, 0, 4),
('story_442_4', '观察周围情况', 'story_442_7', '', 1, 0, 0, 0, 0, 6),
('story_442_5', '继续前进', 'story_442_6', '', 1, 0, 0, 0, 0, 5),
('story_442_5', '停下来思考', 'story_442_7', '', 1, 0, 0, 0, 0, 4),
('story_442_5', '观察周围情况', 'story_442_8', '', 1, 0, 0, 0, 0, 6),
('story_442_6', '仔细探索周围环境', 'story_442_7', '', 1, 0, 0, 0, 0, 8),
('story_442_6', '继续探索', 'story_442_8', '', 1, 0, 0, 0, 0, 5),
('story_442_7', '继续前进', 'story_442_8', '', 1, 0, 0, 0, 0, 5),
('story_442_7', '停下来思考', 'story_442_9', '', 1, 0, 0, 0, 0, 4),
('story_442_7', '观察周围情况', 'story_442_10', '', 1, 0, 0, 0, 0, 6),
('story_442_8', '继续前进', 'story_442_9', '', 1, 0, 0, 0, 0, 5),
('story_442_8', '停下来思考', 'story_442_10', '', 1, 0, 0, 0, 0, 4),
('story_442_8', '观察周围情况', 'story_443_1', '', 1, 0, 0, 0, 0, 6),
('story_442_8', '探索新的方向', 'story_442_11', '', 1, 0, 0, 0, 0, 7),
('story_442_9', '继续前进', 'story_442_10', '', 1, 0, 0, 0, 0, 5),
('story_442_9', '停下来思考', 'story_443_1', '', 1, 0, 0, 0, 0, 4),
('story_442_9', '观察周围情况', 'story_443_1', '', 1, 0, 0, 0, 0, 6),
('story_442_9', '探索新的方向', 'story_442_11', '', 1, 0, 0, 0, 0, 7),
('story_442_10', '继续前进', 'story_443_1', '', 1, 0, 0, 0, 0, 5),
('story_442_10', '停下来思考', 'story_443_1', '', 1, 0, 0, 0, 0, 4),
('story_442_10', '观察周围情况', 'story_443_1', '', 1, 0, 0, 0, 0, 6),
('story_442_11', '继续前进', 'story_443_1', '', 1, 0, 0, 0, 0, 5),
('story_442_11', '停下来思考', 'story_443_1', '', 1, 0, 0, 0, 0, 4),
('story_442_11', '观察周围情况', 'story_443_1', '', 1, 0, 0, 0, 0, 6),
('story_443_1', '继续前进', 'story_443_2', '', 1, 0, 0, 0, 0, 5),
('story_443_1', '停下来思考', 'story_443_3', '', 1, 0, 0, 0, 0, 4),
('story_443_1', '观察周围情况', 'story_443_4', '', 1, 0, 0, 0, 0, 6),
('story_443_2', '仔细探索周围环境', 'story_443_3', '', 1, 0, 0, 0, 0, 8),
('story_443_2', '继续探索', 'story_443_4', '', 1, 0, 0, 0, 0, 5),
('story_443_3', '继续前进', 'story_443_4', '', 1, 0, 0, 0, 0, 5),
('story_443_3', '停下来思考', 'story_443_5', '', 1, 0, 0, 0, 0, 4),
('story_443_3', '观察周围情况', 'story_443_6', '', 1, 0, 0, 0, 0, 6),
('story_443_4', '继续前进', 'story_443_5', '', 1, 0, 0, 0, 0, 5),
('story_443_4', '停下来思考', 'story_443_6', '', 1, 0, 0, 0, 0, 4),
('story_443_4', '观察周围情况', 'story_443_7', '', 1, 0, 0, 0, 0, 6),
('story_443_5', '继续前进', 'story_443_6', '', 1, 0, 0, 0, 0, 5),
('story_443_5', '停下来思考', 'story_443_7', '', 1, 0, 0, 0, 0, 4),
('story_443_5', '观察周围情况', 'story_443_8', '', 1, 0, 0, 0, 0, 6),
('story_443_6', '继续前进', 'story_443_7', '', 1, 0, 0, 0, 0, 5),
('story_443_6', '停下来思考', 'story_443_8', '', 1, 0, 0, 0, 0, 4),
('story_443_6', '观察周围情况', 'story_443_9', '', 1, 0, 0, 0, 0, 6),
('story_443_7', '继续前进', 'story_443_8', '', 1, 0, 0, 0, 0, 5),
('story_443_7', '停下来思考', 'story_443_9', '', 1, 0, 0, 0, 0, 4),
('story_443_7', '观察周围情况', 'story_443_10', '', 1, 0, 0, 0, 0, 6),
('story_443_8', '继续前进', 'story_443_9', '', 1, 0, 0, 0, 0, 5),
('story_443_8', '停下来思考', 'story_443_10', '', 1, 0, 0, 0, 0, 4),
('story_443_8', '观察周围情况', 'story_444_1', '', 1, 0, 0, 0, 0, 6),
('story_443_9', '继续前进', 'story_443_10', '', 1, 0, 0, 0, 0, 5),
('story_443_9', '停下来思考', 'story_444_1', '', 1, 0, 0, 0, 0, 4),
('story_443_9', '观察周围情况', 'story_444_1', '', 1, 0, 0, 0, 0, 6),
('story_448_1', '继续前进', 'story_448_2', '', 1, 0, 0, 0, 0, 5),
('story_448_1', '停下来思考', 'story_448_3', '', 1, 0, 0, 0, 0, 4),
('story_448_1', '观察周围情况', 'story_448_4', '', 1, 0, 0, 0, 0, 6),
('story_448_1', '探索新的方向', 'story_449_1', '', 1, 0, 0, 0, 0, 7),
('story_448_2', '继续前进', 'story_448_3', '', 1, 0, 0, 0, 0, 5),
('story_448_2', '停下来思考', 'story_448_4', '', 1, 0, 0, 0, 0, 4),
('story_448_2', '观察周围情况', 'story_448_5', '', 1, 0, 0, 0, 0, 6),
('story_448_2', '探索新的方向', 'story_449_1', '', 1, 0, 0, 0, 0, 7),
('story_448_3', '继续前进', 'story_448_4', '', 1, 0, 0, 0, 0, 5),
('story_448_3', '停下来思考', 'story_448_5', '', 1, 0, 0, 0, 0, 4),
('story_448_3', '观察周围情况', 'story_448_6', '', 1, 0, 0, 0, 0, 6),
('story_448_4', '继续前进', 'story_448_5', '', 1, 0, 0, 0, 0, 5),
('story_448_4', '停下来思考', 'story_448_6', '', 1, 0, 0, 0, 0, 4),
('story_448_4', '观察周围情况', 'story_448_7', '', 1, 0, 0, 0, 0, 6),
('story_448_5', '继续前进', 'story_448_6', '', 1, 0, 0, 0, 0, 5),
('story_448_5', '停下来思考', 'story_448_7', '', 1, 0, 0, 0, 0, 4),
('story_448_5', '观察周围情况', 'story_448_8', '', 1, 0, 0, 0, 0, 6),
('story_449_1', '继续前进', 'story_449_2', '', 1, 0, 0, 0, 0, 5),
('story_449_1', '停下来思考', 'story_449_3', '', 1, 0, 0, 0, 0, 4),
('story_449_1', '观察周围情况', 'story_449_4', '', 1, 0, 0, 0, 0, 6),
('story_449_2', '继续前进', 'story_449_3', '', 1, 0, 0, 0, 0, 5),
('story_449_2', '停下来思考', 'story_449_4', '', 1, 0, 0, 0, 0, 4),
('story_449_2', '观察周围情况', 'story_449_5', '', 1, 0, 0, 0, 0, 6),
('story_449_3', '继续前进', 'story_449_4', '', 1, 0, 0, 0, 0, 5),
('story_449_3', '停下来思考', 'story_449_5', '', 1, 0, 0, 0, 0, 4),
('story_449_3', '观察周围情况', 'story_449_6', '', 1, 0, 0, 0, 0, 6),
('story_449_4', '继续前进', 'story_449_5', '', 1, 0, 0, 0, 0, 5),
('story_449_4', '停下来思考', 'story_449_6', '', 1, 0, 0, 0, 0, 4),
('story_449_4', '观察周围情况', 'story_449_7', '', 1, 0, 0, 0, 0, 6),
('story_449_5', '继续前进', 'story_449_6', '', 1, 0, 0, 0, 0, 5),
('story_449_5', '停下来思考', 'story_449_7', '', 1, 0, 0, 0, 0, 4),
('story_449_5', '观察周围情况', 'story_449_8', '', 1, 0, 0, 0, 0, 6),
('story_449_6', '继续前进', 'story_449_7', '', 1, 0, 0, 0, 0, 5),
('story_449_6', '停下来思考', 'story_449_8', '', 1, 0, 0, 0, 0, 4),
('story_449_6', '观察周围情况', 'story_449_9', '', 1, 0, 0, 0, 0, 6),
('story_449_7', '继续前进', 'story_449_8', '', 1, 0, 0, 0, 0, 5),
('story_449_7', '停下来思考', 'story_449_9', '', 1, 0, 0, 0, 0, 4),
('story_449_7', '观察周围情况', 'story_449_10', '', 1, 0, 0, 0, 0, 6),
('story_449_8', '继续前进', 'story_449_9', '', 1, 0, 0, 0, 0, 5),
('story_449_8', '停下来思考', 'story_449_10', '', 1, 0, 0, 0, 0, 4),
('story_449_8', '观察周围情况', 'story_450_1', '', 1, 0, 0, 0, 0, 6),
('story_449_8', '探索新的方向', 'story_449_11', '', 1, 0, 0, 0, 0, 7),
('story_449_9', '继续前进', 'story_449_10', '', 1, 0, 0, 0, 0, 5),
('story_449_9', '停下来思考', 'story_450_1', '', 1, 0, 0, 0, 0, 4),
('story_449_9', '观察周围情况', 'story_450_1', '', 1, 0, 0, 0, 0, 6),
('story_449_9', '探索新的方向', 'story_449_11', '', 1, 0, 0, 0, 0, 7),
('story_449_10', '继续前进', 'story_450_1', '', 1, 0, 0, 0, 0, 5),
('story_449_10', '停下来思考', 'story_450_1', '', 1, 0, 0, 0, 0, 4),
('story_449_10', '观察周围情况', 'story_450_1', '', 1, 0, 0, 0, 0, 6),
('story_449_11', '继续前进', 'story_450_1', '', 1, 0, 0, 0, 0, 5),
('story_449_11', '停下来思考', 'story_450_1', '', 1, 0, 0, 0, 0, 4),
('story_449_11', '观察周围情况', 'story_450_1', '', 1, 0, 0, 0, 0, 6),
('story_450_1', '继续前进', 'story_450_2', '', 1, 0, 0, 0, 0, 5),
('story_450_1', '停下来思考', 'story_450_3', '', 1, 0, 0, 0, 0, 4),
('story_450_1', '观察周围情况', 'story_450_4', '', 1, 0, 0, 0, 0, 6),
('story_450_2', '继续前进', 'story_450_3', '', 1, 0, 0, 0, 0, 5),
('story_450_2', '停下来思考', 'story_450_4', '', 1, 0, 0, 0, 0, 4),
('story_450_2', '观察周围情况', 'story_450_5', '', 1, 0, 0, 0, 0, 6),
('story_450_3', '继续前进', 'story_450_4', '', 1, 0, 0, 0, 0, 5),
('story_450_3', '停下来思考', 'story_450_5', '', 1, 0, 0, 0, 0, 4),
('story_450_3', '观察周围情况', 'story_450_6', '', 1, 0, 0, 0, 0, 6),
('story_450_4', '继续前进', 'story_450_5', '', 1, 0, 0, 0, 0, 5),
('story_450_4', '停下来思考', 'story_450_6', '', 1, 0, 0, 0, 0, 4),
('story_450_4', '观察周围情况', 'story_450_7', '', 1, 0, 0, 0, 0, 6),
('story_450_5', '继续前进', 'story_450_6', '', 1, 0, 0, 0, 0, 5),
('story_450_5', '停下来思考', 'story_450_7', '', 1, 0, 0, 0, 0, 4),
('story_450_5', '观察周围情况', 'story_450_8', '', 1, 0, 0, 0, 0, 6),
('story_450_6', '继续前进', 'story_450_7', '', 1, 0, 0, 0, 0, 5),
('story_450_6', '停下来思考', 'story_450_8', '', 1, 0, 0, 0, 0, 4),
('story_450_6', '观察周围情况', 'story_450_9', '', 1, 0, 0, 0, 0, 6),
('story_450_7', '继续前进', 'story_450_8', '', 1, 0, 0, 0, 0, 5),
('story_450_7', '停下来思考', 'story_450_9', '', 1, 0, 0, 0, 0, 4),
('story_450_7', '观察周围情况', 'story_450_10', '', 1, 0, 0, 0, 0, 6),
('story_450_8', '继续前进', 'story_450_9', '', 1, 0, 0, 0, 0, 5),
('story_450_8', '停下来思考', 'story_450_10', '', 1, 0, 0, 0, 0, 4),
('story_450_8', '观察周围情况', 'story_451_1', '', 1, 0, 0, 0, 0, 6),
('story_450_8', '探索新的方向', 'story_450_11', '', 1, 0, 0, 0, 0, 7),
('story_450_9', '继续前进', 'story_450_10', '', 1, 0, 0, 0, 0, 5),
('story_450_9', '停下来思考', 'story_451_1', '', 1, 0, 0, 0, 0, 4),
('story_450_9', '观察周围情况', 'story_451_1', '', 1, 0, 0, 0, 0, 6),
('story_450_9', '探索新的方向', 'story_450_11', '', 1, 0, 0, 0, 0, 7),
('story_450_10', '仔细探索周围环境', 'story_451_1', '', 1, 0, 0, 0, 0, 8),
('story_450_10', '继续探索', 'story_451_1', '', 1, 0, 0, 0, 0, 5),
('story_450_11', '继续前进', 'story_451_1', '', 1, 0, 0, 0, 0, 5),
('story_450_11', '停下来思考', 'story_451_1', '', 1, 0, 0, 0, 0, 4),
('story_450_11', '观察周围情况', 'story_451_1', '', 1, 0, 0, 0, 0, 6),
('story_451_1', '继续前进', 'story_451_2', '', 1, 0, 0, 0, 0, 5),
('story_451_1', '停下来思考', 'story_451_3', '', 1, 0, 0, 0, 0, 4),
('story_451_1', '观察周围情况', 'story_451_4', '', 1, 0, 0, 0, 0, 6),
('story_451_2', '仔细探索周围环境', 'story_451_3', '', 1, 0, 0, 0, 0, 8),
('story_451_2', '继续探索', 'story_451_4', '', 1, 0, 0, 0, 0, 5),
('story_451_3', '检查获得的物品', 'story_451_4', '', 1, 0, 0, 0, 0, 7),
('story_451_3', '继续探索', 'story_451_5', '', 1, 0, 0, 0, 0, 5),
('story_451_4', '仔细探索周围环境', 'story_451_5', '', 1, 0, 0, 0, 0, 8);

-- 批次统计
-- 本批次选择数: 500
-- 批次范围: 15001 - 15500
