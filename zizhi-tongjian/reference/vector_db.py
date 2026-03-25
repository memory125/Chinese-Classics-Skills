#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 - RAG 检索增强引擎
实现：向量数据库 + 文本分割 + 检索功能
"""

import json
import hashlib
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import re
import math

class TextSplitter:
    """智能文本分割器"""
    
    @staticmethod
    def split_chinese_text(text: str, max_length: int = 1000) -> List[str]:
        """
        将中文文本智能分割成多个段落
        保持语义完整性，避免在句子中间切断
        """
        if len(text) <= max_length:
            return [text]
        
        segments = []
        # 分割点：句号、问号、感叹号、分段符
        split_pattern = r'(?<=[。！？])|(?<=[\n\r])'
        parts = re.split(split_pattern, text)
        
        current_segment = ""
        for part in parts:
            if len(current_segment) + len(part) <= max_length:
                current_segment += part
            else:
                if current_segment.strip():
                    segments.append(current_segment.strip())
                current_segment = part
        
        if current_segment.strip():
            segments.append(current_segment.strip())
        
        return segments
    
    @staticmethod
    def extract_key_segments(text: str, num_segments: int = 5) -> List[str]:
        """
        提取关键段落（每段开头或结尾的摘要性文字）
        用于快速检索和摘要
        """
        segments = re.split(r'(?<=[。！？])', text)
        if len(segments) <= num_segments:
            return segments
        
        # 取前 num_segments 个和后 num_segments 个关键段落
        key_segments = segments[:num_segments] + segments[-num_segments:]
        return key_segments


class TextVectorizer:
    """简单文本向量化 - 基于 TF-IDF 思想"""
    
    def __init__(self):
        self.vocabulary = {}
        self.idf_scores = {}
        self.vector_count = 0
    
    def _tokenize(self, text: str) -> List[str]:
        """中文分词（简化版：按字符和词组）"""
        # 简单实现：提取 2-4 字符的词组
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        return words if words else list(text)
    
    def fit(self, documents: List[str]) -> None:
        """建立词汇表和 IDF 分数"""
        doc_freq = {}  # 每个词出现在多少文档中
        doc_lengths = []
        
        # 第一阶段：统计词频
        for doc in documents:
            words = self._tokenize(doc)
            doc_lengths.append(len(words))
            word_set = set(words)
            for word in word_set:
                doc_freq[word] = doc_freq.get(word, 0) + 1
        
        # 第二阶段：计算 IDF
        n_docs = len(documents)
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(doc_freq.keys()))}
        
        for word, freq in doc_freq.items():
            # IDF = log((N+1)/(df+1)) + 1 (平滑处理)
            self.idf_scores[word] = math.log((n_docs + 1) / (freq + 1)) + 1
        
        self.doc_lengths = doc_lengths
    
    def transform(self, documents: List[str]) -> List[Dict]:
        """将文档转换为向量"""
        vectors = []
        
        for doc in documents:
            words = self._tokenize(doc)
            if not words:
                continue
            
            # TF-IDF 向量
            tf_scores = {}
            for word in words:
                tf_scores[word] = tf_scores.get(word, 0) + 1
            
            # 归一化 TF
            max_tf = max(tf_scores.values()) if tf_scores else 1
            for word in tf_scores:
                tf_scores[word] /= max_tf
            
            # 构建向量表示（简化：用词组和 TF-IDF 分数）
            vector = {
                'doc_id': self.vector_count,
                'text': doc,
                'keywords': list(tf_scores.keys()),
                'tf_idf': {
                    word: tf_scores.get(word, 0) * self.idf_scores.get(word, 0)
                    for word in tf_scores
                    if self.idf_scores.get(word, 0) > 0
                },
                'length': len(doc)
            }
            vectors.append(vector)
            self.vector_count += 1
        
        # 保存向量到实例属性，供 search() 使用
        self.vectors = vectors
        
        return vectors
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索查询向量"""
        query_words = self._tokenize(query)
        if not query_words:
            return []
        
        # 计算查询词频
        tf_scores = {}
        for word in query_words:
            tf_scores[word] = tf_scores.get(word, 0) + 1
        
        max_tf = max(tf_scores.values()) if tf_scores else 1
        for word in tf_scores:
            tf_scores[word] /= max_tf
        
        # 计算与每个文档的相似度（余弦相似度简化版）
        scores = []
        for vector in self.vectors:
            score = 0
            for word, tf in tf_scores.items():
                if word in vector['tf_idf']:
                    score += tf * vector['tf_idf'][word]
            scores.append((score, vector))
        
        # 排序并返回 top_k
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]


