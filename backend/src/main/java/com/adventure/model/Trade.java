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
@Table(name = "trades")
public class Trade {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String sellerId; // 卖家玩家ID
    
    @Column(nullable = false)
    private String sellerName; // 卖家名称
    
    @Column(nullable = false)
    private String sellerShip; // 卖家船只名称
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String offering; // 提供的物品，JSON格式
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String wanting; // 想要的物品，JSON格式
    
    @Column(nullable = false)
    private String status = "active"; // active, completed, cancelled
    
    @Column(nullable = false)
    private String quality = "common"; // common, good, excellent, rare, legendary
    
    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
    
    @Column(nullable = false)
    private LocalDateTime updatedAt = LocalDateTime.now();
    
    @PreUpdate
    public void preUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
