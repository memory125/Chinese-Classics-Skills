#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
意图识别系统 - AI 对话助手核心

功能：
1. 关键词匹配规则引擎 (快速，无需训练) ✅
2. 上下文理解机制 🔥 **新增**
3. 多轮对话管理 🔥 **新增**
4. 置信度评分 🔥 **新增**
"""

import re
from typing import Dict, List, Optional, Tuple


class IntentClassifier:
    """意图识别器"""
    
    def __init__(self):
        # 定义意图分类规则
        self.intent_rules = {
            'search': {
                'keywords': ['搜索', '查找', '查询', '找', '有没有', '哪些'],
                'patterns': [
                    r'.*搜索.*',
                    r'.*查找.*',
                    r'.*查询.*',
                    r'.*谁.*',
                    r'.*什么.*'
                ],
                'description': '用户想要搜索历史案例或信息'
            },
            
            'translate': {
                'keywords': ['翻译', '什么意思', '解释', '怎么读', '读音'],
                'patterns': [
                    r'.*翻译.*',
                    r'.*什么意思.*',
                    r'.*解释.*',
                    r'.*文言文.*',
                    r'.*古文.*'
                ],
                'description': '用户想要翻译文言文或查询字词含义'
            },
            
            'character': {
                'keywords': ['人物', '谁', '历史人物', '传记', '生平'],
                'patterns': [
                    r'.*(刘邦|项羽|诸葛亮|曹操|李世民).*',
                    r'.*人物.*',
                    r'.*传记.*',
                    r'.*生平.*'
                ],
                'description': '用户想要查询历史人物信息'
            },
            
            'wisdom': {
                'keywords': ['智慧', '启示', '教训', '经验', '今日锦囊'],
                'patterns': [
                    r'.*智慧.*',
                    r'.*启示.*',
                    r'.*教训.*',
                    r'.*经验.*',
                    r'.*今天.*'
                ],
                'description': '用户想要获取历史智慧或今日锦囊'
            },
            
            'simulator': {
                'keywords': ['模拟', '如果', '假如', '选择', '决策'],
                'patterns': [
                    r'.*如果.*',
                    r'.*假如.*',
                    r'.*选择.*',
                    r'.*决策.*',
                    r'.*历史沙盘.*'
                ],
                'description': '用户想要进行历史事件模拟'
            },
            
            'relationship': {
                'keywords': ['关系', '盟友', '敌人', '联系', '路径'],
                'patterns': [
                    r'.*(刘邦|项羽).*和.*(诸葛亮|曹操).*',
                    r'.*关系.*',
                    r'.*盟友.*',
                    r'.*敌人.*'
                ],
                'description': '用户想要查询人物关系'
            },
            
            'timeline': {
                'keywords': ['时间线', '年代', '历史', '朝代'],
                'patterns': [
                    r'.*时间线.*',
                    r'.*年代.*',
                    r'.*朝代.*',
                    r'.*历史事件.*'
                ],
                'description': '用户想要查看历史时间线'
            },
            
            'greeting': {
                'keywords': ['你好', '您好', '在吗', '开始'],
                'patterns': [
                    r'^[你您].*[好么]',
                    r'^开始.*',
                    r'^你好.*'
                ],
                'description': '用户打招呼或开始对话'
            },
            
            'help': {
                'keywords': ['帮助', '怎么用', '功能', '有什么'],
                'patterns': [
                    r'.*帮助.*',
                    r'.*怎么用.*',
                    r'.*功能.*',
                    r'.*有什么.*'
                ],
                'description': '用户询问系统功能或使用方法'
            },
            
            'unknown': {
                'keywords': [],
                'patterns': [],
                'description': '无法识别的意图，需要澄清'
            }
        }
        
        # 上下文状态管理
        self.context = {}
    
    def classify(self, text: str) -> Dict:
        """分类用户输入
        
        Args:
            text: 用户输入的文本
            
        Returns:
            Dict: 包含意图和置信度的结果
        """
        
        best_intent = 'unknown'
        best_score = 0.0
        best_match_type = None
        
        # 1. 关键词匹配 (权重：0.6)
        keyword_score, matched_keywords = self._match_keywords(text)
        
        if keyword_score > best_score:
            best_score = keyword_score
            best_intent = 'search' if keyword_score > 0.5 else 'unknown'
            best_match_type = 'keyword'
        
        # 2. 正则模式匹配 (权重：0.8)
        pattern_score, matched_pattern = self._match_patterns(text)
        
        if pattern_score > best_score:
            best_score = pattern_score
            best_intent = self._get_intent_from_pattern(matched_pattern)
            best_match_type = 'pattern'
        
        # 3. 上下文感知 (权重：0.9)
        context_score, context_intent = self._use_context(text)
        
        if context_score > best_score:
            best_score = context_score
            best_intent = context_intent
            best_match_type = 'context'
        
        # 4. 特殊处理
        if best_score < 0.3:
            best_intent = 'unknown'
            best_score = 0.2
        
        return {
            "intent": best_intent,
            "confidence": min(best_score, 1.0),
            "match_type": best_match_type,
            "matched_keywords": matched_keywords if matched_keywords else [],
            "matched_pattern": matched_pattern if matched_pattern else None
        }
    
    def _match_keywords(self, text: str) -> Tuple[float, List[str]]:
        """关键词匹配"""
        
        text_lower = text.lower()
        matched_keywords = []
        score = 0.0
        
        for intent_name, rule in self.intent_rules.items():
            if intent_name == 'unknown':
                continue
            
            for keyword in rule['keywords']:
                if keyword in text_lower:
                    matched_keywords.append(keyword)
                    score += 0.2
        
        return min(score, 1.0), matched_keywords
    
    def _match_patterns(self, text: str) -> Tuple[float, Optional[str]]:
        """正则模式匹配"""
        
        text_lower = text.lower()
        best_pattern = None
        best_score = 0.0
        
        for intent_name, rule in self.intent_rules.items():
            if intent_name == 'unknown':
                continue
            
            for pattern in rule['patterns']:
                try:
                    if re.search(pattern, text_lower):
                        score = 0.8  # 模式匹配权重较高
                        if score > best_score:
                            best_score = score
                            best_pattern = intent_name
                except re.error:
                    continue
        
        return best_score, best_pattern
    
    def _get_intent_from_pattern(self, pattern: str) -> str:
        """从匹配的模式获取意图"""
        
        # 特殊处理人物查询
        if 'character' in pattern and any(char in pattern for char in ['刘邦', '项羽', '诸葛亮']):
            return 'character'
        
        return pattern
    
    def _use_context(self, text: str) -> Tuple[float, str]:
        """上下文感知"""
        
        # 检查是否是对前一个问题的延续
        if self.context.get('last_intent'):
            last_intent = self.context['last_intent']
            
            # 如果用户继续追问，保持相同意图
            continuation_keywords = ['然后', '还有', '另外', '为什么', '怎么样']
            text_lower = text.lower()
            
            if any(kw in text_lower for kw in continuation_keywords):
                return 0.9, last_intent
        
        # 检查是否引用了之前提到的内容
        if self.context.get('last_character'):
            character = self.context['last_character']
            if character in text:
                return 0.85, 'character'
        
        return 0.0, None
    
    def update_context(self, intent: str, extracted_data: Dict):
        """更新上下文状态
        
        Args:
            intent: 识别的意图
            extracted_data: 提取的数据 (如人物名、关键词等)
        """
        
        # 保存最后意图
        self.context['last_intent'] = intent
        
        # 提取人物名
        if 'character' in intent or 'relationship' in intent:
            characters = self._extract_characters(extracted_data.get('text', ''))
            if characters:
                self.context['last_character'] = characters[0]
        
        # 保存搜索关键词
        if intent == 'search':
            keywords = extracted_data.get('keywords', [])
            if keywords:
                self.context['last_search_keywords'] = keywords
    
    def _extract_characters(self, text: str) -> List[str]:
        """从文本中提取人物名"""
        
        known_characters = [
            '刘邦', '项羽', '诸葛亮', '曹操', '刘备', '孙权',
            '李世民', '赵匡胤', '宋徽宗', '明英宗', '光绪帝'
        ]
        
        found_chars = []
        for char in known_characters:
            if char in text:
                found_chars.append(char)
        
        return found_chars
    
    def extract_query(self, text: str, intent: str) -> Optional[str]:
        """从用户输入中提取查询内容
        
        Args:
            text: 原始文本
            intent: 识别的意图
            
        Returns:
            Optional[str]: 提取的查询内容
        """
        
        if intent == 'search':
            # 移除关键词，保留核心查询
            keywords = ['搜索', '查找', '查询', '找']
            query = text
            
            for kw in keywords:
                query = query.replace(kw, '').strip()
            
            return query
        
        elif intent == 'translate':
            # 提取需要翻译的文言文
            keywords = ['翻译', '什么意思', '解释']
            query = text
            
            for kw in keywords:
                query = query.replace(kw, '').strip()
            
            return query
        
        elif intent == 'character':
            # 提取人物名
            characters = self._extract_characters(text)
            if characters:
                return characters[0]
        
        return text
    
    def get_help_message(self) -> str:
        """获取帮助信息"""
        
        help_text = """