class RAGSearchEngine:
    """RAG 检索引擎"""
    
    def __init__(self, reference_path: str):
        self.reference_path = Path(reference_path)
        self.vectorizer = TextVectorizer()
        self.documents = []
        self.vectors = []
        self.known_cases = {}
        self._load_documents()
    
    def _load_documents(self):
        """加载所有文档并进行向量化"""
        texts = []
        
        # 加载案例库 - reference/ 的父目录是 skills/zizhi-tongjian，案例库在 references/ (多一个 s)
        base_path = Path(self.reference_path).parent.parent
        case_library_path = base_path / "references" / "case-library"
        
        print(f"🔍 查找案例库：{case_library_path}")
        print(f"   存在性：{case_library_path.exists()}")
        
        if case_library_path.exists():
            for file in case_library_path.glob("*.md"):
                try:
                    content = file.read_text(encoding='utf-8')
                    texts.append({
                        'source': file.name.replace('.md', ''),
                        'content': content,
                        'type': 'case'
                    })
                    print(f"   ✓ 加载：{file.name}")
                except Exception as e:
                    print(f"   ✗ 错误 {file}: {e}")
        
        # 加载人物索引
        char_index = self.reference_path / "character-index.md"
        if char_index.exists():
            try:
                content = char_index.read_text(encoding='utf-8')
                texts.append({
                    'source': 'character-index',
                    'content': content,
                    'type': 'character'
                })
            except Exception as e:
                print(f"Error loading character index: {e}")
        
        # 分割文档
        all_text = []
        for doc in texts:
            segments = TextSplitter.split_chinese_text(doc['content'])
            for i, segment in enumerate(segments):
                all_text.append({
                    'source': doc['source'],
                    'type': doc['type'],
                    'segment_id': f"{doc['source']}_seg{i}" if len(segments) > 1 else doc['source'],
                    'text': segment
                })
        
        # 向量化
        doc_texts = [d['text'] for d in all_text]
        self.vectorizer.fit(doc_texts)
        vectors_list = self.vectorizer.transform(doc_texts)
        
        # 保存向量到实例属性，供 search() 使用
        self.vectors = vectors_list
        
        print(f"✓ 已加载 {len(all_text)} 个文档分段，已建立 {len(self.vectorizer.vocabulary)} 个词汇项")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        搜索相关文档
        """
        if not self.vectors:
            return []
        
        results = self.vectorizer.search(query, top_k)
        
        formatted_results = []
        for score, vector in results:
            formatted_results.append({
                'source': 'unknown',
                'segment_id': vector['doc_id'],
                'text': vector['text'],
                'keywords': vector['keywords'],
                'tf_idf_scores': {k: round(v, 3) for k, v in vector['tf_idf'].items()},
                'relevance_score': round(score, 3)
            })
        
        return formatted_results
    
    def get_case_by_name(self, case_name: str) -> Optional[Dict]:
        """通过案例名称精确获取"""
        if case_name in self.known_cases:
            return self.known_cases[case_name]
        
        # 从文档中搜索
        for vector in self.vectors:
            if case_name in vector['text']:
                return {
                    'name': case_name,
                    'content': vector['text'][:500],  # 限制长度
                    'found_from': vector['source']
                }
        
        return None


def create_vector_db_from_reference(reference_path: str = None):
    """从 references 目录创建向量数据库"""
    if reference_path is None:
        reference_path = str(Path(__file__).parent / "reference")
    
    engine = RAGSearchEngine(reference_path)
    return engine


# 测试
if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).parent))
    
    print("测试 RAG 检索引擎...")
    engine = create_vector_db_from_reference()
    
    print("\n测试查询 1: '鸿门宴'")
    results = engine.search('鸿门宴', top_k=3)
    for r in results:
        print(f"相似度：{r['relevance_score']}")
        print(f"内容：{r['text'][:100]}...")
        print()
    
    print("\n测试查询 2: '向上管理 猜忌'")
    results = engine.search('向上管理 猜忌', top_k=3)
    for r in results:
        print(f"相似度：{r['relevance_score']}")
        print(f"内容：{r['text'][:100]}...")
        print()
