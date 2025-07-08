package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "talents")
public class Talent {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String talentId; // 如 "fishing_master"
    
    @Column(nullable = false)
    private String name; // 天赋名称
    
    @Column(nullable = false)
    private String icon; // 天赋图标
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String description; // 天赋描述
    
    @Column(nullable = false)
    private String type; // survival, skill, combat, etc.
    
    @Column(nullable = false)
    private Integer requirement = 1; // 解锁需求数量
    
    @Column(nullable = false)
    private String condition; // 解锁条件类型：survive_days, fishing_attempts, etc.
    
    @Column(columnDefinition = "TEXT")
    private String hint; // 解锁提示
    
    @Column(columnDefinition = "TEXT")
    private String effects; // 天赋效果，JSON格式
    
    @Column(nullable = false)
    private Boolean revealed = false; // 是否已显示给玩家
    
    @Column(nullable = false)
    private Integer sortOrder = 0; // 排序顺序
}
