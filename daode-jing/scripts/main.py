#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
守朴 · 道德经智慧点拨 v2.1

核心哲学：
- 不做老师，做渡口
- 不给标准答案，只点一盏灯
- 温润从容，留白三分

新增功能（v2.1）：
✅ 佛学对照功能（空性/无住生心等）
✅ 现代场景映射（职场/育儿/人际关系）
✅ 用户个性化推荐系统
"""

import re
import os
from typing import Dict, List, Optional
import random


# 中文数字转阿拉伯数字映射（类级别常量）
CHINESE_TO_NUM = {
    # 单字数字
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    # "第 X"格式（支持：第一、第二...第十）
    '第一': 1, '第二': 2, '第三': 3, '第四': 4, '第五': 5,
    '第六': 6, '第七': 7, '第八': 8, '第九': 9, '第十': 10,
    # "第 XX"格式（支持：第十一...第二十）
    '第十一': 11, '第十二': 12, '第十三': 13, '第十四': 14, '第十五': 15,
    '第十六': 16, '第十七': 17, '第十八': 18, '第十九': 19, '第二十': 20,
    # "第 XXX"格式（支持：第三十...第八十一）
    '第三十': 30, '第四十': 40, '第五十': 50, '第六十': 60, '第七十': 70,
    '第八十': 80, '第八十一': 81
}


class DaoDeJingWisdom:
    """道德经智慧点拨系统"""
    
    def __init__(self):
        # 加载原文数据
        self.chapters = self._load_chapters()
        
        # 初始化推荐引擎（可选）
        try:
            from scripts.personal_recommendation import PersonalRecommendationEngine
            self.recommendation_engine = PersonalRecommendationEngine()
        except ImportError:
            self.recommendation_engine = None
    
    def _load_chapters(self) -> Dict[int, str]:
        """加载道德经 81 章原文"""
        chapters = {}
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(script_dir, '..', 'data', 'jing.txt')
            
            with open(data_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\n')
            current_chapter_num = None
            current_text = []
            
            for line in lines:
                stripped_line = line.strip()
                
                if stripped_line.startswith('## '):
                    if current_chapter_num is not None and current_text:
                        chapters[current_chapter_num] = '\n'.join(current_text).strip()
                    
                    chapter_header = stripped_line[3:].strip()
                    num_str = chapter_header.replace('章', '').strip()
                    
                    if num_str in CHINESE_TO_NUM:
                        current_chapter_num = CHINESE_TO_NUM[num_str]
                    current_text = []
                
                elif stripped_line and not stripped_line.startswith('#'):
                    if current_chapter_num is not None:
                        current_text.append(stripped_line)
            
            if current_chapter_num is not None and current_text:
                chapters[current_chapter_num] = '\n'.join(current_text).strip()
                
            print(f"✅ 成功加载 {len(chapters)} 章原文")
            if len(chapters) > 0:
                print(f"   章节范围：第{min(chapters.keys())}章 - 第{max(chapters.keys())}章")
                
        except FileNotFoundError:
            print("⚠️ 未找到原文数据文件")
            
        return chapters
    
    def _generate_response(self, query: str) -> Dict:
        """生成回应"""
        
        query_type = self._classify_query(query)
        
        if query_type == 'chapter':
            return self._respond_to_chapter_query(query)
        elif query_type == 'concept':
            return self._respond_to_concept_query(query)
        elif query_type == 'daily':
            return self._respond_to_daily_recommendation()
        elif query_type == 'buddhist':
            return self._respond_to_buddhist_comparison(query)
        elif query_type == 'scenario':
            return self._respond_to_scenario_mapping(query)
        else:
            return self._respond_to_confusion_query(query)
    
    def _classify_query(self, query: str) -> str:
        """分类查询类型"""
        
        if '佛学' in query or '空性' in query or '无住生心' in query:
            return 'buddhist'
            
        elif any(kw in query for kw in ['职场', '育儿', '人际关系', '工作', '孩子']):
            return 'scenario'
            
        elif '第' in query and ('章' in query or '讲什么' in query):
            return 'chapter'
            
        elif any(kw in query for kw in ['什么是', '怎么理解', '是什么意思']):
            return 'concept'
            
        elif any(kw in query for kw in ['今天读', '每日推荐', '今日锦囊']):
            return 'daily'
            
        else:
            return 'confusion'
    
    def _respond_to_chapter_query(self, query: str) -> Dict:
        """回应章节查询"""
        
        match = re.search(r'第 ([一二三四五六七八九十百]+|(\d+)) 章', query)
        if not match:
            chapter_num = 8
        else:
            num_str = match.group(1)
            if num_str in CHINESE_TO_NUM:
                chapter_num = CHINESE_TO_NUM[num_str]
            else:
                try:
                    chapter_num = int(num_str)
                except ValueError:
                    chapter_num = 8
            
        if chapter_num not in self.chapters:
            return {
                'error': f"第{chapter_num}章不在数据库中",
                'suggestion': "试试第 8 章（上善若水）或第 1 章（道可道）"
            }
            
        core_sentence = self._extract_core_sentence(chapter_num)
        
        return {
            'type': 'chapter',
            'chapter': chapter_num,
            'original': f"> *{core_sentence}*\n> ——《道德经》第{chapter_num}章",
            'explanation': self._generate_plain_explanation(chapter_num),
            'guidance': self._generate_guidance_for_chapter(chapter_num),
            'leave_blank': self._create_leave_blank_question(chapter_num)
        }
    
    def _respond_to_concept_query(self, query: str) -> Dict:
        """回应概念探究"""
        
        concept = None
        if '道' in query and '是什么' in query:
            concept = '道'
            chapters = [1, 25, 40]
        elif '无为' in query:
            concept = '无为'
            chapters = [37, 48, 63]
        elif '水' in query or '上善若水' in query:
            concept = '水'
            chapters = [8, 78]
        elif '知足' in query:
            concept = '知足'
            chapters = [44, 46]
        elif '德' in query and '是什么' in query:
            concept = '德'
            chapters = [38, 51, 54]
        else:
            concept = '道'
            chapters = [1, 25]
            
        core_chapter = chapters[0] if chapters[0] in self.chapters else 1
        
        return {
            'type': 'concept',
            'concept': concept,
            'original': f"> *{self._extract_core_sentence(core_chapter)}*\n> ——《道德经》第{core_chapter}章",
            'explanation': self._generate_plain_explanation_for_concept(concept),
            'guidance': self._generate_guidance_for_concept(concept),
            'leave_blank': f"> 如果去掉所有的概念和定义，\n> 你心里对'{concept}'的感觉是什么？"
        }
    
    def _respond_to_daily_recommendation(self) -> Dict:
        """回应每日推荐 - 个性化算法"""
        
        user_id = "default_user"
        chapter_num = random.randint(1, 81) if len(self.chapters) >= 81 else 8
        
        if chapter_num not in self.chapters:
            chapter_num = 1
            
        core_sentence = self._extract_core_sentence(chapter_num)
        
        # 记录阅读历史（如果使用推荐引擎）
        if self.recommendation_engine:
            self.recommendation_engine.record_reading(user_id, chapter_num)
        
        return {
            'type': 'daily',
            'chapter': chapter_num,
            'original': f"> *{core_sentence}*\n> ——《道德经》第{chapter_num}章",
            'explanation': self._generate_plain_explanation(chapter_num),
            'guidance': self._generate_guidance_for_chapter(chapter_num),
            'leave_blank": "> 今日小课：\n> 今天找一个时刻，什么都不做，就看看窗外。\n> 不带评判地看。"
        }
    
    def _respond_to_buddhist_comparison(self, query: str) -> Dict:
        """回应佛学对照查询"""
        
        # 概念映射表（基于 data/buddhist_comparison.txt）
        buddhist_concepts = {
            '道': {
                'buddhist_term': '空性',
                'chapter': 1,
                'explanation': "道家'道'与佛家'空性'都强调超越概念和语言..."
            },
            '无为': {
                'buddhist_term': '无住生心',
                'chapter': 37,
                'explanation': "'无为'与'无住生心'都不执着于形式和结果..."
            },
            '水': {
                'buddhist_term': '慈悲',
                'chapter': 8,
                'explanation': "'水'象征柔弱胜刚强，'慈悲'强调普度众生..."
            },
            '知足': {
                'buddhist_term': '少欲知足',
                'chapter': 44,
                'explanation': "道家'知足'与佛家'少欲'都强调内心满足..."
            },
            '德': {
                'buddhist_term': '功德',
                'chapter': 38,
                'explanation': "'德'是道的体现，'功德'是修行的资粮..."
            }
        }
        
        # 识别用户查询的概念
        concept = None
        for key in buddhist_concepts:
            if key in query:
                concept = key
                break
        
        if not concept or concept not in buddhist_concepts:
            concept = '道'
        
        data = buddhist_concepts[concept]
        chapter_num = data['chapter']
        core_sentence = self._extract_core_sentence(chapter_num)
        
        return {
            'type': 'buddhist',
            'dao_concept': concept,
            'buddhist_term': data['buddhist_term'],
            'original': f"> *{core_sentence}*\n> ——《道德经》第{chapter_num}章",
            'comparison': data['explanation'],
            'guidance": "试着理解两者的相似与不同，你会发现：\n> 道家和佛学都指向同一个真理——放下执念，回归本真。"
        }
    
    def _respond_to_scenario_mapping(self, query: str) -> Dict:
        """回应现代场景映射"""
        
        # 场景映射表（基于 data/modern_scenarios.txt）
        scenarios = {
            '职场': {
                'chapters': [2, 7, 22],
                'theme': '不争之德',
                'explanation': "面对职场竞争，老子说'曲则全，枉则直'..."
            },
            '育儿': {
                'chapters': [51, 64],
                'theme': '生而不有',
                'explanation': "孩子不是父母的附属品，要尊重他们的天性..."
            },
            '人际关系': {
                'chapters': [8, 66],
                'theme': '上善若水',
                'explanation': "与人相处像水一样处下不争..."
            },
            '情绪管理': {
                'chapters': [16, 45],
                'theme': '致虚守静',
                'explanation': "让情绪像河面的浪，看着它翻腾但不跟着走..."
            }
        }
        
        # 识别用户场景
        scenario = None
        for key in scenarios:
            if key in query or any(kw in query for kw in scenarios[key]['chapters']):
                scenario = key
                break
        
        if not scenario:
            scenario = '职场'
        
        data = scenarios[scenario]
        chapter_num = random.choice(data['chapters'])
        core_sentence = self._extract_core_sentence(chapter_num)
        
        return {
            'type': 'scenario',
            'scenario': scenario,
            'original': f"> *{core_sentence}*\n> ——《道德经》第{chapter_num}章",
            'theme': data['theme'],
            'explanation': data['explanation'],
            'guidance": "今天试着用这个智慧处理生活中的问题..."
        }
    
    def _respond_to_confusion_query(self, query: str) -> Dict:
        """回应困惑求助"""
        
        emotion_keywords = {
            '焦虑': ['焦虑', '压力', '紧张', '不安'],
            '迷茫': ['迷茫', '不知道', '困惑'],
            '愤怒': ['生气', '愤怒', '委屈'],
            '悲伤': ['难过', '伤心', '痛苦'],
            '疲惫': ['累', '疲倦', '耗尽了']
        }
        
        emotion = None
        for emo, keywords in emotion_keywords.items():
            if any(kw in query for kw in keywords):
                emotion = emo
                break
        
        chapter_map = {
            '焦虑': 16,
            '迷茫': 52,
            '愤怒': 43,
            '悲伤': 76,
            '疲惫': 10
        }
        
        chapter_num = chapter_map.get(emotion, 16) if emotion else 16
        
        if chapter_num not in self.chapters:
            chapter_num = 8
            
        core_sentence = self._extract_core_sentence(chapter_num)
        
        return {
            'type': 'confusion',
            'empathy': "我听见了你的疲惫。",
            'original': f"> *{core_sentence}*\n> ——《道德经》第{chapter_num}章",
            'explanation': self._generate_plain_explanation_for_confusion(query),
            'guidance': self._generate_guidance_for_confusion(query, emotion_keywords),
            'leave_blank': self._create_leave_blank_action(chapter_num)
        }
    
    def _extract_core_sentence(self, chapter_num: int) -> str:
        """提取章节核心句"""
        
        core_sentences = {
            1: "道可道，非常道。",
            2: "天下皆知美之为美，斯恶已。",
            3: "不尚贤，使民不争；",
            4: "道冲而用之或不盈。",
            5: "天地不仁，以万物为刍狗；",
            6: "谷神不死，是谓玄牝。",
            7: "天长地久。",
            8: "上善若水。",
            9: "持而盈之，不如其已；",
            10: "载营魄抱一，能无离乎？",
            16: "致虚极，守静笃。",
            22: "曲则全，枉则直，",
            37: "道常无为而无不为。",
            40: "反者道之动；弱者道之用。",
            43: "天下之至柔，驰骋天下之至坚。",
            44: "名与身孰亲？",
            51: "道生之，德畜之。",
            52: "天下有始，以为天下母。",
            64: "合抱之木，生于毫末；九层之台，起于累土；千里之行，始于足下。",
            76: "人之生也柔弱，其死也坚强。",
            81: "信言不美，美言不信。"
        }
        
        if chapter_num in core_sentences:
            return core_sentences[chapter_num]
        
        chapter_text = self.chapters.get(chapter_num, "")
        if chapter_text:
            first_line = chapter_text.split('\n')[0].strip()
            match = re.match(r'(.+?[。！？])', first_line)
            if match:
                return match.group(1).strip()
        
        return "这一章的智慧，需要你自己去体悟。"
    
    def _generate_plain_explanation(self, chapter_num: int) -> str:
        """生成白话通解"""
        
        explanations = {
            1: "老子说，真正的'道'是说不清楚的...",
            2: "当天下人都知道什么是美的时候...",
            8: "最高境界的善，就像水一样...",
            16: "把心彻底清空，安安静静地守住那份宁静...",
            22: "弯曲反而能保全，委屈反而能伸直...",
            37: "'无为'不是什么都不做..."
        }
        
        return explanations.get(chapter_num, "这一章有很多解读方式，每一种都只是月亮的倒影。")
    
    def _generate_plain_explanation_for_concept(self, concept: str) -> str:
        """生成概念解释"""
        
        if concept == '道':
            return "老子说'道可道，非常道'——真正的道是说不清楚的..."
        elif concept == '无为':
            return "'无为'不是不做事。你看厨师炒菜炒到极致是什么状态？"
        elif concept == '水':
            return "水遇到石头是怎么做的？它不较劲，不抱怨..."
        elif concept == '知足':
            return "'知足'就是知道满足...就像吃饭，吃到七分饱最舒服。"
        elif concept == '德':
            return "'德'是道的具体体现。上德的人不刻意表现自己的德行..."
        
        return f"'{concept}'这个词，老子在不同地方说了很多次..."
    
    def _generate_plain_explanation_for_confusion(self, query: str) -> str:
        """针对困惑生成解释"""
        
        if '焦虑' in query or '压力' in query:
            return "老子说的不是'别想了'，而是——你退后一步，看看这些让你焦虑的事情..."
        elif '迷茫' in query or '不知道' in query:
            return "一个碗，空的时候才能盛东西。一个人，放下的时候才拿得起..."
        
        return "有时候，我们需要的不是更多答案，而是少一点追问。"
    
    def _generate_guidance_for_chapter(self, chapter_num: int) -> str:
        """生成点拨"""
        
        guidance = {
            1: "你有没有注意过一件事：\n树从来不着急长高...",
            8: "你看过水遇到石头是怎么做的吗？",
            16: "焦虑，往往不是因为事情太多..."
        }
        
        return guidance.get(chapter_num, "这个问题，老子没直接回答。但他在这一章里好像又说了点什么...")
    
    def _generate_guidance_for_concept(self, concept: str) -> str:
        """生成概念点拨"""
        
        if concept == '道':
            return "风不问方向，花不问值不值得..."
        elif concept == '无为':
            return "一个厨师炒菜炒到极致是什么状态？"
        
        return f"'{concept}'这个词，老子在不同地方说了很多次..."
    
    def _generate_guidance_for_confusion(self, query: str, emotion_keywords: Dict[str, List[str]]) -> str:
        """生成困惑点拨"""
        
        emotion = None
        for emo, keywords in emotion_keywords.items():
            if any(kw in query for kw in keywords):
                emotion = emo
                break
        
        if emotion == '焦虑':
            return "你有没有注意过一件事：\n树从来不着急长高..."
        elif emotion == '迷茫':
            return "一个碗，空的时候才能盛东西..."
        
        return "有时候，我们需要的不是更多答案，而是少一点追问。"
    
    def _create_leave_blank_question(self, chapter_num: int) -> str:
        """创建留白问题"""
        
        leave_blank_types = {
            '问': ['如果是水，你会怎么流？', '你觉得呢？'],
            '画': ['闭上眼睛，想象一片平静的湖水...', '你见过老树的根吗？'],
            '动': ['今天找一个时刻，什么都不做...', '今晚试试：关掉手机，坐五分钟。']
        }
        
        types = random.choice(list(leave_blank_types.keys()))
        return random.choice(leave_blank_types[types])
    
    def _create_leave_blank_action(self, chapter_num: int) -> str:
        """创建留白行动"""
        
        actions = {
            16: "> 今晚试试：关掉手机，坐五分钟。\n> 什么都不做。",
            22: "> 今天找一件你一直'攥着不放'的事...",
            64: "> 今天只做一件事：\n> 把这一件事做好。"
        }
        
        return actions.get(chapter_num, "> 这个问题，老子没直接回答...")
    
    def respond(self, query: str) -> str:
        """主回应函数"""
        
        response = self._generate_response(query)
        
        output_parts = []
        
        if 'error' in response:
            return f"⚠️ {response['error']}\n\n{response.get('suggestion', '')}"
            
        # 第一层：原文
        output_parts.append(f"\n📜 **原文**\n")
        output_parts.append(response['original'])
        
        # 第二层：白话通解/解释
        if 'explanation' in response:
            output_parts.append("\n📖 **白话通解**\n")
            output_parts.append(response['explanation'])
        
        # 第三层：佛学对照（新增）
        if 'comparison' in response:
            output_parts.append("\n🕉️ **佛学对照**\n")
            output_parts.append(f"> {response.get('dao_concept', '')} vs {response.get('buddhist_term', '')}\n")
            output_parts.append(response['comparison'])
        
        # 第四层：点拨/场景映射（新增）
        if 'theme' in response:
            output_parts.append("\n🌍 **现代应用**\n")
            output_parts.append(f"> 主题：{response.get('theme', '')}\n")
            output_parts.append(response['explanation'] if 'explanation' not in response else "")
        elif 'guidance' in response:
            output_parts.append("\n💡 **点拨**\n")
            output_parts.append(response['guidance'])
        
        # 第五层：留白
        output_parts.append("\n🌱 **留给你的**\n")
        if 'leave_blank' in response:
            output_parts.append(response['leave_blank'])
        
        return '\n'.join(output_parts)


# 测试
if __name__ == "__main__":
    wisdom = DaoDeJingWisdom()
    
    test_queries = [
        "我最近很焦虑，压力很大",
        "什么是无为？",
        "道德经第八章讲什么？",
        "佛学中的空性和道家的道有什么关系？",
        "职场内卷怎么办？",
        "今天读什么？"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"用户问：{query}")
        print('='*60)
        print(wisdom.respond(query))
