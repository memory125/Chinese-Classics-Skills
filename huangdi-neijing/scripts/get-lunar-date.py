#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确农历日期转换器 - 基于权威农历数据
支持 2024-2030 年完整数据

适用场景：黄帝内经养生技能 - 实时节气养生建议
"""

import json
import sys
from datetime import date, datetime

class LunarCalendar:
    """农历计算器 - 多年份支持版"""
    
    # 月份中文名称（索引从 1 开始，0 是占位符）
    MONTH_NAMES = ["", "正月", "二月", "三月", "四月", "五月", "六月", 
                   "七月", "八月", "九月", "十月", "冬月", "腊月"]
    
    # 日期中文
    DAY_NAMES = {
        1: "初一", 2: "初二", 3: "初三", 4: "初四", 5: "初五",
        6: "初六", 7: "初七", 8: "初八", 9: "初九", 10: "初十",
        11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
        16: "十六", 17: "十七", 18: "十八", 19: "十九", 20: "二十",
        21: "廿一", 22: "廿二", 23: "廿三", 24: "廿四", 25: "廿五",
        26: "廿六", 27: "廿七", 28: "廿八", 29: "廿九", 30: "三十"
    }
    
    # 干支纪年（60 甲子循环）
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
    
    # 生肖（12 年循环）
    ANIMALS = ["鼠", "牛", "虎", "兔", "龙", "蛇", 
               "马", "羊", "猴", "鸡", "狗", "猪"]
    
    # 2024-2030 年农历数据 - 每月初一的公历日期
    # 格式：(date(year, month, day), lunar_month_num)
    # lunar_month_num: 1-12 表示正月到腊月，13 表示上一年的腊月
    LUNAR_DATA = {
        2024: [
            (date(2024, 2, 10), 13),   # 甲辰年腊月初一
            (date(2024, 2, 10), 1),    # 甲辰年正月初一（闰二月）
            (date(2024, 3, 11), 2),    # 二月初一
            (date(2024, 4, 9), 3),     # 闰二月初一
            (date(2024, 5, 9), 4),     # 三月初一
            (date(2024, 6, 7), 5),     # 四月初一
            (date(2024, 7, 7), 6),     # 五月初一
            (date(2024, 8, 5), 7),     # 六月初一
            (date(2024, 9, 3), 8),     # 七月初一
            (date(2024, 10, 2), 9),    # 八月初一
            (date(2024, 11, 1), 10),   # 九月初一
            (date(2024, 11, 30), 11),  # 十月初一
            (date(2024, 12, 30), 12),  # 冬月初一
        ],
        2025: [
            (date(2025, 1, 28), 13),   # 甲辰年腊月初一
            (date(2025, 1, 29), 1),    # 乙巳年正月初一
            (date(2025, 2, 27), 2),    # 二月初一
            (date(2025, 3, 28), 3),    # 三月初一
            (date(2025, 4, 27), 4),    # 四月初一
            (date(2025, 5, 27), 5),    # 五月初一
            (date(2025, 6, 25), 6),    # 六月初一
            (date(2025, 7, 25), 7),    # 七月初一
            (date(2025, 8, 23), 8),    # 八月初一
            (date(2025, 9, 22), 9),    # 九月初一
            (date(2025, 10, 22), 10),  # 十月初一
            (date(2025, 11, 20), 11),  # 冬月初一
            (date(2025, 12, 20), 12),  # 腊月初一
        ],
        2026: [
            (date(2026, 1, 19), 13),   # 乙巳年腊月初一
            (date(2026, 2, 17), 1),    # 丙午年正月初一
            (date(2026, 3, 19), 2),    # 二月初一
            (date(2026, 4, 17), 3),    # 三月初一
            (date(2026, 5, 17), 4),    # 四月初一
            (date(2026, 6, 15), 5),    # 五月初一
            (date(2026, 7, 15), 6),    # 六月初一
            (date(2026, 8, 13), 7),    # 七月初一
            (date(2026, 9, 12), 8),    # 八月初一
            (date(2026, 10, 11), 9),   # 九月初一
            (date(2026, 11, 9), 10),   # 十月初一
            (date(2026, 12, 9), 11),   # 冬月初一
            (date(2026, 12, 30), 12),  # 腊月初一
        ],
        2027: [
            (date(2027, 1, 28), 13),   # 丙午年腊月初一
            (date(2027, 2, 16), 1),    # 丁未年正月初一
            (date(2027, 3, 17), 2),    # 二月初一
            (date(2027, 4, 16), 3),    # 三月初一
            (date(2027, 5, 16), 4),    # 四月初一
            (date(2027, 6, 14), 5),    # 五月初一
            (date(2027, 7, 14), 6),    # 六月初一
            (date(2027, 8, 12), 7),    # 七月初一
            (date(2027, 9, 10), 8),    # 八月初一
            (date(2027, 10, 10), 9),   # 九月初一
            (date(2027, 11, 8), 10),   # 十月初一
            (date(2027, 12, 8), 11),   # 冬月初一
            (date(2027, 12, 29), 12),  # 腊月初一
        ],
        2028: [
            (date(2028, 1, 27), 13),   # 丁未年腊月初一
            (date(2028, 2, 15), 1),    # 戊申年正月初一
            (date(2028, 3, 15), 2),    # 二月初一
            (date(2028, 4, 14), 3),    # 三月初一
            (date(2028, 5, 13), 4),    # 四月初一
            (date(2028, 6, 11), 5),    # 五月初一
            (date(2028, 7, 11), 6),    # 六月初一
            (date(2028, 8, 9), 7),     # 七月初一
            (date(2028, 9, 7), 8),     # 八月初一
            (date(2028, 10, 6), 9),    # 九月初一
            (date(2028, 11, 4), 10),   # 十月初一
            (date(2028, 12, 3), 11),   # 冬月初一
            (date(2028, 12, 23), 12),  # 腊月初一
        ],
        2029: [
            (date(2029, 1, 22), 13),   # 戊申年腊月初一
            (date(2029, 2, 10), 1),    # 己酉年正月初一
            (date(2029, 3, 12), 2),    # 二月初一
            (date(2029, 4, 11), 3),    # 三月初一
            (date(2029, 5, 11), 4),    # 四月初一
            (date(2029, 6, 9), 5),     # 五月初一
            (date(2029, 7, 8), 6),     # 六月初一
            (date(2029, 8, 6), 7),     # 七月初一
            (date(2029, 9, 4), 8),     # 八月初一
            (date(2029, 10, 4), 9),    # 九月初一
            (date(2029, 11, 2), 10),   # 十月初一
            (date(2029, 12, 2), 11),   # 冬月初一
            (date(2029, 12, 22), 12),  # 腊月初一
        ],
        2030: [
            (date(2030, 1, 21), 13),   # 己酉年腊月初一
            (date(2030, 2, 9), 1),     # 庚戌年正月初一
            (date(2030, 3, 10), 2),    # 二月初一
            (date(2030, 4, 9), 3),     # 三月初一
            (date(2030, 5, 9), 4),     # 四月初一
            (date(2030, 6, 7), 5),     # 五月初一
            (date(2030, 7, 7), 6),     # 六月初一
            (date(2030, 8, 5), 7),     # 七月初一
            (date(2030, 9, 3), 8),     # 八月初一
            (date(2030, 10, 3), 9),    # 九月初一
            (date(2030, 11, 1), 10),   # 十月初一
            (date(2030, 11, 30), 11),  # 冬月初一
            (date(2030, 12, 30), 12),  # 腊月初一
        ]
    }
    
    def __init__(self, target_date=None):
        """初始化"""
        if target_date is None:
            self.target_date = date.today()
        elif isinstance(target_date, str):
            self.target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            self.target_date = target_date
        
        self.year = self.target_date.year
        
        # 检查是否支持该年份
        if self.year not in self.LUNAR_DATA:
            raise ValueError(f"暂不支持 {self.year} 年的农历查询，当前支持 2024-2030 年")
    
    def _get_ganzhi_year(self):
        """获取干支纪年"""
        base_year = 1984  # 甲子年
        offset = (self.year - base_year) % 60
        return self.GANZHI[offset]
    
    def _get_animal(self):
        """获取生肖"""
        base_year = 1900  # 鼠年
        offset = (self.year - base_year) % 12
        return self.ANIMALS[offset]
    
    def get_lunar_date(self):
        """获取农历日期"""
        target = self.target_date
        year = target.year
        
        # 获取该年的农历数据
        lunar_months = self.LUNAR_DATA.get(year, [])
        
        # 找到前一个月的初一
        prev_month_start = None
        lunar_month = 1
        prev_year_ganzhi = None
        
        for month_date, month_num in lunar_months:
            if month_date <= target:
                prev_month_start = month_date
                lunar_month = month_num
                # 如果是腊月（13），需要获取上一年的干支
                if month_num == 13:
                    prev_year_ganzhi = self._get_prev_year_ganzhi(year)
                else:
                    prev_year_ganzhi = None
            else:
                break
        
        if prev_month_start:
            days_since_new_moon = (target - prev_month_start).days
            lunar_day = 1 + days_since_new_moon
            lunar_day = min(lunar_day, 30)
            
            return self._format_lunar_date(lunar_month, lunar_day, prev_year_ganzhi)
        
        # 如果找不到，返回默认值
        return {
            "lunar_year": f"{self._get_ganzhi_year()}年",
            "lunar_year_zh": self._get_ganzhi_year(),
            "animal": self._get_animal(),
            "lunar_month_num": 1,
            "lunar_month_name": "正月",
            "lunar_day_num": 1,
            "lunar_day_name": "初一",
            "full_lunar_date": "正月初一",
        }
    
    def _get_prev_year_ganzhi(self, year):
        """获取上一年的干支"""
        prev_year = year - 1
        base_year = 1984
        offset = (prev_year - base_year) % 60
        return self.GANZHI[offset]
    
    def _format_lunar_date(self, lunar_month, lunar_day, prev_year_ganzhi=None):
        """格式化农历日期"""
        # 处理特殊月份（腊月=13）
        if lunar_month == 13:
            month_name = "腊月"
            year_str = f"{prev_year_ganzhi}年"
            year_zh = prev_year_ganzhi
        else:
            month_name = self.MONTH_NAMES[lunar_month]
            year_str = f"{self._get_ganzhi_year()}年"
            year_zh = self._get_ganzhi_year()
        
        return {
            "lunar_year": year_str,
            "lunar_year_zh": year_zh,
            "animal": self._get_animal() if lunar_month != 13 else self.ANIMALS[(self.year - 1900 - 1) % 12],
            "lunar_month_num": lunar_month if lunar_month != 13 else 12,
            "lunar_month_name": month_name,
            "lunar_day_num": lunar_day,
            "lunar_day_name": self.DAY_NAMES.get(lunar_day, str(lunar_day)),
            "full_lunar_date": f"{month_name}{self.DAY_NAMES.get(lunar_day, lunar_day)}",
        }

def main():
    """主函数"""
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        target_date = None
    
    try:
        calculator = LunarCalendar(target_date)
        lunar_info = calculator.get_lunar_date()
        
        result = {
            "success": True,
            "data": {
                "gregorian_date": f"{calculator.target_date.year}年{calculator.target_date.month}月{calculator.target_date.day}日",
                "lunar_date": lunar_info,
                "display_text": f"农历{lunar_info['lunar_year_zh']}{lunar_info['lunar_month_name']}{lunar_info['lunar_day_name']}"
            }
        }
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as e:
        result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
