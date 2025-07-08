package com.adventure.controller;

import com.adventure.model.Trade;
import com.adventure.service.TradeService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/trade")
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"})
public class TradeController {
    
    private static final Logger logger = LoggerFactory.getLogger(TradeController.class);
    
    @Autowired
    private TradeService tradeService;
    
    /**
     * 获取市场交易列表
     */
    @GetMapping("/market")
    public ResponseEntity<Map<String, Object>> getMarketTrades(
            @RequestParam(required = false, defaultValue = "all") String quality) {
        logger.info("🏪 [API] 获取市场交易 - 品质筛选: {}", quality);
        
        try {
            List<Trade> trades = tradeService.getTradesByQuality(quality);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("trades", trades);
            response.put("count", trades.size());
            
            logger.info("✅ [API] 市场交易获取成功 - 数量: {}", trades.size());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("❌ [API] 获取市场交易失败: {}", e.getMessage(), e);
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 创建新交易
     */
    @PostMapping("/create")
    public ResponseEntity<Map<String, Object>> createTrade(@RequestBody Map<String, Object> request) {
        logger.info("🏪 [API] 创建交易请求 - 数据: {}", request);
        
        try {
            String sellerId = (String) request.get("sellerId");
            String sellerName = (String) request.get("sellerName");
            String sellerShip = (String) request.get("sellerShip");
            String offering = (String) request.get("offering");
            String wanting = (String) request.get("wanting");
            String quality = (String) request.getOrDefault("quality", "common");
            
            Trade trade = tradeService.createTrade(sellerId, sellerName, sellerShip, offering, wanting, quality);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "交易创建成功");
            response.put("trade", trade);
            
            logger.info("✅ [API] 交易创建成功 - ID: {}", trade.getId());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("❌ [API] 创建交易失败: {}", e.getMessage(), e);
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 完成交易
     */
    @PostMapping("/{tradeId}/complete")
    public ResponseEntity<Map<String, Object>> completeTrade(@PathVariable Long tradeId) {
        logger.info("🏪 [API] 完成交易请求 - ID: {}", tradeId);
        
        try {
            Trade trade = tradeService.completeTrade(tradeId);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "交易完成");
            response.put("trade", trade);
            
            logger.info("✅ [API] 交易完成成功 - ID: {}", trade.getId());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("❌ [API] 完成交易失败: {}", e.getMessage(), e);
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * 获取玩家的交易
     */
    @GetMapping("/player/{playerId}")
    public ResponseEntity<Map<String, Object>> getPlayerTrades(@PathVariable String playerId) {
        logger.info("🏪 [API] 获取玩家交易 - 玩家ID: {}", playerId);
        
        try {
            List<Trade> trades = tradeService.getPlayerTrades(playerId);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("trades", trades);
            response.put("count", trades.size());
            
            logger.info("✅ [API] 玩家交易获取成功 - 数量: {}", trades.size());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("❌ [API] 获取玩家交易失败: {}", e.getMessage(), e);
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
