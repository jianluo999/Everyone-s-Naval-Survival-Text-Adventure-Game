package com.adventure.repository;

import com.adventure.model.Island;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface IslandRepository extends JpaRepository<Island, Long> {
    
    // 根据岛屿ID查找
    Optional<Island> findByIslandId(String islandId);
    
    // 根据类型查找岛屿
    List<Island> findByType(String type);
    
    // 查找可访问的岛屿
    List<Island> findByAccessibleTrue();
    
    // 根据玩家等级查找可访问的岛屿
    @Query("SELECT i FROM Island i WHERE i.accessible = true AND i.requiredLevel <= :playerLevel")
    List<Island> findAccessibleIslandsByLevel(@Param("playerLevel") Integer playerLevel);
    
    // 根据危险等级查找岛屿
    List<Island> findByDangerLevel(Integer dangerLevel);
    
    // 查找指定危险等级范围内的岛屿
    @Query("SELECT i FROM Island i WHERE i.dangerLevel BETWEEN :minLevel AND :maxLevel")
    List<Island> findByDangerLevelBetween(@Param("minLevel") Integer minLevel, @Param("maxLevel") Integer maxLevel);
}
