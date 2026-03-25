#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易统一数据库 — ZhouyiDatabase v4.0 (全名键版)

提供对 64 卦数据的统一访问接口，支持：
- 按卦名查询（支持全称"乾为天"和简称"乾"）
- 按主题/场景搜索  
- 卦象关系计算（错卦、综卦、互卦）
- 爻辞解析

v4.0 更新:
- 使用全名作为主键，避免冲突
- 保持向后兼容的单字查询接口
"""

import re
import os
from typing import Dict, List, Optional, Any

class ZhouyiDatabase:
    """周易数据库 — 统一数据访问层"""
    
    def __init__(self):
        """初始化数据库"""
        self.gua_data = {}  # Key: 全名如"乾为天"
        self.name_index = {}  # Index: 单字 → 全名 (如"乾"→"乾为天")
        
        self._load_builtin_data()
        self._parse_markdown_data()
    
    def _load_builtin_data(self):
        """加载内置基础数据（乾、坤两卦，含完整爻辞）"""
        # 全名作为键
        self.gua_data = {
            "乾为天": {
                "name": "乾为天",
                "hexagram": "䷀",
                "guaci": "元亨利贞",
                "baihua": "大吉大利，利于坚守正道",
                "core_spirit": "刚健自强，持续进取",
                "application": "事业开创、领导力展现",
                "yao_ci": {
                    1: {"original": "潜龙勿用", "baihua": "能力未成熟时韬光养晦"},
                    2: {"original": "见龙在田，利见大人", "baihua": "初显才华时寻求导师"},
                    3: {"original": "君子终日乾乾，夕惕若厉无咎", "baihua": "事业上升期加倍谨慎"},
                    4: {"original": "或跃在渊，无咎", "baihua": "关键转折时可进可退"},
                    5: {"original": "飞龙在天，利见大人", "baihua": "事业巅峰期大展宏图"},
                    6: {"original": "亢龙有悔", "baihua": "得意时警惕过刚易折"}
                },
                "themes": ["事业", "领导力", "进取", "创业"],
                "cases": ["创业初期韬光养晦：时机未到时积累比展示更重要"]
            },
            "坤为地": {
                "name": "坤为地",
                "hexagram": "䷁",
                "guaci": "元亨利牝马之贞，君子有终吉",
                "baihua": "像母马柔顺坚持，持之以恒吉祥",
                "core_spirit": "包容承载，顺势而为",
                "application": "团队合作、学习积累",
                "yao_ci": {
                    1: {"original": "履霜，坚冰至", "baihua": "见微知著，防患未然"},
                    2: {"original": "直方大，不习无不利", "baihua": "培养天性胜过勉强"},
                    3: {"original": "含章可贞，或从王事无成有终", "baihua": "内敛锋芒，不抢功劳"},
                    4: {"original": "括囊，无咎无誉", "baihua": "乱世中明哲保身"},
                    5: {"original": "黄裳，元吉", "baihua": "谦逊低调反而获吉"},
                    6: {"original": "龙战于野，其血玄黄", "baihua": "阴盛极必争，两败俱伤"}
                },
                "themes": ["合作", "包容", "耐心", "积累"],
                "cases": ["见微知著防患未然：小问题往往是更大问题的前兆"]
            }
        }
        
        # 建立单字索引（向后兼容）
        self.name_index = {
            "乾": "乾为天",
            "坤": "坤为地"
        }
    
    def _parse_markdown_data(self):
        """从 Markdown 文件解析完整 64 卦数据"""
        md_file = '/home/wing/.openclaw/workspace/skills/zhouyi-learning/references/六十四卦终极版_v10.md'
        
        if not os.path.exists(md_file):
            print(f"⚠️ 未找到数据文件：{md_file}")
            return
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 逐行解析状态机
            current_gua = None
            parsed_count = 0
            
            for line in lines:
                line_stripped = line.strip()
                
                # 检测新卦块开始：### 数字。卦名䷀
                gua_header_match = re.match(r'###\s+\d+\.\s+([\u4e00-\u9fff]+)([\u4DC0-\u4DFF])', line_stripped)
                
                if gua_header_match:
                    # 保存上一个卦（如果有）
                    if current_gua and 'name' in current_gua:
                        self._save_gua(current_gua)
                        parsed_count += 1
                    
                    # 开始新卦
                    gua_full_name = gua_header_match.group(1)  # "乾为天"或"水天需"
                    hexagram = gua_header_match.group(2)
                    
                    # 提取单字 key（用于索引）
                    if '为' in gua_full_name:
                        gua_key = gua_full_name[0]  # "乾为天" → "乾"
                    else:
                        gua_key = gua_full_name[-1]  # "水天需" → "需"
                    
                    # 跳过已存在的内置数据（乾、坤）
                    if gua_full_name in self.gua_data:
                        current_gua = None
                        continue
                    
                    current_gua = {
                        "name": gua_full_name,
                        "hexagram": hexagram,
                        "guaci": "",
                        "baihua": "",
                        "core_spirit": "",
                        "application": "",
                        "yao_ci": {},
                        "themes": [],
                        "cases": [],
                        "_key": gua_key  # 临时存储单字 key，用于建立索引
                    }
                
                # 解析表格字段（| **卦形** | 六阳爻 |）
                elif current_gua and '|' in line_stripped:
                    field_match = re.match(r'\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|', line_stripped)
                    if field_match:
                        key = field_match.group(1).strip()
                        value = field_match.group(2).strip()
                        
                        field_map = {
                            '卦辞': 'guaci',
                            '白话': 'baihua', 
                            '核心精神': 'core_spirit',
                            '应用场景': 'application'
                        }
                        
                        if key in field_map:
                            current_gua[field_map[key]] = value
                
                # 提取典型案例：> **案例标题**: 内容
                elif current_gua and line_stripped.startswith('> **'):
                    case_match = re.match(r'>\s*\*\*([^:]+)\*\*:\s*(.+)', line_stripped)
                    if case_match:
                        title = case_match.group(1).strip()
                        content = case_match.group(2).strip()
                        current_gua['cases'].append(f"{title}: {content}")
            
            # 保存最后一个卦
            if current_gua and 'name' in current_gua:
                self._save_gua(current_gua)
            
            print(f"✅ 从 Markdown 解析了 {parsed_count} 个卦象")
            print(f"📊 总计：{len(self.gua_data)} 个卦在数据库中")
            
        except Exception as e:
            print(f"❌ 解析失败：{e}")
            import traceback
            traceback.print_exc()
    
    def _save_gua(self, gua_data: Dict[str, Any]):
        """保存解析的卦象数据（使用全名作为键）"""
        gua_full_name = gua_data['name']
        
        # 提取主题标签
        core_spirit = gua_data.get('core_spirit', '')
        application = gua_data.get('application', '')
        gua_data['themes'] = self._extract_themes(core_spirit, application)
        
        # 建立单字索引（用于向后兼容）
        gua_key = gua_data.pop('_key', None)
        if gua_key:
            self.name_index[gua_key] = gua_full_name
        
        # 以全名为键存储
        self.gua_data[gua_full_name] = gua_data
    
    def _extract_themes(self, core_spirit: str, application: str) -> List[str]:
        """从核心精神和应用场景提取主题标签"""
        themes = []
        text = core_spirit + " " + application
        
        theme_keywords = {
            "事业": ["事业", "职业", "工作", "创业"],
            "领导力": ["领导", "管理", "治理"],
            "进取": ["进取", "前进", "发展", "成长"],
            "包容": ["包容", "接纳", "厚德", "承载"],
            "耐心": ["耐心", "等待", "时机"],
            "关系": ["关系", "人际", "家庭", "合作"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(kw in text for kw in keywords):
                themes.append(theme)
        
        return themes[:5]
    
    # ===== API Methods =====
    
    def get_gua(self, gua_name: str) -> Optional[Dict[str, Any]]:
        """
        根据卦名查询（支持全称和单字简称）
        
        Args:
            gua_name: 卦名，如"乾为天"、"乾"、"水天需"、"需"
        
        Returns:
            卦象数据字典，未找到返回 None
        """
        # 如果提供的是全名，直接返回
        if gua_name in self.gua_data:
            return self.gua_data[gua_name]
        
        # 如果提供的是单字，查索引
        if gua_name in self.name_index:
            full_name = self.name_index[gua_name]
            return self.gua_data.get(full_name)
        
        # 尝试模糊匹配（取第一个字符或最后一个字符）
        short_key = gua_name[0] if len(gua_name) > 1 else gua_name
        if short_key in self.name_index:
            full_name = self.name_index[short_key]
            return self.gua_data.get(full_name)
        
        return None
    
    def search_by_theme(self, theme: str) -> List[Dict[str, Any]]:
        """按主题搜索"""
        results = []
        for data in self.gua_data.values():
            text = (data.get('core_spirit', '') + ' ' + 
                   data.get('application', '') + ' ' + 
                   data.get('name', ''))
            if theme in text:
                results.append(data)
        return results
    
    def get_yao_ci(self, gua_name: str, yao_position: int) -> Optional[Dict[str, str]]:
        """查询爻辞"""
        gua = self.get_gua(gua_name)
        if not gua:
            return None
        return gua.get('yao_ci', {}).get(yao_position)
    
    def get_related_gua(self, gua_name: str, relation_type: str) -> Optional[str]:
        """查询卦象关系"""
        # 获取全名
        full_name = self.get_full_name(gua_name)
        if not full_name:
            return None
        
        relation_map = {
            "乾为天": {"错卦": "坤为地", "综卦": "乾为天", "互卦": "乾为天"},
            "坤为地": {"错卦": "乾为天", "综卦": "坤为地", "互卦": "坤为地"}
        }
        
        return relation_map.get(full_name, {}).get(relation_type)
    
    def get_full_name(self, gua_name: str) -> Optional[str]:
        """将单字简称转换为全名"""
        if gua_name in self.gua_data:
            return gua_name  # 已经是全名
        return self.name_index.get(gua_name)
    
    def list_all_gua(self) -> List[str]:
        """列出所有卦的全名"""
        return list(self.gua_data.keys())
    
    def list_all_keys(self) -> List[str]:
        """列出所有单字 key（向后兼容）"""
        return list(self.name_index.keys())
    
    def get_gua_count(self) -> int:
        """返回卦象数量"""
        return len(self.gua_data)

# ===== 测试代码 =====
if __name__ == "__main__":
    print("=" * 60)
    print("ZhouyiDatabase v4.0 测试（全名键）")
    print("=" * 60)
    
    db = ZhouyiDatabase()
    
    print(f"\n📊 已加载 {db.get_gua_count()} 个卦象\n")
    
    # Test 1: 查询乾卦（单字）
    print("📖 测试 1: 查询'乾'（单字简称）")
    qian = db.get_gua("乾")
    if qian:
        print(f"   ✓ 找到：{qian['name']} {qian['hexagram']}")
        print(f"   ✓ 卦辞：{qian['guaci']}")
        print(f"   ✓ 核心精神：{qian['core_spirit']}")
    
    # Test 2: 查询水天需（全称）
    print("\n📖 测试 2: 查询'水天需'（全称）")
    xu = db.get_gua("水天需")
    if xu:
        print(f"   ✓ 找到：{xu['name']} {xu['hexagram']}")
        print(f"   ✓ 卦辞：{xu['guaci']}")
    
    # Test 3: 查询水天需（简称）
    print("\n📖 测试 3: 查询'需'（简称）")
    xu_short = db.get_gua("需")
    if xu_short:
        print(f"   ✓ 找到：{xu_short['name']} {xu_short['hexagram']}")
    
    # Test 4: 主题搜索
    print("\n🔍 测试：搜索'事业'主题")
    results = db.search_by_theme("事业")
    print(f"   ✓ 找到 {len(results)} 个相关卦象")
    for g in results[:5]:
        print(f"     - {g['name']}: {g['core_spirit']}")
    
    # Test 5: 爻辞查询
    print("\n📜 测试：查询乾卦初九爻辞")
    yao = db.get_yao_ci("乾", 1)
    if yao:
        print(f"   ✓ 原文：{yao['original']}")
        print(f"   ✓ 白话：{yao['baihua']}")
    
    # Test 6: 列出所有卦（前 10）
    all_gua = db.list_all_gua()
    print(f"\n📚 已加载卦象列表（前 10 全名）:")
    for name in all_gua[:10]:
        data = db.gua_data[name]
        print(f"   - {name} {data['hexagram']}")
    
    print(f"\n   总计：{len(all_gua)} 个卦（无重复键！）")
    
    # Test 7: 检查单字索引
    print(f"\n📋 单字索引数量：{len(db.list_all_keys())}")
    
    print("\n" + "=" * 60)
    print("✅ ZhouyiDatabase v4.0 初始化完成！")
    print("=" * 60)
