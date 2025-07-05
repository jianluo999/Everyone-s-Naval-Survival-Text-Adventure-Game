package com.adventure;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.CrossOrigin;

@SpringBootApplication
@CrossOrigin(origins = "http://localhost:3000")
public class SailingGameApplication {
    public static void main(String[] args) {
        SpringApplication.run(SailingGameApplication.class, args);
        System.out.println("🚢 航海冒险游戏后端启动成功！");
    }
} 