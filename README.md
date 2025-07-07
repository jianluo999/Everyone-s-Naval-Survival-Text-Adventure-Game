# 项目介绍：互动叙事游戏引擎

本项目是一个功能强大的互动叙事游戏开发框架，旨在将传统的小说文本自动化地处理、分析、优化，并最终呈现为一个可玩的网页游戏。项目整合了前端、后端、数据处理脚本和AI美术生成工具，构成了一个完整的生产管线。

## 核心功能

- **自动化数据处理**：通过Python脚本将分章节的纯文本文稿解析成结构化的游戏数据。
- **叙事流分析与优化**：对故事的分支选项进行深度分析，识别并修复死胡同（dead ends），优化玩家体验。
- **前后端分离架构**：
    - **前端**：使用Vue.js构建的现代化、响应式的游戏界面。
    - **后端**：使用Java (Maven) 构建的稳定API服务器，为游戏提供数据支持。
- **批量数据导入**：提供多种脚本（Python, SQL, Java）将处理好的游戏数据高效导入数据库。
- **AI美术资产整合**：内置Stable Diffusion WebUI，表明项目工作流中包含了使用AI生成游戏场景、角色或物品插图的环节。

## 技术栈

- **前端 (Frontend)**:
    - [Vue.js](https://vuejs.org/)
    - [Vite](https://vitejs.dev/)
    - JavaScript, HTML, CSS
- **后端 (Backend)**:
    - [Java](https://www.java.com/)
    - [Maven](https://maven.apache.org/)
- **数据处理与脚本 (Data Processing & Scripting)**:
    - [Python](https.python.org/)
    - SQL
- **美术资产 (Art Assets)**:
    - [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

## 项目结构

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

## 工作流程

1.  **内容创作**: 将小说的每一章节编写为`.txt`文件，并存放在 `novel_texts/chapters/` 目录下。
2.  **数据解析与转换**:
    - 运行 `split_chapters.py` 等脚本，将文本文件解析为包含场景、对话和选项的基本数据结构。
    - `extract_valid_choices.py` 等脚本会进一步处理这些数据，提取有效的游戏逻辑。
3.  **故事流分析与优化**:
    - `choice_branch_analyzer.py` 和 `story_flow_optimizer.py` 等分析工具会检查整个故事网络，查找逻辑断点或死胡同。
    - `smart_choice_fixer.py` 可能会基于预设规则自动修复一些常见问题。
    - 分析和优化的结果会保存在 `novel_texts/` 目录下的JSON文件（如 `optimized_story_flow.json`）和报告（`.md`文件）中。
4.  **数据导入**:
    - `generate_optimized_sql.py` 将优��后的JSON数据转换为高效的SQL插入语句。
    - 通过 `batch_import_to_db.py` 或 `DataImporter.java` 等工具，将这些SQL脚本或数据文件批量导入到后端的数据库中。
5.  **游戏运行**:
    - 启动 `backend` Java服务器。
    - 启动 `frontend` Vue应用。
    - 玩家通过浏览器访问前端页面，开始游戏。前端向后端请求数据，后端从数据库中读取并返回，驱动游戏进行。
6.  **美术资产生成**: 在开发过程中，使用 `stable-diffusion-webui` 根据场景描述生成相应的图片，并整合到前端项目中。
