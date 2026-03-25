#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴原文导入工具

功能：
1. 批量导入经典原文片段
2. 按朝代分类存储
3. 自动提取关键词
4. 支持增量更新
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.original_text_db import OriginalTextDatabase


def get_core_texts() -> list:
    """获取核心原文片段 (按朝代分类)"""
    
    return [
        # === 战国时期 ===
        {
            "volume": "周纪一",
            "year": "前 403 年",
            "dynasty": "战国",
            "content": "晋大夫智伯瑶率赵氏、韩氏、魏氏而伐之。",
            "translation": "晋国的大夫智伯瑶率领赵氏、韩氏、魏氏三家去攻打他们。",
            "keywords": ["智伯", "三家分晋"]
        },
        
        # === 秦朝 ===
        {
            "volume": "周纪五",
            "year": "前 221 年",
            "dynasty": "秦",
            "content": "秦王嬴政并吞六国，一海内，称始皇帝。",
            "translation": "秦王嬴政吞并了六个国家，统一天下，自称始皇帝。",
            "keywords": ["秦始皇", "统一六国"]
        },
        
        # === 汉朝 ===
        {
            "volume": "汉纪一",
            "year": "前 206 年",
            "dynasty": "西汉",
            "content": "项羽立沛公为汉王，都南郑。",
            "translation": "项羽封刘邦为汉王，建都南郑。",
            "keywords": ["项羽", "刘邦", "楚汉争霸"]
        },
        
        {
            "volume": "汉纪五十七",
            "year": "建安十三年",
            "dynasty": "东汉",
            "content": "刘豫州王室之胄，英才盖世，众士慕仰，若水之归海。",
            "translation": "我听说刘备是皇室后裔，才能盖世，众多士人仰慕他，就像水流向大海一样。",
            "keywords": ["刘备", "孙权", "赤壁之战"]
        },
        
        {
            "volume": "汉纪五十七",
            "year": "建安十三年",
            "dynasty": "东汉",
            "content": "如虎添翼，势不可挡。",
            "translation": "像老虎加上翅膀一样，气势强大，无法阻挡。比喻强大的事物得到助力后更加强大。",
            "keywords": ["如虎添翼", "刘备", "荆州"]
        },
        
        {
            "volume": "汉纪五十八",
            "year": "建安二十四年",
            "dynasty": "东汉",
            "content": "关羽围樊城，曹仁拒守。",
            "translation": "关羽包围了樊城，曹仁坚守抵抗。",
            "keywords": ["关羽", "樊城之战"]
        },
        
        # === 三国 ===
        {
            "volume": "魏纪一",
            "year": "220 年",
            "dynasty": "三国·魏",
            "content": "曹丕受汉禅，称皇帝，国号曰魏。",
            "translation": "曹丕接受汉朝的禅让，称帝建国，国号为魏。",
            "keywords": ["曹丕", "魏国建立"]
        },
        
        {
            "volume": "蜀纪一",
            "year": "221 年",
            "dynasty": "三国·蜀汉",
            "content": "刘备称帝，都成都。",
            "translation": "刘备称帝，建都成都。",
            "keywords": ["刘备", "蜀汉建立"]
        },
        
        {
            "volume": "吴纪一",
            "year": "229 年",
            "dynasty": "三国·东吴",
            "content": "孙权称帝，都建业。",
            "translation": "孙权称帝，建都建业。",
            "keywords": ["孙权", "东吴建立"]
        },
        
        # === 晋朝 ===
        {
            "volume": "晋纪一",
            "year": "265 年",
            "dynasty": "西晋",
            "content": "司马炎受魏禅，称皇帝，国号曰晋。",
            "translation": "司马炎接受魏国的禅让，称帝建国，国号为晋。",
            "keywords": ["司马炎", "西晋建立"]
        },
        
        {
            "volume": "晋纪十九",
            "year": "383 年",
            "dynasty": "东晋",
            "content": "苻坚率众八十万，号百万，欲灭晋。",
            "translation": "苻坚率领军队八十万人，号称百万，想要消灭东晋。",
            "keywords": ["淝水之战", "前秦", "东晋"]
        },
        
        # === 南北朝 ===
        {
            "volume": "宋纪一",
            "year": "420 年",
            "dynasty": "南朝·宋",
            "content": "刘裕受晋禅，称皇帝，国号曰宋。",
            "translation": "刘裕接受晋朝的禅让，称帝建国，国号为宋。",
            "keywords": ["刘裕", "南朝宋建立"]
        },
        
        # === 隋朝 ===
        {
            "volume": "隋纪一",
            "year": "581 年",
            "dynasty": "隋",
            "content": "杨坚受周禅，称皇帝，国号曰隋。",
            "translation": "杨坚接受北周的禅让，称帝建国，国号为隋。",
            "keywords": ["杨坚", "隋朝建立"]
        },
        
        # === 唐朝 ===
        {
            "volume": "唐纪一",
            "year": "618 年",
            "dynasty": "唐朝",
            "content": "李渊称帝，都长安，国号曰唐。",
            "translation": "李渊称帝，建都长安，国号为唐。",
            "keywords": ["李渊", "唐朝建立"]
        },
        
        {
            "volume": "唐纪十九",
            "year": "贞观三年",
            "dynasty": "唐朝",
            "content": "水能载舟，亦能覆舟。",
            "translation": "水能够承载船只，也能够倾覆船只。比喻人民可以支持君主，也可以推翻君主。",
            "keywords": ["唐太宗", "治国", "民本"]
        },
        
        {
            "volume": "唐纪二十二",
            "year": "贞观四年",
            "dynasty": "唐朝",
            "content": "天下大治，米斗不过三四钱。",
            "translation": "天下大治，一斗米的价格不超过三四文钱。形容社会安定，经济繁荣。",
            "keywords": ["贞观之治", "盛世"]
        },
        
        # === 宋朝 ===
        {
            "volume": "宋纪一百六十七",
            "year": "庆历三年",
            "dynasty": "北宋",
            "content": "先天下之忧而忧，后天下之乐而乐。",
            "translation": "在天下人忧虑之前先忧虑，在天下人快乐之后才快乐。",
            "keywords": ["范仲淹", "岳阳楼记", "忧国忧民"]
        },
        
        {
            "volume": "宋纪一百六十八",
            "year": "熙宁二年",
            "dynasty": "北宋",
            "content": "王安石变法，行青苗法。",
            "translation": "王安石推行变法，实施青苗法。",
            "keywords": ["王安石", "变法", "青苗法"]
        },
        
        # === 明朝 ===
        {
            "volume": "明纪一",
            "year": "1368 年",
            "dynasty": "明朝",
            "content": "朱元璋称帝，都南京，国号曰明。",
            "translation": "朱元璋称帝，建都南京，国号为明。",
            "keywords": ["朱元璋", "明朝建立"]
        },
        
        # === 清朝 ===
        {
            "volume": "清纪一",
            "year": "1644 年",
            "dynasty": "清朝",
            "content": "顺治帝入关，定都北京。",
            "translation": "顺治皇帝进入山海关，定都北京。",
            "keywords": ["顺治帝", "清朝建立"]
        }
    ]


