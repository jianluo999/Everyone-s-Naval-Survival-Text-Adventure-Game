package com.adventure.controller;

import com.adventure.model.Player;
import com.adventure.model.Story;
import com.adventure.model.Choice;
import com.adventure.model.Ship;
import com.adventure.model.GameState;
import com.adventure.model.Fish;
import com.adventure.service.GameService;
import com.adventure.service.FishingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.List;
import java.util.stream.Collectors;
import java.time.LocalDateTime;

@RestController
@RequestMapping("/game")
@CrossOrigin(origins = "http://localhost:3000")
public class GameController {
    
    @Autowired
    private GameService gameService;
    
    @Autowired
    private FishingService fishingService;
    
    // DTO 类定义
    public static class PlayerDTO {
        public Long id;
        public String name;
        public Integer gold;
        public Integer strength;
        public Integer spirit;
        public Integer agility;
        public Integer constitution;
        public Integer perception;
        public Integer sanity;
        public Integer maxSanity;
        public Integer energy;
        public Integer maxEnergy;
        public Integer health;
        public Integer maxHealth;
        public Integer hunger;
        public Integer maxHunger;
        public Integer thirst;
        public Integer maxThirst;
        public Integer level;
        public Integer experience;
        public String currentLocation;
        public String status;
        public String talents;
        public ShipDTO ship;
        public GameStateDTO gameState;
        public LocalDateTime createdAt;
        public LocalDateTime updatedAt;
        
        public static PlayerDTO fromEntity(Player player) {
            PlayerDTO dto = new PlayerDTO();
            dto.id = player.getId();
            dto.name = player.getName();
            dto.gold = player.getGold();
            dto.strength = player.getStrength();
            dto.spirit = player.getSpirit();
            dto.agility = player.getAgility();
            dto.constitution = player.getConstitution();
            dto.perception = player.getPerception();
            dto.sanity = player.getSanity();
            dto.maxSanity = player.getMaxSanity();
            dto.energy = player.getEnergy();
            dto.maxEnergy = player.getMaxEnergy();
            dto.health = player.getHealth();
            dto.maxHealth = player.getMaxHealth();
            dto.hunger = player.getHunger();
            dto.maxHunger = player.getMaxHunger();
            dto.thirst = player.getThirst();
            dto.maxThirst = player.getMaxThirst();
            dto.level = player.getLevel();
            dto.experience = player.getExperience();
            dto.currentLocation = player.getCurrentLocation();
            dto.status = player.getStatus();
            dto.talents = player.getTalents();
            dto.ship = player.getShip() != null ? ShipDTO.fromEntity(player.getShip()) : null;
            dto.gameState = player.getGameState() != null ? GameStateDTO.fromEntity(player.getGameState()) : null;
            dto.createdAt = player.getCreatedAt();
            dto.updatedAt = player.getUpdatedAt();
            return dto;
        }
    }
    
    public static class ShipDTO {
        public Long id;
        public String name;
        public String type;
        public String category;
        public Integer level;
        public Integer durability;
        public Integer maxDurability;
        public Integer speed;
        public Integer cargoCapacity;
        public Integer currentCargo;
        public Integer attackPower;
        public Integer defense;
        public Boolean hasGrappleHook;
        public Integer fuel;
        public Integer maxFuel;
        public Integer food;
        public Integer maxFood;
        public Integer water;
        public Integer maxWater;
        public String shipSkills;
        public String rarity;
        public String description;
        public String equipment;
        
        public static ShipDTO fromEntity(Ship ship) {
            ShipDTO dto = new ShipDTO();
            dto.id = ship.getId();
            dto.name = ship.getName();
            dto.type = ship.getType();
            dto.category = ship.getCategory();
            dto.level = ship.getLevel();
            dto.durability = ship.getDurability();
            dto.maxDurability = ship.getMaxDurability();
            dto.speed = ship.getSpeed();
            dto.cargoCapacity = ship.getCargoCapacity();
            dto.currentCargo = ship.getCurrentCargo();
            dto.attackPower = ship.getAttackPower();
            dto.defense = ship.getDefense();
            dto.hasGrappleHook = ship.getHasGrappleHook();
            dto.fuel = ship.getFuel();
            dto.maxFuel = ship.getMaxFuel();
            dto.food = ship.getFood();
            dto.maxFood = ship.getMaxFood();
            dto.water = ship.getWater();
            dto.maxWater = ship.getMaxWater();
            dto.shipSkills = ship.getShipSkills();
            dto.rarity = ship.getRarity();
            dto.description = ship.getDescription();
            dto.equipment = ship.getEquipment();
            return dto;
        }
    }
    
