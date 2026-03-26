#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户个性化推荐系统

核心功能：
1. 记录用户阅读历史
2. 分析用户偏好（情感、主题、章节类型）
3. 智能生成每日推荐
4. 避免重复推荐
5. 基于历史行为优化推荐质量
"""

import random
from typing import Dict, List, Optional, Set
from datetime import datetime


class PersonalRecommendationEngine:
    """个性化推荐引擎"""
    
    def __init__(self):
        # 用户历史记录（userId -> {chapter_num: timestamp}）
        self.user_history = {}
        
        # 章节主题分类
        self.chapter_themes = {
            # 智慧类（1-20章）
            'wisdom': list(range(1, 21)),
            
            # 修身类（21-40章）
            'cultivation': list(range(21, 41)),
            
            # 治国类（41-60章）
            'governance': list(range(41, 61)),
            
            # 处世类（61-81章）
            'life_skills': list(range(61, 82))
        }
        
        # 章节情感倾向
        self.chapter_emotions = {
            'calm': [1, 8, 10, 16, 25, 37, 45, 59, 66],  # 平静类
            'gentle': [7, 22, 28, 43, 76, 78],            # 柔和类
            'deep': [1, 40, 42, 51, 56],                  # 深邃类
            'practical': [2, 9, 13, 20, 33, 44, 67]       # 实用类
        }
        
        # 用户偏好权重（userId -> {theme: weight, emotion: weight}）
        self.user_preferences = {}
    
    def record_reading(self, user_id: str, chapter_num: int) -> None:
        """记录用户的阅读历史"""
        
        if user_id not in self.user_history:
            self.user_history[user_id] = {}
        
        # 添加阅读记录（timestamp）
        self.user_history[user_id][chapter_num] = datetime.now()
        
        # 更新偏好权重
        self._update_preferences(user_id, chapter_num)
    
    def _update_preferences(self, user_id: str, chapter_num: int) -> None:
        """根据阅读历史更新用户偏好"""
        
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'theme_weights': {},
                'emotion_weights': {}
            }
        
        prefs = self.user_preferences[user_id]
        
        # 分析章节主题并增加权重
        for theme, chapters in self.chapter_themes.items():
            if chapter_num in chapters:
                current_weight = prefs['theme_weights'].get(theme, 0)
                prefs['theme_weights'][theme] = current_weight + 1
        
        # 分析情感倾向并增加权重
        for emotion, chapters in self.chapter_emotions.items():
            if chapter_num in chapters:
                current_weight = prefs['emotion_weights'].get(emotion, 0)
                prefs['emotion_weights'][emotional] = current_weight + 1
    
    def get_daily_recommendation(self, user_id: str = 'default', 
                                  exclude_chapters: Optional[Set[int]] = None) -> int:
        """获取每日推荐章节 - 智能算法"""
        
        # 初始化排除列表
        if exclude_chapters is None:
            exclude_chapters = set()
        
        # 1. 检查用户历史，避免重复推荐今天的内容
        today_key = datetime.now().strftime('%Y-%m-%d')
        recent_reads = self._get_recent_readings(user_id, days=7)
        exclude_chapters.update(recent_reads)
        
        # 2. 获取所有未读章节（排除已读的）
        all_chapters = set(range(1, 82))
        unread_chapters = list(all_chapters - exclude_chapters)
        
        if not unread_chapters:
            # 如果所有章节都读过，随机选择一个重新推荐
            return random.randint(1, 81)
        
        # 3. 根据用户偏好加权选择（如果有历史数据）
        prefs = self.user_preferences.get(user_id)
        
        if prefs and any(prefs['theme_weights'].values()):
            # 有足够历史数据，使用个性化推荐算法
            return self._personalized_recommendation(user_id, unread_chapters)
        else:
            # 新用户或数据不足，使用基础推荐
            return self._basic_recommendation(unread_chapters)
    
    def _get_recent_readings(self, user_id: str, days: int = 7) -> Set[int]:
        """获取最近 N 天的阅读记录"""
        
        if user_id not in self.user_history:
            return set()
        
        recent_chapters = set()
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for chapter_num, timestamp in self.user_history[user_id].items():
            if (cutoff_date - timestamp).days <= days:
                recent_chapters.add(chapter_num)
        
        return recent_chapters
    
    def _personalized_recommendation(self, user_id: str, unread_chapters: List[int]) -> int:
        """个性化推荐算法"""
        
        prefs = self.user_preferences[user_id]
        
        # 1. 计算每个章节的推荐分数
        chapter_scores = {}
        
        for chapter_num in unread_chapters:
            score = 0
            
            # 2. 主题匹配加分（根据用户偏好）
            theme_weights = prefs['theme_weights']
            if theme_weights:
                max_theme_weight = max(theme_weights.values())
                for theme, chapters in self.chapter_themes.items():
                    if chapter_num in chapters and theme_weights.get(theme, 0) > 0:
                        score += (theme_weights[theme] / max_theme_weight) * 3
            
            # 3. 情感匹配加分
            emotion_weights = prefs['emotion_weights']
            if emotion_weights:
                max_emotion_weight = max(emotion_weights.values())
                for emotion, chapters in self.chapter_emotions.items():
                    if chapter_num in chapters and emotion_weights.get(emotion, 0) > 0:
                        score += (emotion_weights[emotion] / max_emotion_weight) * 2
            
            # 4. 章节难度梯度（从简单到深入）
            difficulty_bonus = self._calculate_difficulty_score(chapter_num)
            score += difficulty_bonus
            
            chapter_scores[chapter_num] = score
        
        # 5. 根据分数随机选择（高分优先，但不是绝对）
        import numpy as np
        chapters = list(chapter_scores.keys())
        scores = [chapter_scores[c] for c in chapters]
        
        if sum(scores) > 0:
            probabilities = np.array(scores) / sum(scores)
            recommended_chapter = int(np.random.choice(chapters, p=probabilities))
        else:
            # 如果分数都为 0，随机选择
            recommended_chapter = random.choice(chapters)
        
        return recommended_chapter
    
    def _basic_recommendation(self, unread_chapters: List[int]) -> int:
        """基础推荐算法（新用户或数据不足）"""
        
        # 1. 优先推荐核心章节（前 20 章）
        core_chapters = [c for c in unread_chapters if c <= 20]
        
        if core_chapters:
            return random.choice(core_chapters)
        
        # 2. 其次推荐平静类章节（适合初学者）
        calm_chapters = []
        for emotion, chapters in self.chapter_emotions.items():
            if emotion == 'calm':
                calm_chapters.extend([c for c in unread_chapters if c in chapters])
        
        if calm_chapters:
            return random.choice(calm_chapters)
        
        # 3. 最后随机选择
        return random.choice(unread_chapters)
    
    def _calculate_difficulty_score(self, chapter_num: int) -> float:
        """计算章节难度分数（0-1）"""
        
        # 简单章节（前 20 章）：0.8-1.0
        if chapter_num <= 20:
            return 0.9
        
        # 中等章节（21-50 章）：0.5-0.7
        elif chapter_num <= 50:
            return 0.6
        
        # 困难章节（51-81 章）：0.3-0.4
        else:
            return 0.35
    
    def get_user_insights(self, user_id: str) -> Dict:
        """获取用户阅读洞察"""
        
        if user_id not in self.user_history:
            return {
                'total_read': 0,
                'favorite_themes': [],
                'reading_patterns': {},
                'recommendation_suggestion': "你还没有开始阅读，建议从第 1 章（道可道）或第 8 章（上善若水）开始。"
            }
        
        history = self.user_history[user_id]
        prefs = self.user_preferences.get(user_id, {})
        
        # 统计已读章节数
        total_read = len(history)
        
        # 分析主题偏好
        theme_weights = prefs.get('theme_weights', {})
        favorite_themes = sorted(theme_weights.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # 分析阅读模式
        reading_patterns = {
            'most_read_chapter': max(history.keys(), key=lambda k: history[k]) if history else None,
            'reading_frequency': len(history) / (datetime.now().day),  # 平均每天读多少章
        }
        
        # 生成推荐建议
        if total_read < 5:
            suggestion = "你刚开始阅读，建议从第 1 章（道可道）或第 8 章（上善若水）开始。"
        elif 'wisdom' in [t[0] for t in favorite_themes]:
            suggestion = "你喜欢智慧类章节，可以试试第 40 章（反者道之动）或第 51 章（玄德）。"
        elif 'cultivation' in [t[0] for t in favorite_themes]:
            suggestion = "你关注修身养性，建议读第 37 章（无为而治）或第 64 章（慎终如始）。"
        else:
            suggestion = f"根据你的阅读历史，推荐尝试未读的{random.choice(list(self.chapter_themes.values()))}中的章节。"
        
        return {
            'total_read': total_read,
            'favorite_themes': [t[0] for t in favorite_themes],
            'reading_patterns': reading_patterns,
            'recommendation_suggestion': suggestion
        }
    
    def reset_user_data(self, user_id: str) -> None:
        """重置用户数据"""
        
        if user_id in self.user_history:
            del self.user_history[user_id]
        if user_id in self.user_preferences:
            del self.user_preferences[user_id]


# 测试代码
if __name__ == "__main__":
    engine = PersonalRecommendationEngine()
    
    # 模拟用户阅读历史
    test_user = "test_user_001"
    
    print("=== 个性化推荐系统测试 ===\n")
    
    # 第 1 次：新用户，基础推荐
    chapter_1 = engine.get_daily_recommendation(test_user)
    print(f"第 1 次推荐（新用户）: 第{chapter_1}章")
    engine.record_reading(test_user, chapter_1)
    
    # 模拟阅读几章后再次推荐
    for i in range(3):
        next_chapter = random.randint(1, 20)  # 模拟用户读了前 20 章中的某几章
        print(f"用户读了第{next_chapter}章")
        engine.record_reading(test_user, next_chapter)
    
    # 第 2 次：有历史数据，个性化推荐
    chapter_2 = engine.get_daily_recommendation(test_user)
    print(f"\n第 2 次推荐（有历史）: 第{chapter_2}章")
    engine.record_reading(test_user, chapter_2)
    
    # 获取用户洞察
    insights = engine.get_user_insights(test_user)
    print("\n=== 用户阅读洞察 ===")
    for key, value in insights.items():
        print(f"{key}: {value}")
