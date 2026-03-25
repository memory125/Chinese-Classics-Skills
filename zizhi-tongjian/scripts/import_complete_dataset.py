#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴完整数据集导入工具

功能：
1. 加载生成的 294 卷示例数据
2. 批量导入 SQLite 数据库
3. 进度显示和错误处理
4. 验证导入结果
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from database.original_text_db import OriginalTextDatabase


def load_generated_data() -> list:
    """加载生成的示例数据"""
    
    print("📝 加载生成的示例数据...")
    
    # 定义所有卷册 (294 卷)
    volumes = {
        '周纪': [1, 2, 3, 4, 5],           # 5 卷
        '秦纪': [1],                        # 1 卷
        '汉纪': list(range(1, 61)),         # 60 卷
        '魏纪': list(range(1, 11)),         # 10 卷
        '晋纪': list(range(1, 21)),         # 20 卷
        '宋纪_南朝': list(range(1, 17)),    # 16 卷 (南朝)
        '齐纪': list(range(1, 6)),          # 5 卷
        '梁纪': list(range(1, 23)),         # 22 卷
        '陈纪': list(range(1, 12)),         # 11 卷
        '隋纪': list(range(1, 9)),          # 8 卷
        '唐纪': list(range(1, 90)),         # 89 卷
        '后梁纪': [1],                      # 1 卷
        '后唐纪': list(range(1, 15)),       # 14 卷
        '后晋纪': list(range(1, 11)),       # 10 卷
        '后汉纪': [1],                      # 1 卷
        '后周纪': [1],                      # 1 卷
        '宋纪_北宋南宋': list(range(1, 168)) # 167 卷 (注意与南朝宋区分)
    }
    
    texts = []
    total_volumes = sum(len(vols) for vols in volumes.values())
    
    print(f"   总卷数：{total_volumes}卷")
    
    count = 0
    
    for dynasty, vol_list in volumes.items():
        for vol_num in vol_list:
            # 处理卷名格式
            if '宋纪_北宋南宋' in dynasty:
                volume_name = f"宋纪{vol_num}"
                actual_dynasty = "宋朝"
            elif '宋纪_南朝' in dynasty:
                volume_name = f"宋纪{vol_num}"
                actual_dynasty = "南朝·宋"
            else:
                volume_name = f"{dynasty}{vol_num}"
                actual_dynasty = dynasty
            
            # 生成代表性内容
            content = generate_sample_content(actual_dynasty, vol_num)
            
            texts.append({
                "volume": volume_name,
                "year": get_year_range(actual_dynasty),
                "dynasty": actual_dynasty,
                "content": content,
                "translation": f"{volume_name}的译文内容，记录了当时的历史事件...",
                "keywords": [actual_dynasty, volume_name],
                "source": "generated"
            })
            
            count += 1
            
            if count % 50 == 0:
                print(f"   [{count}/{total_volumes}] {volume_name}")
    
    return texts


def generate_sample_content(dynasty: str, vol_num: int) -> str:
    """生成示例内容"""
    
    samples = {
        '周朝': f"【{dynasty}{vol_num}】周朝时期，诸侯争霸，礼崩乐坏。",
        '秦朝': f"【{dynasty}{vol_num}】秦始皇统一六国，建立中央集权制度。",
        '汉朝': f"【{dynasty}{vol_num}】汉朝盛世，文景之治，汉武帝开疆拓土。",
        '三国·魏': f"【{dynasty}{vol_num}】三国时期，曹操、刘备、孙权三分天下。",
        '晋朝': f"【{dynasty}{vol_num}】西晋统一，八王之乱，五胡乱华。",
        '南朝·宋': f"【{dynasty}{vol_num}】南朝宋齐梁陈更迭，文化繁荣。",
        '南朝·齐': f"【{dynasty}{vol_num}】南朝齐国，萧道成建齐。",
        '南朝·梁': f"【{dynasty}{vol_num}】南朝梁国，萧衍建立梁朝。",
        '南朝·陈': f"【{dynasty}{vol_num}】南朝陈国，陈霸先建陈。",
        '隋朝': f"【{dynasty}{vol_num}】隋朝统一，开皇之治，大运河工程。",
        '唐朝': f"【{dynasty}{vol_num}】唐朝盛世，贞观之治，开元盛世。",
        '五代·后梁': f"【{dynasty}{vol_num}】五代十国时期，朱温建后梁。",
        '五代·后唐': f"【{dynasty}{vol_num}】五代后唐，李存勖建立后唐。",
        '五代·后晋': f"【{dynasty}{vol_num}】五代后晋，石敬瑭建立后晋。",
        '五代·后汉': f"【{dynasty}{vol_num}】五代后汉，刘知远建立后汉。",
        '五代·后周': f"【{dynasty}{vol_num}】五代后周，郭威建立后周。",
        '宋朝': f"【{dynasty}{vol_num}】宋朝文化繁荣，理学兴起，经济发达。"
    }
    
    return samples.get(dynasty, f"【{dynasty}{vol_num}】此卷记载了该时期的历史事件。")


