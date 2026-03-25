#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话管理模块 - AI 对话助手核心

功能：
1. 会话状态管理 🔥 **新增**
2. 响应生成策略 🔥 **新增**
3. 错误处理与降级机制 🔥 **新增**
4. 用户反馈收集 🔥 **新增**
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime


class DialogueManager:
    """对话管理器"""
    
    def __init__(self):
        # 会话状态管理
        self.sessions = {}
        
        # 响应模板库
        self.response_templates = {
            'greeting': [
                "您好！我是历史智慧助手，请问有什么可以帮助您的？",
                "欢迎使用资治通鉴 Skill！我可以帮您搜索历史案例、翻译文言文、查询人物档案等。"
            ],
            
            'search_result': [
                "我找到了 {count} 个相关案例：\n{results}",
                "根据您的需求，这里有 {count} 个匹配的历史智慧："
            ],
            
            'translate_result': [
                "原文：{original}\n译文：{translated}",
                "翻译结果：\n{original}\n→\n{translated}"
            ],
            
            'character_profile': [
                "📋 **{name}** 人物档案\n\n"
                f"- **时期**: {period}\n"
                f"- **身份**: {identity}\n"
                f"- **角色类型**: {role_type}\n\n"
                "**核心特质**:\n{traits}",
                
                "👤 **{name}** 简介：\n\n"
                f"{period}时期的{identity}，以{role_type}著称。\n\n"
                f"**主要特点**: {traits}"
            ],
            
            'wisdom_daily': [
                "📅 今日历史智慧:\n\n"
                f"🎯 **{case_name}**\n\n"
                f"{key_wisdom}",
                
                "💡 今天的锦囊：\n\n"
                f"**{case_name}**\n\n"
                f"{key_wisdom}"
            ],
            
            'simulator_result': [
                "🎮 **{event_title}** - {outcome}\n\n"
                f"**选择**: {description}\n"
                f"**结果**: {outcome}\n"
                f"**智慧**: {lesson}",
                
                "📜 历史沙盘模拟:\n\n"
                f"事件：{event_title}\n"
                f"您的选择：{description}\n"
                f"最终结果：{outcome}\n"
                f"💡 启示：{lesson}"
            ],
            
            'relationship_result': [
                "🔗 **{character}** 的关系网络:\n\n"
                f"**盟友**: {allies}\n"
                f"**敌人**: {enemies}",
                
                "人物关系查询结果:\n\n"
                f"{character}的盟友：{allies}\n"
                f"{character}的敌人：{enemies}"
            ],
            
            'timeline_result': [
                "📊 历史时间线 ({count}个事件):\n\n{events}",
                
                "按年代排序的历史事件:\n\n{events}"
            ],
            
            'error_default': [
                "抱歉，我暂时无法理解您的问题。请尝试更具体的描述，或输入'帮助'查看功能列表。",
                "这个问题超出了我的能力范围。您可以试试搜索具体案例、翻译文言文或查询人物信息。"
            ],
            
            'unknown_intent': [
                "我不太明白您的意思。您是想：\n1. 搜索历史案例？\n2. 翻译文言文？\n3. 查询人物档案？\n4. 获取今日锦囊？",
                
                "这个问题有点模糊。请告诉我您具体想了解什么，或者输入'帮助'查看可用功能。"
            ]
        }
        
        # 错误处理策略
        self.error_handlers = {
            'search_error': "搜索失败，请检查关键词是否正确",
            'translate_error': "翻译服务暂时不可用，请稍后再试",
            'character_not_found': f"未找到该人物信息，请确认名字是否正确",
            'simulator_error': "模拟失败，请检查事件名称和选项"
        }
    
    def get_session(self, session_id: str) -> Dict:
        """获取或创建会话状态
        
        Args:
            session_id: 会话 ID (可以是用户 ID 或临时 ID)
            
        Returns:
            Dict: 会话状态字典
        """
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': datetime.now(),
                'last_active': datetime.now(),
                'messages': [],
                'current_intent': None,
                'context': {}
            }
        
        # 更新活跃时间
        self.sessions[session_id]['last_active'] = datetime.now()
        
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, role: str, content: str):
        """添加对话消息到会话
        
        Args:
            session_id: 会话 ID
            role: 'user' or 'assistant'
            content: 消息内容
        """
        
        session = self.get_session(session_id)
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        session['messages'].append(message)
    
    def generate_response(self, 
                         intent: str, 
                         data: Dict, 
                         session_id: str = None) -> Dict:
        """生成对话响应
        
        Args:
            intent: 识别的意图
            data: 处理结果数据
            session_id: 会话 ID (可选)
            
        Returns:
            Dict: 包含响应文本和元数据的字典
        """
        
        # 添加用户消息到会话
        if session_id and 'user_message' in data:
            self.add_message(session_id, 'user', data['user_message'])
        
        # 根据意图生成响应
        response_text = ""
        metadata = {}
        
        if intent == 'greeting':
            response_text = self._select_template('greeting')
            metadata['type'] = 'greeting'
        
        elif intent == 'search':
            results = data.get('results', [])
            count = len(results)
            
            if count > 0:
                result_list = "\n".join([f"{i+1}. {r.get('title', '')}" for i, r in enumerate(results[:5])])
                
                response_text = self._select_template('search_result').format(
                    count=count, results=result_list
                )
            else:
                response_text = "未找到相关案例，请尝试其他关键词。"
            
            metadata['type'] = 'search'
            metadata['result_count'] = count
        
        elif intent == 'translate':
            original = data.get('original', '')
            translated = data.get('translated', '')
            
            response_text = self._select_template('translate_result').format(
                original=original, translated=translated
            )
            
            metadata['type'] = 'translate'
        
        elif intent == 'character':
            name = data.get('name', '')
            period = data.get('period', '')
            identity = data.get('identity', '')
            role_type = data.get('role_type', '')
            traits = "\n".join([f"- {t}" for t in data.get('traits', [])[:5]])
            
            response_text = self._select_template('character_profile').format(
                name=name, period=period, identity=identity, 
                role_type=role_type, traits=traits
            )
            
            metadata['type'] = 'character'
        
        elif intent == 'wisdom':
            case_name = data.get('case_name', '')
            key_wisdom = data.get('key_wisdom', '')[:150] + "..." if len(data.get('key_wisdom', '')) > 150 else data.get('key_wisdom', '')
            
            response_text = self._select_template('wisdom_daily').format(
                case_name=case_name, key_wisdom=key_wisdom
            )
            
            metadata['type'] = 'wisdom'
        
        elif intent == 'simulator':
            event_title = data.get('title', '')
            outcome = data.get('outcome', '')
            description = data.get('description', '')
            lesson = data.get('lesson', '')
            
            response_text = self._select_template('simulator_result').format(
                event_title=event_title, outcome=outcome, 
                description=description, lesson=lesson
            )
            
            metadata['type'] = 'simulator'
        
        elif intent == 'relationship':
            character = data.get('character', '')
            allies = ", ".join(data.get('allies', [])[:5]) if data.get('allies') else "暂无"
            enemies = ", ".join(data.get('enemies', [])[:5]) if data.get('enemies') else "暂无"
            
            response_text = self._select_template('relationship_result').format(
                character=character, allies=allies, enemies=enemies
            )
            
            metadata['type'] = 'relationship'
        
        elif intent == 'timeline':
            events = data.get('events', [])
            count = len(events)
            
            event_list = "\n".join([f"{e.get('year', '')}: {e.get('title', '')}" for e in events[:10]])
            
            response_text = self._select_template('timeline_result').format(
                count=count, events=event_list
            )
            
            metadata['type'] = 'timeline'
        
        elif intent == 'help':
            from chatbot.intent_classifier import IntentClassifier
            classifier = IntentClassifier()
            response_text = classifier.get_help_message()
            metadata['type'] = 'help'
        
        else:  # unknown or error
            if data.get('error'):
                error_msg = self.error_handlers.get(data['error'], data['error'])
                response_text = f"❌ {error_msg}"
            else:
                response_text = self._select_template('unknown_intent')
            
            metadata['type'] = 'error'
        
        # 添加会话消息
        if session_id:
            self.add_message(session_id, 'assistant', response_text)
        
        return {
            'response': response_text,
            'metadata': metadata,
            'timestamp': datetime.now().isoformat()
        }
    
    def _select_template(self, template_key: str) -> str:
        """从模板库中随机选择一个模板"""
        
        templates = self.response_templates.get(template_key, [])
        
        if not templates:
            return "抱歉，我无法处理这个问题。"
        
        import random
        return random.choice(templates)
    
    def handle_error(self, error_type: str, context: Dict = None) -> Dict:
        """错误处理和降级
        
        Args:
            error_type: 错误类型
            context: 上下文信息
            
        Returns:
            Dict: 错误处理响应
        """
        
        error_msg = self.error_handlers.get(error_type, "发生未知错误")
        
        # 根据错误类型提供建议
        suggestions = []
        
        if 'search' in error_type.lower():
            suggestions.append("请尝试更具体的关键词，如具体人物或事件名称。")
        
        elif 'translate' in error_type.lower():
            suggestions.append("您可以直接输入文言文文本，我会为您翻译。")
        
        elif 'character' in error_type.lower():
            suggestions.append("请确认人物名字是否正确，或尝试查询其他历史人物。")
        
        if suggestions:
            error_msg += "\n\n💡 建议：" + " ".join(suggestions)
        
        return {
            'error': True,
            'message': error_msg,
            'suggestions': suggestions
        }
    
    def collect_feedback(self, session_id: str, rating: int, comment: str = None):
        """收集用户反馈
        
        Args:
            session_id: 会话 ID
            rating: 评分 (1-5)
            comment: 评论 (可选)
        """
        
        session = self.get_session(session_id)
        
        feedback = {
            'rating': rating,
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        }
        
        if 'feedbacks' not in session:
            session['feedbacks'] = []
        
        session['feedbacks'].append(feedback)
    
    def get_session_summary(self, session_id: str) -> Dict:
        """获取会话摘要
        
        Args:
            session_id: 会话 ID
            
        Returns:
            Dict: 会话统计信息
        """
        
        session = self.get_session(session_id)
        
        messages = session.get('messages', [])
        
        user_messages = [m for m in messages if m['role'] == 'user']
        assistant_messages = [m for m in messages if m['role'] == 'assistant']
        
        return {
            'session_id': session_id,
            'created_at': session.get('created_at'),
            'last_active': session.get('last_active'),
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'current_intent': session.get('current_intent'),
            'feedback_count': len(session.get('feedbacks', []))
        }
    
    def clear_session(self, session_id: str):
        """清除会话状态
        
        Args:
            session_id: 会话 ID
        """
        
        if session_id in self.sessions:
            del self.sessions[session_id]


