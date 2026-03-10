# novel-brainstorm

**版本**: 2.0  
**功能**: Step 1 & 3 - 需求澄清与头脑风暴（交互式）

---

## 核心设计原则

**不直接面对用户**，所有交互通过主 Skill (orchestrator) 中转。

```
用户 ←→ 主Skill ←→ novel-brainstorm
              ↑
        负责展示问题和收集答案
```

---

## 输入接口

```yaml
mode: "generate_question" | "process_answer" | "finalize"

# mode = generate_question
context:
  project_path: string
  current_confirmed: object      # 已确认的大纲要素
  pending_dimensions: array      # 待讨论的维度列表
  last_answer: null              # 无用户回答

# mode = process_answer  
context:
  project_path: string
  current_confirmed: object
  pending_dimensions: array
  last_answer:                   # 用户的回答
    question_id: string
    answer_text: string
    selected_option: string      # 如适用

# mode = finalize
context:
  project_path: string
  current_confirmed: object      # 全部确认完成
```

---

## 输出接口

```yaml
# action = ask_user （需要继续交互）
status: "in_progress"
action: "ask_user"
question:
  id: string                     # 问题唯一标识
  dimension: string              # 所属维度
  text: string                   # 问题文本
  description: string            # 为什么问这个问题
  options:                       # 选项（如适用）
    - id: "A"
      text: "选项A描述"
    - id: "B" 
      text: "选项B描述"
    - id: "C"
      text: "其他：___"
  allow_free_input: boolean      # 是否允许自由输入
  
confirmed_update: object         # 本次新增/更新的确认内容
next_dimension: string           # 建议下一个维度
progress:                        # 进度
  current: number
  total: number

---

# action = continue （自动继续，无需用户输入）
status: "in_progress"
action: "continue"
message: string                  # 说明为什么要继续
confirmed_update: object
next_dimension: string

---

# action = complete （全部完成）
status: "completed"
action: "complete"
confirmed_elements: object       # 完整的六维度大纲要素
file_updates:
  - path: "memory/brainstorm-result.yaml"
    content: "..."
next_step: "proceed_to_setup" | "proceed_to_outline"
```

---

## 六维度清单

| 序号 | 维度 | 关键问题 |
|:---:|------|---------|
| 1 | protagonist_arc | 主角起点、终点、关键转折 |
| 2 | conflicts | 内在冲突、外在阻力 |
| 3 | key_events | 核心事件、爽点设计 |
| 4 | relationships | 重要关系演变 |
| 5 | milestones | 能力/地位节点 |
| 6 | plot_hooks | 伏笔埋设与回收 |

---

## 交互流程示例

### Round 1: 生成第一个问题

**输入**:
```yaml
mode: "generate_question"
current_confirmed: {}
pending_dimensions: ["protagonist_arc", "conflicts", ...]
```

**输出**:
```yaml
status: "in_progress"
action: "ask_user"
question:
  id: "q1_protagonist_start"
  dimension: "protagonist_arc"
  text: "主角开场是什么状态？"
  description: "这决定了故事的起点和读者的代入感"
  options:
    - id: "A"
      text: "已经很惨（被退婚、被废、被追杀）"
    - id: "B"
      text: "一般惨（家境普通，怀才不遇）"
    - id: "C"
      text: "看似光鲜（实际有隐忧）"
  allow_free_input: true
confirmed_update: {}
next_dimension: "protagonist_arc"
progress:
  current: 1
  total: 6
```

### Round 2: 处理用户回答

**输入**:
```yaml
mode: "process_answer"
current_confirmed: {}
last_answer:
  question_id: "q1_protagonist_start"
  selected_option: "A"
  answer_text: "被退婚的废材少年"
```

**输出**:
```yaml
status: "in_progress"
action: "ask_user"
question:
  id: "q2_protagonist_end"
  dimension: "protagonist_arc"
  text: "那结尾你想让他变成什么样？"
  options:
    - id: "A"
      text: "站在世界巅峰"
    - id: "B"
      text: "找到真爱归隐"
    - id: "C"
      text: "复仇成功但失去一切"
confirmed_update:
  protagonist_arc:
    start: "被退婚的废材少年"
next_dimension: "protagonist_arc"
progress:
  current: 1
  total: 6
```

### Final Round: 完成

**输入**:
```yaml
mode: "finalize"
current_confirmed:
  protagonist_arc: {...}
  conflicts: {...}
  ...
```

**输出**:
```yaml
status: "completed"
action: "complete"
confirmed_elements:
  protagonist_arc: {...}
  conflicts: {...}
  key_events: {...}
  relationships: {...}
  milestones: {...}
  plot_hooks: {...}
file_updates:
  - path: "memory/brainstorm-result.yaml"
    content: "..."
next_step: "proceed_to_setup"
```

---

## 使用方式

由主 Skill (novel-writer) 调用：

```javascript
// 第一轮
const result = await callSubSkill('novel-brainstorm', {
  mode: 'generate_question',
  context: { current_confirmed: {}, pending_dimensions: [...] }
});

// 展示给用户，收集回答
const userAnswer = await presentToUser(result.question);

// 下一轮
const result2 = await callSubSkill('novel-brainstorm', {
  mode: 'process_answer',
  context: {
    current_confirmed: result.confirmed_update,
    last_answer: userAnswer
  }
});

// 循环直到 result.action === 'complete'
```

---

## 注意事项

1. **每轮只问1-2个问题**，不轰炸用户
2. **提供选项+开放输入**，降低决策成本
3. **解释为什么问**，让用户理解价值
4. **显示进度**，让用户知道还有多久
5. **允许回退**，用户可以修改之前的答案
