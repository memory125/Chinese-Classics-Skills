#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史沙盘模拟器 - 为 RAG 系统提供互动式历史体验

功能：
1. 关键事件数据库 (鸿门宴、赤壁之战等)
2. 决策树生成器 (不同选择→不同结果)
3. 结果评估系统 (基于历史事实)
4. 互动界面 (CLI/Web API)
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime


class HistoricalSimulator:
    """历史沙盘模拟器"""
    
    def __init__(self):
        # 关键事件数据库 (可扩展)
        self.events = {
            '鸿门宴': {
                'title': '鸿门宴 - 生死决策',
                'background': '公元前 206 年，刘邦命悬一线。项羽率四十万大军驻扎鸿门，准备攻打刘邦的十万军队。范增劝项羽趁机除掉刘邦，但项羽犹豫不决。',
                'options': [
                    {
                        'id': 'A',
                        'description': '立即前往鸿门，亲自谢罪，放低姿态',
                        'historical_choice': True,
                        'outcome': '成功脱险',
                        'lesson': '示弱可以暂时消除对手戒心，保存实力等待时机',
                        'consequences': {
                            'short_term': '刘邦保住性命，项羽放松警惕',
                            'long_term': '为楚汉争霸争取了宝贵时间'
                        }
                    },
                    {
                        'id': 'B', 
                        'description': '坚守关中，按兵不动',
                        'historical_choice': False,
                        'outcome': '大概率被围攻，全军覆没',
                        'lesson': '实力悬殊时硬拼=自杀，需要战略退让',
                        'consequences': {
                            'short_term': '项羽立即进攻，刘邦军队可能被歼灭',
                            'long_term': '汉朝无法建立'
                        }
                    },
                    {
                        'id': 'C',
                        'description': '夜袭项羽大营',
                        'historical_choice': False,
                        'outcome': '失败率 90%',
                        'lesson': '冒险需要绝对把握，否则就是送死',
                        'consequences': {
                            'short_term': '夜袭失败，刘邦军队损失惨重',
                            'long_term': '项羽彻底消灭刘邦势力'
                        }
                    },
                    {
                        'id': 'D',
                        'description': '求和谈判，割让部分土地',
                        'historical_choice': False,
                        'outcome': '可能成功，但失去民心',
                        'lesson': '妥协可以换取时间，但要付出代价',
                        'consequences': {
                            'short_term': '项羽接受条件，刘邦暂时安全',
                            'long_term': '刘邦失去关中根据地，难以发展'
                        }
                    }
                ],
                'historical_outcome': '刘邦采纳张良建议，亲自前往鸿门谢罪，成功脱险。项羽因优柔寡断放走刘邦，最终在楚汉争霸中失败。',
                'key_figures': ['刘邦', '项羽', '张良', '范增', '樊哙'],
                'modern_applications': [
                    '职场危机处理：面对强势上司的质疑，先示弱再找机会解释',
                    '商业谈判：实力不足时避免正面冲突，寻找合作机会',
                    '人生决策：关键时刻要懂得退让，保存实力'
                ]
            },
            
            '赤壁之战': {
                'title': '赤壁之战 - 以弱胜强',
                'background': '公元 208 年，曹操统一北方后率八十万大军南下，意图一举消灭孙刘联军。刘备败退至夏口，与孙权结盟共同抗曹。',
                'options': [
                    {
                        'id': 'A',
                        'description': '联合孙权，火攻曹军',
                        'historical_choice': True,
                        'outcome': '大获全胜',
                        'lesson': '利用对手弱点 (不习水战、瘟疫流行)，发挥己方优势 (水军)',
                        'consequences': {
                            'short_term': '曹操败退北方，孙刘联军控制长江中游',
                            'long_term': '形成三国鼎立局面'
                        }
                    },
                    {
                        'id': 'B', 
                        'description': '单独与曹操议和',
                        'historical_choice': False,
                        'outcome': '被各个击破',
                        'lesson': '面对强敌时，团结比妥协更重要',
                        'consequences': {
                            'short_term': '孙权或刘备单独投降，暂时保全',
                            'long_term': '曹操统一全国，三国无法形成'
                        }
                    },
                    {
                        'id': 'C',
                        'description': '放弃抵抗，南逃交州',
                        'historical_choice': False,
                        'outcome': '失去根据地',
                        'lesson': '逃跑不能解决问题，必须正面应对挑战',
                        'consequences': {
                            'short_term': '暂时保全性命',
                            'long_term': '彻底失去政治影响力'
                        }
                    },
                    {
                        'id': 'D',
                        'description': '主动进攻曹操大营',
                        'historical_choice': False,
                        'outcome': '惨败',
                        'lesson': '实力悬殊时不要硬拼，需要智取而非力敌',
                        'consequences': {
                            'short_term': '孙刘联军损失惨重',
                            'long_term': '曹操乘胜追击，统一全国'
                        }
                    }
                ],
                'historical_outcome': '周瑜采用黄盖诈降计，火攻曹军连环船，大败曹操。此战奠定了三国鼎立的基础，是中国历史上著名的以弱胜强战役。',
                'key_figures': ['周瑜', '诸葛亮', '鲁肃', '曹操', '黄盖'],
                'modern_applications': [
                    '创业竞争：小公司避开巨头优势领域，寻找细分市场突破',
                    '团队管理：发挥团队成员特长，形成互补优势',
                    '危机处理：利用对手弱点，制定针对性策略'
                ]
            },
            
            '推恩令': {
                'title': '推恩令 - 和平削藩',
                'background': '汉武帝时期，诸侯王势力强大，威胁中央集权。汉景帝曾尝试强制削藩，引发七国之乱。汉武帝采纳主父偃建议，推行推恩令。',
                'options': [
                    {
                        'id': 'A',
                        'description': '推行推恩令，允许诸侯王分封子弟为侯',
                        'historical_choice': True,
                        'outcome': '成功削藩',
                        'lesson': '用"恩赐"的名义逐步削弱对手，避免正面冲突',
                        'consequences': {
                            'short_term': '诸侯国越分越小，无力对抗中央',
                            'long_term': '中央集权加强，汉朝稳定发展'
                        }
                    },
                    {
                        'id': 'B', 
                        'description': '强制削藩，剥夺诸侯王权力',
                        'historical_choice': False,
                        'outcome': '引发叛乱',
                        'lesson': '强硬手段容易激起反抗，需要策略性处理',
                        'consequences': {
                            'short_term': '诸侯王联合反叛 (如七国之乱)',
                            'long_term': '中央政权可能崩溃'
                        }
                    },
                    {
                        'id': 'C',
                        'description': '维持现状，不采取任何措施',
                        'historical_choice': False,
                        'outcome': '诸侯势力继续膨胀',
                        'lesson': '问题不会自动消失，必须主动解决',
                        'consequences': {
                            'short_term': '表面和平',
                            'long_term': '中央权威被架空，可能分裂'
                        }
                    },
                    {
                        'id': 'D',
                        'description': '拉拢部分诸侯王，打击其他诸侯',
                        'historical_choice': False,
                        'outcome': '效果有限',
                        'lesson': '分化瓦解需要配合实质性措施才能见效',
                        'consequences': {
                            'short_term': '部分诸侯倒向中央',
                            'long_term': '问题依然存在，只是推迟爆发'
                        }
                    }
                ],
                'historical_outcome': '推恩令成功实施，诸侯国越分越小，无力对抗中央。汉武帝实现了和平削藩，加强了中央集权，为汉朝鼎盛时期奠定基础。',
                'key_figures': ['汉武帝', '主父偃', '诸侯王'],
                'modern_applications': [
                    '企业管理：通过股权激励逐步稀释大股东控制权',
                    '组织变革：用温和方式推进改革，减少阻力',
                    '政治智慧：给对手"台阶下"，实现双赢'
                ]
            },
            
            '王安石变法': {
                'title': '王安石变法 - 改革困境',
                'background': '北宋中期，财政困难、军队疲弱。宋神宗任用王安石推行变法，试图富国强兵。但变法遭遇强烈反对，最终失败。',
                'options': [
                    {
                        'id': 'A',
                        'description': '稳步推进，争取更多支持',
                        'historical_choice': False,  # 历史实际是激进改革
                        'outcome': '可能成功',
                        'lesson': '改革需要循序渐进，建立广泛联盟',
                        'consequences': {
                            'short_term': '阻力减小，政策更容易推行',
                            'long_term': '变法成功，北宋中兴'
                        }
                    },
                    {
                        'id': 'B', 
                        'description': '激进改革，快速推进',
                        'historical_choice': True,  # 历史实际做法
                        'outcome': '遭遇强烈反对，最终失败',
                        'lesson': '改革过快容易激起反弹，需要平衡各方利益',
                        'consequences': {
                            'short_term': '短期内看到成效',
                            'long_term': '新旧势力激烈冲突，改革夭折'
                        }
                    },
                    {
                        'id': 'C',
                        'description': '放弃变法，维持现状',
                        'historical_choice': False,
                        'outcome': '问题继续恶化',
                        'lesson': '不改革等于慢性自杀，必须面对挑战',
                        'consequences': {
                            'short_term': '表面稳定',
                            'long_term': '北宋逐渐衰落，最终灭亡'
                        }
                    },
                    {
                        'id': 'D',
                        'description': '部分改革，妥协折中',
                        'historical_choice': False,
                        'outcome': '效果有限',
                        'lesson': '改革需要系统性思维，零敲碎打难以奏效',
                        'consequences': {
                            'short_term': '各方都能接受',
                            'long_term': '核心问题未解决，改革流于形式'
                        }
                    }
                ],
                'historical_outcome': '王安石变法因遭遇保守派强烈反对而失败。虽然部分措施被保留，但整体未能实现富国强兵的目标。北宋最终在内外交困中灭亡。',
                'key_figures': ['王安石', '宋神宗', '司马光', '苏轼'],
                'modern_applications': [
                    '企业转型：改革需要平衡创新与稳定，避免激进',
                    '政策制定：考虑各方利益，建立支持联盟',
                    '领导力：改革者需要具备政治智慧和耐心'
                ]
            }
        }
    
    def simulate(self, event_name: str) -> Dict:
        """模拟历史事件"""
        
        if event_name not in self.events:
            return {
                'error': f'未找到事件"{event_name}"',
                'available_events': list(self.events.keys())
            }
        
        event = self.events[event_name]
        
        return {
            'event': event_name,
            'title': event['title'],
            'background': event['background'],
            'options': event['options'],
            'historical_outcome': event['historical_outcome'],
            'key_figures': event.get('key_figures', []),
            'modern_applications': event.get('modern_applications', [])
        }
    
    def make_choice(self, event_name: str, choice_id: str) -> Dict:
        """做出选择并查看结果"""
        
        if event_name not in self.events:
            return {'error': f'未找到事件"{event_name}"'}
        
        event = self.events[event_name]
        
        # 查找选择的详细信息
        selected_option = None
        for option in event['options']:
            if option['id'] == choice_id:
                selected_option = option
                break
        
        if not selected_option:
            return {'error': f'未找到选项"{choice_id}"'}
        
        # 判断是否是历史真实选择
        is_historical = selected_option.get('historical_choice', False)
        
        result = {
            'event': event_name,
            'choice': choice_id,
            'description': selected_option['description'],
            'outcome': selected_option['outcome'],
            'lesson': selected_option['lesson'],
            'consequences': selected_option.get('consequences', {}),
            'is_historical_choice': is_historical,
            'historical_outcome': event['historical_outcome'] if not is_historical else None
        }
        
        # 如果是历史真实选择，给出正面评价
        if is_historical:
            result['evaluation'] = '✅ 这是历史上的正确选择！'
        else:
            result['evaluation'] = f'⚠️ 这不是历史真实选择。历史上选择了：{event["historical_outcome"][:50]}...'
        
        return result
    
    def list_available_events(self) -> List[str]:
        """列出所有可用事件"""
        return list(self.events.keys())


# 测试
if __name__ == "__main__":
    simulator = HistoricalSimulator()
    
    # 测试：列出可用事件
    print("=== 可用历史事件 ===")
    events = simulator.list_available_events()
    for i, event in enumerate(events[:3], 1):
        print(f"{i}. {event}")
    
    # 测试：模拟鸿门宴
    print("\n=== 鸿门宴模拟 ===")
    result = simulator.simulate('鸿门宴')
    
    if 'error' not in result:
        print(f"事件：{result['title']}")
        print(f"\n背景:")
        print(result['background'])
        
        print("\n选项:")
        for option in result['options'][:3]:
            print(f"{option['id']}. {option['description']}")
    
    # 测试：做出选择
    print("\n=== 选择 A: 前往鸿门谢罪 ===")
    choice_result = simulator.make_choice('鸿门宴', 'A')
    
    if 'error' not in choice_result:
        print(f"结果：{choice_result['outcome']}")
        print(f"教训：{choice_result['lesson']}")
        print(f"评价：{choice_result['evaluation']}")
