package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "monsters")
public class Monster {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String monsterId; // 如 "drowned_sailor"
    
    @Column(nullable = false)
    private String name; // 怪物名称
    
    @Column(columnDefinition = "TEXT")
    private String description; // 怪物描述
    
    @Column(nullable = false)
    private Integer health = 100; // 生命值
    
    @Column(nullable = false)
    private Integer maxHealth = 100; // 最大生命值
    
    @Column(nullable = false)
    private Integer attack = 10; // 攻击力
    
    @Column(nullable = false)
    private Integer defense = 0; // 防御力
    
    @Column(nullable = false)
    private Integer speed = 5; // 速度
    
    @Column(nullable = false)
    private String monsterType = "NORMAL"; // 怪物类型：NORMAL, UNDEAD, ELDRITCH等
    
    @Column(columnDefinition = "TEXT")
    private String abilities = ""; // 特殊能力，JSON格式
    
    @Column(columnDefinition = "TEXT")
    private String loot = ""; // 掉落物品，JSON格式
    
    @Column(nullable = false)
    private Integer sanityDamage = 0; // 造成的理智伤害
    
    @Column(nullable = false)
    private Boolean canRevive = false; // 是否可以复活
    
    @Column(nullable = false)
    private Boolean canExplode = false; // 是否会自爆
    
    @Column(nullable = false)
    private String encounterStoryId = ""; // 遭遇时的故事ID
}
