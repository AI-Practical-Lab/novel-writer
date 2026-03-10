# novel-chapter-write

**版本**: 2.0  
**功能**: Step 4.4 - 正文生成

---

## 输入

```yaml
framework: object
characters: object
memory: object
user_feedback: object        # 修改意见（如有）
```

---

## 输出

```yaml
status: "success"
content: string              # 完整章节正文
word_count: number
change_summary:
  plot_progress: {...}
  character_changes: {...}
  new_characters: [...]
  world_changes: [...]
  next_chapter_hints: [...]
```

---

## 写作约束

### 开篇钩子（前100字）
✓ 冲突/危机/秘密/反常
✗ 禁止环境描写、背景介绍

### 节奏控制
✓ 每300字小推进
✓ 每800字情绪转折
✓ 压抑≤1500字必须释放

### 爽点工程（60%-20%-20%）
- 铺垫期：建立期待、制造障碍、压抑情绪
- 爆发期：时机触发、反差呈现、瞬间碾压
- 余韵期：配角反应（≥3种）、环境变化、新钩子

### 语言风格
✓ 多用行为，少用形容词
✓ 少用比喻，直接呈现
✓ 短句为主，动词优先
✓ 展示而非讲述

### 脑洞约束（新增）
✓ 避免经典套路直接复制
✓ 金手指设计要有独特性
✓ 每章至少一个"没想到"元素

### 反套路检查（禁止）
✗ "三十年河东"式台词
✗ 戒指/玉佩里藏老爷爷
✗ 当众测试资质被打脸
✗ 未婚妻上门羞辱

### 结尾强制
✓ 新问题/危机/疑问
✗ 禁止圆满收尾
