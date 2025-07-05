package com.adventure.repository;

import com.adventure.model.Story;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StoryRepository extends JpaRepository<Story, Long> {
    Optional<Story> findByStoryId(String storyId);
    List<Story> findByChapterOrderBySceneAsc(Integer chapter);
    List<Story> findByChapterAndSceneOrderByIdAsc(Integer chapter, Integer scene);
} 