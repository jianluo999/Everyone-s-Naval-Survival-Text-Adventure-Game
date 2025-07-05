package com.adventure.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

/**
 * 材料实体类
 */
@Entity
@Table(name = "materials")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Material {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 材料名称
     */
    @Column(nullable = false)
    private String name;
    
    /**
     * 材料类型：木料、布料、钢铁、食物、淡水等
     */
    @Column(nullable = false)
    private String type;
    
    /**
     * 材料品质
     */
    private String quality = "普通";
    
    /**
     * 材料描述
     */
    @Column(length = 500)
    private String description;
    
    /**
     * 材料图标
     */
    private String icon;
    
    /**
     * 数量
     */
    @Column(nullable = false)
    private Integer quantity = 0;
    
    /**
     * 最大堆叠数量
     */
    private Integer maxStack = 999;
    
    /**
     * 所属玩家ID
     */
    @Column(name = "player_id")
    private Long playerId;
    
    /**
     * 是否可消耗
     */
    private Boolean consumable = true;
    
    /**
     * 营养值（食物类材料）
     */
    private Integer nutrition = 0;
    
    /**
     * 水分值（饮品类材料）
     */
    private Integer hydration = 0;
    
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