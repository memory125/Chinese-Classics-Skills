#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
农历计算器单元测试 - 验证农历转换准确性
"""

import json
import subprocess
import sys
import os

# 添加 scripts 目录到路径
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/scripts'
sys.path.insert(0, SCRIPT_DIR)

# 星期映射（Python weekday: 0=周一）
WEEKDAY_MAP = {
    0: '周一', 1: '周二', 2: '周三', 3: '周四', 
    4: '周五', 5: '周六', 6: '周日'
}

def get_expected_weekday(date_str):
    """计算预期星期"""
    from datetime import date
    parts = date_str.split('-')
    d = date(int(parts[0]), int(parts[1]), int(parts[2]))
    return WEEKDAY_MAP[d.weekday()]

def run_lunar_calc(date_str):
    """运行农历计算器并返回结果（使用 --json 模式）"""
    result = subprocess.run(
        ['python3', 'get-lunar-ganzhi.py', '--date', date_str, '--json'],
        capture_output=True,
        text=True,
        cwd=SCRIPT_DIR,
        timeout=10
    )
    
    if result.returncode != 0:
        raise Exception(f"执行失败：{result.stderr}")
    
    return json.loads(result.stdout)

def test_2026_march_14():
    """测试 2026-03-14（惊蛰后第 9 天）"""
    output = run_lunar_calc("2026-03-14")
    
    assert 'gregorian' in output, "缺少 gregorian 字段"
    assert output['gregorian'] == "2026-03-14", f"日期不匹配：{output['gregorian']}"
    assert 'lunar' in output, "缺少 lunar 字段"
    assert 'ganzhi_year' in output, "缺少 ganzhi_year 字段"
    assert '丙午' in output['ganzhi_year'], f"年份干支错误：{output['ganzhi_year']}"
    
    expected_weekday = get_expected_weekday("2026-03-14")
    assert output['weekday'] == expected_weekday, f"星期错误：期望 {expected_weekday}, 得到 {output['weekday']}"
    
    print("✅ 2026-03-14 测试通过")
    print(f"   公历：{output['gregorian_cn']}")
    print(f"   农历：{output['lunar']}")
    print(f"   干支：{output['ganzhi_year']}")
    print()

def test_2025_march_15():
    """测试 2025-03-15（蛇年）"""
    output = run_lunar_calc("2025-03-15")
    
    assert '乙巳' in output['ganzhi_year'], f"年份干支错误：{output['ganzhi_year']}"
    
    expected_weekday = get_expected_weekday("2025-03-15")
    assert output['weekday'] == expected_weekday, f"星期错误：期望 {expected_weekday}, 得到 {output['weekday']}"
    
    print("✅ 2025-03-15 测试通过")
    print(f"   公历：{output['gregorian_cn']}")
    print(f"   农历：{output['lunar']}")
    print()

def test_2027_jan_1():
    """测试 2027-01-01（丁未年）"""
    output = run_lunar_calc("2027-01-01")
    
    assert '丁未' in output['ganzhi_year'], f"年份干支错误：{output['ganzhi_year']}"
    
    expected_weekday = get_expected_weekday("2027-01-01")
    assert output['weekday'] == expected_weekday, f"星期错误：期望 {expected_weekday}, 得到 {output['weekday']}"
    
    print("✅ 2027-01-01 测试通过")
    print(f"   公历：{output['gregorian_cn']}")
    print(f"   农历：{output['lunar']}")
    print()

def test_unsupported_year():
    """测试不支持的年份（2030 年，应该返回占位符或有效数据）"""
    output = run_lunar_calc("2030-01-01")
    
    # 2030 年可能返回占位符或有效数据，只要不报错即可
    assert 'gregorian' in output, "应该返回基本日期信息"
    assert output['gregorian'] == "2030-01-01", "日期应该正确返回"
    
    print("✅ 2030-01-01（未来年份）测试通过")
    print(f"   返回数据：{output['lunar']}")
    print()

def test_json_output_structure():
    """测试 JSON 输出结构完整性"""
    output = run_lunar_calc("2026-03-15")
    
    required_fields = ['gregorian', 'gregorian_cn', 'lunar', 'ganzhi_year', 'ganzhi_day', 'weekday']
    for field in required_fields:
        assert field in output, f"缺少必需字段：{field}"
    
    print("✅ JSON 输出结构测试通过")
    print(f"   包含字段：{', '.join(output.keys())}")
    print()

def test_edge_cases():
    """测试边界情况"""
    # 测试年份开始
    output = run_lunar_calc("2024-01-01")
    assert '甲辰' in output['ganzhi_year'], "2024 年应该是甲辰年"
    
    # 测试年份结束
    output = run_lunar_calc("2024-12-31")
    assert '甲辰' in output['ganzhi_year'], "2024 年最后一天应该是甲辰年"
    
    # 测试闰年
    output = run_lunar_calc("2024-02-29")
    assert '甲辰' in output['ganzhi_year'], "2024 年 2 月 29 日应该是甲辰年"
    
    print("✅ 边界情况测试通过")
    print()

def main():
    """运行所有测试"""
    print("=" * 60)
    print("农历计算器单元测试")
    print("=" * 60)
    print()
    
    tests = [
        test_2026_march_14,
        test_2025_march_15,
        test_2027_jan_1,
        test_unsupported_year,
        test_json_output_structure,
        test_edge_cases
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_func.__name__} 失败：{e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} 意外错误：{e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("=" * 60)
    print(f"测试完成：✅ {passed} 通过，❌ {failed} 失败")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