def get_year_range(dynasty: str) -> str:
    """获取年份范围"""
    
    ranges = {
        '周朝': "前 403-前 256 年",
        '秦朝': "前 256-前 207 年",
        '汉朝': "前 206-220 年",
        '三国·魏': "220-265 年",
        '晋朝': "265-420 年",
        '南朝·宋': "420-479 年",
        '南朝·齐': "479-502 年",
        '南朝·梁': "502-557 年",
        '南朝·陈': "557-589 年",
        '隋朝': "581-618 年",
        '唐朝': "618-907 年",
        '五代·后梁': "907-923 年",
        '五代·后唐': "923-936 年",
        '五代·后晋': "936-947 年",
        '五代·后汉': "947-950 年",
        '五代·后周': "951-960 年",
        '宋朝': "960-1279 年"
    }
    
    return ranges.get(dynasty, "未知年份")


def main():
    """主程序"""
    
    print("=" * 80)
    print("💾 资治通鉴完整数据集导入工具 v3.0")
    print("=" * 80)
    
    # 1. 加载数据
    print("\n" + "=" * 80)
    print("📥 Step 1: 加载生成的示例数据 (294 卷)")
    print("=" * 80)
    
    texts = load_generated_data()
    
    print(f"\n✅ 共加载 {len(texts)} 条记录")
    
    # 2. 创建数据库并导入
    print("\n" + "=" * 80)
    print("💾 Step 2: 批量导入到 SQLite 数据库")
    print("=" * 80)
    
    db = OriginalTextDatabase()
    
    result = db.bulk_import(texts)
    
    print(f"\n📊 导入结果:")
    print(f"   总数：{result['total']}")
    print(f"   成功：{result['success']}")
    print(f"   失败：{result['errors']}")
    
    if result['error_details']:
        print(f"\n❌ 错误详情 (前 5 条):")
        for error in result['error_details'][:5]:
            print(f"   - {error}")
    
    # 3. 显示统计信息
    print("\n" + "=" * 80)
    print("📊 Step 3: 数据库统计")
    print("=" * 80)
    
    stats = db.get_statistics()
    
    print(f"\n📚 当前数据库状态:")
    print(f"   总记录数：{stats['total_records']}条")
    print(f"   按朝代分布:")
    
    for dynasty, count in sorted(stats['by_dynasty'].items(), key=lambda x: -x[1]):
        print(f"      - {dynasty}: {count}条")
    
    # 4. 测试搜索功能
    print("\n" + "=" * 80)
    print("🔍 Step 4: 搜索功能测试")
    print("=" * 80)
    
    test_queries = ["汉", "唐", "宋", "周", "三国"]
    
    for query in test_queries:
        results = db.search(query, limit=3)
        
        if results:
            print(f"\n✅ '{query}': 找到 {len(results)} 条")
            
            # 显示前 2 条
            for r in results[:2]:
                content_preview = r['content'][:60] + "..." if len(r['content']) > 60 else r['content']
                
                print(f"   - [{r['dynasty']}{r['year']}]")
                print(f"     {content_preview}")
        else:
            print(f"\n❌ '{query}': 未找到结果")
    
    # 5. 按朝代查询测试
    print("\n" + "=" * 80)
    print("📚 Step 5: 按朝代查询测试")
    print("=" * 80)
    
    dynasties = ["汉", "唐", "宋"]
    
    for dynasty in dynasties:
        results = db.search_by_dynastry(dynasty, limit=2)
        
        if results:
            print(f"\n✅ {dynasty}朝：找到 {len(results)} 条")
            
            for r in results[:1]:
                content_preview = r['content'][:50] + "..." if len(r['content']) > 50 else r['content']
                
                print(f"   - [{r['year']}] {content_preview}")
        else:
            print(f"\n❌ {dynasty}朝：未找到记录")
    
    # 6. 性能测试
    print("\n" + "=" * 80)
    print("⚡ Step 6: 查询性能测试")
    print("=" * 80)
    
    import time
    
    queries = ["汉", "唐", "宋"] * 10  # 30 次查询
    
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
    print("🎉 导入完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
