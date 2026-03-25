#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原文数据库集成测试

功能：
1. 将原文数据库与现有翻译模块集成
2. 优先使用本地数据，网络作为补充
3. 提供统一的搜索接口
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.original_text_db import OriginalTextDatabase


def test_integration():
    """测试原文数据库集成"""
    
    print("=" * 80)
    print("🔗 原文数据库与现有系统集成测试")
    print("=" * 80)
    
    # 创建原文数据库实例
    db = OriginalTextDatabase()
    
    # 1. 搜索功能测试
    print("\n--- 测试 1: 全文搜索 ---")
    
    test_queries = [
        "刘备",
        "赤壁之战", 
        "如虎添翼",
        "唐太宗",
        "范仲淹"
    ]
    
    for query in test_queries:
        results = db.search(query, limit=3)
        
        print(f"\n🔍 搜索：'{query}'")
        
        if len(results) > 0:
            print(f"   ✅ 找到 {len(results)} 条结果:")
            
            for i, r in enumerate(results[:2], 1):
                print(f"      {i}. [{r['dynasty']}{r['year']}]")
                print(f"         原文：{r['content']}")
                
                if r['translation']:
                    print(f"         译文：{r['translation']}")
        else:
            print(f"   ❌ 未找到结果 (将使用网络补充)")
    
    # 2. 按朝代查询测试
    print("\n--- 测试 2: 按朝代查询 ---")
    
    dynasties = ["汉", "唐", "宋"]
    
    for dynasty in dynasties:
        results = db.search_by_dynastry(dynasty, limit=2)
        
        print(f"\n📚 {dynasty}朝记录:")
        
        if len(results) > 0:
            print(f"   ✅ 找到 {len(results)} 条")
            
            for r in results[:1]:
                print(f"      - [{r['year']}] {r['content'][:50]}...")
        else:
            print(f"   ❌ 未找到记录")
    
    # 3. 数据库统计
    print("\n--- 测试 3: 数据库统计 ---")
    
    stats = db.get_statistics()
    
    print(f"\n📊 当前数据库状态:")
    print(f"   总记录数：{stats['total_records']}条")
    
    if stats['by_dynasty']:
        print(f"\n   按朝代分布:")
        for dynasty, count in sorted(stats['by_dynasty'].items(), key=lambda x: -x[1]):
            print(f"      - {dynasty}: {count}条")
    
    # 4. 与现有翻译模块对比
    print("\n--- 测试 4: 与现有翻译模块对比 ---")
    
    from scripts.classical_chinese import ClassicalChineseTranslatorV2
    
    translator = ClassicalChineseTranslatorV2(use_rule_based=True)
    
    test_texts = [
        "刘豫州王室之胄",
        "如虎添翼"
    ]
    
    for text in test_texts:
        # 方法 1: 原文数据库查询
        db_results = db.search(text, limit=1)
        
        if db_results and len(db_results[0]['content']) >= len(text):
            print(f"\n📖 '{text}':")
            print(f"   ✅ 原文数据库匹配:")
            print(f"      原文：{db_results[0]['content']}")
            print(f"      译文：{db_results[0]['translation']}")
        else:
            # 方法 2: 规则翻译
            translated = translator.translate(text)
            
            print(f"\n📖 '{text}':")
            print(f"   ⚠️ 原文数据库未匹配，使用规则翻译:")
            print(f"      译文：{translated}")
    
    # 5. 性能测试
    print("\n--- 测试 5: 查询性能 ---")
    
    import time
    
    queries = ["刘备", "唐太宗", "范仲淹"] * 10  # 30 次查询
    
    start_time = time.time()
    
    for query in queries:
        db.search(query, limit=1)
    
    end_time = time.time()
    
    avg_time = (end_time - start_time) / len(queries) * 1000
    
    print(f"\n⚡ 平均查询时间：{avg_time:.2f}ms")
    
    if avg_time < 50:
        print("   ✅ 性能优秀 (<50ms)")
    elif avg_time < 100:
        print("   ⚠️ 性能良好 (50-100ms)")
    else:
        print("   ❌ 性能一般 (>100ms)")
    
    # 关闭数据库
    db.close()
    
    print("\n" + "=" * 80)
    print("🎉 集成测试完成！")
    print("=" * 80)


def show_usage_guide():
    """显示使用指南"""
    
    print("\n" + "=" * 80)
    print("📚 资治通鉴原文数据库 - 使用指南")
    print("=" * 80)
    
    guide = """
【核心功能】

1. 🔍 全文搜索
   db.search(query, limit=20)
   
   示例:
   results = db.search("刘备", limit=5)
   for r in results:
       print(f"{r['dynasty']}{r['year']}: {r['content']}")

2. 📚 按朝代查询
   db.search_by_dynastry(dynasty, limit=50)
   
   示例:
   han_records = db.search_by_dynastry("汉", limit=10)

3. ➕ 添加原文
   db.add_text(volume, year, dynasty, content, translation, keywords)
   
   示例:
   db.add_text(
       volume="汉纪五十七",
       year="建安十三年", 
       dynasty="东汉",
       content="刘豫州王室之胄，英才盖世...",
       translation="我听说刘备是皇室后裔...",
       keywords=["刘备", "孙权"]
   )

4. 📊 数据库统计
   db.get_statistics()
   
   返回:
   {
       'total_records': 总记录数,
       'by_dynasty': {'汉': 10, '唐': 5},
       'by_source': {'local': 12, 'online': 3}
   }

【集成到现有系统】

在翻译模块中优先使用原文数据库:

from database.original_text_db import OriginalTextDatabase

db = OriginalTextDatabase()

# 搜索原文
results = db.search(classical_text)

if results:
    # 找到匹配，直接使用
    translation = results[0]['translation']
else:
    # 未找到，使用规则翻译或网络补充
    from scripts.classical_chinese import ClassicalChineseTranslatorV2
    translator = ClassicalChineseTranslatorV2()
    translation = translator.translate(classical_text)

【数据扩展】

1. 手动添加：运行 scripts/import_original_texts.py
2. 批量导入：使用 db.bulk_import(texts_list)
3. 网络爬取：结合 BeautifulSoup 获取在线资源

【性能优化建议】

- 优先存储核心朝代 (汉、唐、宋)
- 定期清理重复数据
- 使用 FTS5 全文索引加速查询
- 缓存常用搜索结果

"""
    
    print(guide)


if __name__ == "__main__":
    test_integration()
    show_usage_guide()