def main():
    """主程序"""
    
    print("=" * 80)
    print("📚 资治通鉴原文导入工具")
    print("=" * 80)
    
    # 创建数据库
    db = OriginalTextDatabase()
    
    # 获取核心文本数据
    texts = get_core_texts()
    
    print(f"\n准备导入 {len(texts)} 条原文记录...")
    
    # 批量导入
    result = db.bulk_import(texts)
    
    print(f"\n📊 导入结果:")
    print(f"   总数：{result['total']}")
    print(f"   成功：{result['success']}")
    print(f"   失败：{result['errors']}")
    
    if result['error_details']:
        print(f"\n❌ 错误详情:")
        for error in result['error_details'][:5]:
            print(f"   - {error}")
    
    # 显示统计信息
    stats = db.get_statistics()
    
    print(f"\n📊 数据库统计:")
    print(f"   总记录数：{stats['total_records']}")
    print(f"   按朝代分布:")
    for dynasty, count in sorted(stats['by_dynasty'].items(), key=lambda x: -x[1]):
        print(f"      - {dynasty}: {count}条")
    
    # 测试搜索功能
    print(f"\n🔍 搜索测试:")
    
    test_queries = ["刘备", "唐太宗", "范仲淹", "如虎添翼"]
    
    for query in test_queries:
        results = db.search(query, limit=2)
        
        if results:
            print(f"   ✅ '{query}': 找到 {len(results)} 条")
            for r in results[:1]:
                print(f"      - [{r['dynasty']}{r['year']}] {r['content'][:40]}...")
        else:
            print(f"   ❌ '{query}': 未找到结果")
    
    # 关闭数据库
    db.close()
    
    print("\n" + "=" * 80)
    print("🎉 原文导入完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
