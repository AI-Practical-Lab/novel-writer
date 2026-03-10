# novel-setup

**版本**: 2.0  
**功能**: Step 2 - 设定生成

---

## 输入

```yaml
brainstorm_result: object    # 头脑风暴确认的要素
project_path: string
```

---

## 输出

```yaml
status: "success"
generated_files:
  essential:                 # 有内容
    - world-setting.md
    - protagonist.md
    - power-system.md       # 如适用，否则为political-system.md
  extension:                 # 框架先行
    - organizations.md
    - geography.md
    - artifacts.md
    - timeline.md
    - races.md
    - culture.md
user_prompt: |
  扩展设定框架已创建。以下哪些你已经想好了？
  
  □ 势力/组织分布
  □ 地图/关键地点
  □ 物品/道具系统
  □ 历史/时间线
  □ 种族/生物图鉴
  □ 文化/社会规则
  
  勾选的项我帮你填充内容，没勾选的保持'待补充'。
next_action: "wait_user_selection"
```

---

## 执行动作

1. 生成3类必备设定（基于brainstorm结果）
2. 创建6类扩展设定（框架+待补充标记）
3. 询问用户哪些需要立即填充

---

## 13类设定清单

### 必备（3类）
1. world-setting.md
2. protagonist.md
3. power-system.md / political-system.md

### 扩展（6类）
4. organizations.md
5. geography.md
6. artifacts.md
7. timeline.md
8. races.md
9. culture.md

### 动态（写作中维护）
10-13. 配角、伏笔、认知、章节摘要
