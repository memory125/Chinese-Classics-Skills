#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日锦囊盲盒 - 每日推送历史智慧

功能：
1. 案例随机选择器 (从案例库中)
2. 每日更新逻辑 (基于日期)
3. 智能推荐系统 (根据用户偏好)
4. 推送通知系统 (可选)
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime, timedelta
import random


class DailyWisdom:
    """今日锦囊盲盒"""
    
    def __init__(self, case_db_path: str = None):
        # 加载案例库
        if case_db_path is None:
            case_db_path = Path(__file__).parent.parent / "data" / "cases.json"
        
        self.case_db_path = case_db_path
        self.case_db = self._load_case_db()
        
        # 用户偏好 (可扩展)
        self.user_preferences = {
            'preferred_topics': [],  # 偏好的主题
            'avoided_topics': [],    # 避免的主题
            'reading_frequency': 'daily'  # daily, weekly, monthly
        }
    
    def _load_case_db(self) -> Dict:
        """加载案例库"""
        if self.case_db_path.exists():
            with open(self.case_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("⚠️ 案例库不存在")
        return {}
    
    def get_daily_wisdom(self, date: Optional[datetime] = None) -> Dict:
        """获取指定日期的锦囊
        
        Args:
            date: 指定日期，如果为 None 则使用今天
            
        Returns:
            Dict: 今日锦囊内容
        """
        if date is None:
            date = datetime.now()
        
        # 生成基于日期的随机种子 (确保同一天返回相同结果)
        seed_date = date.strftime('%Y-%m-%d')
        random.seed(hash(seed_date))
        
        # 从案例库中随机选择一个案例
        cases = list(self.case_db.keys())
        
        if not cases:
            return {'error': '案例库为空'}
        
        # 根据用户偏好过滤 (如果设置了偏好)
        filtered_cases = self._filter_by_preferences(cases)
        
        # 如果没有符合条件的，使用全部案例
        if not filtered_cases:
            filtered_cases = cases
        
        # 随机选择一个
        selected_case_name = random.choice(filtered_cases)
        case_data = self.case_db[selected_case_name]
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'case_name': selected_case_name,
            'title': case_data.get('title', ''),
            'key_wisdom': case_data.get('key_wisdom', ''),
            'modern_applications': case_data.get('modern_applications', []),
            'volume': case_data.get('volume', ''),
            'year': case_data.get('year', '')
        }
    
    def _filter_by_preferences(self, cases: List[str]) -> List[str]:
        """根据用户偏好过滤案例"""
        
        if not self.user_preferences['preferred_topics']:
            return cases
        
        filtered = []
        for case_name in cases:
            case_data = self.case_db.get(case_name, {})
            
            # 检查是否包含偏好的主题关键词
            title = case_data.get('title', '').lower()
            wisdom = case_data.get('key_wisdom', '').lower()
            all_text = f"{title} {wisdom}"
            
            for topic in self.user_preferences['preferred_topics']:
                if topic.lower() in all_text:
                    filtered.append(case_name)
                    break
        
        return filtered
    
    def get_weekly_summary(self, start_date: Optional[datetime] = None) -> List[Dict]:
        """获取一周的锦囊汇总
        
        Args:
            start_date: 起始日期，如果为 None 则使用今天
            
        Returns:
            List[Dict]: 一周的锦囊列表
        """
        if start_date is None:
            start_date = datetime.now()
        
        weekly_wisdoms = []
        
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            wisdom = self.get_daily_wisdom(current_date)
            
            # 避免重复 (同一天可能生成相同结果，但不同天应该不同)
            if wisdom not in weekly_wisdoms:
                weekly_wisdoms.append(wisdom)
        
        return weekly_wisdoms
    
    def get_monthly_highlights(self, year: int = None, month: int = None) -> List[Dict]:
        """获取月度精华锦囊
        
        Args:
            year: 年份，如果为 None 则使用今年
            month: 月份，如果为 None 则使用本月
            
        Returns:
            List[Dict]: 月度精华列表 (精选前 10 个)
        """
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        # 获取该月所有日期的锦囊
        monthly_wisdoms = []
        
        for day in range(1, 32):  # 最多 31 天
            try:
                date = datetime(year, month, day)
                wisdom = self.get_daily_wisdom(date)
                
                if 'error' not in wisdom:
                    monthly_wisdoms.append(wisdom)
            except ValueError:
                # 跳过无效日期 (如 2 月 30 日)
                continue
        
        # 去重并限制数量
        unique_wisdoms = []
        seen_names = set()
        
        for wisdom in monthly_wisdoms:
            if wisdom['case_name'] not in seen_names:
                unique_wisdoms.append(wisdom)
                seen_names.add(wisdom['case_name'])
                
                if len(unique_wisdoms) >= 10:  # 最多返回 10 个
                    break
        
        return unique_wisdoms
    
    def set_preference(self, preference_type: str, value):
        """设置用户偏好
        
        Args:
            preference_type: 偏好类型 ('preferred_topics', 'avoided_topics', 'reading_frequency')
            value: 偏好值
        """
        if preference_type in self.user_preferences:
            self.user_preferences[preference_type] = value
    
    def get_recommendation(self, topic: str) -> Dict:
        """根据主题推荐锦囊
        
        Args:
            topic: 主题关键词
            
        Returns:
            Dict: 推荐的锦囊
        """
        # 搜索包含该主题的案例
        matching_cases = []
        
        for case_name, case_data in self.case_db.items():
            title = case_data.get('title', '').lower()
            wisdom = case_data.get('key_wisdom', '').lower()
            
            if topic.lower() in title or topic.lower() in wisdom:
                matching_cases.append(case_data)
        
        # 随机选择一个
        if matching_cases:
            selected = random.choice(matching_cases)
            return {
                'type': 'recommendation',
                'topic': topic,
                'case_name': next((k for k, v in self.case_db.items() if v == selected), ''),
                **selected
            }
        
        # 如果没有匹配的，返回随机锦囊
        return self.get_daily_wisdom()


# 测试
if __name__ == "__main__":
    daily = DailyWisdom()
    
    print("=== 测试：今日锦囊盲盒 ===\n")
    
    # 1. 今日锦囊
    print("--- 今日锦囊 ---")
    today_wisdom = daily.get_daily_wisdom()
    
    if 'error' not in today_wisdom:
        print(f"日期：{today_wisdom['date']}")
        print(f"案例：{today_wisdom['case_name']}")
        print(f"标题：{today_wisdom['title']}")
        print(f"\n核心智慧:")
        print(f"{today_wisdom['key_wisdom'][:100]}...")
        
        if today_wisdom.get('modern_applications'):
            print("\n现代应用:")
            for app in today_wisdom['modern_applications'][:2]:
                print(f"  - {app.get('scenario', '')}: {app.get('action', '')}")
    
    # 2. 本周汇总
    print("\n--- 本周汇总 (前 3 天) ---")
    weekly = daily.get_weekly_summary()
    
    for i, wisdom in enumerate(weekly[:3], 1):
        if 'error' not in wisdom:
            print(f"{i}. {wisdom['date']}: {wisdom['case_name']}")
    
    # 3. 主题推荐
    print("\n--- 主题推荐：如虎添翼 ---")
    recommendation = daily.get_recommendation('如虎添翼')
    
    if 'error' not in recommendation:
        print(f"推荐案例：{recommendation['case_name']}")
        print(f"标题：{recommendation['title'][:50]}...")
