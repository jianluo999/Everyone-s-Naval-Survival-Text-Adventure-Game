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
@Table(name = "game_states")
public class GameState {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private Integer currentChapter = 1;
    
    @Column(nullable = false)
    private Integer currentScene = 1;
    
    @Column(nullable = false)
    private String currentStoryId = "story_1_1";
    
    @Column(columnDefinition = "TEXT")
    private String gameData; // JSON格式存储额外的游戏数据
    
    @Column(nullable = false)
    private Boolean isGameActive = true;
    
    @Column(nullable = false)
    private Boolean isGameCompleted = false;
    
    @Column(nullable = false)
    private LocalDateTime lastPlayedAt = LocalDateTime.now();
    
    @Column(nullable = false)
    private Integer totalPlayTime = 0; // 总游戏时间（分钟）
    
    @PreUpdate
    public void preUpdate() {
        lastPlayedAt = LocalDateTime.now();
    }
} 