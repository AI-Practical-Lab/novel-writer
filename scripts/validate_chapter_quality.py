#!/usr/bin/env python3
"""
novel-writer 章节质量审查脚本 - 优秀网文10大标准
使用：python3 validate_chapter_quality.py <书名> <章节号>
"""

import sys
import re
from pathlib import Path

def get_project_path(book_name):
    """获取项目路径"""
    paths = [
        Path.home() / ".openclaw" / "workspace" / "content-projects" / book_name,
        Path.home() / "Documents" / book_name,
    ]
    for path in paths:
        if path.exists():
            return path
    return None

def load_chapter(project_path, chapter_code):
    """加载章节内容"""
    chapter_parts = chapter_code.split('_')
    if len(chapter_parts) != 2:
        return None
    volume, chapter_num = chapter_parts
    chapter_file = project_path / "chapters" / f"vol{volume}_chapter_{chapter_num}.md"
    if not chapter_file.exists():
        return None
    return chapter_file.read_text(encoding='utf-8')

def check_opening_hook(content):
    """标准1：开场抓人 - 前3段必须有强钩子"""
    lines = content.split('\n')
    first_3_paragraphs = '\n'.join([l for l in lines[:15] if l.strip()][:3])
    
    # 检查是否有悬念、冲突或情绪
    hook_patterns = [
        r'[？！]',
        r'["""].*?["""]',
        r'(死|杀|血|死|崩溃|绝望|惊喜|震惊)',
        r'(但是|然而|突然|没想到)',
    ]
    
    hook_score = 0
    for pattern in hook_patterns:
        if re.search(pattern, first_3_paragraphs):
            hook_score += 1
    
    return min(hook_score, 2)  # 满分2分

