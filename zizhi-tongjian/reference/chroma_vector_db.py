#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 - Chroma 向量数据库集成
实现：混合检索、语义搜索、时间线增强
"""

import json
import hashlib
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import re
import math
from datetime import datetime

class ChromaVectorDB:
    """Chroma 向量数据库封装"""
    
    def __init__(self, collection_name: str = "zizhi_tongjian"):
        try:
            import chromadb
            from chromadb.config import Settings
            
            # 初始化 Chroma 客户端
            self.client = chromadb.PersistentClient(
                path=str(Path(__file__).parent / "chroma_db"),
                settings=Settings(
                    anonymized_telemetry=False
                )
            )
            
            # 获取或创建集合
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            print(f"✓ Chroma 向量数据库已初始化：{collection_name}")
            
        except ImportError:
            print("⚠️ ChromaDB 未安装，降级使用 TF-IDF 检索")
            self.client = None
            self.collection = None
    
    def add_documents(self, documents: List[Dict]) -> int:
        """添加文档到向量数据库"""
        if not self.collection:
            return 0
        
        # 准备数据
        ids = []
        metadatas = []
        documents_text = []
        
        for i, doc in enumerate(documents):
            # 生成唯一 ID
            doc_id = hashlib.md5(doc['text'].encode()).hexdigest()[:16]
            ids.append(doc_id)
            
            # 元数据
            metadata = {
                'source': doc.get('source', 'unknown'),
                'type': doc.get('type', 'general'),
                'time_period': doc.get('time_period', ''),
                '人物': doc.get('people', []),
                '事件': doc.get('events', []),
                'keywords': doc.get('keywords', []),
                'created_at': datetime.now().isoformat()
            }
            metadatas.append(metadata)
            
            # 文本
            documents_text.append(doc['text'])
        
        # 批量添加
        self.collection.add(
            ids=ids,
            metadatas=metadatas,
            documents=documents_text,
            embeddings=None  # 使用内置嵌入
        )
        
        return len(documents)
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None,
        include_fields: List[str] = ['document', 'metadata', 'distance']
    ) -> List[Dict]:
        """搜索文档"""
        if not self.collection:
            return []
        
        try:
            # 执行搜索
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filters,
                include=include_fields
            )
            
            # 格式化结果
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'relevance_score': round(1 - results['distances'][0][i], 3)
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"搜索错误：{e}")
            return []
    
    def search_by_filters(
        self,
        filters: Dict,
        top_k: int = 5,
        include_fields: List[str] = ['document', 'metadata']
    ) -> List[Dict]:
        """按过滤器搜索"""
        if not self.collection:
            return []
        
        try:
            results = self.collection.query(
                where=filters,
                n_results=top_k,
                include=include_fields
            )
            
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'relevance_score': 1.0  # 过滤器匹配
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"过滤器搜索错误：{e}")
            return []
    
    def get_by_id(self, doc_id: str) -> Optional[Dict]:
        """根据 ID 获取文档"""
        if not self.collection:
            return None
        
        try:
            results = self.collection.get(
                ids=[doc_id],
                include=['document', 'metadata']
            )
            
            if results['ids'] and len(results['ids'][0]) > 0:
                return {
                    'id': results['ids'][0][0],
                    'text': results['documents'][0][0],
                    'metadata': results['metadatas'][0][0]
                }
            
            return None
            
        except Exception as e:
            print(f"获取文档错误：{e}")
            return None
    
    def update_document(self, doc_id: str, new_text: str) -> bool:
        """更新文档"""
        if not self.collection:
            return False
        
        try:
            self.collection.update(
                ids=[doc_id],
                documents=[new_text]
            )
            return True
        except Exception as e:
            print(f"更新文档错误：{e}")
            return False
    
    def delete_document(self, doc_id: str) -> bool:
        """删除文档"""
        if not self.collection:
            return False
        
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"删除文档错误：{e}")
            return False
    
    def count(self) -> int:
        """返回文档数量"""
        if not self.collection:
            return 0
        return self.collection.count()
    
    def list_collections(self) -> List[str]:
        """列出所有集合"""
        if not self.client:
            return []
        return [col.name for col in self.client.list_collections()]
    
    def get_statistics(self) -> Dict:
        """获取数据库统计信息"""
        if not self.collection:
            return {"total_documents": 0}
        
        all_docs = self.collection.get(include=['metadata'])
        
        # 按类型统计
        type_counts = {}
        source_counts = {}
        for metadata in all_docs['metadatas']:
            doc_type = metadata.get('type', 'unknown')
            source = metadata.get('source', 'unknown')
            
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
            source_counts[source] = source_counts.get(source, 0) + 1
        
        return {
            "total_documents": self.count(),
            "by_type": type_counts,
            "by_source": source_counts,
            "created_at": datetime.now().isoformat()
        }


class HybridSearchEngine:
    """混合检索引擎（关键词 + 向量 + 过滤器）"""
    
    def __init__(self, vector_db: ChromaVectorDB):
        self.vector_db = vector_db
    
    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None,
        keywords: Optional[List[str]] = None
    ) -> List[Dict]:
        """混合搜索：关键词 + 向量 + 过滤器"""
        results = []
        
        # 1. 向量搜索
        vector_results = self.vector_db.search(
            query=query,
            top_k=top_k * 2,  # 获取更多结果用于融合
            filters=filters
        )
        
        # 2. 关键词搜索（如果提供了关键词）
        if keywords:
            keyword_filters = {
                'keywords': {'$contains': keywords[0]}
            } if filters else {'keywords': {'$contains': keywords[0]}}
            keyword_results = self.vector_db.search_by_filters(
                filters=keyword_filters,
                top_k=top_k
            )
            vector_results.extend(keyword_results)
        
        # 3. 去重和融合
        seen_ids = set()
        merged_results = []
        
        for result in vector_results:
            if result['id'] not in seen_ids:
                seen_ids.add(result['id'])
                # 计算综合得分
                score = result.get('relevance_score', 0)
                if 'distance' in result:
                    score = 1 - result['distance']
                
                result['relevance_score'] = score
                merged_results.append(result)
        
        # 4. 排序并返回
        merged_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return merged_results[:top_k]


# 测试
if __name__ == "__main__":
    from pathlib import Path
    
    # 初始化
    db = ChromaVectorDB()
    engine = HybridSearchEngine(db)
    
    print("=" * 60)
    print("测试：添加文档")
    print("=" * 60)
    
    test_docs = [
        {
            'text': '鸿门宴是秦末重要政治事件，刘邦项羽对峙',
            'source': '鸿门宴',
            'type': 'event',
            'people': ['刘邦', '项羽', '范增'],
            'events': ['鸿门宴'],
            'keywords': ['鸿门宴', '政治', '对峙']
        },
        {
            'text': '刘邦建立汉朝，成为中国历史上重要朝代',
            'source': '建立汉朝',
            'type': 'event',
            'people': ['刘邦'],
            'events': ['建立汉朝'],
            'keywords': ['汉朝', '刘邦', '建立']
        },
        {
            'text': '项羽勇猛无敌，是秦末著名军事家',
            'source': '项羽',
            'type': 'character',
            'people': ['项羽'],
            'events': ['巨鹿之战'],
            'keywords': ['项羽', '军事', '勇猛']
        }
    ]
    
    count = db.add_documents(test_docs)
    print(f"✓ 添加 {count} 个文档")
    
    print("\n" + "=" * 60)
    print("测试：向量搜索")
    print("=" * 60)
    results = db.search('鸿门宴 刘邦', top_k=3)
    for r in results:
        print(f"相似度：{r['relevance_score']:.3f}")
        print(f"文本：{r['text'][:50]}...")
        print(f"元数据：{r['metadata']}")
        print()
    
    print("\n" + "=" * 60)
    print("测试：混合搜索")
    print("=" * 60)
    hybrid_results = engine.hybrid_search(
        query='项羽 勇猛',
        top_k=3,
        keywords=['项羽']
    )
    for r in hybrid_results:
        print(f"相似度：{r['relevance_score']:.3f}")
        print(f"文本：{r['text'][:50]}...")
        print(f"元数据：{r['metadata']}")
        print()
    
    print("\n" + "=" * 60)
    print("测试：数据库统计")
    print("=" * 60)
    stats = db.get_statistics()
    print(json.dumps(stats, indent=2))
