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
@Table(name = "chat_messages")
public class ChatMessage {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String playerName;
    
    @Column(nullable = false, columnDefinition = "TEXT")
    private String content;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ChatChannel channel;
    
    @Column(nullable = false)
    private LocalDateTime timestamp = LocalDateTime.now();
    
    // 可选：消息类型（普通消息、系统消息、交易消息等）
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private MessageType messageType = MessageType.NORMAL;
    
    // 可选：区域信息（用于区域聊天）
    private String region;
    
    // 可选：交易相关信息（JSON格式）
    @Column(columnDefinition = "TEXT")
    private String tradeData;
    
    public enum ChatChannel {
        WORLD,      // 世界频道
        REGION,     // 区域频道
        SYSTEM,     // 系统频道
        TRADE       // 交易频道
    }
    
    public enum MessageType {
        NORMAL,     // 普通消息
        SYSTEM,     // 系统消息
        TRADE,      // 交易消息
        WARNING,    // 警告消息
        ANNOUNCEMENT // 公告消息
    }
    
    // 构造函数
    public ChatMessage(String playerName, String content, ChatChannel channel) {
        this.playerName = playerName;
        this.content = content;
        this.channel = channel;
        this.timestamp = LocalDateTime.now();
    }
    
    public ChatMessage(String playerName, String content, ChatChannel channel, MessageType messageType) {
        this.playerName = playerName;
        this.content = content;
        this.channel = channel;
        this.messageType = messageType;
        this.timestamp = LocalDateTime.now();
    }
}
