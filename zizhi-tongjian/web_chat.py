#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 Skill - AI 对话助手 Web 界面 (Streamlit)

功能：
1. 智能聊天对话框 🔥 **新增**
2. 会话历史管理 🔥 **新增**
3. 意图识别展示 🔥 **新增**
4. 多轮对话支持 🔥 **新增**
"""

import streamlit as st
import requests
from datetime import datetime
import json

# ==================== 配置 ====================

API_BASE_URL = "http://localhost:8002"  # FastAPI Chat API 地址

st.set_page_config(
    page_title="🤖 资治通鉴 AI 对话助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS 样式 ====================

st.markdown("""
<style>
    .chat-container {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }
    
    .user-message {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        max-width: 70%;
    }
    
    .assistant-message {
        background-color: #ffffff;
        color: #333;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 10px;
        max-width: 70%;
        border: 1px solid #e0e0e0;
    }
    
    .intent-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        margin-left: 10px;
    }
    
    .confidence-high { background-color: #4CAF50; color: white; }
    .confidence-medium { background-color: #FF9800; color: white; }
    .confidence-low { background-color: #F44336; color: white; }
</style>
""", unsafe_allow_html=True)

# ==================== 页面标题 ====================

st.markdown('<h1 style="text-align: center;">🤖 资治通鉴 AI 对话助手</h1>', 
            unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #666; margin-bottom: 2rem;">
    <p>智能搜索 · 文言文翻译 · 人物档案 · 今日锦囊 · 历史沙盘 · 知识图谱</p>
</div>
""", unsafe_allow_html=True)

# ==================== 侧边栏配置 ====================

st.sidebar.title("⚙️ 设置")

# 会话管理
session_id = st.sidebar.text_input(
    "会话 ID", 
    value=f"user_{datetime.now().strftime('%H%M%S')}",
    help="用于保存对话历史，留空则使用随机 ID"
)

if not session_id:
    session_id = f"user_{datetime.now().strftime('%H%M%S')}"

# 显示当前会话信息
session_info = st.sidebar.expander("📊 会话信息", expanded=False)
with session_info:
    st.markdown(f"**当前会话**: {session_id}")
    
    # 获取会话摘要
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/chat/session/{session_id}",
            timeout=5
        )
        
        if response.status_code == 200:
            summary = response.json().get('summary', {})
            
            st.markdown("---")
            st.write(f"**总消息数**: {summary.get('total_messages', 0)}")
            st.write(f"**用户消息**: {summary.get('user_messages', 0)}")
            st.write(f"**助手回复**: {summary.get('assistant_messages', 0)}")
            
            if summary.get('current_intent'):
                st.write(f"**当前意图**: {summary['current_intent']}")
    except:
        pass

# 清除会话按钮
if st.sidebar.button("🗑️ 清除会话"):
    try:
        requests.delete(
            f"{API_BASE_URL}/api/chat/session/{session_id}",
            timeout=5
        )
        st.success("会话已清除！")
        st.rerun()
    except Exception as e:
        st.error(f"清除失败：{str(e)}")

st.sidebar.markdown("---")
st.sidebar.info("""
**功能列表**:
- 🔍 搜索历史案例
- 📖 翻译文言文
- 👤 查询人物档案
- 📅 今日锦囊推荐
- 🎮 模拟历史事件
- 🔗 查询人物关系

输入'帮助'查看完整功能！
""")

# ==================== 聊天界面 ====================

st.header("💬 智能对话")

# 显示会话 ID
col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"📝 当前会话：`{session_id}`")
with col2:
    # 获取历史消息
    try:
        history_response = requests.get(
            f"{API_BASE_URL}/api/chat/history",
            params={"session_id": session_id, "limit": 50},
            timeout=10
        )
        
        if history_response.status_code == 200:
            messages = history_response.json()
            
            # 显示历史消息
            for msg in messages[-10:]:  # 只显示最近 10 条
                if msg['role'] == 'user':
                    st.markdown(f'<div class="user-message">{msg["content"]}</div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message">{msg["content"][:500]}...</div>', 
                               unsafe_allow_html=True)
    except Exception as e:
        st.warning("无法加载历史消息，请确保 API 服务已启动。")

# ==================== 聊天输入框 ====================

col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_area(
        "输入您的问题...",
        height=80,
        placeholder="例如：搜索如虎添翼、翻译刘豫州王室之胄、诸葛亮的人物档案...",
        key="chat_input"
    )

with col2:
    send_button = st.button("🚀 发送", type="primary")

# ==================== 快速建议按钮 ====================

st.markdown("---")
st.markdown("**💡 快速建议**:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔍 搜索案例"):
        user_input = "搜索如虎添翼"
        send_button = True
        
with col2:
    if st.button("📖 翻译文言文"):
        user_input = "翻译刘豫州王室之胄"
        send_button = True
        
