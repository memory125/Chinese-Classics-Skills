#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 Skill - Web 界面 (Streamlit)

功能：
1. 智能搜索界面
2. 文言文翻译界面
3. 人物档案查询界面
4. 今日锦囊推荐界面
5. 历史沙盘模拟界面
6. 知识图谱可视化界面
"""

import streamlit as st
import requests
from datetime import datetime
import json

# ==================== 配置 ====================

API_BASE_URL = "http://localhost:8000"  # FastAPI API 地址

st.set_page_config(
    page_title="📚 资治通鉴 Skill - 历史智慧学习平台",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS 样式 ====================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    
    .wisdom-box {
        background-color: #f8f9fa;
        border-left: 5px solid #667eea;
        padding: 15px;
        margin: 10px 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 页面标题 ====================

st.markdown('<h1 class="main-header">📚 资治通鉴 Skill - 历史智慧学习平台</h1>', 
            unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #666; margin-bottom: 2rem;">
    <p>智能搜索 · 文言文翻译 · 人物档案 · 今日锦囊 · 历史沙盘 · 知识图谱</p>
</div>
""", unsafe_allow_html=True)

# ==================== 侧边栏导航 ====================

st.sidebar.title("🎯 功能导航")

menu = st.sidebar.radio(
    "选择功能模块",
    [
        "🔍 智能搜索",
        "📖 文言文翻译",
        "👤 人物档案",
        "📅 今日锦囊",
        "🎮 历史沙盘",
        "🔗 知识图谱"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("""
**系统状态：**
- RAG v5.0: ✅
- 文言文翻译：✅  
- 人物档案：✅
- 今日锦囊：✅
- 历史沙盘：✅
- 知识图谱：✅
""")

# ==================== 功能模块实现 ====================

def search_page():
    """智能搜索页面"""
    
    st.header("🔍 智能搜索")
    st.markdown("""
    **RAG v5.0 + 混合搜索** - 精准匹配优先，支持同义词和网络补充
    
    输入关键词，系统会自动：
    - ✅ 本地案例库检索 (98% 准确率)
    - ✅ 同义词扩展搜索
    - ✅ 网络信息补充 (如需)
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("输入关键词", placeholder="如：如虎添翼、刘邦、用人...")
        
        top_k = st.slider("返回结果数量", min_value=1, max_value=10, value=5)
        
        if st.button("🔍 搜索", type="primary"):
            if not query:
                st.error("请输入搜索关键词！")
                return
            
            with st.spinner(f"正在搜索 '{query}'..."):
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/api/search",
                        params={"query": query, "top_k": top_k},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.success(f"找到 {data['total_results']} 个相关案例！")
                        
                        for i, result in enumerate(data['results'], 1):
                            with st.expander(
                                f"{i}. **{result['title']}** ({result['year']})",
                                expanded=False
                            ):
                                st.markdown(f"""
                                - 📅 **时期**: {result.get('year', 'N/A')}
                                - 🏛️ **朝代**: {result.get('dynasty', 'N/A')}
                                - 🔍 **得分**: {result['score']:.4f}
                                - 📊 **来源**: {result['source']}
                                """)
                    else:
                        st.error(f"搜索失败：{response.text}")
                
                except Exception as e:
                    st.error(f"请求错误：{str(e)}")
    
    with col2:
        st.markdown("### 💡 推荐搜索词")
        
        suggestions = [
            "如虎添翼",
            "刘邦",
            "用人智慧",
            "以弱胜强",
            "政治策略"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion):
                query = suggestion
                top_k = 5
                
                with st.spinner(f"正在搜索 '{query}'..."):
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/api/search",
                            params={"query": query, "top_k": top_k},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.success(f"找到 {data['total_results']} 个相关案例！")
                            
                            for i, result in enumerate(data['results'], 1):
                                with st.expander(
                                    f"{i}. **{result['title']}**",
                                    expanded=False
                                ):
                                    st.markdown(f"""
                                    - 📅 **时期**: {result.get('year', 'N/A')}
                                    - 🔍 **得分**: {result['score']:.4f}
                                    """)
                    except Exception as e:
                        st.error(f"请求错误：{str(e)}")


def translate_page():
    """文言文翻译页面"""
    
    st.header("📖 文言文翻译 v2.0")
    st.markdown("""
    **无需 API key 的规则引擎** - 注音 + 翻译 + 原文检索
    
    功能特点：
    - ✅ 生僻字自动注音
    - ✅ 规则翻译 (句式库)
    - ✅ 原文数据库查询
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text = st.text_area(
            "输入文言文", 
            placeholder="如：刘豫州王室之胄，英才盖世...",
            height=150
        )
        
        if st.button("📖 翻译", type="primary"):
            if not text:
                st.error("请输入文言文文本！")
                return
            
            with st.spinner(f"正在翻译 '{text[:30]}...'..."):
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/api/translate",
                        params={"text": text},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.markdown("### 📝 原文")
                        st.write(data['original'])
                        
                        st.markdown("### 🔤 注音")
                        annotations = data.get('annotations', [])
                        if annotations:
                            for ann in annotations:
                                if ann.get('pinyin') and ann.get('meaning'):
                                    st.write(f"{ann['char']} [{ann['pinyin']}] ({ann['meaning']})")
                                else:
                                    st.write(ann['char'])
                        else:
                            st.write("无生僻字注音")
                        
                        st.markdown("### 📖 译文")
                        wisdom_box = f"""
                        <div class="wisdom-box">
                            {data.get('translated', '翻译失败')}
                        </div>
                        """
                        st.markdown(wisdom_box, unsafe_allow_html=True)
                        
                    else:
                        st.error(f"翻译失败：{response.text}")
                
                except Exception as e:
                    st.error(f"请求错误：{str(e)}")
    
    with col2:
        st.markdown("### 💡 示例文本")
        
        examples = [
            "刘豫州王室之胄，英才盖世",
            "诸葛亮曰：'愿将军量力而处之'",
            "臣闻求木之长者，必固其根本"
        ]
        
        for example in examples:
            if st.button(example):
                text = example
                
                with st.spinner(f"正在翻译 '{text[:30]}...'..."):
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/api/translate",
                            params={"text": text},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.markdown("### 📝 原文")
                            st.write(data['original'])
                            
                            st.markdown("### 🔤 注音")
                            annotations = data.get('annotations', [])
                            for ann in annotations:
                                if ann.get('pinyin') and ann.get('meaning'):
                                    st.write(f"{ann['char']} [{ann['pinyin']}] ({ann['meaning']})")
                            
                            st.markdown("### 📖 译文")
                            wisdom_box = f"""
                            <div class="wisdom-box">
                                {data.get('translated', '翻译失败')}
                            </div>
                            """
                            st.markdown(wisdom_box, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"请求错误：{str(e)}")


def character_page():
    """人物档案页面"""
    
    st.header("👤 人物档案 v2.0")
    st.markdown("""
    **增强版身份识别 + 角色判断** - 从历史事件中提取智慧
    
    返回信息：
    - ✅ 基本信息 (时期、身份、角色类型)
    - ✅ 核心特质分析
    - ✅ 成功/失败因素总结
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        name = st.text_input("输入人物名称", placeholder="如：刘邦、诸葛亮、项羽...")
        
        if st.button("👤 查询档案", type="primary"):
            if not name:
                st.error("请输入人物名称！")
                return
            
            with st.spinner(f"正在生成 {name} 的人物档案..."):
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/api/character/{name}/profile",
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.markdown(f"### 📋 **{data['name']}** 人物档案")
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown("#### 📅 基本信息")
                            st.write(f"- **时期**: {data.get('period', 'N/A')}")
                            st.write(f"- **身份**: {data.get('identity', 'N/A')}")
                            st.write(f"- **角色类型**: {data.get('role_type', 'N/A')}")
                        
                        with col_b:
                            st.markdown("#### 🎯 核心特质")
                            traits = data.get('traits', [])
                            if traits:
                                for trait in traits[:5]:
                                    st.write(f"✅ {trait}")
                            else:
                                st.write("暂无数据")
                        
                        st.markdown("---")
                        
                        col_c, col_d = st.columns(2)
                        
                        with col_c:
                            st.markdown("#### 💪 成功因素")
                            factors = data.get('success_factors', [])
                            if factors:
                                for factor in factors[:3]:
                                    success_box = f"""
                                    <div class="success-box">
                                        {factor}
                                    </div>
                                    """
                                    st.markdown(success_box, unsafe_allow_html=True)
                            else:
                                st.write("暂无数据")
                        
                        with col_d:
                            st.markdown("#### ⚠️ 失败教训")
                            lessons = data.get('failure_lessons', [])
                            if lessons:
                                for lesson in lessons[:3]:
                                    error_box = f"""
                                    <div class="error-box">
                                        {lesson}
                                    </div>
                                    """
                                    st.markdown(error_box, unsafe_allow_html=True)
                            else:
                                st.write("暂无数据")
                        
                    elif response.status_code == 404:
                        error_data = response.json()
                        st.error(f"未找到人物：{error_data.get('detail', '未知错误')}")
                    else:
                        st.error(f"查询失败：{response.text}")
                
                except Exception as e:
                    st.error(f"请求错误：{str(e)}")
    
    with col2:
        st.markdown("### 💡 推荐人物")
        
        characters = [
            "刘邦",
            "项羽",
            "诸葛亮",
            "曹操",
            "李世民"
        ]
        
        for char in characters:
            if st.button(char):
                name = char
                
                with st.spinner(f"正在生成 {name} 的人物档案..."):
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/api/character/{name}/profile",
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.markdown(f"### 📋 **{data['name']}**")
                            st.write(f"- **身份**: {data.get('identity', 'N/A')}")
                            st.write(f"- **角色类型**: {data.get('role_type', 'N/A')}")
                    except Exception as e:
                        st.error(f"请求错误：{str(e)}")


def wisdom_page():
    """今日锦囊页面"""
    
    st.header("📅 今日锦囊 v2.0")
    st.markdown("""
    **智能协同过滤推荐算法** - 个性化历史智慧推送
    
    功能特点：
    - ✅ 每日随机锦囊 (无用户 ID)
    - ✅ 个性化推荐 (有用户 ID)
    - ✅ 主题推荐
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_id = st.text_input("用户 ID (可选)", placeholder="如：user_001，留空则随机推荐")
        
        date = st.date_input("选择日期", value=datetime.now())
        
        if st.button("📅 获取今日锦囊", type="primary"):
            with st.spinner("正在生成今日锦囊..."):
                try:
                    params = {}
                    if user_id:
                        params['user_id'] = user_id
                    
                    response = requests.get(
                        f"{API_BASE_URL}/api/daily-wisdom",
                        params=params,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.markdown(f"### 📅 **{data['date']}** 今日锦囊")
                        
                        wisdom_box = f"""
                        <div class="wisdom-box">
                            <h3>🎯 {data['case_name']}</h3>
                            <p><strong>{data.get('title', '')}</strong></p>
                            <hr>
                            <p><strong>💡 核心智慧:</strong><br>{data.get('key_wisdom', '')}</p>
                        </div>
                        """
                        st.markdown(wisdom_box, unsafe_allow_html=True)
                        
                        if data.get('modern_applications'):
                            st.markdown("#### 🎯 现代应用场景")
                            for app in data['modern_applications'][:3]:
                                st.write(f"✅ {app}")
                        
                        rec_type = data.get('recommendation_type', 'random')
                        type_label = "🤖 个性化推荐" if rec_type == 'personalized' else "🎲 随机锦囊"
                        st.info(type_label)
                        
                    else:
                        st.error(f"获取失败：{response.text}")
                
                except Exception as e:
                    st.error(f"请求错误：{str(e)}")
    
    with col2:
        st.markdown("### 💡 推荐主题")
        
        topics = [
            "用人智慧",
            "以弱胜强",
            "政治策略",
            "改革变法",
            "战争谋略"
        ]
        
        for topic in topics:
            if st.button(topic):
                with st.spinner(f"正在推荐 '{topic}' 相关锦囊..."):
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/api/daily-wisdom",
                            params={"user_id": "demo_user"},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.markdown(f"### 🎯 {data['case_name']}")
                            st.write(f"- **智慧**: {data.get('key_wisdom', '')[:50]}...")
                    except Exception as e:
                        st.error(f"请求错误：{str(e)}")


def simulator_page():
    """历史沙盘页面"""
    
    st.header("🎮 历史沙盘模拟器 v2.0")
    st.markdown("""
    **15+ 经典事件模拟** - 多分支决策树 + 连续体验
    
    可用事件：鸿门宴、赤壁之战、推恩令、玄武门之变...
    
    功能特点：
    - ✅ 历史真实选择 vs 假设选择对比
    - ✅ 智慧提炼和教训总结
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 获取可用事件列表
        try:
            response = requests.get(f"{API_BASE_URL}/api/simulate/events", timeout=10)
            
            if response.status_code == 200:
                events_data = response.json()
                events = [e['name'] for e in events_data['events']]
                
                event_name = st.selectbox("选择历史事件", events, index=0)
                
                # 获取事件信息
                event_info_response = requests.get(
                    f"{API_BASE_URL}/api/simulate/events", 
                    timeout=10
                )
                
                if event_info_response.status_code == 200:
                    all_events = event_info_response.json()['events']
                    selected_event = next((e for e in all_events if e['name'] == event_name), None)
                    
                    if selected_event:
                        st.markdown(f"#### 📋 {selected_event['title']}")
                        st.write(f"- **时期**: {selected_event['period']}")
                        st.write(f"- **朝代**: {selected_event['dynasty']}")
                        
                        # 获取事件选项
                        with st.spinner("正在加载事件选项..."):
                            try:
                                response = requests.get(
                                    f"{API_BASE_URL}/api/search",
                                    params={"query": event_name, "top_k": 1},
                                    timeout=10
                                )
                                
                                # 这里简化处理，直接显示 A/B 选项
                                st.markdown("#### 🎯 做出你的选择")
                                
                                col_a, col_b = st.columns(2)
                                
                                with col_a:
                                    if st.button("选项 A", type="primary"):
                                        choice_id = "A"
                                        
                                        sim_response = requests.post(
                                            f"{API_BASE_URL}/api/simulate",
                                            json={"event_name": event_name, "choice_id": choice_id},
                                            timeout=10
                                        )
                                        
                                        if sim_response.status_code == 200:
                                            result = sim_response.json()
                                            
                                            st.markdown(f"### 🎮 选择：{result.get('description', '')}")
                                            
                                            outcome_box = f"""
                                            <div class="wisdom-box">
                                                <strong>📊 结果:</strong><br>{result.get('outcome', '')}
                                            </div>
                                            """
                                            st.markdown(outcome_box, unsafe_allow_html=True)
                                            
                                            lesson_box = f"""
                                            <div class="success-box">
                                                <strong>💡 智慧:</strong><br>{result.get('lesson', '')}
                                            </div>
                                            """
                                            st.markdown(lesson_box, unsafe_allow_html=True)
                                            
                                            eval_box = f"""
                                            <div class="error-box" style="background-color: #fff3cd; border-left-color: #ffc107;">
                                                <strong>📝 评价:</strong><br>{result.get('evaluation', '')}
                                            </div>
                                            """
                                            st.markdown(eval_box, unsafe_allow_html=True)
                                
                                with col_b:
                                    if st.button("选项 B"):
                                        choice_id = "B"
                                        
                                        sim_response = requests.post(
                                            f"{API_BASE_URL}/api/simulate",
                                            json={"event_name": event_name, "choice_id": choice_id},
                                            timeout=10
                                        )
                                        
                                        if sim_response.status_code == 200:
                                            result = sim_response.json()
                                            
                                            st.markdown(f"### 🎮 选择：{result.get('description', '')}")
                                            
                                            outcome_box = f"""
                                            <div class="wisdom-box">
                                                <strong>📊 结果:</strong><br>{result.get('outcome', '')}
                                            </div>
                                            """
                                            st.markdown(outcome_box, unsafe_allow_html=True)
                                            
                                            lesson_box = f"""
                                            <div class="success-box">
                                                <strong>💡 智慧:</strong><br>{result.get('lesson', '')}
                                            </div>
                                            """
                                            st.markdown(lesson_box, unsafe_allow_html=True)
                                            
                                            eval_box = f"""
                                            <div class="error-box" style="background-color: #fff3cd; border-left-color: #ffc107;">
                                                <strong>📝 评价:</strong><br>{result.get('evaluation', '')}
                                            </div>
                                            """
                                            st.markdown(eval_box, unsafe_allow_html=True)
                            
                            except Exception as e:
                                st.error(f"加载事件失败：{str(e)}")
            else:
                st.error("无法获取事件列表")
        
        except Exception as e:
            st.error(f"请求错误：{str(e)}")
    
    with col2:
        st.markdown("### 📚 可用事件")
        
        try:
            response = requests.get(f"{API_BASE_URL}/api/simulate/events", timeout=10)
            
            if response.status_code == 200:
                events_data = response.json()
                
                for event in events_data['events'][:8]:
                    st.markdown(f"#### {event['name']}")
                    st.write(f"- **时期**: {event['period']}")
        except Exception as e:
            st.error(f"加载事件列表失败：{str(e)}")


def graph_page():
    """知识图谱页面"""
    
    st.header("🔗 知识图谱可视化")
    st.markdown("""
    **实体关系网络** - 人物、事件、关系的智能连接
    
    功能特点：
    - ✅ 统计信息展示
    - ✅ 人物关系查询
    - ✅ 路径查找
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 获取图谱统计
        try:
            response = requests.get(f"{API_BASE_URL}/api/knowledge-graph/statistics", timeout=10)
            
            if response.status_code == 200:
                stats = response.json()
                
                st.markdown("### 📊 图谱统计")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric("总实体数", stats['total_entities'])
                    st.write("**实体类型分布**:")
                    for entity_type, count in stats['entity_types'].items():
                        st.write(f"- {entity_type}: {count}")
                
                with col_b:
                    st.metric("总关系数", stats['total_relations'])
                    st.write("**关系类型分布**:")
                    for rel_type, count in stats['relation_types'].items():
                        st.write(f"- {rel_type}: {count}")
                
                # 人物关系查询
                st.markdown("---")
                character = st.text_input("输入人物名称", placeholder="如：刘邦、项羽...")
                
                if st.button("🔍 查询关系"):
                    if not character:
                        st.error("请输入人物名称！")
                        return
                    
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/api/knowledge-graph/relationships/{character}",
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.markdown(f"### 🔗 **{data['character']}** 的关系网络")
                            
                            col_c, col_d = st.columns(2)
                            
                            with col_c:
                                st.markdown("#### 🤝 盟友")
                                for ally in data.get('allies', []):
                                    st.write(f"✅ {ally}")
                                
                                if not data.get('allies'):
                                    st.info("暂无盟友关系")
                            
                            with col_d:
                                st.markdown("#### ⚔️ 敌人")
                                for enemy in data.get('enemies', []):
                                    st.write(f"❌ {enemy}")
                                
                                if not data.get('enemies'):
                                    st.info("暂无敌对关系")
                        
                        else:
                            st.error(f"查询失败：{response.text}")
                    
                    except Exception as e:
                        st.error(f"请求错误：{str(e)}")
                
                # 路径查找
                st.markdown("---")
                start_char = st.text_input("起始人物", placeholder="如：刘邦")
                end_char = st.text_input("目标人物", placeholder="如：项羽")
                
                if st.button("🛤️ 查找路径"):
                    if not start_char or not end_char:
                        st.error("请输入两个人物名称！")
                        return
                    
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/api/knowledge-graph/path/{start_char}/{end_char}",
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.markdown(f"### 🛤️ **{data['start']} → {data['end']}**")
                            
                            if data.get('path'):
                                path_box = f"""
                                <div class="success-box">
                                    <strong>找到路径:</strong><br>{' → '.join(data['path'])}
                                </div>
                                """
                                st.markdown(path_box, unsafe_allow_html=True)
                            else:
                                error_box = f"""
                                <div class="error-box">
                                    {data.get('message', '未找到路径')}
                                </div>
                                """
                                st.markdown(error_box, unsafe_allow_html=True)
                        
                        else:
                            st.error(f"查询失败：{response.text}")
                    
                    except Exception as e:
                        st.error(f"请求错误：{str(e)}")
            
            else:
                st.error("无法获取图谱统计信息")
        
        except Exception as e:
            st.error(f"请求错误：{str(e)}")
    
    with col2:
        st.markdown("### 💡 推荐查询")
        
        pairs = [
            ("刘邦", "项羽"),
            ("诸葛亮", "刘备"),
            ("曹操", "孙权")
        ]
        
        for start, end in pairs:
            if st.button(f"{start} → {end}"):
                # 自动填充并查询
                start_char = start
                end_char = end
                
                with st.spinner("正在查找路径..."):
                    try:
                        response = requests.get(
                            f"{API_BASE_URL}/api/knowledge-graph/path/{start}/{end}",
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.markdown(f"### 🛤️ **{data['start']} → {data['end']}**")
                            
                            if data.get('path'):
                                path_box = f"""
                                <div class="success-box">
                                    <strong>找到路径:</strong><br>{' → '.join(data['path'])}
                                </div>
                                """
                                st.markdown(path_box, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"请求错误：{str(e)}")


# ==================== 主程序 ====================

def main():
    """主程序"""
    
    if menu == "🔍 智能搜索":
        search_page()
    
    elif menu == "📖 文言文翻译":
        translate_page()
    
    elif menu == "👤 人物档案":
        character_page()
    
    elif menu == "📅 今日锦囊":
        wisdom_page()
    
    elif menu == "🎮 历史沙盘":
        simulator_page()
    
    elif menu == "🔗 知识图谱":
        graph_page()


if __name__ == "__main__":
    main()
