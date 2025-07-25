-- 优化选择数据批次 55
INSERT INTO choices (story_id, text, next_story_id, requirements, is_available, health_cost, health_reward, gold_cost, gold_reward, experience_reward) VALUES
('story_488_13', '停下来思考', 'story_488_13_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_488_13', '检查身上的物品', 'story_488_13_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_489_1', '准备迎战', 'story_489_2', '', 1, 5, 0, 0, 10, 15),
('story_489_1', '寻找战术优势', 'story_489_1_tactical', '', 1, 0, 0, 0, 5, 10),
('story_489_2', '认真倾听对方的话', 'story_489_3', '', 1, 0, 0, 0, 0, 7),
('story_489_2', '提出我的疑问', 'story_489_2_question', '', 1, 0, 0, 0, 0, 5),
('story_489_3', '认真倾听对方的话', 'story_489_4', '', 1, 0, 0, 0, 0, 7),
('story_489_3', '提出我的疑问', 'story_489_3_question', '', 1, 0, 0, 0, 0, 5),
('story_489_4', '准备战斗', 'story_489_5', '', 1, 0, 0, 0, 0, 8),
('story_489_4', '寻找掩护', 'story_489_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_489_4', '观察敌情', 'story_489_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_489_4', '制定策略', 'story_489_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_489_5', '仔细观察周围环境', 'story_489_6', '', 1, 0, 0, 0, 0, 8),
('story_489_5', '继续向前探索', 'story_489_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_489_5', '停下来思考', 'story_489_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_489_5', '检查身上的物品', 'story_489_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_489_6', '认真倾听对方的话', 'story_489_7', '', 1, 0, 0, 0, 0, 7),
('story_489_6', '提出我的疑问', 'story_489_6_question', '', 1, 0, 0, 0, 0, 5),
('story_489_7', '仔细观察周围环境', 'story_489_8', '', 1, 0, 0, 0, 0, 8),
('story_489_7', '继续向前探索', 'story_489_7_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_489_7', '停下来思考', 'story_489_7_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_489_7', '检查身上的物品', 'story_489_7_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_489_8', '准备迎战', 'story_489_9', '', 1, 5, 0, 0, 10, 15),
('story_489_8', '寻找战术优势', 'story_489_8_tactical', '', 1, 0, 0, 0, 5, 10),
('story_489_9', '仔细观察周围环境', 'story_489_10', '', 1, 0, 0, 0, 0, 8),
('story_489_9', '继续向前探索', 'story_489_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_489_9', '停下来思考', 'story_489_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_489_9', '检查身上的物品', 'story_489_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_489_10', '仔细观察周围环境', 'story_489_11', '', 1, 0, 0, 0, 0, 8),
('story_489_10', '继续向前探索', 'story_489_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_489_10', '停下来思考', 'story_489_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_489_10', '检查身上的物品', 'story_489_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_489_11', '准备迎战', 'story_489_12', '', 1, 5, 0, 0, 10, 15),
('story_489_11', '寻找战术优势', 'story_489_11_tactical', '', 1, 0, 0, 0, 5, 10),
('story_489_12', '仔细观察周围环境', 'story_489_13', '', 1, 0, 0, 0, 0, 8),
('story_489_12', '继续向前探索', 'story_489_12_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_489_12', '停下来思考', 'story_489_12_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_489_12', '检查身上的物品', 'story_489_12_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_490_1', '准备迎战', 'story_490_2', '', 1, 5, 0, 0, 10, 15),
('story_490_1', '寻找战术优势', 'story_490_1_tactical', '', 1, 0, 0, 0, 5, 10),
('story_490_2', '准备迎战', 'story_490_3', '', 1, 5, 0, 0, 10, 15),
('story_490_2', '寻找战术优势', 'story_490_2_tactical', '', 1, 0, 0, 0, 5, 10),
('story_490_3', '仔细观察周围环境', 'story_490_4', '', 1, 0, 0, 0, 0, 8),
('story_490_3', '继续向前探索', 'story_490_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_490_3', '停下来思考', 'story_490_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_490_3', '检查身上的物品', 'story_490_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_490_4', '仔细观察周围环境', 'story_490_5', '', 1, 0, 0, 0, 0, 8),
('story_490_4', '继续向前探索', 'story_490_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_490_4', '停下来思考', 'story_490_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_490_4', '检查身上的物品', 'story_490_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_490_5', '认真倾听对方的话', 'story_490_6', '', 1, 0, 0, 0, 0, 7),
('story_490_5', '提出我的疑问', 'story_490_5_question', '', 1, 0, 0, 0, 0, 5),
('story_490_6', '仔细观察周围环境', 'story_490_7', '', 1, 0, 0, 0, 0, 8),
('story_490_6', '继续向前探索', 'story_490_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_490_6', '停下来思考', 'story_490_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_490_6', '检查身上的物品', 'story_490_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_490_7', '仔细观察周围环境', 'story_490_8', '', 1, 0, 0, 0, 0, 8),
('story_490_7', '继续向前探索', 'story_490_7_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_490_7', '停下来思考', 'story_490_7_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_490_7', '检查身上的物品', 'story_490_7_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_490_8', '仔细观察周围环境', 'story_490_9', '', 1, 0, 0, 0, 0, 8),
('story_490_8', '继续向前探索', 'story_490_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_490_8', '停下来思考', 'story_490_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_490_8', '检查身上的物品', 'story_490_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_490_9', '仔细观察周围环境', 'story_490_10', '', 1, 0, 0, 0, 0, 8),
('story_490_9', '继续向前探索', 'story_490_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_490_9', '停下来思考', 'story_490_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_490_9', '检查身上的物品', 'story_490_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_490_10', '仔细观察周围环境', 'story_490_11', '', 1, 0, 0, 0, 0, 8),
('story_490_10', '继续向前探索', 'story_490_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_490_10', '停下来思考', 'story_490_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_490_10', '检查身上的物品', 'story_490_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_1', '准备迎战', 'story_491_2', '', 1, 5, 0, 0, 10, 15),
('story_491_1', '寻找战术优势', 'story_491_1_tactical', '', 1, 0, 0, 0, 5, 10),
('story_491_2', '仔细观察周围环境', 'story_491_3', '', 1, 0, 0, 0, 0, 8),
('story_491_2', '继续向前探索', 'story_491_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_2', '停下来思考', 'story_491_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_2', '检查身上的物品', 'story_491_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_3', '仔细观察周围环境', 'story_491_4', '', 1, 0, 0, 0, 0, 8),
('story_491_3', '继续向前探索', 'story_491_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_3', '停下来思考', 'story_491_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_3', '检查身上的物品', 'story_491_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_4', '仔细观察周围环境', 'story_491_5', '', 1, 0, 0, 0, 0, 8),
('story_491_4', '继续向前探索', 'story_491_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_4', '停下来思考', 'story_491_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_4', '检查身上的物品', 'story_491_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_5', '仔细观察周围环境', 'story_491_6', '', 1, 0, 0, 0, 0, 8),
('story_491_5', '继续向前探索', 'story_491_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_5', '停下来思考', 'story_491_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_5', '检查身上的物品', 'story_491_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_6', '仔细观察周围环境', 'story_491_7', '', 1, 0, 0, 0, 0, 8),
('story_491_6', '继续向前探索', 'story_491_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_6', '停下来思考', 'story_491_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_6', '检查身上的物品', 'story_491_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_7', '仔细观察这个发现', 'story_491_8', '', 1, 0, 0, 0, 0, 8),
('story_491_7', '谨慎地接近查看', 'story_491_7_careful', '', 1, 0, 0, 0, 0, 6),
('story_491_8', '仔细观察这个发现', 'story_491_9', '', 1, 0, 0, 0, 0, 8),
('story_491_8', '谨慎地接近查看', 'story_491_8_careful', '', 1, 0, 0, 0, 0, 6),
('story_491_8', '认真倾听对方的话', 'story_491_9', '', 1, 0, 0, 0, 0, 7),
('story_491_8', '提出我的疑问', 'story_491_8_question', '', 1, 0, 0, 0, 0, 5),
('story_491_9', '仔细观察周围环境', 'story_491_10', '', 1, 0, 0, 0, 0, 8),
('story_491_9', '继续向前探索', 'story_491_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_9', '停下来思考', 'story_491_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_9', '检查身上的物品', 'story_491_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_10', '仔细观察周围环境', 'story_491_11', '', 1, 0, 0, 0, 0, 8),
('story_491_10', '继续向前探索', 'story_491_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_10', '停下来思考', 'story_491_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_10', '检查身上的物品', 'story_491_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_11', '仔细观察周围环境', 'story_491_12', '', 1, 0, 0, 0, 0, 8),
('story_491_11', '继续向前探索', 'story_491_11_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_11', '停下来思考', 'story_491_11_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_11', '检查身上的物品', 'story_491_11_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_12', '仔细观察周围环境', 'story_491_13', '', 1, 0, 0, 0, 0, 8),
('story_491_12', '继续向前探索', 'story_491_12_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_12', '停下来思考', 'story_491_12_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_12', '检查身上的物品', 'story_491_12_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_491_13', '仔细观察周围环境', 'story_491_14', '', 1, 0, 0, 0, 0, 8),
('story_491_13', '继续向前探索', 'story_491_13_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_491_13', '停下来思考', 'story_491_13_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_491_13', '检查身上的物品', 'story_491_13_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_492_1', '仔细观察周围环境', 'story_492_2', '', 1, 0, 0, 0, 0, 8),
('story_492_1', '继续向前探索', 'story_492_1_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_492_1', '停下来思考', 'story_492_1_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_492_1', '检查身上的物品', 'story_492_1_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_492_2', '仔细观察周围环境', 'story_492_3', '', 1, 0, 0, 0, 0, 8),
('story_492_2', '继续向前探索', 'story_492_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_492_2', '停下来思考', 'story_492_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_492_2', '检查身上的物品', 'story_492_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_492_3', '准备战斗', 'story_492_4', '', 1, 0, 0, 0, 0, 8),
('story_492_3', '寻找掩护', 'story_492_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_492_3', '观察敌情', 'story_492_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_492_3', '制定策略', 'story_492_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_492_4', '准备迎战', 'story_492_5', '', 1, 5, 0, 0, 10, 15),
('story_492_4', '寻找战术优势', 'story_492_4_tactical', '', 1, 0, 0, 0, 5, 10),
('story_492_5', '认真倾听对方的话', 'story_492_6', '', 1, 0, 0, 0, 0, 7),
('story_492_5', '提出我的疑问', 'story_492_5_question', '', 1, 0, 0, 0, 0, 5),
('story_492_5', '准备迎战', 'story_492_6', '', 1, 5, 0, 0, 10, 15),
('story_492_5', '寻找战术优势', 'story_492_5_tactical', '', 1, 0, 0, 0, 5, 10),
('story_492_6', '仔细观察周围环境', 'story_492_7', '', 1, 0, 0, 0, 0, 8),
('story_492_6', '继续向前探索', 'story_492_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_492_6', '停下来思考', 'story_492_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_492_6', '检查身上的物品', 'story_492_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_492_7', '认真倾听对方的话', 'story_492_8', '', 1, 0, 0, 0, 0, 7),
('story_492_7', '提出我的疑问', 'story_492_7_question', '', 1, 0, 0, 0, 0, 5),
('story_492_7', '准备迎战', 'story_492_8', '', 1, 5, 0, 0, 10, 15),
('story_492_7', '寻找战术优势', 'story_492_7_tactical', '', 1, 0, 0, 0, 5, 10),
('story_492_8', '仔细观察周围环境', 'story_492_9', '', 1, 0, 0, 0, 0, 8),
('story_492_8', '继续向前探索', 'story_492_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_492_8', '停下来思考', 'story_492_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_492_8', '检查身上的物品', 'story_492_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_492_9', '仔细观察周围环境', 'story_492_10', '', 1, 0, 0, 0, 0, 8),
('story_492_9', '继续向前探索', 'story_492_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_492_9', '停下来思考', 'story_492_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_492_9', '检查身上的物品', 'story_492_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_1', '仔细观察周围环境', 'story_493_2', '', 1, 0, 0, 0, 0, 8),
('story_493_1', '继续向前探索', 'story_493_1_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_1', '停下来思考', 'story_493_1_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_1', '检查身上的物品', 'story_493_1_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_2', '仔细观察周围环境', 'story_493_3', '', 1, 0, 0, 0, 0, 8),
('story_493_2', '继续向前探索', 'story_493_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_2', '停下来思考', 'story_493_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_2', '检查身上的物品', 'story_493_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_3', '认真倾听对方的话', 'story_493_4', '', 1, 0, 0, 0, 0, 7),
('story_493_3', '提出我的疑问', 'story_493_3_question', '', 1, 0, 0, 0, 0, 5),
('story_493_4', '准备迎战', 'story_493_5', '', 1, 5, 0, 0, 10, 15),
('story_493_4', '寻找战术优势', 'story_493_4_tactical', '', 1, 0, 0, 0, 5, 10),
('story_493_5', '认真倾听对方的话', 'story_493_6', '', 1, 0, 0, 0, 0, 7),
('story_493_5', '提出我的疑问', 'story_493_5_question', '', 1, 0, 0, 0, 0, 5),
('story_493_6', '仔细观察周围环境', 'story_493_7', '', 1, 0, 0, 0, 0, 8),
('story_493_6', '继续向前探索', 'story_493_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_6', '停下来思考', 'story_493_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_6', '检查身上的物品', 'story_493_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_7', '仔细观察周围环境', 'story_493_8', '', 1, 0, 0, 0, 0, 8),
('story_493_7', '继续向前探索', 'story_493_7_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_7', '停下来思考', 'story_493_7_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_7', '检查身上的物品', 'story_493_7_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_8', '仔细观察周围环境', 'story_493_9', '', 1, 0, 0, 0, 0, 8),
('story_493_8', '继续向前探索', 'story_493_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_8', '停下来思考', 'story_493_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_8', '检查身上的物品', 'story_493_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_9', '准备迎战', 'story_493_10', '', 1, 5, 0, 0, 10, 15),
('story_493_9', '寻找战术优势', 'story_493_9_tactical', '', 1, 0, 0, 0, 5, 10),
('story_493_10', '认真倾听对方的话', 'story_493_11', '', 1, 0, 0, 0, 0, 7),
('story_493_10', '提出我的疑问', 'story_493_10_question', '', 1, 0, 0, 0, 0, 5),
('story_493_11', '仔细观察周围环境', 'story_493_12', '', 1, 0, 0, 0, 0, 8),
('story_493_11', '继续向前探索', 'story_493_11_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_11', '停下来思考', 'story_493_11_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_11', '检查身上的物品', 'story_493_11_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_12', '准备迎战', 'story_493_13', '', 1, 5, 0, 0, 10, 15),
('story_493_12', '寻找战术优势', 'story_493_12_tactical', '', 1, 0, 0, 0, 5, 10),
('story_493_13', '仔细观察周围环境', 'story_493_14', '', 1, 0, 0, 0, 0, 8),
('story_493_13', '继续向前探索', 'story_493_13_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_13', '停下来思考', 'story_493_13_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_13', '检查身上的物品', 'story_493_13_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_14', '仔细搜查', 'story_493_15', '', 1, 0, 0, 0, 0, 8),
('story_493_14', '快速浏览', 'story_493_14_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_493_14', '重点检查', 'story_493_14_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_493_14', '全面探索', 'story_493_14_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_493_15', '认真倾听对方的话', 'story_493_16', '', 1, 0, 0, 0, 0, 7),
('story_493_15', '提出我的疑问', 'story_493_15_question', '', 1, 0, 0, 0, 0, 5),
('story_493_16', '认真倾听对方的话', 'story_493_17', '', 1, 0, 0, 0, 0, 7),
('story_493_16', '提出我的疑问', 'story_493_16_question', '', 1, 0, 0, 0, 0, 5),
('story_494_1', '准备迎战', 'story_494_2', '', 1, 5, 0, 0, 10, 15),
('story_494_1', '寻找战术优势', 'story_494_1_tactical', '', 1, 0, 0, 0, 5, 10),
('story_494_2', '仔细观察周围环境', 'story_494_3', '', 1, 0, 0, 0, 0, 8),
('story_494_2', '继续向前探索', 'story_494_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_2', '停下来思考', 'story_494_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_2', '检查身上的物品', 'story_494_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_494_3', '仔细观察周围环境', 'story_494_4', '', 1, 0, 0, 0, 0, 8),
('story_494_3', '继续向前探索', 'story_494_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_3', '停下来思考', 'story_494_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_3', '检查身上的物品', 'story_494_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_494_4', '仔细观察周围环境', 'story_494_5', '', 1, 0, 0, 0, 0, 8),
('story_494_4', '继续向前探索', 'story_494_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_4', '停下来思考', 'story_494_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_4', '检查身上的物品', 'story_494_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_494_5', '仔细观察周围环境', 'story_494_6', '', 1, 0, 0, 0, 0, 8),
('story_494_5', '继续向前探索', 'story_494_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_5', '停下来思考', 'story_494_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_5', '检查身上的物品', 'story_494_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_494_6', '认真倾听对方的话', 'story_494_7', '', 1, 0, 0, 0, 0, 7),
('story_494_6', '提出我的疑问', 'story_494_6_question', '', 1, 0, 0, 0, 0, 5),
('story_494_7', '准备迎战', 'story_494_8', '', 1, 5, 0, 0, 10, 15),
('story_494_7', '寻找战术优势', 'story_494_7_tactical', '', 1, 0, 0, 0, 5, 10),
('story_494_8', '仔细观察周围环境', 'story_494_9', '', 1, 0, 0, 0, 0, 8),
('story_494_8', '继续向前探索', 'story_494_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_8', '停下来思考', 'story_494_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_8', '检查身上的物品', 'story_494_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_494_9', '仔细观察周围环境', 'story_494_10', '', 1, 0, 0, 0, 0, 8),
('story_494_9', '继续向前探索', 'story_494_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_9', '停下来思考', 'story_494_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_9', '检查身上的物品', 'story_494_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_494_10', '认真倾听对方的话', 'story_494_11', '', 1, 0, 0, 0, 0, 7),
('story_494_10', '提出我的疑问', 'story_494_10_question', '', 1, 0, 0, 0, 0, 5),
('story_494_11', '仔细观察周围环境', 'story_494_12', '', 1, 0, 0, 0, 0, 8),
('story_494_11', '继续向前探索', 'story_494_11_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_11', '停下来思考', 'story_494_11_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_11', '检查身上的物品', 'story_494_11_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_494_12', '仔细观察周围环境', 'story_494_13', '', 1, 0, 0, 0, 0, 8),
('story_494_12', '继续向前探索', 'story_494_12_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_494_12', '停下来思考', 'story_494_12_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_494_12', '检查身上的物品', 'story_494_12_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_1', '仔细观察这个发现', 'story_495_2', '', 1, 0, 0, 0, 0, 8),
('story_495_1', '谨慎地接近查看', 'story_495_1_careful', '', 1, 0, 0, 0, 0, 6),
('story_495_2', '准备战斗', 'story_495_3', '', 1, 0, 0, 0, 0, 8),
('story_495_2', '寻找掩护', 'story_495_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_2', '观察敌情', 'story_495_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_2', '制定策略', 'story_495_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_3', '准备战斗', 'story_495_4', '', 1, 0, 0, 0, 0, 8),
('story_495_3', '寻找掩护', 'story_495_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_3', '观察敌情', 'story_495_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_3', '制定策略', 'story_495_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_4', '仔细观察周围环境', 'story_495_5', '', 1, 0, 0, 0, 0, 8),
('story_495_4', '继续向前探索', 'story_495_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_4', '停下来思考', 'story_495_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_4', '检查身上的物品', 'story_495_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_5', '仔细观察周围环境', 'story_495_6', '', 1, 0, 0, 0, 0, 8),
('story_495_5', '继续向前探索', 'story_495_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_5', '停下来思考', 'story_495_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_5', '检查身上的物品', 'story_495_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_6', '仔细观察周围环境', 'story_495_7', '', 1, 0, 0, 0, 0, 8),
('story_495_6', '继续向前探索', 'story_495_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_6', '停下来思考', 'story_495_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_6', '检查身上的物品', 'story_495_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_7', '仔细观察这个发现', 'story_495_8', '', 1, 0, 0, 0, 0, 8),
('story_495_7', '谨慎地接近查看', 'story_495_7_careful', '', 1, 0, 0, 0, 0, 6),
('story_495_8', '仔细观察周围环境', 'story_495_9', '', 1, 0, 0, 0, 0, 8),
('story_495_8', '继续向前探索', 'story_495_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_8', '停下来思考', 'story_495_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_8', '检查身上的物品', 'story_495_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_9', '仔细观察周围环境', 'story_495_10', '', 1, 0, 0, 0, 0, 8),
('story_495_9', '继续向前探索', 'story_495_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_9', '停下来思考', 'story_495_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_9', '检查身上的物品', 'story_495_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_10', '仔细观察周围环境', 'story_495_11', '', 1, 0, 0, 0, 0, 8),
('story_495_10', '继续向前探索', 'story_495_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_495_10', '停下来思考', 'story_495_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_495_10', '检查身上的物品', 'story_495_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_495_11', '认真倾听对方的话', 'story_495_12', '', 1, 0, 0, 0, 0, 7),
('story_495_11', '提出我的疑问', 'story_495_11_question', '', 1, 0, 0, 0, 0, 5),
('story_495_12', '认真倾听对方的话', 'story_495_13', '', 1, 0, 0, 0, 0, 7),
('story_495_12', '提出我的疑问', 'story_495_12_question', '', 1, 0, 0, 0, 0, 5),
('story_496_1', '仔细观察周围环境', 'story_496_2', '', 1, 0, 0, 0, 0, 8),
('story_496_1', '继续向前探索', 'story_496_1_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_1', '停下来思考', 'story_496_1_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_1', '检查身上的物品', 'story_496_1_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_2', '仔细观察周围环境', 'story_496_3', '', 1, 0, 0, 0, 0, 8),
('story_496_2', '继续向前探索', 'story_496_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_2', '停下来思考', 'story_496_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_2', '检查身上的物品', 'story_496_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_3', '仔细观察周围环境', 'story_496_4', '', 1, 0, 0, 0, 0, 8),
('story_496_3', '继续向前探索', 'story_496_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_3', '停下来思考', 'story_496_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_3', '检查身上的物品', 'story_496_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_4', '仔细观察周围环境', 'story_496_5', '', 1, 0, 0, 0, 0, 8),
('story_496_4', '继续向前探索', 'story_496_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_4', '停下来思考', 'story_496_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_4', '检查身上的物品', 'story_496_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_5', '仔细观察周围环境', 'story_496_6', '', 1, 0, 0, 0, 0, 8),
('story_496_5', '继续向前探索', 'story_496_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_5', '停下来思考', 'story_496_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_5', '检查身上的物品', 'story_496_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_6', '仔细观察周围环境', 'story_496_7', '', 1, 0, 0, 0, 0, 8),
('story_496_6', '继续向前探索', 'story_496_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_6', '停下来思考', 'story_496_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_6', '检查身上的物品', 'story_496_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_7', '认真倾听对方的话', 'story_496_8', '', 1, 0, 0, 0, 0, 7),
('story_496_7', '提出我的疑问', 'story_496_7_question', '', 1, 0, 0, 0, 0, 5),
('story_496_8', '仔细观察周围环境', 'story_496_9', '', 1, 0, 0, 0, 0, 8),
('story_496_8', '继续向前探索', 'story_496_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_8', '停下来思考', 'story_496_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_8', '检查身上的物品', 'story_496_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_9', '仔细观察周围环境', 'story_496_10', '', 1, 0, 0, 0, 0, 8),
('story_496_9', '继续向前探索', 'story_496_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_9', '停下来思考', 'story_496_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_9', '检查身上的物品', 'story_496_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_10', '仔细观察周围环境', 'story_496_11', '', 1, 0, 0, 0, 0, 8),
('story_496_10', '继续向前探索', 'story_496_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_10', '停下来思考', 'story_496_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_10', '检查身上的物品', 'story_496_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_11', '仔细观察周围环境', 'story_496_12', '', 1, 0, 0, 0, 0, 8),
('story_496_11', '继续向前探索', 'story_496_11_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_11', '停下来思考', 'story_496_11_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_11', '检查身上的物品', 'story_496_11_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_12', '认真倾听对方的话', 'story_496_13', '', 1, 0, 0, 0, 0, 7),
('story_496_12', '提出我的疑问', 'story_496_12_question', '', 1, 0, 0, 0, 0, 5),
('story_496_13', '仔细观察周围环境', 'story_496_14', '', 1, 0, 0, 0, 0, 8),
('story_496_13', '继续向前探索', 'story_496_13_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_13', '停下来思考', 'story_496_13_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_13', '检查身上的物品', 'story_496_13_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_496_14', '仔细观察周围环境', 'story_496_15', '', 1, 0, 0, 0, 0, 8),
('story_496_14', '继续向前探索', 'story_496_14_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_496_14', '停下来思考', 'story_496_14_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_496_14', '检查身上的物品', 'story_496_14_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_1', '仔细观察周围环境', 'story_497_2', '', 1, 0, 0, 0, 0, 8),
('story_497_1', '继续向前探索', 'story_497_1_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_1', '停下来思考', 'story_497_1_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_1', '检查身上的物品', 'story_497_1_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_2', '仔细观察周围环境', 'story_497_3', '', 1, 0, 0, 0, 0, 8),
('story_497_2', '继续向前探索', 'story_497_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_2', '停下来思考', 'story_497_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_2', '检查身上的物品', 'story_497_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_3', '仔细观察周围环境', 'story_497_4', '', 1, 0, 0, 0, 0, 8),
('story_497_3', '继续向前探索', 'story_497_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_3', '停下来思考', 'story_497_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_3', '检查身上的物品', 'story_497_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_4', '仔细观察周围环境', 'story_497_5', '', 1, 0, 0, 0, 0, 8),
('story_497_4', '继续向前探索', 'story_497_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_4', '停下来思考', 'story_497_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_4', '检查身上的物品', 'story_497_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_5', '仔细观察周围环境', 'story_497_6', '', 1, 0, 0, 0, 0, 8),
('story_497_5', '继续向前探索', 'story_497_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_5', '停下来思考', 'story_497_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_5', '检查身上的物品', 'story_497_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_6', '仔细观察周围环境', 'story_497_7', '', 1, 0, 0, 0, 0, 8),
('story_497_6', '继续向前探索', 'story_497_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_6', '停下来思考', 'story_497_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_6', '检查身上的物品', 'story_497_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_7', '认真倾听对方的话', 'story_497_8', '', 1, 0, 0, 0, 0, 7),
('story_497_7', '提出我的疑问', 'story_497_7_question', '', 1, 0, 0, 0, 0, 5),
('story_497_8', '仔细观察周围环境', 'story_497_9', '', 1, 0, 0, 0, 0, 8),
('story_497_8', '继续向前探索', 'story_497_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_8', '停下来思考', 'story_497_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_8', '检查身上的物品', 'story_497_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_9', '仔细观察周围环境', 'story_497_10', '', 1, 0, 0, 0, 0, 8),
('story_497_9', '继续向前探索', 'story_497_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_9', '停下来思考', 'story_497_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_9', '检查身上的物品', 'story_497_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_10', '仔细观察周围环境', 'story_497_11', '', 1, 0, 0, 0, 0, 8),
('story_497_10', '继续向前探索', 'story_497_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_10', '停下来思考', 'story_497_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_10', '检查身上的物品', 'story_497_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_11', '准备迎战', 'story_497_12', '', 1, 5, 0, 0, 10, 15),
('story_497_11', '寻找战术优势', 'story_497_11_tactical', '', 1, 0, 0, 0, 5, 10),
('story_497_12', '仔细观察周围环境', 'story_497_13', '', 1, 0, 0, 0, 0, 8),
('story_497_12', '继续向前探索', 'story_497_12_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_497_12', '停下来思考', 'story_497_12_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_497_12', '检查身上的物品', 'story_497_12_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_497_13', '准备迎战', 'story_497_14', '', 1, 5, 0, 0, 10, 15),
('story_497_13', '寻找战术优势', 'story_497_13_tactical', '', 1, 0, 0, 0, 5, 10),
('story_497_14', '准备迎战', 'story_497_15', '', 1, 5, 0, 0, 10, 15),
('story_497_14', '寻找战术优势', 'story_497_14_tactical', '', 1, 0, 0, 0, 5, 10),
('story_498_1', '仔细观察周围环境', 'story_498_2', '', 1, 0, 0, 0, 0, 8),
('story_498_1', '继续向前探索', 'story_498_1_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_498_1', '停下来思考', 'story_498_1_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_498_1', '检查身上的物品', 'story_498_1_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_498_2', '仔细观察这个发现', 'story_498_3', '', 1, 0, 0, 0, 0, 8),
('story_498_2', '谨慎地接近查看', 'story_498_2_careful', '', 1, 0, 0, 0, 0, 6),
('story_498_3', '仔细观察周围环境', 'story_498_4', '', 1, 0, 0, 0, 0, 8),
('story_498_3', '继续向前探索', 'story_498_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_498_3', '停下来思考', 'story_498_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_498_3', '检查身上的物品', 'story_498_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_498_4', '认真倾听对方的话', 'story_498_5', '', 1, 0, 0, 0, 0, 7),
('story_498_4', '提出我的疑问', 'story_498_4_question', '', 1, 0, 0, 0, 0, 5),
('story_498_5', '仔细观察周围环境', 'story_498_6', '', 1, 0, 0, 0, 0, 8),
('story_498_5', '继续向前探索', 'story_498_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_498_5', '停下来思考', 'story_498_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_498_5', '检查身上的物品', 'story_498_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_498_6', '认真倾听对方的话', 'story_498_7', '', 1, 0, 0, 0, 0, 7),
('story_498_6', '提出我的疑问', 'story_498_6_question', '', 1, 0, 0, 0, 0, 5),
('story_499_1', '仔细观察周围环境', 'story_499_2', '', 1, 0, 0, 0, 0, 8),
('story_499_1', '继续向前探索', 'story_499_1_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_499_1', '停下来思考', 'story_499_1_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_499_1', '检查身上的物品', 'story_499_1_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_499_2', '仔细观察周围环境', 'story_499_3', '', 1, 0, 0, 0, 0, 8),
('story_499_2', '继续向前探索', 'story_499_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_499_2', '停下来思考', 'story_499_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_499_2', '检查身上的物品', 'story_499_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_499_3', '仔细观察周围环境', 'story_499_4', '', 1, 0, 0, 0, 0, 8),
('story_499_3', '继续向前探索', 'story_499_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_499_3', '停下来思考', 'story_499_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_499_3', '检查身上的物品', 'story_499_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_499_4', '认真倾听对方的话', 'story_499_5', '', 1, 0, 0, 0, 0, 7),
('story_499_4', '提出我的疑问', 'story_499_4_question', '', 1, 0, 0, 0, 0, 5),
('story_499_5', '认真倾听对方的话', 'story_499_6', '', 1, 0, 0, 0, 0, 7),
('story_499_5', '提出我的疑问', 'story_499_5_question', '', 1, 0, 0, 0, 0, 5),
('story_499_5', '准备迎战', 'story_499_6', '', 1, 5, 0, 0, 10, 15),
('story_499_5', '寻找战术优势', 'story_499_5_tactical', '', 1, 0, 0, 0, 5, 10),
('story_500_1', '认真倾听对方的话', 'story_500_2', '', 1, 0, 0, 0, 0, 7),
('story_500_1', '提出我的疑问', 'story_500_1_question', '', 1, 0, 0, 0, 0, 5),
('story_500_2', '仔细观察周围环境', 'story_500_3', '', 1, 0, 0, 0, 0, 8),
('story_500_2', '继续向前探索', 'story_500_2_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_2', '停下来思考', 'story_500_2_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_2', '检查身上的物品', 'story_500_2_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_3', '仔细观察周围环境', 'story_500_4', '', 1, 0, 0, 0, 0, 8),
('story_500_3', '继续向前探索', 'story_500_3_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_3', '停下来思考', 'story_500_3_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_3', '检查身上的物品', 'story_500_3_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_4', '仔细观察周围环境', 'story_500_5', '', 1, 0, 0, 0, 0, 8),
('story_500_4', '继续向前探索', 'story_500_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_4', '停下来思考', 'story_500_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_4', '检查身上的物品', 'story_500_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_5', '认真倾听对方的话', 'story_500_6', '', 1, 0, 0, 0, 0, 7),
('story_500_5', '提出我的疑问', 'story_500_5_question', '', 1, 0, 0, 0, 0, 5),
('story_500_6', '仔细观察周围环境', 'story_500_7', '', 1, 0, 0, 0, 0, 8),
('story_500_6', '继续向前探索', 'story_500_6_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_6', '停下来思考', 'story_500_6_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_6', '检查身上的物品', 'story_500_6_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_7', '准备迎战', 'story_500_8', '', 1, 5, 0, 0, 10, 15),
('story_500_7', '寻找战术优势', 'story_500_7_tactical', '', 1, 0, 0, 0, 5, 10),
('story_500_8', '仔细观察周围环境', 'story_500_9', '', 1, 0, 0, 0, 0, 8),
('story_500_8', '继续向前探索', 'story_500_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_8', '停下来思考', 'story_500_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_8', '检查身上的物品', 'story_500_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_9', '准备迎战', 'story_500_10', '', 1, 5, 0, 0, 10, 15),
('story_500_9', '寻找战术优势', 'story_500_9_tactical', '', 1, 0, 0, 0, 5, 10),
('story_500_10', '仔细观察周围环境', 'story_500_11', '', 1, 0, 0, 0, 0, 8),
('story_500_10', '继续向前探索', 'story_500_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_10', '停下来思考', 'story_500_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_10', '检查身上的物品', 'story_500_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_11', '仔细观察周围环境', 'story_500_12', '', 1, 0, 0, 0, 0, 8),
('story_500_11', '继续向前探索', 'story_500_11_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_11', '停下来思考', 'story_500_11_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_11', '检查身上的物品', 'story_500_11_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_12', '仔细观察周围环境', 'story_500_13', '', 1, 0, 0, 0, 0, 8),
('story_500_12', '继续向前探索', 'story_500_12_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_12', '停下来思考', 'story_500_12_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_12', '检查身上的物品', 'story_500_12_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_500_13', '仔细观察周围环境', 'story_500_14', '', 1, 0, 0, 0, 0, 8),
('story_500_13', '继续向前探索', 'story_500_13_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_500_13', '停下来思考', 'story_500_13_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_500_13', '检查身上的物品', 'story_500_13_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_1', '仔细观察周围环境', 'story_501_2', '', 1, 0, 0, 0, 0, 8),
('story_501_1', '继续向前探索', 'story_501_1_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_501_1', '停下来思考', 'story_501_1_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_501_1', '检查身上的物品', 'story_501_1_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_2', '准备迎战', 'story_501_3', '', 1, 5, 0, 0, 10, 15),
('story_501_2', '寻找战术优势', 'story_501_2_tactical', '', 1, 0, 0, 0, 5, 10),
('story_501_3', '准备迎战', 'story_501_4', '', 1, 5, 0, 0, 10, 15),
('story_501_3', '寻找战术优势', 'story_501_3_tactical', '', 1, 0, 0, 0, 5, 10),
('story_501_4', '仔细观察周围环境', 'story_501_5', '', 1, 0, 0, 0, 0, 8),
('story_501_4', '继续向前探索', 'story_501_4_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_501_4', '停下来思考', 'story_501_4_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_501_4', '检查身上的物品', 'story_501_4_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_5', '仔细观察周围环境', 'story_501_6', '', 1, 0, 0, 0, 0, 8),
('story_501_5', '继续向前探索', 'story_501_5_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_501_5', '停下来思考', 'story_501_5_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_501_5', '检查身上的物品', 'story_501_5_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_6', '准备迎战', 'story_501_7', '', 1, 5, 0, 0, 10, 15),
('story_501_6', '寻找战术优势', 'story_501_6_tactical', '', 1, 0, 0, 0, 5, 10),
('story_501_7', '仔细观察周围环境', 'story_501_8', '', 1, 0, 0, 0, 0, 8),
('story_501_7', '继续向前探索', 'story_501_7_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_501_7', '停下来思考', 'story_501_7_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_501_7', '检查身上的物品', 'story_501_7_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_8', '仔细观察周围环境', 'story_501_9', '', 1, 0, 0, 0, 0, 8),
('story_501_8', '继续向前探索', 'story_501_8_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_501_8', '停下来思考', 'story_501_8_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_501_8', '检查身上的物品', 'story_501_8_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_9', '仔细观察周围环境', 'story_501_10', '', 1, 0, 0, 0, 0, 8),
('story_501_9', '继续向前探索', 'story_501_9_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_501_9', '停下来思考', 'story_501_9_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_501_9', '检查身上的物品', 'story_501_9_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_10', '仔细观察周围环境', 'story_501_11', '', 1, 0, 0, 0, 0, 8),
('story_501_10', '继续向前探索', 'story_501_10_alt_1', '', 1, 0, 0, 0, 0, 5),
('story_501_10', '停下来思考', 'story_501_10_alt_2', '', 1, 0, 0, 0, 0, 5),
('story_501_10', '检查身上的物品', 'story_501_10_alt_3', '', 1, 0, 0, 0, 0, 5),
('story_501_11', '仔细观察这个发现', 'story_501_12', '', 1, 0, 0, 0, 0, 8),
('story_501_11', '谨慎地接近查看', 'story_501_11_careful', '', 1, 0, 0, 0, 0, 6),
('story_501_12', '认真倾听对方的话', 'story_501_13', '', 1, 0, 0, 0, 0, 7),
('story_501_12', '提出我的疑问', 'story_501_12_question', '', 1, 0, 0, 0, 0, 5);
