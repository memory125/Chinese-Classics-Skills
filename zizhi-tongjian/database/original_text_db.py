#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴原文数据库 - SQLite + FTS5 全文索引

功能：
1. 创建 SQLite 数据库 (包含 FTS5 全文索引)
2. 批量导入原文数据
3. 高效全文搜索
4. 与现有系统无缝集成
"""

import sqlite3
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime


class OriginalTextDatabase:
    """资治通鉴原文数据库管理器 (SQLite + FTS5)"""
    
    def __init__(self, db_path: str = None):
        """初始化数据库
        
        Args:
            db_path: 数据库文件路径，默认 data/original_texts.db
        """
        
        if db_path is None:
            base_dir = Path(__file__).parent.parent / "data"
            self.db_path = str(base_dir / "original_texts.db")
        else:
            self.db_path = db_path
        
        # 创建目录
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 连接数据库
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # 创建表结构
        self._create_tables()
        
        print(f"✅ 原文数据库已初始化：{self.db_path}")
    
    def _create_tables(self):
        """创建数据表和全文索引"""
        
        cursor = self.conn.cursor()
        
        # 1. 主表 - 存储原文内容
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS original_texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                volume TEXT NOT NULL,           -- 卷名 (如：汉纪五十七)
                year TEXT NOT NULL,             -- 年份 (如：建安十三年)
                dynasty TEXT NOT NULL,          -- 朝代 (如：东汉)
                content TEXT NOT NULL,          -- 原文内容
                translation TEXT,               -- 译文 (可选)
                keywords TEXT,                  -- 关键词 (逗号分隔)
                source TEXT DEFAULT 'local',    -- 来源 (local/online)
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. FTS5 全文索引表
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS original_texts_fts 
            USING fts5(volume, year, dynasty, content, content='original_texts', content_rowid='id')
        """)
        
        # 3. 创建触发器 - 自动同步 FTS 索引
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS original_texts_ai AFTER INSERT ON original_texts BEGIN
                INSERT INTO original_texts_fts (rowid, volume, year, dynasty, content)
                VALUES (new.id, new.volume, new.year, new.dynasty, new.content);
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS original_texts_ad AFTER DELETE ON original_texts BEGIN
                INSERT INTO original_texts_fts (original_texts_fts, rowid, volume, year, dynasty, content)
                VALUES ('delete', old.id, old.volume, old.year, old.dynasty, old.content);
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS original_texts_au AFTER UPDATE ON original_texts BEGIN
                INSERT INTO original_texts_fts (original_texts_fts, rowid, volume, year, dynasty, content)
                VALUES ('delete', old.id, old.volume, old.year, old.dynasty, old.content);
                INSERT INTO original_texts_fts (rowid, volume, year, dynasty, content)
                VALUES (new.id, new.volume, new.year, new.dynasty, new.content);
            END
        """)
        
        # 4. 创建普通索引 (加速查询)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_texts_dynastry ON original_texts(dynasty)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_texts_year ON original_texts(year)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_texts_volume ON original_texts(volume)
        """)
        
        self.conn.commit()
        print("✅ 数据表和索引创建完成 (1 主表 + 1 FTS5 索引 + 3 普通索引)")
    
    def add_text(self, 
                 volume: str, 
                 year: str, 
                 dynasty: str, 
                 content: str, 
                 translation: Optional[str] = None,
                 keywords: Optional[List[str]] = None,
                 source: str = 'local') -> Dict:
        """添加原文记录
        
        Args:
            volume: 卷名 (如：汉纪五十七)
            year: 年份 (如：建安十三年)
            dynasty: 朝代 (如：东汉)
            content: 原文内容
            translation: 译文 (可选)
            keywords: 关键词列表 (可选)
            source: 来源 (local/online)
            
        Returns:
            Dict: 操作结果
        """
        
        try:
            # 处理关键词
            keywords_str = ",".join(keywords) if keywords else ""
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO original_texts 
                (volume, year, dynasty, content, translation, keywords, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (volume, year, dynasty, content, translation, keywords_str, source))
            
            self.conn.commit()
            
            return {
                "status": "success",
                "id": cursor.lastrowid,
                "message": f"已添加原文记录 #{cursor.lastrowid}"
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search(self, 
              query: str, 
              limit: int = 20,
              offset: int = 0) -> List[Dict]:
        """全文搜索
        
        Args:
            query: 搜索关键词
            limit: 返回数量限制
            offset: 偏移量 (分页)
            
        Returns:
            List[Dict]: 搜索结果列表
        """
        
        try:
            cursor = self.conn.cursor()
            
            # FTS5 全文搜索
            cursor.execute("""
                SELECT o.id, o.volume, o.year, o.dynasty, 
                       o.content, o.translation, o.keywords,
                       fts.score as relevance_score
                FROM original_texts_fts fts
                JOIN original_texts o ON fts.rowid = o.id
                WHERE original_texts_fts MATCH ?
                ORDER BY fts.score
                LIMIT ? OFFSET ?
            """, (query, limit, offset))
            
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "volume": row[1],
                    "year": row[2],
                    "dynasty": row[3],
                    "content": row[4],
                    "translation": row[5] or "",
                    "keywords": row[6].split(",") if row[6] else [],
                    "relevance_score": float(row[7]) if row[7] else 0.0
                })
            
            return results
        
        except Exception as e:
            print(f"❌ 搜索失败：{e}")
            return []
    
    def search_by_dynastry(self, 
                          dynasty: str, 
                          limit: int = 50) -> List[Dict]:
        """按朝代查询
        
        Args:
            dynasty: 朝代名称 (如：汉、唐、宋)
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 结果列表
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, volume, year, dynasty, content, translation, keywords
                FROM original_texts
                WHERE dynasty LIKE ?
                ORDER BY year DESC
                LIMIT ?
            """, (f"%{dynasty}%", limit))
            
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "volume": row[1],
                    "year": row[2],
                    "dynasty": row[3],
                    "content": row[4],
                    "translation": row[5] or "",
                    "keywords": row[6].split(",") if row[6] else []
                })
            
            return results
        
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return []
    
    def get_by_id(self, record_id: int) -> Optional[Dict]:
        """根据 ID 获取原文记录
        
        Args:
            record_id: 记录 ID
            
        Returns:
            Optional[Dict]: 原文记录或 None
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, volume, year, dynasty, content, translation, keywords
                FROM original_texts
                WHERE id = ?
            """, (record_id,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "volume": row[1],
                    "year": row[2],
                    "dynasty": row[3],
                    "content": row[4],
                    "translation": row[5] or "",
                    "keywords": row[6].split(",") if row[6] else []
                }
            
            return None
        
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return None
    
    def get_statistics(self) -> Dict:
        """获取数据库统计信息
        
        Returns:
            Dict: 统计数据
        """
        
        try:
            cursor = self.conn.cursor()
            
            # 总记录数
            cursor.execute("SELECT COUNT(*) FROM original_texts")
            total_records = cursor.fetchone()[0]
            
            # 按朝代统计
            cursor.execute("""
                SELECT dynasty, COUNT(*) as count
                FROM original_texts
                GROUP BY dynasty
                ORDER BY count DESC
            """)
            dynasty_stats = {row[0]: row[1] for row in cursor.fetchall()}
            
            # 按来源统计
            cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM original_texts
                GROUP BY source
            """)
            source_stats = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                "total_records": total_records,
                "by_dynasty": dynasty_stats,
                "by_source": source_stats
            }
        
        except Exception as e:
            print(f"❌ 获取统计失败：{e}")
            return {}
    
    def bulk_import(self, texts: List[Dict]) -> Dict:
        """批量导入原文数据
        
        Args:
            texts: 原文记录列表，每项包含 volume/year/dynasty/content/translation
            
        Returns:
            Dict: 导入结果统计
        """
        
        success_count = 0
        error_count = 0
        errors = []
        
        for i, text_data in enumerate(texts):
            try:
                result = self.add_text(
                    volume=text_data.get('volume', ''),
                    year=text_data.get('year', ''),
                    dynasty=text_data.get('dynasty', ''),
                    content=text_data.get('content', ''),
                    translation=text_data.get('translation'),
                    keywords=text_data.get('keywords', []),
                    source=text_data.get('source', 'local')
                )
                
                if result['status'] == 'success':
                    success_count += 1
                else:
                    error_count += 1
                    errors.append(f"第{i+1}条：{result['message']}")
            
            except Exception as e:
                error_count += 1
                errors.append(f"第{i+1}条异常：{str(e)}")
        
        return {
            "status": "success" if error_count == 0 else "partial",
            "total": len(texts),
            "success": success_count,
            "errors": error_count,
            "error_details": errors[:10]  # 只显示前 10 个错误
        }
    
    def export_to_json(self, output_path: str = None) -> Dict:
        """导出数据库内容为 JSON
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            Dict: 导出结果
        """
        
        if output_path is None:
            base_dir = Path(__file__).parent.parent / "data"
            output_path = str(base_dir / "original_texts_export.json")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, volume, year, dynasty, content, translation, keywords
                FROM original_texts
                ORDER BY id DESC
            """)
            
            rows = cursor.fetchall()
            
            data = []
            for row in rows:
                data.append({
                    "id": row[0],
                    "volume": row[1],
                    "year": row[2],
                    "dynasty": row[3],
                    "content": row[4],
                    "translation": row[5] or "",
                    "keywords": row[6].split(",") if row[6] else []
                })
            
            import json
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据已导出：{output_path} ({len(data)}条记录)")
            
            return {"status": "success", "path": output_path, "count": len(data)}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def clear_all(self) -> Dict:
        """清空所有数据
        
        Returns:
            Dict: 操作结果
        """
        
        try:
            cursor = self.conn.cursor()
            
            # 删除 FTS 索引
            cursor.execute("DROP TABLE IF EXISTS original_texts_fts")
            
            # 删除主表
            cursor.execute("DELETE FROM original_texts")
            
            # 重建 FTS 索引
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS original_texts_fts 
                USING fts5(volume, year, dynasty, content, content='original_texts', content_rowid='id')
            """)
            
            self.conn.commit()
            
            return {"status": "success", "message": "数据已清空"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def close(self):
        """关闭数据库连接"""
        
        if self.conn:
            self.conn.close()
            print("✅ 原文数据库连接已关闭")


# ==================== 测试数据 ====================

def get_sample_data() -> List[Dict]:
    """获取示例数据用于测试"""
    
    return [
        {
            "volume": "汉纪五十七",
            "year": "建安十三年",
            "dynasty": "东汉",
            "content": "刘豫州王室之胄，英才盖世，众士慕仰，若水之归海。",
            "translation": "我听说刘备是皇室后裔，才能盖世，众多士人仰慕他，就像水流向大海一样。",
            "keywords": ["刘备", "孙权", "赤壁之战"]
        },
        {
            "volume": "汉纪五十七",
            "year": "建安十三年",
            "dynasty": "东汉",
            "content": "若使涂山佐禹，则夏室不倾；伊尹相汤，则商祚永延。",
            "translation": "如果让涂山氏辅佐大禹，那么夏朝就不会倾覆；伊尹辅佐商汤，那么商朝的国运就会长久延续。",
            "keywords": ["辅佐", "治国"]
        },
        {
            "volume": "唐纪十九",
            "year": "贞观三年",
            "dynasty": "唐朝",
            "content": "水能载舟，亦能覆舟。",
            "translation": "水能够承载船只，也能够倾覆船只。比喻人民可以支持君主，也可以推翻君主。",
            "keywords": ["唐太宗", "治国", "民本"]
        },
        {
            "volume": "宋纪一百六十七",
            "year": "庆历三年",
            "dynasty": "北宋",
            "content": "先天下之忧而忧，后天下之乐而乐。",
            "translation": "在天下人忧虑之前先忧虑，在天下人快乐之后才快乐。",
            "keywords": ["范仲淹", "岳阳楼记", "忧国忧民"]
        },
        {
            "volume": "汉纪五十七",
            "year": "建安十三年",
            "dynasty": "东汉",
            "content": "如虎添翼，势不可挡。",
            "translation": "像老虎加上翅膀一样，气势强大，无法阻挡。比喻强大的事物得到助力后更加强大。",
            "keywords": ["如虎添翼", "刘备", "荆州"]
        }
    ]


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 80)
    print("📚 资治通鉴原文数据库 - 测试")
    print("=" * 80)
    
    # 创建数据库
    db = OriginalTextDatabase()
    
    # 1. 添加示例数据
    print("\n--- 测试 1: 添加示例数据 ---")
    
    sample_data = get_sample_data()
    
    for i, text in enumerate(sample_data, 1):
        result = db.add_text(
            volume=text['volume'],
            year=text['year'],
            dynasty=text['dynasty'],
            content=text['content'],
            translation=text['translation'],
            keywords=text['keywords']
        )
        
        print(f"{i}. {result['message']}")
    
    # 2. 全文搜索测试
    print("\n--- 测试 2: 全文搜索 ---")
    
    search_queries = ["刘备", "赤壁", "唐太宗", "范仲淹"]
    
    for query in search_queries:
        results = db.search(query, limit=3)
        
        print(f"\n🔍 搜索：'{query}' (找到 {len(results)} 条)")
        
        for r in results[:2]:
            print(f"   - [{r['dynasty']}{r['year']}] {r['volume']}")
            print(f"     内容：{r['content'][:50]}...")
    
    # 3. 按朝代查询测试
    print("\n--- 测试 3: 按朝代查询 ---")
    
    dynasty_results = db.search_by_dynastry("汉", limit=3)
    
    print(f"\n📊 汉朝记录 (找到 {len(dynasty_results)} 条)")
    
    for r in dynasty_results[:2]:
        print(f"   - [{r['year']}] {r['content'][:50]}...")
    
    # 4. 统计信息测试
    print("\n--- 测试 4: 数据库统计 ---")
    
    stats = db.get_statistics()
    
    print(f"\n📊 总记录数：{stats['total_records']}")
    print(f"按朝代分布:")
    for dynasty, count in stats['by_dynasty'].items():
        print(f"   - {dynasty}: {count}条")
    
    # 5. 导出测试
    print("\n--- 测试 5: 导出数据 ---")
    
    export_result = db.export_to_json()
    
    if export_result['status'] == 'success':
        print(f"✅ 已导出：{export_result['path']} ({export_result['count']}条)")
    
    # 关闭连接
    db.close()
    
    print("\n" + "=" * 80)
    print("🎉 原文数据库测试完成！")
    print("=" * 80)