with col3:
    if st.button("👤 人物档案"):
        user_input = "诸葛亮的人物传记"
        send_button = True
        
with col4:
    if st.button("📅 今日锦囊"):
        user_input = "今天的智慧是什么"
        send_button = True

# ==================== 发送消息处理 ====================

if send_button and user_input.strip():
    with st.spinner("正在思考..."):
        try:
            # 调用聊天 API
            response = requests.post(
                f"{API_BASE_URL}/api/chat",
                json={
                    "message": user_input,
                    "session_id": session_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                chat_result = response.json()
                
                # 显示助手回复
                st.markdown("---")
                st.markdown(f'<div class="assistant-message">{chat_result["response"]}</div>', 
                           unsafe_allow_html=True)
                
                # 显示意图识别信息
                intent_info = st.expander("🔍 意图识别详情", expanded=False)
                with intent_info:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**识别结果**:")
                        st.write(f"- **意图**: {chat_result['intent']}")
                        st.write(f"- **置信度**: {chat_result['confidence']:.2%}")
                        
                        # 显示置信度徽章
                        confidence = chat_result['confidence']
                        if confidence >= 0.8:
                            badge_class = "confidence-high"
                        elif confidence >= 0.5:
                            badge_class = "confidence-medium"
                        else:
                            badge_class = "confidence-low"
                        
                        st.write(f'<span class="intent-badge {badge_class}">置信度：{confidence:.2%}</span>', 
                               unsafe_allow_html=True)
                    
                    with col2:
                        st.write("**元数据**:")
                        metadata = chat_result.get('metadata', {})
                        for key, value in metadata.items():
                            if isinstance(value, list):
                                st.write(f"- {key}: {len(value)} 项")
                            else:
                                st.write(f"- {key}: {value}")
                
                # 显示反馈按钮
                feedback_col1, feedback_col2 = st.columns(2)
                
                with feedback_col1:
                    if st.button("👍 有帮助"):
                        try:
                            requests.post(
                                f"{API_BASE_URL}/api/chat/feedback",
                                params={
                                    "session_id": session_id,
                                    "rating": 5,
                                    "comment": "回答很有帮助"
                                },
                                timeout=5
                            )
                            st.success("感谢您的反馈！")
                        except:
                            pass
                
                with feedback_col2:
                    if st.button("👎 没帮助"):
                        try:
                            requests.post(
                                f"{API_BASE_URL}/api/chat/feedback",
                                params={
                                    "session_id": session_id,
                                    "rating": 1,
                                    "comment": "回答不够准确"
                                },
                                timeout=5
                            )
                            st.success("感谢您的反馈！")
                        except:
                            pass
                
                # 重新渲染以显示新消息
                st.rerun()
                
            else:
                error_msg = response.json().get('detail', '请求失败')
                st.error(f"❌ {error_msg}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ 无法连接到 AI 对话助手 API，请确保服务已启动：\n\n```bash\ncd api && python3 -m uvicorn chat:app --reload --port 8002\n```")
        
        except Exception as e:
            st.error(f"❌ 发生错误：{str(e)}")

# ==================== 帮助信息 ====================

st.markdown("---")
help_expander = st.expander("📚 功能说明", expanded=False)

with help_expander:
    st.markdown("""
### 🤖 AI 对话助手功能说明
    
#### 🔍 **智能搜索**
- 示例："搜索如虎添翼"、"查找刘邦的故事"
- 返回：相关历史案例列表及核心智慧
    
#### 📖 **文言文翻译**
- 示例："翻译刘豫州王室之胄"、"什么意思"
- 返回：原文注音 + 白话译文
    
#### 👤 **人物档案查询**
- 示例："诸葛亮的人物传记"、"曹操的生平"
- 返回：时期、身份、角色类型、核心特质等
    
#### 📅 **今日锦囊推荐**
- 示例："今天的智慧是什么"、"有什么历史启示"
- 返回：每日精选历史案例及现代应用
    
#### 🎮 **历史事件模拟**
- 示例："如果鸿门宴项羽杀了刘邦会怎样"
- 返回：假设性分析 + 历史对比
    
#### 🔗 **人物关系查询**
- 示例："刘邦和项羽的关系"、"诸葛亮的朋友"
- 返回：盟友、敌人等关系网络

### 💡 **使用技巧**
1. 输入越具体，回答越准确
2. 支持多轮对话，系统会记住上下文
3. 可以追问细节，如"然后呢？"、"为什么？"
4. 随时输入'帮助'查看功能列表
    """)

# ==================== 主程序 ====================

def main():
    """主程序"""
    
    st.markdown("""
<div style="text-align: center; margin-top: 2rem;">
    <p style="color: #999;">资治通鉴 Skill v3.0 - AI 对话助手</p>
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
