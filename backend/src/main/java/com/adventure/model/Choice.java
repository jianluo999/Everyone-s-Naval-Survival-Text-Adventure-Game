package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "choices")
public class Choice {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String text; // 选择的文本
    
    @Column(nullable = false)
    private String nextStoryId; // 指向下一个故事的ID
    
    @Column(nullable = false)
    private Integer goldCost = 0; // 选择需要的金币
    
    @Column(nullable = false)
    private Integer goldReward = 0; // 选择获得的金币
    
    @Column(nullable = false)
    private Integer healthCost = 0; // 选择需要的健康值
    
    @Column(nullable = false)
    private Integer healthReward = 0; // 选择获得的健康值
    
    @Column(nullable = false)
    private Integer experienceReward = 0; // 选择获得的经验值
    
    @Column(nullable = false)
    private String requirements = ""; // 选择的需求条件（JSON格式）
    
    @Column(nullable = false)
    private Boolean isAvailable = true; // 选择是否可用
    
    @Column(nullable = false)
    private String storyId; // 所属故事的ID
} 