def check_pacing(content):
    """标准2：节奏紧凑 - 每3-5段一个小高潮"""
    paragraphs = [p for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
    
    # 检查高潮标记（冲突、转折、对话爆发）
    climax_markers = ['"', '"', '？', '！', '突然', '但是', '然后', '结果']
    
    climax_count = 0
    for i, para in enumerate(paragraphs):
        if any(marker in para for marker in climax_markers):
            climax_count += 1
    
    # 平均每5段应有1个高潮
    expected_climax = len(paragraphs) / 5
    ratio = climax_count / max(expected_climax, 1)
    
    return min(int(ratio * 2), 2)  # 满分2分

def check_conflict(content):
    """标准3：每章有冲突 - 至少2个冲突"""
    conflict_patterns = [
        r'(不服|不满|愤怒|怼|反驳|质问)',
        r'(拒绝|不同意|反对|抗争)',
        r'(矛盾|冲突|对立|斗争)',
        r'["""].*?(不|没|别|滚|操|他妈|傻逼|垃圾)["""]',
    ]
    
    conflict_count = 0
    for pattern in conflict_patterns:
        if re.search(pattern, content):
            conflict_count += 1
    
    return min(conflict_count, 2)  # 满分2分

def check_character_motivation(content):
    """标准4：人物有动机 - 主角和反派动机清晰"""
    motivation_markers = [
        r'(为了|因为|想|要|希望|期待|害怕|担心)',
        r'(凭什么|为什么|怎么回事)',
        r'(我不服|我不甘心|我要|我必须)',
    ]
    
    motivation_count = 0
    for marker in motivation_markers:
        if re.search(marker, content):
            motivation_count += 1
    
    return min(motivation_count, 2)  # 满分2分

def check_dialogue(content):
    """标准5：对话有戏 - 推动情节，有潜台词"""
    # 提取所有对话
    dialogues = re.findall(r'["""]([^"""]+)["""]', content)
    
    if len(dialogues) < 3:
        return 0
    
    # 检查对话是否有潜台词（简短、有冲突、有情绪）
    good_dialogue = 0
    for dialogue in dialogues:
        if len(dialogue) < 50 and ('你' in dialogue or '我' in dialogue):
            good_dialogue += 1
    
    ratio = good_dialogue / max(len(dialogues), 1)
    return min(int(ratio * 2), 2)  # 满分2分

def check_ending_hook(content):
    """标准6：结尾有钩子 - 必须为下一章留悬念"""
    last_lines = '\n'.join(content.split('\n')[-10:])
    
    hook_patterns = [
        r'[？！]',
        r'(但是|然而|突然|没想到|原来|竟然)',
        r'(等着|来了|响了|响了|震动)',
        r'(门|电话|手机|消息|声音)',
        r'[(（]第.*章.*完[)）]',
    ]
    
    hook_score = 0
    for pattern in hook_patterns:
        if re.search(pattern, last_lines):
            hook_score += 1
    
    return min(hook_score, 2)  # 满分2分

def check_information_density(content):
    """标准7：信息密度 - 每100字有新信息"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', content))
    
    # 检查新信息点（数字、名字、事件、转折）
    info_patterns = [
        r'\d+',
        r'[\u4e00-\u9fa5]{2,4}(?:公司|部门|项目|方案)',
        r'(但是|然而|突然|没想到|原来|竟然)',
        r'(发现|知道|意识到|明白)',
    ]
    
    info_count = 0
    for pattern in info_patterns:
        info_count += len(re.findall(pattern, content))
    
    # 平均每100字应有1个信息点
    expected_info = chinese_chars / 100
    ratio = info_count / max(expected_info, 1)
    
    return min(int(ratio * 2), 2)  # 满分2分

def check_imagery(content):
    """标准8：画面感 - 五感描写"""
    sensory_words = {
        '视觉': ['看', '见', '光', '色', '影', '闪', '亮', '暗', '白', '黑', '红'],
        '听觉': ['听', '声', '音', '响', '震', '嗡', '静', '吵', '铃'],
        '嗅觉': ['闻', '香', '臭', '味', '气', '熏'],
        '触觉': ['摸', '触', '感', '冷', '热', '凉', '暖', '抖', '颤'],
        '味觉': ['尝', '吃', '喝', '甜', '苦', '酸', '辣', '咸'],
    }
    
    sensory_count = 0
    for category, words in sensory_words.items():
        if any(word in content for word in words):
            sensory_count += 1
    
    return min(sensory_count, 2)  # 满分2分

def check_emotion(content):
    """标准9：情感真实 - 情感有层次"""
    emotion_words = [
        r'(期待|兴奋|高兴|笑)',
        r'(惊讶|震惊|愣|呆)',
        r'(愤怒|生气|怒|骂|操|他妈)',
        r'(难过|伤心|失望|绝望|苦)',
        r'(无奈|累|疲惫|无力|沉默)',
        r'(希望|想|决定|坚定)',
    ]
    
    emotion_count = 0
    for pattern in emotion_words:
        if re.search(pattern, content):
            emotion_count += 1
    
    return min(emotion_count, 2)  # 满分2分

def check_ai_flavor(content):
    """标准10：去AI味 - 自然流畅"""
    ai_patterns = [
        r'(从某种意义上说|从某种角度来看)',
        r'(值得注意的是|关键在于|核心在于)',
        r'(一方面.*另一方面|既.*又.*但是)',
        r'(此外|另外|同时|并且|因此|所以)',
        r'(最终|最后|结局是|结果是)',
        r'background music',  # 英文混入
    ]
    
    ai_count = 0
    for pattern in ai_patterns:
        if re.search(pattern, content):
            ai_count += 1
    
    # 分数越高越好，所以用 2 - ai_count
    return max(2 - ai_count, 0)  # 满分2分

def main():
    if len(sys.argv) < 3:
        print("用法：python3 validate_chapter_quality.py <书名> <章节号>")
        print("示例：python3 validate_chapter_quality.py 我的员工都是隐藏大佬 1_01")
        sys.exit(1)
    
    book_name = sys.argv[1]
    chapter_code = sys.argv[2]
    
    project_path = get_project_path(book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{book_name}'")
        sys.exit(1)
    
    content = load_chapter(project_path, chapter_code)
    if not content:
        print(f"❌ 错误：找不到章节文件 '{chapter_code}'")
        sys.exit(1)
    
    print(f"🔍 优秀网文10大标准审查：{book_name} 第{chapter_code}章")
    print("=" * 60)
    
    # 执行10项检查
    checks = [
        ("开场抓人", check_opening_hook, "前3段有悬念/冲突/情绪"),
        ("节奏紧凑", check_pacing, "每3-5段有小高潮"),
        ("每章有冲突", check_conflict, "至少2个冲突"),
        ("人物有动机", check_character_motivation, "主角和反派动机清晰"),
        ("对话有戏", check_dialogue, "对话推动情节，有潜台词"),
        ("结尾有钩子", check_ending_hook, "为下一章留悬念"),
        ("信息密度", check_information_density, "每100字有新信息"),
        ("画面感", check_imagery, "五感描写"),
        ("情感真实", check_emotion, "情感有层次"),
        ("去AI味", check_ai_flavor, "自然流畅，无AI痕迹"),
    ]
    
    total_score = 0
    max_score = 0
    
    for name, check_func, desc in checks:
        score = check_func(content)
        total_score += score
        max_score += 2
        
        status = "✓" if score >= 1 else "⚠"
        bar = "█" * score + "░" * (2 - score)
        
        print(f"{status} {name:12s} [{bar}] {score}/2 - {desc}")
    
    print("=" * 60)
    percentage = (total_score / max_score) * 100
    
    if percentage >= 80:
        level = "优秀"
        emoji = "🌟"
    elif percentage >= 60:
        level = "良好"
        emoji = "✅"
    elif percentage >= 40:
        level = "及格"
        emoji = "⚠️"
    else:
        level = "不及格"
        emoji = "❌"
    
    print(f"{emoji} 总分：{total_score}/{max_score} ({percentage:.1f}%) - {level}")
    
    if percentage < 80:
        print("\n💡 改进建议：")
        if check_opening_hook(content) < 2:
            print("  - 开场加强钩子，增加悬念或冲突")
        if check_pacing(content) < 2:
            print("  - 节奏加快，每3-5段设置一个小高潮")
        if check_conflict(content) < 2:
            print("  - 增加冲突，让主角主动反抗")
        if check_character_motivation(content) < 2:
            print("  - 明确人物动机，增加内心戏")
        if check_dialogue(content) < 2:
            print("  - 对话要有潜台词，推动情节")
        if check_ending_hook(content) < 2:
            print("  - 结尾加强钩子，留下悬念")
        if check_information_density(content) < 2:
            print("  - 增加信息密度，每100字有新信息")
        if check_imagery(content) < 2:
            print("  - 增加五感描写，增强画面感")
        if check_emotion(content) < 2:
            print("  - 情感要有层次，展现情绪变化")
        if check_ai_flavor(content) < 2:
            print("  - 去除AI痕迹，让语言更自然")
    
    print("\n✅ 审查完成")
    return 0 if percentage >= 60 else 1

if __name__ == "__main__":
    sys.exit(main())
