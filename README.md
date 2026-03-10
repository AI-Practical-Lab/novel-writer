# ai-novel-skill| AI 小说创作引擎 v3.0

这是一个能实现**长篇小说从创意到完稿全流程自动化**的 Skill 项目。作者只需用自然语言告诉 AI 你想写什么故事，它就能帮你完成从**创意构思、世界观搭建、人物设定、章节大纲、逐章写作到最终合稿**的整套流程。

支持主流 AI 编辑器：Antigravity / Trae / Claude Code / Cursor。

![ai_novel](assets/ai_novel.png)

---

## 能做什么

| 功能        | 说明                                |
| --------- | --------------------------------- |
| **创意构思**  | 与 AI 讨论书名、篇幅、视角、情感基调等核心要素         |
| **世界观搭建** | 自动生成时代背景、核心场景、制度礼仪等设定文档           |
| **人物设定**  | 创建结构化角色卡（YAML格式）、人物关系图谱           |
| **卷纲设计**  | 设计三卷主题、核心冲突、情感弧线                  |
| **章节大纲**  | 为每卷生成所有章节的情节概述，遵循四大推进原则           |
| **逐章写作**  | 自动写作 2500-3500 字/章，确保画面感、代入感、冲突张力 |
| **角色检查**  | 每章完成后自动检查新角色，为重要角色创建角色卡           |
| **伏笔追踪**  | 自动记录已埋设伏笔，确保前后呼应                  |
| **经验进化**  | 记录用户修改意见，持续改进写作质量                 |
| **检查点机制** | 关键节点自动创建快照，支持随时回滚恢复               |
| **最终合稿**  | 合并所有章节生成 final.md 和 final.docx    |

---

## 做不到什么

- **不是全自动写作机器** -- 关键节点（章纲、卷纲）必须得到用户确认后才能继续
- **不能替代人工审校** -- 每章完成后需要用户审阅，根据反馈进行修改
- **不能保证出版质量** -- 生成内容需要人工润色才能达到出版标准
- **不支持多语言写作** -- 目前主要针对中文长篇小说优化
- **不能实时联网查资料** -- 世界观设定依赖 AI 已有知识，特定领域需用户提供资料

---

## 🚀 快速开始 (Quick Start)

### 1. 安装 Skill (Install)

**🤖 Antigravity / Gemini Code Assist:**
```bash
git clone https://github.com/AI-Practical-Lab/ai-novel-skill.git .agent/skills/ai-novel-skill
```

**🚀 Trae IDE:**
```bash
ai-novel-skillgit clone https://github.com/AI-Practical-Lab/ai-novel-skill.git .trae/skills/novel-writer
```

**🧠 Claude Code:**
```bash
git clone https://github.com/AI-Practical-Lab/ai-novel-skill.git .claude/skills/ai-novel-skill
```

**💻 Cursor / VSCode / 通用:**
```bash
git clone https://github.com/AI-Practical-Lab/ai-novel-skill.git skills/ai-novel-skill
```

### 2. 试试这样跟 AI 说

**开始一本新小说**
> "我想写一本小说"

**指定类型创作**
> "帮我写一本古代言情长篇小说，要感人一点的"

**继续之前的创作**
> "继续写《他养大了皇帝》"

**查看当前进度**
> "小说写到哪了？"

**回滚到检查点**
> "回滚到第3章完成时的状态"

**修改已写章节**
> "第5章节奏太慢，帮我重写"

---

## 📦 环境准备

### 项目输出路径

**路径规则**：`~/Documents/{书名}/`

- 目录名使用**纯中文字符**，与书名完全一致
- 示例：《他养大了皇帝》→ `~/Documents/他养大了皇帝/`

**目录结构**：
```
~/Documents/{书名}/
├── config/
│   ├── project_info.md        # 项目元信息
│   ├── worldbuilding.md       # 世界观设定
│   ├── characters.md          # 人物小传
│   └── volume_outline.md      # 卷纲
├── memory/
│   ├── character_cards.md     # 角色卡（YAML格式）
│   ├── relationship_map.md    # 人物关系图谱
│   ├── foreshadowing.md       # 伏笔追踪
│   ├── lessons_learned.md     # 创作经验积累
│   └── checkpoints/           # 检查点快照
├── chapters/
│   ├── vol1_chapter_01.md
│   ├── vol1_chapter_02.md
│   └── ...
├── deliverables/
│   ├── final.md               # 合并稿
│   └── final.docx             # 导出文档
└── status.md                  # 当前状态（唯一真相源）
```

