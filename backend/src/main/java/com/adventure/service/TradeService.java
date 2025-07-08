package com.adventure.service;

import com.adventure.model.Trade;
import com.adventure.repository.TradeRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class TradeService {
    
    private static final Logger logger = LoggerFactory.getLogger(TradeService.class);
    
    @Autowired
    private TradeRepository tradeRepository;
    
    /**
     * 获取所有活跃的交易
     */
    public List<Trade> getActiveTrades() {
        logger.info("🏪 [TRADE] 获取活跃交易列表");
        return tradeRepository.findActiveTradesOrderByCreatedAt();
    }
    
    /**
     * 根据品质筛选交易
     */
    public List<Trade> getTradesByQuality(String quality) {
        logger.info("🏪 [TRADE] 根据品质筛选交易 - 品质: {}", quality);
        if ("all".equals(quality)) {
            return getActiveTrades();
        }
        return tradeRepository.findByQualityAndStatus(quality, "active");
    }
    
    /**
     * 创建新交易
     */
    public Trade createTrade(String sellerId, String sellerName, String sellerShip, 
                           String offering, String wanting, String quality) {
        logger.info("🏪 [TRADE] 创建新交易 - 卖家: {}, 船只: {}", sellerName, sellerShip);
        
        Trade trade = new Trade();
        trade.setSellerId(sellerId);
        trade.setSellerName(sellerName);
        trade.setSellerShip(sellerShip);
        trade.setOffering(offering);
        trade.setWanting(wanting);
        trade.setQuality(quality);
        trade.setStatus("active");
        
        Trade savedTrade = tradeRepository.save(trade);
        logger.info("✅ [TRADE] 交易创建成功 - ID: {}", savedTrade.getId());
        
        return savedTrade;
    }
    
    /**
     * 完成交易
     */
    public Trade completeTrade(Long tradeId) {
        logger.info("🏪 [TRADE] 完成交易 - ID: {}", tradeId);
        
        Optional<Trade> tradeOpt = tradeRepository.findById(tradeId);
        if (tradeOpt.isEmpty()) {
            throw new RuntimeException("交易不存在");
        }
        
        Trade trade = tradeOpt.get();
        trade.setStatus("completed");
        
        Trade savedTrade = tradeRepository.save(trade);
        logger.info("✅ [TRADE] 交易完成 - ID: {}", savedTrade.getId());
        
        return savedTrade;
    }
    
    /**
     * 取消交易
     */
    public Trade cancelTrade(Long tradeId) {
        logger.info("🏪 [TRADE] 取消交易 - ID: {}", tradeId);
        
        Optional<Trade> tradeOpt = tradeRepository.findById(tradeId);
        if (tradeOpt.isEmpty()) {
            throw new RuntimeException("交易不存在");
        }
        
        Trade trade = tradeOpt.get();
        trade.setStatus("cancelled");
        
        Trade savedTrade = tradeRepository.save(trade);
        logger.info("✅ [TRADE] 交易取消 - ID: {}", savedTrade.getId());
        
        return savedTrade;
    }
    
    /**
     * 获取玩家的交易
     */
    public List<Trade> getPlayerTrades(String playerId) {
        logger.info("🏪 [TRADE] 获取玩家交易 - 玩家ID: {}", playerId);
        return tradeRepository.findBySellerId(playerId);
    }
}
