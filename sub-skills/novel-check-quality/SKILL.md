# novel-check-quality

**版本**: 2.0  
**功能**: 质量检查

---

## 输入

```yaml
chapter_content: string
chapter_number: number
framework: object
project_path: string
```

---

## 输出

```yaml
status: "success"
passed: boolean
warnings:
  - type: "consistency" | "structure" | "style"
    message: string
    severity: "low" | "medium" | "high"
errors:
  - type: string
    message: string
    severity: "critical"
details:
  word_count: number
  structure_ratio:
    setup: number
    climax: number
    aftermath: number
```

---

## 检查维度

| 维度 | 检查项 | 处理方式 |
|------|--------|---------|
| 一致性 | 设定冲突、人物OOC | 警告，不阻塞 |
| 结构 | 60-20-20比例 | 错误，需修正 |
| 风格 | 形容词过多 | 警告，不阻塞 |
| 完整性 | 必填元素缺失 | 错误，需修正 |

检查结果供参考，严重结构错误才阻塞流程。
