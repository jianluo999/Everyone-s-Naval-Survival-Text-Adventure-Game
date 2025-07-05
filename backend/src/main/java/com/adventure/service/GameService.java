package com.adventure.service;

import com.adventure.model.*;
import com.adventure.repository.PlayerRepository;
import com.adventure.repository.StoryRepository;
import com.adventure.repository.ChoiceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class GameService {
    
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
        if (playerRepository.existsByName(playerName)) {
            throw new RuntimeException("玩家名称已存在");
        }
        
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
        
        return playerRepository.save(player);
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
        Optional<Story> storyOpt = storyRepository.findByStoryId(storyId);
        if (!storyOpt.isPresent()) {
            return null;
        }
        
        Story story = storyOpt.get();
        List<Choice> choices = choiceRepository.findByStoryId(storyId);
        
        return new StoryWithChoices(story, choices);
    }
    
    /**
     * 玩家做出选择
     */
    public Player makeChoice(String playerName, Long choiceId, String nextStoryId) {
        Player player = playerRepository.findByName(playerName)
                .orElseThrow(() -> new RuntimeException("玩家不存在"));
        
        Story nextStory = storyRepository.findByStoryId(nextStoryId)
                .orElseThrow(() -> new RuntimeException("故事不存在"));
        
        // 获取选择信息并应用影响
        if (choiceId != null) {
            Choice choice = choiceRepository.findById(choiceId)
                    .orElseThrow(() -> new RuntimeException("选择不存在"));
            
            // 应用选择的影响
            applyChoiceEffects(player, choice);
        }
        
        // 更新游戏状态
        GameState gameState = player.getGameState();
        
        // 检查是否可以执行行动
        if (!gameState.performAction()) {
            throw new RuntimeException("今日行动次数已满，请等待明天");
        }
        
        // 推进时间（每个选择消耗1-3小时）
        int timeAdvance = 1 + (int)(Math.random() * 3);
        gameState.advanceTime(timeAdvance);
        
        gameState.setCurrentStoryId(nextStoryId);
        gameState.setCurrentChapter(nextStory.getChapter());
        gameState.setCurrentScene(nextStory.getScene());
        gameState.setLastPlayedAt(LocalDateTime.now());
        
        // 应用每日消耗
        applyDailyConsumption(player, gameState);
        
        // 检查是否游戏结束
        if (nextStory.getIsEnding()) {
            gameState.setIsGameCompleted(true);
            gameState.setIsGameActive(false);
        }
        
        return playerRepository.save(player);
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
        
        // 选择会消耗一定精力
        int energyCost = 5 + (int)(Math.random() * 10);
        player.setEnergy(Math.max(0, player.getEnergy() - energyCost));
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