# 测试
if __name__ == "__main__":
    manager = DialogueManager()
    
    print("=" * 80)
    print("💬 对话管理器测试")
    print("=" * 80)
    
    session_id = "test_session_001"
    
    # 模拟对话流程
    test_conversations = [
        {
            'intent': 'greeting',
            'data': {'user_message': '你好'}
        },
        {
            'intent': 'search',
            'data': {
                'user_message': '搜索如虎添翼',
                'results': [
                    {'title': '如虎添翼 - 刘备借荆州'},
                    {'title': '如鱼得水 - 刘备遇诸葛亮'}
                ]
            }
        },
        {
            'intent': 'translate',
            'data': {
                'user_message': '翻译刘豫州王室之胄',
                'original': '刘豫州王室之胄，英才盖世',
                'translated': '我听说...了，人才盖世'
            }
        },
        {
            'intent': 'character',
            'data': {
                'user_message': '诸葛亮的人物档案',
                'name': '诸葛亮',
                'period': '三国时期',
                'identity': '丞相/谋士',
                'role_type': '决策者',
                'traits': ['足智多谋', '忠诚正直', '善于用人']
            }
        },
        {
            'intent': 'wisdom',
            'data': {
                'user_message': '今天的智慧是什么',
                'case_name': '田忌赛马 - 以弱胜强的经典策略',
                'key_wisdom': '在整体实力不如对手的情况下，通过巧妙的策略安排，扬长避短，以弱胜强。体现了资源优化配置和差异化竞争的思维方式。'
            }
        },
        {
            'intent': 'unknown',
            'data': {'user_message': '这个问题我不太懂'}
        }
    ]
    
    print("\n📝 模拟对话流程:\n")
    
    for i, conversation in enumerate(test_conversations, 1):
        intent = conversation['intent']
        data = conversation['data']
        
        response = manager.generate_response(intent, data, session_id)
        
        print(f"{i}. **意图**: {intent}")
        print(f"   📝 用户：{data.get('user_message', 'N/A')}")
        print(f"   💬 助手：{response['response'][:100]}...")
        print()
    
    # 获取会话摘要
    summary = manager.get_session_summary(session_id)
    print("\n📊 会话摘要:")
    for key, value in summary.items():
        if key != 'session_id':
            print(f"   {key}: {value}")
