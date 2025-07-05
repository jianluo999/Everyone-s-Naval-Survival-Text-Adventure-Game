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
        
        // 更新游戏状态
        GameState gameState = player.getGameState();
        gameState.setCurrentStoryId(nextStoryId);
        gameState.setCurrentChapter(nextStory.getChapter());
        gameState.setCurrentScene(nextStory.getScene());
        gameState.setLastPlayedAt(LocalDateTime.now());
        
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
     * 内部类：故事和选择的组合
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
} 