#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加"田忌赛马"案例到 cases.json

核心概念：以弱胜强，策略制胜
"""

import json
from pathlib import Path

def main():
    json_path = Path(__file__).parent.parent / "data" / "cases.json"
    
    # 加载现有数据
    with open(json_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)
    
    # 田忌赛马案例
    tianjisaima_case = {
        "title": "田忌赛马 - 以弱胜强的经典策略",
        "volume": "卷第一·周纪一·威烈王二十三年 (典故出自《史记》)",
        "dynasty": "战国",
        "year": "公元前 354 年",
        "key_wisdom": "田忌赛马的核心智慧：在整体实力不如对手的情况下，通过巧妙的策略安排，扬长避短，以弱胜强。孙膑建议用下等马对上等马、上等马对中等马、中等马对下等马，三局两胜。这体现了：1) 资源优化配置 2) 差异化竞争 3) 整体最优而非局部最优的思维方式。",
        "modern_applications": [
            {
                "scenario": "商业竞争策略",
                "action": "避开对手优势领域，在细分市场竞争",
                "example": "小公司不与巨头正面竞争，专注 niche 市场"
            },
            {
                "scenario": "资源优化配置",
                "action": "将有限资源投入到最能产生价值的地方",
                "example": "创业团队集中火力攻克核心功能，而非面面俱到"
            },
            {
                "scenario": "比赛/竞技策略",
                "action": "根据对手特点制定针对性战术",
                "example": "乒乓球比赛中针对对手弱点发球"
            }
        ],
        "protagonists": ["田忌", "孙膑", "齐威王"],
        "background": "战国时期，齐国大将田忌经常与齐威王赛马。双方各出上、中、下三等马，每等马比一次，三局两胜。田忌每次都是上等对上等、中等对中等、下等对下等，结果总是输。后来孙膑给田忌出主意：用下等马对齐威王的上等马（必输），用上等马对齐威王的中等马（必胜），用中等马对齐威王的下等马（必胜）。结果三局两胜，田忌赢了。这就是著名的'田忌赛马'故事，体现了策略和智慧的重要性。"
    }
    
    # 添加案例
    cases["田忌赛马"] = tianjisaima_case
    
    # 保存
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已添加'田忌赛马'案例")
    print(f"当前案例总数：{len(cases)}")

if __name__ == "__main__":
    main()