---

## 📂 文件夹说明

- `SKILL.md`: 给 AI 看的完整说明书，包含状态机和强制验证规则
- `README.md`: 给用户看的本文档
- `scripts/`: 验证脚本和检查点管理脚本
  - `validate_step.py`: 强制验证脚本，每步必跑
  - `checkpoint.py`: 检查点创建和回滚
  - `workflow.py`: 工作流管理
- `sub-skills/`: 子技能目录
  - `novel-init/`: 项目初始化
  - `novel-brainstorm/`: 创意构思
  - `novel-setup/`: 项目设置
  - `novel-memory-load/`: 记忆加载
  - `novel-chapter-frame/`: 章节框架
  - `novel-chapter-write/`: 章节写作
  - `novel-chapter-character/`: 角色检查
  - `novel-chapter-update/`: 章节更新
  - `novel-check-quality/`: 质量检查

---

## ⚠️ 核心机制说明

### 强制验证机制
每一步完成后必须运行验证脚本，失败则阻断流程：
```bash
# 验证 Step 2（项目初始化）
python scripts/validate_step.py --step 2 --book-name "书名"

# 验证 Step 3（世界构建）
python scripts/validate_step.py --step 3 --book-name "书名"

# 验证章节写作
python scripts/validate_step.py --step 6 --chapter 1_01 --book-name "书名"
```

### 检查点机制
关键节点自动创建快照，支持随时回滚：
```bash
# 创建检查点
python scripts/checkpoint.py create --book-name "书名" --name "step_3_complete"

# 回滚到检查点
python scripts/checkpoint.py rollback --book-name "书名" --name "step_3_complete"
```

### 状态机流程
```
Step 0: init → Step 1: brainstorm → Step 2: project_init 
→ Step 3: world_building → Step 4: volume_outline 
→ Step 5: volume_chapter_outline → Step 6: chapter_loop 
→ Step 7: final_assemble
```

### 章节情节推进四大原则
1. **因果链原则**：每章危机必须从上一章隐患发展而来
2. **抉择+代价原则**：主角每章必须做出明确抉择，每个抉择都有代价
3. **升级递进原则**：危机必须层层升级，禁止同一级别危机重复出现
4. **节奏权重原则**：过渡/铺垫/高潮/结尾阶段用章节数量体现节奏

---

## ⚠️ 常见问题 (FAQ)

1. **如何查看当前写作进度？**
   查看 `~/Documents/{书名}/status.md` 文件，这是唯一真相源。

2. **如何修改已写的章节？**
   告诉 AI "帮我修改第X章"，AI 会根据你的反馈重写并记录到 `lessons_learned.md`。

3. **验证失败怎么办？**
   验证脚本会输出具体错误，根据提示修复后重新运行验证。

4. **可以跳过某个步骤吗？**
   不可以。强制验证机制确保每一步都完成才能进入下一步。

5. **如何恢复之前的创作？**
   告诉 AI "继续写《书名》"，AI 会自动读取 status.md 从断点继续。

6. **写了一半想回滚怎么办？**
   告诉 AI "回滚到XXX检查点"，AI 会恢复到该检查点状态。

---

## 🔄 如何更新 (Update)

当有新功能发布时，您可以输入以下命令一键更新：

```bash
cd .trae/skills/novel-writer
git pull
```

---

## 🌟 核心特性 (V3.0)

- **强制验证机制**：每一步必须通过验证脚本，确保流程完整性
- **检查点机制**：关键节点自动创建快照，支持随时回滚恢复
- **进化机制**：记录用户修改意见，持续改进写作质量
- **角色追踪**：自动检查新角色，维护人物关系图谱
- **伏笔管理**：自动记录已埋设伏笔，确保前后呼应
- **上下文感知**：写作时自动读取前文、角色卡、伏笔等信息
- **质量约束**：字数控制（2500-3500字/章）、画面感、代入感、冲突张力等八大写作原则

---

## 打赏支持

如果这个项目对你有帮助，欢迎打赏支持。你的支持会直接转化为继续开发和维护的动力。
![good](assets/good.jpg)