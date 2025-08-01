# 使用示例

## 1. 上传小说文本

将你的小说txt文件放入 `novel_texts/raw/` 文件夹中。

例如：
```
novel_texts/raw/
├── 航海求生小说.txt
└── 或者分章节的文件
    ├── 第1章.txt
    ├── 第2章.txt
    └── ...
```

## 2. 分割大文件（如果需要）

如果你的小说是一个大文件，可以使用分割脚本：

```bash
cd novel_texts/scripts
python text_splitter.py
```

这会将大文件按章节分割成小文件。

## 3. 转换为游戏格式

使用转换脚本将小说转换为游戏剧情：

```bash
cd novel_texts/scripts
python novel_to_game.py
```

转换后的文件会保存在 `novel_texts/processed/` 文件夹中。

## 4. 手动调整

转换后的文件可能需要手动调整：

- 检查人称转换是否正确
- 调整选择分支的逻辑
- 添加属性影响和状态变化
- 优化场景分割

## 5. 集成到游戏

将处理好的剧情内容集成到游戏的后端数据中。

## 文件格式说明

### 输入格式（小说txt）
```
第1章 标题

段落内容...

段落内容...
```

### 输出格式（游戏md）
```markdown
# 第1章 标题

## 场景 1

**场景ID**: scene_1_1

你发现自己在一艘破旧的船上...

### 选择分支

1. 查看航海日志
2. 检查船舱
3. 观察海况

---
```

## 注意事项

1. 确保文本编码为UTF-8
2. 章节标题格式要规范
3. 转换后需要人工检查和调整
4. 选择分支需要根据剧情逻辑调整
