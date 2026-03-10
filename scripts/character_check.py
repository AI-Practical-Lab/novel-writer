#!/usr/bin/env python3
"""
novel-writer 角色检查脚本 - 每章完成后强制执行
使用：python3 character_check.py <书名> <章节号>
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

def extract_characters_from_chapter(chapter_content):
    """从章节内容中提取人物"""
    characters = set()
    
    # 匹配中文人名（2-4个汉字，常见姓氏开头）
    common_surnames = r'[丙刘胡郭张王李赵钱孙周吴郑冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍万柯卢莫经房裘缪干解应宗丁宣邓郁单杭洪包诸左石崔吉钮龚]'
    
    # 查找可能的人名（姓+名）
    pattern = rf'{common_surnames}[\u4e00-\u9fa5]{{1,3}}(?:[\u4e00-\u9fa5])?'
    matches = re.findall(pattern, chapter_content)
    
    for match in matches:
        # 过滤掉常见的非人名词
        non_names = ['大人', '大夫', '小子', '小的', '陛下', '什么', '怎么', '这个', '那个', '没有', '知道', '不能', '可以']
        if match not in non_names and len(match) >= 2:
            characters.add(match)
    
    return sorted(characters)

def load_character_cards(project_path):
    """加载现有角色卡"""
    cards_file = project_path / "memory" / "character_cards.md"
    if not cards_file.exists():
        return {}
    
    content = cards_file.read_text(encoding='utf-8')
    cards = {}
    
    # 解析YAML格式的角色卡
    current_role = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- id:'):
            current_role = line.replace('- id:', '').strip()
            cards[current_role] = {}
        elif current_role and ':' in line:
            key, value = line.split(':', 1)
            cards[current_role][key.strip()] = value.strip()
    
    return cards

def check_character_importance(character, project_path, current_volume, current_chapter):
    """检查角色在后续章节的重要性"""
    outline_file = project_path / "config" / f"volume_{current_volume}_chapter_outline.md"
    if not outline_file.exists():
        outline_file = project_path / "config" / "volume_1_chapter_outline.md"
    
    if not outline_file.exists():
        return False, 0
    
    content = outline_file.read_text(encoding='utf-8')
    
    # 统计角色在大纲中出现的次数
    count = len(re.findall(re.escape(character), content))
    
    # 如果出现2次以上，认为是重要角色
    is_important = count >= 2
    
    return is_important, count

def main():
    if len(sys.argv) < 3:
        print("使用：python3 character_check.py <书名> <章节号>")
        print("示例：python3 character_check.py 沉默的忠诚 1_08")
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
    chapter_file = project_path / "chapters" / f"vol{volume}_chapter_{chapter_num}.md"
    
    if not chapter_file.exists():
        print(f"❌ 错误：章节文件不存在 {chapter_file.name}")
        sys.exit(1)
    
    print(f"\n🔍 角色检查：{book_name} 第{chapter}章\n")
    
    # 读取章节内容
    chapter_content = chapter_file.read_text(encoding='utf-8')
    
    # 提取人物
    characters = extract_characters_from_chapter(chapter_content)
    print(f"📖 本章出场人物 ({len(characters)} 个)：")
    for char in characters[:20]:  # 只显示前20个
        print(f"  - {char}")
    if len(characters) > 20:
        print(f"  ... 还有 {len(characters) - 20} 个")
    
    # 加载现有角色卡
    existing_cards = load_character_cards(project_path)
    print(f"\n🎭 已有角色卡 ({len(existing_cards)} 个)")
    
    # 检查哪些人物没有角色卡
    new_characters = []
    for char in characters:
        char_id = char.lower().replace(' ', '_')
        if char_id not in existing_cards and char not in ['大人', '大夫', '小子', '小的']:
            new_characters.append(char)
    
    if new_characters:
        print(f"\n⚠️  新出场人物 ({len(new_characters)} 个，无角色卡)：")
        for char in new_characters:
            # 检查重要性
            is_important, count = check_character_importance(char, project_path, volume, chapter_num)
            if is_important:
                print(f"  🔴 {char} (重要角色，在后续大纲中出现 {count} 次)")
            else:
                print(f"  🟡 {char} (工具人，建议可选创建)")
    else:
        print("\n✅ 所有人物都有角色卡")
    
    # 更新关系图（如果有新人物）
    relationship_file = project_path / "memory" / "relationship_map.md"
    if relationship_file.exists():
        print(f"\n✓ 关系图存在：{relationship_file.name}")
    else:
        print(f"\n⚠️  关系图不存在，建议创建")
    
    print("\n📋 建议操作：")
    if new_characters:
        print("1. 为重要角色创建角色卡（memory/character_cards.md）")
        print("2. 更新人物关系图（memory/relationship_map.md）")
    else:
        print("无需更新角色信息")
    
    print("\n✅ 角色检查完成")

if __name__ == '__main__':
    main()
