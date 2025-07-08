package com.adventure.repository;

import com.adventure.model.Fish;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FishRepository extends JpaRepository<Fish, Long> {
    
    // 根据类型查找鱼类
    List<Fish> findByType(String type);
    
    // 根据稀有度查找鱼类
    List<Fish> findByRarity(String rarity);
    
    // 查找可食用的鱼类
    List<Fish> findByIsEdibleTrue();
    
    // 查找有毒的鱼类
    List<Fish> findByIsToxicTrue();
    
    // 根据钓鱼难度查找
    List<Fish> findByCatchDifficultyLessThanEqual(Integer difficulty);
    
    // 随机获取一条鱼（用于钓鱼）
    @Query(value = "SELECT * FROM fish WHERE catch_probability >= :minProbability ORDER BY RAND() LIMIT 1", nativeQuery = true)
    Fish findRandomFish(@Param("minProbability") Double minProbability);

    // 根据玩家条件获取可钓到的鱼类
    @Query(value = "SELECT * FROM fish WHERE catch_difficulty <= :playerSkill ORDER BY RAND() LIMIT :limit", nativeQuery = true)
    List<Fish> findFishByPlayerSkill(@Param("playerSkill") Integer playerSkill, @Param("limit") Integer limit);
} 