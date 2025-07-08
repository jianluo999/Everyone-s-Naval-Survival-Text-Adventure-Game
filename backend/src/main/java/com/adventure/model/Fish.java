package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "fish")
public class Fish {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name; // 鱼类名称
    
    @Column(nullable = false)
    private String type; // 鱼类类型：NORMAL, STRANGE, DANGEROUS
    
    @Column(columnDefinition = "TEXT")
    private String description; // 描述
    
    @Column
    private String imageName; // 图片文件名
    
    @Column(nullable = false)
    private String rarity; // 稀有度：COMMON, UNCOMMON, RARE, LEGENDARY
    
    @Column(nullable = false)
    private Integer size = 1; // 鱼的大小（1-100）
    
    @Column(nullable = false)
    private Double weight = 0.1; // 重量（kg）
    
    @Column(nullable = false)
    private Boolean isEdible = true; // 是否可食用
    
    @Column(nullable = false)
    private Boolean isToxic = false; // 是否有毒
    
    // 食用效果
    @Column(nullable = false)
    private Integer healthEffect = 0; // 对健康的影响
    
    @Column(nullable = false)
    private Integer sanityEffect = 0; // 对理智的影响
    
    @Column(nullable = false)
    private Integer energyEffect = 0; // 对精力的影响
    
    @Column(nullable = false)
    private Integer hungerRestore = 0; // 恢复饥饿值
    
    @Column(nullable = false)
    private Integer thirstRestore = 0; // 恢复口渴值
    
    // 属性加成（临时）
    @Column(nullable = false)
    private Integer strengthBonus = 0; // 力量加成
    
    @Column(nullable = false)
    private Integer spiritBonus = 0; // 精神加成
    
    @Column(nullable = false)
    private Integer agilityBonus = 0; // 敏捷加成
    
    @Column(nullable = false)
    private Integer constitutionBonus = 0; // 体质加成
    
    @Column(nullable = false)
    private Integer perceptionBonus = 0; // 感知加成
    
    @Column(nullable = false)
    private Integer bonusDuration = 0; // 加成持续时间（分钟）
    
    @Column(nullable = false)
    private Integer catchDifficulty = 1; // 钓鱼难度（1-10）
    
    @Column(nullable = false)
    private Double catchProbability = 0.5; // 钓到概率（0-1）
    
    @Column(columnDefinition = "TEXT")
    private String catchCondition; // 钓到条件（JSON格式）
    
    @Column(columnDefinition = "TEXT")
    private String specialEffects; // 特殊效果（JSON格式）
} 