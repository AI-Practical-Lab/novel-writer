#!/usr/bin/env python3
"""
验证章纲是否已确认
使用：python3 validate_outline_confirmation.py <书名> <章节号>
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

def main():
    if len(sys.argv) < 3:
        print("使用：python3 validate_outline_confirmation.py <书名> <章节号>")
        print("示例：python3 validate_outline_confirmation.py 沉默的忠诚 1_08")
        sys.exit(1)
    
    book_name = sys.argv[1]
    chapter = sys.argv[2]
    
    project_path = get_project_path(book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目 '{book_name}'")
        sys.exit(1)
    
    status_file = project_path / "status.md"
    if not status_file.exists():
        print(f"❌ 错误：status.md 不存在")
        sys.exit(1)
    
    content = status_file.read_text(encoding='utf-8')
    
    # 解析章节号
    chapter_parts = chapter.split('_')
    if len(chapter_parts) == 2:
        volume, chapter_num = chapter_parts
        # 尝试匹配多种格式
        patterns = [
            rf"第{volume}卷第{int(chapter_num)}章.*章纲已确认",
            rf"第{volume}卷.*第{int(chapter_num)}章.*已确认",
            rf"vol{volume}_chapter_{chapter_num}.*confirmed",
            rf"第{int(volume)}卷.*章纲已确认",
        ]
    else:
        patterns = [rf"第{chapter}章.*章纲已确认"]
    
    for pattern in patterns:
        if re.search(pattern, content):
            print(f"✅ 章纲已确认：第{chapter}章")
            sys.exit(0)
    
    print(f"❌ 章纲未确认：第{chapter}章")
    print(f"   请在 status.md 中添加确认标记，例如：")
    print(f"   '第1卷第8章 - 章纲已确认，等待写作'")
    sys.exit(1)

if __name__ == '__main__':
    main()
