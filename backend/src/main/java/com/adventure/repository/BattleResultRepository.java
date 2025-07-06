package com.adventure.repository;

import com.adventure.model.BattleResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BattleResultRepository extends JpaRepository<BattleResult, Long> {
    List<BattleResult> findByPlayerIdOrderByBattleTimeDesc(Long playerId);
    List<BattleResult> findByMonsterIdOrderByBattleTimeDesc(String monsterId);
}
