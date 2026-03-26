# 📚 Chinese Classics Skills (中国经典智慧学习平台)

一个基于 OpenClaw 的智能技能集合，整合了中国四大经典著作的学习工具：《道德经》、《资治通鉴》、《周易》和《黄帝内经》。

---

## 🎯 项目简介

本项目提供四个核心技能模块，帮助用户深入学习和应用中国古代经典智慧：

### 🧘 **0. 道德经 Skill** (daode-jing) ⭐ 新增
- **版本**: v3.0
- **功能**: 
  - ✅ 八十一章完整原文库
  - ✅ 佛学对照解读（200+ 条对照）
  - ✅ 现代场景映射（250+ 应用场景）
  - ✅ 个性化推荐引擎
  - ✅ 白话文智能翻译
  - ✅ 修行实践指南
- **特色**: 
  - 道家智慧现代化应用
  - 佛道思想对比学习
  - 生活/职场场景化解读

### 📖 **1. 资治通鉴 Skill** (zizhi-tongjian)
- **版本**: v3.0
- **功能**: 
  - ✅ RAG v5.0 智能搜索 (200+ 精选案例)
  - ✅ SQLite 原文数据库 (294+ 卷完整内容)
  - ✅ AI 文言文翻译引擎
  - ✅ 人物履历生成器
  - ✅ 今日锦囊推荐系统
  - ✅ 历史沙盘模拟器 (15+ 经典事件)
  - ✅ FastAPI RESTful API + Streamlit Web 界面
- **特色**: 
  - 覆盖战国至北宋 1362 年历史
  - 智能混合搜索 (本地优先 + 网络补充)
  - 多轮对话 AI 助手
  - 现代应用场景映射

### 📜 **3. 周易学习 Skill** (zhouyi-learning)
- **版本**: v1.0
- **功能**:
  - ✅ 六十四卦完整查询系统
  - ✅ 卦辞爻辞白话解读
  - ✅ 起卦解卦工具
  - ✅ 案例分析库
  - ✅ 每日练习题库
  - ✅ 周易哲学智慧解析
- **特色**:
  - 零基础友好设计
  - 实用解卦方法
  - 历史案例辅助理解

### 🌿 **4. 黄帝内经 Skill** (huangdi-neijing)
- **版本**: v1.0
- **功能**:
  - ✅ 基础理论系统讲解
  - ✅ 阴阳五行深度解析
  - ✅ 脏腑经络知识图谱
  - ✅ 病因病机分析工具
  - ✅ 养生之道实践指南
  - ✅ 症状智能分析
- **特色**:
  - 中医经典现代化解读
  - 理论与实践结合
  - 健康养生实用建议

---

## 🚀 快速开始

### 环境要求
```bash
Python 3.8+
OpenClaw CLI
```

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/memory125/Chinese-Classics-Skills.git
   cd Chinese-Classics-Skills
   ```

2. **使用技能**
   
   **方式一：通过 OpenClaw 直接调用（推荐）**
   ```bash
   # 资治通鉴
   "将相和的故事是什么？"
   "分析刘邦的人物履历"
   
   # 周易学习
   "帮我查一下乾卦"
   "今天每日一卦是什么？"
   
   # 道德经
   "道可道非常道的含义是什么？"
   "无为而治在现代管理中的应用"
   
   # 黄帝内经
   "头痛，失眠，乏力怎么办？"
   "春季如何养生？"
   ```

3. **启动独立服务**
   ```bash
   # 资治通鉴 API (端口 8002)
   cd zizhi-tongjian/api
   python3 -m uvicorn main:app --reload --port 8002
   
   # 资治通鉴 Web 界面 (端口 8501)
   cd ..
   streamlit run web_chat.py
   ```

---

## 📁 项目结构

```
Chinese-Classics-Skills/
├── daode-jing/                   # 道德经 Skill (v3.0) ⭐ 新增
│   ├── data/                     # 原文 + 佛学对照 + 场景映射
│   │   ├── jing.txt              # 八十一章原文
│   │   ├── buddhist_comparison.txt  # 200+ 条佛道对照
│   │   └── modern_scenarios.txt  # 250+ 现代应用场景
│   ├── scripts/                  # 核心功能脚本
│   │   ├── main.py               # 主查询引擎
│   │   └── personal_recommendation.py  # 个性化推荐
│   ├── README.md                 # 使用文档
│   └── SKILL.md                  # OpenClaw Skill 定义
│
├── zizhi-tongjian/              # 资治通鉴 Skill (v3.0)
│   ├── api/                      # FastAPI RESTful API
│   ├── database/                 # SQLite 原文数据库
│   ├── scripts/                  # 核心算法脚本
│   ├── chatbot/                  # AI 对话助手
│   ├── data/                     # 案例库 + 原文数据
│   └── web_chat.py               # Streamlit Web 界面
│
├── zhouyi-learning/              # 周易学习 Skill (v1.0)
│   ├── scripts/                  # 六十四卦查询
│   ├── data/                     # 卦辞爻辞库
│   └── references/               # 知识库
│
├── huangdi-neijing/              # 黄帝内经 Skill (v1.0)
│   ├── scripts/                  # 中医分析工具
│   ├── data/                     # 经典原文库
│   └── references/               # 理论知识库
│
├── README.md                     # 本文件
└── LICENSE                       # MIT License
```

---

## 📊 核心功能演示

### 🧘 **道德经 - 智能解读**
```python
from daode-jing.scripts.main import DaodeJingSearcher

