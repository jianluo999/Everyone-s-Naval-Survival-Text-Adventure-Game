package com.adventure.repository;

import com.adventure.model.Talent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TalentRepository extends JpaRepository<Talent, Long> {
    
    // 根据天赋ID查找
    Optional<Talent> findByTalentId(String talentId);
    
    // 根据类型查找天赋
    List<Talent> findByType(String type);
    
    // 查找已显示的天赋，按排序顺序
    @Query("SELECT t FROM Talent t WHERE t.revealed = true ORDER BY t.sortOrder ASC")
    List<Talent> findRevealedTalentsOrderBySortOrder();
    
    // 查找所有天赋，按排序顺序
    @Query("SELECT t FROM Talent t ORDER BY t.sortOrder ASC")
    List<Talent> findAllOrderBySortOrder();
    
    // 根据解锁条件类型查找天赋
    List<Talent> findByCondition(String condition);
}
