package com.adventure.repository;

import com.adventure.model.Monster;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface MonsterRepository extends JpaRepository<Monster, Long> {
    Optional<Monster> findByMonsterId(String monsterId);
    List<Monster> findByMonsterType(String monsterType);
    List<Monster> findByEncounterStoryId(String storyId);
}
