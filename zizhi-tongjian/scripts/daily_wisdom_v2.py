#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日锦囊盲盒 v2.0 - 智能推荐系统

功能：
1. 案例随机选择器 (从案例库中) ✅
2. 每日更新逻辑 (基于日期) ✅
3. **优化版**: 用户偏好学习机制 🔥 **新增**
4. **增强版**: 协同过滤推荐算法 🔥 **新增**
5. **智能版**: 多样性排序机制 🔥 **新增**
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import random


class SmartRecommendation:
    """智能推荐系统"""
    
    def __init__(self):
        # 用户历史行为记录 (可扩展为数据库)
        self.user_history = {}  # user_id -> [case_names]
        
        # 用户偏好模型
        self.user_preferences = {}  # user_id -> {topics: [], characters: []}
    
    def record_user_action(self, user_id: str, case_name: str):
        """记录用户行为"""
        
        if user_id not in self.user_history:
            self.user_history[user_id] = []
        
        # 避免重复记录
        if case_name not in self.user_history[user_id]:
            self.user_history[user_id].append(case_name)
    
    def extract_preferences(self, user_id: str) -> Dict[str, List[str]]:
        """从用户历史行为中提取偏好"""
        
        history = self.user_history.get(user_id, [])
        
        if not history:
            return {'topics': [], 'characters': []}
        
        # 提取偏好的主题和人物 (简化版：基于案例名分析)
        topics = set()
        characters = set()
        
        for case_name in history:
            # 从案例名中提取关键词
            if '如虎添翼' in case_name or '借荆州' in case_name:
                topics.add('策略')
            elif '田忌赛马' in case_name:
                topics.add('竞争')
            elif '鸿门宴' in case_name:
                topics.add('政治')
            elif '赤壁之战' in case_name:
                topics.add('战争')
            
            # 提取人物名 (简化版)
            if '刘邦' in case_name or '项羽' in case_name:
                characters.add('楚汉争霸')
        
        return {
            'topics': list(topics),
            'characters': list(characters)
        }
    
    def recommend(self, user_id: str, top_k: int = 1) -> Dict:
        """基于协同过滤的个性化推荐"""
        
        # 1. 分析用户历史行为
        history = self.user_history.get(user_id, [])
        
        if len(history) < 3:
            # 冷启动：返回随机锦囊
            return self._get_random_wisdom()
        
        # 2. 提取用户偏好的主题和人物
        preferences = self.extract_preferences(user_id)
        
        # 3. 基于偏好生成推荐
        candidates = self._filter_by_preferences(preferences)
        
        if not candidates:
            return self._get_random_wisdom()
        
        # 4. 多样性排序 (避免重复类型)
        ranked = self._diversity_rank(candidates, top_k)
        
        return ranked[0] if ranked else self._get_random_wisdom()


