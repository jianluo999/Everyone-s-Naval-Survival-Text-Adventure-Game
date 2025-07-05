package com.sailinggame.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

/**
 * 装备实体类
 */
@Entity
@Table(name = "equipment")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Equipment {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 装备名称
     */
    @Column(nullable = false)
    private String name;
    
    /**
     * 装备类型：遗物、工具、武器等
     */
    @Column(nullable = false)
    private String type;
    
    /**
     * 装备品质：普通、良品、精品、珍品、极品、英雄、大师
     */
    @Column(nullable = false)
    private String quality;
    
    /**
     * 装备描述
     */
    @Column(length = 1000)
    private String description;
    
    /**
     * 装备图标
     */
    private String icon;
    
    /**
     * 攻击力
     */
    private Integer attack = 0;
    
    /**
     * 防御力
     */
    private Integer defense = 0;
    
    /**
     * 耐久度
     */
    private Integer durability = 100;
    
    /**
     * 最大耐久度
     */
    private Integer maxDurability = 100;
    
    /**
     * 成功率（对于燧发枪等装备）
     */
    private Double successRate = 1.0;
    
    /**
     * 冷却时间（秒）
     */
    private Integer cooldown = 0;
    
    /**
     * 特殊效果JSON
     */
    @Column(length = 2000)
    private String specialEffects;
    
    /**
     * 使用理智消耗
     */
    private Integer sanityConsumption = 0;
    
    /**
     * 是否可使用
     */
    private Boolean usable = true;
    
    /**
     * 所属玩家ID
     */
    @Column(name = "player_id")
    private Long playerId;
    
    /**
     * 是否已装备
     */
    private Boolean equipped = false;
    
    /**
     * 装备位置（武器、工具、饰品等）
     */
    private String equipSlot;
    
    /**
     * 创建时间
     */
    @Column(name = "created_at")
    private java.time.LocalDateTime createdAt;
    
    /**
     * 更新时间
     */
    @Column(name = "updated_at")
    private java.time.LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = java.time.LocalDateTime.now();
        updatedAt = java.time.LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = java.time.LocalDateTime.now();
    }
} 