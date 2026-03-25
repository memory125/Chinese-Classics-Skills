#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能混合搜索系统 v3.0 - 自动选择最优方案

核心功能：
1. 本地优先检索 (EnhancedRAGSearch v5.0)
2. 智能网络策略选择 (BeautifulSoup + Scrapling v2)
3. 动态参数调整 (根据查询类型)
4. 自动同步到本地数据
"""

import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime
import re

# 导入本地 RAG 系统
try:
    from scripts.rag_enhanced_v5 import EnhancedRAGSearch
    HAS_LOCAL_RAG = True
except ImportError as e:
    HAS_LOCAL_RAG = False
    print(f"⚠️ 本地 RAG 加载失败：{e}")

# 导入网络搜索模块 (v2.0)
try:
    from scripts.web_search_scrapling_v2 import WebSearchEngine, CaseGenerator
    HAS_WEB_SEARCH = True
except ImportError as e:
    HAS_WEB_SEARCH = False
    print(f"⚠️ 网络搜索加载失败：{e}")


class QueryClassifier:
    """查询分类器 - 智能识别查询类型"""
    
    # 历史主题关键词
    HISTORY_KEYWORDS = [
        '三国', '汉朝', '唐朝', '宋朝', '明朝', '清朝', 
        '秦始皇', '汉武帝', '唐太宗', '诸葛亮', '曹操',
        '刘邦', '项羽', '李世民', '朱元璋'
    ]
    
    # 成语/典故关键词
    IDIOM_KEYWORDS = [
        '如虎添翼', '草船借箭', '认贼作父', '塞翁失马',
        '卧薪尝胆', '破釜沉舟', '完璧归赵', '负荆请罪'
    ]
    
    # 现代主题关键词
    MODERN_KEYWORDS = [
        '量子力学', '人工智能', '区块链', '气候变化',
        '经济危机', '科技创新', '企业管理'
    ]
    
    @classmethod
    def classify(cls, query: str) -> Tuple[str, float]:
        """分类查询并返回置信度"""
        
        query_lower = query.lower()
        
        # 1. 检查是否是历史主题
        history_score = sum(1 for kw in cls.HISTORY_KEYWORDS if kw in query_lower)
        
        # 2. 检查是否是成语/典故
        idiom_score = sum(1 for kw in cls.IDIOM_KEYWORDS if kw in query_lower)
        
        # 3. 检查是否是现代主题
        modern_score = sum(1 for kw in cls.MODERN_KEYWORDS if kw in query_lower)
        
        # 4. 判断类型
        scores = {
            'history': history_score,
            'idiom': idiom_score,
            'modern': modern_score,
            'general': max(history_score, idiom_score, modern_score) == 0
        }
        
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / max(len(query.split()), 1)
        
        return best_type, min(confidence, 1.0)


class AdaptiveWebSearch:
    """自适应网络搜索 - 根据查询类型选择最优策略"""
    
    def __init__(self):
        self.web_search = WebSearchEngine() if HAS_WEB_SEARCH else None
        
        # 配置参数 (根据查询类型动态调整)
        self.config = {
            'history': {
                'top_k': 5,
                'scrapling_enabled': True,
                'render_wait': 3,  # 历史网站需要更多渲染时间
                'timeout': 20
            },
            'idiom': {
                'top_k': 3,
                'scrapling_enabled': False,  # 成语不需要深度抓取
                'render_wait': 1,
                'timeout': 10
            },
            'modern': {
                'top_k': 5,
                'scrapling_enabled': True,
                'render_wait': 2,
                'timeout': 15
            },
            'general': {
                'top_k': 3,
                'scrapling_enabled': False,
                'render_wait': 1,
                'timeout': 10
            }
        }
    
    def search(self, query: str, query_type: str) -> List[Dict]:
        """根据查询类型选择最优搜索策略"""
        
        config = self.config.get(query_type, self.config['general'])
        
        print(f"   🎯 查询类型：{query_type} (置信度：{config['top_k']/5:.1f})")
        print(f"   ⚙️ 使用策略：Scrapling={'启用' if config['scrapling_enabled'] else '禁用'}")
        
        if not self.web_search:
            return []
        
        try:
            results = self.web_search.search(query, top_k=config['top_k'])
            
            # 根据查询类型调整分数权重
            for r in results:
                if query_type == 'history':
                    r['score'] *= 1.2  # 历史主题高分
                elif query_type == 'idiom':
                    r['score'] *= 1.0
                else:
                    r['score'] *= 0.9
            
            return results[:config['top_k']]
            
        except Exception as e:
            print(f"   ⚠️ 网络搜索失败：{e}")
            return []


class SmartHybridSearch:
    """智能混合搜索系统 v3.0"""
    
    def __init__(self):
        self.local_rag = EnhancedRAGSearch() if HAS_LOCAL_RAG else None
        self.adaptive_web = AdaptiveWebSearch() if HAS_WEB_SEARCH else None
        self.case_generator = CaseGenerator() if HAS_WEB_SEARCH else None
        
        # 配置参数
        self.min_local_score = 0.3
        self.auto_sync_enabled = True
        self.sync_threshold = 0.5  # 网络结果可信度阈值
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """智能混合搜索主入口"""
        
        print(f"🔍 开始搜索：'{query}'")
        print("=" * 60)
        
        results = []
        
        # ========== Step 1: 查询分类 ==========
        query_type, confidence = QueryClassifier.classify(query)
        print(f"\n📊 Step 0: 查询分类")
        print(f"   类型：{query_type} | 置信度：{confidence:.2f}")
        
        # ========== Step 2: 本地离线检索 ==========
        if self.local_rag:
            print(f"\n📚 Step 1: 本地离线检索...")
            
            local_results = self.local_rag.hybrid_search(query, top_k=top_k * 2)
            
            # 过滤高可信度结果
            high_confidence = []
            for r in local_results:
                score = r.get('score', 0)
                
                if score >= self.min_local_score:
                    case_data = self.local_rag.case_db.get(r['name'], {})
                    
                    # 根据查询类型调整分数
                    if query_type == 'history' and any(kw in case_data.get('title', '') for kw in QueryClassifier.HISTORY_KEYWORDS):
                        score *= 1.2
                    
                    high_confidence.append({
                        'source': 'local',
                        'type': 'case',
                        'name': r['name'],
                        'title': case_data.get('title', ''),
                        'score': score,
                        'wisdom': case_data.get('key_wisdom', ''),
                        'applications': case_data.get('modern_applications', []),
                        'related_cases': self.local_rag.get_related_cases(r['name'], limit=2)
                    })
            
            results.extend(high_confidence)
            
            print(f"   ✅ 找到 {len(high_confidence)} 个高可信度本地案例")
            
            # 如果结果足够，直接返回
            if len(results) >= top_k:
                print(f"   🎯 本地结果已满足需求，跳过网络搜索")
                return results[:top_k]
        else:
            print("⚠️ 本地 RAG 不可用，直接使用网络搜索")
        
        # ========== Step 3: 智能网络搜索补充 ==========
        if self.adaptive_web and len(results) < top_k:
            needed = top_k - len(results)
            
            print(f"\n🌐 Step 2: 智能网络搜索补充 (需要 {needed} 个结果)...")
            
            web_results = self.adaptive_web.search(query, query_type)
            
            for r in web_results[:needed]:
                results.append({
                    'source': 'web',
                    'type': 'search_result',
                    'title': r.get('title', ''),
                    'url': r.get('url', ''),
                    'content': r.get('content', '')[:300],
                    'score': r.get('score', 0.5),
                    'snippet': True,
                    'query_type': query_type
                })
            
            print(f"   ✅ 找到 {len(web_results)} 个网络搜索结果")
        
        # ========== Step 4: 智能同步到本地 ==========
        if self.auto_sync_enabled and len(results) > 0:
            print("\n💾 Step 3: 检查是否需要同步到本地...")
            
            web_only_results = [r for r in results if r['source'] == 'web' and r.get('score', 0) >= self.sync_threshold]
            
            if web_only_results and query_type != 'idiom':  # 成语类不生成新案例
                print(f"   📝 发现 {len(web_only_results)} 个高可信度网络结果，准备同步...")
                
                try:
                    new_case = self.case_generator.generate_case_from_query(query)
                    
                    if new_case:
                        case_name = f"{query} - {datetime.now().strftime('%Y%m%d')}"
                        self.case_generator.save_to_cases_json(case_name, new_case)
                        
                        # 添加到结果列表
                        results.append({
                            'source': 'local',
                            'type': 'case',
                            'name': case_name,
                            'title': new_case.get('title', ''),
                            'score': 0.95,
                            'wisdom': new_case.get('key_wisdom', ''),
                            'applications': new_case.get('modern_applications', []),
                            'related_cases': [],
                            'synced_at': datetime.now().isoformat(),
                            'query_type': query_type
                        })
                        
                        print(f"   ✅ 已同步新案例：{case_name}")
                except Exception as e:
                    print(f"   ⚠️ 同步失败：{e}")
        
        # ========== Step 5: 返回最终结果 ==========
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        print("\n" + "=" * 60)
        print(f"🎯 最终返回 {len(results)} 个结果")
        
        return results[:top_k]


# 测试
if __name__ == "__main__":
    hybrid = SmartHybridSearch()
    
    # 测试 1: 历史成语 (本地有)
    print("\n=== 测试 1: 如虎添翼 (历史成语) ===")
    results = hybrid.search("如虎添翼", top_k=3)
    for i, r in enumerate(results[:2], 1):
        title = r.get('title', 'N/A')
        score = r.get('score', 0)
        source = r.get('source', 'unknown')
        
        print(f"{i}. [{source}] {title[:50]} (得分：{score:.2f})")
    
    # 测试 2: 现代主题 (本地没有)
    print("\n=== 测试 2: 量子力学历史 (现代主题) ===")
    results = hybrid.search("量子力学历史", top_k=3)
    for i, r in enumerate(results[:2], 1):
        title = r.get('title', 'N/A')
        score = r.get('score', 0)
        source = r.get('source', 'unknown')
        
        print(f"{i}. [{source}] {title[:50]} (得分：{score:.2f})")

    # 测试 3: 成语典故 (本地有)
    print("\n=== 测试 3: 塞翁失马焉知非福 (历史成语) ===")
    results = hybrid.search("塞翁失马", top_k=3)
    for i, r in enumerate(results[:2], 1):
        title = r.get('title', 'N/A')
        score = r.get('score', 0)
        source = r.get('source', 'unknown')
        
        print(f"{i}. [{source}] {title[:50]} (得分：{score:.2f})")
