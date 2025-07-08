package com.adventure.controller;

import com.adventure.model.ChatMessage;
import com.adventure.service.ChatService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"})
public class ChatController {

    private static final Logger logger = LoggerFactory.getLogger(ChatController.class);

    @Autowired
    private ChatService chatService;

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    /**
     * 处理聊天消息发送
     */
    @MessageMapping("/chat.sendMessage")
    @SendTo("/topic/public")
    public ChatMessage sendMessage(@Payload ChatMessage chatMessage) {
        logger.info("💬 [CHAT] 收到消息 - 玩家: {}, 频道: {}, 内容: {}", 
                   chatMessage.getPlayerName(), chatMessage.getChannel(), chatMessage.getContent());
        
        try {
            // 保存消息到数据库
            ChatMessage savedMessage = chatService.saveMessage(chatMessage);
            
            // 根据频道广播消息
            broadcastMessage(savedMessage);
            
            logger.info("✅ [CHAT] 消息发送成功 - ID: {}", savedMessage.getId());
            return savedMessage;
        } catch (Exception e) {
            logger.error("❌ [CHAT] 消息发送失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 处理玩家加入聊天
     */
    @MessageMapping("/chat.addUser")
    @SendTo("/topic/public")
    public ChatMessage addUser(@Payload ChatMessage chatMessage, SimpMessageHeaderAccessor headerAccessor) {
        // 在WebSocket会话中添加用户名
        headerAccessor.getSessionAttributes().put("username", chatMessage.getPlayerName());
        
        logger.info("🎮 [CHAT] 玩家加入聊天 - {}", chatMessage.getPlayerName());
        
        // 创建系统消息
        ChatMessage systemMessage = new ChatMessage(
            "系统", 
            chatMessage.getPlayerName() + " 加入了聊天", 
            ChatMessage.ChatChannel.SYSTEM,
            ChatMessage.MessageType.SYSTEM
        );
        
        return chatService.saveMessage(systemMessage);
    }

    /**
     * REST API: 获取聊天历史
     */
    @GetMapping("/api/chat/history/{channel}")
    public ResponseEntity<Map<String, Object>> getChatHistory(
            @PathVariable String channel,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size) {
        
        try {
            ChatMessage.ChatChannel chatChannel = ChatMessage.ChatChannel.valueOf(channel.toUpperCase());
            List<ChatMessage> messages = chatService.getRecentMessages(chatChannel, PageRequest.of(page, size));
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("messages", messages);
            response.put("total", messages.size());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("❌ [CHAT] 获取聊天历史失败: {}", e.getMessage(), e);
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * REST API: 获取活跃玩家列表
     */
    @GetMapping("/api/chat/active-players")
    public ResponseEntity<Map<String, Object>> getActivePlayers() {
        try {
            List<String> activePlayers = chatService.getActivePlayersNames();
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("players", activePlayers);
            response.put("count", activePlayers.size());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("❌ [CHAT] 获取活跃玩家失败: {}", e.getMessage(), e);
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 根据频道广播消息
     */
    private void broadcastMessage(ChatMessage message) {
        String destination = switch (message.getChannel()) {
            case WORLD -> "/topic/chat/world";
            case REGION -> "/topic/chat/region";
            case SYSTEM -> "/topic/chat/system";
            case TRADE -> "/topic/chat/trade";
        };
        
        messagingTemplate.convertAndSend(destination, message);
        logger.info("📡 [CHAT] 消息已广播到 {} - 内容: {}", destination, message.getContent());
    }
}
