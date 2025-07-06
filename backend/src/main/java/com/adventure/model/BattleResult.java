package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "battle_results")
public class BattleResult {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private Long playerId; // 玩家ID
    
    @Column(nullable = false)
    private String monsterId; // 怪物ID
    
    @Column(nullable = false)
    private String battleType = "ENCOUNTER"; // 战斗类型：ENCOUNTER, BOSS, RANDOM等
    
    @Column(nullable = false)
    private Boolean playerWon = false; // 玩家是否获胜
    
    @Column(nullable = false)
    private Integer damageDealt = 0; // 玩家造成的伤害
    
    @Column(nullable = false)
    private Integer damageTaken = 0; // 玩家受到的伤害
    
    @Column(nullable = false)
    private Integer sanityLost = 0; // 失去的理智值
    
    @Column(columnDefinition = "TEXT")
    private String battleLog = ""; // 战斗日志，JSON格式
    
    @Column(columnDefinition = "TEXT")
    private String rewards = ""; // 战斗奖励，JSON格式
    
    @Column(nullable = false)
    private LocalDateTime battleTime = LocalDateTime.now(); // 战斗时间
    
    @Column(nullable = false)
    private String storyContext = ""; // 故事背景
}
