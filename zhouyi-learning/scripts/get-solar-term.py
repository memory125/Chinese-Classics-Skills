#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节气计算器 - 周易学习技能
基于二十四节气为卦象推荐提供时间背景

功能：
- 获取当前节气
- 节气与八卦对应（春震夏离秋兑冬坎）
- 季节五行属性
"""

import json
import sys
from datetime import date, datetime

class SolarTermCalculator:
    """节气计算器 - 周易专用版"""
    
    # 2026 年二十四节气精确时间（UTC+8）
    SOLAR_TERMS_2026 = [
        ("小寒", date(2026, 1, 5)),
        ("大寒", date(2026, 1, 20)),
        ("立春", date(2026, 2, 3)),
        ("雨水", date(2026, 2, 18)),
        ("惊蛰", date(2026, 3, 5)),
        ("春分", date(2026, 3, 20)),
        ("清明", date(2026, 4, 5)),
        ("谷雨", date(2026, 4, 20)),
        ("立夏", date(2026, 5, 5)),
        ("小满", date(2026, 5, 21)),
        ("芒种", date(2026, 6, 5)),
        ("夏至", date(2026, 6, 21)),
        ("小暑", date(2026, 7, 7)),
        ("大暑", date(2026, 7, 23)),
        ("立秋", date(2026, 8, 7)),
        ("处暑", date(2026, 8, 23)),
        ("白露", date(2026, 9, 7)),
        ("秋分", date(2026, 9, 22)),
        ("寒露", date(2026, 10, 8)),
        ("霜降", date(2026, 10, 23)),
        ("立冬", date(2026, 11, 7)),
        ("小雪", date(2026, 11, 22)),
        ("大雪", date(2026, 12, 7)),
        ("冬至", date(2026, 12, 21)),
    ]
    
    # 节气到季节/八卦映射
    SEASON_MAP = {
        "立春": ("春季", "震卦", "木"),
        "雨水": ("春季", "震卦", "木"),
        "惊蛰": ("春季", "震卦", "木"),
        "春分": ("春季", "巽卦", "木"),
        "清明": ("春季", "巽卦", "木"),
        "谷雨": ("春季", "巽卦", "木"),
        
        "立夏": ("夏季", "离卦", "火"),
        "小满": ("夏季", "离卦", "火"),
        "芒种": ("夏季", "离卦", "火"),
        "夏至": ("夏季", "离卦", "火"),
        "小暑": ("夏季", "离卦", "火"),
        "大暑": ("夏季", "兑卦", "金"),
        
        "立秋": ("秋季", "兑卦", "金"),
        "处暑": ("秋季", "兑卦", "金"),
        "白露": ("秋季", "兑卦", "金"),
        "秋分": ("秋季", "乾卦", "金"),
        "寒露": ("秋季", "乾卦", "金"),
        "霜降": ("秋季", "乾卦", "金"),
        
        "立冬": ("冬季", "坎卦", "水"),
        "小雪": ("冬季", "坎卦", "水"),
        "大雪": ("冬季", "坎卦", "水"),
        "冬至": ("冬季", "坎卦", "水"),
        "小寒": ("冬季", "艮卦", "土"),
        "大寒": ("冬季", "艮卦", "土"),
    }
    
    # 卦象推荐（按节气特点）
    GUA_RECOMMENDATION = {
        "立春": ["复", "临", "泰"],  # 一阳来复，万物复苏
        "雨水": ["需", "蒙", "师"],  # 滋润萌发
        "惊蛰": ["震", "豫", "随"],  # 春雷动，万物生
        "春分": ["同人", "大有", "谦"],  # 阴阳平衡
        "清明": ["贲", "剥", "颐"],  # 明朗洁净
        "谷雨": ["小过", "既济", "未济"],  # 雨生百谷
        
        "立夏": ["鼎", "革", "家人"],  # 万物至此皆长大
        "小满": ["姤", "萃", "升"],  # 麦类饱满
        "芒种": ["咸", "恒", "遁"],  # 忙种时节
        "夏至": ["乾", "大壮", "夬"],  # 阳气最盛
        "小暑": ["晋", "明夷", "丰"],  # 炎热始
        "大暑": ["旅", "巽", "兑"],  # 极热天气
        
        "立秋": ["坤", "比", "师"],  # 凉风至
        "处暑": ["节", "中孚", "涣"],  # 出暑转凉
        "白露": ["观", "大过", "坎"],  # 露凝而白
        "秋分": ["小畜", "履", "泰"],  # 昼夜平分
        "寒露": ("蹇", "解", "损"),  # 露水更凉
        "霜降": ["益", "夬", "姤"],  # 天气渐冷
        
        "立冬": ["屯", "蒙", "需"],  # 万物收藏
        "小雪": ["讼", "师", "比"],  # 降水变雪
        "大雪": ["蛊", "临", "观"],  # 雪量增大
        "冬至": ["复", "坤", "艮"],  # 阴极阳生
        "小寒": ["颐", "大过", "坎"],  # 寒冷开始
        "大寒": ["离", "咸", "恒"],  # 最冷时节
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
    
    def get_current_solar_term(self):
        """获取当前节气信息"""
        target = self.target_date
        
        # 找到当前所在的节气区间
        current_term = None
        days_since_term = float('inf')
        
        for term_name, term_date in self.SOLAR_TERMS_2026:
            if term_date <= target:
                diff = (target - term_date).days
                if diff < days_since_term:
                    current_term = term_name
                    days_since_term = diff
        
        if not current_term:
            current_term = "小寒"
            days_since_term = 0
        
        # 获取节气信息
        season_info = self.SEASON_MAP.get(current_term, ("四季", "坤卦", "土"))
        
        return {
            "solar_term": current_term,
            "season": season_info[0],
            "bagua": season_info[1],
            "element": season_info[2],
            "days_since_term": days_since_term,
            "term_guidance": self._get_term_guidance(current_term),
            "recommended_gua": self.GUA_RECOMMENDATION.get(current_term, ["坤", "复", "谦"])
        }
    
    def _get_term_guidance(self, term_name):
        """获取节气指导"""
        guidance_map = {
            "立春": "东风解冻，蛰虫始振。宜：播种希望，制定新目标。",
            "雨水": "獭祭鱼，鸿雁来。宜：润物细无声，默默耕耘。",
            "惊蛰": "桃始华，仓庚鸣。宜：振作精神，开始行动。",
            "春分": "玄鸟至，雷乃发声。宜：平衡阴阳，协调关系。",
            "清明": "桐始华，田鼠化为鴽。宜：明心见性，清理杂念。",
            "谷雨": "萍始生，鸣鸠拂其羽。宜：厚积薄发，期待丰收。",
            
            "立夏": "蝼蝈鸣，蚯蚓出。宜：顺势而为，积极成长。",
            "小满": "苦菜秀，靡草死。宜：知足常乐，珍惜当下。",
            "芒种": "螳螂生，鵙始鸣。宜：抓紧时间，忙碌有序。",
            "夏至": "鹿角解，蝉始鸣。宜：盛极必衰，保持谦逊。",
            "小暑": "温风至，蟋蟀居壁。宜：静心养气，避免浮躁。",
            "大暑": "腐草为萤，土润溽暑。宜：以静制动，韬光养晦。",
            
            "立秋": "凉风至，白露生。宜：收敛锋芒，准备收获。",
            "处暑": "鹰乃祭鸟，天地始肃。宜：清理总结，告别过去。",
            "白露": "鸿雁来，玄鸟归。宜：思乡念旧，感恩惜福。",
            "秋分": "雷始收声，蛰虫坯户。宜：内外平衡，公私兼顾。",
            "寒露": "鸿雁来宾，雀入大水为蛤。宜：未雨绸缪，提前准备。",
            "霜降": "豺乃祭兽，草木黄落。宜：审时度势，及时调整。",
            
            "立冬": "水始冰，地始冻。宜：蓄势待发，养精蓄锐。",
            "小雪": "虹藏不见，天气上升。宜：内敛沉淀，修炼内功。",
            "大雪": "鹖鴠不鸣，虎始交。宜：隐忍待机，厚积薄发。",
            "冬至": "蚯蚓结，麋角解。宜：阴极阳生，孕育新机。",
            "小寒": "雁北乡，鹊始巢。宜：等待时机，静观其变。",
            "大寒": "鸡乳，獭祭鱼。宜：寒冬将尽，曙光在前。",
        }
        return guidance_map.get(term_name, "顺应时节，修身养性。")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        target_date = None
    
    calculator = SolarTermCalculator(target_date)
    result = calculator.get_current_solar_term()
    
    output = {
        "success": True,
        "data": result,
        "target_date": str(calculator.target_date)
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
