#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日一卦 - 周易学习技能 v1.0
根据农历日期和节气推荐每日卦象

核心思路：
1. 结合农历日期的天干地支
2. 考虑当前节气特点  
3. 提供贴合当日的卦象启示

版本：v1.0 (2026-03-25)
"""

import json
import sys
from datetime import date, datetime
import random

class DailyGua:
    """每日一卦生成器"""
    
    # 简化版六十四卦数据（常用卦象）
    SIXTY_FOUR_GUA = {
        "乾": {"hexagram": "䷀", "nature": "健", "theme": "自强不息", "element": "天"},
        "坤": {"hexagram": "䷁", "nature": "顺", "theme": "厚德载物", "element": "地"},
        "屯": {"hexagram": "䷂", "nature": "难", "theme": "艰难创业", "element": "水雷"},
        "蒙": {"hexagram": "䷃", "nature": "昧", "theme": "启蒙求知", "element": "山水"},
        "需": {"hexagram": "䷄", "nature": "待", "theme": "耐心等待", "element": "水天"},
        "讼": {"hexagram": "䷅", "nature": "争", "theme": "慎始敬终", "element": "天水"},
        "师": {"hexagram": "䷆", "nature": "众", "theme": "以正治国", "element": "地水"},
        "比": {"hexagram": "䷇", "nature": "辅", "theme": "亲附和睦", "element": "水土"},
        "小畜": {"hexagram": "䷈", "nature": "蓄", "theme": "小有积蓄", "element": "风天"},
        "履": {"hexagram": "䷉", "nature": "礼", "theme": "如履薄冰", "element": "天泽"},
        "泰": {"hexagram": "䷊", "nature": "通", "theme": "天地交泰", "element": "地天"},
        "否": {"hexagram": "䷋", "nature": "塞", "theme": "小人道长", "element": "天地"},
        "同人": {"hexagram": "䷌", "nature": "和", "theme": "天下大同", "element": "天火"},
        "大有": {"hexagram": "䷍", "nature": "盛", "theme": "盛大拥有", "element": "火天"},
        "谦": {"hexagram": "䷎", "nature": "卑", "theme": "谦虚受益", "element": "地山"},
        "豫": {"hexagram": "䷏", "nature": "乐", "theme": "顺时而动", "element": "雷地"},
        "随": {"hexagram": "䷐", "nature": "从", "theme": "随时而变", "element": "泽雷"},
        "蛊": {"hexagram": "䷑", "nature": "坏", "theme": "革故鼎新", "element": "山风"},
        "临": {"hexagram": "䷒", "nature": "进", "theme": "亲临督导", "element": "地泽"},
        "观": {"hexagram": "䷓", "nature": "视", "theme": "以大观小", "element": "风地"},
        "噬嗑": {"hexagram": "䷔", "nature": "合", "theme": "明断是非", "element": "火雷"},
        "贲": {"hexagram": "䷕", "nature": "饰", "theme": "文质彬彬", "element": "山火"},
        "剥": {"hexagram": "䷖", "nature": "落", "theme": "阴盛阳衰", "element": "山地"},
        "复": {"hexagram": "䷗", "nature": "返", "theme": "一阳来复", "element": "地雷"},
        "无妄": {"hexagram": "䷘", "nature": "真", "theme": "实事求是", "element": "天雷"},
        "大畜": {"hexagram": "䷙", "nature": "止", "theme": "大为蓄积", "element": "山天"},
        "颐": {"hexagram": "䷚", "nature": "养", "theme": "自求口实", "element": "山雷"},
        "大过": {"hexagram": "䷛", "nature": "溺", "theme": "非常行动", "element": "泽风"},
        "坎": {"hexagram": "䷜", "nature": "险", "theme": "重险在前", "element": "水"},
        "离": {"hexagram": "䷝", "nature": "丽", "theme": "明两作", "element": "火"},
        "咸": {"hexagram": "䷞", "nature": "感", "theme": "无心之感", "element": "泽山"},
        "恒": {"hexagram": "䷟", "nature": "久", "theme": "长久之道", "element": "雷风"},
        "遁": {"hexagram": "䷠", "nature": "退", "theme": "退避待时", "element": "天山"},
        "大壮": {"hexagram": "䷡", "nature": "盛", "theme": "刚健有力", "element": "雷天"},
        "晋": {"hexagram": "䷢", "nature": "进", "theme": "旭日东升", "element": "火地"},
        "明夷": {"hexagram": "䷣", "nature": "伤", "theme": "光明受伤", "element": "地火"},
        "家人": {"hexagram": "䷤", "name": "风火家人", "nature": "亲", "theme": "家道正", "element": "风火"},
        "睽": {"hexagram": "䷥", "nature": "乖", "theme": "异中求同", "element": "火泽"},
        "蹇": {"hexagram": "䷦", "nature": "难", "theme": "见险而止", "element": "水山"},
        "解": {"hexagram": "䷧", "nature": "散", "theme": "解难释困", "element": "雷水"},
        "损": {"hexagram": "䷨", "nature": "减", "theme": "损下益上", "element": "山泽"},
        "益": {"hexagram": "䷩", "nature": "增", "theme": "损上益下", "element": "风雷"},
        "夬": {"hexagram": "䷪", "nature": "决", "theme": "果决去除", "element": "泽天"},
        "姤": {"hexagram": "䷫", "name": "天风姤", "nature": "遇", "theme": "阴阳相遇", "element": "天风"},
        "萃": {"hexagram": "䷬", "nature": "聚", "theme": "聚合人心", "element": "泽地"},
        "升": {"hexagram": "䷭", "name": "地风升", "nature": "进", "theme": "积小成大", "element": "地风"},
        "困": {"hexagram": "䷮", "nature": "险", "theme": "困顿之时", "element": "泽水"},
        "井": {"hexagram": "䷯", "nature": "养", "theme": "养人无穷", "element": "水风"},
        "革": {"hexagram": "䷰", "nature": "改", "theme": "变革革新", "element": "泽火"},
        "鼎": {"hexagram": "䷱", "nature": "新", "theme": "鼎新革故", "element": "火风"},
        "震": {"hexagram": "䷲", "nature": "动", "theme": "震惊百里", "element": "雷"},
        "艮": {"hexagram": "䷳", "nature": "止", "theme": "动静适时", "element": "山"},
        "渐": {"hexagram": "䷴", "nature": "进", "theme": "渐进有序", "element": "风山"},
        "归妹": {"hexagram": "䷵", "nature": "嫁", "theme": "少女配长男", "element": "雷泽"},
        "丰": {"hexagram": "䷶", "nature": "大", "theme": "丰盛之时", "element": "雷火"},
        "旅": {"hexagram": "䷷", "nature": "客", "theme": "行旅不安", "element": "火山"},
        "巽": {"hexagram": "䷸", "name": "巽为风", "nature": "入", "theme": "顺从入微", "element": "风"},
        "兑": {"hexagram": "䷹", "name": "兑为泽", "nature": "说", "theme": "欣悦和乐", "element": "泽"},
        "涣": {"hexagram": "䷺", "name": "风水涣", "nature": "散", "theme": "涣散凝聚", "element": "风水"},
        "节": {"hexagram": "䷻", "nature": "制", "theme": "节制有度", "element": "水泽"},
        "中孚": {"hexagram": "䷼", "name": "风泽中孚", "nature": "信", "theme": "诚信感化", "element": "风泽"},
        "小过": {"hexagram": "䷽", "name": "雷山小过", "nature": "过", "theme": "小有过度", "element": "雷山"},
        "既济": {"hexagram": "䷾", "nature": "成", "theme": "事已成", "element": "水火"},
        "未济": {"hexagram": "䷿", "nature": "乱", "theme": "事未成", "element": "火水"}
    }
    
    # 八卦与农历月份对应（春季）
    MONTH_BAGUA = {
        1: ["震", "巽"],   # 正月：春木生发
        2: ["巽", "离"],   # 二月：春夏交替
        3: ["离", "兑"],   # 三月：夏火旺盛
    }
    
    def __init__(self, target_date=None):
        """初始化"""
        if target_date is None:
            self.target_date = date.today()
        elif isinstance(target_date, str):
            self.target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            self.target_date = target_date
        
        # 简单的农历计算（实际应调用 get-lunar-ganzhi.py）
        self.lunar_info = self._get_lunar_date_simplified()
    
    def _get_lunar_date_simplified(self):
        """简化的农历日期获取"""
        year = self.target_date.year
        month = self.target_date.month
        day = self.target_date.day
        
        # 2026 年数据（硬编码，与黄帝内经同步）
        if year == 2026:
            from datetime import date as d
            target = self.target_date
            
            # 2026 年农历月份起始
            lunar_months = [
                (d(2026, 1, 19), "腊月", 13),
                (d(2026, 2, 17), "正月", 1),
                (d(2026, 3, 19), "二月", 2),
            ]
            
            prev_start = None
            lunar_month_name = ""
            lunar_month_num = 1
            
            for month_date, lmonth_name, lmonth_num in lunar_months:
                if month_date <= target:
                    prev_start = month_date
                    lunar_month_name = lmonth_name
                    lunar_month_num = lmonth_num
                else:
                    break
            
            if prev_start:
                lunar_day = (target - prev_start).days + 1
                # 转换为中文日期
                if lunar_day == 1:
                    day_str = "初一"
                elif lunar_day == 2:
                    day_str = "初二"
                elif lunar_day == 3:
                    day_str = "初三"
                elif lunar_day <= 10:
                    day_str = f"初{lunar_day}"
                elif lunar_day == 11:
                    day_str = "十一"
                elif lunar_day == 20:
                    day_str = "二十"
                elif lunar_day <= 20:
                    day_str = f"十{lunar_day-10}"
                elif lunar_day <= 29:
                    day_str = f"廿{lunar_day-20}"
                elif lunar_day == 30:
                    day_str = "三十"
                else:
                    day_str = "三十"
                return {"month": lunar_month_name, "lunar_month_num": lunar_month_num, "day": lunar_day, "day_str": day_str}
        
        return {"month": "未知月", "lunar_month_num": 1, "day": day}
    
    def generate_daily_gua(self):
        """生成每日一卦（整合农历 + 节气）"""
        import subprocess
        import logging
        
        # 初始化日志
        logger = logging.getLogger(__name__)
        
        try:
            result = subprocess.run(
                ['python3', 'get-solar-term.py'],
                capture_output=True, 
                text=True,
                cwd='/home/wing/.openclaw/workspace/skills/zhouyi-learning/scripts',
                timeout=10
            )
            
            if result.returncode != 0:
                logger.error(f"节气计算失败：{result.stderr}")
                raise Exception(f"Subprocess error: {result.stderr}")
            
            solar_data = json.loads(result.stdout)
            
            if not solar_data.get('success'):
                logger.warning("节气数据返回失败，使用备用方案")
                recommended_gua_list = ["坤", "复", "谦"]
                solar_term = ""
            else:
                recommended_gua_list = solar_data['data'].get('recommended_gua', [])
                solar_term = solar_data['data'].get('solar_term', '')
                
        except subprocess.TimeoutExpired:
            logger.error("节气计算超时")
            recommended_gua_list = ["坤", "复", "谦"]
            solar_term = ""
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败：{e}")
            recommended_gua_list = ["坤", "复", "谦"]
            solar_term = ""
        except Exception as e:
            logger.error(f"意外错误：{e}")
            recommended_gua_list = ["坤", "复", "谦"]
            solar_term = ""
        
        # 优先使用节气推荐的卦象
        if recommended_gua_list and len(recommended_gua_list) > 0:
            main_gua_name = random.choice(recommended_gua_list)
        else:
            main_gua_name = random.choice(list(self.SIXTY_FOUR_GUA.keys()))
        
        gua_data = self.SIXTY_FOUR_GUA.get(main_gua_name, {
            "hexagram": "?", 
            "nature": "未知", 
            "theme": "待补充"
        })
        
        # 计算惊蛰后第几天（2026 年惊蛰是 3 月 5 日）
        jizhe_date = date(self.target_date.year, 3, 5) if self.target_date.year == 2026 else None
        days_after_jizhe = None
        if jizhe_date and self.target_date.month >= 3:
            days_after_jizhe = (self.target_date - jizhe_date).days
        
        return {
            "date": {
                "gregorian": f"{self.target_date.year}年{self.target_date.month}月{self.target_date.day}日",
                "lunar": f"{self.lunar_info['month']}{self.lunar_info.get('day_str', '未知')}",
                "lunar_day": self.lunar_info["day"]
            },
            "solar_term": {
                "term": solar_term,
                "recommendation_source": "节气推荐" if solar_term else "随机选择",
                "days_after_jizhe": days_after_jizhe if days_after_jizhe else None
            },
            "solar_term": {
                "term": solar_term,
                "recommendation_source": "节气推荐" if solar_term else "随机选择"
            },
            "hexagram": {
                "name": main_gua_name,
                "symbol": gua_data.get("hexagram", "?"),
                "nature": gua_data.get("nature", "未知"),
                "theme": gua_data.get("theme", "待补充")
            },
            "insight": self._generate_insight(main_gua_name),
            "reflection_question": self._generate_reflection(main_gua_name)
        }
    
    def _generate_insight(self, gua_name):
        """生成卦象启示"""
        insights = {
            "乾": "今日宜自强不息，积极行动。天道刚健，当效法其精神。",
            "坤": "今日宜顺势而为，包容厚德。地道柔顺，当效法其包容。",
            "震": "今日可能有变动发生，宜积极应对变化。",
            "离": "今日宜明察事理，保持清醒判断。"
        }
        return insights.get(gua_name, "今日宜静心观察，顺势而为。")
    
    def _generate_reflection(self, gua_name):
        """生成反思问题"""
        questions = {
            "乾": "今天有哪些事情需要我更加积极主动？",
            "坤": "今天有哪些地方可以展现包容与耐心？",
            "震": "面对变化，我的第一反应是什么？",
            "离": "今天有什么需要我明察秋毫的事情？"
        }
        return questions.get(gua_name, "今天的经历给了我什么启示？")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        target_date = None
    
    generator = DailyGua(target_date)
    result = generator.generate_daily_gua()
    
    output = {
        "success": True,
        "data": result
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