    public static class GameStateDTO {
        public Long id;
        public Integer currentChapter;
        public Integer currentScene;
        public String currentStoryId;
        public String gameData;
        public Boolean isGameActive;
        public Boolean isGameCompleted;
        public LocalDateTime lastPlayedAt;
        public Integer totalPlayTime;
        public Integer currentDay;
        public Integer currentHour;
        public LocalDateTime gameStartTime;
        public LocalDateTime lastDayUpdateTime;
        public Integer actionsToday;
        public Integer maxActionsPerDay;
        public String timeDescription;
        
        public static GameStateDTO fromEntity(GameState gameState) {
            GameStateDTO dto = new GameStateDTO();
            dto.id = gameState.getId();
            dto.currentChapter = gameState.getCurrentChapter();
            dto.currentScene = gameState.getCurrentScene();
            dto.currentStoryId = gameState.getCurrentStoryId();
            dto.gameData = gameState.getGameData();
            dto.isGameActive = gameState.getIsGameActive();
            dto.isGameCompleted = gameState.getIsGameCompleted();
            dto.lastPlayedAt = gameState.getLastPlayedAt();
            dto.totalPlayTime = gameState.getTotalPlayTime();
            dto.currentDay = gameState.getCurrentDay();
            dto.currentHour = gameState.getCurrentHour();
            dto.gameStartTime = gameState.getGameStartTime();
            dto.lastDayUpdateTime = gameState.getLastDayUpdateTime();
            dto.actionsToday = gameState.getActionsToday();
            dto.maxActionsPerDay = gameState.getMaxActionsPerDay();
            dto.timeDescription = gameState.getTimeDescription();
            return dto;
        }
    }
    
    public static class StoryDTO {
        public Long id;
        public String storyId;
        public String title;
        public String content;
        public Integer chapter;
        public Integer scene;
        public String imageUrl;
        public List<ChoiceDTO> choices;
        public Boolean isEnding;
        public String storyType;
        
        public static StoryDTO fromEntity(Story story, List<Choice> choices) {
            StoryDTO dto = new StoryDTO();
            dto.id = story.getId();
            dto.storyId = story.getStoryId();
            dto.title = story.getTitle();
            dto.content = story.getContent();
            dto.chapter = story.getChapter();
            dto.scene = story.getScene();
            dto.imageUrl = story.getImageUrl();
            dto.isEnding = story.getIsEnding();
            dto.storyType = story.getStoryType();
            dto.choices = choices.stream()
                    .map(ChoiceDTO::fromEntity)
                    .collect(Collectors.toList());
            return dto;
        }
    }
    
    public static class ChoiceDTO {
        public Long id;
        public String text;
        public String nextStoryId;
        public Integer goldCost;
        public Integer goldReward;
        public Integer healthCost;
        public Integer healthReward;
        public Integer experienceReward;
        public String requirements;
        public Boolean isAvailable;
        
        public static ChoiceDTO fromEntity(Choice choice) {
            ChoiceDTO dto = new ChoiceDTO();
            dto.id = choice.getId();
            dto.text = choice.getText();
            dto.nextStoryId = choice.getNextStoryId();
            dto.goldCost = choice.getGoldCost();
            dto.goldReward = choice.getGoldReward();
            dto.healthCost = choice.getHealthCost();
            dto.healthReward = choice.getHealthReward();
            dto.experienceReward = choice.getExperienceReward();
            dto.requirements = choice.getRequirements();
            dto.isAvailable = choice.getIsAvailable();
            return dto;
        }
    }
    
