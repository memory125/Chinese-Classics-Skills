#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 - RAG 检索接口
整合向量数据库，提供统一检索 API
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

# 添加路径
sys.path.append(str(Path(__file__).parent.parent))

from reference.vector_db import create_vector_db_from_reference, RAGSearchEngine, TextSplitter

def search_by_query(query: str, top_k: int = 5, include_examples: bool = True) -> List[Dict]:
    """
    根据查询关键词搜索历史案例
    """
    try:
        engine = create_vector_db_from_reference()
        results = engine.search(query, top_k)
        
        formatted = []
        for r in results:
            formatted.append({
                "相似度": f"{r['relevance_score'] * 100:.1f}%",
                "来源": r['source'],
                "关键词": ", ".join(r['keywords'][:5]),
                "内容预览": r['text'][:200] + "..." if len(r['text']) > 200 else r['text']
            })
        
        return formatted
    
    except Exception as e:
        return [{"error": f"搜索失败：{str(e)}"}]

def search_by_case_name(case_name: str) -> Optional[Dict]:
    """
    通过案例名称精确查询
    """
    try:
        engine = create_vector_db_from_reference()
        result = engine.get_case_by_name(case_name)
        return result
        
    except Exception as e:
        return {"error": f"查询失败：{str(e)}"}

def search_similar_scenarios(scenario: str, limit: int = 3) -> List[Dict]:
    """
    根据场景查找相似案例
    """
    from reference.scenario_tags_enhanced import RecommendationEngine
    
    engine = RecommendationEngine()
    recommendations = engine.recommend_by_scenario(scenario)
    
    return [
        {
            "场景": rec["场景"],
            "案例": rec["案例"],
            "核心智慧": rec["核心智慧"],
            "现代应用": rec["现代应用"]
        }
        for rec in recommendations[:limit]
    ]


# 测试
if __name__ == "__main__":
    print("=" * 60)
    print("测试 1: 关键词搜索 - 鸿门宴")
    print("=" * 60)
    results = search_by_query("鸿门宴", top_k=3)
    for r in results:
        print(f"相似度：{r['相似度']}")
        print(f"关键词：{r['关键词']}")
        print(f"内容：{r['内容预览']}")
        print()
    
    print("=" * 60)
    print("测试 2: 场景搜索 - 向上管理")
    print("=" * 60)
    scenarios = search_similar_scenarios("向上管理", limit=3)
    for s in scenarios:
        print(f"案例：{s['案例']}")
        print(f"核心智慧：{s['核心智慧']}")
        print(f"现代应用：{s['现代应用']}")
        print()
