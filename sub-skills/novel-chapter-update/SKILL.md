# novel-chapter-update

**版本**: 2.0  
**功能**: Step 4.7 - 记忆更新

---

## 输入

```yaml
chapter_number: number
chapter_content: string
change_summary: object
project_path: string
```

---

## 输出

```yaml
status: "success"
updated_files:
  - chapters/chapter-{N}.md
  - memory/protagonist.md
  - memory/characters/{name}.md
  - memory/plot-hooks.md
  - memory/cognitive-log.md
  - memory/chapter-summaries.md
  - config/status.md
```

---

## 更新顺序

1. 保存章节正文
2. 更新主角档案
3. 更新/创建配角档案
4. 更新伏笔追踪表
5. 追加认知日志
6. 添加章节摘要
7. 更新项目状态

所有更新原子化，失败可回滚。
