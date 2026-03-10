# novel-memory-load

**版本**: 2.0  
**功能**: 智能加载写作所需记忆

---

## 输入

```yaml
chapter_number: number
framework: object
project_path: string
```

---

## 输出

```yaml
status: "success"
memory:
  essential:
    - world_setting
    - protagonist
    - power_system
    - outline
  relevant:
    - active_hooks
    - previous_chapter
    - previous_summary
    - characters: [...]
  filtered: boolean
```

---

## 加载策略

1. 加载必载记忆
2. 读取活跃伏笔
3. 读取上一章
4. 根据framework加载出场人物
   - 检查离线时间
   - 间隔≥10章：生成变化
5. Token计数（≤8000）
6. 超限则按相关性截断
