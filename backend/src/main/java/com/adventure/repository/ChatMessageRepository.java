package com.adventure.repository;

import com.adventure.model.ChatMessage;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ChatMessageRepository extends JpaRepository<ChatMessage, Long> {
    
    /**
     * 根据频道获取最近的消息
     */
    List<ChatMessage> findByChannelOrderByTimestampDesc(ChatMessage.ChatChannel channel, Pageable pageable);
    
    /**
     * 根据频道和时间范围获取消息
     */
    List<ChatMessage> findByChannelAndTimestampAfterOrderByTimestampAsc(
        ChatMessage.ChatChannel channel, 
        LocalDateTime after
    );
    
    /**
     * 根据区域获取区域聊天消息
     */
    List<ChatMessage> findByChannelAndRegionOrderByTimestampDesc(
        ChatMessage.ChatChannel channel, 
        String region, 
        Pageable pageable
    );
    
    /**
     * 获取指定玩家的消息历史
     */
    List<ChatMessage> findByPlayerNameOrderByTimestampDesc(String playerName, Pageable pageable);
    
    /**
     * 获取最近的系统消息
     */
    @Query("SELECT cm FROM ChatMessage cm WHERE cm.channel = :channel AND cm.messageType = :messageType ORDER BY cm.timestamp DESC")
    List<ChatMessage> findRecentSystemMessages(
        @Param("channel") ChatMessage.ChatChannel channel,
        @Param("messageType") ChatMessage.MessageType messageType,
        Pageable pageable
    );
    
    /**
     * 清理过期消息（保留最近N天的消息）
     */
    void deleteByTimestampBefore(LocalDateTime before);
    
    /**
     * 统计频道消息数量
     */
    long countByChannel(ChatMessage.ChatChannel channel);
    
    /**
     * 获取活跃玩家列表（最近发言的玩家）
     */
    @Query("SELECT DISTINCT cm.playerName FROM ChatMessage cm WHERE cm.timestamp > :since ORDER BY cm.timestamp DESC")
    List<String> findActivePlayersNames(@Param("since") LocalDateTime since);
}
