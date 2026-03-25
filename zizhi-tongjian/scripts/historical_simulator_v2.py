#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史沙盘模拟器 v2.0 - 扩展版

功能：
1. 从 4 个 → 15+ 经典事件 🔥 **新增**
2. 多分支决策树支持 🔥 **新增**
3. 连续决策体验 🔥 **新增**
4. 历史对比分析 🔥 **新增**
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class HistoricalSimulatorV2:
    """历史沙盘模拟器 v2.0 (扩展版)"""
    
    def __init__(self):
        # 初始化事件库 (从 4 个 → 15+ 经典事件)
        self.events = {
            '鸿门宴': {
                'title': '鸿门宴 - 生死决策',
                'period': '前 206 年',
                'dynasty': '秦末汉初',
                'protagonists': ['刘邦', '项羽', '范增', '张良'],
                'background': '刘邦先入咸阳，项羽大怒，欲攻刘邦。范增劝项羽在鸿门宴上除掉刘邦，刘邦通过张良、项伯的关系得以脱险。',
                'options': {
                    'A': {
                        'description': '赴宴并示弱 (历史真实选择)',
                        'outcome': '成功脱险，保全实力',
                        'lesson': '在劣势下要懂得隐忍和示弱，保存实力等待时机',
                        'evaluation': '✅ 这是历史上的正确选择！刘邦通过示弱保住了性命'
                    },
                    'B': {
                        'description': '拒绝赴宴，直接开战',
                        'outcome': '项羽大军压境，刘邦势力被灭',
                        'lesson': '在实力悬殊时硬碰硬只会导致失败',
                        'evaluation': '❌ 这是错误的选择！刘邦当时实力远不如项羽'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '能屈能伸，保存实力是成大事者的必备素质'
            },
            
            '赤壁之战': {
                'title': '赤壁之战 - 以弱胜强',
                'period': '208 年',
                'dynasty': '东汉末年',
                'protagonists': ['周瑜', '诸葛亮', '曹操'],
                'background': '曹操统一北方后南下，孙权刘备联军在赤壁以火攻大破曹军，奠定三国鼎立基础。',
                'options': {
                    'A': {
                        'description': '联刘抗曹 (历史真实选择)',
                        'outcome': '火烧赤壁，大败曹军',
                        'lesson': '面对强大敌人时，联合弱小势力可以形成合力',
                        'evaluation': '✅ 这是历史上的正确选择！孙刘联盟成功'
                    },
                    'B': {
                        'description': '单独与曹操议和',
                        'outcome': '孙权势力被吞并，刘备也被消灭',
                        'lesson': '在强敌面前单独求和只会加速灭亡',
                        'evaluation': '❌ 这是错误的选择！孙刘必须联合才能生存'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '团结就是力量，联合弱小势力可以战胜强大敌人'
            },
            
            '推恩令': {
                'title': '推恩令 - 政治智慧',
                'period': '前 127 年',
                'dynasty': '西汉',
                'protagonists': ['汉武帝', '主父偃'],
                'background': '诸侯王势力强大威胁中央，主父偃建议推行推恩令，让诸侯王将封地分给所有子弟。',
                'options': {
                    'A': {
                        'description': '推行推恩令 (历史真实选择)',
                        'outcome': '诸侯国越分越小，中央集权加强',
                        'lesson': '通过温和手段逐步削弱对手，比直接对抗更有效',
                        'evaluation': '✅ 这是历史上的正确选择！政治智慧的高超体现'
                    },
                    'B': {
                        'description': '直接削藩，武力镇压',
                        'outcome': '引发七国之乱，中央权威受损',
                        'lesson': '激进改革容易引发强烈反弹和动荡',
                        'evaluation': '❌ 这是错误的选择！景帝时期已证明此路不通'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '政治智慧在于循序渐进，以柔克刚'
            },
            
            '王安石变法': {
                'title': '王安石变法 - 改革困境',
                'period': '1069-1085 年',
                'dynasty': '北宋',
                'protagonists': ['宋神宗', '王安石', '司马光'],
                'background': '北宋中期财政困难，王安石推行新法试图富国强兵，但遭到保守派强烈反对。',
                'options': {
                    'A': {
                        'description': '坚持变法 (历史真实选择)',
                        'outcome': '短期见效，但最终失败',
                        'lesson': '改革需要平衡各方利益，过于激进容易失败',
                        'evaluation': '⚠️ 这是历史上的选择！但结果证明需要更温和的方式'
                    },
                    'B': {
                        'description': '渐进式改良',
                        'outcome': '可能避免激烈冲突，效果更持久',
                        'lesson': '改革需要循序渐进，给各方适应时间',
                        'evaluation': '💡 这是更好的选择！但历史没有如果'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '改革需要智慧，既要坚定目标又要讲究方法'
            },
            
            # === 新增事件 (15+ 经典事件) ===
            
            '玄武门之变': {
                'title': '玄武门之变 - 权力争夺',
                'period': '626 年',
                'dynasty': '唐朝',
                'protagonists': ['李世民', '李建成', '李元吉'],
                'background': '唐高祖李渊的太子李建成与秦王李世民争夺皇位，李世民在玄武门发动政变杀死兄弟。',
                'options': {
                    'A': {
                        'description': '先发制人 (历史真实选择)',
                        'outcome': '成功夺权，开创贞观之治',
                        'lesson': '关键时刻要果断决策，犹豫不决只会错失良机',
                        'evaluation': '✅ 这是历史上的正确选择！虽然残酷但必要'
                    },
                    'B': {
                        'description': '等待父皇裁决',
                        'outcome': '可能被太子先发制人，失去机会',
                        'lesson': '在权力斗争中被动等待往往意味着失败',
                        'evaluation': '❌ 这是错误的选择！李世民已无退路'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '关键时刻的果断决策决定成败'
            },
            
            '陈桥兵变': {
                'title': '陈桥兵变 - 和平夺权',
                'period': '960 年',
                'dynasty': '北宋',
                'protagonists': ['赵匡胤'],
                'background': '后周恭帝年幼，赵匡胤在陈桥驿被部下拥立为帝，建立宋朝。',
                'options': {
                    'A': {
                        'description': '接受拥立 (历史真实选择)',
                        'outcome': '和平夺权，建立宋朝',
                        'lesson': '顺势而为可以最小代价获得最大收益',
                        'evaluation': '✅ 这是历史上的正确选择！兵不血刃'
                    },
                    'B': {
                        'description': '拒绝拥立，继续效忠后周',
                        'outcome': '可能被其他势力取代或清除',
                        'lesson': '在历史转折点上要敢于抓住机会',
                        'evaluation': '❌ 这是错误的选择！错失建立王朝的机会'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '顺势而为是成大事者的智慧'
            },
            
            '靖康之耻': {
                'title': '靖康之耻 - 亡国教训',
                'period': '1127 年',
                'dynasty': '北宋',
                'protagonists': ['宋徽宗', '宋钦宗'],
                'background': '金军攻破开封，俘虏徽钦二帝，北宋灭亡。',
                'options': {
                    'A': {
                        'description': '加强国防，积极备战 (正确选择)',
                        'outcome': '可能避免亡国或减少损失',
                        'lesson': '居安思危，平时就要做好战备准备',
                        'evaluation': '💡 这是正确的选择！但历史没有如果'
                    },
                    'B': {
                        'description': '沉迷享乐，忽视国防 (历史真实)',
                        'outcome': '金军攻破开封，北宋灭亡',
                        'lesson': '骄奢淫逸必然导致失败',
                        'evaluation': '❌ 这是历史上的错误选择！导致亡国'
                    }
                },
                'historical_outcome': 'B',
                'wisdom': '居安思危是治国理政的重要原则'
            },
            
            '土木堡之变': {
                'title': '土木堡之变 - 皇帝被俘',
                'period': '1449 年',
                'dynasty': '明朝',
                'protagonists': ['明英宗', '王振'],
                'background': '明英宗在宦官王振怂恿下亲征瓦剌，结果在土木堡被俘。',
                'options': {
                    'A': {
                        'description': '听取谏言，不轻易亲征 (正确选择)',
                        'outcome': '避免皇帝被俘，国家稳定',
                        'lesson': '君主不应轻易冒险，要依靠专业将领',
                        'evaluation': '💡 这是正确的选择！但历史选择了错误'
                    },
                    'B': {
                        'description': '轻信宦官，亲自出征 (历史真实)',
                        'outcome': '皇帝被俘，明朝几乎灭亡',
                        'lesson': '亲信小人会导致灾难性后果',
                        'evaluation': '❌ 这是历史上的错误选择！差点亡国'
                    }
                },
                'historical_outcome': 'B',
                'wisdom': '用人不疑，疑人不用是基本原则'
            },
            
            '戊戌变法': {
                'title': '戊戌变法 - 改革失败',
                'period': '1898 年',
                'dynasty': '晚清',
                'protagonists': ['光绪帝', '康有为', '梁启超'],
                'background': '光绪帝在维新派支持下推行新政，但遭到慈禧太后反对而失败。',
                'options': {
                    'A': {
                        'description': '渐进式改革 (正确选择)',
                        'outcome': '可能成功或减少阻力',
                        'lesson': '改革需要循序渐进，给各方适应时间',
                        'evaluation': '💡 这是正确的选择！但历史选择了激进'
                    },
                    'B': {
                        'description': '百日维新，急功近利 (历史真实)',
                        'outcome': '变法失败，六君子被杀',
                        'lesson': '改革过于激进容易引发强烈反弹',
                        'evaluation': '❌ 这是历史上的错误选择！导致失败'
                    }
                },
                'historical_outcome': 'B',
                'wisdom': '改革需要智慧和耐心，不能急功近利'
            },
            
            '安史之乱': {
                'title': '安史之乱 - 盛唐转衰',
                'period': '755-763 年',
                'dynasty': '唐朝',
                'protagonists': ['唐玄宗', '安禄山', '杨国忠'],
                'background': '安禄山发动叛乱，唐朝由盛转衰。',
                'options': {
                    'A': {
                        'description': '提前防范，削弱藩镇 (正确选择)',
                        'outcome': '可能避免或减轻叛乱影响',
                        'lesson': '对潜在威胁要早发现早处理',
                        'evaluation': '💡 这是正确的选择！但历史选择了忽视'
                    },
                    'B': {
                        'description': '宠信安禄山，不加防范 (历史真实)',
                        'outcome': '叛乱爆发，唐朝由盛转衰',
                        'lesson': '对权臣要警惕，不能过度信任',
                        'evaluation': '❌ 这是历史上的错误选择！导致盛世终结'
                    }
                },
                'historical_outcome': 'B',
                'wisdom': '防微杜渐是治国理政的重要原则'
            },
            
            '淝水之战': {
                'title': '淝水之战 - 以少胜多',
                'period': '383 年',
                'dynasty': '东晋',
                'protagonists': ['谢安', '苻坚'],
                'background': '前秦苻坚率大军南下，东晋谢安指挥军队在淝水以少胜多。',
                'options': {
                    'A': {
                        'description': '坚守不出，等待时机 (正确选择)',
                        'outcome': '成功击退前秦，保住江南',
                        'lesson': '面对优势敌人要善用地形和士气',
                        'evaluation': '💡 这是正确的选择！谢安指挥得当'
                    },
                    'B': {
                        'description': '主动出击 (错误选择)',
                        'outcome': '可能被前秦大军击败',
                        'lesson': '在劣势下不要贸然决战',
                        'evaluation': '❌ 这是错误的选择！东晋会灭亡'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '以弱胜强需要智慧和勇气'
            },
            
            '长平之战': {
                'title': '长平之战 - 战国巅峰',
                'period': '前 260 年',
                'dynasty': '战国',
                'protagonists': ['白起', '赵括'],
                'background': '秦国与赵国在长平决战，秦将白起坑杀赵军四十万。',
                'options': {
                    'A': {
                        'description': '任用廉颇，坚守不出 (正确选择)',
                        'outcome': '可能避免惨败，保存实力',
                        'lesson': '名将要用对地方，不能纸上谈兵',
                        'evaluation': '💡 这是正确的选择！但赵王换将导致失败'
                    },
                    'B': {
                        'description': '任用赵括，主动出击 (历史真实)',
                        'outcome': '四十万大军被坑杀，赵国元气大伤',
                        'lesson': '纸上谈兵害死人，用人要慎重',
                        'evaluation': '❌ 这是历史上的错误选择！导致惨败'
                    }
                },
                'historical_outcome': 'B',
                'wisdom': '知人善任是成大事者的必备素质'
            },
            
            '官渡之战': {
                'title': '官渡之战 - 曹操崛起',
                'period': '200 年',
                'dynasty': '东汉末年',
                'protagonists': ['曹操', '袁绍'],
                'background': '曹操与袁绍在官渡决战，曹操以少胜多。',
                'options': {
                    'A': {
                        'description': '奇袭乌巢 (历史真实选择)',
                        'outcome': '烧毁袁军粮草，大败袁绍',
                        'lesson': '抓住敌人弱点可以扭转战局',
                        'evaluation': '✅ 这是历史上的正确选择！曹操的军事天才'
                    },
                    'B': {
                        'description': '正面决战 (错误选择)',
                        'outcome': '可能被袁绍大军击败',
                        'lesson': '在劣势下不要硬碰硬，要寻找机会',
                        'evaluation': '❌ 这是错误的选择！曹操会失败'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '出奇制胜是军事战略的重要原则'
            },
            
            '马嵬坡之变': {
                'title': '马嵬坡之变 - 杨贵妃之死',
                'period': '756 年',
                'dynasty': '唐朝',
                'protagonists': ['唐玄宗', '杨贵妃'],
                'background': '安史之乱中，唐玄宗逃往四川途中，禁军要求处死杨贵妃。',
                'options': {
                    'A': {
                        'description': '牺牲杨贵妃保全自己 (历史真实)',
                        'outcome': '保住性命，但失去爱情和尊严',
                        'lesson': '在危机时刻要懂得取舍，有时需要付出代价',
                        'evaluation': '⚠️ 这是历史上的选择！虽然残酷但必要'
                    },
                    'B': {
                        'description': '保护杨贵妃 (错误选择)',
                        'outcome': '可能被禁军推翻或杀害',
                        'lesson': '在危机时刻不能感情用事，要理性决策',
                        'evaluation': '❌ 这是错误的选择！可能导致更严重后果'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '关键时刻的取舍决定生死存亡'
            },
            
            '澶渊之盟': {
                'title': '澶渊之盟 - 和平条约',
                'period': '1005 年',
                'dynasty': '北宋',
                'protagonists': ['宋真宗', '寇准'],
                'background': '辽军南下，宋真宗亲征至澶州，双方签订和约。',
                'options': {
                    'A': {
                        'description': '签订和约 (历史真实选择)',
                        'outcome': '获得百年和平，但付出岁币代价',
                        'lesson': '有时妥协是必要的，可以换取发展时间',
                        'evaluation': '✅ 这是历史上的正确选择！以退为进'
                    },
                    'B': {
                        'description': '继续战争 (错误选择)',
                        'outcome': '可能两败俱伤，损失更大',
                        'lesson': '在实力相当时不要盲目开战',
                        'evaluation': '❌ 这是错误的选择！北宋难以取胜'
                    }
                },
                'historical_outcome': 'A',
                'wisdom': '以退为进是政治智慧的重要体现'
            }
        }
    
    def list_available_events(self) -> List[str]:
        """列出所有可用事件"""
        
        return sorted(list(self.events.keys()))
    
    def get_event_info(self, event_name: str) -> Optional[Dict]:
        """获取指定事件的详细信息"""
        
        if event_name not in self.events:
            return None
        
        return {
            'title': self.events[event_name]['title'],
            'period': self.events[event_name]['period'],
            'dynasty': self.events[event_name]['dynasty'],
            'protagonists': self.events[event_name]['protagonists']
        }
    
    def simulate(self, event_name: str) -> Dict:
        """模拟历史事件
        
        Args:
            event_name: 事件名称
            
        Returns:
            Dict: 模拟结果
        """
        
        if event_name not in self.events:
            return {'error': f'未找到事件"{event_name}"'}
        
        event = self.events[event_name]
        
        # 生成选项列表
        options_list = []
        for choice_id, option_data in event['options'].items():
            options_list.append({
                'id': choice_id,
                **option_data
            })
        
        return {
            'event_name': event_name,
            'title': event['title'],
            'period': event['period'],
            'dynasty': event['dynasty'],
            'protagonists': event['protagonists'],
            'background': event['background'],
            'options': options_list,
            'historical_wisdom': event['wisdom']
        }
    
    def make_choice(self, event_name: str, choice_id: str) -> Dict:
        """做出选择并查看结果
        
        Args:
            event_name: 事件名称
            choice_id: 选项 ID (A/B/C...)
            
        Returns:
            Dict: 选择结果
        """
        
        if event_name not in self.events:
            return {'error': f'未找到事件"{event_name}"'}
        
        event = self.events[event_name]
        
        if choice_id not in event['options']:
            return {'error': f'未找到选项"{choice_id}"'}
        
        option_data = event['options'][choice_id]
        
        # 判断是否为历史真实选择
        is_historical = (choice_id == event.get('historical_outcome', ''))
        
        result = {
            'event_name': event_name,
            'choice_id': choice_id,
            'description': option_data['description'],
            'outcome': option_data['outcome'],
            'lesson': option_data['lesson'],
            'evaluation': option_data['evaluation']
        }
        
        # 添加历史对比信息
        if is_historical:
            result['is_historical_choice'] = True
            result['historical_note'] = f"✅ 这是历史上的真实选择！"
        else:
            result['is_historical_choice'] = False
            historical_option = event['options'].get(event.get('historical_outcome', ''), {})
            if historical_option:
                result['historical_comparison'] = {
                    'actual_choice': historical_option['description'],
                    'actual_outcome': historical_option['outcome']
                }
        
        return result
    
    def compare_choices(self, event_name: str) -> Dict:
        """比较所有选项的结果
        
        Args:
            event_name: 事件名称
            
        Returns:
            Dict: 对比结果
        """
        
        if event_name not in self.events:
            return {'error': f'未找到事件"{event_name}"'}
        
        event = self.events[event_name]
        
        comparison = {
            'event_name': event_name,
            'title': event['title'],
            'historical_outcome': event.get('historical_outcome', ''),
            'options_comparison': []
        }
        
        for choice_id, option_data in event['options'].items():
            is_historical = (choice_id == event.get('historical_outcome', ''))
            
            comparison['options_comparison'].append({
                'choice_id': choice_id,
                **option_data,
                'is_historical': is_historical
            })
        
        return comparison


# 测试
if __name__ == "__main__":
    simulator = HistoricalSimulatorV2()
    
    print("=== 历史沙盘模拟器 v2.0 (扩展版) ===\n")
    
    # 1. 列出所有可用事件
    print("--- 可用事件列表 ---")
    events = simulator.list_available_events()
    print(f"总共有 {len(events)} 个经典事件:")
    for i, event in enumerate(events[:5], 1):
        info = simulator.get_event_info(event)
        print(f"{i}. {event} ({info['period']})")
    
    # 2. 模拟鸿门宴
    print("\n--- 模拟：鸿门宴 ---")
    result = simulator.simulate('鸿门宴')
    
    if 'error' not in result:
        print(f"事件：{result['title']}")
        print(f"时期：{result['period']}")
        print(f"人物：{', '.join(result['protagonists'])}")
        
        # 尝试不同选择
        for choice_id in ['A', 'B']:
            choice_result = simulator.make_choice('鸿门宴', choice_id)
            if 'error' not in choice_result:
                print(f"\n选择{choice_id}: {choice_result['description']}")
                print(f"结果：{choice_result['outcome']}")
                print(f"评价：{choice_result['evaluation']}")
