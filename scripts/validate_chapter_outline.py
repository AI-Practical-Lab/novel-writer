#!/usr/bin/env python3
"""
验证章纲格式是否符合规范
使用：python3 validate_chapter_outline.py <书名> <章节号>
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

def validate_outline(outline_content):
    """验证章纲内容"""
    errors = []
    warnings = []
    
    # 检查必需字段
    required_fields = {
        '时间': r'时间[：:]',
        '权重': r'权重[：:]',
        '危机来源': r'危机来源[：:]',
        '核心冲突': r'核心冲突[：:]',
        '主角抉择': r'主角抉择[：:]',
        '埋下隐患': r'埋下隐患[：:]',
        '接下一章': r'接下一章[：:]',
    }
    
    for field_name, pattern in required_fields.items():
        if not re.search(pattern, outline_content):
            errors.append(f"缺少必需字段：{field_name}")
    
    # 检查字数
    if len(outline_content) < 300:
        errors.append(f"章纲字数不足（{len(outline_content)} < 300）")
    elif len(outline_content) < 500:
        warnings.append(f"章纲字数偏少（{len(outline_content)} < 500）")
    
    # 检查是否有场景设计
    if '场景' not in outline_content:
        warnings.append("建议添加场景设计")
    
    # 检查权重标记
    weight_pattern = r'[⭐★]|[1-5]星'
    if not re.search(weight_pattern, outline_content):
        warnings.append("建议添加权重标记（⭐-⭐⭐⭐⭐⭐）")
    
    return errors, warnings

def main():
    if len(sys.argv) < 3:
        print("使用：python3 validate_chapter_outline.py <书名> <章节号>")
        print("示例：python3 validate_chapter_outline.py 沉默的忠诚 1_09")
        sys.exit(1)
    
    book_name = sys.argv[1]
    chapter = sys.argv[2]
    
    project_path = get_project_path(book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目 '{book_name}'")
        sys.exit(1)
    
    # 解析章节号
    chapter_parts = chapter.split('_')
    if len(chapter_parts) != 2:
        print(f"❌ 错误：章节号格式应为 'X_Y' (如 1_01)")
        sys.exit(1)
    
    volume, chapter_num = chapter_parts
    outline_file = project_path / "memory" / f"chapter_{volume}_{chapter_num}_outline.md"
    
    if not outline_file.exists():
        print(f"❌ 错误：章纲文件不存在 {outline_file.name}")
        sys.exit(1)
    
    print(f"\n🔍 验证章纲：{book_name} 第{chapter}章\n")
    
    outline_content = outline_file.read_text(encoding='utf-8')
    errors, warnings = validate_outline(outline_content)
    
    if errors:
        print("❌ 错误：")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("⚠️  警告：")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✅ 章纲格式正确")
        sys.exit(0)
    elif not errors:
        print("\n✅ 章纲基本正确（有警告但不影响继续）")
        sys.exit(0)
    else:
        print("\n❌ 章纲验证失败，请修正后重试")
        sys.exit(1)

if __name__ == '__main__':
    main()