searcher = DaodeJingSearcher()
result = searcher.search("无为而治", include_buddhist=True)
print(result['chapter'])      # 原文章节
print(result['interpretation']) # 白话解读
print(result['buddhist_comparison']) # 佛学对照
```

### 🔍 **资治通鉴 - 智能搜索**
```python
from zizhi-tongjian.scripts.hybrid_search_v3 import SmartHybridSearch

rag = SmartHybridSearch()
results = rag.hybrid_search("将相和", top_k=5)

for r in results:
    print(f"{r['name']}: {r['score']}")
```

### 📖 **周易 - 卦象查询**
```python
from zhouyi-learning.scripts.zhouyi_database import get_gua_by_name

qian = get_gua_by_name("乾")
print(qian['interpretation'])
```

### 🌿 **黄帝内经 - 症状分析**
```python
from huangdi-neijing.scripts.health_analysis import HealthAnalyzer

analyzer = HealthAnalyzer()
advice = analyzer.analyze_symptoms("头痛，失眠，乏力")
print(advice)
```

---

## 🎯 使用场景

### 💼 **职场人士**
- 学习历史智慧，提升决策能力
- 应用周易哲学，把握人生机遇
- 黄帝内经养生，保持健康状态

### 📚 **学生群体**
- 系统学习中国传统文化
- 理解经典著作的现代价值
- 培养批判性思维和人文素养

### 🏥 **健康爱好者**
- 中医理论自学
- 个性化养生方案制定
- 症状初步分析和预防

---

## 🔧 技术栈

| 模块 | 技术栈 |
|------|--------|
| **后端框架** | FastAPI + Streamlit |
| **数据库** | SQLite (FTS5) + JSON |
| **AI/ML** | Transformers, RAG v5.0 |
| **可视化** | NetworkX, matplotlib, plotly |
| **前端** | Streamlit Web 界面 |

---

## 📈 项目统计

### 道德经 Skill (v3.0) ⭐ 新增
- ✅ 原文库：81 章完整内容
- ✅ 佛学对照：200+ 条深度对比
- ✅ 场景映射：250+ 现代应用场景
- ✅ 推荐引擎：个性化学习路径

### 资治通鉴 Skill (v3.0)
- ✅ 案例库：200+ 精选历史案例
- ✅ 原文数据库：294+ 卷完整内容
- ✅ API 端点：30+ RESTful 接口
- ✅ Web 页面：7 个功能模块
- ✅ AI 助手：10+ 种意图识别

### 周易学习 Skill (v1.0)
- ✅ 六十四卦：完整查询系统
- ✅ 案例库：50+ 历史解卦案例
- ✅ 练习题库：200+ 每日练习题

### 黄帝内经 Skill (v1.0)
- ✅ 理论模块：阴阳五行/脏腑经络
- ✅ 症状分析：智能诊断工具
- ✅ 养生方案：个性化建议生成

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- Python: PEP8 + Black
- 注释：Google Style Docstrings
- 文档：Markdown 格式

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🔗 相关链接

- **道德经详细文档**: [`daode-jing/README.md`](daode-jing/README.md) ⭐ 新增
- **资治通鉴详细文档**: [`zizhi-tongjian/README.md`](zizhi-tongjian/README.md)
- **周易学习详细文档**: [`zhouyi-learning/README.md`](zhouyi-learning/README.md)
- **黄帝内经详细文档**: [`huangdi-neijing/README.md`](huangdi-neijing/README.md)

---

**🎉 立即开始您的中国经典智慧学习之旅！**

*最后更新：2026-03-26*  
*版本：v1.1 (新增道德经 v3.0)*  
*维护者：memory125*  
*仓库地址：https://github.com/memory125/Chinese-Classics-Skills*
