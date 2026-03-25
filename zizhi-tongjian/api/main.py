#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 Skill - FastAPI RESTful API

功能：
1. 智能搜索接口
2. 人物档案接口
3. 今日锦囊接口
4. 历史沙盘模拟接口
5. 文言文翻译接口
6. 知识图谱查询接口
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.hybrid_search_v3 import SmartHybridSearch
from scripts.classical_chinese import ClassicalChineseTranslatorV2
from scripts.character_trajectory_v2 import CharacterTrajectoryGeneratorV2
from scripts.daily_wisdom_v2 import DailyWisdomV2
from scripts.historical_simulator_v2 import HistoricalSimulatorV2
from scripts.knowledge_graph import KnowledgeGraph

# 初始化核心组件
rag = SmartHybridSearch()
translator = ClassicalChineseTranslatorV2(use_rule_based=True)
generator = CharacterTrajectoryGeneratorV2(rag)
daily = DailyWisdomV2()
simulator = HistoricalSimulatorV2()
kg = KnowledgeGraph()

# 创建 FastAPI 应用
app = FastAPI(
    title="资治通鉴 Skill API",
    description="""
## 📚 资治通鉴历史智慧学习平台 API
    
### 核心功能：
- 🔍 **智能搜索**: RAG v5.0 + 混合搜索
- 📖 **文言文翻译**: 无需 API key 的规则引擎
- 👤 **人物档案**: 增强版身份识别 + 角色判断
- 📅 **今日锦囊**: 智能协同过滤推荐
- 🎮 **历史沙盘**: 15+ 经典事件模拟
- 🔗 **知识图谱**: 实体关系网络查询
    
### 使用示例：
```bash
# 搜索
GET /api/search?query=如虎添翼&top_k=3

# 人物档案
GET /api/character/{name}/profile

# 今日锦囊
GET /api/daily-wisdom?user_id=user_001

# 历史沙盘模拟
POST /api/simulate
{
    "event_name": "鸿门宴",
    "choice_id": "A"
}
```
""",
    version="2.0.0",
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


# ==================== 请求/响应模型 ====================

class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str = Field(..., description="搜索关键词")
    top_k: int = Field(default=5, ge=1, le=20, description="返回结果数量 (1-20)")


class CharacterProfileResponse(BaseModel):
    """人物档案响应模型"""
    name: str
    period: Optional[str] = None
    identity: Optional[str] = None
    role_type: Optional[str] = None
    traits: List[str] = []
    success_factors: List[str] = []
    failure_lessons: List[str] = []


class DailyWisdomResponse(BaseModel):
    """今日锦囊响应模型"""
    date: str
    case_name: str
    title: str
    key_wisdom: Optional[str] = None
    recommendation_type: str = "random"


class EventSimulationRequest(BaseModel):
    """历史沙盘模拟请求模型"""
    event_name: str = Field(..., description="事件名称")
    choice_id: str = Field(..., description="选项 ID (A/B/C...)")


class EventSimulationResponse(BaseModel):
    """历史沙盘模拟响应模型"""
    event_name: str
    title: str
    period: Optional[str] = None
    dynasty: Optional[str] = None
    protagonist: List[str] = []
    background: Optional[str] = None
    choice_id: Optional[str] = None
    description: Optional[str] = None
    outcome: Optional[str] = None
    lesson: Optional[str] = None
    evaluation: Optional[str] = None
    is_historical_choice: bool = False


class KnowledgeGraphResponse(BaseModel):
    """知识图谱响应模型"""
    total_entities: int
    total_relations: int
    entity_types: Dict[str, int]
    relation_types: Dict[str, int]


# ==================== API 端点 ====================

@app.get("/", tags=["根路径"])
async def root():
    """API 根路径"""
    return {
        "message": "📚 资治通鉴 Skill API v2.0",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/api/health", tags=["系统"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "components": {
            "rag": "✅" if len(rag.case_db) > 30 else "❌",
            "translator": "✅" if translator.use_rule_based else "❌",
            "simulator": "✅" if len(simulator.list_available_events()) >= 15 else "❌",
            "knowledge_graph": "✅" if len(kg.entities) > 100 else "❌"
        }
    }


