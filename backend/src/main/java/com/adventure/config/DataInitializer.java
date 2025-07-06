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
        // 如果数据库中已有数据，则不重复初始化
        if (storyRepository.count() > 0) {
            return;
        }
        
        System.out.println("🎮 开始初始化游戏数据...");
        
        // 创建游戏装备
        createGameEquipment();
        
        // 创建游戏故事
        createGameStories();
        
        // 创建怪异鱼类
        createStrangeFish();
        
        // 创建默认玩家
        createDefaultPlayer();
        
        System.out.println("✅ 游戏数据初始化完成！");
    }
    
    private void createGameStories() {
        // 第一章：觉醒
        Story story1_1 = new Story();
        story1_1.setStoryId("story_1_1");
        story1_1.setTitle("神秘的觉醒");
        story1_1.setContent("「欢迎来到全民航海求生游戏...」\n\n" +
                "奇特的声音从脑海响起。你苏醒过来，发现自己正躺在一张老旧的床上。" +
                "你试着起身，竟然奇迹般地站了起来！身体的疾病和残缺都已经完全治愈。\n\n" +
                "环顾四周，你发现自己在一处狭窄昏暗的船舱里。不远处的桌子上躺着一具干枯的骸骨，" +
                "看起来是自杀身亡的前任船主。窗外是一望无际的大海，时不时荡起浪涛。\n\n" +
                "在床上，你发现了一本散发微光的小册子——「航海日志」。现在，你需要做出第一个决定...");
        story1_1.setChapter(1);
        story1_1.setScene(1);
        story1_1.setStoryType("AWAKENING");
        story1_1.setIsEnding(false);
        storyRepository.save(story1_1);
        
        // 第二个故事：航海日志
        Story story1_2 = new Story();
        story1_2.setStoryId("story_1_2");
        story1_2.setTitle("航海日志的秘密");
        story1_2.setContent("你打开了航海日志，里面记录着游戏的规则和你的状态信息。\n\n" +
                "【游戏规则】\n" +
                "1. 未经允许，其他人无法登上你的船只\n" +
                "2. 你船上的物品不会被其他玩家盗窃，除非你已死亡\n" +
                "3. 每艘船都装有爪钩，可以抓取飘来的物品\n" +
                "4. 你需要升级强化你的船只，让它看起来足够安全\n" +
                "5. 要小心夜晚，当心雾气，一旦陷入后方黑雾，你将会死亡\n\n" +
                "【你的状态】\n" +
                "力量：3，精神：7+1，敏捷：4，体质：3，感知：5\n" +
                "理智：100/100，精力：100/100，气血：100/100\n" +
                "天赋：钢铁意志 - 你永不服输，理智至少会保留1点\n\n" +
                "你还发现了聊天频道，里面有世界聊天、区域聊天和私密聊天。现在你需要决定下一步行动...");
        story1_2.setChapter(1);
        story1_2.setScene(2);
        story1_2.setStoryType("TUTORIAL");
        story1_2.setIsEnding(false);
        storyRepository.save(story1_2);
        
        // 第三个故事：船舱探索
        Story story1_3 = new Story();
        story1_3.setStoryId("story_1_3");
        story1_3.setTitle("船舱探索");
        story1_3.setContent("你仔细搜查船舱，发现了一些有用的物品：\n\n" +
                "- 一把生锈的匕首\n" +
                "- 几块干硬的面包\n" +
                "- 一个装着淡水的木桶\n" +
                "- 一些破旧的绳索\n\n" +
                "这些物品虽然简陋，但在海上求生中可能会派上用场。");
        story1_3.setChapter(1);
        story1_3.setScene(3);
        story1_3.setStoryType("NORMAL");
        story1_3.setIsEnding(false);
        storyRepository.save(story1_3);
        
        // 第四个故事：观察海况
        Story story1_4 = new Story();
        story1_4.setStoryId("story_1_4");
        story1_4.setTitle("观察海况");
        story1_4.setContent("你走到窗边，透过破旧的玻璃观察外面的海况。\n\n" +
                "海面相对平静，阳光透过云层洒在深蓝色的海水上。" +
                "远处似乎有几艘船只在航行，但距离太远看不清楚。\n\n" +
                "你注意到船只似乎在缓慢漂移，也许是受到了海流的影响。" +
                "现在是了解更多信息的时候了。");
        story1_4.setChapter(1);
        story1_4.setScene(4);
        story1_4.setStoryType("NORMAL");
        story1_4.setIsEnding(false);
        storyRepository.save(story1_4);
        
        // 第五个故事：聊天频道
        Story story1_5 = new Story();
        story1_5.setStoryId("story_1_5");
        story1_5.setTitle("聊天频道");
        story1_5.setContent("你打开了聊天频道，看到了各种信息在不断滚动着...\n\n" +
                "【世界聊天】\n" +
                "🌊 张三：有人知道怎么升级船只吗？\n" +
                "⚓ 李四：小心夜晚的雾气！我昨天差点死掉！\n" +
                "🚢 王五：有人看到漂浮的宝箱了吗？\n" +
                "💀 神秘玩家：黑雾正在加速...大家要小心了\n\n" +
                "你意识到这个世界中还有很多其他玩家，每个人都在为生存而努力。" +
                "现在你需要决定是否要和他们互动。");
        story1_5.setChapter(1);
        story1_5.setScene(5);
        story1_5.setStoryType("SOCIAL");
        story1_5.setIsEnding(false);
        storyRepository.save(story1_5);
        
        // 第六个故事：船只探索
        Story story1_6 = new Story();
        story1_6.setStoryId("story_1_6");
        story1_6.setTitle("船只探索");
        story1_6.setContent("你开始仔细探索这艘破旧的木筏。\n\n" +
                "【船只状态】\n" +
                "- 船名：破旧木筏\n" +
                "- 耐久度：100/100\n" +
                "- 速度：8节\n" +
                "- 载货量：20/20\n" +
                "- 防御力：2\n" +
                "- 装备：爪钩×1\n\n" +
                "你发现船上有一个简单的操作台，上面有几个按钮和一个舵轮。" +
                "窗外的海水在阳光下闪闪发光，但你知道平静的表面下隐藏着未知的危险。\n\n" +
                "你需要决定第一步该做什么。");
        story1_6.setChapter(1);
        story1_6.setScene(6);
        story1_6.setStoryType("EXPLORATION");
        story1_6.setIsEnding(false);
        storyRepository.save(story1_6);
        
        // 第七个故事：开始航行
        Story story1_7 = new Story();
        story1_7.setStoryId("story_1_7");
        story1_7.setTitle("初次航行");
        story1_7.setContent("你启动了船只，开始了你的第一次航行。\n\n" +
                "船只缓慢地开始移动，海水在船底发出轻柔的声音。" +
                "你紧握着舵轮，感受着海风拂过面颊。\n\n" +
                "前方的海域看起来平静而神秘。你注意到：\n" +
                "- 东方有一座小岛，冒着轻烟\n" +
                "- 北方有几艘船只在航行\n" +
                "- 南方的海水颜色较深，可能有危险\n" +
                "- 西方远处有乌云聚集\n\n" +
                "这是你人生的新开始，每个选择都将决定你的命运。");
        story1_7.setChapter(1);
        story1_7.setScene(7);
        story1_7.setStoryType("SAILING");
        story1_7.setIsEnding(false);
        storyRepository.save(story1_7);

        // 第八个故事：东方小岛的夜晚 - 第一次噩梦
        Story story1_8 = new Story();
        story1_8.setStoryId("story_1_8");
        story1_8.setTitle("东方小岛的夜晚");
        story1_8.setContent("你驾驶着船只向东方的小岛航行，经过一段时间的航行，你终于接近了那座冒着轻烟的小岛。\n\n" +
                "夜幕降临，你将船只停靠在小岛附近的浅滩。岛上似乎有人类活动的痕迹，但现在一片寂静。\n" +
                "你决定在船上过夜，明天再上岛探索。\n\n" +
                "海上的第一个夜晚，注定难眠。你躺在船长室的床上，听着海浪拍打船体的声音。\n" +
                "不知躺了多久才睡着，在床上辗转反侧，额头不停冒出冷汗。\n\n" +
                "你开始做噩梦...");
        story1_8.setChapter(1);
        story1_8.setScene(8);
        story1_8.setStoryType("NIGHT_ENCOUNTER");
        story1_8.setIsEnding(false);
        storyRepository.save(story1_8);

        Story story1_9 = new Story();
        story1_9.setStoryId("story_1_9");
        story1_9.setTitle("与其他船只的邂逅");
        story1_9.setContent("你决定向北方的船只靠近...\n\n" +
                "随着距离的缩短，你看清了那些船只的轮廓。\n" +
                "它们看起来像是商船，船上的人似乎也注意到了你。\n\n" +
                "【待续...】\n" +
                "更多精彩内容即将到来！");
        story1_9.setChapter(1);
        story1_9.setScene(9);
        story1_9.setStoryType("ENCOUNTER");
        story1_9.setIsEnding(true); // 临时设为结束
        storyRepository.save(story1_9);

        Story story1_10 = new Story();
        story1_10.setStoryId("story_1_10");
        story1_10.setTitle("海上的观察与等待");
        story1_10.setContent("你选择在当前位置等待，仔细观察周围的情况...\n\n" +
                "在这片平静的海域中，你有时间思考接下来的计划。\n" +
                "远处的景象让你对这个世界有了更多的了解。\n\n" +
                "【待续...】\n" +
                "更多精彩内容即将到来！");
        story1_10.setChapter(1);
        story1_10.setScene(10);
        story1_10.setStoryType("OBSERVATION");
        story1_10.setIsEnding(true); // 临时设为结束
        storyRepository.save(story1_10);

        // 第九个故事：噩梦中的溺尸
        Story story1_11 = new Story();
        story1_11.setStoryId("story_1_11");
        story1_11.setTitle("噩梦中的溺尸");
        story1_11.setContent("在梦中，你看见一具肿胀的溺尸，悄无声息地推开门，走了进来。\n\n" +
                "梦境是如此真实，仿佛亲眼所见。你记得那溺尸走动的声音——啪叽、啪叽！\n" +
                "就好像湿润的拖把拍在地上。\n\n" +
                "梦中的你拿起床头的燧发枪朝溺尸打去，但枪哑火了。\n" +
                "下一瞬，你被这溺尸按在了床上，成了板上鱼肉，被开膛破肚...\n\n" +
                "【你体验了死亡，被虐杀吞噬，理智下降15】\n\n" +
                "\"啊！\"你突然惊醒，用手摸向自己的腹部，发现完好无损后，才长舒一口气。\n" +
                "还好是梦！但忽然，你发现船长室的门居然是开着的...");
        story1_11.setChapter(1);
        story1_11.setScene(11);
        story1_11.setStoryType("NIGHTMARE");
        story1_11.setIsEnding(false);
        storyRepository.save(story1_11);

        // 第十个故事：真实的威胁
        Story story1_12 = new Story();
        story1_12.setStoryId("story_1_12");
        story1_12.setTitle("真实的威胁");
        story1_12.setContent("你立刻把燧发枪抓在手中。\"是风吗？不可能，今天海上就没什么风！\"\n\n" +
                "啪叽、啪叽！熟悉的脚步声传来。\n\n" +
                "一具浮肿的溺尸出现在门口。它似乎在海里泡了很久，已经被泡得肿胀发臭，\n" +
                "身上还穿着烂成碎布的水手服，挂满海藻。\n" +
                "此刻，它正用惨白的眼眸看向你...\n\n" +
                "【看见不明生物，你的理智下降5】\n\n" +
                "\"FXXK！\"你怒骂一声，必须立刻做出选择！");
        story1_12.setChapter(1);
        story1_12.setScene(12);
        story1_12.setStoryType("BATTLE_START");
        story1_12.setIsEnding(false);
        storyRepository.save(story1_12);

        // 第十一个故事：枪械失效
        Story story1_13 = new Story();
        story1_13.setStoryId("story_1_13");
        story1_13.setTitle("枪械失效");
        story1_13.setContent("你立刻开枪射击，但咔的一声——枪卡壳了！\n\n" +
                "溺尸似乎还留有几分神智，看见手枪哑火，便咧开大嘴笑了起来。\n" +
                "嘴里没几颗牙，一只螃蟹从中爬出。\n\n" +
                "【恶心的景象，你理智下降3】\n\n" +
                "这一幕和噩梦非常像，所以你早有准备。枪没响的同时，\n" +
                "你就把燧发枪当石头砸了出去，正中溺尸头部。\n\n" +
                "趁溺尸被砸的间隙，你必须立刻行动！");
        story1_13.setChapter(1);
        story1_13.setScene(13);
        story1_13.setStoryType("BATTLE_CONTINUE");
        story1_13.setIsEnding(false);
        storyRepository.save(story1_13);

        // 第十二个故事：甲板战斗
        Story story1_14 = new Story();
        story1_14.setStoryId("story_1_14");
        story1_14.setTitle("甲板上的生死搏斗");
        story1_14.setContent("你抄起长矛，对溺尸发起冲锋，一矛扎进腐尸脖子，然后身体也撞了上去。\n\n" +
                "你并非要造成杀伤，而是急着离开船长室。只有逃出这狭窄的空间，\n" +
                "去到甲板，你才有和溺尸一战的可能！\n\n" +
                "冲刺的力量很大，加上体重，你勉强从溺尸身旁挤了出去。\n" +
                "那腥臭腐烂的味道，差点让你吐出来。\n\n" +
                "【恶心的臭味，你理智下降5】\n\n" +
                "你马不停蹄，跑到了船头甲板。在这里，你有足够的空间周旋！");
        story1_14.setChapter(1);
        story1_14.setScene(14);
        story1_14.setStoryType("BATTLE_CONTINUE");
        story1_14.setIsEnding(false);
        storyRepository.save(story1_14);

        // 第十三个故事：战斗胜利
        Story story1_15 = new Story();
        story1_15.setStoryId("story_1_15");
        story1_15.setTitle("第一场胜利");
        story1_15.setContent("经过激烈的战斗，你终于击败了溺尸。但就在你以为危险结束时，\n" +
                "船舱内传来了嘎吱嘎吱的骨骼摩擦声...\n\n" +
                "那具船长骸骨站了起来，手持钓竿，眼眶中燃烧着惨绿色的灵魂之火。\n" +
                "它悄无声息地走到你身后，趁你不备发起偷袭！\n\n" +
                "【被亡者偷袭，你理智下降10】\n" +
                "【理智低于50，你进入癫狂状态！】\n\n" +
                "愤怒和疯狂充斥着你的大脑，但同时也带来了超越常人的力量...");
        story1_15.setChapter(1);
        story1_15.setScene(15);
        story1_15.setStoryType("BOSS_BATTLE");
        story1_15.setIsEnding(false);
        storyRepository.save(story1_15);

        // 第十四个故事：癫狂状态下的战斗
        Story story1_16 = new Story();
        story1_16.setStoryId("story_1_16");
        story1_16.setTitle("癫狂的力量");
        story1_16.setContent("癫狂状态下，你的力量、敏捷和体质都得到了提升，同时免疫恐惧和疼痛。\n\n" +
                "你冲进船舱，找到了人头章鱼的残骸，毫不犹豫地吞了下去。\n" +
                "【你吞下了人头章鱼，力量+1，体质+1，精神-1，理智-20，持续1分钟】\n\n" +
                "现在你的力量翻了一倍！你欺身上前，这时骷髅还在疑惑枪为何打不响。\n" +
                "下一秒，它被你扑倒在地，两根臂骨被狠狠扯下。\n\n" +
                "你得势不饶人，右手穿过骷髅颅骨的破口，抓向里面的灵魂之火...");
        story1_16.setChapter(1);
        story1_16.setScene(16);
        story1_16.setStoryType("MADNESS_BATTLE");
        story1_16.setIsEnding(false);
        storyRepository.save(story1_16);

        // 第十五个故事：夜晚的结束
        Story story1_17 = new Story();
        story1_17.setStoryId("story_1_17");
        story1_17.setTitle("恐怖夜晚的结束");
        story1_17.setContent("你握住了那团灵魂之火，并不烫手，反而很温暖。\n\n" +
                "骷髅反应剧烈，浑身战栗，很快散落一地，变成一摊平平无奇的骨头，\n" +
                "灵魂之火也彻底熄灭。\n\n" +
                "但你没有掉以轻心。保险起见，你将颅骨摆在船舷上，\n" +
                "两分钟后，果不其然，颅骨内重新亮起惨绿色的光芒。\n\n" +
                "你二话不说，果断开枪。\"嘭！\"火光迸射，枪声尖厉。\n" +
                "这颅骨直接被燧发枪轰成了碎渣。\n\n" +
                "【枪声古怪，你理智下降1】\n\n" +
                "终于，这恐怖的夜晚结束了。你虽然受了伤，但活了下来。\n" +
                "更重要的是，你学会了在这个危险世界中生存的第一课...");
        story1_17.setChapter(1);
        story1_17.setScene(17);
        story1_17.setStoryType("CHAPTER_END");
        story1_17.setIsEnding(true);
        storyRepository.save(story1_17);

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
} 