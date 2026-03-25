#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多文风切换系统 - 为 RAG 系统提供多种输出风格

功能：
1. 学术版 (严谨、专业)
2. 职场版 (实用、高效)
3. 吃瓜版 (幽默、生动)
4. 白话版 (通俗易懂)
5. 动态切换逻辑
"""

from typing import Dict, List, Optional


class StyleSwitcher:
    """文风切换器"""
    
    # 文风配置
    STYLES = {
        'academic': {
            'name': '学术版',
            'description': '严谨、专业，适合学术研究',
            'tone': 'formal',
            'structure': 'structured'
        },
        'workplace': {
            'name': '职场版', 
            'description': '实用、高效，适合职场应用',
            'tone': 'professional',
            'structure': 'actionable'
        },
        'gossip': {
            'name': '吃瓜版',
            'description': '幽默、生动，像讲故事一样',
            'tone': 'casual',
            'structure': 'narrative'
        },
        'plain': {
            'name': '白话版',
            'description': '通俗易懂，适合零基础学习',
            'tone': 'friendly',
            'structure': 'simple'
        }
    }
    
    # Prompt 模板库 (每种文风的提示词)
    PROMPT_TEMPLATES = {
        'academic': """你是一个资深的历史研究学者。请用严谨、专业的学术语言回答以下问题：

要求:
1. 引用准确的历史出处和文献
2. 使用规范的学术术语
3. 保持客观中立的态度
4. 提供详细的论证过程
5. 避免口语化和情绪化表达

请按照以下结构组织答案:
- 历史背景
- 核心事件分析
- 史料依据
- 学术观点
- 现代启示""",
        
        'workplace': """你是一个职场导师，擅长从历史中提炼管理智慧。请用实用、高效的风格回答：

要求:
1. 直接给出可操作的行动建议
2. 结合现代职场场景
3. 突出关键成功因素
4. 提供具体的应用方法
5. 避免冗长的历史叙述

请按照以下结构组织答案:
- 核心智慧 (一句话总结)
- 职场应用场景
- 具体行动步骤
- 注意事项
- 成功案例""",
        
        'gossip': """你是一个幽默风趣的历史博主，擅长把历史讲成精彩的故事。请用生动、有趣的风格回答：

要求:
1. 像讲故事一样娓娓道来
2. 加入适当的调侃和幽默
3. 突出戏剧性和冲突感
4. 使用网络流行语 (适度)
5. 让读者欲罢不能

请按照以下结构组织答案:
- 开场白 (吸引眼球)
- 故事背景 (设置悬念)
- 高潮部分 (精彩对决)
- 结局反转 (意想不到的结果)
- 吃瓜总结 (金句收尾)""",
        
        'plain': """你是一个亲切的历史老师，擅长用大白话讲解复杂的历史。请用简单、易懂的风格回答：

要求:
1. 用最通俗的语言解释
2. 避免专业术语和古文引用
3. 多用比喻和生活化的例子
4. 循序渐进地讲解
5. 确保零基础也能听懂

