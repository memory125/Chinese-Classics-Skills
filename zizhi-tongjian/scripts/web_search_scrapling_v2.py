#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络搜索模块 v2.0 - 使用 BeautifulSoup + Scrapling

功能：
1. DuckDuckGo HTML 解析 (BeautifulSoup)
2. Scrapling Fetcher 内容提取 (新 API)
3. AI 总结提取
4. 结构化数据生成
"""

import json
from typing import List, Dict, Optional
from pathlib import Path
import urllib.request
import urllib.parse
import re
from datetime import datetime

# 第三方库 - BeautifulSoup
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("⚠️ 未安装 beautifulsoup4")

# 第三方库 - Scrapling
try:
    from scrapling import DynamicFetcher
    HAS_SCRAPLING = True
except ImportError:
    HAS_SCRAPLING = False
    print("⚠️ 未安装 scrapling")


class WebSearchEngine:
    """网络搜索引擎 v2.0 (BeautifulSoup + Scrapling)"""
    
    def __init__(self):
        # BeautifulSoup
        if not HAS_BS4:
            print("⚠️ BeautifulSoup 不可用，使用正则解析 fallback")
        
        # Scrapling Fetcher - 新 API 配置
        if HAS_SCRAPLING:
            try:
                # 先配置，再创建实例 (修复警告)
                DynamicFetcher.configure(
                    render_wait=2,
                    timeout=15,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                self.fetcher = DynamicFetcher()
                print("✅ Scrapling Fetcher 已加载 (新 API)")
            except Exception as e:
                print(f"⚠️ Scrapling 配置失败：{e}")
                self.fetcher = None
        else:
            self.fetcher = None
        
        # DuckDuckGo 搜索 URL 模板
        self.ddg_base_url = "https://html.duckduckgo.com/html/"
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """多引擎搜索 + Scrapling 内容提取"""
        
        results = []
        
        # 1. DuckDuckGo HTML 搜索 (BeautifulSoup 解析)
        ddg_results = self._search_ddg_html(query, limit=top_k)
        results.extend(ddg_results)
        
        print(f"   📄 DuckDuckGo 找到 {len(ddg_results)} 个结果")
        
        # 2. 使用 Scrapling 抓取详细内容 (如果启用且结果存在)
        if self.fetcher and len(results) > 0:
            detailed_results = []
            
            for r in results[:top_k]:
                url = r.get('url', '')
                
                try:
                    # 使用 Scrapling Fetcher 抓取页面内容 (新 API)
                    response = self.fetcher.get(
                        url,
                        render_wait=2,
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        # 提取主要内容
                        content = self._extract_content(response)
                        
                        r['content'] = content[:800]  # 限制长度
                        r['score'] = 0.9  # Scrapling 抓取的内容高分
                        
                        detailed_results.append(r)
                except Exception as e:
                    print(f"   ⚠️ Scrapling 抓取失败 {url}: {e}")
            
            results = detailed_results if detailed_results else results
        
        return results[:top_k]
    
    def _search_ddg_html(self, query: str, limit: int) -> List[Dict]:
        """DuckDuckGo HTML 搜索 (BeautifulSoup 解析)"""
        
        url = f"{self.ddg_base_url}?q={urllib.parse.quote(query)}"
        
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                
                if HAS_BS4:
                    # 使用 BeautifulSoup 解析 (推荐)
                    return self._parse_with_bs4(html, limit)
                else:
                    # 回退到正则解析
                    return self._parse_with_regex(html, limit)
                    
        except Exception as e:
            print(f"⚠️ DuckDuckGo 搜索失败：{e}")
            return []
    
    def _parse_with_bs4(self, html: str, limit: int) -> List[Dict]:
        """使用 BeautifulSoup 解析 HTML"""
        
        soup = BeautifulSoup(html, 'lxml')
        results = []
        
        # 查找所有结果项
        for item in soup.find_all('div', class_='result'):
            link = item.find('a', class_='result__a')
            
            if link:
                url = link.get('href', '')
                title = link.get_text().strip()
                
                # 查找 snippet
                snippet_div = item.find('div', class_='result__snippet')
                content = snippet_div.get_text().strip() if snippet_div else ''
                
                results.append({
                    'source': 'duckduckgo',
                    'title': title,
                    'url': url,
                    'content': content[:500],  # 初始内容 (snippet)
                    'score': 0.7
                })
                
                if len(results) >= limit:
                    break
        
        return results
    
    def _parse_with_regex(self, html: str, limit: int) -> List[Dict]:
        """使用正则表达式解析 HTML (fallback)"""
        
        # 匹配结果项 (DuckDuckGo HTML 格式)
        result_pattern = re.compile(
            r'<div class="result"><a class="result__a" href="(.*?)"[^>]*>(.*?)</a>'
            r'[\s\S]*?<div class="result__snippet">(.*?)</div>',
            re.DOTALL
        )
        
        results = []
        
        for match in result_pattern.finditer(html):
            url = match.group(1)
            title = match.group(2).strip()
            snippet = match.group(3).strip()
            
            results.append({
                'source': 'duckduckgo',
                'title': title,
                'url': url,
                'content': snippet[:500],
                'score': 0.7
            })
            
            if len(results) >= limit:
                break
        
        return results
    
    def _extract_content(self, response) -> str:
        """使用 Scrapling Fetcher 提取页面主要内容"""
        
        # 1. 提取文本内容
        text = response.text
        
        # 2. 移除不需要的元素 (脚本、样式等)
        unwanted_tags = ['script', 'style', 'nav', 'footer', 'header']
        for tag in unwanted_tags:
            text = re.sub(rf'<{tag}[^>]*>[\s\S]*?</{tag}>', '', text, flags=re.IGNORECASE)
        
        # 3. 提取主要段落
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL | re.IGNORECASE)
        
        # 4. 合并主要内容 (前 10-20 个段落)
        main_content = []
        for p in paragraphs[:15]:
            clean_p = re.sub(r'\s+', ' ', p).strip()
            if len(clean_p) > 50:  # 过滤太短的段落
                main_content.append(clean_p)
        
        return '\n\n'.join(main_content)


class CaseGenerator:
    """案例生成器 - 将网络搜索结果转换为 cases.json 格式"""
    
    def __init__(self):
        self.web_search = WebSearchEngine()
    
    def generate_case_from_query(self, query: str) -> Optional[Dict]:
        """根据查询生成新案例"""
        
        print(f"🔍 正在搜索：'{query}'...")
        
        # 1. 网络搜索
        search_results = self.web_search.search(query, top_k=3)
        
        if not search_results:
            print("⚠️ 未找到相关搜索结果")
            return None
        
        print(f"✅ 找到 {len(search_results)} 个搜索结果")
        
        # 2. 提取关键信息
        title = f"{query} - 历史智慧与现代启示"
        wisdom_parts = []
        background_parts = []
        source_urls = []
        
        for r in search_results:
            content = r.get('content', '')
            url = r.get('url', '')
            
            if url:
                source_urls.append(url)
            
            # 提取核心智慧 (关键词匹配)
            wisdom_keywords = ['智慧', '启示', '经验', '教训', '关键']
            for keyword in wisdom_keywords:
                if keyword in content:
                    # 查找包含关键词的句子
                    sentences = re.split(r'[。！？]', content)
                    for sent in sentences:
                        if keyword in sent and len(sent) > 20:
                            wisdom_parts.append(sent.strip())
            
            # 提取背景信息
            if "历史" in content or "故事" in content or "背景" in content:
                background_parts.append(content[:300])
        
        # 3. 构建核心智慧 (去重 + 精简)
        wisdom = ' '.join(list(set(wisdom_parts)))[:500]
        
        if not wisdom:
            wisdom = f"{query}的历史智慧：通过研究相关历史事件和故事，提取其中的核心智慧和启示。"
        
        # 4. 构建背景描述
        background = ' '.join(background_parts)[:800]
        
        if not background:
            background = f"关于'{query}'的网络搜索结果汇总，包含多个来源的信息和分析。"
        
        # 5. 生成现代应用建议 (基于查询主题)
        applications = [
            {
                'scenario': f"{query}在现代的应用",
                'action': "从历史智慧中学习应对策略和方法",
                'example': "将古代智慧应用到现代决策、管理或生活中"
            },
            {
                'scenario': "危机处理与转机把握",
                "action": "识别危机中的机会，化险为夷",
                'example': "面对困难时保持乐观，寻找突破口"
            }
        ]
        
        # 6. 构建案例数据
        case_data = {
            'title': title,
            'volume': f'网络搜索结果·{query}',
            'dynasty': '现代',
            'year': datetime.now().strftime('%Y 年'),
            'key_wisdom': wisdom,
            'modern_applications': applications,
            'protagonists': [query],
            'background': background,
            'source_urls': source_urls[:5]  # 最多记录 5 个来源
        }
        
        return case_data
    
    def save_to_cases_json(self, case_name: str, case_data: Dict):
        """保存到 cases.json"""
        json_path = Path(__file__).parent.parent / "data" / "cases.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # 添加新案例
        cases[case_name] = case_data
        
        # 保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(cases, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已保存到 {json_path}")


# 测试
if __name__ == "__main__":
    generator = CaseGenerator()
    
    # 测试搜索
    print("=== 测试：网络搜索 ===")
    results = generator.web_search.search("三国鼎立", top_k=3)
    for i, r in enumerate(results[:2], 1):
        title = r.get('title', 'N/A')
        source = r.get('source', 'unknown')
        has_content = len(r.get('content', '')) > 100
        
        print(f"{i}. [{source}] {title[:50]}...")
        print(f"   内容长度：{len(r.get('content', ''))} 字符 | 抓取成功：{has_content}")
    
    # 测试生成案例
    print("\n=== 测试：生成案例 ===")
    case = generator.generate_case_from_query("三国鼎立")
    if case:
        print(f"✅ 生成案例：{case['title']}")
        print(f"   智慧：{case['key_wisdom'][:100]}...")
