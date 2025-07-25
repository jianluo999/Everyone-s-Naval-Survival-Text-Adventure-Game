-- 批量导入第1章剩余场景
USE sailing_game;

-- 删除可能存在的重复数据
DELETE FROM stories WHERE story_id IN ('story_1_24', 'story_1_25', 'story_1_26', 'story_1_27', 'story_1_28', 'story_1_29', 'story_1_30');

-- 插入第1章场景24-30
INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) VALUES
('story_1_24', '船只差异', '"你有蔬菜？我怎么只有香肠？"\n\n在海上，蔬菜可比肉类珍稀多了。\n\n"船呢，你们的船大吗，我的船有一百多米，太大了..."\n\n"什么！我的船只有十米！"\n\n那人很快发来了船的信息。\n\n【钢铁雄心号，一级，耐久5000/5000，容量8000单位，航速五节】\n\n【船体技能：火力全开：火炮射速提高至200%，持续15分钟。\n\n三连射鲸巨叉：可穿透挂住某个物体。】\n\n【简介：它的速度或许不快，但你的速度最好要快！】', 1, 24, 'NORMAL', false, NOW(), NOW()),

('story_1_25', '公平性质疑', '"靠！这游戏根本不公平，你的船一级就有大炮！"\n\n"特殊船有技能的，我的船完全是白板。"\n\n"我要刷初始，有没有氪金商城？我有的是钱！"\n\n"你们都是傻子吗？\n\n你的船速只有5节，比黑雾还慢！"\n\n"对哦，黑雾是10节！你完蛋了，啊哈哈哈！"\n\n这时候有公告弹出。\n\n【航海公告：\n\n你们所有人开局都不一样！船只、船上物品、个人天赋和起始位置都是根据你们性格经历设定好的，拒绝异议！】', 1, 25, 'DIALOGUE', false, NOW(), NOW()),

('story_1_26', '探索船舱', '"谁信啊，肯定有暗箱操作！有人开局就有武器，我只有吃的！"\n\n"别人囤粮我囤枪，别人就是我粮仓！"\n\n"有没有可能，有炮的人附近会刷怪，而你不会？"\n\n你合上日志，也开始在房间翻找起来。\n\n你发现骸骨手里的燧发枪是一件装备。\n\n【名称：浸水锈蚀的燧发枪】\n\n【种类：遗物】\n\n【品质：精品】\n\n【简介：这曾是一把大师之作，但泡水太久，锈蚀严重，只有五成概率能打响，可对异魔造成中量伤害。', 1, 26, 'NORMAL', false, NOW(), NOW()),

('story_1_27', '武器获得', '注意：使用遗物，有降低理智的风险。】\n\n你将燧发枪拿起，感觉沉甸甸的，很有分量。\n\n虽然锈蚀严重，但你能感觉到它曾经的威力。\n\n这时，你注意到骸骨的另一只手里还握着什么东西。\n\n是一张纸条，上面写着：\n\n"如果有人看到这张纸条，说明我已经死了。\n\n记住，永远不要相信海上的声音，那些不是人类的声音。\n\n黑雾中有东西在游荡，它们在寻找活人。\n\n保持理智，保持警惕。"', 1, 27, 'NORMAL', false, NOW(), NOW()),

('story_1_28', '警告纸条', '纸条的背面还有一些字迹：\n\n"船舱里还有一些补给，在床底下的箱子里。\n\n如果你能活过第一个夜晚，记住我的话：\n\n白天航行，夜晚停船。\n\n永远不要在夜晚航行，除非你想死。\n\n还有，如果你听到有人在海上呼救，不要理会，那不是人。"\n\n看完纸条，你感到一阵寒意。\n\n这个世界比你想象的更加危险。\n\n你决定先检查一下床底下的箱子。', 1, 28, 'NORMAL', false, NOW(), NOW()),

('story_1_29', '补给发现', '你蹲下身，在床底下摸索着。\n\n果然，有一个木制的箱子。\n\n你将它拖出来，打开一看：\n\n里面有一些干粮、淡水，还有一些奇怪的物品。\n\n【获得：干面包 x5】\n\n【获得：淡水 x3瓶】\n\n【获得：神秘的海螺 x1】\n\n【获得：航海图残片 x1】\n\n海螺散发着微弱的蓝光，图残片上标记着一些岛屿的位置。\n\n这些物品可能对你的生存很重要。', 1, 29, 'NORMAL', false, NOW(), NOW()),

('story_1_30', '准备出海', '收拾好物品后，你走出船舱，来到甲板上。\n\n海风吹拂着你的脸庞，远处是一望无际的大海。\n\n天空中有几朵白云，看起来天气还不错。\n\n你的船虽然破旧，但似乎还能航行。\n\n现在你需要决定下一步的行动：\n\n是继续探索这艘船，还是开始航行寻找其他的岛屿？\n\n或者先在聊天频道里收集更多信息？\n\n无论如何，你的航海求生之旅即将开始。', 1, 30, 'NORMAL', false, NOW(), NOW());

-- 查看导入结果
SELECT COUNT(*) as total_stories FROM stories;
SELECT story_id, title FROM stories WHERE chapter = 1 ORDER BY scene;
