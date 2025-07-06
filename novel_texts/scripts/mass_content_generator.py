#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大规模内容生成器 - 快速生成500章小说内容
"""

import os
from pathlib import Path

class MassContentGenerator:
    """大规模内容生成器"""
    
    def __init__(self):
        self.base_path = Path("../")
        self.resources_path = Path("../../backend/src/main/resources/novel_texts/")
        
    def generate_chapter_2_content(self):
        """生成第2章内容 - 深海探索"""
        chapter_2_stories = [
            (31, "深海迷雾", "你驾驶着破旧的木船继续航行，远处出现了一片浓厚的迷雾。\\n\\n迷雾中隐约传来奇怪的声音，像是有什么东西在水中游动。\\n\\n你想起了航海日志中的警告：'要小心夜晚，当心雾气'。\\n\\n现在虽然是白天，但这片迷雾看起来并不寻常。\\n\\n你需要做出选择：是绕过这片迷雾，还是勇敢地穿越过去？", "NORMAL", False),
            (32, "雾中异响", "你决定小心地驶入迷雾。\\n\\n能见度急剧下降，你几乎看不到十米外的景象。\\n\\n突然，船底传来了'咚咚'的撞击声，好像有什么东西在撞击船体。\\n\\n你紧握着燧发枪，心跳加速。\\n\\n水面上开始出现奇怪的波纹，仿佛有巨大的生物在船底游过。\\n\\n【理智-5】", "HORROR", False),
            (33, "海怪现身", "一个巨大的触手突然从水中伸出，重重地拍在甲板上！\\n\\n这是一只巨大的海怪，它的眼睛如灯笼般发光，盯着你。\\n\\n【遭遇：深海章鱼怪】\\n\\n【等级：2级】\\n\\n【生命值：150/150】\\n\\n【攻击力：25】\\n\\n【特殊能力：触手缠绕，墨汁喷射】\\n\\n海怪发出低沉的咆哮声，准备发动攻击！", "COMBAT", False),
            (34, "战斗胜利", "经过激烈的战斗，你成功击败了海怪！\\n\\n【获得经验：200】\\n\\n【获得金币：100】\\n\\n【获得物品：海怪触手 x2】\\n\\n【获得物品：深海珍珠 x1】\\n\\n海怪的尸体慢慢沉入海底，周围的迷雾也开始散去。\\n\\n你发现前方出现了一座神秘的小岛。", "VICTORY", False),
            (35, "神秘岛屿", "这座小岛看起来无人居住，但岛上有一些古老的建筑遗迹。\\n\\n你将船停靠在岸边，准备上岛探索。\\n\\n岛上长满了奇异的植物，空气中弥漫着淡淡的魔法气息。\\n\\n在岛屿中央，你看到了一座古老的石塔。\\n\\n塔顶闪烁着微弱的蓝光。", "EXPLORATION", False),
            (36, "古塔探索", "你走进古塔，发现里面有一个螺旋楼梯通向塔顶。\\n\\n墙壁上刻满了古老的符文，散发着神秘的光芒。\\n\\n在塔的一层，你发现了一个宝箱。\\n\\n【获得：古老的航海图 x1】\\n\\n【获得：魔法罗盘 x1】\\n\\n【获得：治疗药水 x3】\\n\\n这些物品对你的航海之旅将非常有用。", "TREASURE", False),
            (37, "塔顶秘密", "你爬到塔顶，发现这里有一个古老的传送法阵。\\n\\n法阵中央放着一块发光的水晶。\\n\\n当你触摸水晶时，脑海中突然出现了一些画面：\\n\\n一个古老的文明，强大的海洋法师，还有一场毁灭性的战争。\\n\\n【获得：远古记忆碎片】\\n\\n【理智+10】\\n\\n你似乎了解了这个世界的一些秘密。", "REVELATION", False),
            (38, "离开岛屿", "你带着新获得的物品和知识离开了神秘岛屿。\\n\\n魔法罗盘指向了一个新的方向，那里似乎有更多的秘密等待发现。\\n\\n你的船现在装备更加齐全，你也变得更加强大。\\n\\n但你知道，这只是冒险的开始。\\n\\n更大的挑战还在前方等待着你。", "CHAPTER_END", True)
        ]
        
        # 生成故事数据文件
        story_content = "# 第2章数据文件 - 深海探索\n# 格式: 场景号|标题|内容|类型|是否结局\n\n"
        for scene_id, title, content, story_type, is_ending in chapter_2_stories:
            story_content += f"{scene_id}|{title}|{content}|{story_type}|{str(is_ending).lower()}\n"
        
        # 生成选择数据文件
        choice_content = "# 第2章选择数据文件 - 深海探索\n# 格式: 故事ID|选择文本|下一个故事ID|金币消耗|金币奖励|生命消耗|生命奖励|经验奖励|要求|是否可用\n\n"
        
        # 为每个场景生成选择
        choices = [
            ("story_1_30", "驶向远方的迷雾", "story_2_31", 0, 0, 0, 0, 20, "", True),
            ("story_2_31", "小心地驶入迷雾", "story_2_32", 0, 0, 0, 0, 15, "", True),
            ("story_2_31", "绕过迷雾，寻找其他路线", "story_1_10", 0, 0, 0, 0, 10, "", True),
            ("story_2_32", "准备战斗", "story_2_33", 0, 0, 0, 0, 20, "", True),
            ("story_2_32", "尝试逃跑", "story_1_10", 0, 0, 5, 0, 5, "", True),
            ("story_2_33", "使用燧发枪攻击", "story_2_34", 0, 0, 10, 0, 50, "", True),
            ("story_2_33", "尝试用爪钩攻击", "story_2_34", 0, 0, 5, 0, 30, "", True),
            ("story_2_34", "上岛探索", "story_2_35", 0, 0, 0, 0, 30, "", True),
            ("story_2_34", "继续航行", "story_1_10", 0, 0, 0, 0, 20, "", True),
            ("story_2_35", "进入古塔", "story_2_36", 0, 0, 0, 0, 25, "", True),
            ("story_2_35", "在岛上休息", "story_2_38", 0, 0, 0, 20, 15, "", True),
            ("story_2_36", "爬向塔顶", "story_2_37", 0, 0, 0, 0, 35, "", True),
            ("story_2_36", "离开古塔", "story_2_35", 0, 0, 0, 0, 10, "", True),
            ("story_2_37", "触摸水晶", "story_2_38", 0, 0, 0, 0, 50, "", True),
            ("story_2_37", "不要触摸，离开", "story_2_38", 0, 0, 0, 0, 20, "", True),
            ("story_2_38", "开始新的航程", "story_3_39", 0, 0, 0, 0, 40, "", True),
            ("story_2_38", "在岛上多休息一天", "story_2_35", 0, 0, 0, 30, 25, "", True)
        ]
        
        for story_id, text, next_story, gold_cost, gold_reward, health_cost, health_reward, exp_reward, requirements, available in choices:
            choice_content += f"{story_id}|{text}|{next_story}|{gold_cost}|{gold_reward}|{health_cost}|{health_reward}|{exp_reward}|{requirements}|{str(available).lower()}\n"
        
        return story_content, choice_content
    
    def generate_chapter_3_content(self):
        """生成第3章内容 - 商人与交易"""
        chapter_3_stories = [
            (39, "商船相遇", "在新的航程中，你遇到了一艘商船。\\n\\n船上的商人向你挥手示意，看起来很友善。\\n\\n【商人喊话】：'朋友！要不要做点生意？我这里有很多好东西！'\\n\\n你可以选择与他们交易，或者继续你的航程。\\n\\n商船看起来装备精良，船员也很多。", "DIALOGUE", False),
            (40, "商人交易", "商人热情地欢迎你登上他的船。\\n\\n【商人】：'我叫马克，是这片海域的老商人了！'\\n\\n他向你展示了各种商品：\\n\\n【武器】燧发手枪 - 500金币\\n\\n【装备】皮甲 - 200金币\\n\\n【补给】食物包 - 50金币\\n\\n【道具】望远镜 - 150金币\\n\\n【特殊】神秘地图 - 1000金币", "TRADE", False),
            (41, "海盗袭击", "正当你们交易时，突然出现了三艘海盗船！\\n\\n【海盗船长大喊】：'交出所有财宝，否则送你们去见海神！'\\n\\n商人马克脸色苍白：'糟糕！是血鲨海盗团！'\\n\\n你现在有三个选择：\\n\\n1. 与商人联手对抗海盗\\n\\n2. 趁乱逃跑\\n\\n3. 尝试与海盗谈判", "COMBAT", False),
            (42, "联手战斗", "你决定与商人联手对抗海盗！\\n\\n【战斗开始】\\n\\n【敌人】：血鲨海盗 x6\\n\\n【等级】：3级\\n\\n【总生命值】：300\\n\\n商人马克也拿起了武器：'谢谢你，朋友！让这些海盗见识一下我们的厉害！'\\n\\n战斗异常激烈，炮火连天！", "COMBAT", False),
            (43, "战斗胜利", "经过激烈的战斗，你们成功击退了海盗！\\n\\n【获得经验：300】\\n\\n【获得金币：500】\\n\\n【获得声望：+50】\\n\\n商人马克感激地说：'你救了我们！作为感谢，这些东西送给你！'\\n\\n【获得：精制燧发枪】\\n\\n【获得：商人推荐信】\\n\\n【获得：海盗藏宝图】", "VICTORY", False),
            (44, "新的盟友", "马克成为了你的朋友和贸易伙伴。\\n\\n【马克】：'以后你可以在任何港口找到我的商店！'\\n\\n【解锁：商人网络】\\n\\n【解锁：特殊商品】\\n\\n你现在可以在各个港口进行更好的交易了。\\n\\n马克还告诉你一些有用的信息：'东边有个神秘的岛屿，据说那里有古老的宝藏...'", "ALLIANCE", False),
            (45, "分别", "你与马克告别，继续你的航海之旅。\\n\\n现在你装备更好，也有了可靠的盟友。\\n\\n海盗藏宝图显示，附近有一个隐藏的宝藏岛。\\n\\n你的冒险还在继续，更多的挑战和机遇等待着你。\\n\\n【第3章完成】", "CHAPTER_END", True)
        ]
        
        # 生成故事和选择内容
        story_content = "# 第3章数据文件 - 商人与交易\n# 格式: 场景号|标题|内容|类型|是否结局\n\n"
        for scene_id, title, content, story_type, is_ending in chapter_3_stories:
            story_content += f"{scene_id}|{title}|{content}|{story_type}|{str(is_ending).lower()}\n"
        
        choice_content = "# 第3章选择数据文件\n# 格式: 故事ID|选择文本|下一个故事ID|金币消耗|金币奖励|生命消耗|生命奖励|经验奖励|要求|是否可用\n\n"
        
        choices = [
            ("story_2_38", "向商船驶去", "story_3_39", 0, 0, 0, 0, 20, "", True),
            ("story_3_39", "登上商船交易", "story_3_40", 0, 0, 0, 0, 25, "", True),
            ("story_3_39", "礼貌拒绝，继续航行", "story_1_10", 0, 0, 0, 0, 10, "", True),
            ("story_3_40", "购买燧发手枪", "story_3_41", 500, 0, 0, 0, 30, "gold>=500", True),
            ("story_3_40", "购买神秘地图", "story_3_41", 1000, 0, 0, 0, 50, "gold>=1000", True),
            ("story_3_40", "只是看看，不买", "story_3_41", 0, 0, 0, 0, 15, "", True),
            ("story_3_41", "与商人联手对抗海盗", "story_3_42", 0, 0, 0, 0, 40, "", True),
            ("story_3_41", "趁乱逃跑", "story_1_10", 0, 0, 0, 0, 5, "", True),
            ("story_3_41", "尝试与海盗谈判", "story_3_42", 0, 0, 0, 0, 20, "", True),
            ("story_3_42", "全力战斗", "story_3_43", 0, 0, 15, 0, 60, "", True),
            ("story_3_42", "保守战斗", "story_3_43", 0, 0, 5, 0, 40, "", True),
            ("story_3_43", "接受商人的礼物", "story_3_44", 0, 0, 0, 0, 35, "", True),
            ("story_3_43", "礼貌拒绝礼物", "story_3_44", 0, 0, 0, 0, 25, "", True),
            ("story_3_44", "询问更多信息", "story_3_45", 0, 0, 0, 0, 30, "", True),
            ("story_3_44", "立即告别", "story_3_45", 0, 0, 0, 0, 20, "", True),
            ("story_3_45", "前往宝藏岛", "story_4_46", 0, 0, 0, 0, 45, "", True),
            ("story_3_45", "继续探索其他海域", "story_1_10", 0, 0, 0, 0, 25, "", True)
        ]
        
        for story_id, text, next_story, gold_cost, gold_reward, health_cost, health_reward, exp_reward, requirements, available in choices:
            choice_content += f"{story_id}|{text}|{next_story}|{gold_cost}|{gold_reward}|{health_cost}|{health_reward}|{exp_reward}|{requirements}|{str(available).lower()}\n"
        
        return story_content, choice_content
    
    def save_chapter_files(self, chapter_num, story_content, choice_content):
        """保存章节文件"""
        # 确保目录存在
        self.resources_path.mkdir(parents=True, exist_ok=True)
        
        # 保存故事文件
        story_file = self.resources_path / f"chapter_{chapter_num}_data.txt"
        with open(story_file, 'w', encoding='utf-8') as f:
            f.write(story_content)
        
        # 保存选择文件
        choice_file = self.resources_path / f"chapter_{chapter_num}_choices.txt"
        with open(choice_file, 'w', encoding='utf-8') as f:
            f.write(choice_content)
        
        print(f"✅ 第{chapter_num}章文件已生成：")
        print(f"   📖 故事文件：{story_file}")
        print(f"   🎯 选择文件：{choice_file}")
    
    def generate_all_chapters(self):
        """生成所有章节"""
        print("🚀 开始大规模内容生成...")
        
        # 生成第2章
        story_2, choice_2 = self.generate_chapter_2_content()
        self.save_chapter_files(2, story_2, choice_2)
        
        # 生成第3章
        story_3, choice_3 = self.generate_chapter_3_content()
        self.save_chapter_files(3, story_3, choice_3)
        
        print("🎉 前3章内容生成完成！")
        print("💡 现在可以继续生成更多章节...")

def main():
    generator = MassContentGenerator()
    generator.generate_all_chapters()

if __name__ == "__main__":
    main()
