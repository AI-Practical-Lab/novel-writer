# novel-chapter-frame

**版本**: 2.0  
**功能**: Step 4.2 - 章纲构思

---

## 输入

```yaml
chapter_number: number
previous_chapter_summary: string
memory_context: object
outline_requirement: string
```

---

## 输出

```yaml
status: "success"
framework:
  chapter: number
  type: "setup" | "climax" | "aftermath" | "transition"
  goal:
    narrative: string
    emotion: string
    word_count: 3000
  structure:
    setup: [beat1, beat2, ...]      # 60%
    climax: [beat1, beat2]          # 20%
    aftermath: [beat1, beat2]       # 20%
  characters:
    required: [name1, name2]
    optional: [name3]
    new: [{name, role, importance}]
  hooks:
    resolve: [hook_id]
    plant: [{description, importance}]
    remind: [hook_id]
```

---

## 约束检查

- 铺垫 ≤ 60%
- 爆发 ≥ 20%
- 余韵 ≥ 20%
- 不满足则重新生成
