package com.adventure.service;

import com.adventure.model.Fish;
import com.adventure.model.Player;
import com.adventure.repository.FishRepository;
import com.adventure.repository.PlayerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

@Service
@Transactional
public class FishingService {
    
    @Autowired
    private FishRepository fishRepository;
    
    @Autowired
    private PlayerRepository playerRepository;
    
    private final Random random = new Random();
    
    /**
     * 钓鱼结果类
     */
    public static class FishingResult {
        private boolean success;
        private Fish caughtFish;
        private String message;
        private Map<String, Integer> playerChanges;
        private String fishingSpot;
        private int fishingDuration;

        public FishingResult(boolean success, String message) {
            this.success = success;
            this.message = message;
            this.playerChanges = new HashMap<>();
        }

        // Getters and setters
        public boolean isSuccess() { return success; }
        public void setSuccess(boolean success) { this.success = success; }

        public Fish getCaughtFish() { return caughtFish; }
        public void setCaughtFish(Fish caughtFish) { this.caughtFish = caughtFish; }

        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }

        public Map<String, Integer> getPlayerChanges() { return playerChanges; }
        public void setPlayerChanges(Map<String, Integer> playerChanges) { this.playerChanges = playerChanges; }

        public String getFishingSpot() { return fishingSpot; }
        public void setFishingSpot(String fishingSpot) { this.fishingSpot = fishingSpot; }

