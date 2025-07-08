package com.adventure.service;

import com.adventure.model.ChatMessage;
import com.adventure.repository.ChatMessageRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@Transactional
public class ChatService {

    private static final Logger logger = LoggerFactory.getLogger(ChatService.class);

    @Autowired
    private ChatMessageRepository chatMessageRepository;

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    /**
     * 保存聊天消息
     */
    public ChatMessage saveMessage(ChatMessage message) {
        logger.info("💾 [CHAT-SERVICE] 保存消息 - 玩家: {}, 频道: {}", 
                   message.getPlayerName(), message.getChannel());
        
        // 设置时间戳
        if (message.getTimestamp() == null) {
            message.setTimestamp(LocalDateTime.now());
        }
        
        // 内容过滤和验证
        message.setContent(filterMessage(message.getContent()));
        
        return chatMessageRepository.save(message);
    }

    /**
     * 获取最近的消息
     */
    public List<ChatMessage> getRecentMessages(ChatMessage.ChatChannel channel, Pageable pageable) {
        logger.info("📖 [CHAT-SERVICE] 获取最近消息 - 频道: {}, 页面: {}", channel, pageable.getPageNumber());
        return chatMessageRepository.findByChannelOrderByTimestampDesc(channel, pageable);
    }

    /**
     * 获取指定时间后的消息
     */
    public List<ChatMessage> getMessagesAfter(ChatMessage.ChatChannel channel, LocalDateTime after) {
        return chatMessageRepository.findByChannelAndTimestampAfterOrderByTimestampAsc(channel, after);
    }

    /**
     * 获取区域聊天消息
     */
    public List<ChatMessage> getRegionMessages(String region, Pageable pageable) {
        return chatMessageRepository.findByChannelAndRegionOrderByTimestampDesc(
            ChatMessage.ChatChannel.REGION, region, pageable);
    }

    /**
     * 获取活跃玩家名单
     */
    public List<String> getActivePlayersNames() {
        // 获取最近1小时内发言的玩家
        LocalDateTime since = LocalDateTime.now().minusHours(1);
        return chatMessageRepository.findActivePlayersNames(since);
    }

    /**
     * 发送系统消息
     */
    public void sendSystemMessage(String content, ChatMessage.ChatChannel channel) {
        ChatMessage systemMessage = new ChatMessage(
            "系统", 
            content, 
            channel, 
            ChatMessage.MessageType.SYSTEM
        );
        
        ChatMessage savedMessage = saveMessage(systemMessage);
        broadcastMessage(savedMessage);
        
        logger.info("📢 [CHAT-SERVICE] 系统消息已发送 - 频道: {}, 内容: {}", channel, content);
    }

    /**
     * 发送警告消息
     */
    public void sendWarningMessage(String content) {
        ChatMessage warningMessage = new ChatMessage(
            "系统警告", 
            content, 
            ChatMessage.ChatChannel.SYSTEM, 
            ChatMessage.MessageType.WARNING
        );
        
        ChatMessage savedMessage = saveMessage(warningMessage);
        broadcastMessage(savedMessage);
        
        logger.info("⚠️ [CHAT-SERVICE] 警告消息已发送 - 内容: {}", content);
    }

    /**
     * 发送公告消息
     */
    public void sendAnnouncementMessage(String content) {
        ChatMessage announcement = new ChatMessage(
            "系统公告", 
            content, 
            ChatMessage.ChatChannel.SYSTEM, 
            ChatMessage.MessageType.ANNOUNCEMENT
        );
        
        ChatMessage savedMessage = saveMessage(announcement);
        broadcastMessage(savedMessage);
        
        logger.info("📣 [CHAT-SERVICE] 公告消息已发送 - 内容: {}", content);
    }

    /**
     * 清理过期消息
     */
    public void cleanupOldMessages(int daysToKeep) {
        LocalDateTime cutoffDate = LocalDateTime.now().minusDays(daysToKeep);
        chatMessageRepository.deleteByTimestampBefore(cutoffDate);
        logger.info("🧹 [CHAT-SERVICE] 已清理 {} 天前的消息", daysToKeep);
    }

    /**
     * 消息内容过滤
     */
    private String filterMessage(String content) {
        if (content == null || content.trim().isEmpty()) {
            throw new IllegalArgumentException("消息内容不能为空");
        }
        
        // 限制消息长度
        if (content.length() > 500) {
            content = content.substring(0, 500) + "...";
        }
        
        // 简单的敏感词过滤（可以扩展）
        content = content.replaceAll("(?i)(fuck|shit|damn)", "***");
        
        return content.trim();
    }

    /**
     * 广播消息到对应频道
     */
    private void broadcastMessage(ChatMessage message) {
        String destination = switch (message.getChannel()) {
            case WORLD -> "/topic/chat/world";
            case REGION -> "/topic/chat/region";
            case SYSTEM -> "/topic/chat/system";
            case TRADE -> "/topic/chat/trade";
        };
        
        messagingTemplate.convertAndSend(destination, message);
    }
}
