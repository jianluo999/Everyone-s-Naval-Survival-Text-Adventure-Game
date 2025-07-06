package com.adventure.config;

import com.adventure.model.Choice;
import com.adventure.model.Story;
import com.adventure.model.Equipment;
import com.adventure.model.Player;
import com.adventure.model.Ship;
import com.adventure.model.GameState;
import com.adventure.model.Fish;
import com.adventure.model.Monster;
import com.adventure.repository.StoryRepository;
import com.adventure.repository.ChoiceRepository;
import com.adventure.repository.EquipmentRepository;
import com.adventure.repository.PlayerRepository;
import com.adventure.repository.FishRepository;
import com.adventure.repository.MonsterRepository;
import com.adventure.service.GameService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.io.*;
import java.nio.charset.StandardCharsets;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {
    
    @Autowired
    private StoryRepository storyRepository;
    
    @Autowired
    private ChoiceRepository choiceRepository;
    
    @Autowired
    private EquipmentRepository equipmentRepository;
    
    @Autowired
    private PlayerRepository playerRepository;
    
    @Autowired
    private FishRepository fishRepository;

    @Autowired
    private MonsterRepository monsterRepository;

    @Autowired
    private GameService gameService;
    
    @Override
    public void run(String... args) throws Exception {
        System.out.println("🎮 开始初始化游戏数据...");

        // 检查并创建游戏装备
        if (equipmentRepository.count() == 0) {
            createGameEquipment();
        } else {
            System.out.println("⚠️ 游戏装备已存在，跳过创建");
        }

        // 检查并创建基础游戏故事（story_1_1 到 story_1_3）
        if (storyRepository.findByStoryId("story_1_1").isEmpty()) {
            createBasicGameStories();
        } else {
            System.out.println("⚠️ 基础游戏故事已存在，跳过创建");
        }

        // 检查并创建批量故事（story_1_19 开始）
        if (storyRepository.findByStoryId("story_1_19").isEmpty()) {
            createBatchStories();
        } else {
            System.out.println("⚠️ 批量故事已存在，跳过创建");
        }

        // 检查并创建怪异鱼类
        if (fishRepository.count() == 0) {
            createStrangeFish();
        } else {
            System.out.println("⚠️ 怪异鱼类已存在，跳过创建");
        }

        // 检查并创建默认玩家
        if (playerRepository.count() == 0) {
            createDefaultPlayer();
        } else {
            System.out.println("⚠️ 默认玩家已存在，跳过创建");
        }

        System.out.println("✅ 游戏数据初始化完成！");
        System.out.println("📊 当前数据库状态：");
        System.out.println("   - 故事数量: " + storyRepository.count());
        System.out.println("   - 选择数量: " + choiceRepository.count());
        System.out.println("   - 装备数量: " + equipmentRepository.count());
        System.out.println("   - 鱼类数量: " + fishRepository.count());
        System.out.println("   - 玩家数量: " + playerRepository.count());
    }
    
    private void createBasicGameStories() {
        // 第一章第一场景：游戏开始（使用小说原文）
        Story story1_1 = new Story();
        story1_1.setStoryId("story_1_1");
        story1_1.setTitle("全民航海求生游戏");
        story1_1.setContent("「欢迎来到全民航海求生游戏....」\n\n" +
                "「接下来，你们将在海上度过余生.....」\n\n" +
                "「不必担心你们身体有疾病或者残缺，本系统会帮你们通通治好，给你们一个相对公平的起点.....」\n\n" +
                "「你们可以在海上自由航行，做你们想做的一切....」\n\n" +
                "「是成为无名小卒，还是名扬天下，这都取决于你自己....」\n\n" +
                "「大海会给你无限可能，你需要注意的事也只有一点。」\n\n" +
                "「保持前进，不要被背后的黑雾追上。」\n\n" +
                "「黑雾的速度目前为十节！」\n\n" +
                "奇特的声音从脑海响起。你苏醒过来，发现自己正躺在一张陈旧的床上。");
        story1_1.setChapter(1);
        story1_1.setScene(1);
        story1_1.setStoryType("AWAKENING");
        story1_1.setIsEnding(false);
        storyRepository.save(story1_1);

        // 第一章第二场景：苏醒
        Story story1_2 = new Story();
        story1_2.setStoryId("story_1_2");
        story1_2.setTitle("苏醒");
        story1_2.setContent("奇特的声音从脑海响起。\n\n" +
                "你苏醒过来，发现自己正躺在一张陈旧的床上。\n" +
                "你试着起身，却被带起的灰尘呛得咳嗽起来。\n\n" +
                "环顾四周，你发现自己在一处狭窄昏暗的破房子里。\n" +
                "不远处有一张桌子，上面躺着一具干枯的骸骨，左手还握着一把锈蚀的燧发枪，大半个颅骨不翼而飞，看起来是自杀身亡。\n\n" +
                "\"这是...？\"\n" +
                "你没有表露害怕，反倒看向自己消瘦的双手。\n" +
                "你竟然站起来了，这简直是奇迹！");
        story1_2.setChapter(1);
        story1_2.setScene(2);
        story1_2.setStoryType("AWAKENING");
        story1_2.setIsEnding(false);
        storyRepository.save(story1_2);

        // 第一章第三场景：身体恢复
        Story story1_3 = new Story();
        story1_3.setStoryId("story_1_3");
        story1_3.setTitle("身体恢复");
        story1_3.setContent("数分钟前，你还是瘫痪在床的病人，现在却奇迹般的恢复了健康！\n\n" +
                "在十二岁时，你被诊断出患有多发性硬化，到二十岁时，已完全瘫痪。\n" +
                "但你没有放弃自己的人生，一直用嘴玩游戏并直播，靠自己的赚的钱养活自己，一直到二十五岁。\n\n" +
                "你经常玩恐怖游戏，对不会动的骸骨尸体，没多大反应。\n\n" +
                "\"这声音说的....是真的！\"\n" +
                "你自语道，看向窗外。\n" +
                "那是一望无际的大海，时不时荡起浪涛。\n\n" +
                "与此同时，奇特的声音再度响起，男女难辨。");
        story1_3.setChapter(1);
        story1_3.setScene(3);
        story1_3.setStoryType("BACKGROUND");
        story1_3.setIsEnding(false);
        storyRepository.save(story1_3);

        // 第五个故事：世界聊天
        Story story1_5 = new Story();
        story1_5.setStoryId("story_1_5");
        story1_5.setTitle("世界聊天");
        story1_5.setContent("十几分钟后，混乱的发言渐渐变少，聊天变得有营养起来。\n\n" +
                "「你们手册的规则也是7条吗？」\n" +
                "「求抱团，有没有组队的！」\n" +
                "「距离太远，又没坐标，现在根本没法抱团！」\n" +
                "「我们应该分享情报，彼此帮助！」\n" +
                "「你们有检查过船了吗，我发现了一件装备。」\n\n" +
                "下面配了装备的信息。\n" +
                "【名称：染血的鱼叉】\n" +
                "【种类：遗物】\n" +
                "【品质：良品】（物品等级：普通，良品，精品，珍品，极品，英雄，大师.....）\n" +
                "【简介：很锋利，可对异魔造成微量伤害，然后激怒它们。】\n" +
                "注意：使用遗物，有降低理智的风险。\n\n" +
                "然后世界频道炸开了锅。\n" +
                "「异魔是什么？这世界有怪物？」\n" +
                "「我怎么啥都没有，只在船舱里找到了一些淡水，面包和蔬菜。」\n" +
                "「你有蔬菜？我怎么只有香肠？」");
        story1_5.setChapter(1);
        story1_5.setScene(5);
        story1_5.setStoryType("CHAT");
        story1_5.setIsEnding(false);
        storyRepository.save(story1_5);
        
        // 第六个故事：梦魇号
        Story story1_6 = new Story();
        story1_6.setStoryId("story_1_6");
        story1_6.setTitle("幽灵船梦魇号");
        story1_6.setContent("杨逸合上日志，也开始在房间翻找起来。\n" +
                "他发现骸骨手里的燧发枪是一件装备。\n\n" +
                "【名称：浸水锈蚀的燧发枪】\n" +
                "【种类：遗物】\n" +
                "【品质：精品】\n" +
                "【简介：这曾是一把大师之作，但泡水太久，锈蚀严重，只有五成概率能打响，可对异魔造成中量伤害。" +
                "这枪不需要子弹，自动装填时间为一分钟，弹容为1。】\n\n" +
                "杨逸表情严肃起来。正如公告所言，开局条件都是公平的。" +
                "那他得到这把枪，岂不是意味着地狱开局？\n\n" +
                "他推开桌上的骸骨，发现骸骨下方还压着一张纸，已经腐烂了，只有部分字迹勉强可以辨认。\n" +
                "\".....船上没补给了，我只能尝试钓鱼。\"\n" +
                "\"....今天运气不错，钓到一条老虎斑，足够吃两天了。\"\n" +
                "\".....嘿嘿，我钓到一把古董手枪，虽然枪声古怪，但看起来值不少钱！\"\n" +
                "后面是大片血迹，只看得见最后一行。\n" +
                "\"海里怎么会有这种东西？\"");
        story1_6.setChapter(2);
        story1_6.setScene(1);
        story1_6.setStoryType("DISCOVERY");
        story1_6.setIsEnding(false);
        storyRepository.save(story1_6);

        // 第七个故事：船只状态
        Story story1_7 = new Story();
        story1_7.setStoryId("story_1_7");
        story1_7.setTitle("船只状态");
        story1_7.setContent("杨逸看完后微微皱眉，起身走出船长室。\n" +
                "外边是甲板走廊，他抬头仔细打量自己的船只。\n\n" +
                "【梦魇号，一级，耐久300/300，容量400单位，航速40节】\n" +
                "【船体技能：\n" +
                "梦魇：船上睡觉会做噩梦，精力恢复效率-75%。\n" +
                "垂钓者的诅咒：这艘船被诅咒，钓不到正常的鱼。】\n" +
                "【简介：这艘船在海上漂了数百年，终于迎来了它的新主人....】\n\n" +
                "杨逸看完船只信息，脸色变得难看起来。这船是一艘幽灵船。\n" +
                "船体外侧布满藤壶海藻，不知多少年没清理了。\n" +
                "甲板也湿漉漉的，踩上去会发出嘎吱嘎吱的响声。\n" +
                "他玩过不少恐怖游戏。像这种场景，大概率藏有怪！\n" +
                "好在他搜了个遍，也没发现第二个能动的东西。");
        story1_7.setChapter(2);
        story1_7.setScene(2);
        story1_7.setStoryType("SHIP_STATUS");
        story1_7.setIsEnding(false);
        storyRepository.save(story1_7);

        // 第八个故事：钓鱼开始
        Story story1_8 = new Story();
        story1_8.setStoryId("story_1_8");
        story1_8.setTitle("你管这叫鱼？");
        story1_8.setContent("杨逸长舒一口气。他也不想刚开局，就和莫名其妙的生物，来一场酣畅淋漓的对决。\n\n" +
                "船只情况他也摸索清楚了。这船大概十二米长，由船舵，船长室、甲板、船舱几部分组成。\n" +
                "船舵位于船头甲板的平台，高出一截，视线良好。\n" +
                "后方则是船长室，里面有床和简单的家具。\n" +
                "再后面，则是船的中庭，竖立有一根高大的桅杆。\n" +
                "尾部则是船舱，直通船体内部，用于囤积货物。\n\n" +
                "杨逸进船舱看过，里面空无一物，连虫子都没有，只有一股潮湿恶心的霉味扑面而来。\n" +
                "他的开局，补给为0....毕竟这幽灵船在海上漂了不知多少年，如果有吃有喝，那才奇怪了！\n\n" +
                "杨逸打开日志，继续查看世界频道，想看看其他人有什么发现。");
        story1_8.setChapter(3);
        story1_8.setScene(1);
        story1_8.setStoryType("FISHING_START");
        story1_8.setIsEnding(false);
        storyRepository.save(story1_8);

        // 第九个故事：钓鱼发现
        Story story1_9 = new Story();
        story1_9.setStoryId("story_1_9");
        story1_9.setTitle("钓鱼发现");
        story1_9.setContent("聊天的人基本都在晒自己的船。大部分是普通船只，也有特殊船，其中有几艘船格外亮眼。\n\n" +
                "【疾风号，一级，耐久800/800，容量500单位，航速70节】\n" +
                "【船体技能：乘风破浪：船速增加100%，持续时间5分钟。】\n" +
                "【简介：你们连它尾气都吸不到，信我！】\n\n" +
                "这应该是目前最快的一艘船。其他白板船只，根据大小，船速都在30到40节左右，大的船只一般耐久高些，但速度慢一些。\n" +
                "杨逸的梦魇号，速度算是中等偏上。\n\n" +
                "通过查看聊天记录，可以判断。在这里钓鱼，能钓到很多不可思议的东西。甚至还有怪物。\n" +
                "杨逸已经有了心理准备，如果浮上来的东西不对劲，他立刻就切线。\n\n" +
                "他抄起鱼竿，准备钓鱼。");
        story1_9.setChapter(3);
        story1_9.setScene(2);
        story1_9.setStoryType("FISHING_PREP");
        story1_9.setIsEnding(false);
        storyRepository.save(story1_9);

        // 第十个故事：第一次钓鱼
        Story story1_10 = new Story();
        story1_10.setStoryId("story_1_10");
        story1_10.setTitle("第一次钓鱼");
        story1_10.setContent("杨逸深吸一口气，看了一眼自己的状态。\n" +
                "理智：100/100\n" +
                "精力：90/100\n\n" +
                "他还用日志的简易合成功能，用5木料做了一把简易长矛，以备不时之需。\n" +
                "同时燧发枪别在腰后。待会钓到巨物后，说不定要用物理手段降服。\n\n" +
                "钓饵的话，杨逸已经在日志里确认过了，这里钓鱼不需要鱼饵，应该是系统之力。\n" +
                "但挂上鱼饵的话，能提高钓鱼效率。\n\n" +
                "准备工作就绪。现在....开钓！\n" +
                "杨逸甩竿，鱼钩划出一道弧线，落入海里。\n" +
                "他并不是很擅长钓鱼，但现在...他有的是时间学习！\n\n" +
                "十五分钟过去，浮标一点动静都没有。");
        story1_10.setChapter(3);
        story1_10.setScene(3);
        story1_10.setStoryType("FIRST_FISHING");
        story1_10.setIsEnding(false);
        storyRepository.save(story1_10);

        // 第十一个故事：长腿沙丁鱼
        Story story1_11 = new Story();
        story1_11.setStoryId("story_1_11");
        story1_11.setTitle("长腿沙丁鱼");
        story1_11.setContent("几分钟后，浮标终于开始抖动，似乎有东西在咬钩。\n" +
                "杨逸屏息凝神。他手头有长矛，有手枪，只要是条鱼，应该就问题不大.....\n\n" +
                "浮标沉入，就是现在，拉竿！\n" +
                "杨逸大力一拉，死死盯着蔚蓝色的海面。\n" +
                "他没有看见什么巨大阴影，仅随手一拉就将那东西扯出了海面，简直毫无阻力。\n\n" +
                "甩上来的，是一条拇指粗细的小鱼，但不完全是鱼。\n" +
                "体长约三厘米，鱼身呈流线型，和一般沙丁鱼差不多。\n" +
                "可这鱼，两侧生有四条五厘米的大长腿，四足站立，站在船甲板上。\n\n" +
                "杨逸呆了，和这条鱼对视起来....\n" +
                "\"这是鱼?\"\n" +
                "【你发现一条怪鱼，理智下降2点。】\n\n" +
                "下一秒，这鱼娴熟使用自己的大长腿，往大海逃去，被杨逸一矛拍死在地上。");
        story1_11.setChapter(3);
        story1_11.setScene(4);
        story1_11.setStoryType("STRANGE_FISH");
        story1_11.setIsEnding(false);
        storyRepository.save(story1_11);

        // 第十二个故事：鱼类信息
        Story story1_12 = new Story();
        story1_12.setStoryId("story_1_12");
        story1_12.setTitle("鱼类信息");
        story1_12.setContent("【名称：长腿沙丁鱼】\n" +
                "【种类：食物】\n" +
                "【简介：深渊鱼种，据说经常吃它，可以变成大长腿。" +
                "可以吃，无毒，味道鲜美，但吃它需要勇气，可能降低理智。】\n\n" +
                "杨逸将鱼捏起，重量应该不到一百克，四条惨白的长腿已经骨折，结构和人类的腿一模一样，触感QQ弹弹。\n" +
                "\"这能吃？\"\n\n" +
                "杨逸想起了这艘船带的技能——垂钓者诅咒：将钓不到正常鱼类。\n" +
                "他用日志，拍下这条鱼的照片，分享到了世界频道。\n" +
                "\"请问你们有谁钓到过这种鱼吗？\"\n\n" +
                "一石激起千层浪。\n" +
                "\"卧槽，你这是什么东西，精神污染啊，理智-8。\"\n" +
                "\"你管这叫鱼？\"\n" +
                "\"你为什么要伤害我的眼睛，理智-10！\"\n" +
                "\"拉黑了！\"\n" +
                "\"拉黑！\"\n" +
                "\"此生不复见！\"");
        story1_12.setChapter(3);
        story1_12.setScene(5);
        story1_12.setStoryType("FISH_INFO");
        story1_12.setIsEnding(false);
        storyRepository.save(story1_12);

        // 第十三个故事：好友申请
        Story story1_13 = new Story();
        story1_13.setStoryId("story_1_13");
        story1_13.setTitle("好友申请");
        story1_13.setContent("杨逸瞬间被上十亿人拉黑，这些人或多或少，都有理智下降。\n" +
                "但有一人忽然私聊了过来。\n" +
                "\"你所在海域的海水是不是黑的？最好快些离开，否则可能遭到一些正体不明的怪物袭击！\"\n\n" +
                "杨逸看了一眼自己船下蔚蓝一片的大海，有几分无语。\n" +
                "\"并不是，我的船是幽灵船...\"\n\n" +
                "\"哇，你可以啊！加个好友呗！\"\n" +
                "疾风号船长徐达提交好友申请。\n\n" +
                "杨逸同意了，加个好友而已，并不会有任何损失。\n" +
                "\"你最好不要再发这种照片了，我理智只有54了，再跌就要发疯了。\"\n" +
                "\"知道了。\"\n\n" +
                "杨逸也意识到了事情的严重性，但为了食物和淡水，他必须继续钓鱼！");
        story1_13.setChapter(3);
        story1_13.setScene(6);
        story1_13.setStoryType("FRIEND_REQUEST");
        story1_13.setIsEnding(false);
        storyRepository.save(story1_13);

        // 第十四个故事：浸水的宝箱
        Story story1_14 = new Story();
        story1_14.setStoryId("story_1_14");
        story1_14.setTitle("浸水的宝箱");
        story1_14.setContent("这次钓了一个多小时，天色都开始变暗了。第一个夜晚即将到来。\n" +
                "杨逸现在饥肠辘辘，散落在一旁的长腿沙丁鱼在他眼中变得可口起来。\n" +
                "但吃这种鱼....大概率会掉理智。除非万不得已，他并不是很想吃，而且这船上，并也没有火炉，只能生吃....\n\n" +
                "浮标抖动，杨逸立刻有了精神。他用力一拉，一条黑色的鱼被拉了上来。\n" +
                "这次的鱼没大长腿，全是尖刺，体表黏糊糊的，像水肿的黏膜，刚掉在甲板上，那些黏膜就破掉了，流出黑色腥臭的脓液。\n\n" +
                "【这鱼很恶心，你理智下降2】\n" +
                "杨逸还没用长矛扎它，这鱼就抢先一步断了气。\n\n" +
                "【名称：囊肿刺豚】\n" +
                "【种类：食物】\n" +
                "【简介：深渊鱼类，它的体液含有剧毒，正常人不会吃它的，除非....不想活了。】");
        story1_14.setChapter(4);
        story1_14.setScene(1);
        story1_14.setStoryType("TREASURE_BOX");
        story1_14.setIsEnding(false);
        storyRepository.save(story1_14);

        // 第十五个故事：发现宝箱
        Story story1_15 = new Story();
        story1_15.setStoryId("story_1_15");
        story1_15.setTitle("发现宝箱");
        story1_15.setContent("\"有毒？\"杨逸不敢上手，用长矛将其刺穿，丢入了船舱。\n" +
                "同时，他还刻意把多刺了几次，直到把矛尖染成黑色，变成了一把剧毒木矛。\n\n" +
                "天色渐暗，离天黑只剩不到一小时了。系统强调过，夜晚会有危险，所以杨逸并不打算在晚上钓鱼。\n" +
                "可就在他收起钓竿，准备回船长室时，海面突然飘过一个特殊物体。\n\n" +
                "那是一个箱子，确切来说是一个宝箱，只有公文包大小，从梦魇号侧面飘过。\n" +
                "杨逸心头一紧，立刻来到船舵前，调转船头，追向那宝箱。\n" +
                "这机遇，可绝对不能错过了！\n\n" +
                "他操控船头的爪钩，抓向宝箱。可这宝箱却像活物一般，滑不溜秋，不断闪躲。\n" +
                "废了不少功夫，他才把宝箱抓了上来，立刻跑进船舱查看。");
        story1_15.setChapter(4);
        story1_15.setScene(2);
        story1_15.setStoryType("TREASURE_FOUND");
        story1_15.setIsEnding(false);
        storyRepository.save(story1_15);

        // 第十六个故事：人头章鱼
        Story story1_16 = new Story();
        story1_16.setStoryId("story_1_16");
        story1_16.setTitle("人头章鱼");
        story1_16.setContent("【名称：浸水的腐木宝箱】\n" +
                "【种类：宝箱】\n" +
                "【简介：这或许不是你想要的那种宝箱】\n\n" +
                "杨逸留了个心眼，一手持燧发枪对准宝箱，用长矛将其挑开。\n" +
                "里面装着的....是一个死人头，没有头发，皮肤呈灰白色，似乎有一层粘液附着在上面。\n\n" +
                "刚打开，这死人头就有了反应，睁开自己浑浊的眼眸，开始说话。\n" +
                "\"先生，能不能耽搁您几分钟，容我给您介绍一下全知全能的主？\"\n\n" +
                "【你不能理解它的话，理智下降5点】\n" +
                "杨逸头皮发麻，身体微颤。\n" +
                "\"先生，能不能...\"\n" +
                "下一瞬，这人头跳了出来，杨逸这才看清它的真身，那是一条章鱼，只是脑袋换成了人头，下面是一堆扭曲的触须。");
        story1_16.setChapter(4);
        story1_16.setScene(3);
        story1_16.setStoryType("HUMAN_HEAD_OCTOPUS");
        story1_16.setIsEnding(false);
        storyRepository.save(story1_16);

        // 第十七个故事：第一次噩梦
        Story story1_17 = new Story();
        story1_17.setStoryId("story_1_17");
        story1_17.setTitle("第一次噩梦");
        story1_17.setContent("癫狂状态下，你的力量、敏捷和体质都得到了提升，同时免疫恐惧和疼痛。\n\n" +
                "你冲进船舱，找到了人头章鱼的残骸，毫不犹豫地吞了下去。\n" +
                "【你吞下了人头章鱼，力量+1，体质+1，精神-1，理智-20，持续1分钟】\n\n" +
                "现在你的力量翻了一倍！你欺身上前，这时骷髅还在疑惑枪为何打不响。\n" +
                "下一秒，它被你扑倒在地，两根臂骨被狠狠扯下。\n\n" +
                "你得势不饶人，右手穿过骷髅颅骨的破口，抓向里面的灵魂之火...");
        story1_17.setChapter(1);
        story1_17.setScene(17);
        story1_17.setStoryType("MADNESS_BATTLE");
        story1_17.setIsEnding(false);
        storyRepository.save(story1_17);

        // 第十八个故事：夜晚的结束
        Story story1_18 = new Story();
        story1_18.setStoryId("story_1_18");
        story1_18.setTitle("恐怖夜晚的结束");
        story1_18.setContent("你握住了那团灵魂之火，并不烫手，反而很温暖。\n\n" +
                "骷髅反应剧烈，浑身战栗，很快散落一地，变成一摊平平无奇的骨头，\n" +
                "灵魂之火也彻底熄灭。\n\n" +
                "但你没有掉以轻心。保险起见，你将颅骨摆在船舷上，\n" +
                "两分钟后，果不其然，颅骨内重新亮起惨绿色的光芒。\n\n" +
                "你二话不说，果断开枪。\"嘭！\"火光迸射，枪声尖厉。\n" +
                "这颅骨直接被燧发枪轰成了碎渣。\n\n" +
                "【枪声古怪，你理智下降1】\n\n" +
                "终于，这恐怖的夜晚结束了。你虽然受了伤，但活了下来。\n" +
                "更重要的是，你学会了在这个危险世界中生存的第一课...");
        story1_18.setChapter(1);
        story1_18.setScene(18);
        story1_18.setStoryType("CHAPTER_END");
        story1_18.setIsEnding(true);
        storyRepository.save(story1_18);

        // 创建选择（现在不再需要双向关联）
        createChoices();

        // 创建怪物数据
        createMonsters();
    }
    
    private void createChoices() {
        // story_1_1 的选择
        Choice choice1_1_1 = new Choice();
        choice1_1_1.setText("立即打开航海日志，了解游戏规则");
        choice1_1_1.setNextStoryId("story_1_2");
        choice1_1_1.setGoldCost(0);
        choice1_1_1.setGoldReward(0);
        choice1_1_1.setHealthCost(0);
        choice1_1_1.setHealthReward(0);
        choice1_1_1.setExperienceReward(10);
        choice1_1_1.setRequirements("");
        choice1_1_1.setIsAvailable(true);
        choice1_1_1.setStoryId("story_1_1");
        choiceRepository.save(choice1_1_1);
        
        Choice choice1_1_2 = new Choice();
        choice1_1_2.setText("先检查船舱，看看有什么有用的物品");
        choice1_1_2.setNextStoryId("story_1_3");
        choice1_1_2.setGoldCost(0);
        choice1_1_2.setGoldReward(10);
        choice1_1_2.setHealthCost(0);
        choice1_1_2.setHealthReward(0);
        choice1_1_2.setExperienceReward(5);
        choice1_1_2.setRequirements("");
        choice1_1_2.setIsAvailable(true);
        choice1_1_2.setStoryId("story_1_1");
        choiceRepository.save(choice1_1_2);
        
        Choice choice1_1_3 = new Choice();
        choice1_1_3.setText("走到窗边，观察外面的海况");
        choice1_1_3.setNextStoryId("story_1_4");
        choice1_1_3.setGoldCost(0);
        choice1_1_3.setGoldReward(0);
        choice1_1_3.setHealthCost(0);
        choice1_1_3.setHealthReward(0);
        choice1_1_3.setExperienceReward(15);
        choice1_1_3.setRequirements("");
        choice1_1_3.setIsAvailable(true);
        choice1_1_3.setStoryId("story_1_1");
        choiceRepository.save(choice1_1_3);
        
        // story_1_2 的选择（修复循环问题）
        Choice choice1_2_1 = new Choice();
        choice1_2_1.setText("在世界聊天中发言，寻找其他玩家");
        choice1_2_1.setNextStoryId("story_1_5");
        choice1_2_1.setGoldCost(0);
        choice1_2_1.setGoldReward(0);
        choice1_2_1.setHealthCost(0);
        choice1_2_1.setHealthReward(0);
        choice1_2_1.setExperienceReward(20);
        choice1_2_1.setRequirements("");
        choice1_2_1.setIsAvailable(true);
        choice1_2_1.setStoryId("story_1_2");
        choiceRepository.save(choice1_2_1);
        
        Choice choice1_2_2 = new Choice();
        choice1_2_2.setText("开始探索你的船只，了解设备");
        choice1_2_2.setNextStoryId("story_1_6");
        choice1_2_2.setGoldCost(0);
        choice1_2_2.setGoldReward(0);
        choice1_2_2.setHealthCost(0);
        choice1_2_2.setHealthReward(0);
        choice1_2_2.setExperienceReward(10);
        choice1_2_2.setRequirements("");
        choice1_2_2.setIsAvailable(true);
        choice1_2_2.setStoryId("story_1_2");
        choiceRepository.save(choice1_2_2);
        
        Choice choice1_2_3 = new Choice();
        choice1_2_3.setText("立即启动船只，开始航行");
        choice1_2_3.setNextStoryId("story_1_7");
        choice1_2_3.setGoldCost(0);
        choice1_2_3.setGoldReward(0);
        choice1_2_3.setHealthCost(0);
        choice1_2_3.setHealthReward(0);
        choice1_2_3.setExperienceReward(15);
        choice1_2_3.setRequirements("");
        choice1_2_3.setIsAvailable(true);
        choice1_2_3.setStoryId("story_1_2");
        choiceRepository.save(choice1_2_3);
        
        // story_1_3 的选择
        Choice choice1_3_1 = new Choice();
        choice1_3_1.setText("继续阅读航海日志");
        choice1_3_1.setNextStoryId("story_1_2");
        choice1_3_1.setGoldCost(0);
        choice1_3_1.setGoldReward(0);
        choice1_3_1.setHealthCost(0);
        choice1_3_1.setHealthReward(10);
        choice1_3_1.setExperienceReward(15);
        choice1_3_1.setRequirements("");
        choice1_3_1.setIsAvailable(true);
        choice1_3_1.setStoryId("story_1_3");
        choiceRepository.save(choice1_3_1);
        
        // story_1_4 的选择
        Choice choice1_4_1 = new Choice();
        choice1_4_1.setText("回到船舱，查看航海日志");
        choice1_4_1.setNextStoryId("story_1_2");
        choice1_4_1.setGoldCost(0);
        choice1_4_1.setGoldReward(0);
        choice1_4_1.setHealthCost(0);
        choice1_4_1.setHealthReward(0);
        choice1_4_1.setExperienceReward(10);
        choice1_4_1.setRequirements("");
        choice1_4_1.setIsAvailable(true);
        choice1_4_1.setStoryId("story_1_4");
        choiceRepository.save(choice1_4_1);
        
        // story_1_5 的选择（聊天频道）
        Choice choice1_5_1 = new Choice();
        choice1_5_1.setText("在世界聊天中询问船只升级方法");
        choice1_5_1.setNextStoryId("story_1_6");
        choice1_5_1.setGoldCost(0);
        choice1_5_1.setGoldReward(0);
        choice1_5_1.setHealthCost(0);
        choice1_5_1.setHealthReward(0);
        choice1_5_1.setExperienceReward(15);
        choice1_5_1.setRequirements("");
        choice1_5_1.setIsAvailable(true);
        choice1_5_1.setStoryId("story_1_5");
        choiceRepository.save(choice1_5_1);
        
        Choice choice1_5_2 = new Choice();
        choice1_5_2.setText("询问关于夜晚雾气的信息");
        choice1_5_2.setNextStoryId("story_1_7");
        choice1_5_2.setGoldCost(0);
        choice1_5_2.setGoldReward(0);
        choice1_5_2.setHealthCost(0);
        choice1_5_2.setHealthReward(0);
        choice1_5_2.setExperienceReward(20);
        choice1_5_2.setRequirements("");
        choice1_5_2.setIsAvailable(true);
        choice1_5_2.setStoryId("story_1_5");
        choiceRepository.save(choice1_5_2);
        
        Choice choice1_5_3 = new Choice();
        choice1_5_3.setText("保持沉默，先观察情况");
        choice1_5_3.setNextStoryId("story_1_6");
        choice1_5_3.setGoldCost(0);
        choice1_5_3.setGoldReward(5);
        choice1_5_3.setHealthCost(0);
        choice1_5_3.setHealthReward(0);
        choice1_5_3.setExperienceReward(10);
        choice1_5_3.setRequirements("");
        choice1_5_3.setIsAvailable(true);
        choice1_5_3.setStoryId("story_1_5");
        choiceRepository.save(choice1_5_3);
        
        // story_1_6 的选择（船只探索）
        Choice choice1_6_1 = new Choice();
        choice1_6_1.setText("检查船只的耐久度和装备");
        choice1_6_1.setNextStoryId("story_1_7");
        choice1_6_1.setGoldCost(0);
        choice1_6_1.setGoldReward(0);
        choice1_6_1.setHealthCost(0);
        choice1_6_1.setHealthReward(0);
        choice1_6_1.setExperienceReward(15);
        choice1_6_1.setRequirements("");
        choice1_6_1.setIsAvailable(true);
        choice1_6_1.setStoryId("story_1_6");
        choiceRepository.save(choice1_6_1);
        
        Choice choice1_6_2 = new Choice();
        choice1_6_2.setText("尝试使用爪钩捕获附近的物品");
        choice1_6_2.setNextStoryId("story_1_7");
        choice1_6_2.setGoldCost(0);
        choice1_6_2.setGoldReward(10);
        choice1_6_2.setHealthCost(0);
        choice1_6_2.setHealthReward(0);
        choice1_6_2.setExperienceReward(20);
        choice1_6_2.setRequirements("");
        choice1_6_2.setIsAvailable(true);
        choice1_6_2.setStoryId("story_1_6");
        choiceRepository.save(choice1_6_2);
        
        Choice choice1_6_3 = new Choice();
        choice1_6_3.setText("开始准备航行");
        choice1_6_3.setNextStoryId("story_1_7");
        choice1_6_3.setGoldCost(0);
        choice1_6_3.setGoldReward(0);
        choice1_6_3.setHealthCost(0);
        choice1_6_3.setHealthReward(0);
        choice1_6_3.setExperienceReward(10);
        choice1_6_3.setRequirements("");
        choice1_6_3.setIsAvailable(true);
        choice1_6_3.setStoryId("story_1_6");
        choiceRepository.save(choice1_6_3);
        
        // story_1_7 的选择（初次航行）- 修复循环引用
        Choice choice1_7_1 = new Choice();
        choice1_7_1.setText("向东方的小岛航行");
        choice1_7_1.setNextStoryId("story_1_8"); // 修复：指向新的故事节点
        choice1_7_1.setGoldCost(0);
        choice1_7_1.setGoldReward(0);
        choice1_7_1.setHealthCost(0);
        choice1_7_1.setHealthReward(0);
        choice1_7_1.setExperienceReward(25);
        choice1_7_1.setRequirements("");
        choice1_7_1.setIsAvailable(true);
        choice1_7_1.setStoryId("story_1_7");
        choiceRepository.save(choice1_7_1);

        Choice choice1_7_2 = new Choice();
        choice1_7_2.setText("向北方的船只靠近");
        choice1_7_2.setNextStoryId("story_1_9"); // 修复：指向新的故事节点
        choice1_7_2.setGoldCost(0);
        choice1_7_2.setGoldReward(0);
        choice1_7_2.setHealthCost(0);
        choice1_7_2.setHealthReward(0);
        choice1_7_2.setExperienceReward(30);
        choice1_7_2.setRequirements("");
        choice1_7_2.setIsAvailable(true);
        choice1_7_2.setStoryId("story_1_7");
        choiceRepository.save(choice1_7_2);

        Choice choice1_7_3 = new Choice();
        choice1_7_3.setText("在当前位置等待，观察情况");
        choice1_7_3.setNextStoryId("story_1_10"); // 修复：指向新的故事节点
        choice1_7_3.setGoldCost(0);
        choice1_7_3.setGoldReward(0);
        choice1_7_3.setHealthCost(0);
        choice1_7_3.setHealthReward(0);
        choice1_7_3.setExperienceReward(15);
        choice1_7_3.setRequirements("");
        choice1_7_3.setIsAvailable(true);
        choice1_7_3.setStoryId("story_1_7");
        choiceRepository.save(choice1_7_3);

        // story_1_8 的选择（东方小岛的夜晚）
        Choice choice1_8_1 = new Choice();
        choice1_8_1.setText("尝试继续入睡，忽略不安的感觉");
        choice1_8_1.setNextStoryId("story_1_11");
        choice1_8_1.setGoldCost(0);
        choice1_8_1.setGoldReward(0);
        choice1_8_1.setHealthCost(0);
        choice1_8_1.setHealthReward(0);
        choice1_8_1.setExperienceReward(5);
        choice1_8_1.setRequirements("");
        choice1_8_1.setIsAvailable(true);
        choice1_8_1.setStoryId("story_1_8");
        choiceRepository.save(choice1_8_1);

        Choice choice1_8_2 = new Choice();
        choice1_8_2.setText("保持警觉，检查船舱周围");
        choice1_8_2.setNextStoryId("story_1_12");
        choice1_8_2.setGoldCost(0);
        choice1_8_2.setGoldReward(0);
        choice1_8_2.setHealthCost(0);
        choice1_8_2.setHealthReward(0);
        choice1_8_2.setExperienceReward(10);
        choice1_8_2.setRequirements("");
        choice1_8_2.setIsAvailable(true);
        choice1_8_2.setStoryId("story_1_8");
        choiceRepository.save(choice1_8_2);

        // story_1_11 的选择（噩梦后）
        Choice choice1_11_1 = new Choice();
        choice1_11_1.setText("立刻检查门口，看看是否有危险");
        choice1_11_1.setNextStoryId("story_1_12");
        choice1_11_1.setGoldCost(0);
        choice1_11_1.setGoldReward(0);
        choice1_11_1.setHealthCost(0);
        choice1_11_1.setHealthReward(0);
        choice1_11_1.setExperienceReward(15);
        choice1_11_1.setRequirements("");
        choice1_11_1.setIsAvailable(true);
        choice1_11_1.setStoryId("story_1_11");
        choiceRepository.save(choice1_11_1);

        // story_1_12 的选择（面对溺尸）
        Choice choice1_12_1 = new Choice();
        choice1_12_1.setText("立刻开枪射击溺尸");
        choice1_12_1.setNextStoryId("story_1_13");
        choice1_12_1.setGoldCost(0);
        choice1_12_1.setGoldReward(0);
        choice1_12_1.setHealthCost(0);
        choice1_12_1.setHealthReward(0);
        choice1_12_1.setExperienceReward(20);
        choice1_12_1.setRequirements("");
        choice1_12_1.setIsAvailable(true);
        choice1_12_1.setStoryId("story_1_12");
        choiceRepository.save(choice1_12_1);

        Choice choice1_12_2 = new Choice();
        choice1_12_2.setText("冲出船长室，到甲板上战斗");
        choice1_12_2.setNextStoryId("story_1_14");
        choice1_12_2.setGoldCost(0);
        choice1_12_2.setGoldReward(0);
        choice1_12_2.setHealthCost(0);
        choice1_12_2.setHealthReward(0);
        choice1_12_2.setExperienceReward(25);
        choice1_12_2.setRequirements("");
        choice1_12_2.setIsAvailable(true);
        choice1_12_2.setStoryId("story_1_12");
        choiceRepository.save(choice1_12_2);

        // story_1_13 的选择（枪械失效后）
        Choice choice1_13_1 = new Choice();
        choice1_13_1.setText("抄起长矛冲向溺尸，突破到甲板");
        choice1_13_1.setNextStoryId("story_1_14");
        choice1_13_1.setGoldCost(0);
        choice1_13_1.setGoldReward(0);
        choice1_13_1.setHealthCost(5);
        choice1_13_1.setHealthReward(0);
        choice1_13_1.setExperienceReward(20);
        choice1_13_1.setRequirements("");
        choice1_13_1.setIsAvailable(true);
        choice1_13_1.setStoryId("story_1_13");
        choiceRepository.save(choice1_13_1);

        // story_1_14 的选择（甲板战斗）
        Choice choice1_14_1 = new Choice();
        choice1_14_1.setText("利用甲板空间与溺尸周旋，寻找机会反击");
        choice1_14_1.setNextStoryId("story_1_15");
        choice1_14_1.setGoldCost(0);
        choice1_14_1.setGoldReward(0);
        choice1_14_1.setHealthCost(10);
        choice1_14_1.setHealthReward(0);
        choice1_14_1.setExperienceReward(30);
        choice1_14_1.setRequirements("");
        choice1_14_1.setIsAvailable(true);
        choice1_14_1.setStoryId("story_1_14");
        choiceRepository.save(choice1_14_1);

        // story_1_15 的选择（面对船长骸骨）
        Choice choice1_15_1 = new Choice();
        choice1_15_1.setText("进入癫狂状态，寻找能增强力量的物品");
        choice1_15_1.setNextStoryId("story_1_16");
        choice1_15_1.setGoldCost(0);
        choice1_15_1.setGoldReward(0);
        choice1_15_1.setHealthCost(0);
        choice1_15_1.setHealthReward(0);
        choice1_15_1.setExperienceReward(40);
        choice1_15_1.setRequirements("");
        choice1_15_1.setIsAvailable(true);
        choice1_15_1.setStoryId("story_1_15");
        choiceRepository.save(choice1_15_1);

        // story_1_16 的选择（癫狂战斗）
        Choice choice1_16_1 = new Choice();
        choice1_16_1.setText("抓住灵魂之火，彻底消灭船长骸骨");
        choice1_16_1.setNextStoryId("story_1_17");
        choice1_16_1.setGoldCost(0);
        choice1_16_1.setGoldReward(50);
        choice1_16_1.setHealthCost(0);
        choice1_16_1.setHealthReward(0);
        choice1_16_1.setExperienceReward(100);
        choice1_16_1.setRequirements("");
        choice1_16_1.setIsAvailable(true);
        choice1_16_1.setStoryId("story_1_16");
        choiceRepository.save(choice1_16_1);
    }

    private void createMonsters() {
        // 创建溺亡者
        Monster drownedSailor = new Monster();
        drownedSailor.setMonsterId("drowned_sailor");
        drownedSailor.setName("溺亡者");
        drownedSailor.setDescription("溺亡在海里的不幸之人，怀着对生者的怨念，重新站了起来。身体肿胀发臭，行动缓慢但力量惊人。");
        drownedSailor.setHealth(80);
        drownedSailor.setMaxHealth(80);
        drownedSailor.setAttack(15);
        drownedSailor.setDefense(5);
        drownedSailor.setSpeed(3);
        drownedSailor.setMonsterType("UNDEAD");
        drownedSailor.setAbilities("{\"self_destruct\": true, \"grab_attack\": true}");
        drownedSailor.setLoot("{\"experience\": 30, \"materials\": [\"腐烂的水手服\", \"海藻\"]}");
        drownedSailor.setSanityDamage(5);
        drownedSailor.setCanRevive(false);
        drownedSailor.setCanExplode(true);
        drownedSailor.setEncounterStoryId("story_1_12");
        monsterRepository.save(drownedSailor);

        // 创建船长遗骸
        Monster captainSkeleton = new Monster();
        captainSkeleton.setMonsterId("captain_skeleton");
        captainSkeleton.setName("船长的遗骸");
        captainSkeleton.setDescription("他曾经是一位酷爱钓鱼的船长，直到他钓到了不该钓的东西...现在他的骸骨重新站了起来。");
        captainSkeleton.setHealth(60);
        captainSkeleton.setMaxHealth(60);
        captainSkeleton.setAttack(12);
        captainSkeleton.setDefense(8);
        captainSkeleton.setSpeed(4);
        captainSkeleton.setMonsterType("UNDEAD");
        captainSkeleton.setAbilities("{\"fishing_rod_attack\": true, \"stealth\": true}");
        captainSkeleton.setLoot("{\"experience\": 40, \"materials\": [\"船长帽\", \"钓鱼竿\"]}");
        captainSkeleton.setSanityDamage(10);
        captainSkeleton.setCanRevive(true);
        captainSkeleton.setCanExplode(false);
        captainSkeleton.setEncounterStoryId("story_1_15");
        monsterRepository.save(captainSkeleton);
    }
    
    private void createGameEquipment() {
        // 创建基础装备
        Equipment rustySword = new Equipment();
        rustySword.setName("生锈的剑");
        rustySword.setType("武器");
        rustySword.setQuality("普通");
        rustySword.setDescription("一把生锈的剑，虽然锈迹斑斑，但依然锋利");
        rustySword.setAttack(5);
        rustySword.setDefense(0);
        rustySword.setDurability(50);
        rustySword.setMaxDurability(50);
        rustySword.setEquipSlot("武器");
        rustySword.setUsable(true);
        rustySword.setEquipped(false);
        rustySword.setPlayerId(null);
        
        Equipment leatherArmor = new Equipment();
        leatherArmor.setName("皮革护甲");
        leatherArmor.setType("防具");
        leatherArmor.setQuality("普通");
        leatherArmor.setDescription("简单的皮革护甲，能提供基本的防护");
        leatherArmor.setAttack(0);
        leatherArmor.setDefense(3);
        leatherArmor.setDurability(80);
        leatherArmor.setMaxDurability(80);
        leatherArmor.setEquipSlot("护甲");
        leatherArmor.setUsable(true);
        leatherArmor.setEquipped(false);
        leatherArmor.setPlayerId(null);
        
        Equipment fishingRod = new Equipment();
        fishingRod.setName("钓鱼竿");
        fishingRod.setType("工具");
        fishingRod.setQuality("普通");
        fishingRod.setDescription("简单的钓鱼竿，可以用来钓鱼获取食物");
        fishingRod.setAttack(0);
        fishingRod.setDefense(0);
        fishingRod.setDurability(100);
        fishingRod.setMaxDurability(100);
        fishingRod.setEquipSlot("工具");
        fishingRod.setUsable(true);
        fishingRod.setEquipped(false);
        fishingRod.setPlayerId(null);
        
        equipmentRepository.save(rustySword);
        equipmentRepository.save(leatherArmor);
        equipmentRepository.save(fishingRod);
    }
    
    private void createDefaultPlayer() {
        // 检查是否已有默认玩家
        if (playerRepository.count() > 0) {
            return;
        }
        
        System.out.println("🏴‍☠️ 创建默认玩家...");
        
        // 创建几个测试用的默认玩家
        String[] defaultNames = {"李船长", "王航海", "测试玩家"};
        
        for (String name : defaultNames) {
            try {
                Player player = gameService.createPlayer(name);
                System.out.println("✅ 创建玩家: " + name + " (ID: " + player.getId() + ")");
            } catch (Exception e) {
                System.err.println("❌ 创建玩家失败: " + name + " - " + e.getMessage());
            }
        }
        
        System.out.println("🎯 默认玩家创建完成！");
    }
    
    private void createStrangeFish() {
        // 检查是否已有鱼类数据
        if (fishRepository.count() > 0) {
            return;
        }
        
        System.out.println("🐟 创建怪异鱼类...");
        
        // 长腿沙丁鱼
        Fish longLegSardine = new Fish();
        longLegSardine.setName("长腿沙丁鱼");
        longLegSardine.setType("STRANGE");
        longLegSardine.setDescription("深渊鱼种，据说经常吃它，可以变成大长腿。可以吃，无毒，味道鲜美，但吃它需要勇气，可能降低理智。");
        longLegSardine.setRarity("COMMON");
        longLegSardine.setSize(3);
        longLegSardine.setWeight(0.1);
        longLegSardine.setIsEdible(true);
        longLegSardine.setIsToxic(false);
        longLegSardine.setHealthEffect(5);
        longLegSardine.setSanityEffect(-2);
        longLegSardine.setEnergyEffect(10);
        longLegSardine.setHungerRestore(15);
        longLegSardine.setThirstRestore(0);
        longLegSardine.setAgilityBonus(1);
        longLegSardine.setBonusDuration(30);
        longLegSardine.setCatchDifficulty(2);
        longLegSardine.setCatchProbability(0.6);
        longLegSardine.setCatchCondition("{}");
        longLegSardine.setSpecialEffects("{\"sanity_loss_on_catch\": 2}");
        fishRepository.save(longLegSardine);
        
        // 囊肿刺豚
        Fish cysticPufferfish = new Fish();
        cysticPufferfish.setName("囊肿刺豚");
        cysticPufferfish.setType("DANGEROUS");
        cysticPufferfish.setDescription("深渊鱼类，它的体液含有剧毒，正常人不会吃它的，除非....不想活了。");
        cysticPufferfish.setRarity("UNCOMMON");
        cysticPufferfish.setSize(8);
        cysticPufferfish.setWeight(0.5);
        cysticPufferfish.setIsEdible(false);
        cysticPufferfish.setIsToxic(true);
        cysticPufferfish.setHealthEffect(-50);
        cysticPufferfish.setSanityEffect(-5);
        cysticPufferfish.setEnergyEffect(-20);
        cysticPufferfish.setHungerRestore(0);
        cysticPufferfish.setThirstRestore(0);
        cysticPufferfish.setCatchDifficulty(4);
        cysticPufferfish.setCatchProbability(0.3);
        cysticPufferfish.setCatchCondition("{}");
        cysticPufferfish.setSpecialEffects("{\"sanity_loss_on_catch\": 5, \"poison_weapon\": true}");
        fishRepository.save(cysticPufferfish);
        
        // 人头章鱼
        Fish humanHeadOctopus = new Fish();
        humanHeadOctopus.setName("人头章鱼");
        humanHeadOctopus.setType("DANGEROUS");
        humanHeadOctopus.setDescription("深渊鱼种，不要试图去理解它的话，那不过是为了偷袭你，分散你注意力的手段。可食用，可作为素材，微毒性，吃下后力量暂时+1，体质+1，精神-1，理智-20。");
        humanHeadOctopus.setRarity("RARE");
        humanHeadOctopus.setSize(15);
        humanHeadOctopus.setWeight(1.2);
        humanHeadOctopus.setIsEdible(true);
        humanHeadOctopus.setIsToxic(true);
        humanHeadOctopus.setHealthEffect(0);
        humanHeadOctopus.setSanityEffect(-20);
        humanHeadOctopus.setEnergyEffect(0);
        humanHeadOctopus.setHungerRestore(25);
        humanHeadOctopus.setThirstRestore(0);
        humanHeadOctopus.setStrengthBonus(1);
        humanHeadOctopus.setConstitutionBonus(1);
        humanHeadOctopus.setSpiritBonus(-1);
        humanHeadOctopus.setBonusDuration(60);
        humanHeadOctopus.setCatchDifficulty(7);
        humanHeadOctopus.setCatchProbability(0.1);
        humanHeadOctopus.setCatchCondition("{}");
        humanHeadOctopus.setSpecialEffects("{\"sanity_loss_on_catch\": 10, \"speaks_strange_words\": true}");
        fishRepository.save(humanHeadOctopus);
        
        // 普通海鲈鱼（作为对比）
        Fish normalSeaBass = new Fish();
        normalSeaBass.setName("海鲈鱼");
        normalSeaBass.setType("NORMAL");
        normalSeaBass.setDescription("一条普通的海鲈鱼，新鲜美味，是很好的食物来源。");
        normalSeaBass.setRarity("COMMON");
        normalSeaBass.setSize(25);
        normalSeaBass.setWeight(2.0);
        normalSeaBass.setIsEdible(true);
        normalSeaBass.setIsToxic(false);
        normalSeaBass.setHealthEffect(10);
        normalSeaBass.setSanityEffect(0);
        normalSeaBass.setEnergyEffect(15);
        normalSeaBass.setHungerRestore(30);
        normalSeaBass.setThirstRestore(5);
        normalSeaBass.setCatchDifficulty(3);
        normalSeaBass.setCatchProbability(0.8);
        normalSeaBass.setCatchCondition("{}");
        normalSeaBass.setSpecialEffects("{}");
        fishRepository.save(normalSeaBass);
        
        // 深海怪鱼
        Fish deepSeaMonster = new Fish();
        deepSeaMonster.setName("深海怪鱼");
        deepSeaMonster.setType("DANGEROUS");
        deepSeaMonster.setDescription("来自深海的可怕生物，体型巨大，具有攻击性。不建议新手钓鱼者尝试。");
        deepSeaMonster.setRarity("LEGENDARY");
        deepSeaMonster.setSize(100);
        deepSeaMonster.setWeight(50.0);
        deepSeaMonster.setIsEdible(true);
        deepSeaMonster.setIsToxic(false);
        deepSeaMonster.setHealthEffect(50);
        deepSeaMonster.setSanityEffect(-10);
        deepSeaMonster.setEnergyEffect(30);
        deepSeaMonster.setHungerRestore(100);
        deepSeaMonster.setThirstRestore(0);
        deepSeaMonster.setStrengthBonus(2);
        deepSeaMonster.setConstitutionBonus(2);
        deepSeaMonster.setBonusDuration(120);
        deepSeaMonster.setCatchDifficulty(10);
        deepSeaMonster.setCatchProbability(0.05);
        deepSeaMonster.setCatchCondition("{}");
        deepSeaMonster.setSpecialEffects("{\"sanity_loss_on_catch\": 15, \"requires_weapon\": true}");
        fishRepository.save(deepSeaMonster);
        
        System.out.println("🐟 怪异鱼类创建完成！");
    }

    // ==================== 批量生成的故事内容 ====================
    /**
     * 数据驱动的故事创建方法 - 从文本文件批量加载
     */
    private void createBatchStories() {
        System.out.println("📚 开始从文本文件批量加载故事内容...");

        try {
            // 从文本文件加载故事数据
            loadStoriesFromTextFiles();
            System.out.println("✅ 批量故事内容加载完成！");

            // 加载选择数据
            createBatchChoices();
        } catch (Exception e) {
            System.err.println("❌ 批量加载故事失败: " + e.getMessage());
            e.printStackTrace();
            // 如果批量加载失败，使用默认故事
            createDefaultBatchStories();
        }
    }

    /**
     * 从文本文件加载故事
     */
    private void loadStoriesFromTextFiles() {
        // 读取第1章的所有场景
        loadChapterFromFile(1, "novel_texts/chapter_1_data.txt");

        // 读取第2章到第11章
        for (int i = 2; i <= 11; i++) {
            loadChapterFromFile(i, "novel_texts/chapter_" + i + "_data.txt");
        }

        // 可以继续添加更多章节
        // loadChapterFromFile(12, "novel_texts/chapter_12_data.txt");
        // loadChapterFromFile(13, "novel_texts/chapter_13_data.txt");
        // ... 直到500章

        System.out.println("📖 已加载11个章节，文本文件系统支持无限扩展！");
    }

    /**
     * 从文件加载指定章节的故事
     */
    private void loadChapterFromFile(int chapter, String filePath) {
        try {
            // 尝试从类路径读取文件
            InputStream inputStream = getClass().getClassLoader().getResourceAsStream(filePath);
            if (inputStream == null) {
                System.out.println("⚠️ 文件不存在，使用默认数据: " + filePath);
                loadDefaultChapterData(chapter);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
            String line;
            int sceneCount = 0;

            while ((line = reader.readLine()) != null) {
                line = line.trim();
                // 跳过注释和空行
                if (line.startsWith("#") || line.isEmpty()) {
                    continue;
                }

                // 解析数据行：场景号|标题|内容|类型|是否结局
                String[] parts = line.split("\\|", 5);
                if (parts.length >= 5) {
                    int scene = Integer.parseInt(parts[0]);
                    String title = parts[1];
                    String content = parts[2].replace("\\n\\n", "\n\n");
                    String type = parts[3];
                    boolean isEnding = Boolean.parseBoolean(parts[4]);

                    createStoryFromData(chapter, scene, title, content, type, isEnding);
                    sceneCount++;
                }
            }
            reader.close();

            System.out.println("✅ 从文件加载第" + chapter + "章，共" + sceneCount + "个场景");

        } catch (Exception e) {
            System.err.println("❌ 读取文件失败: " + filePath + " - " + e.getMessage());
            loadDefaultChapterData(chapter);
        }
    }

    /**
     * 加载默认章节数据（备用方案）
     */
    private void loadDefaultChapterData(int chapter) {
        System.out.println("📚 使用第" + chapter + "章默认数据...");

        // 第1章默认数据
        if (chapter == 1) {
            createStoryFromData(1, 18, "航海日志详细规则",
                "你将它拿起，打开，第一页写有规则。\n\n" +
                "【1.未经允许，其他人无法登上你的船只。】\n\n" +
                "【2.你船上的物品不会被其他玩家盗窃，除非你已死亡。】\n\n" +
                "【3.每艘船都装有爪钩，耐久无限，大胆抓向飘来的物品吧！】\n\n" +
                "【4.你需要升级强化您的船只，让它看起来足够安全。】\n\n" +
                "【5.要小心夜晚，当心雾气，一旦陷入后方黑雾，你将会死亡。】\n\n" +
                "【6.本手册灵魂绑定，可在脑海中翻阅。】\n\n" +
                "【7.在海上，你永远不会感到寂寞。】",
                "TUTORIAL", false);

            createStoryFromData(1, 19, "属性详情",
                "这册子摸起来像皮肤，你往后翻去。\n\n" +
                "第二页，是当天的天气情况，暂且略过。\n\n" +
                "第三页，则是状态信息。\n\n" +
                "你\n\n状态：健康『一个大字型人体图案，全部是绿色』",
                "TUTORIAL", false);
        }
    }

    /**
     * 通用的故事创建方法 - 消除重复代码
     */
    private void createStoryFromData(int chapter, int scene, String title, String content, String type, boolean isEnding) {
        Story story = new Story();
        story.setStoryId("story_" + chapter + "_" + scene);
        story.setTitle(title);
        story.setContent(content);
        story.setChapter(chapter);
        story.setScene(scene);
        story.setStoryType(type);
        story.setIsEnding(isEnding);
        storyRepository.save(story);

        System.out.println("✅ 创建故事: " + title + " (第" + chapter + "章第" + scene + "场景)");
    }

    /**
     * 默认的批量故事创建（备用方案）
     */
    private void createDefaultBatchStories() {
        System.out.println("📚 使用默认批量故事内容...");

        // 检查是否已经有批量故事，避免重复创建
        if (storyRepository.findByStoryId("story_1_19").isPresent()) {
            System.out.println("⚠️ 批量故事已存在，跳过默认创建");
            return;
        }

        // 第1章第23场景：航海日志详细规则（修复重复ID问题）
        createStoryFromData(1, 23, "航海日志详细规则",
            "你将它拿起，打开，第一页写有规则。\n\n" +
            "【1.未经允许，其他人无法登上你的船只。】\n\n" +
            "【2.你船上的物品不会被其他玩家盗窃，除非你已死亡。】\n\n" +
            "【3.每艘船都装有爪钩，耐久无限，大胆抓向飘来的物品吧！】\n\n" +
            "【4.你需要升级强化您的船只，让它看起来足够安全。】\n\n" +
            "【5.要小心夜晚，当心雾气，一旦陷入后方黑雾，你将会死亡。】\n\n" +
            "【6.本手册灵魂绑定，可在脑海中翻阅。】\n\n" +
            "【7.在海上，你永远不会感到寂寞。】",
            "TUTORIAL", false);

        // 第1章第19场景：属性详情
        Story story1_19 = new Story();
        story1_19.setStoryId("story_1_19");
        story1_19.setTitle("属性详情");
        story1_19.setContent("这册子摸起来像皮肤，你往后翻去。\n\n" +
                "第二页，是当天的天气情况，暂且略过。\n\n" +
                "第三页，则是状态信息。\n\n" +
                "你\n\n" +
                "状态：健康『一个大字型人体图案，全部是绿色』\n\n" +
                "（成年人属性各项平均值为5，可以通过后天锻炼提升到10。）\n\n" +
                "（属性10是凡物的极限。）\n\n" +
                "力量：3（0/50）\n\n" +
                "精神：7+1（0/8000）  （精神越高，理智抗性越高，同时理智恢复速度加快）\n\n" +
                "敏捷：4（0/100）\n\n" +
                "体质：3（0/50）\n\n" +
                "感知：5（0/200）");
        story1_19.setChapter(1);
        story1_19.setScene(19);
        story1_19.setStoryType("STATUS");
        story1_19.setIsEnding(false);
        storyRepository.save(story1_19);

        // 第1章第20场景：理智与天赋
        Story story1_20 = new Story();
        story1_20.setStoryId("story_1_20");
        story1_20.setTitle("理智与天赋");
        story1_20.setContent("理智：100/100（理智低于50将疯狂，低于30将产生自杀念头，低于10....）\n\n" +
                "精力：100/100（精力低于50将困倦，低于30可能昏厥。）\n\n" +
                "气血：100/100\n\n" +
                "天赋：\n\n" +
                "钢铁意志：你永不服输，精神上限+1，你理智至少会保留1点，且不会自杀，理智大量降低（低于50），会进入癫狂状态。\n\n" +
                "你看完属性界面，稍微安心。\n\n" +
                "低属性所需经验很少，这样你追属性也不会太难。\n\n" +
                "你继续往后翻，找到了聊天频道。");
        story1_20.setChapter(1);
        story1_20.setScene(20);
        story1_20.setStoryType("STATUS");
        story1_20.setIsEnding(false);
        storyRepository.save(story1_20);

        // 第1章第21场景：世界聊天
        Story story1_21 = new Story();
        story1_21.setStoryId("story_1_21");
        story1_21.setTitle("世界聊天");
        story1_21.setContent("里面分为世界聊天，区域聊天，和私密聊天。\n\n" +
                "目前世界频道最热闹，陆续有人发言。\n\n" +
                "\"有人吗？\"\n\n" +
                "\"这到底是什么情况？\"\n\n" +
                "\"我刚刚在拉屎，还没擦屁股呢，转眼间就到船上了！\"\n\n" +
                "\"这里就我一个人，你们谁有手机吗，帮我报个警！\"\n\n" +
                "\"谁绑架的我，你知道我爸是谁吗？\"\n\n" +
                "\"说不定你爸也一起过来了！\"\n\n" +
                "\"儿子，是你吗？\"\n\n" +
                "\"别瞎认！\"\n\n" +
                "\"我骨折的手居然好了....\"\n\n" +
                "\"有痛觉...这不是梦！\"");
        story1_21.setChapter(1);
        story1_21.setScene(21);
        story1_21.setStoryType("CHAT");
        story1_21.setIsEnding(false);
        storyRepository.save(story1_21);

        // 第1章第22场景：情报收集
        Story story1_22 = new Story();
        story1_22.setStoryId("story_1_22");
        story1_22.setTitle("情报收集");
        story1_22.setContent("在线人数高达几十亿，估计所有人都被拉了进来。\n\n" +
                "你没有急着发话，而是在看聊天信息，收集潜在的情报。\n\n" +
                "每人每天，只能发10条世界信息，再多就得支付海螺币了，一百海螺币一条\n\n" +
                "这海螺币是什么东西，你不清楚，手上也没有。\n\n" +
                "十几分钟后，混乱的发言渐渐变少，聊天变得有营养起来。\n\n" +
                "\"你们手册的规则也是7条吗？\"\n\n" +
                "\"求抱团，有没有组队的！\"\n\n" +
                "\"距离太远，又没坐标，现在根本没法抱团！\"\n\n" +
                "\"我们应该分享情报，彼此帮助！\"");
        story1_22.setChapter(1);
        story1_22.setScene(22);
        story1_22.setStoryType("CHAT");
        story1_22.setIsEnding(false);
        storyRepository.save(story1_22);

        System.out.println("✅ 批量故事内容加载完成！");
    }

    // ==================== 批量生成的选择内容 ====================
    /**
     * 数据驱动的选择创建方法 - 从文本文件批量加载
     */
    private void createBatchChoices() {
        System.out.println("🎯 开始从文本文件批量加载选择内容...");

        try {
            // 从文本文件加载选择数据
            loadChoicesFromTextFiles();
            System.out.println("✅ 批量选择内容加载完成！");
        } catch (Exception e) {
            System.err.println("❌ 批量加载选择失败: " + e.getMessage());
            e.printStackTrace();
            // 如果批量加载失败，使用默认选择
            createDefaultBatchChoices();
        }
    }

    /**
     * 从文本文件加载选择
     */
    private void loadChoicesFromTextFiles() {
        // 读取第1章的所有选择
        loadChapterChoicesFromFile(1, "novel_texts/chapter_1_choices.txt");

        // 读取第2章的选择 - 深海探索
        loadChapterChoicesFromFile(2, "novel_texts/chapter_2_choices.txt");

        // 读取第3章的选择 - 商人与交易
        loadChapterChoicesFromFile(3, "novel_texts/chapter_3_choices.txt");

        // 读取第4章的选择 - 宝藏岛探险
        loadChapterChoicesFromFile(4, "novel_texts/chapter_4_choices.txt");

        // 读取第5章的选择 - 海怪之王
        loadChapterChoicesFromFile(5, "novel_texts/chapter_5_choices.txt");

        // 可以继续添加更多章节的选择
        // loadChapterChoicesFromFile(6, "novel_texts/chapter_6_choices.txt");
        // loadChapterChoicesFromFile(7, "novel_texts/chapter_7_choices.txt");
        // ... 直到500章

        System.out.println("🎯 已加载5个章节的选择，选择文件系统支持无限扩展！");
    }

    /**
     * 从文件加载指定章节的选择
     */
    private void loadChapterChoicesFromFile(int chapter, String filePath) {
        try {
            // 尝试从类路径读取文件
            InputStream inputStream = getClass().getClassLoader().getResourceAsStream(filePath);
            if (inputStream == null) {
                System.out.println("⚠️ 选择文件不存在，使用默认数据: " + filePath);
                loadDefaultChapterChoices(chapter);
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
            String line;
            int choiceCount = 0;

            while ((line = reader.readLine()) != null) {
                line = line.trim();
                // 跳过注释和空行
                if (line.startsWith("#") || line.isEmpty()) {
                    continue;
                }

                // 解析数据行：故事ID|选择文本|下一个故事ID|金币消耗|金币奖励|生命消耗|生命奖励|经验奖励|要求|是否可用
                String[] parts = line.split("\\|", 10);
                if (parts.length >= 10) {
                    String storyId = parts[0];
                    String text = parts[1];
                    String nextStoryId = parts[2];
                    int goldCost = Integer.parseInt(parts[3]);
                    int goldReward = Integer.parseInt(parts[4]);
                    int healthCost = Integer.parseInt(parts[5]);
                    int healthReward = Integer.parseInt(parts[6]);
                    int experienceReward = Integer.parseInt(parts[7]);
                    String requirements = parts[8];
                    boolean isAvailable = Boolean.parseBoolean(parts[9]);

                    createChoiceFromData(storyId, text, nextStoryId, goldCost, goldReward,
                                       healthCost, healthReward, experienceReward, requirements, isAvailable);
                    choiceCount++;
                }
            }
            reader.close();

            System.out.println("✅ 从文件加载第" + chapter + "章选择，共" + choiceCount + "个选择");

        } catch (Exception e) {
            System.err.println("❌ 读取选择文件失败: " + filePath + " - " + e.getMessage());
            loadDefaultChapterChoices(chapter);
        }
    }

    /**
     * 通用的选择创建方法 - 消除重复代码
     */
    private void createChoiceFromData(String storyId, String text, String nextStoryId,
                                    int goldCost, int goldReward, int healthCost, int healthReward,
                                    int experienceReward, String requirements, boolean isAvailable) {
        Choice choice = new Choice();
        choice.setText(text);
        choice.setNextStoryId(nextStoryId);
        choice.setGoldCost(goldCost);
        choice.setGoldReward(goldReward);
        choice.setHealthCost(healthCost);
        choice.setHealthReward(healthReward);
        choice.setExperienceReward(experienceReward);
        choice.setRequirements(requirements);
        choice.setIsAvailable(isAvailable);
        choice.setStoryId(storyId);
        choiceRepository.save(choice);

        System.out.println("✅ 创建选择: " + text + " (从 " + storyId + " 到 " + nextStoryId + ")");
    }

    /**
     * 默认的批量选择创建（备用方案）
     */
    private void createDefaultBatchChoices() {
        System.out.println("🎯 使用默认批量选择内容...");

        // 第1章默认选择
        loadDefaultChapterChoices(1);
    }

    /**
     * 加载默认章节选择数据（备用方案）
     */
    private void loadDefaultChapterChoices(int chapter) {
        System.out.println("🎯 使用第" + chapter + "章默认选择数据...");

        // 第1章默认选择
        if (chapter == 1) {
            // story_1_3 添加新选择：详细阅读航海日志规则
            createChoiceFromData("story_1_3", "详细阅读航海日志的所有规则", "story_1_23",
                               0, 0, 0, 0, 15, "", true);

            // story_1_23 的选择：阅读完规则后的选择
            createChoiceFromData("story_1_23", "翻到第三页，查看自己的属性详情", "story_1_19",
                               0, 0, 0, 0, 10, "", true);
            createChoiceFromData("story_1_23", "合上手册，开始探索船舱", "story_1_6",
                               0, 0, 0, 0, 5, "", true);
        }
    }

    // ==================== 原有的硬编码选择内容（保留作为备用） ====================
    private void createLegacyBatchChoices() {
        System.out.println("🎯 开始加载传统硬编码选择内容...");

        // story_1_23 的选择：阅读完规则后的选择（修复重复ID问题）
        Choice choice1_23_1 = new Choice();
        choice1_23_1.setText("翻到第三页，查看自己的属性详情");
        choice1_23_1.setNextStoryId("story_1_19");
        choice1_23_1.setGoldCost(0);
        choice1_23_1.setGoldReward(0);
        choice1_23_1.setHealthCost(0);
        choice1_23_1.setHealthReward(0);
        choice1_23_1.setExperienceReward(10);
        choice1_23_1.setRequirements("");
        choice1_23_1.setIsAvailable(true);
        choice1_23_1.setStoryId("story_1_23");
        choiceRepository.save(choice1_23_1);

        Choice choice1_23_2 = new Choice();
        choice1_23_2.setText("合上手册，开始探索船舱");
        choice1_23_2.setNextStoryId("story_1_6");
        choice1_23_2.setGoldCost(0);
        choice1_23_2.setGoldReward(0);
        choice1_23_2.setHealthCost(0);
        choice1_23_2.setHealthReward(0);
        choice1_23_2.setExperienceReward(5);
        choice1_23_2.setRequirements("");
        choice1_23_2.setIsAvailable(true);
        choice1_23_2.setStoryId("story_1_23");
        choiceRepository.save(choice1_23_2);

        // story_1_19 的选择：查看完属性后的选择
        Choice choice1_19_1 = new Choice();
        choice1_19_1.setText("继续往后翻，查看理智和天赋详情");
        choice1_19_1.setNextStoryId("story_1_20");
        choice1_19_1.setGoldCost(0);
        choice1_19_1.setGoldReward(0);
        choice1_19_1.setHealthCost(0);
        choice1_19_1.setHealthReward(0);
        choice1_19_1.setExperienceReward(15);
        choice1_19_1.setRequirements("");
        choice1_19_1.setIsAvailable(true);
        choice1_19_1.setStoryId("story_1_19");
        choiceRepository.save(choice1_19_1);

        Choice choice1_19_2 = new Choice();
        choice1_19_2.setText("合上手册，开始探索船舱");
        choice1_19_2.setNextStoryId("story_1_6");
        choice1_19_2.setGoldCost(0);
        choice1_19_2.setGoldReward(0);
        choice1_19_2.setHealthCost(0);
        choice1_19_2.setHealthReward(0);
        choice1_19_2.setExperienceReward(10);
        choice1_19_2.setRequirements("");
        choice1_19_2.setIsAvailable(true);
        choice1_19_2.setStoryId("story_1_19");
        choiceRepository.save(choice1_19_2);

        // story_1_20 的选择：查看完理智天赋后的选择
        Choice choice1_20_1 = new Choice();
        choice1_20_1.setText("继续往后翻，查看聊天频道");
        choice1_20_1.setNextStoryId("story_1_21");
        choice1_20_1.setGoldCost(0);
        choice1_20_1.setGoldReward(0);
        choice1_20_1.setHealthCost(0);
        choice1_20_1.setHealthReward(0);
        choice1_20_1.setExperienceReward(10);
        choice1_20_1.setRequirements("");
        choice1_20_1.setIsAvailable(true);
        choice1_20_1.setStoryId("story_1_20");
        choiceRepository.save(choice1_20_1);

        Choice choice1_20_2 = new Choice();
        choice1_20_2.setText("合上手册，开始探索船舱");
        choice1_20_2.setNextStoryId("story_1_6");
        choice1_20_2.setGoldCost(0);
        choice1_20_2.setGoldReward(0);
        choice1_20_2.setHealthCost(0);
        choice1_20_2.setHealthReward(0);
        choice1_20_2.setExperienceReward(5);
        choice1_20_2.setRequirements("");
        choice1_20_2.setIsAvailable(true);
        choice1_20_2.setStoryId("story_1_20");
        choiceRepository.save(choice1_20_2);

        // story_1_21 的选择：看完聊天后的选择
        Choice choice1_21_1 = new Choice();
        choice1_21_1.setText("继续观察聊天，收集更多情报");
        choice1_21_1.setNextStoryId("story_1_22");
        choice1_21_1.setGoldCost(0);
        choice1_21_1.setGoldReward(0);
        choice1_21_1.setHealthCost(0);
        choice1_21_1.setHealthReward(0);
        choice1_21_1.setExperienceReward(15);
        choice1_21_1.setRequirements("");
        choice1_21_1.setIsAvailable(true);
        choice1_21_1.setStoryId("story_1_21");
        choiceRepository.save(choice1_21_1);

        Choice choice1_21_2 = new Choice();
        choice1_21_2.setText("合上手册，开始行动");
        choice1_21_2.setNextStoryId("story_1_6");
        choice1_21_2.setGoldCost(0);
        choice1_21_2.setGoldReward(0);
        choice1_21_2.setHealthCost(0);
        choice1_21_2.setHealthReward(0);
        choice1_21_2.setExperienceReward(10);
        choice1_21_2.setRequirements("");
        choice1_21_2.setIsAvailable(true);
        choice1_21_2.setStoryId("story_1_21");
        choiceRepository.save(choice1_21_2);

        // story_1_22 的选择：收集完情报后的选择
        Choice choice1_22_1 = new Choice();
        choice1_22_1.setText("合上手册，开始探索船舱");
        choice1_22_1.setNextStoryId("story_1_6");
        choice1_22_1.setGoldCost(0);
        choice1_22_1.setGoldReward(0);
        choice1_22_1.setHealthCost(0);
        choice1_22_1.setHealthReward(0);
        choice1_22_1.setExperienceReward(15);
        choice1_22_1.setRequirements("");
        choice1_22_1.setIsAvailable(true);
        choice1_22_1.setStoryId("story_1_22");
        choiceRepository.save(choice1_22_1);

        Choice choice1_22_2 = new Choice();
        choice1_22_2.setText("准备开始钓鱼");
        choice1_22_2.setNextStoryId("story_1_10");
        choice1_22_2.setGoldCost(0);
        choice1_22_2.setGoldReward(0);
        choice1_22_2.setHealthCost(0);
        choice1_22_2.setHealthReward(0);
        choice1_22_2.setExperienceReward(20);
        choice1_22_2.setRequirements("");
        choice1_22_2.setIsAvailable(true);
        choice1_22_2.setStoryId("story_1_22");
        choiceRepository.save(choice1_22_2);

        System.out.println("✅ 批量选择内容加载完成！");
    }
}