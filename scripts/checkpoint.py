#!/usr/bin/env python3
"""
novel-writer 检查点脚本 - 创建和回滚检查点
使用：
  python3 checkpoint.py create --book-name "书名" --name "checkpoint_name"
  python3 checkpoint.py rollback --book-name "书名" --name "checkpoint_name"
  python3 checkpoint.py list --book-name "书名"
"""

import argparse
import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

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

def get_checkpoint_dir(project_path):
    """获取检查点目录"""
    checkpoint_dir = project_path / "memory" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    return checkpoint_dir

def create_checkpoint(args):
    """创建检查点"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    checkpoint_name = args.name
    checkpoint_file = checkpoint_dir / f"{checkpoint_name}.checkpoint"
    
    # 收集项目状态
    checkpoint_data = {
        "name": checkpoint_name,
        "created_at": datetime.now().isoformat(),
        "book_name": args.book_name,
        "files": {}
    }
    
    # 要备份的关键文件
    key_files = [
        "status.md",
        "config/project_info.md",
        "config/worldbuilding.md",
        "config/characters.md",
        "config/volume_outline.md",
    ]
    
    # 动态查找章节文件
    chapters_dir = project_path / "chapters"
    if chapters_dir.exists():
        for chapter_file in sorted(chapters_dir.glob("vol*_chapter_*.md")):
            relative_path = chapter_file.relative_to(project_path)
            key_files.append(str(relative_path))
    
    # 读取并存储文件内容
    for file_path in key_files:
        full_path = project_path / file_path
        if full_path.exists():
            try:
                content = full_path.read_text(encoding='utf-8')
                checkpoint_data["files"][file_path] = content
                print(f"✓ 已备份：{file_path}")
            except Exception as e:
                print(f"⚠ 跳过 {file_path}: {e}")
    
    # 保存检查点
    checkpoint_file.write_text(json.dumps(checkpoint_data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n✅ 检查点已创建：{checkpoint_name}")
    print(f"   位置：{checkpoint_file}")
    print(f"   时间：{checkpoint_data['created_at']}")
    print(f"   文件数：{len(checkpoint_data['files'])}")
    
    return True

def rollback_checkpoint(args):
    """回滚到检查点"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    checkpoint_name = args.name
    checkpoint_file = checkpoint_dir / f"{checkpoint_name}.checkpoint"
    
    if not checkpoint_file.exists():
        print(f"❌ 错误：检查点 '{checkpoint_name}' 不存在")
        print(f"   可用检查点：")
        list_checkpoints(args)
        return False
    
    # 读取检查点数据
    checkpoint_data = json.loads(checkpoint_file.read_text(encoding='utf-8'))
    
    print(f"\n⚠️  即将回滚到检查点：{checkpoint_name}")
    print(f"   创建时间：{checkpoint_data['created_at']}")
    print(f"   这将覆盖当前项目的以下文件：")
    
    for file_path in checkpoint_data["files"].keys():
        print(f"     - {file_path}")
    
    if not args.force:
        print(f"\n确认回滚？输入 'yes' 继续：")
        confirmation = input().strip().lower()
        if confirmation != 'yes':
            print("已取消回滚")
            return False
    
    # 执行回滚
    restored_count = 0
    for file_path, content in checkpoint_data["files"].items():
        full_path = project_path / file_path
        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            print(f"✓ 已恢复：{file_path}")
            restored_count += 1
        except Exception as e:
            print(f"❌ 恢复失败 {file_path}: {e}")
    
    print(f"\n✅ 回滚完成，恢复了 {restored_count} 个文件")
    return True

def list_checkpoints(args):
    """列出所有检查点"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    
    checkpoints = sorted(checkpoint_dir.glob("*.checkpoint"))
    
    if not checkpoints:
        print(f"📭 没有找到检查点")
        return True
    
    print(f"\n📋 检查点列表 ({len(checkpoints)} 个)：\n")
    print(f"{'名称':<40} {'创建时间':<25} {'文件数':<10}")
    print("-" * 75)
    
    for cp_file in checkpoints:
        try:
            data = json.loads(cp_file.read_text(encoding='utf-8'))
            name = data.get('name', cp_file.stem)
            created = data.get('created_at', 'unknown')[:19]
            file_count = len(data.get('files', {}))
            print(f"{name:<40} {created:<25} {file_count:<10}")
        except Exception as e:
            print(f"{cp_file.stem:<40} {'读取失败':<25} {'?':<10}")
    
    return True

def delete_checkpoint(args):
    """删除检查点"""
    project_path = get_project_path(args.book_name)
    if not project_path:
        print(f"❌ 错误：找不到项目目录 '{args.book_name}'")
        return False
    
    checkpoint_dir = get_checkpoint_dir(project_path)
    checkpoint_file = checkpoint_dir / f"{args.name}.checkpoint"
    
    if not checkpoint_file.exists():
        print(f"❌ 错误：检查点 '{args.name}' 不存在")
        return False
    
    checkpoint_file.unlink()
    print(f"✅ 已删除检查点：{args.name}")
    return True

def main():
    parser = argparse.ArgumentParser(description='novel-writer 检查点管理脚本')
    parser.add_argument('action', choices=['create', 'rollback', 'list', 'delete'], 
                        help='操作类型')
    parser.add_argument('--book-name', type=str, required=True, help='书名')
    parser.add_argument('--name', type=str, help='检查点名称')
    parser.add_argument('--force', action='store_true', help='强制回滚，不询问确认')
    
    args = parser.parse_args()
    
    if args.action in ['create', 'rollback', 'delete'] and not args.name:
        parser.error(f"'{args.action}' 操作需要 --name 参数")
    
    actions = {
        'create': create_checkpoint,
        'rollback': rollback_checkpoint,
        'list': list_checkpoints,
        'delete': delete_checkpoint,
    }
    
    result = actions[args.action](args)
    
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
