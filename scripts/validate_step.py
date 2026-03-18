#!/usr/bin/env python3
"""
novel-writer 验证脚本 - 强制验证每一步的产出
使用：python3 validate_step.py --step <N> --book-name "书名" [--chapter X_Y]
"""

import argparse
import os
import sys
import re
from pathlib import Path

def get_project_path(book_name):
    """获取项目路径"""
    # 优先检查 workspace，然后是 Documents
    paths = [
        Path.home() / ".openclaw" / "workspace" / "content-projects" / book_name,
        Path.home() / "Documents" / book_name,
    ]
    for path in paths:
        if path.exists():
            return path
    return None

def validate_step_0(args):
    """验证 Step 0: init"""
    print("✓ Step 0: 初始化阶段无需验证")
    return True

def validate_step_1(args):
    """验证 Step 1: brainstorm - 五个要素已确认"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    status_file = project_path / "status.md"
    if not status_file.exists():
        print(f"❌ 错误：status.md 不存在")
        return False
    
    content = status_file.read_text(encoding='utf-8')
    
    checks = [
        ("书名已确认", r"书名已确认"),
        ("篇幅已确认", r"篇幅已确认"),
        ("视角已确认", r"视角已确认"),
        ("范围已确认", r"范围已确认"),
        ("基调已确认", r"基调已确认"),
    ]
    
    all_passed = True
    for name, pattern in checks:
        if re.search(pattern, content):
            print(f"✓ {name}")
        else:
            print(f"❌ {name} - 未找到确认标记")
            all_passed = False
    
    return all_passed

def validate_step_2(args):
    """验证 Step 2: project_init - 目录结构"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    required_dirs = ['config', 'memory', 'chapters', 'deliverables']
    required_files = ['config/project_info.md']
    
    all_passed = True
    
    # 检查目录
    for dir_name in required_dirs:
        dir_path = project_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"✓ 目录存在：{dir_name}/")
        else:
            print(f"❌ 目录缺失：{dir_name}/")
            all_passed = False
    
    # 检查文件
    for file_path in required_files:
        full_path = project_path / file_path
        if full_path.exists() and full_path.stat().st_size > 0:
            print(f"✓ 文件存在且非空：{file_path}")
        else:
            print(f"❌ 文件缺失或为空：{file_path}")
            all_passed = False
    
    return all_passed

def validate_step_3(args):
    """验证 Step 3: world_building - 世界观和人物"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    required_files = [
        ('config/worldbuilding.md', 500),
        ('config/characters.md', 500),
        ('memory/character_cards.md', 100),
        ('memory/relationship_map.md', 100),
    ]
    
    all_passed = True
    
    for file_path, min_size in required_files:
        full_path = project_path / file_path
        if not full_path.exists():
            print(f"❌ 文件缺失：{file_path}")
            all_passed = False
            continue
        
        size = full_path.stat().st_size
        if size >= min_size:
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} 内容不足 ({size} < {min_size} bytes)")
            all_passed = False
    
    # 检查角色卡 YAML 结构
    character_cards = project_path / "memory" / "character_cards.md"
    if character_cards.exists():
        content = character_cards.read_text(encoding='utf-8')
        # 统计 id: 出现的次数（YAML 角色定义）
        role_count = len(re.findall(r'^\s*-?\s*id\s*:', content, re.MULTILINE))
        if role_count >= 3:
            print(f"✓ 角色卡包含至少3个角色 ({role_count}个)")
        else:
            print(f"❌ 角色卡角色数量不足 ({role_count} < 3)")
            all_passed = False
    
    return all_passed

def validate_step_4(args):
    """验证 Step 4: volume_outline - 卷纲设计"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    outline_file = project_path / "config" / "volume_outline.md"
    if not outline_file.exists():
        print(f"❌ 文件缺失：config/volume_outline.md")
        return False
    
    content = outline_file.read_text(encoding='utf-8')
    
    # 检查是否包含至少3卷
    volume_count = len(re.findall(r'第[一二三四]卷|Volume \d|## 第[1234]卷', content))
    if volume_count >= 3:
        print(f"✓ 卷纲包含至少3卷规划 ({volume_count}卷)")
    else:
        print(f"❌ 卷纲卷数不足 ({volume_count} < 3)")
        return False
    
    # 检查用户确认
    status_file = project_path / "status.md"
    if status_file.exists():
        status_content = status_file.read_text(encoding='utf-8')
        if "卷纲已确认" in status_content or "volume_outline confirmed" in status_content.lower():
            print("✓ 用户已确认卷纲")
            return True
    
    print("⚠ 警告：未找到用户确认记录（建议确认后继续）")
    return True  # 警告但不阻断