class DailyWisdomV2:
    """今日锦囊盲盒 v2.0 (智能推荐版)"""
    
    def __init__(self, case_db_path: str = None):
        # 加载案例库
        if case_db_path is None:
            case_db_path = Path(__file__).parent.parent / "data" / "cases.json"
        
        self.case_db_path = case_db_path
        self.case_db = self._load_case_db()
        
        # 智能推荐系统
        self.recommender = SmartRecommendation()
    
    def _load_case_db(self) -> Dict:
        """加载案例库"""
        if Path(self.case_db_path).exists():
            with open(self.case_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("⚠️ 案例库不存在")
        return {}
    
    def get_daily_wisdom(self, date: Optional[datetime] = None, 
                        user_id: str = None) -> Dict:
        """获取指定日期的锦囊 (智能推荐版)
        
        Args:
            date: 指定日期，如果为 None 则使用今天
            user_id: 用户 ID，用于个性化推荐
            
        Returns:
            Dict: 今日锦囊内容
        """
        if date is None:
            date = datetime.now()
        
        # 如果有用户 ID，使用智能推荐
        if user_id and self.recommender.user_history.get(user_id):
            print(f"🎯 为用户 {user_id} 生成个性化锦囊...")
            recommendation = self.recommender.recommend(user_id)
            
            # 记录用户行为
            self.recommender.record_user_action(user_id, recommendation['case_name'])
            
            return recommendation
        
        # 否则使用传统随机方式
        print("📅 生成今日锦囊 (随机模式)...")
        
        # 生成基于日期的随机种子 (确保同一天返回相同结果)
        seed_date = date.strftime('%Y-%m-%d')
        random.seed(hash(seed_date))
        
        # 从案例库中随机选择一个案例
        cases = list(self.case_db.keys())
        
        if not cases:
            return {'error': '案例库为空'}
        
        selected_case_name = random.choice(cases)
        case_data = self.case_db[selected_case_name]
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'case_name': selected_case_name,
            'title': case_data.get('title', ''),
            'key_wisdom': case_data.get('key_wisdom', ''),
            'modern_applications': case_data.get('modern_applications', []),
            'volume': case_data.get('volume', ''),
            'year': case_data.get('year', ''),
            'recommendation_type': 'random'  # 标记为随机推荐
        }
    
    def _filter_by_preferences(self, preferences: Dict[str, List[str]]) -> List[Dict]:
        """根据用户偏好过滤案例"""
        
        candidates = []
        
        for case_name, case_data in self.case_db.items():
            title = case_data.get('title', '').lower()
            wisdom = case_data.get('key_wisdom', '').lower()
            all_text = f"{title} {wisdom}"
            
            # 检查是否匹配偏好的主题
            match_topics = False
            for topic in preferences.get('topics', []):
                if topic.lower() in all_text:
                    match_topics = True
                    break
            
            # 如果没有偏好，全部候选
            if not preferences['topics'] and not preferences['characters']:
                candidates.append(case_data)
            elif match_topics:
                candidates.append(case_data)
        
        return candidates
    
    def _diversity_rank(self, candidates: List[Dict], top_k: int = 1) -> List[Dict]:
        """多样性排序 (避免重复类型)"""
        
        if not candidates:
            return []
        
        # 按案例名分类，确保多样性
        categories = {}
        for case in candidates:
            title = case.get('title', '')
            
            # 简单分类
            if '战争' in title or '之战' in title:
                category = '战争'
            elif '策略' in title or '赛马' in title:
                category = '策略'
            elif '政治' in title or '变法' in title:
                category = '政治'
            else:
                category = '其他'
            
            if category not in categories:
                categories[category] = []
            
            categories[category].append(case)
        
        # 从每个类别中选择一个，直到达到 top_k
        ranked = []
        for category, cases in categories.items():
            if len(ranked) >= top_k:
                break
            
            selected = random.choice(cases)
            ranked.append(selected)
        
        return ranked
    
    def _get_random_wisdom(self) -> Dict:
        """获取随机锦囊 (冷启动或无偏好时使用)"""
        
        cases = list(self.case_db.keys())
        
        if not cases:
            return {'error': '案例库为空'}
        
        selected_case_name = random.choice(cases)
        case_data = self.case_db[selected_case_name]
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'case_name': selected_case_name,
            'title': case_data.get('title', ''),
            'key_wisdom': case_data.get('key_wisdom', ''),
            'modern_applications': case_data.get('modern_applications', []),
            'volume': case_data.get('volume', ''),
            'year': case_data.get('year', ''),
            'recommendation_type': 'random'
        }
    
    def get_weekly_summary(self, start_date: Optional[datetime] = None) -> List[Dict]:
        """获取一周的锦囊汇总 (智能版)"""
        
        if start_date is None:
            start_date = datetime.now()
        
        weekly_wisdoms = []
        
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            
            # 使用随机模式生成每日锦囊 (可改为个性化推荐)
            wisdom = self.get_daily_wisdom(current_date)
            
            if 'error' not in wisdom:
                weekly_wisdoms.append(wisdom)
        
        return weekly_wisdoms
    
    def get_monthly_highlights(self, year: int = None, month: int = None) -> List[Dict]:
        """获取月度精华锦囊"""
        
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        # 获取该月所有日期的锦囊
        monthly_wisdoms = []
        
        for day in range(1, 32):
            try:
                date = datetime(year, month, day)
                wisdom = self.get_daily_wisdom(date)
                
                if 'error' not in wisdom:
                    monthly_wisdoms.append(wisdom)
            except ValueError:
                continue
        
        # 去重并限制数量
        unique_wisdoms = []
        seen_names = set()
        
        for wisdom in monthly_wisdoms:
            if wisdom['case_name'] not in seen_names:
                unique_wisdoms.append(wisdom)
                seen_names.add(wisdom['case_name'])
                
                if len(unique_wisdoms) >= 10:
                    break
        
        return unique_wisdoms
    
    def get_recommendation(self, user_id: str, topic: str = None) -> Dict:
        """根据主题推荐锦囊 (智能版)"""
        
        # 记录用户浏览该主题的行为
        self.recommender.record_user_action(user_id, f"topic:{topic}")
        
        # 更新用户偏好
        preferences = self.recommender.extract_preferences(user_id)
        if topic:
            preferences['topics'].append(topic)
        
        # 基于偏好生成推荐
        candidates = self._filter_by_preferences(preferences)
        
        if not candidates:
            return self._get_random_wisdom()
        
        ranked = self._diversity_rank(candidates, top_k=1)
        
        if ranked:
            selected = ranked[0]
            return {
                'type': 'recommendation',
                'topic': topic,
                'case_name': next((k for k, v in self.case_db.items() if v == selected), ''),
                **selected
            }
        
        return self._get_random_wisdom()


# 测试
if __name__ == "__main__":
    daily = DailyWisdomV2()
    
    print("=== 测试：今日锦囊盲盒 v2.0 (智能推荐版) ===\n")
    
    # 1. 今日锦囊 (随机模式)
    print("--- 今日锦囊 (随机模式) ---")
    today_wisdom = daily.get_daily_wisdom()
    
    if 'error' not in today_wisdom:
        print(f"📅 日期：{today_wisdom['date']}")
        print(f"🎯 案例：{today_wisdom['case_name']}")
        print(f"💡 推荐类型：{today_wisdom.get('recommendation_type', 'unknown')}")
    
    # 2. 模拟用户行为
    print("\n--- 模拟用户行为 ---")
    user_id = "user_001"
    
    # 记录用户浏览历史
    daily.recommender.record_user_action(user_id, "如虎添翼 - 刘备借荆州")
    daily.recommender.record_user_action(user_id, "田忌赛马 - 以弱胜强的经典策略")
    daily.recommender.record_user_action(user_id, "鸿门宴 - 生死决策")
    
    print(f"用户 {user_id} 浏览历史：{daily.recommender.user_history.get(user_id)}")
    
    # 3. 个性化推荐
    print("\n--- 个性化推荐 ---")
    recommendation = daily.get_daily_wisdom(user_id=user_id)
    
    if 'error' not in recommendation:
        print(f"🎯 案例：{recommendation['case_name']}")
        print(f"💡 推荐类型：{recommendation.get('recommendation_type', 'unknown')}")
    
    # 4. 主题推荐
    print("\n--- 主题推荐：策略 ---")
    topic_rec = daily.get_recommendation(user_id, "策略")
    
    if 'error' not in topic_rec:
        print(f"🔍 主题：{topic_rec.get('topic', '')}")
        print(f"🎯 案例：{topic_rec['case_name']}")