    /**
     * 创建新玩家
     */
    @PostMapping("/player")
    public ResponseEntity<Map<String, Object>> createPlayer(@RequestBody Map<String, String> request) {
        try {
            String playerName = request.get("name");
            if (playerName == null || playerName.trim().isEmpty()) {
                return ResponseEntity.badRequest().body(Map.of("error", "玩家名称不能为空"));
            }
            
            Player player = gameService.createPlayer(playerName.trim());
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "玩家创建成功");
            response.put("player", PlayerDTO.fromEntity(player));
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 获取玩家信息
     */
    @GetMapping("/player/{name}")
    public ResponseEntity<Map<String, Object>> getPlayer(@PathVariable String name) {
        try {
            Optional<Player> player = gameService.getPlayer(name);
            if (player.isPresent()) {
                Map<String, Object> response = new HashMap<>();
                response.put("success", true);
                response.put("player", PlayerDTO.fromEntity(player.get()));
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 获取当前故事
     */
    @GetMapping("/story/{storyId}")
    public ResponseEntity<Map<String, Object>> getStory(@PathVariable String storyId) {
        try {
            GameService.StoryWithChoices storyWithChoices = gameService.getStoryWithChoices(storyId);
            if (storyWithChoices != null) {
                Map<String, Object> response = new HashMap<>();
                response.put("success", true);
                response.put("story", StoryDTO.fromEntity(storyWithChoices.getStory(), storyWithChoices.getChoices()));
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 玩家做出选择
     */
    @PostMapping("/choice")
    public ResponseEntity<Map<String, Object>> makeChoice(@RequestBody Map<String, Object> request) {
        try {
            String playerName = (String) request.get("playerName");
            Long choiceId = Long.valueOf(request.get("choiceId").toString());
            String nextStoryId = (String) request.get("nextStoryId");
            
            Player player = gameService.makeChoice(playerName, choiceId, nextStoryId);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "选择成功");
            response.put("player", PlayerDTO.fromEntity(player));
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 更新玩家状态
     */
    @PutMapping("/player/{name}/stats")
    public ResponseEntity<Map<String, Object>> updatePlayerStats(
            @PathVariable String name,
            @RequestBody Map<String, Integer> changes) {
        try {
            Integer goldChange = changes.get("gold");
            Integer healthChange = changes.get("health");
            Integer expChange = changes.get("experience");
            
            Player player = gameService.updatePlayerStats(name, goldChange, healthChange, expChange);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "玩家状态更新成功");
            response.put("player", PlayerDTO.fromEntity(player));
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 钓鱼
     */
    @PostMapping("/player/{name}/fishing")
    public ResponseEntity<Map<String, Object>> goFishing(@PathVariable String name) {
        try {
            FishingService.FishingResult result = fishingService.goFishing(name);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", result.isSuccess());
            response.put("message", result.getMessage());
            response.put("playerChanges", result.getPlayerChanges());
            
            if (result.getCaughtFish() != null) {
                response.put("fish", createFishDTO(result.getCaughtFish()));
            }
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 食用鱼类
     */
    @PostMapping("/player/{name}/eat/{fishId}")
    public ResponseEntity<Map<String, Object>> eatFish(@PathVariable String name, @PathVariable Long fishId) {
        try {
            FishingService.FishingResult result = fishingService.eatFish(name, fishId);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", result.isSuccess());
            response.put("message", result.getMessage());
            response.put("playerChanges", result.getPlayerChanges());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 创建鱼类DTO
     */
    private Map<String, Object> createFishDTO(Fish fish) {
        Map<String, Object> fishDTO = new HashMap<>();
        fishDTO.put("id", fish.getId());
        fishDTO.put("name", fish.getName());
        fishDTO.put("type", fish.getType());
        fishDTO.put("description", fish.getDescription());
        fishDTO.put("rarity", fish.getRarity());
        fishDTO.put("size", fish.getSize());
        fishDTO.put("weight", fish.getWeight());
        fishDTO.put("isEdible", fish.getIsEdible());
        fishDTO.put("isToxic", fish.getIsToxic());
        fishDTO.put("healthEffect", fish.getHealthEffect());
        fishDTO.put("sanityEffect", fish.getSanityEffect());
        fishDTO.put("energyEffect", fish.getEnergyEffect());
        fishDTO.put("hungerRestore", fish.getHungerRestore());
        fishDTO.put("thirstRestore", fish.getThirstRestore());
        return fishDTO;
    }
    
    /**
     * 时间推进和每日消耗
     */
    @PostMapping("/player/{name}/advance-time")
    public ResponseEntity<Map<String, Object>> advanceTime(@PathVariable String name) {
        try {
            Player player = gameService.getPlayer(name)
                    .orElseThrow(() -> new RuntimeException("玩家不存在"));
            
            GameState gameState = player.getGameState();
            
            // 推进时间（1小时）
            gameState.advanceTime(1);
            
            // 应用每日消耗
            gameService.applyDailyConsumption(player, gameState);
            
            // 保存更新
            player = gameService.savePlayer(player);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "时间推进成功");
            response.put("player", PlayerDTO.fromEntity(player));
            response.put("currentDay", gameState.getCurrentDay());
            response.put("currentHour", gameState.getCurrentHour());
            response.put("timeDescription", gameState.getTimeDescription());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 获取游戏时间信息
     */
    @GetMapping("/player/{name}/time")
    public ResponseEntity<Map<String, Object>> getTimeInfo(@PathVariable String name) {
        try {
            Player player = gameService.getPlayer(name)
                    .orElseThrow(() -> new RuntimeException("玩家不存在"));
            
            GameState gameState = player.getGameState();
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("currentDay", gameState.getCurrentDay());
            response.put("currentHour", gameState.getCurrentHour());
            response.put("timeDescription", gameState.getTimeDescription());
            response.put("actionsToday", gameState.getActionsToday());
            response.put("maxActionsPerDay", gameState.getMaxActionsPerDay());
            response.put("remainingActions", gameState.getMaxActionsPerDay() - gameState.getActionsToday());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 健康检查
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "healthy");
        response.put("service", "sailing-game-backend");
        response.put("message", "🚢 航海冒险游戏后端运行正常");
        return ResponseEntity.ok(response);
    }
} 