def validate_step_5(args):
    """验证 Step 5: volume_chapter_outline - 整卷章节大纲"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    # 获取当前卷号
    status_file = project_path / "status.md"
    current_volume = 1
    if status_file.exists():
        content = status_file.read_text(encoding='utf-8')
        match = re.search(r'第(\d+)卷', content)
        if match:
            current_volume = int(match.group(1))
    
    outline_file = project_path / "config" / f"volume_{current_volume}_chapter_outline.md"
    if not outline_file.exists():
        # 尝试其他命名格式
        outline_file = project_path / "config" / "volume_1_chapter_outline.md"
    
    if not outline_file.exists():
        print(f"❌ 文件缺失：章节大纲文件")
        return False
    
    content = outline_file.read_text(encoding='utf-8')
    
    # 检查是否包含章节
    chapter_count = len(re.findall(r'第[\d一二三四五六七八九十]+章', content))
    if chapter_count >= 1:
        print(f"✓ 章节大纲包含 {chapter_count} 章")
    else:
        print(f"❌ 章节大纲未找到章节定义")
        return False
    
    return True

def validate_step_6(args):
    """验证 Step 6: chapter_loop - 单章写作"""
    if not args.chapter:
        print("❌ 错误：验证章节需要 --chapter 参数")
        return False
    
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    # 解析章节号 (如 "1_01" 表示第1卷第1章)
    chapter_parts = args.chapter.split('_')
    if len(chapter_parts) != 2:
        print(f"❌ 错误：章节号格式应为 'X_Y' (如 1_01)")
        return False
    
    volume, chapter_num = chapter_parts
    chapter_file = project_path / "chapters" / f"vol{volume}_chapter_{chapter_num}.md"
    
    if not chapter_file.exists():
        print(f"❌ 文件缺失：{chapter_file.name}")
        return False
    
    content = chapter_file.read_text(encoding='utf-8')
    byte_count = len(content.encode('utf-8'))
    
    # 计算中文字数（更准确的估算）
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', content))
    
    # 字数检查：要求3000-4000中文字
    if chinese_chars < 3000:
        print(f"❌ 字数不足：{chinese_chars} 字 (要求 3000-4000 字)")
        return False
    elif chinese_chars > 4000:
        print(f"⚠ 字数偏多：{chinese_chars} 字 (建议 3000-4000 字)")
    else:
        print(f"✓ 字数正常：{chinese_chars} 字")
    
    # 检查是否有开场钩子
    first_lines = '\n'.join(content.split('\n')[:10])
    hook_indicators = ['。', '？', '！', '"', '"', "'", '...', '——']
    has_hook = any(indicator in first_lines for indicator in hook_indicators)
    
    if has_hook:
        print("✓ 开场有标点符号/对话")
    else:
        print("⚠ 建议：开头添加更有吸引力的钩子")
    
    # 检查画面感描写
    sensory_words = ['看', '听', '闻', '摸', '感觉', '光线', '声音', '气味', '温度']
    has_sensory = any(word in content for word in sensory_words)
    
    if has_sensory:
        print("✓ 包含感官描写")
    else:
        print("⚠ 建议：增加感官细节描写")
    
    # 检查对话
    dialogue_count = len(re.findall(r'[""].*?[""]', content))
    if dialogue_count >= 3:
        print(f"✓ 包含对话 ({dialogue_count}处)")
    else:
        print(f"⚠ 对话较少 ({dialogue_count}处)，建议增加人物对话")
    
    return True

def validate_step_7(args):
    """验证 Step 7: final_assemble - 最终合稿"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    final_md = project_path / "deliverables" / "final.md"
    
    if not final_md.exists():
        print(f"❌ 文件缺失：deliverables/final.md")
        return False
    
    size = final_md.stat().st_size
    print(f"✓ 合稿文件存在 ({size} bytes)")
    
    # 检查是否包含所有章节
    content = final_md.read_text(encoding='utf-8')
    chapter_count = len(re.findall(r'第[\d一二三四五六七八九十]+章', content))
    print(f"✓ 合稿包含约 {chapter_count} 章")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='novel-writer 步骤验证脚本')
    parser.add_argument('--step', type=int, required=True, help='要验证的步骤 (0-7)')
    parser.add_argument('--book-name', type=str, required=True, help='书名')
    parser.add_argument('--chapter', type=str, help='章节号 (如 1_01)')
    parser.add_argument('--volume', type=int, help='卷号')
    
    args = parser.parse_args()
    
    validators = {
        0: validate_step_0,
        1: validate_step_1,
        2: validate_step_2,
        3: validate_step_3,
        4: validate_step_4,
        5: validate_step_5,
        6: validate_step_6,
        7: validate_step_7,
    }
    
    if args.step not in validators:
        print(f"❌ 错误：无效的步骤号 {args.step}")
        sys.exit(1)
    
    print(f"\n🔍 验证 Step {args.step}: {args.book_name}\n")
    
    result = validators[args.step](args)
    
    print()
    if result:
        print("✅ 验证通过")
        sys.exit(0)
    else:
        print("❌ 验证失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
