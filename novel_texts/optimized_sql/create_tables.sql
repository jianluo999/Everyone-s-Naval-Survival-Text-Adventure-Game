-- 数据库表结构创建脚本
-- 确保数据库表结构正确

-- 创建stories表
CREATE TABLE IF NOT EXISTS stories (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    story_id VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    chapter INT NOT NULL,
    scene INT NOT NULL,
    story_type VARCHAR(50) DEFAULT 'general',
    is_ending BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_story_id (story_id),
    INDEX idx_chapter (chapter),
    INDEX idx_story_type (story_type)
);

-- 创建choices表
CREATE TABLE IF NOT EXISTS choices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    story_id VARCHAR(50) NOT NULL,
    text VARCHAR(500) NOT NULL,
    next_story_id VARCHAR(50) NOT NULL,
    requirements VARCHAR(200) DEFAULT '',
    is_available BOOLEAN DEFAULT TRUE,
    health_cost INT DEFAULT 0,
    health_reward INT DEFAULT 0,
    gold_cost INT DEFAULT 0,
    gold_reward INT DEFAULT 0,
    experience_reward INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_story_id (story_id),
    INDEX idx_next_story_id (next_story_id),
    FOREIGN KEY (story_id) REFERENCES stories(story_id) ON DELETE CASCADE
);

