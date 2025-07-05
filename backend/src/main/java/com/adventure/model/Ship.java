package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ships")
public class Ship {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name = "破旧木筏";
    
    @Column(nullable = false)
    private String type = "BASIC";
    
    /**
     * 船只分类：破旧木筏、钢铁雄心号、疾风号、樱花号、梦魇号等
     */
    @Column(nullable = false)
    private String category = "破旧木筏";
    
    /**
     * 船只等级
     */
    @Column(nullable = false)
    private Integer level = 1;
    
    @Column(nullable = false)
    private Integer durability = 100;
    
    @Column(nullable = false)
    private Integer maxDurability = 100;
    
    @Column(nullable = false)
    private Integer speed = 8; // 航行速度（节）
    
    @Column(nullable = false)
    private Integer cargoCapacity = 20; // 载货量
    
    @Column(nullable = false)
    private Integer currentCargo = 0;
    
    @Column(nullable = false)
    private Integer attackPower = 0; // 攻击力
    
    @Column(nullable = false)
    private Integer defense = 2; // 防御力
    
    @Column(nullable = false)
    private Boolean hasGrappleHook = true; // 是否有爪钩
    
    @Column(nullable = false)
    private Integer fuel = 100; // 燃料
    
    @Column(nullable = false)
    private Integer maxFuel = 100; // 最大燃料
    
    @Column(nullable = false)
    private Integer food = 50; // 食物
    
    @Column(nullable = false)
    private Integer maxFood = 100; // 最大食物存储
    
    @Column(nullable = false)
    private Integer water = 50; // 淡水
    
    @Column(nullable = false)
    private Integer maxWater = 100; // 最大淡水存储
    
    /**
     * 船只技能JSON字符串
     */
    @Column(columnDefinition = "TEXT")
    private String shipSkills = "[]";
    
    /**
     * 船只稀有度
     */
    private String rarity = "普通";
    
    /**
     * 所属玩家ID
     */
    @Column(name = "player_id")
    private Long playerId;
    
    @Column(columnDefinition = "TEXT")
    private String description = "一艘破旧的木筏，勉强能在海上漂浮。需要尽快升级以应对更大的挑战。";
    
    @Column(columnDefinition = "TEXT")
    private String equipment = "[]"; // 装备，JSON格式存储
} 