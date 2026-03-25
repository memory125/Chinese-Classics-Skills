#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄帝内经节气计算器
根据公历日期自动获取农历日期和当前节气
"""

import json
import sys
from datetime import datetime, date

# 二十四节气简表（近似日期，可用于快速定位）
SOLAR_TERMS = [
    ("立春", "02-03"), ("雨水", "02-18"), ("惊蛰", "03-05"),
    ("春分", "03-20"), ("清明", "04-04"), ("谷雨", "04-19"),
    ("立夏", "05-05"), ("小满", "05-20"), ("芒种", "06-05"),
    ("夏至", "06-21"), ("小暑", "07-06"), ("大暑", "07-22"),
    ("立秋", "08-07"), ("处暑", "08-22"), ("白露", "09-07"),
    ("秋分", "09-22"), ("寒露", "10-08"), ("霜降", "10-23"),
    ("立冬", "11-07"), ("小雪", "11-22"), ("大雪", "12-07"),
    ("冬至", "12-21"), ("小寒", "01-05"), ("大寒", "01-20")
]

SEASONS = {
    "立春": "春季（养肝）", "雨水": "春季（养肝）", "惊蛰": "春季（养肝）",
    "春分": "春季（养肝）", "清明": "春季（养肝）", "谷雨": "春季（养肝）",
    "立夏": "夏季（养心）", "小满": "夏季（养心）", "芒种": "夏季（养心）",
    "夏至": "夏季（养心）", "小暑": "夏季（养心）", "大暑": "夏季（养心）",
    "立秋": "秋季（养肺）", "处暑": "秋季（养肺）", "白露": "秋季（养肺）",
    "秋分": "秋季（养肺）", "寒露": "秋季（养肺）", "霜降": "秋季（养肺）",
    "立冬": "冬季（养肾）", "小雪": "冬季（养肾）", "大雪": "冬季（养肾）",
    "冬至": "冬季（养肾）", "小寒": "冬季（养肾）", "大寒": "冬季（养肾）"
}

def get_current_solar_term_info():
    """获取当前日期对应的节气信息"""
    today = date.today()
    year = today.year
    month_day = today.strftime("%m-%d")
    
    # 简单匹配当前节气（实际应使用精确的节气计算算法）
    current_term = None
    for term, tm in SOLAR_TERMS:
        if tm <= month_day:
            current_term = term
        else:
            break
    
    if not current_term:
        current_term = "大寒"  # 默认最后一个节气
    
    season_info = SEASONS.get(current_term, "四季养生")
    
    return {
        "公历": today.strftime("%Y年%m月%d日"),
        "节气": current_term,
        "季节": season_info,
        "日期对象": today.isoformat()
    }

def main():
    info = get_current_solar_term_info()
    
    # 输出 JSON 格式供其他脚本调用
    output = {
        "success": True,
        "data": {
            "gregorian_date": info["公历"],
            "solar_term": info["节气"],
            "season": info["季节"],
            "date_iso": info["日期对象"]
        }
    }
    
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
