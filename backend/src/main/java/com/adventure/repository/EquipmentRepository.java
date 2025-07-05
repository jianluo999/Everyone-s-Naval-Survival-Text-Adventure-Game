package com.adventure.repository;

import com.adventure.model.Equipment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EquipmentRepository extends JpaRepository<Equipment, Long> {
    
    /**
     * 根据玩家ID查找装备
     */
    List<Equipment> findByPlayerId(Long playerId);
    
    /**
     * 根据玩家ID和装备类型查找装备
     */
    List<Equipment> findByPlayerIdAndType(Long playerId, String type);
    
    /**
     * 根据玩家ID查找已装备的装备
     */
    List<Equipment> findByPlayerIdAndEquippedTrue(Long playerId);
    
    /**
     * 根据玩家ID和装备位置查找装备
     */
    List<Equipment> findByPlayerIdAndEquipSlot(Long playerId, String equipSlot);
    
    /**
     * 根据装备品质查找装备
     */
    List<Equipment> findByQuality(String quality);
    
    /**
     * 根据装备名称查找装备
     */
    List<Equipment> findByName(String name);
    
    /**
     * 查找可用的装备
     */
    List<Equipment> findByPlayerIdAndUsableTrue(Long playerId);
} 