#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件时间线数据库 - 使用 matplotlib/plotly 绘制历史事件时间轴

功能：
1. 事件数据库构建 (时间、地点、人物、结果)
2. 时间线生成器 (按年代排序)
3. 可视化展示 (甘特图/时间轴)
4. 多维度筛选 (朝代、主题、人物)
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import re


class EventTimeline:
    """事件时间线数据库"""
    
    def __init__(self, case_db_path: str = None):
        # 加载案例库
        if case_db_path is None:
            case_db_path = Path(__file__).parent.parent / "data" / "cases.json"
        
        self.case_db_path = case_db_path
        self.case_db = self._load_case_db()
        
        # 构建事件数据库
        self.events = self._build_event_database()
    
    def _load_case_db(self) -> Dict:
        """加载案例库"""
        if Path(self.case_db_path).exists():
            with open(self.case_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("⚠️ 案例库不存在")
        return {}
    
    def _build_event_database(self) -> List[Dict]:
        """从案例库构建事件数据库"""
        
        events = []
        
        for case_name, case_data in self.case_db.items():
            # 提取年份信息
            year_str = case_data.get('year', '')
            year_num = self._parse_year(year_str)
            
            event = {
                'id': case_name,
                'title': case_data.get('title', ''),
                'year': year_str,
                'year_num': year_num,
                'dynasty': case_data.get('dynasty', ''),
                'volume': case_data.get('volume', ''),
                'protagonists': case_data.get('protagonists', []),
                'outcome': self._determine_outcome(case_data.get('key_wisdom', '')),
                'category': self._categorize_event(case_name, case_data),
                'description': case_data.get('background', '')[:200] if case_data.get('background') else '',
                'wisdom': case_data.get('key_wisdom', '')[:100] if case_data.get('key_wisdom') else ''
            }
            
            events.append(event)
        
        # 按年份排序
        events.sort(key=lambda x: x['year_num'])
        
        return events
    
    def _parse_year(self, year_str: str) -> int:
        """解析年份字符串为数字"""
        
        if not year_str:
            return 0
        
        # 提取数字 (支持多种格式)
        patterns = [
            r'(\d+) 年',           # "208 年"
            r'前 (\d+)',          # "前 208"
            r'(\d+) 至 (\d+)',    # "208-209"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, year_str)
            if match:
                try:
                    return int(match.group(1))
                except:
                    pass
        
        # fallback: 返回 0
        return 0
    
    def _determine_outcome(self, wisdom: str) -> str:
        """根据智慧判断事件结果"""
        
        if not wisdom:
            return 'neutral'
        
        success_keywords = ['成功', '胜利', '成就', '崛起', '建立', '胜', '成']
        failure_keywords = ['失败', '败亡', '灭亡', '崩溃', '覆灭', '败', '亡']
        
        wisdom_lower = wisdom.lower()
        
        for kw in success_keywords:
            if kw in wisdom_lower:
                return 'success'
        
        for kw in failure_keywords:
            if kw in wisdom_lower:
                return 'failure'
        
        return 'neutral'
    
    def _categorize_event(self, case_name: str, case_data: Dict) -> str:
        """对事件进行分类"""
        
        title = case_name.lower()
        wisdom = case_data.get('key_wisdom', '').lower()
        
        # 定义分类关键词
        categories = {
            '战争': ['战', '攻', '伐', '征'],
            '政治': ['政', '令', '策', '改革'],
            '外交': ['盟', '交', '和', '聘'],
            '经济': ['财', '税', '农', '商'],
            '文化': ['文', '学', '礼', '教'],
            '军事': ['军', '兵', '将', '帅'],
        }
        
        for category, keywords in categories.items():
            if any(kw in (title + wisdom) for kw in keywords):
                return category
        
        return '其他'
    
    def get_events_by_period(self, start_year: int = None, end_year: int = None) -> List[Dict]:
        """获取指定时间段内的事件
        
        Args:
            start_year: 起始年份
            end_year: 结束年份
            
        Returns:
            List[Dict]: 事件列表
        """
        
        filtered = self.events
        
        if start_year is not None:
            filtered = [e for e in filtered if e['year_num'] >= start_year]
        
        if end_year is not None:
            filtered = [e for e in filtered if e['year_num'] <= end_year]
        
        return filtered
    
    def get_events_by_dynasty(self, dynasty: str) -> List[Dict]:
        """获取指定朝代的事件
        
        Args:
            dynasty: 朝代名称
            
        Returns:
            List[Dict]: 事件列表
        """
        
        return [e for e in self.events if dynasty.lower() in e['dynasty'].lower()]
    
    def get_events_by_category(self, category: str) -> List[Dict]:
        """获取指定类别的事件
        
        Args:
            category: 事件类别
            
        Returns:
            List[Dict]: 事件列表
        """
        
        return [e for e in self.events if e['category'] == category]
    
    def get_events_by_person(self, person_name: str) -> List[Dict]:
        """获取指定人物参与的事件
        
        Args:
            person_name: 人物名称
            
        Returns:
            List[Dict]: 事件列表
        """
        
        return [e for e in self.events if any(person_name.lower() in p.lower() 
                                               for p in e['protagonists'])]
    
    def get_timeline_summary(self) -> Dict:
        """获取时间线统计摘要
        
        Returns:
            Dict: 统计数据
        """
        
        summary = {
            'total_events': len(self.events),
            'dynasties_covered': list(set(e['dynasty'] for e in self.events)),
            'categories_count': {},
            'outcomes_count': {'success': 0, 'failure': 0, 'neutral': 0},
            'year_range': {
                'earliest': min((e['year_num'] for e in self.events if e['year_num'] > 0), default=0),
                'latest': max((e['year_num'] for e in self.events if e['year_num'] > 0), default=0)
            }
        }
        
        # 统计类别分布
        for event in self.events:
            category = event['category']
            summary['categories_count'][category] = summary['categories_count'].get(category, 0) + 1
        
        # 统计结果分布
        for event in self.events:
            outcome = event['outcome']
            summary['outcomes_count'][outcome] += 1
        
        return summary
    
    def generate_timeline_data(self, output_format: str = 'json') -> Dict:
        """生成时间线数据 (用于可视化)
        
        Args:
            output_format: 输出格式 ('json', 'csv', 'html')
            
        Returns:
            Dict: 时间线数据
        """
        
        timeline_data = {
            'title': '《资治通鉴》历史事件时间线',
            'description': '涵盖战国至宋朝的重要历史事件',
            'events': self.events,
            'summary': self.get_timeline_summary()
        }
        
        return timeline_data
    
    def export_to_csv(self, output_path: str = None):
        """导出为 CSV 格式
        
        Args:
            output_path: 输出文件路径
        """
        
        import csv
        
        if output_path is None:
            output_path = Path(__file__).parent.parent / "data" / "events_timeline.csv"
        
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'year', 'title', 'dynasty', 'category', 
                'protagonists', 'outcome', 'description'
            ])
            
            writer.writeheader()
            
            for event in self.events:
                writer.writerow({
                    'year': event['year'],
                    'title': event['title'],
                    'dynasty': event['dynasty'],
                    'category': event['category'],
                    'protagonists': ', '.join(event['protagonists']),
                    'outcome': event['outcome'],
                    'description': event['description'][:100]
                })
        
        print(f"✅ 时间线数据已导出到：{output_path}")


# 测试
if __name__ == "__main__":
    timeline = EventTimeline()
    
    print("=== 测试：事件时间线数据库 ===\n")
    
    # 1. 统计摘要
    print("--- 时间线统计 ---")
    summary = timeline.get_timeline_summary()
    
    print(f"总事件数：{summary['total_events']}")
    print(f"涵盖朝代：{', '.join(summary['dynasties_covered'][:5])}...")
    print(f"年份范围：{summary['year_range']['earliest']} - {summary['year_range']['latest']}")
    
    print("\n类别分布:")
    for category, count in summary['categories_count'].items():
        print(f"  - {category}: {count}个")
    
    # 2. 按朝代筛选
    print("\n--- 汉朝事件 (前 5 个) ---")
    han_events = timeline.get_events_by_dynasty('汉')
    
    for event in han_events[:5]:
        print(f"{event['year']}: {event['title']}")
    
    # 3. 按人物筛选
    print("\n--- 刘邦参与的事件 (前 5 个) ---")
    liu_events = timeline.get_events_by_person('刘邦')
    
    for event in liu_events[:5]:
        print(f"{event['year']}: {event['title']}")
