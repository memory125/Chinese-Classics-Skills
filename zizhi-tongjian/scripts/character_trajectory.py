#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人物履历生成器 - 为 RAG 系统提供深度人物分析能力

功能：
1. 人物档案生成 (基本信息、时间线、特质)
2. 成功/失败因素分析
3. 现代启示提取
4. 人物关系网络构建
5. **优化版**: 改进检索逻辑，支持同义词和别名
6. **增强版**: 优化身份识别和特质提取规则
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import re


class CharacterTrajectoryGenerator:
    """人物履历生成器 (增强版)"""
    
    # 人物同义词/别名库 (可扩展)
    CHARACTER_ALIASES = {
        '刘邦': ['汉高祖', '刘季', '沛公'],
        '项羽': ['项籍', '西楚霸王'],
        '诸葛亮': ['孔明', '诸葛孔明', '卧龙'],
        '曹操': ['曹孟德', '魏武帝'],
        '刘备': ['刘玄德', '汉昭烈帝'],
        '孙权': ['孙仲谋'],
        '周瑜': ['公瑾'],
        '李世民': ['唐太宗', '太宗'],
        '郭子仪': ['汾阳王'],
        '王安石': ['王介甫'],
        '司马光': ['君实'],
        '苻坚': ['秦王坚'],
        '安禄山': ['禄山'],
        '张邦昌': [],
        '刘豫': [],
        '田忌': [],
        '孙膑': [],
    }
    
    # 身份关键词映射 (优化版)
    IDENTITY_KEYWORDS = {
        '皇帝/君主': ['帝', '皇', '王', '陛下', '天子'],
        '将军/统帅': ['将', '帅', '军', '大将军', '都督'],
        '谋士/丞相': ['相', '宰', '谋', '策', '师', '臣光曰'],
        '诸侯/藩王': ['侯', '王', '公', '伯'],
        '商人/平民': ['商', '民', '贩', '徒'],
    }
    
    def __init__(self, rag_system):
        self.rag = rag_system
    
    def generate_profile(self, character_name: str) -> Dict:
        """生成人物档案 (增强版)"""
        
        print(f"📋 正在生成 {character_name} 的人物档案...")
        
        # 1. 检索人物相关事件 (使用优化后的检索逻辑)
        events = self._search_character_events(character_name)
        
        if not events:
            return {'error': f'未找到关于"{character_name}"的历史记录'}
        
        print(f"   ✅ 找到 {len(events)} 个相关事件")
        
        # 2. 构建时间线 (按年份排序)
        timeline = sorted(events, key=lambda x: self._parse_year(x.get('year', '')))
        
        # 3. 提取核心特质
        traits = self._extract_traits(timeline)
        
        # 4. 分析成功/失败因素
        success_factors = self._analyze_success_factors(timeline)
        failure_lessons = self._analyze_failure_lessons(timeline)
        
        # 5. 生成现代启示
        modern_lessons = self._generate_modern_lessons(traits, success_factors)
        
        # 6. 构建人物关系网络
        relationships = self._build_relationships(character_name, timeline)
        
        # 7. 提取基本信息 (优化版)
        basic_info = self._extract_basic_info(timeline, character_name)
        
        return {
            'name': character_name,
            **basic_info,
            'timeline': timeline[:15],  # 限制前 15 个关键事件
            'traits': traits,
            'success_factors': success_factors,
            'failure_lessons': failure_lessons,
            'relationships': relationships,
            'modern_lessons': modern_lessons,
            'generated_at': datetime.now().isoformat()
        }
    
    def _search_character_events(self, name: str) -> List[Dict]:
        """搜索人物相关事件 (优化版 - 支持同义词和别名)"""
        
        print(f"   🔍 开始检索：{name}")
        
        # 1. 获取所有别名/同义词
        aliases = self.CHARACTER_ALIASES.get(name, [])
        all_names = [name] + aliases
        
        print(f"   📝 搜索关键词：{', '.join(all_names)}")
        
        events_map = {}  # 使用字典去重
        
        for search_name in all_names:
            try:
                # 使用 RAG v5.0 系统检索
                results = self.rag.hybrid_search(search_name, top_k=30)
                
                print(f"   ✅ {search_name} 找到 {len(results)} 个结果")
                
                for r in results:
                    case_data = self.rag.case_db.get(r['name'], {})
                    
                    # 检查人物是否匹配 (更宽松的条件)
                    protagonists = case_data.get('protagonists', [])
                    title = case_data.get('title', '')
                    wisdom = case_data.get('key_wisdom', '')
                    background = case_data.get('background', '')
                    
                    # 组合所有文本进行搜索
                    all_text = f"{title} {wisdom} {background}".lower()
                    search_name_lower = search_name.lower()
                    
                    if (search_name_lower in str(protagonists).lower() or 
                        search_name_lower in title.lower() or 
                        search_name_lower in wisdom.lower() or
                        search_name_lower in background.lower()):
                        
                        # 去重：使用案例名称作为 key
                        case_key = r['name']
                        if case_key not in events_map:
                            events_map[case_key] = {
                                'year': case_data.get('year', ''),
                                'event': title,
                                'volume': case_data.get('volume', ''),
                                'outcome': self._determine_outcome(wisdom),
                                'wisdom': wisdom[:100] if wisdom else '',
                                'protagonists': protagonists
                            }
            
            except Exception as e:
                print(f"   ⚠️ {search_name} 检索失败：{e}")
        
        # 转换为列表并排序
        events = list(events_map.values())
        return events
    
    def _parse_year(self, year_str: str) -> int:
        """解析年份字符串为数字"""
        
        if not year_str:
            return 0
        
        # 提取数字 (支持多种格式)
        patterns = [
            r'(\d+) 年',           # "208 年"
            r'前 (\d+)',          # "前 208"
            r'(\d+) 至 (\d+)',    # "208-209"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, year_str)
            if match:
                try:
                    return int(match.group(1))
                except:
                    pass
        
        # fallback: 返回 0
        return 0
    
    def _determine_outcome(self, wisdom: str) -> str:
        """根据智慧判断事件结果"""
        
        if not wisdom:
            return 'neutral'
        
        success_keywords = ['成功', '胜利', '成就', '崛起', '建立', '胜', '成']
        failure_keywords = ['失败', '败亡', '灭亡', '崩溃', '覆灭', '败', '亡']
        
        wisdom_lower = wisdom.lower()
        
        for kw in success_keywords:
            if kw in wisdom_lower:
                return 'success'
        
        for kw in failure_keywords:
            if kw in wisdom_lower:
                return 'failure'
        
        return 'neutral'  # 中性结果
    
    def _extract_traits(self, timeline: List[Dict]) -> List[str]:
        """从时间线中提取核心特质 (优化版)"""
        
        traits = []
        trait_scores = {}
        
        for event in timeline:
            wisdom = event.get('wisdom', '')
            
            if not wisdom:
                continue
            
            # 定义特质关键词映射 (增强版)
            trait_keywords = {
                '善于用人': ['知人善任', '用人不疑', '团队', '人才', '韩信', '萧何', '张良'],
                '能屈能伸': ['屈伸', '隐忍', '等待时机', '退让', '谢罪', '示弱'],
                '善于纳谏': ['纳谏', '听取意见', '采纳建议', '从善如流'],
                '政治敏锐度高': ['敏锐', '时机', '判断', '识时务'],
                '战略眼光长远': ['长远', '大局', '规划', '三分天下'],
                '领导力强': ['领导', '统帅', '指挥', '威信'],
                '勇猛无畏': ['勇敢', '冲锋', '破釜沉舟', '必死'],
                '优柔寡断': ['犹豫', '不决', '错失良机'],
                '骄傲自满': ['骄傲', '轻敌', '自大', '狂妄'],
                '猜忌多疑': ['猜忌', '怀疑', '诛杀功臣'],
            }
            
            for trait, keywords in trait_keywords.items():
                if any(kw in wisdom.lower() for kw in keywords):
                    trait_scores[trait] = trait_scores.get(trait, 0) + 1
        
        # 按得分排序，取前 8 个
        sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [trait for trait, score in sorted_traits[:8]]
    
    def _analyze_success_factors(self, timeline: List[Dict]) -> List[str]:
        """分析成功因素 (优化版)"""
        
        success_events = [e for e in timeline if e['outcome'] == 'success']
        
        factors = []
        factor_scores = {}
        
        for event in success_events[:10]:  # 前 10 个成功案例
            wisdom = event.get('wisdom', '')
            
            if not wisdom:
                continue
            
            # 定义成功因素关键词映射 (增强版)
            factor_keywords = {
                '正确的战略决策': ['战略', '决策', '规划', '三分天下'],
                '把握时机': ['时机', '机会', '趁势', '天时地利'],
                '团结团队': ['团队', '合作', '同心', '众士慕仰'],
                '消除隐患': ['隐患', '预防', '警惕', '防患未然'],
                '知人善任': ['用人', '人才', '韩信', '张良', '萧何'],
                '示弱消疑': ['示弱', '谢罪', '隐忍', '让功'],
            }
            
            for factor, keywords in factor_keywords.items():
                if any(kw in wisdom.lower() for kw in keywords):
                    factor_scores[factor] = factor_scores.get(factor, 0) + 1
        
        # 按得分排序，取前 5 个
        sorted_factors = sorted(factor_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [factor for factor, score in sorted_factors[:5]]
    
    def _analyze_failure_lessons(self, timeline: List[Dict]) -> List[str]:
        """分析失败教训 (优化版)"""
        
        failure_events = [e for e in timeline if e['outcome'] == 'failure']
        
        lessons = []
        lesson_scores = {}
        
        for event in failure_events[:10]:  # 前 10 个失败案例
            wisdom = event.get('wisdom', '')
            
            if not wisdom:
                continue
            
            # 定义失败教训关键词映射 (增强版)
            lesson_keywords = {
                '骄傲自满导致失败': ['骄傲', '轻敌', '自大', '狂妄'],
                '用人不当': ['猜忌', '误信', '错用', '诛杀功臣'],
                '战略失误': ['错误决策', '判断失误', '方向错误', '失策'],
                '内部不和': ['内斗', '分裂', '矛盾', '离心离德'],
                '优柔寡断错失良机': ['犹豫', '不决', '错失时机'],
            }
            
            for lesson, keywords in lesson_keywords.items():
                if any(kw in wisdom.lower() for kw in keywords):
                    lesson_scores[lesson] = lesson_scores.get(lesson, 0) + 1
        
        # 按得分排序，取前 5 个
        sorted_lessons = sorted(lesson_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [lesson for lesson, score in sorted_lessons[:5]]
    
    def _build_relationships(self, character_name: str, timeline: List[Dict]) -> Dict:
        """构建人物关系网络 (优化版)"""
        
        relationships = {
            'allies': [],      # 盟友
            'enemies': [],     # 敌人
            'mentors': [],     # 导师/上级
            'subordinates': [] # 下属/追随者
        }
        
        for event in timeline:
            wisdom = event.get('wisdom', '')
            protagonists = event.get('protagonists', [])
            
            if not protagonists:
                continue
            
            # 根据关键词判断关系类型
            if any(kw in wisdom.lower() for kw in ['联盟', '合作', '结盟', '联']):
                relationships['allies'].extend(protagonists)
            
            if any(kw in wisdom.lower() for kw in ['对抗', '战争', '敌对', '战']):
                # 排除当前人物本身
                enemies = [p for p in protagonists if p != character_name]
                relationships['enemies'].extend(enemies)
        
        # 去重并限制数量
        for key in relationships:
            unique = list(set(relationships[key]))[:5]
            relationships[key] = unique
        
        return relationships
    
    def _extract_basic_info(self, timeline: List[Dict], character_name: str) -> Dict:
        """提取基本信息 (优化版 - 更精准的身份识别)"""
        
        if not timeline:
            return {
                'period': '',
                'identity': ''
            }
        
        # 从第一个事件推断时期
        first_year = timeline[0].get('year', '')
        
        # **优化版**: 更精准的身份识别逻辑
        identity_scores = {}
        
        for event in timeline:
            title = event.get('event', '')
            wisdom = event.get('wisdom', '')
            protagonists = event.get('protagonists', [])
            
            # 组合所有文本进行搜索
            all_text = f"{title} {wisdom}".lower()
            
            for identity, keywords in self.IDENTITY_KEYWORDS.items():
                score = 0
                
                # 检查关键词匹配
                for kw in keywords:
                    if kw.lower() in all_text:
                        score += 1
                    
                    # 特别处理：如果人物名在 protagonists 中且有关键词，加分更高
                    if character_name.lower() in str(protagonists).lower():
                        if kw.lower() in all_text:
                            score += 2
                
                identity_scores[identity] = identity_scores.get(identity, 0) + score
        
        # 按得分排序，取最高分
        sorted_identities = sorted(identity_scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_identities and sorted_identities[0][1] > 0:
            identity = sorted_identities[0][0].split('/')[0]  # 取第一个身份
        else:
            # fallback: 根据人物名推断
            if '高祖' in character_name or '太宗' in character_name:
                identity = '皇帝/君主'
            elif '将' in character_name or '帅' in character_name:
                identity = '将军/统帅'
            else:
                identity = '历史人物'
        
        return {
            'period': first_year,
            'identity': identity
        }
    
    def _generate_modern_lessons(self, traits: List[str], success_factors: List[str]) -> str:
        """生成现代启示"""
        
        lessons = []
        
        trait_map = {
            '善于用人': "在现代职场中，学会识别和任用人才是领导力的核心",
            '能屈能伸': "面对挫折时保持韧性，等待合适的时机再行动",
            '善于纳谏': "听取他人意见，避免陷入信息茧房",
            '政治敏锐度高': "关注行业趋势和政策变化，提前布局",
            '战略眼光长远': "不要只看眼前利益，要有长期规划",
            '领导力强': "建立团队信任，通过影响力而非权力领导",
            '勇猛无畏': "关键时刻要敢于担当，但也要有策略",
            '优柔寡断错失良机': "决策时要果断，避免犹豫不决",
            '骄傲自满导致失败': "成功后要保持谦逊，警惕自满情绪",
            '猜忌多疑': "建立信任机制，避免无端猜忌破坏团队",
        }
        
        for trait in traits:
            if trait in trait_map:
                lessons.append(f"- {trait}: {trait_map[trait]}")
        
        for factor in success_factors:
            lessons.append(f"- 成功因素：{factor}")
        
        return '\n'.join(lessons)


# 测试
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    
    from scripts.rag_enhanced_v5 import EnhancedRAGSearch
    
    rag = EnhancedRAGSearch()
    generator = CharacterTrajectoryGenerator(rag)
    
    # 测试：生成刘邦人物档案 (增强版)
    print("=== 测试：刘邦人物档案 (增强版) ===")
    profile = generator.generate_profile("刘邦")
    
    if 'error' in profile:
        print(profile['error'])
    else:
        print(f"姓名：{profile['name']}")
        print(f"时期：{profile['period']}")
        print(f"身份：{profile['identity']} ← **优化版!**")
        
        print("\n核心特质:")
        for trait in profile['traits'][:5]:
            print(f"  - {trait}")
        
        print("\n成功因素:")
        for factor in profile['success_factors'][:3]:
            print(f"  - {factor}")
        
        print("\n失败教训:")
        for lesson in profile['failure_lessons'][:2]:
            print(f"  - {lesson}")