@app.get("/api/search", tags=["智能搜索"])
async def search(
    query: str = Query(..., description="搜索关键词"),
    top_k: int = Query(default=5, ge=1, le=20, description="返回结果数量")
):
    """
    智能搜索接口
    
    - **query**: 搜索关键词 (如：如虎添翼、刘邦、用人)
    - **top_k**: 返回结果数量 (默认 5，最大 20)
    
    支持：
    - 精准匹配搜索
    - 同义词搜索
    - 现代主题网络补充
    """
    
    if not query:
        raise HTTPException(status_code=400, detail="query 参数不能为空")
    
    try:
        results = rag.hybrid_search(query, top_k=top_k)
        
        formatted_results = []
        for r in results:
            case_data = rag.case_db.get(r['name'], {})
            
            formatted_results.append({
                "name": r['name'],
                "title": case_data.get('title', ''),
                "score": round(r.get('score', 0), 4),
                "source": r.get('source', 'local'),
                "year": case_data.get('year', ''),
                "dynasty": case_data.get('dynasty', '')
            })
        
        return {
            "query": query,
            "total_results": len(formatted_results),
            "results": formatted_results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败：{str(e)}")


@app.get("/api/search/{query}", tags=["智能搜索"])
async def search_by_path(query: str, top_k: int = Query(default=5)):
    """通过 URL 路径搜索"""
    return await search(query=query, top_k=top_k)


@app.get("/api/character/{name}/profile", tags=["人物档案"])
async def get_character_profile(name: str):
    """
    获取人物档案
    
    - **name**: 人物名称 (如：刘邦、诸葛亮、项羽)
    
    返回信息包括：
    - 基本信息 (时期、身份、角色类型)
    - 核心特质
    - 成功因素
    - 失败教训
    """
    
    if not name:
        raise HTTPException(status_code=400, detail="name 参数不能为空")
    
    try:
        profile = generator.generate_profile(name)
        
        if 'error' in profile:
            raise HTTPException(status_code=404, detail=profile['error'])
        
        return {
            "name": profile.get('name', ''),
            "period": profile.get('period', ''),
            "identity": profile.get('identity', ''),
            "role_type": profile.get('role_type', ''),
            "traits": profile.get('traits', [])[:10],  # 限制前 10 个特质
            "success_factors": profile.get('success_factors', [])[:5],
            "failure_lessons": profile.get('failure_lessons', [])[:5]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取人物档案失败：{str(e)}")


@app.get("/api/character/{name}/timeline", tags=["人物档案"])
async def get_character_timeline(name: str):
    """
    获取人物时间线
    
    - **name**: 人物名称
    
    返回该人物的关键事件时间线
    """
    
    if not name:
        raise HTTPException(status_code=400, detail="name 参数不能为空")
    
    try:
        profile = generator.generate_profile(name)
        
        if 'error' in profile:
            raise HTTPException(status_code=404, detail=profile['error'])
        
        timeline = profile.get('timeline', [])[:15]  # 限制前 15 个事件
        
        formatted_timeline = []
        for event in timeline:
            formatted_timeline.append({
                "year": event.get('year', ''),
                "event": event.get('event', ''),
                "outcome": event.get('outcome', ''),
                "wisdom": event.get('wisdom', '')[:100] if event.get('wisdom') else ''
            })
        
        return {
            "name": name,
            "total_events": len(formatted_timeline),
            "timeline": formatted_timeline
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取时间线失败：{str(e)}")


@app.get("/api/daily-wisdom", tags=["今日锦囊"])
async def get_daily_wisdom(
    date: Optional[str] = Query(None, description="日期 (YYYY-MM-DD)"),
    user_id: Optional[str] = Query(None, description="用户 ID，用于个性化推荐")
):
    """
    获取今日锦囊
    
    - **date**: 指定日期，如果为 None 则使用今天
    - **user_id**: 用户 ID，如果有则返回个性化推荐
    
    返回：
    - 今日历史智慧案例
    - 核心智慧总结
    - 现代应用场景
    """
    
    try:
        # 解析日期
        from datetime import datetime
        
        if date:
            try:
                parsed_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD")
        else:
            parsed_date = None
        
        wisdom = daily.get_daily_wisdom(parsed_date, user_id)
        
        if 'error' in wisdom:
            raise HTTPException(status_code=500, detail=wisdom['error'])
        
        return {
            "date": wisdom.get('date', ''),
            "case_name": wisdom.get('case_name', ''),
            "title": wisdom.get('title', ''),
            "key_wisdom": wisdom.get('key_wisdom', ''),
            "modern_applications": wisdom.get('modern_applications', [])[:3],
            "recommendation_type": wisdom.get('recommendation_type', 'random')
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取今日锦囊失败：{str(e)}")


@app.post("/api/simulate", tags=["历史沙盘"], response_model=EventSimulationResponse)
async def simulate_event(request: EventSimulationRequest):
    """
    历史沙盘模拟
    
    - **event_name**: 事件名称 (如：鸿门宴、赤壁之战)
    - **choice_id**: 选项 ID (A/B/C...)
    
    返回选择结果和历史对比分析
    """
    
    if not request.event_name:
        raise HTTPException(status_code=400, detail="event_name 不能为空")
    
    if not request.choice_id:
        raise HTTPException(status_code=400, detail="choice_id 不能为空")
    
    try:
        # 先获取事件信息
        event_info = simulator.get_event_info(request.event_name)
        
        if not event_info:
            raise HTTPException(
                status_code=404, 
                detail=f'未找到事件"{request.event_name}"，可用事件：{simulator.list_available_events()}'
            )
        
        # 做出选择
        result = simulator.make_choice(request.event_name, request.choice_id)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return EventSimulationResponse(
            event_name=request.event_name,
            title=event_info['title'],
            period=event_info['period'],
            dynasty=event_info['dynasty'],
            protagonist=event_info['protagonists'],
            background=simulator.events[request.event_name]['background'],
            choice_id=result.get('choice_id'),
            description=result.get('description'),
            outcome=result.get('outcome'),
            lesson=result.get('lesson'),
            evaluation=result.get('evaluation'),
            is_historical_choice=result.get('is_historical_choice', False)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模拟失败：{str(e)}")


@app.get("/api/simulate/events", tags=["历史沙盘"])
async def list_simulatable_events():
    """列出所有可模拟的事件"""
    
    events = simulator.list_available_events()
    
    event_list = []
    for event_name in events:
        info = simulator.get_event_info(event_name)
        
        if info:
            event_list.append({
                "name": event_name,
                "title": info['title'],
                "period": info['period'],
                "dynasty": info['dynasty']
            })
    
    return {
        "total_events": len(event_list),
        "events": sorted(event_list, key=lambda x: x['name'])
    }


@app.get("/api/translate", tags=["文言文翻译"])
async def translate_classical_chinese(
    text: str = Query(..., description="文言文文本")
):
    """
    文言文翻译接口
    
    - **text**: 需要翻译的文言文文本
    
    返回：
    - 注音信息
    - 规则翻译结果
    """
    
    if not text:
        raise HTTPException(status_code=400, detail="text 参数不能为空")
    
    try:
        # 注音
        annotations = translator.annotate_pinyin(text)
        
        # 翻译
        translated = translator.translate(text)
        
        return {
            "original": text,
            "annotations": [
                {
                    "char": item['char'],
                    "pinyin": item.get('pinyin', ''),
                    "meaning": item.get('meaning', '')
                }
                for item in annotations if 'char' in item
            ],
            "translated": translated,
            "has_llm_api": False  # 当前使用规则翻译，无需 API key
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"翻译失败：{str(e)}")


@app.get("/api/knowledge-graph/statistics", tags=["知识图谱"])
async def get_kg_statistics():
    """获取知识图谱统计信息"""
    
    try:
        visualizer = None
        from scripts.interactive_graph import InteractiveGraphVisualizer
        visualizer = InteractiveGraphVisualizer(kg)
        
        stats = visualizer.export_statistics()
        
        return {
            "total_entities": stats['total_entities'],
            "total_relations": stats['total_relations'],
            "entity_types": stats['entity_types'],
            "relation_types": stats['relation_types']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败：{str(e)}")


@app.get("/api/knowledge-graph/relationships/{character}", tags=["知识图谱"])
async def get_character_relationships(character: str):
    """
    获取指定人物的关系网络
    
    - **character**: 人物名称 (如：刘邦、项羽)
    
    返回：
    - 盟友列表
    - 敌人列表
    - 其他关系
    """
    
    if not character:
        raise HTTPException(status_code=400, detail="character 参数不能为空")
    
    try:
        from scripts.character_graph import CharacterGraph
        
        graph = CharacterGraph()
        
        relationships = graph.get_relationships(character)
        
        if 'error' in relationships:
            raise HTTPException(status_code=404, detail=relationships['error'])
        
        return {
            "character": character,
            "allies": relationships.get('ally', []),
            "enemies": relationships.get('enemy', []),
            "master_servant": relationships.get('master_servant', []),
            "family": relationships.get('family', [])
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取关系失败：{str(e)}")


@app.get("/api/knowledge-graph/path/{start}/{end}", tags=["知识图谱"])
async def find_path(start: str, end: str):
    """
    查找两个人物之间的最短路径
    
    - **start**: 起始人物名称
    - **end**: 目标人物名称
    
    返回：
    - 关系路径列表
    """
    
    if not start or not end:
        raise HTTPException(status_code=400, detail="start 和 end 参数不能为空")
    
    try:
        from scripts.character_graph import CharacterGraph
        
        graph = CharacterGraph()
        
        path = graph.find_shortest_path(start, end)
        
        if not path:
            return {
                "start": start,
                "end": end,
                "path": None,
                "message": f"未找到从'{start}'到'{end}'的直接关系路径"
            }
        
        return {
            "start": start,
            "end": end,
            "path": path,
            "length": len(path) - 1,
            "message": f"找到路径：{' → '.join(path)}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查找路径失败：{str(e)}")


@app.get("/api/events/timeline", tags=["事件时间线"])
async def get_event_timeline(
    dynasty: Optional[str] = Query(None, description="朝代筛选 (如：汉、唐)"),
    limit: int = Query(default=20, ge=1, le=50, description="返回数量限制")
):
    """
    获取事件时间线
    
    - **dynasty**: 可选，按朝代筛选
    - **limit**: 返回数量限制 (默认 20)
    
    返回：
    - 按年代排序的历史事件列表
    """
    
    try:
        from scripts.event_timeline import EventTimeline
        
        timeline = EventTimeline()
        
        if dynasty:
            events = timeline.get_events_by_dynasty(dynasty)
        else:
            events = timeline.events[:limit]
        
        formatted_events = []
        for event in events[:limit]:
            formatted_events.append({
                "year": event['year'],
                "title": event['title'],
                "dynasty": event['dynasty'],
                "category": event['category'],
                "protagonists": event['protagonists']
            })
        
        return {
            "total_events": len(formatted_events),
            "filtered_by_dynasty": dynasty,
            "events": formatted_events
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取时间线失败：{str(e)}")


# ==================== 启动命令 ====================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("🚀 资治通鉴 Skill API v2.0 启动中...")
    print("=" * 80)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
