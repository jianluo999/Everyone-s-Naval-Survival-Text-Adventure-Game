package com.adventure.config;

import com.adventure.model.Choice;
import com.adventure.model.Story;
import com.adventure.model.Equipment;
import com.adventure.model.Player;
import com.adventure.model.Ship;
import com.adventure.model.GameState;
import com.adventure.model.Fish;
import com.adventure.repository.StoryRepository;
import com.adventure.repository.ChoiceRepository;
import com.adventure.repository.EquipmentRepository;
import com.adventure.repository.PlayerRepository;
import com.adventure.repository.FishRepository;
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
        
        // 创建选择（现在不再需要双向关联）
        createChoices();
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
        
        // story_1_7 的选择（初次航行）
        Choice choice1_7_1 = new Choice();
        choice1_7_1.setText("向东方的小岛航行");
        choice1_7_1.setNextStoryId("story_1_1");
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
        choice1_7_2.setNextStoryId("story_1_1");
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
        choice1_7_3.setNextStoryId("story_1_1");
        choice1_7_3.setGoldCost(0);
        choice1_7_3.setGoldReward(0);
        choice1_7_3.setHealthCost(0);
        choice1_7_3.setHealthReward(0);
        choice1_7_3.setExperienceReward(15);
        choice1_7_3.setRequirements("");
        choice1_7_3.setIsAvailable(true);
        choice1_7_3.setStoryId("story_1_7");
        choiceRepository.save(choice1_7_3);
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