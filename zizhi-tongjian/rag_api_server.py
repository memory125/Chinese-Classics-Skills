#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG API 服务器 - 为 Web 界面提供 RESTful API (带 CORS 支持) v5.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from scripts.rag_enhanced_v5 import EnhancedRAGSearch

class RAGAPIHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """设置 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
    
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/search':
            query = parsed_path.query.split('=')[1] if '=' in parsed_path.query else ''
            query = urllib.parse.unquote(query)
            
            # 调用 RAG v5.0 系统 (精准匹配优化版)
            rag = EnhancedRAGSearch()
            results = rag.hybrid_search(query, top_k=5)
            
            # 格式化结果
            formatted_results = []
            for r in results:
                case_data = rag.case_db.get(r['name'], {})
                
                formatted_result = {
                    'name': r['name'],
                    'score': float(r['score']),
                    'method': r['method'],
                    'title': case_data.get('title', ''),
                    'wisdom': case_data.get('key_wisdom', ''),
                    'applications': case_data.get('modern_applications', []),
                    'related': [],
                    'precision_score': r.get('precision_score', 0)
                }
                
                # 添加相关案例
                related = rag.get_related_cases(r['name'], limit=2)
                formatted_result['related'] = [
                    {'name': r['name'], 'relevance': r['relevance'], 'score': r['score']}
                    for r in related
                ]
                
                formatted_results.append(formatted_result)
            
            # 返回 JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(formatted_results, ensure_ascii=False).encode())
        
        else:
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[API] {args[0]}")

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8081), RAGAPIHandler)
    print("🚀 RAG API Server v5.0 running on http://localhost:8081 (CORS enabled)")
    server.serve_forever()
