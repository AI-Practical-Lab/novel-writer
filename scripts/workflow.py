#!/usr/bin/env python3
"""
novel-writer 工作流控制脚本 - 确保每个环节都有验证
使用：python3 workflow.py <命令> [参数]
"""

import argparse
import sys
import subprocess
from pathlib import Path

def run_validation(script_name, *args):
    """运行验证脚本"""
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"❌ 错误：验证脚本不存在 {script_name}")
        return False
    
    cmd = ['python3', str(script_path)] + list(args)
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def cmd_create_outline(args):
    """创建章纲后的验证流程"""
    print("\n📋 Step 6.1: 创建章纲\n")
    
    # 验证章纲格式
    if not run_validation('validate_chapter_outline.py', args.book_name, args.chapter):
        print("\n❌ 章纲格式验证失败")
        return False
    
    print("\n✅ 章纲创建完成")
    print(f"\n下一步：")
    print(f"1. 请审阅章纲：memory/chapter_{args.chapter}_outline.md")
    print(f"2. 确认后，更新 status.md 为'第X卷第Y章 - 章纲已确认'")
    print(f"3. 运行：python3 workflow.py confirm-outline {args.book_name} {args.chapter}")
    return True

def cmd_confirm_outline(args):
    """确认章纲后的验证流程"""
    print("\n✅ Step 6.1 完成: 章纲已确认\n")
    
    # 验证章纲确认状态
    if not run_validation('validate_outline_confirmation.py', args.book_name, args.chapter):
        print("\n❌ 章纲未确认，无法进入写作阶段")
        return False
    
    print("\n✅ 章纲确认验证通过")
    print(f"\n下一步：")
    print(f"运行：python3 workflow.py write {args.book_name} {args.chapter}")
    return True

def cmd_write(args):
    """写作前的验证流程"""
    print("\n✍️  Step 6.2: 章节写作\n")
    
    # 必须验证章纲已确认
    if not run_validation('validate_outline_confirmation.py', args.book_name, args.chapter):
        print("\n❌ 阻断：章纲未确认，不能开始写作")
        print("请先完成：")
        print(f"1. 创建章纲：python3 workflow.py create-outline {args.book_name} {args.chapter}")
        print(f"2. 用户确认后：python3 workflow.py confirm-outline {args.book_name} {args.chapter}")
        return False
    
    print("\n✅ 写作前验证通过，可以开始写作")
    return True

def cmd_after_write(args):
    """写作完成后的验证流程"""
    print("\n📝 Step 6.2 完成: 章节写作\n")
    
    # 验证章节
    if not run_validation('validate_step.py', '--step', '6', '--book-name', args.book_name, '--chapter', args.chapter):
        print("\n⚠️  章节验证有警告，建议检查")
    
    print("\n下一步：")
    print(f"运行：python3 workflow.py character-check {args.book_name} {args.chapter}")
    return True

def cmd_character_check(args):
    """角色检查流程"""
    print("\n🎭 Step 6.3: 角色检查\n")
    
    if not run_validation('character_check.py', args.book_name, args.chapter):
        print("\n⚠️  角色检查未完成")
        return False
    
    print("\n✅ 角色检查完成")
    print("\n下一步：")
    print("等待用户审阅章节")
    print("满意 → 进入下一章")
    print("修改 → 重新写作")
    return True

def main():
    parser = argparse.ArgumentParser(description='novel-writer 工作流控制')
    parser.add_argument('command', choices=[
        'create-outline', 'confirm-outline', 'write', 
        'after-write', 'character-check'
    ], help='工作流命令')
    parser.add_argument('book_name', help='书名')
    parser.add_argument('chapter', help='章节号 (如 1_09)')
    
    args = parser.parse_args()
    
    commands = {
        'create-outline': cmd_create_outline,
        'confirm-outline': cmd_confirm_outline,
        'write': cmd_write,
        'after-write': cmd_after_write,
        'character-check': cmd_character_check,
    }
    
    result = commands[args.command](args)
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
