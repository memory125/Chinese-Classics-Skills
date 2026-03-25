#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 - 用户数据库
实现：SQLite 用户档案、行为日志、个性化配置
"""

import json
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

class UserDatabase:
    """用户 SQLite 数据库"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = str(Path(__file__).parent.parent / "user_data.db")
        
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_queries INTEGER DEFAULT 0,
                total_points INTEGER DEFAULT 0,
                preferences TEXT
            )
        ''')
        
        # 用户行为日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action_type TEXT,
                action_params TEXT,
                result_data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # 成就解锁表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                achievement_id TEXT,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                points INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # 用户偏好表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT,
                preference_key TEXT,
                preference_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id, preference_key)
            )
        ''')
        
        # 索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_actions_user_id ON user_actions(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_actions_timestamp ON user_actions(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id)')
        
        conn.commit()
        conn.close()
        
        print(f"✓ 用户数据库已初始化：{self.db_path}")
    
    def get_or_create_user(self, user_id: str) -> Dict:
        """获取或创建用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查用户是否存在
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            user = {
                'user_id': existing[0],
                'created_at': existing[1],
                'last_active': existing[2],
                'total_queries': existing[3],
                'total_points': existing[4],
                'preferences': existing[5]
            }
        else:
            # 创建新用户
            preferences = json.dumps({
                'focus_areas': [],
                'preferred_style': 'standard'
            })
            
            cursor.execute('''
                INSERT INTO users (user_id, preferences)
                VALUES (?, ?)
            ''', (user_id, preferences))
            
            user = {
                'user_id': user_id,
                'created_at': datetime.now().isoformat(),
                'last_active': datetime.now().isoformat(),
                'total_queries': 0,
                'total_points': 0,
                'preferences': json.dumps({
                    'focus_areas': [],
                    'preferred_style': 'standard'
                })
            }
        
        # 更新最后活跃时间
        cursor.execute('''
            UPDATE users SET last_active = ? WHERE user_id = ?
        ''', (datetime.now().isoformat(), user_id))
        
        conn.commit()
        conn.close()
        
        return user
    
    def record_action(self, user_id: str, action_type: str, action_params: Dict = None, 
                     result_data: Dict = None) -> int:
        """记录用户行为"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_actions (user_id, action_type, action_params, result_data)
            VALUES (?, ?, ?, ?)
        ''', (user_id, action_type, 
              json.dumps(action_params or {}),
              json.dumps(result_data or {})))
        
        action_id = cursor.lastrowid
        
        # 更新用户统计
        cursor.execute('''
            UPDATE users SET total_queries = total_queries + 1, last_active = ?
            WHERE user_id = ?
        ''', (datetime.now().isoformat(), user_id))
        
        conn.commit()
        conn.close()
        
        return action_id
    
    def get_user_actions(self, user_id: str, action_type: str = None, 
                        days: int = 30) -> List[Dict]:
        """获取用户行为历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, user_id, action_type, action_params, result_data, timestamp
            FROM user_actions
            WHERE user_id = ?
        '''
        params = [user_id]
        
        if action_type:
            query += ' AND action_type = ?'
            params.append(action_type)
        
        # 时间过滤
        date_limit = (datetime.now() - timedelta(days=days)).isoformat()
        query += ' AND timestamp >= ?'
        params.append(date_limit)
        
        query += ' ORDER BY timestamp DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        actions = []
        for row in rows:
            actions.append({
                'id': row[0],
                'user_id': row[1],
                'action_type': row[2],
                'action_params': json.loads(row[3]),
                'result_data': json.loads(row[4]),
                'timestamp': row[5]
            })
        
        return actions
    
    def unlock_achievement(self, user_id: str, achievement_id: str, points: int) -> bool:
        """解锁成就"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已解锁
        cursor.execute('''
            SELECT id FROM user_achievements
            WHERE user_id = ? AND achievement_id = ?
        ''', (user_id, achievement_id))
        
        if cursor.fetchone():
            conn.close()
            return False
        
        # 解锁成就
        cursor.execute('''
            INSERT INTO user_achievements (user_id, achievement_id, points)
            VALUES (?, ?, ?)
        ''', (user_id, achievement_id, points))
        
        # 更新用户积分
        cursor.execute('''
            UPDATE users SET total_points = total_points + ? WHERE user_id = ?
        ''', (points, user_id))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_user_achievements(self, user_id: str) -> List[Dict]:
        """获取用户成就"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT achievement_id, unlocked_at, points
            FROM user_achievements
            WHERE user_id = ?
            ORDER BY unlocked_at DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        achievements = []
        for row in rows:
            achievements.append({
                'achievement_id': row[0],
                'unlocked_at': row[1],
                'points': row[2]
            })
        
        return achievements
    
    def get_user_preferences(self, user_id: str, key: str = None) -> Dict:
        """获取用户偏好"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if key:
            cursor.execute('''
                SELECT preference_value FROM user_preferences
                WHERE user_id = ? AND preference_key = ?
            ''', (user_id, key))
            
            row = cursor.fetchone()
            conn.close()
            
            return json.loads(row[0]) if row else {}
        
        cursor.execute('''
            SELECT preference_key, preference_value FROM user_preferences
            WHERE user_id = ?
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        preferences = {}
        for row in rows:
            preferences[row[0]] = json.loads(row[1])
        
        return preferences
    
    def set_user_preference(self, user_id: str, key: str, value: Dict):
        """设置用户偏好"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (user_id, preference_key, preference_value)
            VALUES (?, ?, ?)
        ''', (user_id, key, json.dumps(value)))
        
        conn.commit()
        conn.close()
    
    def get_weekly_statistics(self, user_id: str) -> Dict:
        """获取周度统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        week_start = (datetime.now() - timedelta(days=7)).isoformat()
        
        # 查询本周数据
        cursor.execute('''
            SELECT COUNT(*), 
                   COUNT(DISTINCT action_type),
                   SUM(CASE WHEN action_type = 'query' THEN 1 ELSE 0 END)
            FROM user_actions
            WHERE user_id = ? AND timestamp >= ?
        ''', (user_id, week_start))
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total_actions': row[0] or 0,
            'unique_actions': row[1] or 0,
            'queries': row[2] or 0
        }
    
    def get_user_statistics(self, user_id: str) -> Dict:
        """获取用户统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        achievements = self.get_user_achievements(user_id)
        
        return {
            'user_id': row[0],
            'created_at': row[1],
            'last_active': row[2],
            'total_queries': row[3],
            'total_points': row[4],
            'achievements_count': len(achievements),
            'total_achievement_points': sum(a['points'] for a in achievements),
            'preferences': json.loads(row[5]) if row[5] else {}
        }


# 测试
if __name__ == "__main__":
    db = UserDatabase()
    user_id = "test_user_001"
    
    print("=" * 60)
    print("测试：获取/创建用户")
    print("=" * 60)
    user = db.get_or_create_user(user_id)
    print(json.dumps(user, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("测试：记录行为")
    print("=" * 60)
    for i in range(5):
        action_id = db.record_action(user_id, "query", 
                                     {"query": "鸿门宴"},
                                     {"result": "找到 1 个案例"})
        print(f"✓ 记录动作 #{i+1}: ID={action_id}")
    
    print("\n" + "=" * 60)
    print("测试：用户统计")
    print("=" * 60)
    stats = db.get_user_statistics(user_id)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("测试：解锁成就")
    print("=" * 60)
    result = db.unlock_achievement(user_id, "hongmen_expert", 50)
    print(f"成就解锁结果：{result}")
    
    print("\n" + "=" * 60)
    print("测试：周度统计")
    print("=" * 60)
    weekly = db.get_weekly_statistics(user_id)
    print(json.dumps(weekly, indent=2))
