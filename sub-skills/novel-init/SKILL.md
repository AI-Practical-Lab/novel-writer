# novel-init

**版本**: 2.0  
**功能**: Step 0 - 项目初始化

---

## 输入

```yaml
project_name: string    # 项目名称（用户提供）
```

---

## 输出

```yaml
status: "success"
message: "项目已创建"
project_path: string
file_tree:
  - config/status.md
  - config/prompts.yaml
  - memory/world-setting.md
  - memory/protagonist.md
  - memory/power-system.md
  - memory/organizations.md
  - memory/geography.md
  - memory/artifacts.md
  - memory/timeline.md
  - memory/races.md
  - memory/culture.md
  - memory/outline.md
  - memory/plot-hooks.md
  - memory/cognitive-log.md
  - memory/chapter-summaries.md
  - memory/characters/core/
  - memory/characters/secondary/
  - memory/characters/archive/
  - chapters/
  - deliverables/
next_action: "proceed_to_brainstorm"
```

---

## 执行动作

1. 创建目录结构（根目录：`~/文稿/novel-projects/{project_name}`）
2. 生成初始 status.md
3. 生成 prompts.yaml（提示词配置）
4. 返回成功信息

---

## 注意事项

- **输出路径固定为 `~/文稿/novel-projects/`**
- 如果目录已存在，询问是否覆盖或另起名
- 项目名称支持中文
