package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "islands")
public class Island {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String islandId; // 如 "island_beach_001"
    
    @Column(nullable = false)
    private String name; // 岛屿名称
    
    @Column(nullable = false)
    private String icon; // 岛屿图标
    
    @Column(columnDefinition = "TEXT")
    private String description; // 岛屿描述
    
    @Column(nullable = false)
    private String type; // beach, forest, cave, ruins, etc.
    
    @Column(nullable = false)
    private Integer x = 0; // 地图X坐标
    
    @Column(nullable = false)
    private Integer y = 0; // 地图Y坐标
    
    @Column(nullable = false)
    private Integer size = 20; // 地图上的大小
    
    @Column(nullable = false)
    private Boolean accessible = true; // 是否可访问
    
    @Column(columnDefinition = "TEXT")
    private String availableActions; // 可用行动，JSON格式
    
    @Column(columnDefinition = "TEXT")
    private String resources; // 可获得的资源，JSON格式
    
    @Column(nullable = false)
    private Integer dangerLevel = 1; // 危险等级 1-5
    
    @Column(nullable = false)
    private Integer requiredLevel = 1; // 需要的玩家等级
}
