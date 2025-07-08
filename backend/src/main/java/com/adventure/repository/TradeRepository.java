package com.adventure.repository;

import com.adventure.model.Trade;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TradeRepository extends JpaRepository<Trade, Long> {
    
    // 根据状态查找交易
    List<Trade> findByStatus(String status);
    
    // 根据卖家查找交易
    List<Trade> findBySellerId(String sellerId);
    
    // 根据品质查找交易
    List<Trade> findByQuality(String quality);
    
    // 查找活跃的交易，按创建时间排序
    @Query("SELECT t FROM Trade t WHERE t.status = 'active' ORDER BY t.createdAt DESC")
    List<Trade> findActiveTradesOrderByCreatedAt();
    
    // 根据品质和状态查找交易
    List<Trade> findByQualityAndStatus(String quality, String status);
    
    // 查找指定卖家的活跃交易
    @Query("SELECT t FROM Trade t WHERE t.sellerId = :sellerId AND t.status = 'active'")
    List<Trade> findActiveTradesBySeller(@Param("sellerId") String sellerId);
}
