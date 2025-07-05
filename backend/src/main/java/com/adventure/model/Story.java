package com.adventure.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "stories")
public class Story {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String storyId; // 如 "story_1_1"
    
    @Column(nullable = false)
    private String title;
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String content;
    
    @Column(nullable = false)
    private Integer chapter = 1;
    
    @Column(nullable = false)
    private Integer scene = 1;
    
    @Column(columnDefinition = "TEXT")
    private String imageUrl; // 场景图片URL
    
    @Column(nullable = false)
    private Boolean isEnding = false;
    
    @Column(nullable = false)
    private String storyType = "NORMAL"; // NORMAL, BATTLE, TRADE, etc.
} 