请按照以下结构组织答案:
- 这是什么 (一句话解释)
- 发生了什么 (简单叙述)
- 为什么重要 (通俗说明)
- 对我们有什么用 (实际应用)
- 记住这几点 (要点总结)"""
    }
    
    def __init__(self, current_style: str = 'workplace'):
        """初始化文风切换器
        
        Args:
            current_style: 当前使用的文风 ('academic', 'workplace', 'gossip', 'plain')
        """
        self.current_style = current_style
    
    def get_current_style(self) -> Dict:
        """获取当前文风的配置信息"""
        return self.STYLES.get(self.current_style, self.STYLES['workplace'])
    
    def switch_style(self, style_name: str) -> bool:
        """切换文风
        
        Args:
            style_name: 目标文风 ('academic', 'workplace', 'gossip', 'plain')
            
        Returns:
            bool: 是否成功切换
        """
        if style_name in self.STYLES:
            self.current_style = style_name
            return True
        return False
    
    def get_prompt(self) -> str:
        """获取当前文风的 Prompt 模板"""
        return self.PROMPT_TEMPLATES.get(self.current_style, self.PROMPT_TEMPLATES['workplace'])
    
    def format_output(self, content: Dict, style: Optional[str] = None) -> Dict:
        """根据指定文风格式化输出内容
        
        Args:
            content: 原始内容字典 (包含 title, wisdom, applications 等)
            style: 目标文风，如果为 None 则使用当前文风
            
        Returns:
            Dict: 格式化后的内容
        """
        target_style = style or self.current_style
        
        # 根据文风调整输出格式
        if target_style == 'academic':
            return self._format_academic(content)
        elif target_style == 'workplace':
            return self._format_workplace(content)
        elif target_style == 'gossip':
            return self._format_gossip(content)
        else:  # plain
            return self._format_plain(content)
    
    def _format_academic(self, content: Dict) -> Dict:
        """学术版格式化"""
        return {
            'title': f"【历史研究】{content.get('title', '')}",
            'abstract': f"本文探讨{content.get('title', '')}的历史意义与现代启示",
            'background': self._academic_tone(content.get('background', '')),
            'analysis': self._analyze_wisdom_academic(content.get('key_wisdom', '')),
            'references': [f"参见：{content.get('volume', '')}"],
            'modern_applications': [
                f"- {app.get('scenario', '')}: {self._academic_tone(app.get('action', ''))}"
                for app in content.get('modern_applications', [])
            ],
            'conclusion': "综上所述，该历史案例具有重要的学术价值和现实意义"
        }
    
    def _format_workplace(self, content: Dict) -> Dict:
        """职场版格式化"""
        wisdom = content.get('key_wisdom', '')
        
        # 提取核心智慧 (一句话总结)
        core_insight = self._extract_core_insight(wisdom)
        
        return {
            'title': f"💼 {content.get('title', '')}",
            'core_insight': core_insight,
            'workplace_applications': [
                f"🎯 场景：{app.get('scenario', '')}\n   💡 方法：{app.get('action', '')}\n   📌 案例：{app.get('example', '')}"
                for app in content.get('modern_applications', [])
            ],
            'key_takeaways': [
                "1. 把握时机，顺势而为",
                "2. 团结团队，凝聚人心", 
                "3. 保持谦逊，持续学习"
            ],
            'action_items': [
                "✅ 本周行动：识别一个可借鉴的历史智慧",
                "📝 下周计划：制定应用方案并执行",
                "🔄 月度复盘：评估效果并调整策略"
            ]
        }
    
    def _format_gossip(self, content: Dict) -> Dict:
        """吃瓜版格式化"""
        return {
            'title': f"🍉 震惊！{content.get('title', '')}背后的真相",
            'opening': "各位吃瓜群众，今天给大家扒一扒这个超有意思的历史故事...",
            'story': self._gossip_tone(content.get('background', '')),
            'twist': f"没想到吧？结局竟然是这样的！{content.get('key_wisdom', '')}",
            'golden_quotes': [
                "🔥 金句：'历史不会重复，但会押韵'",
                "💡 感悟：古人诚不欺我啊！",
                "😂 吐槽：要是放在今天，这操作绝对上热搜"
            ],
            'summary': f"总结一下：{content.get('title', '')}告诉我们... (吃瓜总结)"
        }
    
    def _format_plain(self, content: Dict) -> Dict:
        """白话版格式化"""
        return {
            'title': f"📚 {content.get('title', '')}",
            'what_is_it': "简单来说，这就是一个关于...的故事",
            'story_summary': self._plain_tone(content.get('background', '')),
            'why_matters': "这个故事为什么重要呢？因为...",
            'how_to_use': [
                f"1. {app.get('scenario', '')} - 可以这样做：{app.get('action', '')}"
                for app in content.get('modern_applications', [])
            ],
            'key_points': "记住这几点就够了:",
            'takeaways': [
                "• 核心智慧很简单",
                "• 关键是要灵活运用",
                "• 不要生搬硬套"
            ]
        }
    
    def _academic_tone(self, text: str) -> str:
        """转换为学术语气"""
        # 简化版：添加学术前缀和后缀
        return f"【史料分析】{text}。【研究价值】该案例具有重要的历史研究意义。"
    
    def _gossip_tone(self, text: str) -> str:
        """转换为吃瓜语气"""
        # 简化版：添加吃瓜元素
        return f"话说当年... {text} ...简直太精彩了！"
    
    def _plain_tone(self, text: str) -> str:
        """转换为白话语气"""
        # 简化版：用简单语言重述
        return f"简单来说，就是{text[:100]}..." if len(text) > 100 else text
    
    def _analyze_wisdom_academic(self, wisdom: str) -> str:
        """学术分析智慧"""
        return f"【核心观点】{wisdom}\n【理论依据】该智慧体现了中国古代哲学思想中的辩证思维\n【现代价值】对当代管理实践具有重要启示意义"
    
    def _extract_core_insight(self, wisdom: str) -> str:
        """提取核心洞察 (一句话总结)"""
        # 简化版：取前 50 个字符
        return f"{wisdom[:50]}..." if len(wisdom) > 50 else wisdom


# 测试
if __name__ == "__main__":
    switcher = StyleSwitcher('workplace')
    
    # 示例内容
    sample_content = {
        'title': '田忌赛马 - 以弱胜强的经典策略',
        'background': '战国时期，齐国大将田忌经常与齐威王赛马。双方各出上、中、下三等马，每等马比一次，三局两胜。孙膑建议用下等马对上等马、上等马对中等马、中等马对下等马，结果三局两胜。',
        'key_wisdom': '田忌赛马的核心智慧：在整体实力不如对手的情况下，通过巧妙的策略安排，扬长避短，以弱胜强。体现了资源优化配置和差异化竞争的思维方式。',
        'modern_applications': [
            {
                'scenario': '商业竞争策略',
                'action': '避开对手优势领域，在细分市场竞争',
                'example': '小公司不与巨头正面竞争，专注 niche 市场'
            },
            {
                'scenario': '资源优化配置',
                'action': '将有限资源投入到最能产生价值的地方',
                'example': '创业团队集中火力攻克核心功能'
            }
        ]
    }
    
    print("=== 测试：多文风切换系统 ===\n")
    
    # 测试不同文风
    for style in ['academic', 'workplace', 'gossip', 'plain']:
        switcher.switch_style(style)
        current = switcher.get_current_style()
        
        print(f"--- {current['name']} ---")
        formatted = switcher.format_output(sample_content, style)
        
        # 显示标题和核心内容
        if 'title' in formatted:
            print(formatted['title'])
        if 'core_insight' in formatted:
            print(f"💡 {formatted['core_insight']}")
        elif 'opening' in formatted:
            print(formatted['opening'][:50] + "...")
        
        print()
