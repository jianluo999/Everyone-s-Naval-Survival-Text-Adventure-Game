package com.adventure.repository;

import com.adventure.model.Player;
import com.adventure.model.PlayerTalent;
import com.adventure.model.Talent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PlayerTalentRepository extends JpaRepository<PlayerTalent, Long> {
    
    // 根据玩家查找所有天赋
    List<PlayerTalent> findByPlayer(Player player);
    
    // 根据玩家查找已解锁的天赋
    @Query("SELECT pt FROM PlayerTalent pt WHERE pt.player = :player AND pt.unlocked = true")
    List<PlayerTalent> findUnlockedTalentsByPlayer(@Param("player") Player player);
    
    // 根据玩家和天赋查找
    Optional<PlayerTalent> findByPlayerAndTalent(Player player, Talent talent);
    
    // 根据玩家ID查找天赋
    @Query("SELECT pt FROM PlayerTalent pt WHERE pt.player.id = :playerId")
    List<PlayerTalent> findByPlayerId(@Param("playerId") Long playerId);
    
    // 查找玩家的特定类型天赋
    @Query("SELECT pt FROM PlayerTalent pt WHERE pt.player = :player AND pt.talent.type = :type")
    List<PlayerTalent> findByPlayerAndTalentType(@Param("player") Player player, @Param("type") String type);
}
