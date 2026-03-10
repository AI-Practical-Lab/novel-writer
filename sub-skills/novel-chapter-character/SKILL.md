# novel-chapter-character

**版本**: 2.0  
**功能**: Step 4.3 - 人物配置

---

## 输入

```yaml
framework: object            # 章纲中的人物需求
chapter_number: number
project_path: string
```

---

## 输出

```yaml
status: "success"
character_configs:
  existing:
    - name: string
      source: "existing"
      current_state: object
      offline_changes: string  # 间隔≥10章时生成
  new:
    - name: string
      source: "created"
      profile: object
      archive_decision: "yes" | "no"
```

---

## 离线角色更新规则

```
间隔 < 10章：保持原样
间隔 ≥ 10章：按需生成变化

变化类型：
A. 保持原样
B. 小幅进展
C. 重大突破
D. 遭遇变故

选择依据：剧情需要 > 角色目标 > 随机合理
```
