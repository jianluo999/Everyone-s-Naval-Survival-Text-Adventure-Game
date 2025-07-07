package com.adventure.service;

import com.adventure.model.*;
import com.adventure.repository.PlayerRepository;
import com.adventure.repository.StoryRepository;
import com.adventure.repository.ChoiceRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class GameService {

    private static final Logger logger = LoggerFactory.getLogger(GameService.class);

    @Autowired
    private PlayerRepository playerRepository;
    
    @Autowired
    private StoryRepository storyRepository;
    
    @Autowired
    private ChoiceRepository choiceRepository;
    
    /**
     * 创建新玩家
     */
    public Player createPlayer(String playerName) {
        logger.info("🎮 [SERVICE] 开始创建玩家 - 名称: '{}'", playerName);

        if (playerRepository.existsByName(playerName)) {
            logger.warn("⚠️ [SERVICE] 玩家名称已存在: '{}'", playerName);
            throw new RuntimeException("玩家名称已存在");
        }

        logger.info("🏗️ [SERVICE] 初始化玩家基础属性");
        Player player = new Player();
        player.setName(playerName);
        player.setGold(100);
        
        // 设置角色属性（根据小说设定）
        player.setStrength(3);
        player.setSpirit(7); // 钢铁意志天赋+1
        player.setAgility(4);
        player.setConstitution(3);
        player.setPerception(5);
        player.setSanity(100);
        player.setMaxSanity(100);
        player.setEnergy(100);
        player.setMaxEnergy(100);
        player.setHealth(100);
        player.setMaxHealth(100);
        
        // 设置生存系统
        player.setHunger(100);
        player.setMaxHunger(100);
        player.setThirst(100);
        player.setMaxThirst(100);
        
        player.setLevel(1);
        player.setExperience(0);
        player.setCurrentLocation("神秘海域");
        player.setStatus("健康");
        player.setTalents("钢铁意志");
        
        logger.info("🚢 [SERVICE] 创建初始船只 - 破旧木筏");
        // 创建初始船只
        Ship ship = new Ship();
        ship.setName("破旧木筏");
        ship.setType("BASIC");
        ship.setDurability(100);
        ship.setMaxDurability(100);
        ship.setSpeed(8);
        ship.setCargoCapacity(20);
        ship.setCurrentCargo(0);
        ship.setAttackPower(0);
        ship.setDefense(2);
        ship.setHasGrappleHook(true);
        ship.setFuel(100);
        ship.setMaxFuel(100);
        ship.setFood(50);
        ship.setMaxFood(100);
        ship.setWater(50);
        ship.setMaxWater(100);
        ship.setDescription("一艘破旧的木筏，勉强能在海上漂浮。需要尽快升级以应对更大的挑战。");
        ship.setEquipment("[]");
        player.setShip(ship);

        logger.info("🎯 [SERVICE] 初始化游戏状态 - 起始故事: story_1_1");
        // 创建游戏状态
        GameState gameState = new GameState();
        gameState.setCurrentChapter(1);
        gameState.setCurrentScene(1);
        gameState.setCurrentStoryId("story_1_1");
        gameState.setGameData("{}");
        gameState.setIsGameActive(true);
        gameState.setIsGameCompleted(false);
        gameState.setLastPlayedAt(LocalDateTime.now());
        gameState.setTotalPlayTime(0);
        player.setGameState(gameState);

        Player savedPlayer = playerRepository.save(player);
        logger.info("✅ [SERVICE] 玩家创建成功 - ID: {}, 名称: '{}'", savedPlayer.getId(), savedPlayer.getName());

        return savedPlayer;
    }
    
    /**
     * 获取玩家信息
     */
    public Optional<Player> getPlayer(String playerName) {
        return playerRepository.findByName(playerName);
    }
    
    /**
     * 获取当前故事
     */
    public Optional<Story> getCurrentStory(String storyId) {
        return storyRepository.findByStoryId(storyId);
    }
    
    /**
     * 获取故事的选择
     */
    public List<Choice> getStoryChoices(String storyId) {
        return choiceRepository.findByStoryId(storyId);
    }
    
    /**
     * 获取故事和选择的完整信息
     */
    public StoryWithChoices getStoryWithChoices(String storyId) {
        logger.info("📖 [SERVICE] 查询故事和选择 - storyId: '{}'", storyId);

        Optional<Story> storyOpt = storyRepository.findByStoryId(storyId);
        if (!storyOpt.isPresent()) {
            logger.warn("⚠️ [SERVICE] 故事不存在 - storyId: '{}'", storyId);
            return null;
        }

        Story story = storyOpt.get();
        List<Choice> choices = choiceRepository.findByStoryId(storyId);

        logger.info("✅ [SERVICE] 故事查询成功 - 标题: '{}', 章节: {}-{}, 选择数量: {}",
                   story.getTitle(), story.getChapter(), story.getScene(), choices.size());

        return new StoryWithChoices(story, choices);
    }
    
    /**
     * 玩家做出选择
     */
    public Player makeChoice(String playerName, Long choiceId, String nextStoryId) {
        logger.info("🎯 [SERVICE] 处理玩家选择 - 玩家: '{}', 选择ID: {}, 目标故事: '{}'",
                   playerName, choiceId, nextStoryId);

        Player player = playerRepository.findByName(playerName)
                .orElseThrow(() -> new RuntimeException("玩家不存在"));

        Story nextStory = storyRepository.findByStoryId(nextStoryId)
                .orElseThrow(() -> new RuntimeException("故事不存在"));

        logger.info("📊 [SERVICE] 玩家当前状态 - 理智: {}/{}, 健康: {}/{}, 当前故事: '{}'",
                   player.getSanity(), player.getMaxSanity(),
                   player.getHealth(), player.getMaxHealth(),
                   player.getGameState().getCurrentStoryId());

        // 循环检测：检查是否会导致无限循环
        GameState gameState = player.getGameState();
        if (detectStoryLoop(gameState.getCurrentStoryId(), nextStoryId)) {
            logger.error("🔄 [SERVICE] 检测到故事循环 - 当前: '{}', 目标: '{}'",
                        gameState.getCurrentStoryId(), nextStoryId);
            throw new RuntimeException("检测到故事循环，无法执行此选择");
        }

        // 获取选择信息并应用影响
        if (choiceId != null) {
            Choice choice = choiceRepository.findById(choiceId)
                    .orElseThrow(() -> new RuntimeException("选择不存在"));

            logger.info("💰 [SERVICE] 应用选择效果 - 选择文本: '{}', 金币消耗/奖励: {}/{}, 经验奖励: {}",
                       choice.getText(), choice.getGoldCost(), choice.getGoldReward(), choice.getExperienceReward());

            // 应用选择的影响
            applyChoiceEffects(player, choice);
        }

        // 更新游戏状态

        // 故事选择不消耗行动次数，不推进时间，不应用每日消耗
        // 只更新故事状态和处理故事特殊效果

        gameState.setCurrentStoryId(nextStoryId);
        gameState.setCurrentChapter(nextStory.getChapter());
        gameState.setCurrentScene(nextStory.getScene());
        gameState.setLastPlayedAt(LocalDateTime.now());

        logger.info("🎭 [SERVICE] 处理故事特殊效果 - 故事: '{}'", nextStoryId);
        // 处理故事特殊效果（理智值变化等）
        processStoryEffects(player, nextStoryId);

        // 故事选择不触发每日恢复和消耗机制

        // 检查是否游戏结束
        if (nextStory.getIsEnding()) {
            logger.info("🏁 [SERVICE] 游戏结束 - 玩家: '{}', 结局故事: '{}'", playerName, nextStoryId);
            gameState.setIsGameCompleted(true);
            gameState.setIsGameActive(false);
        }

        Player savedPlayer = playerRepository.save(player);
        logger.info("✅ [SERVICE] 选择处理完成 - 玩家: '{}', 新故事: '{}', 理智: {}/{}",
                   savedPlayer.getName(), nextStoryId,
                   savedPlayer.getSanity(), savedPlayer.getMaxSanity());

        return savedPlayer;
    }

    /**
     * 检测故事循环
     * 简单的循环检测：如果当前故事和目标故事形成已知的循环模式，则返回true
     */
    private boolean detectStoryLoop(String currentStoryId, String nextStoryId) {
        // 检测已知的循环模式
        if ("story_1_7".equals(currentStoryId) && "story_1_1".equals(nextStoryId)) {
            return true; // 这是之前的循环bug
        }

        // 检测直接回到自己的情况
        if (currentStoryId != null && currentStoryId.equals(nextStoryId)) {
            return true;
        }

        // 可以在这里添加更复杂的循环检测逻辑
        // 比如维护一个最近访问的故事历史，检测是否在短时间内重复访问相同的故事序列

        return false;
    }

    /**
     * 处理理智值变化
     */
    public void applySanityChange(Player player, int sanityChange, String reason) {
        int oldSanity = player.getSanity();
        int newSanity = Math.max(0, Math.min(player.getMaxSanity(), player.getSanity() + sanityChange));
        player.setSanity(newSanity);

        logger.info("🧠 [SERVICE] 理智值变化 - 玩家: '{}', 变化: {} ({}→{}), 原因: '{}'",
                   player.getName(), sanityChange, oldSanity, newSanity, reason);

        // 检查是否进入癫狂状态
        if (newSanity < 50 && !player.getIsMadness()) {
            player.setIsMadness(true);
            logger.warn("😵 [SERVICE] 玩家进入癫狂状态 - 玩家: '{}', 理智: {}", player.getName(), newSanity);
            // 癫狂状态下的属性加成会在前端处理或通过特殊效果处理
        } else if (newSanity >= 50 && player.getIsMadness()) {
            player.setIsMadness(false);
            logger.info("😌 [SERVICE] 玩家恢复理智 - 玩家: '{}', 理智: {}", player.getName(), newSanity);
        }

        // 检查危险状态
        if (newSanity <= 10) {
            logger.error("💀 [SERVICE] 玩家理智极度危险 - 玩家: '{}', 理智: {}", player.getName(), newSanity);
        } else if (newSanity <= 30) {
            logger.warn("⚠️ [SERVICE] 玩家理智危险 - 玩家: '{}', 理智: {}", player.getName(), newSanity);
        }
    }

    /**
     * 处理受伤状态
     */
    public void applyInjury(Player player, String bodyPart, String severity) {
        // 这里可以实现复杂的受伤系统
        // 暂时简化为更新状态描述
        String currentStatus = player.getStatus();
        if (!"健康".equals(currentStatus)) {
            player.setStatus("受伤");
        }

        // 可以扩展为JSON格式存储具体的受伤部位和程度
        String injuryData = "{\"" + bodyPart + "\": \"" + severity + "\"}";
        player.setInjuryStatus(injuryData);
    }

    /**
     * 检查并处理特殊故事效果
     */
    public void processStoryEffects(Player player, String storyId) {
        switch (storyId) {
            case "story_1_11":
                // 噩梦：理智下降15
                applySanityChange(player, -15, "体验死亡噩梦");
                break;
            case "story_1_12":
                // 看见溺尸：理智下降5
                applySanityChange(player, -5, "看见不明生物");
                break;
            case "story_1_13":
                // 恶心景象：理智下降3
                applySanityChange(player, -3, "恶心的景象");
                break;
            case "story_1_14":
                // 恶臭：理智下降5
                applySanityChange(player, -5, "恶心的臭味");
                break;
            case "story_1_15":
                // 被偷袭：理智下降10
                applySanityChange(player, -10, "被亡者偷袭");
                break;
            case "story_1_16":
                // 吞食人头章鱼：理智下降20
                applySanityChange(player, -20, "吞食邪恶生物");
                // 这里可以添加临时属性加成的逻辑
                break;
            case "story_1_17":
                // 古怪枪声：理智下降1
                applySanityChange(player, -1, "古怪的枪声");
                break;
        }
    }
    
    /**
     * 更新玩家状态
     */
    public Player updatePlayerStats(String playerName, Integer goldChange, Integer healthChange, Integer expChange) {
        Player player = playerRepository.findByName(playerName)
                .orElseThrow(() -> new RuntimeException("玩家不存在"));
        
        // 更新金币
        if (goldChange != null) {
            player.setGold(Math.max(0, player.getGold() + goldChange));
        }
        
        // 更新健康值
        if (healthChange != null) {
            int newHealth = Math.max(0, Math.min(player.getMaxHealth(), player.getHealth() + healthChange));
            player.setHealth(newHealth);
        }
        
        // 更新经验值
        if (expChange != null) {
            player.setExperience(player.getExperience() + expChange);
            
            // 检查是否升级
            int newLevel = player.getLevel();
            int expRequired = newLevel * 100; // 简单的升级公式
            
            if (player.getExperience() >= expRequired) {
                player.setLevel(newLevel + 1);
                player.setMaxHealth(player.getMaxHealth() + 10);
                player.setHealth(player.getMaxHealth()); // 升级时满血
            }
        }
        
        return playerRepository.save(player);
    }
    
    /**
     * 应用选择的影响
     */
    private void applyChoiceEffects(Player player, Choice choice) {
        // 检查玩家是否有足够的资源
        if (choice.getGoldCost() > 0 && player.getGold() < choice.getGoldCost()) {
            throw new RuntimeException("金币不足");
        }
        
        if (choice.getHealthCost() > 0 && player.getHealth() < choice.getHealthCost()) {
            throw new RuntimeException("健康值不足");
        }
        
        // 应用消耗
        if (choice.getGoldCost() > 0) {
            player.setGold(player.getGold() - choice.getGoldCost());
        }
        
        if (choice.getHealthCost() > 0) {
            player.setHealth(Math.max(1, player.getHealth() - choice.getHealthCost()));
        }
        
        // 应用奖励
        if (choice.getGoldReward() > 0) {
            player.setGold(player.getGold() + choice.getGoldReward());
        }
        
        if (choice.getHealthReward() > 0) {
            int newHealth = Math.min(player.getMaxHealth(), player.getHealth() + choice.getHealthReward());
            player.setHealth(newHealth);
        }
        
        if (choice.getExperienceReward() > 0) {
            player.setExperience(player.getExperience() + choice.getExperienceReward());
            checkLevelUp(player);
        }

        // 故事选择不应该消耗精力 - 只有特定的行动（如钓鱼、探索等）才消耗精力
        // 移除了自动精力消耗逻辑
    }
    
    /**
     * 应用每日恢复
     */
    public void applyDailyRecovery(Player player, GameState gameState) {
        logger.info("🌅 [SERVICE] 应用每日恢复 - 玩家: '{}', 第{}天", player.getName(), gameState.getCurrentDay());

        // 精力恢复 (恢复30-50点)
        int energyRecovery = 30 + (int)(Math.random() * 21);
        player.setEnergy(Math.min(player.getMaxEnergy(), player.getEnergy() + energyRecovery));
        logger.info("⚡ [SERVICE] 精力恢复 - 玩家: '{}', 恢复: {}点, 当前: {}/{}",
                   player.getName(), energyRecovery, player.getEnergy(), player.getMaxEnergy());

        // 健康恢复 (恢复10-20点)
        int healthRecovery = 10 + (int)(Math.random() * 11);
        player.setHealth(Math.min(player.getMaxHealth(), player.getHealth() + healthRecovery));
        logger.info("❤️ [SERVICE] 健康恢复 - 玩家: '{}', 恢复: {}点, 当前: {}/{}",
                   player.getName(), healthRecovery, player.getHealth(), player.getMaxHealth());

        // 理智恢复 (恢复5-15点)
        int sanityRecovery = 5 + (int)(Math.random() * 11);
        player.setSanity(Math.min(player.getMaxSanity(), player.getSanity() + sanityRecovery));
        logger.info("🧠 [SERVICE] 理智恢复 - 玩家: '{}', 恢复: {}点, 当前: {}/{}",
                   player.getName(), sanityRecovery, player.getSanity(), player.getMaxSanity());

        // 饥饿和口渴恢复 (如果有食物和水)
        Ship ship = player.getShip();
        if (ship != null) {
            if (ship.getFood() > 0) {
                int hungerRecovery = 20 + (int)(Math.random() * 21);
                player.setHunger(Math.min(player.getMaxHunger(), player.getHunger() + hungerRecovery));
                ship.setFood(Math.max(0, ship.getFood() - 1));
                logger.info("🍖 [SERVICE] 饥饿恢复 - 玩家: '{}', 恢复: {}点, 消耗食物1单位",
                           player.getName(), hungerRecovery);
            }

            if (ship.getWater() > 0) {
                int thirstRecovery = 25 + (int)(Math.random() * 21);
                player.setThirst(Math.min(player.getMaxThirst(), player.getThirst() + thirstRecovery));
                ship.setWater(Math.max(0, ship.getWater() - 1));
                logger.info("💧 [SERVICE] 口渴恢复 - 玩家: '{}', 恢复: {}点, 消耗淡水1单位",
                           player.getName(), thirstRecovery);
            }
        }
    }

    /**
     * 应用每日消耗
     */
    public void applyDailyConsumption(Player player, GameState gameState) {
        // 根据时间推进应用消耗
        int hoursAdvanced = 1; // 基础时间消耗
        
        // 饥饿值消耗 (每小时消耗1-2点)
        int hungerLoss = hoursAdvanced * (1 + (int)(Math.random() * 2));
        player.setHunger(Math.max(0, player.getHunger() - hungerLoss));
        
        // 口渴值消耗 (每小时消耗1-3点)
        int thirstLoss = hoursAdvanced * (1 + (int)(Math.random() * 3));
        player.setThirst(Math.max(0, player.getThirst() - thirstLoss));
        
        // 如果饥饿或口渴过低，影响其他属性
        if (player.getHunger() < 20) {
            player.setEnergy(Math.max(0, player.getEnergy() - 5));
            player.setHealth(Math.max(1, player.getHealth() - 2));
        }
        
        if (player.getThirst() < 20) {
            player.setEnergy(Math.max(0, player.getEnergy() - 8));
            player.setSanity(Math.max(1, player.getSanity() - 3));
        }
        
        // 深夜时间额外消耗理智值
        if (gameState.getCurrentHour() >= 22 || gameState.getCurrentHour() <= 5) {
            player.setSanity(Math.max(1, player.getSanity() - 2));
        }
        
        // 船只消耗
        Ship ship = player.getShip();
        if (ship != null) {
            // 燃料消耗
            ship.setFuel(Math.max(0, ship.getFuel() - 1));
            
            // 食物消耗
            if (ship.getFood() > 0) {
                ship.setFood(Math.max(0, ship.getFood() - 1));
                // 有食物时恢复饥饿值
                player.setHunger(Math.min(player.getMaxHunger(), player.getHunger() + 5));
            }
            
            // 淡水消耗
            if (ship.getWater() > 0) {
                ship.setWater(Math.max(0, ship.getWater() - 1));
                // 有淡水时恢复口渴值
                player.setThirst(Math.min(player.getMaxThirst(), player.getThirst() + 8));
            }
        }
    }
    
    /**
     * 检查升级
     */
    private void checkLevelUp(Player player) {
        int currentLevel = player.getLevel();
        int requiredExp = currentLevel * 100;
        
        if (player.getExperience() >= requiredExp) {
            player.setLevel(currentLevel + 1);
            player.setMaxHealth(player.getMaxHealth() + 10);
            player.setMaxEnergy(player.getMaxEnergy() + 10);
            player.setMaxSanity(player.getMaxSanity() + 5);
            
            // 升级时恢复部分状态
            player.setHealth(Math.min(player.getMaxHealth(), player.getHealth() + 20));
            player.setEnergy(Math.min(player.getMaxEnergy(), player.getEnergy() + 20));
            player.setSanity(Math.min(player.getMaxSanity(), player.getSanity() + 10));
        }
    }

    /**
     * 故事和选择的包装类
     */
    public static class StoryWithChoices {
        private Story story;
        private List<Choice> choices;
        
        public StoryWithChoices(Story story, List<Choice> choices) {
            this.story = story;
            this.choices = choices;
        }
        
        public Story getStory() {
            return story;
        }
        
        public List<Choice> getChoices() {
            return choices;
        }
    }

    /**
     * 保存玩家
     */
    public Player savePlayer(Player player) {
        return playerRepository.save(player);
    }
} 