📚 **资治通鉴 Skill - 历史智慧助手**

我可以帮您：

1. 🔍 **搜索历史案例**: "搜索如虎添翼"、"查找刘邦的故事"
2. 📖 **翻译文言文**: "翻译刘豫州王室之胄"、"什么意思"
3. 👤 **查询人物档案**: "诸葛亮的人物传记"、"曹操的生平"
4. 📅 **获取今日锦囊**: "今天的智慧"、"有什么历史启示"
5. 🎮 **模拟历史事件**: "如果鸿门宴项羽杀了刘邦会怎样"
6. 🔗 **查询人物关系**: "刘邦和项羽的关系"

请告诉我您想了解什么！
"""
        
        return help_text.strip()


# 测试
if __name__ == "__main__":
    classifier = IntentClassifier()
    
    print("=" * 80)
    print("🤖 意图识别系统测试")
    print("=" * 80)
    
    test_cases = [
        "搜索如虎添翼",
        "翻译刘豫州王室之胄",
        "诸葛亮的人物传记",
        "今天的智慧是什么",
        "如果鸿门宴项羽杀了刘邦会怎样",
        "刘邦和项羽的关系",
        "你好"
    ]
    
    print("\n📝 测试用例:\n")
    
    for i, text in enumerate(test_cases, 1):
        result = classifier.classify(text)
        
        print(f"{i}. {text}")
        print(f"   🎯 意图：{result['intent']} (置信度：{result['confidence']:.2f})")
        print(f"   💡 匹配方式：{result['match_type']}")
        
        if result.get('matched_keywords'):
            print(f"   🔑 关键词：{', '.join(result['matched_keywords'])}")
        
        # 提取查询内容
        query = classifier.extract_query(text, result['intent'])
        if query and query != text:
            print(f"   📝 提取的查询：{query}")
        
        print()
