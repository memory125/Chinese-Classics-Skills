#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易学习技能 - 测试运行器
运行所有测试并汇总结果
"""

import subprocess
import sys
import os

def run_test_file(test_file):
    """运行单个测试文件"""
    print(f"\n{'='*60}")
    print(f"运行：{test_file}")
    print('='*60)
    
    result = subprocess.run(
        ['python3', test_file],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=False
    )
    
    return result.returncode == 0

def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("  周易学习技能 - 完整测试套件")
    print("="*60)
    
    test_files = [
        'test_lunar_calendar.py',
        'test_core_functions.py'
    ]
    
    results = {}
    
    for test_file in test_files:
        test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_file)
        if os.path.exists(test_path):
            results[test_file] = run_test_file(test_file)
        else:
            print(f"\n⚠️  测试文件不存在：{test_file}")
            results[test_file] = False
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    print()
    print(f"总计：{total} 个测试文件")
    print(f"✅ 通过：{passed}")
    print(f"❌ 失败：{failed}")
    print("="*60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
