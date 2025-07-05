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
@Table(name = "players")
public class Player {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String name;
    
    @Column(nullable = false)
    private Integer gold = 100;
    
    // 角色属性系统
    @Column(nullable = false)
    private Integer strength = 3; // 力量
    
    @Column(nullable = false)
    private Integer spirit = 7; // 精神
    
    @Column(nullable = false)
    private Integer agility = 4; // 敏捷
    
    @Column(nullable = false)
    private Integer constitution = 3; // 体质
    
    @Column(nullable = false)
    private Integer perception = 5; // 感知
    
    @Column(nullable = false)
    private Integer sanity = 100; // 理智
    
    @Column(nullable = false)
    private Integer maxSanity = 100; // 最大理智
    
    @Column(nullable = false)
    private Integer energy = 100; // 精力
    
    @Column(nullable = false)
    private Integer maxEnergy = 100; // 最大精力
    
    @Column(nullable = false)
    private Integer health = 100; // 气血
    
    @Column(nullable = false)
    private Integer maxHealth = 100; // 最大气血
    
    // 生存系统
    @Column(nullable = false)
    private Integer hunger = 100; // 饥饿值
    
    @Column(nullable = false)
    private Integer maxHunger = 100; // 最大饥饿值
    
    @Column(nullable = false)
    private Integer thirst = 100; // 口渴值
    
    @Column(nullable = false)
    private Integer maxThirst = 100; // 最大口渴值
    
    @Column(nullable = false)
    private Integer level = 1;
    
    @Column(nullable = false)
    private Integer experience = 0;
    
    @Column(nullable = false)
    private String currentLocation = "神秘海域";
    
    @Column(nullable = false)
    private String status = "健康"; // 玩家状态
    
    @Column(columnDefinition = "TEXT")
    private String talents = "钢铁意志"; // 天赋，JSON格式存储
    
    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "ship_id")
    private Ship ship;
    
    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "game_state_id")
    private GameState gameState;
    
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
    
    @Column(nullable = false)
    private LocalDateTime updatedAt = LocalDateTime.now();
    
    @PreUpdate
    public void preUpdate() {
        updatedAt = LocalDateTime.now();
    }
} 