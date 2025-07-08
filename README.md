# Everyone's Naval Survival Text Adventure Game

[![GitHub stars](https://img.shields.io/github/stars/jianluo999/Everyone-s-Naval-Survival-Text-Adventure-Game.svg)](https://github.com/jianluo999/Everyone-s-Naval-Survival-Text-Adventure-Game/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/jianluo999/Everyone-s-Naval-Survival-Text-Adventure-Game.svg)](https://github.com/jianluo999/Everyone-s-Naval-Survival-Text-Adventure-Game/network)
[![GitHub issues](https://img.shields.io/github/issues/jianluo999/Everyone-s-Naval-Survival-Text-Adventure-Game.svg)](https://github.com/jianluo999/Everyone-s-Naval-Survival-Text-Adventure-Game/issues)

## 🌊 项目简介

欢迎来到危险的海上生存世界！这是一个功能强大的互动叙事游戏开发框架，专门为海上冒险生存题材设计。项目将传统的小说文本自动化地处理、分析、优化，并最终呈现为一个引人入胜的网页游戏。

**🚧 项目状态：开发中 (Work in Progress)**

本项目目前正在积极开发中，包含500+章节和数千个场景的庞大故事系统。我们正在不断完善游戏机制、优化用户体验，并添加更多精彩的故事内容。
![image](https://github.com/user-attachments/assets/291a29b8-955a-4d27-8f4b-2707f0554192)




## ⭐ 核心功能

### 🎮 游戏特色
- **沉浸式海上生存体验**：面对饥饿、干渴、海怪和无数危险
- **丰富的故事分支**：500+章节，数千个场景，每个选择都影响命运
- **第二人称叙事**：让您完全沉浸在冒险者的角色中
- **打字机效果**：文字逐字显示，营造紧张刺激的阅读体验
- **智能故事流**：所有分支最终汇聚，确保没有死胡同
![image](https://github.com/user-attachments/assets/6f5f0971-1d38-4211-b725-8568181e0436)

### 🛠️ 技术特色
- **自动化数据处理**：通过Python脚本将分章节的纯文本文稿解析成结构化的游戏数据
- **叙事流分析与优化**：对故事的分支选项进行深度分析，识别并修复死胡同，优化玩家体验
- **前后端分离架构**：
    - **前端**：使用Vue.js构建的现代化、响应式的游戏界面
    - **后端**：使用Java (Maven) 构建的稳定API服务器，为游戏提供数据支持
- **批量数据导入**：提供多种脚本（Python, SQL, Java）将处理好的游戏数据高效导入数据库
- **AI美术资产整合**：内置Stable Diffusion WebUI，支持AI生成游戏场景、角色插图

## 🛠️ 技术栈

- **前端 (Frontend)**:
    - [Vue.js](https://vuejs.org/)
    - [Vite](https://vitejs.dev/)
    - JavaScript, HTML, CSS
- **后端 (Backend)**:
    - [Java](https://www.java.com/)
    - [Maven](https://maven.apache.org/)
- **数据处理与脚本 (Data Processing & Scripting)**:
    - [Python](https://python.org/)
    - SQL
- **美术资产 (Art Assets)**:
    - [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

## 📁 项目结构

```
.
├── backend/            # Java后端Maven项目
├── frontend/           # Vue.js前端项目
├── novel_texts/        # 核心数据目录
│   ├── chapters/       # 存放原始小说章节的文本文件
│   ├── optimized_scenes/ # 存放优化后的场景数据
│   ├── optimized_sql/  # 存放优化后的SQL脚本
│   └── ...             # 其他处理后的JSON数据、报告和SQL批处理文件
├── stable-diffusion-webui/ # AI图片生成工具
├── *.py                # 根目录下的Python工具脚本
├── *.sql               # 根目录下的SQL导入脚本
└── README.md           # 本文档
```

- **`backend/`**: Java后端服务，负责提供API接口，与数据库交互，向前端输送游戏逻辑和内容。
- **`frontend/`**: 玩家直接交互的Web应用。通过调用后端API来获取故事场景、选项，并展示给玩家。
- **`novel_texts/`**: 项目的数据中枢。包含了从最原始的章节文本到经过多层处理和优化的结构化数据（如JSON文件）、SQL脚本以及分析报告。
- **根目录脚本 (`*.py`, `*.java`, `*.sql`)**: 一系列用于实现自动化工作流的独立工具。这些脚本负责解析、转换、分析和导入数据。
- **`stable-diffusion-webui/`**: 暗示了项目的美术资产（如图形、背景）可能是通过AI生成的，以匹配故事情节。

## 🔄 工作流程

1.  **内容创作**: 将小说的每一章节编写为`.txt`文件，并存放在 `novel_texts/chapters/` 目录下。
2.  **数据解析与转换**:
    - 运行 `split_chapters.py` 等脚本，将文本文件解析为包含场景、对话和选项的基本数据结构。
    - `extract_valid_choices.py` 等脚本会进一步处理这些数据，提取有效的游戏逻辑。
3.  **故事流分析与优化**:
    - `choice_branch_analyzer.py` 和 `story_flow_optimizer.py` 等分析工具会检查整个故事网络，查找逻辑断点或死胡同。
    - `smart_choice_fixer.py` 可能会基于预设规则自动修复一些常见问题。
    - 分析和优化的结果会保存在 `novel_texts/` 目录下的JSON文件（如 `optimized_story_flow.json`）和报告（`.md`文件）中。
4.  **数据导入**:
    - `generate_optimized_sql.py` 将优化后的JSON数据转换为高效的SQL插入语句。
    - 通过 `batch_import_to_db.py` 或 `DataImporter.java` 等工具，将这些SQL脚本或数据文件批量导入到后端的数据库中。
5.  **游戏运行**:
    - 启动 `backend` Java服务器。
    - 启动 `frontend` Vue应用。
    - 玩家通过浏览器访问前端页面，开始游戏。前端向后端请求数据，后端从数据库中读取并返回，驱动游戏进行。
6.  **美术资产生成**: 在开发过程中，使用 `stable-diffusion-webui` 根据场景描述生成相应的图片，并整合到前端项目中。

## 🚀 快速开始

### 环境要求
- **Java**: JDK 11 或更高版本
- **Node.js**: 16.0 或更高版本
- **Python**: 3.8 或更高版本
- **MySQL**: 8.0 或更高版本

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/jianluo999/Everyone-s-Naval-Survival-Text-Adventure-Game.git
   cd Everyone-s-Naval-Survival-Text-Adventure-Game
   ```

2. **设置数据库**
   - 创建MySQL数据库
   - 运行数据库初始化脚本

3. **启动后端服务**
   ```bash
   cd backend
   mvn clean install
   mvn spring-boot:run
   ```
   后端服务将在 `http://localhost:8080` 启动

4. **启动前端应用**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   前端应用将在 `http://localhost:5173` 启动

5. **开始游戏**
   在浏览器中访问前端地址，开始您的海上冒险之旅！

## 📖 使用说明

### 游戏玩法
- 阅读故事文本，做出选择
- 每个选择都会影响故事的发展方向
- 管理您的资源：食物、水、体力
- 面对各种挑战：天气、海怪、其他幸存者
- 寻找最终的生存之路

### 开发者指南
- 查看 `novel_texts/` 目录了解数据结构
- 使用Python脚本处理和优化故事数据
- 参考各种分析报告了解故事流优化

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📝 开发日志

- **当前版本**: 开发中
- **最新更新**: 正在完善故事分支和用户界面
- **下一步计划**: 
  - 完善所有章节内容
  - 优化游戏性能
  - 添加更多互动元素
  - 完善AI美术资产生成

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **jianluo999** - *项目创建者* - [GitHub](https://github.com/jianluo999)

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和测试者！

---

**⚠️ 注意**: 本项目仍在开发中，部分功能可能不完整或存在bug。我们正在努力完善所有功能，敬请期待正式版本的发布！
