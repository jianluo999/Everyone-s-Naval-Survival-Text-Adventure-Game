package com.adventure.repository;

import com.adventure.model.Choice;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChoiceRepository extends JpaRepository<Choice, Long> {
    
    /**
     * 根据故事ID查找选择
     */
    List<Choice> findByStoryId(String storyId);
    
    /**
     * 根据故事ID和是否可用查找选择
     */
    List<Choice> findByStoryIdAndIsAvailable(String storyId, Boolean isAvailable);
    
    /**
     * 根据下一个故事ID查找选择
     */
    List<Choice> findByNextStoryId(String nextStoryId);
} 