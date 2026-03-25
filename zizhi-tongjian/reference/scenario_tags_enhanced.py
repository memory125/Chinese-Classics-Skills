#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资治通鉴 - 智能推荐系统
实现：基于场景和用户偏好的个性化推荐
"""

import json
from typing import Dict, List, Optional
from datetime import datetime

class RecommendationEngine:
    """智能推荐系统"""
    
    def __init__(self):
        self.scenario_tags = self._load_scenario_tags()
        self.case_library = self._load_case_library()
        self.user_preferences = {}  # 简化：内存存储
        
        # 案例关联图谱
        self.case_relationships = self._load_case_relationships()
    
    def _load_scenario_tags(self) -> Dict:
        """增强版场景标签库"""
        return {
            "职场管理": {
                "向上管理": ["王翦灭楚求田问舍", "郭子仪交出兵权", "萧何自污保身", "李斯赵高关系"],
                "向下管理": ["曹操用人", "刘备三顾茅庐", "唐太宗纳谏", "朱元璋杀功臣"],
                "团队建设": ["光武中兴", "贞观之治", "汉初休养生息", "康乾盛世"],
                "裁员优化": ["商鞅变法", "王安石变法", "张居正改革", "戊戌变法"],
                "跳槽转行": ["张良择主", "陈平叛项归汉", "贾谊投湘", "魏征投唐"],
                "反内卷": ["范蠡功成身退", "张良学道", "陶渊明归隐", "李泌隐居"],
                "处理猜忌": ["韩安国自污", "萧何买地自污", "郭子仪开府门", "王翦请田"],
                "职场站队": ["王导平衡门阀", "曹操挟天子", "司马懿装病", "诸葛亮辅刘"],
                "领导力提升": ["刘邦用人", "刘备三顾", "曹操唯才是举", "李世民纳谏"],
            },
            "人际关系": {
                "团队冲突": ["鸿门和解", "将相和", "李世民玄武门后用人", "赤壁联盟"],
                "同事关系": ["蔺相如廉颇", "管仲鲍叔牙", "刘备关羽张飞", "苏轼苏辙"],
                "朋友借钱": ["季布一诺", "范式张劭", "管鲍分金", "范张鸡黍"],
                "婆媳关系": ["舜孝感动天", "王祥卧冰", "孟宗哭竹", "曾子杀猪"],
                "夫妻矛盾": ["司马相如卓文君", "汉武帝陈皇后", "曹操蔡文姬", "孙权小乔"],
                "家庭和睦": ["颜回安贫乐道", "孔融让梨", "黄香温席", "孟母三迁"],
            },
            "投资理财": {
                "大额投资": ["范蠡三聚三散", "吕不韦奇货可居", "石崇王恺斗富", "沈万三"],
                "股票止损": ["张良知止", "范蠡急流勇退", "文种不听劝", "萧何求田问舍"],
                "时机判断": ["高祖还乡", "孙权决断", "刘备取益州", "曹操赤壁"],
                "风险管理": ["韩信将兵", "李广难封", "赵括纸上谈兵", "马谡失街亭"],
                "价值投资": ["陶朱公致富", "子贡经商", "白圭治生", "吕不韦奇货"],
            },
            "感情婚姻": {
                "异地恋": ["司马相如卓文君", "苏武李陵", "柳毅传书", "牛郎织女"],
                "婚前犹豫": ["刘备孙尚香", "曹操蔡文姬", "孙权小乔", "李隆基杨玉环"],
                "婆媳关系": ["姜子牙马氏", "朱买臣崔氏", "宋弘老妻", "梁鸿孟光"],
                "离婚决策": ["孟光举案齐眉", "卓文君当垆", "苏轼朝云", "唐玄宗杨贵妃"],
                "信任重建": ["刘备托孤", "萧何自污", "郭子仪忠勇", "诸葛亮尽忠"],
            },
            "健康养生": {
                "坚持困难": ["王羲之练字", "匡衡凿壁", "孙康映雪", "车胤囊萤"],
                "手术决策": ["华佗治病", "张仲景行医", "孙思邈救人", "扁鹊见蔡桓公"],
                "心理疏导": ["庄子鼓盆", "颜回安贫", "苏轼豁达", "范仲淹岳阳楼"],
                "压力管理": ["陶渊明归隐", "王维隐居", "白居易知足", "苏轼赤壁赋"],
            },
            "学习规划": {
                "考研深造": ["匡衡读书", "车胤囊萤", "孙敬悬梁", "苏秦刺股"],
                "技能选择": ["张衡发明", "蔡伦造纸", "祖冲之算经", "毕昇活字印刷"],
                "时间管理": ["孔子学而不厌", "颜回勤学", "欧阳修三上", "司马光警枕"],
                "学习方法": ["曾国藩日课", "王阳明格物", "朱熹读书", "陆九渊语录"],
            },
            "历史对比": {
                "削藩策略": ["汉景帝削藩", "汉武帝推恩", "明太祖削藩", "雍正削藩"],
                "统一战争": ["秦始皇统一", "刘邦统一", "李世民统一", "朱元璋统一"],
                "帝王治国": ["刘邦治国", "李世民治国", "唐玄宗治国", "康熙治国"],
                "名臣对比": ["管仲 vs 商鞅", "萧何 vs 曹操", "诸葛亮 vs 王猛", "范蠡 vs 文种"],
                "失败教训": ["项羽失败", "袁绍失败", "苻坚失败", "崇祯失败"],
            }
        }
    
    def _load_case_library(self) -> Dict:
        """加载案例库（增强版，包含标签）"""
        return {
            "王翦灭楚求田问舍": {
                "出处": "卷六·秦纪二·秦始皇十二年",
                "原文": "王翦曰：'大王弗用臣之计，必以李信等为可任。'",
                "白话": "王翦要出征前，反复向秦始皇要田产宅院，看起来贪得无厌",
                "关键点": ["主动示弱", "消除猜忌", "求田问舍"],
                "适用场景": ["向上管理", "消除猜忌", "职场自保"],
                "现代应用": "适度展示小缺点，降低威胁感",
                "反思问题": "你是否因为太优秀而让人不安？",
                "关联案例": ["萧何自污保身", "郭子仪开府门"]
            },
            "萧何自污保身": {
                "出处": "卷十二·汉纪四·高祖十一年",
                "原文": "何乃多受贾竖财物，以自污。",
                "白话": "萧何故意强买民田、收受贿赂，败坏自己的名声",
                "关键点": ["自污名声", "降低威胁", "明哲保身"],
                "适用场景": ["向上管理", "消除猜忌", "职场自保"],
                "现代应用": "适当暴露无伤大雅的缺点，避免完美形象",
                "反思问题": "完美的你，是否让人不敢接近？",
                "关联案例": ["王翦灭楚求田问舍", "郭子仪开府门"]
            },
            "范蠡功成身退": {
                "出处": "《史记·越王勾践世家》",
                "原文": "范蠡遂去，自齐遗大夫种书。",
                "白话": "范蠡助越王复国后，立即离开，散尽家财",
                "关键点": ["急流勇退", "善始善终", "看透局势"],
                "适用场景": ["功成身退", "巅峰退出", "人生智慧"],
                "现代应用": "知道何时离开比知道何时进入更重要",
                "反思问题": "你是否知道何时该退出某个职位/项目？",
                "关联案例": ["张良学道", "陶渊明归隐"]
            },
            "韩信胯下之辱": {
                "出处": "《史记·淮阴侯列传》",
                "原文": "信孰视之，俯出胯下，蒲伏。",
                "白话": "韩信被小人挑衅，选择从胯下钻过，忍受屈辱",
                "关键点": ["忍辱负重", "大谋者不计较小节"],
                "适用场景": ["面对挑衅", "忍辱负重", "长远规划"],
                "现代应用": "为了更大的目标，可以暂时忍受不公",
                "反思问题": "你是否为了一时的面子而牺牲了未来？",
                "关联案例": ["勾践卧薪尝胆", "司马相如忍辱"]
            },
            "郭子仪开府门": {
                "出处": "卷二百二十三·唐纪三十九·广德二年",
                "原文": "子仪悉除壁垒，开门纳贼。",
                "白话": "郭子仪面对叛军，敞开家门，不修城墙",
                "关键点": ["坦诚相见", "以德服人", "消除猜忌"],
                "适用场景": ["信任危机", "消除猜忌", "以柔克刚"],
                "现代应用": "主动展示诚意，用信任换取信任",
                "反思问题": "你是否敢于主动示好，化解猜忌？",
                "关联案例": ["萧何自污", "王翦求田"]
            },
            "鸿门宴决策": {
                "出处": "卷十二·汉纪四·高祖元年",
                "原文": "范增数目项王，举所佩玉玦以示之者三。",
                "白话": "范增多次暗示项羽杀掉刘邦，项羽犹豫不决",
                "关键点": ["项羽犹豫", "刘邦脱险", "鸿门宴", "生死抉择"],
                "适用场景": ["实力悬殊", "生死决策", "示弱保命"],
                "现代应用": "实力不足时，示弱是最佳策略",
                "反思问题": "你是否在关键时刻因为犹豫而错失良机？",
                "关联案例": ["赤壁之战", "官渡之战"]
            },
            "推恩令决策": {
                "出处": "卷十八·汉纪十·元朔二年",
                "原文": "主父偃说上曰：'愿陛下令诸侯推恩分子弟，以地侯之。'",
                "白话": "主父偃建议汉武帝让诸侯王把封地分给所有子弟",
                "关键点": ["推恩令", "和平削藩", "温和策略", "政治智慧"],
                "适用场景": ["制度改革", "削藩策略", "渐进式变革"],
                "现代应用": "温和而持续的改革比激进改革更容易成功",
                "反思问题": "你的改革是激进还是渐进？",
                "关联案例": ["汉景帝削藩", "张居正改革"]
            },
            "曹操唯才是举": {
                "出处": "卷六十六·汉纪五十八·建安十五年",
                "原文": "夫有行之士，未必能进取；进取之士，未必能有行也。",
                "白话": "曹操发布求贤令，强调才能比品德更重要",
                "关键点": ["唯才是举", "用人不拘一格", "实用主义"],
                "适用场景": ["招聘人才", "团队建设", "打破偏见"],
                "现代应用": "招聘时重能力轻标签，避免错过真正的人才",
                "反思问题": "你是否因为表面原因拒绝了好的人才？",
                "关联案例": ["刘备三顾茅庐", "唐太宗纳谏"]
            }
        }
    
    def _load_case_relationships(self) -> Dict:
        """加载案例关联关系图谱"""
        return {
            "刘邦": {
                "相似人物": ["朱元璋", "光武帝刘秀", "唐高祖李渊"],
                "对比人物": ["项羽", "刘邦 - 项羽对比"],
                "事件链": ["鸿门宴", "约法三章", "楚汉战争", "建立汉朝"]
            },
            "项羽": {
                "相似人物": ["袁绍", "苻坚", "崇祯"],
                "对比人物": ["刘邦", "项羽 - 刘邦对比"],
                "事件链": ["起兵反秦", "巨鹿之战", "鸿门宴", "垓下之战", "乌江自刎"]
            }
        }
    
    def recommend_by_scenario(self, scenario: str) -> List[Dict]:
        """根据场景推荐案例"""
        recommendations = []
        
        for category, tags in self.scenario_tags.items():
            if scenario in tags:
                for tag, case_names in tags.items():
                    for name in case_names:
                        if name in self.case_library:
                            case = self.case_library[name]
                            recommendations.append({
                                "场景": f"{category} - {tag}",
                                "案例": name,
                                "相关性": "高",
                                "核心智慧": case["关键点"][0] if case["关键点"] else "无",
                                "现代应用": case.get("现代应用", "")
                            })
        
        # 去重
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec["案例"] not in seen:
                seen.add(rec["案例"])
                unique_recommendations.append(rec)
        
        return unique_recommendations[:5]
    
    def recommend_similar_cases(self, base_case: str, num_similar: int = 3) -> List[Dict]:
        """推荐相似案例"""
        if base_case not in self.case_library:
            return []
        
        base_case_data = self.case_library[base_case]
        base_keywords = set(base_case_data.get("关键点", []))
        
        candidates = []
        for name, case in self.case_library.items():
            if name == base_case:
                continue
            
            case_keywords = set(case.get("关键点", []))
            overlap = base_keywords & case_keywords
            if overlap:
                candidates.append({
                    "案例": name,
                    "相似度": len(overlap),
                    "共同点": list(overlap),
                    "核心智慧": case["关键点"][0] if case["关键点"] else "无",
                    "现代应用": case.get("现代应用", "")
                })
        
        # 按相似度排序
        candidates.sort(key=lambda x: x["相似度"], reverse=True)
        return candidates[:num_similar]
    
    def recommend_by_tags(self, tags: List[str]) -> List[Dict]:
        """根据标签组合推荐"""
        recommendations = []
        
        for category, tag_dict in self.scenario_tags.items():
            for tag, case_names in tag_dict.items():
                # 检查是否有匹配的标签
                matching_tags = [t for t in tags if t in tag]
                if matching_tags:
                    for name in case_names[:3]:  # 每个标签取前 3 个
                        if name in self.case_library:
                            case = self.case_library[name]
                            recommendations.append({
                                "场景": f"{category} - {tag}",
                                "匹配标签": matching_tags,
                                "案例": name,
                                "核心智慧": case["关键点"][0] if case["关键点"] else "无",
                                "适用场景": case.get("适用场景", [])
                            })
        
        # 去重并排序
        seen = set()
        unique = []
        for rec in recommendations:
            if rec["案例"] not in seen:
                seen.add(rec["案例"])
                unique.append(rec)
        
        # 按匹配标签数量排序
        unique.sort(key=lambda x: len(x.get("匹配标签", [])), reverse=True)
        return unique[:5]
    
    def get_personalized_recommendations(self, user_history: Optional[Dict] = None) -> List[Dict]:
        """基于用户历史个性化推荐"""
        if not user_history:
            user_history = {}
        
        # 推荐用户最近看过的案例的关联案例
        recent_cases = user_history.get("recent_cases", [])
        all_recommendations = []
        
        for case_name in recent_cases[:3]:  # 取最近 3 个
            similar = self.recommend_similar_cases(case_name, num_similar=2)
            all_recommendations.extend(similar)
        
        # 去重并返回
        seen = set()
        unique = []
        for rec in all_recommendations:
            if rec["案例"] not in seen:
                seen.add(rec["案例"])
                unique.append(rec)
        
        return unique[:5]
    
    def generate_daily_wisdom(self, user_preferences: Optional[Dict] = None) -> Dict:
        """生成今日锦囊，考虑用户偏好"""
        from scripts.daily_wisdom import DailyWisdom
        wisdom_engine = DailyWisdom()
        
        all_wisdoms = wisdom_engine.wisdoms
        
        # 如果用户有偏好，优先推荐相关领域的
        if user_preferences and "focus_areas" in user_preferences:
            focus = user_preferences["focus_areas"]
            for wisdom in all_wisdoms:
                if any(area in wisdom["适用场景"] for area in focus):
                    return wisdom
        
        # 随机推荐
        wisdom = wisdom_engine.get_random_wisdom()
        return wisdom


# 测试
if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    
    engine = RecommendationEngine()
    
    print("=" * 60)
    print("测试 1: 场景推荐 - 向上管理")
    print("=" * 60)
    recs = engine.recommend_by_scenario("向上管理")
    for rec in recs[:3]:
        print(f"案例：{rec['案例']}")
        print(f"核心智慧：{rec['核心智慧']}")
        print(f"现代应用：{rec['现代应用']}")
        print()
    
    print("=" * 60)
    print("测试 2: 相似案例推荐")
    print("=" * 60)
    similar = engine.recommend_similar_cases("王翦灭楚求田问舍")
    for rec in similar[:3]:
        print(f"案例：{rec['案例']}")
        print(f"相似度：{rec['相似度']}")
        print(f"共同点：{rec['共同点']}")
        print()
    
    print("=" * 60)
    print("测试 3: 标签组合推荐")
    print("=" * 60)
    tags_recs = engine.recommend_by_tags(["向上管理", "消除猜忌"])
    for rec in tags_recs[:3]:
        print(f"案例：{rec['案例']}")
        print(f"匹配标签：{rec['匹配标签']}")
        print()
