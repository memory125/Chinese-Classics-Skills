#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理器 - 用户系统核心

功能：
1. SQLite 表结构设计 (users/preferences/history/logs)
2. 数据持久化层封装
3. 批量导入/导出工具
4. 性能优化 (索引 + 缓存)
"""

import sqlite3
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import json


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = None):
        """初始化数据库
        
        Args:
            db_path: 数据库文件路径，默认 data/zizhi_tongjian.db
        """
        
        if db_path is None:
            base_dir = Path(__file__).parent.parent / "data"
            self.db_path = str(base_dir / "zizhi_tongjian.db")
        else:
            self.db_path = db_path
        
        # 创建目录
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 连接数据库
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # 创建表结构
        self._create_tables()
        
        # 创建索引 (性能优化)
        self._create_indexes()
        
        print(f"✅ 数据库已初始化：{self.db_path}")
    
    def _create_tables(self):
        """创建数据表"""
        
        cursor = self.conn.cursor()
        
        # 1. 用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                role TEXT DEFAULT 'user'
            )
        """)
        
        # 2. 用户偏好表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                preferred_topics TEXT,
                favorite_characters TEXT,
                reading_frequency TEXT DEFAULT 'daily',
                notification_enabled BOOLEAN DEFAULT 1,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # 3. 用户历史行为表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action_type TEXT NOT NULL,
                query_text TEXT,
                result_count INTEGER DEFAULT 0,
                duration_ms REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # 4. API 访问日志表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                status_code INTEGER,
                request_time REAL,
                ip_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        
        # 5. 用户收藏表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                case_name TEXT NOT NULL,
                bookmarked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # 6. 用户学习进度表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                case_name TEXT NOT NULL,
                read_count INTEGER DEFAULT 1,
                last_read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        self.conn.commit()
        print("✅ 数据表创建完成 (6 个表)")
    
    def _create_indexes(self):
        """创建索引 (性能优化)"""
        
        cursor = self.conn.cursor()
        
        # 用户相关索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username 
            ON users(username)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email 
            ON users(email)
        """)
        
        # 历史行为索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_user_id 
            ON user_history(user_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_action_type 
            ON user_history(action_type)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_created_at 
            ON user_history(created_at)
        """)
        
        # API 日志索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_api_logs_endpoint 
            ON api_logs(endpoint)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_api_logs_user_id 
            ON api_logs(user_id)
        """)
        
        # 收藏表索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bookmarks_user_id 
            ON user_bookmarks(user_id)
        """)
        
        self.conn.commit()
        print("✅ 索引创建完成 (8 个索引)")
    
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> Dict:
        """创建用户
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码 (明文)
            role: 角色 (user/admin)
            
        Returns:
            Dict: 用户信息或错误信息
        """
        
        from passlib.hash import bcrypt
        
        try:
            # 密码加密
            password_hash = bcrypt.hash(password)
            
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, role)
            )
            self.conn.commit()
            
            user_id = cursor.lastrowid
            
            # 创建用户偏好记录
            cursor.execute(
                "INSERT INTO user_preferences (user_id) VALUES (?)",
                (user_id,)
            )
            self.conn.commit()
            
            return {
                "status": "success",
                "user_id": user_id,
                "username": username,
                "email": email
            }
        
        except sqlite3.IntegrityError:
            return {"status": "error", "message": "用户名已存在"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def authenticate(self, username: str, password: str) -> Dict:
        """验证用户
        
        Args:
            username: 用户名
            password: 密码 (明文)
            
        Returns:
            Dict: 用户信息或错误信息
        """
        
        from passlib.hash import bcrypt
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id, username, email, password_hash, role FROM users WHERE username = ? AND is_active = 1",
                (username,)
            )
            
            user = cursor.fetchone()
            
            if user and bcrypt.verify(password, user[3]):
                # 更新最后登录时间
                cursor.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.now(), user[0])
                )
                self.conn.commit()
                
                return {
                    "status": "success",
                    "user_id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role": user[4]
                }
            
            return {"status": "error", "message": "用户名或密码错误"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_user_preferences(self, user_id: int) -> Dict:
        """获取用户偏好
        
        Args:
            user_id: 用户 ID
            
        Returns:
            Dict: 用户偏好信息
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT preferred_topics, favorite_characters, reading_frequency, notification_enabled FROM user_preferences WHERE user_id = ?",
                (user_id,)
            )
            
            row = cursor.fetchone()
            
            if row:
                return {
                    "preferred_topics": row[0].split(",") if row[0] else [],
                    "favorite_characters": row[1].split(",") if row[1] else [],
                    "reading_frequency": row[2],
                    "notification_enabled": bool(row[3])
                }
            
            return {"status": "error", "message": "未找到用户偏好"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_user_preferences(self, user_id: int, preferences: Dict) -> Dict:
        """更新用户偏好
        
        Args:
            user_id: 用户 ID
            preferences: 偏好字典
            
        Returns:
            Dict: 操作结果
        """
        
        try:
            cursor = self.conn.cursor()
            
            preferred_topics = ",".join(preferences.get('preferred_topics', []))
            favorite_characters = ",".join(preferences.get('favorite_characters', []))
            reading_frequency = preferences.get('reading_frequency', 'daily')
            notification_enabled = 1 if preferences.get('notification_enabled', True) else 0
            
            cursor.execute("""
                UPDATE user_preferences 
                SET preferred_topics = ?, favorite_characters = ?, 
                    reading_frequency = ?, notification_enabled = ?
                WHERE user_id = ?
            """, (preferred_topics, favorite_characters, reading_frequency, 
                  notification_enabled, user_id))
            
            self.conn.commit()
            
            return {"status": "success"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def record_user_action(self, user_id: int, action_type: str, 
                          query_text: str = None, result_count: int = 0,
                          duration_ms: float = 0) -> Dict:
        """记录用户行为
        
        Args:
            user_id: 用户 ID
            action_type: 动作类型 (search/translate/profile/wisdom/simulator)
            query_text: 查询文本
            result_count: 结果数量
            duration_ms: 耗时 (毫秒)
            
        Returns:
            Dict: 操作结果
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO user_history 
                (user_id, action_type, query_text, result_count, duration_ms)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, action_type, query_text, result_count, duration_ms))
            
            self.conn.commit()
            
            return {"status": "success"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def record_api_log(self, user_id: Optional[int], endpoint: str, 
                      method: str, status_code: int, request_time: float,
                      ip_address: str = None) -> Dict:
        """记录 API 访问日志
        
        Args:
            user_id: 用户 ID (可选，匿名请求为 None)
            endpoint: API 端点
            method: HTTP 方法
            status_code: 状态码
            request_time: 请求耗时 (秒)
            ip_address: IP 地址
            
        Returns:
            Dict: 操作结果
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO api_logs 
                (user_id, endpoint, method, status_code, request_time, ip_address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, endpoint, method, status_code, request_time, ip_address))
            
            self.conn.commit()
            
            return {"status": "success"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_user_history(self, user_id: int, action_type: str = None, 
                        limit: int = 50) -> List[Dict]:
        """获取用户历史行为
        
        Args:
            user_id: 用户 ID
            action_type: 动作类型筛选 (可选)
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 历史记录列表
        """
        
        try:
            cursor = self.conn.cursor()
            
            if action_type:
                cursor.execute("""
                    SELECT * FROM user_history 
                    WHERE user_id = ? AND action_type = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (user_id, action_type, limit))
            else:
                cursor.execute("""
                    SELECT * FROM user_history 
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (user_id, limit))
            
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            return []
    
    def get_api_statistics(self, days: int = 7) -> Dict:
        """获取 API 统计信息
        
        Args:
            days: 统计天数
            
        Returns:
            Dict: 统计数据
        """
        
        try:
            cursor = self.conn.cursor()
            
            # 总请求数
            cursor.execute("""
                SELECT COUNT(*) FROM api_logs 
                WHERE created_at >= datetime('now', ?)
            """, (f"-{days} days",))
            total_requests = cursor.fetchone()[0]
            
            # 按端点统计
            cursor.execute("""
                SELECT endpoint, COUNT(*), AVG(request_time)
                FROM api_logs 
                WHERE created_at >= datetime('now', ?)
                GROUP BY endpoint
                ORDER BY COUNT(*) DESC
            """, (f"-{days} days",))
            
            endpoint_stats = []
            for row in cursor.fetchall():
                endpoint_stats.append({
                    "endpoint": row[0],
                    "requests": row[1],
                    "avg_time_ms": round(row[2] * 1000, 2)
                })
            
            # 按状态码统计
            cursor.execute("""
                SELECT status_code, COUNT(*)
                FROM api_logs 
                WHERE created_at >= datetime('now', ?)
                GROUP BY status_code
            """, (f"-{days} days",))
            
            status_stats = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                "total_requests": total_requests,
                "endpoint_statistics": endpoint_stats,
                "status_statistics": status_stats,
                "period_days": days
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def add_bookmark(self, user_id: int, case_name: str, notes: str = None) -> Dict:
        """添加收藏
        
        Args:
            user_id: 用户 ID
            case_name: 案例名称
            notes: 备注
            
        Returns:
            Dict: 操作结果
        """
        
        try:
            cursor = self.conn.cursor()
            
            # 检查是否已存在
            cursor.execute("""
                SELECT id FROM user_bookmarks 
                WHERE user_id = ? AND case_name = ?
            """, (user_id, case_name))
            
            if cursor.fetchone():
                return {"status": "error", "message": "已收藏"}
            
            cursor.execute("""
                INSERT INTO user_bookmarks (user_id, case_name, notes)
                VALUES (?, ?, ?)
            """, (user_id, case_name, notes))
            
            self.conn.commit()
            
            return {"status": "success"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_bookmarks(self, user_id: int) -> List[Dict]:
        """获取用户收藏列表
        
        Args:
            user_id: 用户 ID
            
        Returns:
            List[Dict]: 收藏列表
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM user_bookmarks 
                WHERE user_id = ?
                ORDER BY bookmarked_at DESC
            """, (user_id,))
            
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            return []
    
    def remove_bookmark(self, user_id: int, case_name: str) -> Dict:
        """移除收藏
        
        Args:
            user_id: 用户 ID
            case_name: 案例名称
            
        Returns:
            Dict: 操作结果
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM user_bookmarks 
                WHERE user_id = ? AND case_name = ?
            """, (user_id, case_name))
            
            self.conn.commit()
            
            return {"status": "success"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_reading_progress(self, user_id: int, case_name: str) -> Dict:
        """更新阅读进度
        
        Args:
            user_id: 用户 ID
            case_name: 案例名称
            
        Returns:
            Dict: 操作结果
        """
        
        try:
            cursor = self.conn.cursor()
            
            # 检查是否已存在
            cursor.execute("""
                SELECT id, read_count FROM user_progress 
                WHERE user_id = ? AND case_name = ?
            """, (user_id, case_name))
            
            row = cursor.fetchone()
            
            if row:
                new_count = row[1] + 1
                cursor.execute("""
                    UPDATE user_progress 
                    SET read_count = ?, last_read_at = ?
                    WHERE id = ?
                """, (new_count, datetime.now(), row[0]))
            else:
                cursor.execute("""
                    INSERT INTO user_progress (user_id, case_name, read_count)
                    VALUES (?, ?, 1)
                """, (user_id, case_name))
            
            self.conn.commit()
            
            return {"status": "success"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_user_progress(self, user_id: int) -> Dict:
        """获取用户学习进度
        
        Args:
            user_id: 用户 ID
            
        Returns:
            Dict: 学习进度统计
        """
        
        try:
            cursor = self.conn.cursor()
            
            # 总阅读次数
            cursor.execute("""
                SELECT COUNT(DISTINCT case_name), SUM(read_count)
                FROM user_progress 
                WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            
            return {
                "total_cases": row[0] or 0,
                "total_reads": row[1] or 0
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def export_data(self, output_path: str = None) -> Dict:
        """导出数据
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            Dict: 导出结果
        """
        
        if output_path is None:
            base_dir = Path(__file__).parent.parent / "data"
            output_path = str(base_dir / "user_data_export.json")
        
        try:
            data = {
                "export_time": datetime.now().isoformat(),
                "users": [],
                "preferences": [],
                "bookmarks": []
            }
            
            # 导出用户数据 (不包含密码)
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, username, email, created_at, last_login, role 
                FROM users
            """)
            
            for row in cursor.fetchall():
                data["users"].append({
                    "id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "created_at": row[3],
                    "last_login": row[4],
                    "role": row[5]
                })
            
            # 导出偏好数据
            cursor.execute("""
                SELECT user_id, preferred_topics, favorite_characters 
                FROM user_preferences
            """)
            
            for row in cursor.fetchall():
                data["preferences"].append({
                    "user_id": row[0],
                    "preferred_topics": row[1],
                    "favorite_characters": row[2]
                })
            
            # 导出收藏数据
            cursor.execute("""
                SELECT user_id, case_name, bookmarked_at 
                FROM user_bookmarks
            """)
            
            for row in cursor.fetchall():
                data["bookmarks"].append({
                    "user_id": row[0],
                    "case_name": row[1],
                    "bookmarked_at": row[2]
                })
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据已导出：{output_path}")
            
            return {"status": "success", "path": output_path}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def close(self):
        """关闭数据库连接"""
        
        if self.conn:
            self.conn.close()
            print("✅ 数据库连接已关闭")


# 测试
if __name__ == "__main__":
    db = DatabaseManager()
    
    print("\n" + "=" * 80)
    print("📊 数据库管理器测试")
    print("=" * 80)
    
    # 1. 创建用户
    print("\n--- 测试 1: 创建用户 ---")
    result = db.create_user(
        username="test_user",
        email="test@example.com",
        password="secure_password123"
    )
    print(f"结果：{result}")
    
    # 2. 验证用户
    print("\n--- 测试 2: 验证用户 ---")
    result = db.authenticate("test_user", "secure_password123")
    print(f"结果：{result}")
    
    if result["status"] == "success":
        user_id = result["user_id"]
        
        # 3. 获取偏好
        print("\n--- 测试 3: 获取用户偏好 ---")
        prefs = db.get_user_preferences(user_id)
        print(f"偏好：{prefs}")
        
        # 4. 更新偏好
        print("\n--- 测试 4: 更新用户偏好 ---")
        result = db.update_user_preferences(user_id, {
            "preferred_topics": ["用人智慧", "战略决策"],
            "favorite_characters": ["刘邦", "诸葛亮"]
        })
        print(f"结果：{result}")
        
        # 5. 记录行为
        print("\n--- 测试 5: 记录用户行为 ---")
        result = db.record_user_action(
            user_id=user_id,
            action_type="search",
            query_text="刘邦",
            result_count=3,
            duration_ms=120.5
        )
        print(f"结果：{result}")
        
        # 6. 添加收藏
        print("\n--- 测试 6: 添加收藏 ---")
        result = db.add_bookmark(user_id, "如虎添翼 - 刘备借荆州", "经典案例")
        print(f"结果：{result}")
        
        # 7. 获取收藏列表
        print("\n--- 测试 7: 获取收藏列表 ---")
        bookmarks = db.get_bookmarks(user_id)
        print(f"收藏数量：{len(bookmarks)}")
        
        # 8. API 统计
        print("\n--- 测试 8: API 统计 ---")
        stats = db.get_api_statistics(days=7)
        print(f"统计数据：{stats}")
    
    # 关闭连接
    db.close()
    
    print("\n" + "=" * 80)
    print("🎉 数据库管理器测试完成！")
    print("=" * 80)