        public int getFishingDuration() { return fishingDuration; }
        public void setFishingDuration(int fishingDuration) { this.fishingDuration = fishingDuration; }
    }
    
    /**
     * 执行钓鱼（带钓点选择）
     */
    public FishingResult goFishing(String playerName, String fishingSpot) {
        Player player = playerRepository.findByName(playerName)
                .orElseThrow(() -> new RuntimeException("玩家不存在"));

        // 检查玩家状态
        if (player.getEnergy() < 10) {
            return new FishingResult(false, "精力不足，无法钓鱼！需要至少10点精力。");
        }

        if (player.getSanity() < 20) {
            return new FishingResult(false, "理智过低，无法集中注意力钓鱼！");
        }

        // 检查钓点权限
        if (!canFishAtSpot(player, fishingSpot)) {
            return new FishingResult(false, "你还不能在这个位置钓鱼！");
        }

        // 消耗精力
        player.setEnergy(Math.max(0, player.getEnergy() - 10));

        // 计算钓鱼技能（更复杂的计算公式，避免高等级玩家过于强势）
        int baseSkill = player.getPerception();
        int levelBonus = Math.min(player.getLevel() / 3, 10); // 等级加成有上限
        int sanityPenalty = player.getSanity() < 50 ? (50 - player.getSanity()) / 10 : 0; // 理智影响
        int energyPenalty = player.getEnergy() < 30 ? (30 - player.getEnergy()) / 5 : 0; // 精力影响

        int fishingSkill = Math.max(1, baseSkill + levelBonus - sanityPenalty - energyPenalty);

        // 根据钓点和技能选择鱼类
        Fish caughtFish = selectFishBySpot(fishingSkill, fishingSpot);

        FishingResult result = new FishingResult(true, "");
        result.setFishingSpot(fishingSpot);
        result.setFishingDuration(generateRandomFishingTime(fishingSpot));

        if (caughtFish == null) {
            // 没钓到鱼
            result.setMessage(generateNoFishMessage(fishingSpot));
            result.getPlayerChanges().put("energy", -10);
        } else {
            // 钓到鱼了
            result.setCaughtFish(caughtFish);
            result.setMessage(generateFishingMessage(caughtFish, fishingSpot));

            // 应用钓鱼效果
            applyFishingEffects(player, caughtFish, result);
        }

        // 保存玩家状态
        playerRepository.save(player);

        return result;
    }

    /**
     * 兼容旧版本的钓鱼方法
     */
    public FishingResult goFishing(String playerName) {
        return goFishing(playerName, "bow"); // 默认船头钓鱼
    }
    
    /**
     * 检查玩家是否可以在指定钓点钓鱼
     */
    private boolean canFishAtSpot(Player player, String spot) {
        switch (spot) {
            case "bow":
            case "port":
            case "starboard":
                return true; // 基础钓点，所有玩家都可以使用
            case "stern":
                return player.getLevel() >= 5; // 船尾需要5级
            case "captain":
                return player.getLevel() >= 10 &&
                       (player.getShip() != null && !"BASIC".equals(player.getShip().getType()));
            default:
                return false;
        }
    }

    /**
     * 根据钓点选择鱼类
     */
    private Fish selectFishBySpot(int playerSkill, String spot) {
        double baseChance = getSpotSuccessRate(spot);

        if (random.nextDouble() > baseChance) {
            return null; // 没钓到
        }

        // 根据钓点类型选择鱼类
        String fishType = getSpotFishType(spot);

        try {
            // 根据钓点调整成功概率，使用现有的随机选择逻辑
            double spotMultiplier = getSpotRarityMultiplier(spot);
            return fishRepository.findRandomFish(spotMultiplier);
        } catch (Exception e) {
            // 如果随机查询失败，fallback到原有逻辑
            return selectRandomFish(playerSkill);
        }
    }

    /**
     * 获取钓点成功率
     */
    private double getSpotSuccessRate(String spot) {
        switch (spot) {
            case "bow": return 0.7;      // 船头：70%
            case "port": return 0.5;     // 左舷：50%
            case "starboard": return 0.6; // 右舷：60%
            case "stern": return 0.3;    // 船尾：30%
            case "captain": return 0.1;  // 船长专用：10%
            default: return 0.5;
        }
    }

    /**
     * 获取钓点鱼类类型
     */
    private String getSpotFishType(String spot) {
        switch (spot) {
            case "bow": return "COMMON";     // 船头：常见鱼类
            case "port": return "DEEP_SEA";  // 左舷：深海鱼类
            case "starboard": return "TROPICAL"; // 右舷：热带鱼类
            case "stern": return "STRANGE";  // 船尾：奇异生物
            case "captain": return "LEGENDARY"; // 船长专用：传说鱼类
            default: return "COMMON";
        }
    }

    /**
     * 获取钓点稀有度倍数
     */
    private double getSpotRarityMultiplier(String spot) {
        switch (spot) {
            case "bow": return 0.1;      // 船头：常见鱼类
            case "port": return 0.05;    // 左舷：更稀有
            case "starboard": return 0.08; // 右舷：中等稀有
            case "stern": return 0.02;   // 船尾：很稀有
            case "captain": return 0.01; // 船长专用：极稀有
            default: return 0.1;
        }
    }

    /**
     * 生成随机钓鱼时间（5-20秒）
     */
    private int generateRandomFishingTime(String spot) {
        int baseTime;
        switch (spot) {
            case "bow": baseTime = 8; break;      // 船头：较快
            case "port": baseTime = 15; break;    // 左舷：较慢
            case "starboard": baseTime = 10; break; // 右舷：中等
            case "stern": baseTime = 18; break;   // 船尾：很慢
            case "captain": baseTime = 12; break; // 船长专用：中等
            default: baseTime = 10;
        }

        // 在基础时间上随机±5秒
        return Math.max(5, Math.min(20, baseTime + random.nextInt(11) - 5));
    }

    /**
     * 随机选择鱼类（原有方法，保持兼容性）
     */
    private Fish selectRandomFish(int playerSkill) {
        double baseChance = 0.7; // 基础钓鱼成功率

        if (random.nextDouble() > baseChance) {
            return null; // 没钓到
        }

        // 根据玩家技能选择鱼类
        try {
            return fishRepository.findRandomFish(0.1);
        } catch (Exception e) {
            // 如果随机查询失败，fallback到固定选择
            return fishRepository.findByCatchDifficultyLessThanEqual(playerSkill)
                    .stream()
                    .findFirst()
                    .orElse(null);
        }
    }
    
    /**
     * 生成没钓到鱼的消息
     */
    private String generateNoFishMessage(String spot) {
        String spotName = getSpotDisplayName(spot);
        String[] messages = {
            "你在" + spotName + "等了很长时间，但什么都没钓到...",
            spotName + "的鱼儿今天似乎不太活跃...",
            "虽然在" + spotName + "很有耐心，但这次运气不太好...",
            "在" + spotName + "钓了一会儿，鱼儿都很狡猾..."
        };

        return messages[random.nextInt(messages.length)];
    }

    /**
     * 生成钓鱼成功消息（带钓点信息）
     */
    private String generateFishingMessage(Fish fish, String spot) {
        String spotName = getSpotDisplayName(spot);
        String[] messages = {
            "你在" + spotName + "钓到了一条" + fish.getName() + "！",
            "经过在" + spotName + "的耐心等待，你成功捕获了" + fish.getName() + "！",
            "在" + spotName + "，你的鱼钩上挂着一条" + fish.getName() + "，看起来很新鲜！",
            "太好了！在" + spotName + "钓到了" + fish.getName() + "！"
        };

        return messages[random.nextInt(messages.length)];
    }

    /**
     * 获取钓点显示名称
     */
    private String getSpotDisplayName(String spot) {
        switch (spot) {
            case "bow": return "船头";
            case "port": return "左舷";
            case "starboard": return "右舷";
            case "stern": return "船尾";
            case "captain": return "船长专用钓点";
            default: return "未知位置";
        }
    }

    /**
     * 应用钓鱼效果
     */
    private void applyFishingEffects(Player player, Fish fish, FishingResult result) {
        Map<String, Integer> changes = result.getPlayerChanges();
        
        // 基础精力消耗
        changes.put("energy", -10);
        
        // 理智值影响（钓到奇怪的鱼会降低理智）
        if ("STRANGE".equals(fish.getType()) || "DANGEROUS".equals(fish.getType())) {
            int sanityLoss = 0;
            
            if ("STRANGE".equals(fish.getType())) {
                sanityLoss = 2 + random.nextInt(3); // 2-4点理智损失
            } else if ("DANGEROUS".equals(fish.getType())) {
                sanityLoss = 5 + random.nextInt(5); // 5-9点理智损失
            }
            
            player.setSanity(Math.max(1, player.getSanity() - sanityLoss)); // 钢铁意志：理智至少保留1点
            changes.put("sanity", -sanityLoss);
        }
        
        // 经验值奖励
        int expGain = calculateExpGain(fish);
        player.setExperience(player.getExperience() + expGain);
        changes.put("experience", expGain);
        
        // 检查升级
        checkLevelUp(player, changes);
    }
    
    /**
     * 计算经验值奖励
     */
    private int calculateExpGain(Fish fish) {
        int baseExp = 5;
        
        switch (fish.getRarity()) {
            case "COMMON": return baseExp;
            case "UNCOMMON": return baseExp * 2;
            case "RARE": return baseExp * 3;
            case "LEGENDARY": return baseExp * 5;
            default: return baseExp;
        }
    }
    
    /**
     * 检查升级
     */
    private void checkLevelUp(Player player, Map<String, Integer> changes) {
        int currentLevel = player.getLevel();
        int requiredExp = currentLevel * 100;
        
        if (player.getExperience() >= requiredExp) {
            player.setLevel(currentLevel + 1);
            player.setMaxHealth(player.getMaxHealth() + 10);
            player.setMaxEnergy(player.getMaxEnergy() + 10);
            player.setMaxSanity(player.getMaxSanity() + 5);
            
            // 升级时恢复部分状态
            player.setHealth(player.getMaxHealth());
            player.setEnergy(player.getMaxEnergy());
            
            changes.put("levelUp", 1);
            changes.put("level", player.getLevel());
        }
    }
    
    /**
     * 生成钓鱼信息
     */
    private String generateFishingMessage(Fish fish) {
        StringBuilder message = new StringBuilder();
        message.append("🎣 你钓到了一条").append(fish.getName()).append("！\n\n");
        message.append("📊 鱼类信息：\n");
        message.append("- 类型：").append(getTypeDescription(fish.getType())).append("\n");
        message.append("- 稀有度：").append(getRarityDescription(fish.getRarity())).append("\n");
        message.append("- 大小：").append(fish.getSize()).append("cm\n");
        message.append("- 重量：").append(fish.getWeight()).append("kg\n\n");
        message.append("📝 描述：").append(fish.getDescription());
        
        if ("STRANGE".equals(fish.getType()) || "DANGEROUS".equals(fish.getType())) {
            message.append("\n\n⚠️ 这条鱼看起来很不寻常，让你感到不安...");
        }
        
        return message.toString();
    }
    
    /**
     * 获取类型描述
     */
    private String getTypeDescription(String type) {
        switch (type) {
            case "NORMAL": return "普通鱼类";
            case "STRANGE": return "奇异鱼类";
            case "DANGEROUS": return "危险鱼类";
            default: return "未知类型";
        }
    }
    
    /**
     * 获取稀有度描述
     */
    private String getRarityDescription(String rarity) {
        switch (rarity) {
            case "COMMON": return "常见";
            case "UNCOMMON": return "不常见";
            case "RARE": return "稀有";
            case "LEGENDARY": return "传说";
            default: return "未知";
        }
    }
    
    /**
     * 食用鱼类
     */
    public FishingResult eatFish(String playerName, Long fishId) {
        Player player = playerRepository.findByName(playerName)
                .orElseThrow(() -> new RuntimeException("玩家不存在"));
                
        Fish fish = fishRepository.findById(fishId)
                .orElseThrow(() -> new RuntimeException("鱼类不存在"));
        
        FishingResult result = new FishingResult(true, "");
        Map<String, Integer> changes = result.getPlayerChanges();
        
        if (!fish.getIsEdible()) {
            return new FishingResult(false, "这条鱼不能食用！");
        }
        
        if (fish.getIsToxic() && player.getSanity() > 30) {
            return new FishingResult(false, "你的理智告诉你，这条鱼有毒，不应该吃它！");
        }
        
        // 应用食用效果
        player.setHealth(Math.min(player.getMaxHealth(), 
                Math.max(0, player.getHealth() + fish.getHealthEffect())));
        player.setSanity(Math.max(1, player.getSanity() + fish.getSanityEffect()));
        player.setEnergy(Math.min(player.getMaxEnergy(), 
                Math.max(0, player.getEnergy() + fish.getEnergyEffect())));
        player.setHunger(Math.min(player.getMaxHunger(), 
                player.getHunger() + fish.getHungerRestore()));
        player.setThirst(Math.min(player.getMaxThirst(), 
                player.getThirst() + fish.getThirstRestore()));
        
        changes.put("health", fish.getHealthEffect());
        changes.put("sanity", fish.getSanityEffect());
        changes.put("energy", fish.getEnergyEffect());
        changes.put("hunger", fish.getHungerRestore());
        changes.put("thirst", fish.getThirstRestore());
        
        playerRepository.save(player);
        
        result.setMessage("你食用了" + fish.getName() + "。" + 
                (fish.getIsToxic() ? "虽然有些不适，但你还是坚持吃完了..." : "味道还不错！"));
        
        return result;
    }
} 