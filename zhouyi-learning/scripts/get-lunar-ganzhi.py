#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
农历 + 干支计算工具 - 周易学习技能
支持 2024-2030 年（7 年范围）

核心功能：
1. 公历转农历日期
2. 六十甲子干支计算
3. 节气查询（简化版）
"""

from datetime import date, timedelta

def get_lunar_date(target_date=None):
    """
    获取农历日期
    
    Args:
        target_date: 目标日期，格式为"YYYY-MM-DD"或 date 对象，默认为今天
    
    Returns:
        农历日期字符串，如"丙午年 正月 十五日"
    """
    if target_date is None:
        target_date = date.today()
    elif isinstance(target_date, str):
        parts = target_date.split('-')
        target_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
    
    # 年份干支（60 甲子循环）
    GANZHI_YEARS = [
        "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", 
        "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥",
        "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳",
        "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥",
        "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
        "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥",
        "庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳",
        "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥",
        "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳",
        "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
    ]
    
    # 月份干支（简化，仅显示月份）
    MONTH_NAMES = {
        1: "正月", 2: "二月", 3: "三月", 4: "四月", 5: "五月", 6: "六月",
        7: "七月", 8: "八月", 9: "九月", 10: "十月", 11: "冬月", 12: "腊月"
    }
    
    # 日期中文（1-30）
    DAY_NAMES = {
        1: "初一", 2: "初二", 3: "初三", 4: "初四", 5: "初五",
        6: "初六", 7: "初七", 8: "初八", 9: "初九", 10: "初十",
        11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
        16: "十六", 17: "十七", 18: "十八", 19: "十九", 20: "二十",
        21: "廿一", 22: "廿二", 23: "廿三", 24: "廿四", 25: "廿五",
        26: "廿六", 27: "廿七", 28: "廿八", 29: "廿九", 30: "三十"
    }
    
    # 农历数据（支持 2024-2030）
    # 格式：(日期，农历月份), 月份 13 表示闰月
    LUNAR_DATA = {
        2024: [
            (date(2024, 2, 10), 13),  # 甲辰年腊月初一
            (date(2024, 2, 10), 1),   # 甲辰年正月初一（闰二月）
            (date(2024, 3, 10), 2),
            (date(2024, 4, 9), 2),    # 闰二月初一
            (date(2024, 5, 9), 4),
            (date(2024, 6, 7), 5),
            (date(2024, 7, 7), 6),
            (date(2024, 8, 5), 7),
            (date(2024, 9, 4), 8),
            (date(2024, 10, 3), 9),
            (date(2024, 11, 2), 10),
            (date(2024, 12, 1), 11),
            (date(2024, 12, 31), 12),
        ],
        2025: [
            (date(2025, 1, 29), 13),  # 甲辰年腊月初一
            (date(2025, 2, 28), 1),   # 乙巳年正月初一（闰六月）
            (date(2025, 3, 29), 2),
            (date(2025, 4, 27), 3),
            (date(2025, 5, 26), 4),
            (date(2025, 6, 25), 5),
            (date(2025, 7, 24), 6),
            (date(2025, 8, 23), 6),   # 闰六月初一
            (date(2025, 9, 21), 7),
            (date(2025, 10, 21), 8),
            (date(2025, 11, 19), 9),
            (date(2025, 12, 19), 10),
            (date(2025, 12, 19), 11),
            (date(2025, 12, 19), 12),
        ],
        2026: [
            (date(2026, 1, 19), 13),  # 乙巳年腊月初一
            (date(2026, 2, 17), 1),   # 丙午年正月初一
            (date(2026, 3, 19), 2),
            (date(2026, 4, 17), 3),
            (date(2026, 5, 17), 4),
            (date(2026, 6, 15), 5),
            (date(2026, 7, 15), 6),
            (date(2026, 8, 13), 7),
            (date(2026, 9, 12), 8),
            (date(2026, 10, 11), 9),
            (date(2026, 11, 9), 10),
            (date(2026, 12, 9), 11),
            (date(2026, 12, 30), 12),
        ],
        2027: [
            (date(2027, 1, 8), 12),   # 丙午年腊月初一
            (date(2027, 2, 6), 1),    # 丁未年正月初一
            (date(2027, 3, 8), 2),
            (date(2027, 4, 6), 3),
            (date(2027, 5, 6), 4),
            (date(2027, 6, 4), 5),
            (date(2027, 7, 4), 6),
            (date(2027, 8, 2), 7),
            (date(2027, 9, 1), 8),
            (date(2027, 9, 30), 9),
            (date(2027, 10, 30), 10),
            (date(2027, 11, 28), 11),
            (date(2027, 12, 28), 12),
        ],
        2028: [
            (date(2028, 1, 26), 13),  # 丁未年腊月初一
            (date(2028, 2, 24), 1),   # 戊申年正月初一
            (date(2028, 3, 24), 2),
            (date(2028, 4, 22), 3),
            (date(2028, 5, 21), 4),
            (date(2028, 6, 20), 5),
            (date(2028, 7, 19), 6),
            (date(2028, 8, 17), 7),
            (date(2028, 9, 16), 8),
            (date(2028, 10, 15), 9),
            (date(2028, 11, 13), 10),
            (date(2028, 12, 13), 11),
            (date(2028, 12, 31), 12),
        ],
        2029: [
            (date(2029, 1, 12), 13),  # 戊申年腊月初一
            (date(2029, 2, 10), 1),   # 己酉年正月初一（闰五月）
            (date(2029, 3, 12), 2),
            (date(2029, 4, 10), 3),
            (date(2029, 5, 10), 4),
            (date(2029, 6, 8), 5),
            (date(2029, 7, 8), 5),    # 闰五月初一
            (date(2029, 8, 6), 7),
            (date(2029, 9, 5), 8),
            (date(2029, 10, 4), 9),
            (date(2029, 11, 3), 10),
            (date(2029, 12, 2), 11),
            (date(2029, 12, 31), 12),
        ],
        2030: [
            (date(2030, 1, 30), 13),  # 己酉年腊月初一
            (date(2030, 2, 28), 1),   # 庚戌年正月初一
            (date(2030, 3, 30), 2),
            (date(2030, 4, 28), 3),
            (date(2030, 5, 28), 4),
            (date(2030, 6, 26), 5),
            (date(2030, 7, 26), 6),
            (date(2030, 8, 24), 7),
            (date(2030, 9, 22), 8),
            (date(2030, 10, 22), 9),
            (date(2030, 11, 20), 10),
            (date(2030, 12, 20), 11),
            (date(2030, 12, 31), 12),
        ],
    }
    
    # 计算年份干支
    year = target_date.year
    year_ganzhi = GANZHI_YEARS[(year - 1984) % 60]
    
    # 查找农历日期
    if year not in LUNAR_DATA:
        return f"暂不支持 {year}年的农历计算（支持 2024-2030）"
    
    lunar_months = LUNAR_DATA[year]
    
    # 找到所属月份
    lunar_month = 1
    lunar_day = 1
    is_leap = False
    
    for i in range(len(lunar_months) - 1):
        start_date, month_num = lunar_months[i]
        next_date, _ = lunar_months[i + 1]
        
        if start_date <= target_date < next_date:
            lunar_month = month_num
            is_leap = (month_num == 13)
            
            # 计算天数
            days_diff = (target_date - start_date).days
            lunar_day = days_diff + 1
            
            # 如果超过 30 天，可能是最后一个月
            if lunar_day > 30:
                lunar_day = 30
            
            break
    
    # 处理年底的情况
    if lunar_month == 1 and year > 2024:
        # 检查是否是上一年的腊月
        prev_year_data = LUNAR_DATA.get(year - 1, [])
        if prev_year_data:
            last_month_start = prev_year_data[-1][0]
            if target_date >= last_month_start:
                lunar_month = 12
                is_leap = False
                days_diff = (target_date - last_month_start).days
                lunar_day = min(days_diff + 1, 30)
                year_ganzhi = GANZHI_YEARS[(year - 1 - 1984) % 60]
    
    # 构建结果
    month_name = MONTH_NAMES.get(lunar_month, f"月{lunar_month}")
    if is_leap:
        month_name = "闰" + month_name
    
    day_name = DAY_NAMES.get(lunar_day, f"日{lunar_day}")
    
    return f"{year_ganzhi}年 {month_name} {day_name}"


def get_ganzhi(target_date=None):
    """
    获取干支纪年、月、日
    
    Args:
        target_date: 目标日期，格式为"YYYY-MM-DD"或 date 对象，默认为今天
    
    Returns:
        包含年、月、日干支的字典
    """
    if target_date is None:
        target_date = date.today()
    elif isinstance(target_date, str):
        parts = target_date.split('-')
        target_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
    
    # 六十甲子
    GANZHI = [
        "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", 
        "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥",
        "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳",
        "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥",
        "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
        "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥",
        "庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳",
        "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥",
        "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳",
        "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
    ]
    
    # 计算年干支（1984 年是甲子年）
    year_ganzhi = GANZHI[(target_date.year - 1984) % 60]
    
    # 简化月干支（仅显示月份序号）
    month_index = ((target_date.year - 1984) % 60 + (target_date.month - 1) // 2) % 60
    month_ganzhi = GANZHI[month_index]
    
    # 简化日干支（基于日期计算，不精确）
    # 实际日干支需要复杂的农历计算，这里用简化版本
    day_offset = (target_date - date(1984, 2, 1)).days
    day_ganzhi = GANZHI[day_offset % 60]
    
    return {
        "year": year_ganzhi,
        "month": f"第{(target_date.month - 1) // 2 + 1}个月",
        "day": day_ganzhi,
        "date": target_date
    }


def main():
    """主函数"""
    print("="*60)
    print("📅 农历 + 干支查询工具".center(60))
    print("="*60)
    print("\n支持日期范围：2024-2030 年\n")
    
    # 显示今天的农历
    today = date.today()
    lunar = get_lunar_date(today)
    ganzhi = get_ganzhi(today)
    
    print(f"今天公历：{today.strftime('%Y年%m月%d日 %A')}")
    print(f"今天农历：{lunar}")
    print(f"\n干支信息:")
    print(f"  年：{ganzhi['year']}")
    print(f"  月：{ganzhi['month']}")
    print(f"  日：{ganzhi['day']}")
    
    # 交互查询
    print("\n" + "-"*60)
    print("输入日期查询（格式：YYYY-MM-DD），或按 Enter 退出")
    
    while True:
        user_input = input("\n请输入日期：").strip()
        if not user_input:
            print("感谢使用！")
            break
        
        try:
            target = date.fromisoformat(user_input)
            lunar = get_lunar_date(target)
            ganzhi = get_ganzhi(target)
            
            print(f"\n公历：{target.strftime('%Y年%m月%d日 %A')}")
            print(f"农历：{lunar}")
            print(f"干支：年{ganzhi['year']} 日{ganzhi['day']}")
        except Exception as e:
            print(f"日期格式错误：{e}")


def main_cli():
    """命令行主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="农历 + 干支计算工具 - 周易学习技能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 get-lunar-ganzhi.py                  # 今日日期
  python3 get-lunar-ganzhi.py --date 2026-03-15  # 指定日期
  python3 get-lunar-ganzhi.py --date 2026-03-15 --json  # JSON 输出
        """
    )
    
    parser.add_argument('--date', '-d', type=str, default=None,
                       help='查询日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('--json', '-j', action='store_true',
                       help='以 JSON 格式输出')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='交互式模式（默认行为）')
    
    args = parser.parse_args()
    
    # 如果指定了 --date 或 --json，使用非交互模式
    if args.date or args.json:
        run_non_interactive(args.date, args.json)
    else:
        # 默认交互模式
        run_interactive()


def run_non_interactive(date_str=None, output_json=False):
    """非交互式运行"""
    if date_str is None:
        target = date.today()
    else:
        try:
            parts = date_str.split('-')
            target = date(int(parts[0]), int(parts[1]), int(parts[2]))
        except Exception as e:
            error_msg = f"日期格式错误：{e}"
            if output_json:
                print(json.dumps({"error": error_msg}))
            else:
                print(error_msg)
            return
    
    lunar = get_lunar_date(target)
    ganzhi = get_ganzhi(target)
    
    if output_json:
        # 星期映射（Python weekday: 0=周一）
        WEEKDAY_CN = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        weekday = WEEKDAY_CN[target.weekday()]
        
        output = {
            "gregorian": target.strftime("%Y-%m-%d"),
            "gregorian_cn": target.strftime("%Y 年%m 月%d日"),
            "lunar": lunar,
            "ganzhi_year": ganzhi['year'],
            "ganzhi_day": ganzhi['day'],
            "weekday": weekday
        }
        print(json.dumps(output, ensure_ascii=False))
    else:
        print("="*60)
        print("农历 + 干支查询")
        print("="*60)
        print(f"公历：{target.strftime('%Y 年%m 月%d日 %A')}")
        print(f"农历：{lunar}")
        print(f"干支：年{ganzhi['year']} 日{ganzhi['day']}")
        print("="*60)


def run_interactive():
    """交互式运行"""
    import json
    
    # 显示今日信息
    today = date.today()
    lunar = get_lunar_date(today)
    ganzhi = get_ganzhi(today)
    
    print("="*60)
    print("农历 + 干支计算工具 - 周易学习技能")
    print("支持 2024-2030 年（7 年范围）")
    print("="*60)
    print()
    print("📅 今日信息")
    print("-"*60)
    print(f"公历：{today.strftime('%Y 年%m 月%d日 %A')}")
    print(f"农历：{lunar}")
    print(f"干支：年{ganzhi['year']} 日{ganzhi['day']}")
    
    # 交互查询
    print("\n" + "-"*60)
    print("输入日期查询（格式：YYYY-MM-DD），或按 Enter 退出")
    
    while True:
        user_input = input("\n请输入日期：").strip()
        if not user_input:
            print("感谢使用！")
            break
        
        try:
            target = date.fromisoformat(user_input)
            lunar = get_lunar_date(target)
            ganzhi = get_ganzhi(target)
            
            print(f"\n公历：{target.strftime('%Y 年%m 月%d日 %A')}")
            print(f"农历：{lunar}")
            print(f"干支：年{ganzhi['year']} 日{ganzhi['day']}")
        except Exception as e:
            print(f"日期格式错误：{e}")


if __name__ == "__main__":
    import sys
    import json
    main_cli()
