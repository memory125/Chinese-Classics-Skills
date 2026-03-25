#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 对话助手 API - FastAPI 聊天端点

功能：
1. /api/chat - 主聊天接口
2. /api/chat/history - 获取对话历史
3. /api/chat/feedback - 提交反馈
4. WebSocket 实时通信支持 (可选)
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from chatbot.intent_classifier import IntentClassifier
from chatbot.dialogue_manager import DialogueManager

# 初始化核心组件
intent_classifier = IntentClassifier()
dialogue_manager = DialogueManager()

# 创建 FastAPI 应用
app = FastAPI(
    title="AI Chat Assistant API",
    description="""
## 🤖 资治通鉴 AI 对话助手 API
    
### 功能：
- 🔍 **智能搜索**: RAG v5.0 + 混合搜索
- 📖 **文言文翻译**: 无需 API key 的规则引擎
- 👤 **人物档案**: 增强版身份识别 + 角色判断
- 📅 **今日锦囊**: 智能协同过滤推荐
- 🎮 **历史沙盘**: 15+ 经典事件模拟
- 🔗 **知识图谱**: 实体关系网络查询
    
### 使用示例：
```bash
# 聊天
POST /api/chat
{
    "message": "搜索如虎添翼",
    "session_id": "user_001"
}

# 获取对话历史
GET /api/chat/history?session_id=user_001
```
""",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Pydantic Models ====================

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Query(..., description="用户消息")
    session_id: Optional[str] = Query(None, description="会话 ID (可选)")


class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    intent: str
    confidence: float
    metadata: Dict
    timestamp: str


class HistoryRequest(BaseModel):
    """历史请求模型"""
    session_id: str = Query(..., description="会话 ID")
    limit: int = Query(default=50, ge=1, le=200, description="返回数量限制")


# ==================== API 端点 ====================

@app.get("/", tags=["根路径"])
async def root():
    """API 根路径"""
    return {
        "message": "🤖 资治通鉴 AI 对话助手 v3.0",
        "version": "3.0.0",
        "docs": "/docs"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    主聊天接口
    
    - **message**: 用户输入的消息
    - **session_id**: 会话 ID (可选，用于保持上下文)
    
    返回：AI 助手的响应和元数据
    """
    
    try:
        # 1. 意图识别
        intent_result = intent_classifier.classify(request.message)
        
        # 2. 提取查询内容
        extracted_query = intent_classifier.extract_query(
            request.message, 
            intent_result['intent']
        )
        
        # 3. 更新上下文
        intent_classifier.update_context(
            intent_result['intent'],
            {'text': request.message}
        )
        
        # 4. 根据意图处理请求
        data = {}
        
        if intent_result['intent'] == 'greeting':
            data = {
                'user_message': request.message,
                'results': [],
                'name': '',
                'period': '',
                'identity': '',
                'role_type': '',
                'traits': [],
                'case_name': '',
                'key_wisdom': ''
            }
        
        elif intent_result['intent'] == 'search':
            from scripts.hybrid_search_v3 import SmartHybridSearch
            
            rag = SmartHybridSearch()
            results = rag.hybrid_search(extracted_query, top_k=5)
            
            data = {
                'user_message': request.message,
                'results': [
                    {'title': r.get('name', ''), 'score': r.get('score', 0)}
                    for r in results[:5]
                ]
            }
        
        elif intent_result['intent'] == 'translate':
            from scripts.classical_chinese import ClassicalChineseTranslatorV2
            
            translator = ClassicalChineseTranslatorV2(use_rule_based=True)
            
            annotations = translator.annotate_pinyin(extracted_query)
            translated = translator.translate(extracted_query)
            
            data = {
                'user_message': request.message,
                'original': extracted_query,
                'translated': translated,
                'annotations': [
                    {'char': item['char'], 'pinyin': item.get('pinyin', ''), 
                     'meaning': item.get('meaning', '')}
                    for item in annotations if 'char' in item
                ]
            }
        
        elif intent_result['intent'] == 'character':
            from scripts.character_trajectory_v2 import CharacterTrajectoryGeneratorV2
            
            rag = SmartHybridSearch()
            generator = CharacterTrajectoryGeneratorV2(rag)
            
            profile = generator.generate_profile(extracted_query)
            
            if 'error' in profile:
                data = {
                    'user_message': request.message,
                    'name': extracted_query,
                    'period': '',
                    'identity': '',
                    'role_type': '',
                    'traits': [],
                    'error': 'character_not_found'
                }
            else:
                data = {
                    'user_message': request.message,
                    'name': profile.get('name', ''),
                    'period': profile.get('period', ''),
                    'identity': profile.get('identity', ''),
                    'role_type': profile.get('role_type', ''),
                    'traits': profile.get('traits', [])[:5]
                }
        
        elif intent_result['intent'] == 'wisdom':
            from scripts.daily_wisdom_v2 import DailyWisdomV2
            
            daily = DailyWisdomV2()
            wisdom = daily.get_daily_wisdom()
            
            data = {
                'user_message': request.message,
                'case_name': wisdom.get('case_name', ''),
                'key_wisdom': wisdom.get('key_wisdom', '')
            }
        
        elif intent_result['intent'] == 'simulator':
            from scripts.historical_simulator_v2 import HistoricalSimulatorV2
            
            simulator = HistoricalSimulatorV2()
            
            # 尝试提取事件名称 (简化处理)
            event_name = extracted_query.split()[0] if extracted_query else None
            
            if not event_name:
                data = {
                    'user_message': request.message,
                    'error': 'simulator_error'
                }
            else:
                result = simulator.simulate(event_name)
                
                if 'error' in result:
                    data = {
                        'user_message': request.message,
                        'error': 'simulator_error'
                    }
                else:
                    # 获取第一个选项的结果作为示例
                    options = result.get('options', [])
                    if options:
                        first_option = options[0]
                        choice_result = simulator.make_choice(event_name, first_option['id'])
                        
                        data = {
                            'user_message': request.message,
                            'title': result.get('title', ''),
                            'outcome': choice_result.get('outcome', ''),
                            'description': choice_result.get('description', ''),
                            'lesson': choice_result.get('lesson', '')
                        }
        
        elif intent_result['intent'] == 'relationship':
            from scripts.character_graph import CharacterGraph
            
            graph = CharacterGraph()
            
            # 尝试提取人物名 (简化处理)
            character = extracted_query.split()[0] if extracted_query else None
            
            if not character:
                data = {
                    'user_message': request.message,
                    'character': '',
                    'allies': [],
                    'enemies': []
                }
            else:
                relationships = graph.get_relationships(character)
                
                if 'error' in relationships:
                    data = {
                        'user_message': request.message,
                        'character': character,
                        'allies': [],
                        'enemies': []
                    }
                else:
                    data = {
                        'user_message': request.message,
                        'character': character,
                        'allies': relationships.get('ally', [])[:5],
                        'enemies': relationships.get('enemy', [])[:5]
                    }
        
        elif intent_result['intent'] == 'timeline':
            from scripts.event_timeline import EventTimeline
            
            timeline = EventTimeline()
            
            events = timeline.events[:10]
            
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'year': event.get('year', ''),
                    'title': event.get('title', '')
                })
            
            data = {
                'user_message': request.message,
                'events': formatted_events
            }
        
        elif intent_result['intent'] == 'help':
            data = {'user_message': request.message}
        
        else:  # unknown
            data = {
                'user_message': request.message,
                'error': 'unknown_intent'
            }
        
        # 5. 生成响应
        response_data = dialogue_manager.generate_response(
            intent_result['intent'], 
            data, 
            request.session_id
        )
        
        return ChatResponse(
            response=response_data['response'],
            intent=intent_result['intent'],
            confidence=intent_result['confidence'],
            metadata=response_data['metadata'],
            timestamp=response_data['timestamp']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/history", response_model=List[Dict])
async def get_chat_history(
    session_id: str = Query(..., description="会话 ID"),
    limit: int = Query(default=50, ge=1, le=200, description="返回数量限制")
):
    """获取对话历史
    
    - **session_id**: 会话 ID
    - **limit**: 返回消息数量限制 (默认 50)
    
    返回：最近的对话记录列表
    """
    
    try:
        session = dialogue_manager.get_session(session_id)
        
        messages = session.get('messages', [])[-limit:]
        
        return [
            {
                'role': msg['role'],
                'content': msg['content'],
                'timestamp': msg['timestamp']
            }
            for msg in messages
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/feedback")
async def submit_feedback(
    session_id: str = Query(...),
    rating: int = Query(..., ge=1, le=5, description="评分 1-5"),
    comment: Optional[str] = Query(None)
):
    """提交用户反馈
    
    - **session_id**: 会话 ID
    - **rating**: 评分 (1-5)
    - **comment**: 评论 (可选)
    
    返回：反馈提交结果
    """
    
    try:
        dialogue_manager.collect_feedback(session_id, rating, comment)
        
        return {
            "status": "success",
            "message": "感谢您的反馈！"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/session/{session_id}")
async def get_session_summary(session_id: str):
    """获取会话摘要
    
    - **session_id**: 会话 ID
    
    返回：会话统计信息
    """
    
    try:
        summary = dialogue_manager.get_session_summary(session_id)
        
        return {
            "status": "success",
            "summary": summary
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/chat/session/{session_id}")
async def clear_session(session_id: str):
    """清除会话状态
    
    - **session_id**: 会话 ID
    
    返回：清除结果
    """
    
    try:
        dialogue_manager.clear_session(session_id)
        
        return {
            "status": "success",
            "message": "会话已清除"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 启动命令 ====================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("🤖 AI 对话助手 API v3.0 启动中...")
    print("=" * 80)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
        reload=True
    )
