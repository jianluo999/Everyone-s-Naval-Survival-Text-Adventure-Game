package com.adventure.repository;

import com.adventure.model.Material;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface MaterialRepository extends JpaRepository<Material, Long> {
    
    /**
     * 根据玩家ID查找材料
     */
    List<Material> findByPlayerId(Long playerId);
    
    /**
     * 根据玩家ID和材料类型查找材料
     */
    List<Material> findByPlayerIdAndType(Long playerId, String type);
    
    /**
     * 根据玩家ID和材料名称查找材料
     */
    Optional<Material> findByPlayerIdAndName(Long playerId, String name);
    
    /**
     * 根据材料类型查找材料
     */
    List<Material> findByType(String type);
    
    /**
     * 根据玩家ID查找食物类材料
     */
    @Query("SELECT m FROM Material m WHERE m.playerId = :playerId AND m.nutrition > 0")
    List<Material> findFoodByPlayerId(@Param("playerId") Long playerId);
    
    /**
     * 根据玩家ID查找饮品类材料
     */
    @Query("SELECT m FROM Material m WHERE m.playerId = :playerId AND m.hydration > 0")
    List<Material> findDrinksByPlayerId(@Param("playerId") Long playerId);
    
    /**
     * 根据玩家ID查找可消耗材料
     */
    List<Material> findByPlayerIdAndConsumableTrue(Long playerId);
    
    /**
     * 根据玩家ID和材料类型查找有数量的材料
     */
    @Query("SELECT m FROM Material m WHERE m.playerId = :playerId AND m.type = :type AND m.quantity > 0")
    List<Material> findByPlayerIdAndTypeWithQuantity(@Param("playerId") Long playerId, @Param("type") String type);
} 