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
    
    // 天数系统
    @Column(nullable = false)
    private Integer currentDay = 1; // 当前天数
    
    @Column(nullable = false)
    private Integer currentHour = 8; // 当前小时（0-23）
    
    @Column(nullable = false)
    private LocalDateTime gameStartTime = LocalDateTime.now(); // 游戏开始时间
    
    @Column(nullable = false)
    private LocalDateTime lastDayUpdateTime = LocalDateTime.now(); // 上次天数更新时间
    
    @Column(nullable = false)
    private Integer actionsToday = 0; // 今日行动次数
    
    @Column(nullable = false)
    private Integer maxActionsPerDay = 10; // 每日最大行动次数
    
    @PreUpdate
    public void preUpdate() {
        lastPlayedAt = LocalDateTime.now();
    }
    
    // 时间推进方法
    public void advanceTime(int hours) {
        this.currentHour += hours;
        while (this.currentHour >= 24) {
            this.currentHour -= 24;
            this.currentDay++;
            this.actionsToday = 0; // 新的一天重置行动次数
        }
    }
    
    // 执行行动
    public boolean performAction() {
        if (this.actionsToday >= this.maxActionsPerDay) {
            return false; // 行动次数已满
        }
        this.actionsToday++;
        return true;
    }
    
    // 获取时间描述
    public String getTimeDescription() {
        if (currentHour >= 6 && currentHour < 12) {
            return "上午";
        } else if (currentHour >= 12 && currentHour < 18) {
            return "下午";
        } else if (currentHour >= 18 && currentHour < 22) {
            return "傍晚";
        } else {
            return "深夜";
        }
    }
} 