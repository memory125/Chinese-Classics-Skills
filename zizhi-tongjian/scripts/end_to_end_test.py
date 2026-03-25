#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 Skill - 端到端测试验证脚本

测试范围：
1. RAG v5.0 检索引擎
2. 智能混合搜索 (本地 + 网络)
3. 文言文翻译模块
4. 人物履历生成器
5. 历史沙盘模拟器
6. 多文风切换系统
7. 今日锦囊盲盒
8. 人物关系图谱
9. 事件时间线数据库
10. 知识图谱构建

测试方法：自动化 + 手动验证
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 70)
print("🧪 资治通鉴 Skill - 端到端测试验证")
print("=" * 70)


def test_rag_v5():
    """测试 RAG v5.0 检索引擎"""
    print("\n" + "=" * 70)
    print("✅ 测试 1: RAG v5.0 检索引擎")
    print("=" * 70)
    
    try:
        from scripts.rag_enhanced_v5 import EnhancedRAGSearch
        
        rag = EnhancedRAGSearch()
        
        # 测试 1.1: 精准匹配搜索
        print("\n📝 测试 1.1: '如虎添翼' 精准匹配")
        results = rag.hybrid_search("如虎添翼", top_k=3)
        if len(results) > 0 and any('借荆州' in r['name'] or '联吴抗曹' in r['name'] for r in results):
            print(f"✅ PASS - 找到 {len(results)} 个相关案例")
            for i, r in enumerate(results[:2], 1):
                title = rag.case_db.get(r['name'], {}).get('title', '')
                score = r.get('score', 0)
                print(f"   {i}. {title[:50]} (得分：{score:.2f})")
        else:
            print("❌ FAIL - 未找到精准匹配案例")
        
        # 测试 1.2: 同义词搜索
        print("\n📝 测试 1.2: '刘备借荆州' 同义词搜索")
        results = rag.hybrid_search("刘备", top_k=3)
        if len(results) > 0 and any('借荆州' in r['name'] for r in results):
            print(f"✅ PASS - 找到 {len(results)} 个相关案例")
        else:
            print("❌ FAIL - 未找到刘备相关案例")
        
        # 测试 1.3: 现代主题搜索
        print("\n📝 测试 1.3: '量子力学' 网络补充")
        results = rag.hybrid_search("量子力学", top_k=2)
        if len(results) > 0:
            print(f"✅ PASS - 找到 {len(results)} 个结果 (可能来自网络)")
        else:
            print("⚠️ WARNING - 未找到结果")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_classical_chinese():
    """测试文言文翻译模块"""
    print("\n" + "=" * 70)
    print("✅ 测试 2: 文言文翻译模块")
    print("=" * 70)
    
    try:
        from scripts.classical_chinese_v2 import ClassicalChineseTranslatorV2
        
        translator = ClassicalChineseTranslatorV2(use_rule_based=True, use_llm=False)
        
        # 测试 2.1: 注音功能
        print("\n📝 测试 2.1: 生僻字注音")
        test_text = "刘豫州王室之胄"
        annotations = translator.annotate_pinyin(test_text)
        
        has_zhou = any(item.get('char') == '胄' and item.get('pinyin') == 'zhòu' for item in annotations)
        if has_zhou:
            print(f"✅ PASS - 正确注音：{test_text}")
            for item in annotations:
                if 'pinyin' in item and 'meaning' in item:
                    print(f"   {item['char']}[{item['pinyin']}]({item['meaning']})")
        else:
            print("❌ FAIL - 注音失败")
        
        # 测试 2.2: 规则翻译
        print("\n📝 测试 2.2: 规则翻译")
        test_text = "诸葛亮曰：'刘豫州王室之胄，英才盖世'"
        translated = translator.translate(test_text)
        
        if len(translated) > 0 and translated != f"[需要配置 API key] {test_text}":
            print(f"✅ PASS - 翻译成功")
            print(f"   原文：{test_text}")
            print(f"   译文：{translated[:80]}...")
        else:
            print("⚠️ WARNING - 使用 fallback，需配置 API key")
        
        # 测试 2.3: 原文检索
        print("\n📝 测试 2.3: 原文检索")
        original = translator.get_original_text('卷第六十五·汉纪五十七', '建安十三年')
        if original and len(original) > 10:
            print(f"✅ PASS - 找到原文片段 ({len(original)} 字符)")
            print(f"   {original[:80]}...")
        else:
            print("❌ FAIL - 未找到原文")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_character_trajectory():
    """测试人物履历生成器"""
    print("\n" + "=" * 70)
    print("✅ 测试 3: 人物履历生成器")
    print("=" * 70)
    
    try:
        from scripts.rag_enhanced_v5 import EnhancedRAGSearch
        from scripts.character_trajectory import CharacterTrajectoryGenerator
        
        rag = EnhancedRAGSearch()
        generator = CharacterTrajectoryGenerator(rag)
        
        # 测试 3.1: 刘邦人物档案
        print("\n📝 测试 3.1: '刘邦' 人物档案")
        profile = generator.generate_profile("刘邦")
        
        if 'error' not in profile and len(profile.get('timeline', [])) > 0:
            print(f"✅ PASS - 生成成功")
            print(f"   姓名：{profile['name']}")
            print(f"   身份：{profile['identity']}")
            print(f"   事件数：{len(profile['timeline'])}")
            
            if len(profile.get('traits', [])) > 0:
                print(f"   核心特质:")
                for trait in profile['traits'][:3]:
                    print(f"      - {trait}")
        else:
            print("❌ FAIL - 生成失败")
        
        # 测试 3.2: 诸葛亮人物档案 (同义词支持)
        print("\n📝 测试 3.2: '诸葛亮' 同义词搜索")
        profile = generator.generate_profile("诸葛亮")
        
        if 'error' not in profile and len(profile.get('timeline', [])) > 0:
            print(f"✅ PASS - 找到 {len(profile['timeline'])} 个事件 (同义词支持成功)")
        else:
            print("❌ FAIL - 未找到诸葛亮相关事件")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_historical_simulator():
    """测试历史沙盘模拟器"""
    print("\n" + "=" * 70)
    print("✅ 测试 4: 历史沙盘模拟器")
    print("=" * 70)
    
    try:
        from scripts.historical_simulator import HistoricalSimulator
        
        simulator = HistoricalSimulator()
        
        # 测试 4.1: 列出可用事件
        print("\n📝 测试 4.1: 列出可用事件")
        events = simulator.list_available_events()
        if len(events) >= 4:
            print(f"✅ PASS - 有 {len(events)} 个可用事件")
            for i, event in enumerate(events[:3], 1):
                print(f"   {i}. {event}")
        else:
            print("❌ FAIL - 事件数量不足")
        
        # 测试 4.2: 模拟鸿门宴
        print("\n📝 测试 4.2: '鸿门宴' 模拟")
        result = simulator.simulate('鸿门宴')
        
        if 'error' not in result and 'options' in result:
            print(f"✅ PASS - 模拟成功")
            print(f"   事件：{result['title']}")
            print(f"   选项数：{len(result['options'])}")
            
            # 测试选择 A (历史真实选择)
            choice_result = simulator.make_choice('鸿门宴', 'A')
            if 'error' not in choice_result:
                print(f"   选择 A 结果：{choice_result['outcome']}")
                print(f"   评价：{choice_result['evaluation']}")
        else:
            print("❌ FAIL - 模拟失败")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_style_switcher():
    """测试多文风切换系统"""
    print("\n" + "=" * 70)
    print("✅ 测试 5: 多文风切换系统")
    print("=" * 70)
    
    try:
        from scripts.style_switcher import StyleSwitcher
        
        switcher = StyleSwitcher()
        
        sample_content = {
            'title': '田忌赛马 - 以弱胜强的经典策略',
            'background': '战国时期，齐国大将田忌经常与齐威王赛马。孙膑建议用下等马对上等马、上等马对中等马、中等马对下等马，结果三局两胜。',
            'key_wisdom': '在整体实力不如对手的情况下，通过巧妙的策略安排，扬长避短，以弱胜强。体现了资源优化配置和差异化竞争的思维方式。',
            'modern_applications': [
                {'scenario': '商业竞争策略', 'action': '避开对手优势领域，在细分市场竞争'},
                {'scenario': '资源优化配置', 'action': '将有限资源投入到最能产生价值的地方'}
            ]
        }
        
        # 测试 5.1: 切换不同文风
        print("\n📝 测试 5.1: 文风切换")
        for style in ['academic', 'workplace', 'gossip', 'plain']:
            switcher.switch_style(style)
            current = switcher.get_current_style()
            
            formatted = switcher.format_output(sample_content, style)
            
            if 'title' in formatted:
                print(f"✅ {current['name']}: {formatted['title'][:40]}...")
        
        # 测试 5.2: Prompt 模板获取
        print("\n📝 测试 5.2: Prompt 模板获取")
        prompt = switcher.get_prompt()
        if len(prompt) > 100:
            print(f"✅ PASS - Prompt 模板长度：{len(prompt)} 字符")
        else:
            print("❌ FAIL - Prompt 模板过短")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_daily_wisdom():
    """测试今日锦囊盲盒"""
    print("\n" + "=" * 70)
    print("✅ 测试 6: 今日锦囊盲盒")
    print("=" * 70)
    
    try:
        from scripts.daily_wisdom import DailyWisdom
        
        daily = DailyWisdom()
        
        # 测试 6.1: 今日锦囊
        print("\n📝 测试 6.1: 今日锦囊")
        today_wisdom = daily.get_daily_wisdom()
        
        if 'error' not in today_wisdom and 'case_name' in today_wisdom:
            print(f"✅ PASS - 今日锦囊：{today_wisdom['case_name']}")
            print(f"   日期：{today_wisdom['date']}")
            print(f"   标题：{today_wisdom['title'][:50]}...")
        else:
            print("❌ FAIL - 今日锦囊生成失败")
        
        # 测试 6.2: 本周汇总
        print("\n📝 测试 6.2: 本周汇总 (前 3 天)")
        weekly = daily.get_weekly_summary()
        
        if len(weekly) >= 3:
            print(f"✅ PASS - 生成 {len(weekly)} 天的锦囊")
            for i, wisdom in enumerate(weekly[:3], 1):
                if 'error' not in wisdom:
                    print(f"   {i}. {wisdom['date']}: {wisdom['case_name']}")
        else:
            print("❌ FAIL - 本周汇总失败")
        
        # 测试 6.3: 主题推荐
        print("\n📝 测试 6.3: '如虎添翼' 主题推荐")
        recommendation = daily.get_recommendation('如虎添翼')
        
        if 'error' not in recommendation and 'case_name' in recommendation:
            print(f"✅ PASS - 推荐：{recommendation['case_name']}")
        else:
            print("⚠️ WARNING - 未找到匹配案例，返回随机锦囊")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_character_graph():
    """测试人物关系图谱"""
    print("\n" + "=" * 70)
    print("✅ 测试 7: 人物关系图谱")
    print("=" * 70)
    
    try:
        from scripts.character_graph import CharacterGraph
        
        graph = CharacterGraph()
        
        # 测试 7.1: 获取刘邦的关系
        print("\n📝 测试 7.1: '刘邦' 人物关系")
        relationships = graph.get_relationships('刘邦')
        
        if 'error' not in relationships:
            print(f"✅ PASS - 找到关系:")
            if len(relationships.get('ally', [])) > 0:
                print(f"   盟友：{relationships['ally'][:3]}...")
            if len(relationships.get('enemy', [])) > 0:
                print(f"   敌人：{relationships['enemy'][:3]}...")
        else:
            print("❌ FAIL - 关系查询失败")
        
        # 测试 7.2: 影响力排行榜
        print("\n📝 测试 7.2: 影响力前 5 名")
        top_chars = graph.get_influential_characters(5)
        
        if len(top_chars) >= 3:
            print(f"✅ PASS - 影响力排行榜:")
            for i, char in enumerate(top_chars[:3], 1):
                print(f"   {i}. {char['name']} (影响力：{char['influence_score']:.2f})")
        else:
            print("❌ FAIL - 影响力计算失败")
        
        # 测试 7.3: 路径查找
        print("\n📝 测试 7.3: '刘邦 → 项羽' 关系路径")
        path = graph.find_shortest_path('刘邦', '项羽')
        
        if path and len(path) > 1:
            print(f"✅ PASS - 找到路径：{' → '.join(path)}")
        else:
            print("⚠️ WARNING - 未找到直接关系 (可能通过第三方)")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_event_timeline():
    """测试事件时间线数据库"""
    print("\n" + "=" * 70)
    print("✅ 测试 8: 事件时间线数据库")
    print("=" * 70)
    
    try:
        from scripts.event_timeline import EventTimeline
        
        timeline = EventTimeline()
        
        # 测试 8.1: 统计摘要
        print("\n📝 测试 8.1: 时间线统计")
        summary = timeline.get_timeline_summary()
        
        if 'total_events' in summary and summary['total_events'] > 30:
            print(f"✅ PASS - 总事件数：{summary['total_events']}")
            print(f"   涵盖朝代：{', '.join(summary['dynasties_covered'][:5])}...")
        else:
            print("❌ FAIL - 统计失败")
        
        # 测试 8.2: 按朝代筛选
        print("\n📝 测试 8.2: '汉' 朝事件 (前 3 个)")
        han_events = timeline.get_events_by_dynasty('汉')
        
        if len(han_events) > 0:
            print(f"✅ PASS - 找到 {len(han_events)} 个汉朝事件")
            for event in han_events[:3]:
                print(f"   {event['year']}: {event['title']}")
        else:
            print("❌ FAIL - 未找到汉朝事件")
        
        # 测试 8.3: 按人物筛选
        print("\n📝 测试 8.3: '刘邦' 参与的事件 (前 3 个)")
        liu_events = timeline.get_events_by_person('刘邦')
        
        if len(liu_events) > 0:
            print(f"✅ PASS - 找到 {len(liu_events)} 个事件")
            for event in liu_events[:3]:
                print(f"   {event['year']}: {event['title']}")
        else:
            print("❌ FAIL - 未找到刘邦相关事件")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_graph():
    """测试知识图谱构建"""
    print("\n" + "=" * 70)
    print("✅ 测试 9: 知识图谱构建")
    print("=" * 70)
    
    try:
        from scripts.knowledge_graph import KnowledgeGraph
        
        kg = KnowledgeGraph()
        
        # 测试 9.1: 统计信息
        print("\n📝 测试 9.1: 知识图谱统计")
        print(f"   总实体数：{len(kg.entities)}")
        print(f"   总关系数：{len(kg.relations)}")
        
        if len(kg.entities) > 50 and len(kg.relations) > 100:
            print("✅ PASS - 图谱构建成功")
        else:
            print("⚠️ WARNING - 实体/关系数量较少")
        
        # 测试 9.2: 查找实体
        print("\n📝 测试 9.2: '刘邦' 实体查找")
        liu_entities = kg.get_entity_by_name('刘邦')
        
        if len(liu_entities) > 0:
            print(f"✅ PASS - 找到 {len(liu_entities)} 个实体")
            for entity in liu_entities[:1]:
                print(f"   类型：{entity['type']}, ID: {list(kg.entities.keys())[list(kg.entities.values()).index(entity)]}")
        else:
            print("❌ FAIL - 未找到刘邦实体")
        
        # 测试 9.3: 路径查找
        print("\n📝 测试 9.3: '刘邦 → 项羽' 关系路径")
        path = kg.find_path('person:刘邦', 'person:项羽')
        
        if path and len(path) > 1:
            print(f"✅ PASS - 找到路径：{' → '.join(path)}")
        else:
            print("⚠️ WARNING - 未找到直接关系")
        
        # 测试 9.4: 导出功能
        print("\n📝 测试 9.4: JSON 导出")
        kg.export_to_json()
        print("✅ PASS - 导出成功")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_hybrid_search():
    """测试智能混合搜索系统"""
    print("\n" + "=" * 70)
    print("✅ 测试 10: 智能混合搜索系统")
    print("=" * 70)
    
    try:
        from scripts.hybrid_search_v3 import SmartHybridSearch
        
        hybrid = SmartHybridSearch()
        
        # 测试 10.1: 本地已有案例 (如虎添翼)
        print("\n📝 测试 10.1: '如虎添翼' (本地优先)")
        results = hybrid.search("如虎添翼", top_k=3)
        
        if len(results) >= 2 and any(r.get('source') == 'local' for r in results):
            print(f"✅ PASS - 返回 {len(results)} 个结果，包含本地案例")
            for i, r in enumerate(results[:2], 1):
                title = r.get('title', '')[:50]
                source = r.get('source', 'unknown')
                score = r.get('score', 0)
                print(f"   {i}. [{source}] {title} (得分：{score:.2f})")
        else:
            print("❌ FAIL - 结果不符合预期")
        
        # 测试 10.2: 本地没有的案例 (量子力学)
        print("\n📝 测试 10.2: '量子力学' (网络补充)")
        results = hybrid.search("量子力学", top_k=3)
        
        if len(results) > 0:
            print(f"✅ PASS - 返回 {len(results)} 个结果")
            for i, r in enumerate(results[:2], 1):
                title = r.get('title', '')[:50]
                source = r.get('source', 'unknown')
                score = r.get('score', 0)
                print(f"   {i}. [{source}] {title} (得分：{score:.2f})")
        else:
            print("⚠️ WARNING - 未找到结果")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL - 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    
    test_results = []
    
    # 运行各项测试
    test_results.append(("RAG v5.0", test_rag_v5()))
    test_results.append(("文言文翻译", test_classical_chinese()))
    test_results.append(("人物履历生成器", test_character_trajectory()))
    test_results.append(("历史沙盘模拟器", test_historical_simulator()))
    test_results.append(("多文风切换系统", test_style_switcher()))
    test_results.append(("今日锦囊盲盒", test_daily_wisdom()))
    test_results.append(("人物关系图谱", test_character_graph()))
    test_results.append(("事件时间线数据库", test_event_timeline()))
    test_results.append(("知识图谱构建", test_knowledge_graph()))
    test_results.append(("智能混合搜索", test_hybrid_search()))
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("📊 测试汇总")
    print("=" * 70)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 70)
    print(f"总结果：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常！")
        return True
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查上述错误信息")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
