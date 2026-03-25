#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中医体质自测题
基于《黄帝内经》理论的九种体质判断系统

使用方法：
python constitution-quiz.py
"""

import json

class ConstitutionQuiz:
    """体质自测题类"""
    
    # 九种体质及其特征描述
    CONSTITUTIONS = {
        "平和质": {
            "name": "平和质",
            "description": "健康平衡型",
            "features": [
                "体型匀称，面色红润",
                "精力充沛，睡眠良好",
                "食欲正常，大小便通畅"
            ],
            "neijing_basis": "形与神俱，阴阳平衡",
            "nurturing_focus": ["保持现有生活方式", "均衡饮食适度运动"]
        },
        "气虚质": {
            "name": "气虚质",
            "description": "能量不足型",
            "features": [
                "容易疲劳，少气懒言",
                "动则汗出，易感冒",
                "食欲不振，大便稀溏"
            ],
            "neijing_basis": "久卧伤气，脾为后天之本",
            "nurturing_focus": ["补气健脾", "适度运动避免过度劳累"]
        },
        "阳虚质": {
            "name": "阳虚质",
            "description": "阳气不足型",
            "features": [
                "畏寒肢冷，尤其腰膝",
                "精神不振，易疲劳",
                "食少腹胀，大便稀溏"
            ],
            "neijing_basis": "阳气者，若天与日",
            "nurturing_focus": ["温补阳气", "注意保暖尤其腰足"]
        },
        "阴虚质": {
            "name": "阴虚质",
            "description": "阴液不足型",
            "features": [
                "手足心热，午后潮热",
                "口燥咽干，喜冷饮",
                "失眠多梦，大便干燥"
            ],
            "neijing_basis": "阴虚则内热",
            "nurturing_focus": ["滋阴润燥", "避免辛辣刺激"]
        },
        "痰湿质": {
            "name": "痰湿质",
            "description": "湿浊内蕴型",
            "features": [
                "形体肥胖，腹部肥软",
                "面部油光，多汗黏腻",
                "口中黏腻，胸闷脘痞"
            ],
            "neijing_basis": "湿气通于脾",
            "nurturing_focus": ["健脾祛湿", "清淡饮食坚持运动"]
        },
        "湿热质": {
            "name": "湿热质",
            "description": "湿热内蕴型",
            "features": [
                "面部油光，易生痤疮",
                "口苦口臭，身体困重",
                "大便黏滞，小便短赤"
            ],
            "neijing_basis": "湿热不攘，大筋软短",
            "nurturing_focus": ["清热利湿", "保持环境干燥通风"]
        },
        "血瘀质": {
            "name": "血瘀质",
            "description": "血行不畅型",
            "features": [
                "面色晦暗，唇色紫暗",
                "皮肤粗糙，有瘀斑",
                "记忆力减退，易烦躁"
            ],
            "neijing_basis": "血气不和，百病乃生",
            "nurturing_focus": ["活血化瘀", "促进血液循环"]
        },
        "气郁质": {
            "name": "气郁质",
            "description": "气机郁滞型",
            "features": [
                "情绪低落，容易抑郁",
                "胸胁胀满，喜叹息",
                "睡眠差，食欲不振"
            ],
            "neijing_basis": "百病生于气也",
            "nurturing_focus": ["疏肝解郁", "保持心情舒畅"]
        },
        "特禀质": {
            "name": "特禀质",
            "description": "过敏体质型",
            "features": [
                "易过敏（花粉、食物）",
                "鼻塞流涕，皮肤瘙痒",
                "容易气喘，反复发作"
            ],
            "neijing_basis": "正气存内，邪不可干",
            "nurturing_focus": ["避免过敏原", "增强免疫力"]
        }
    }
    
    # 自测题目（每个体质对应的问题）
    QUESTIONS = [
        {
            "id": 1,
            "question": "你平时容易感到疲劳吗？",
            "options": [
                {"text": "经常感觉疲倦无力", "const": "气虚质", "weight": 3},
                {"text": "偶尔疲劳，休息后恢复", "const": "平和质", "weight": 1},
                {"text": "很少疲劳，精力充沛", "const": "平和质", "weight": 2}
            ]
        },
        {
            "id": 2,
            "question": "你对寒冷的耐受度如何？",
            "options": [
                {"text": "特别怕冷，手脚冰凉", "const": "阳虚质", "weight": 3},
                {"text": "比一般人怕冷", "const": "阳虚质", "weight": 2},
                {"text": "正常或偏耐热", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 3,
            "question": "你的睡眠质量如何？",
            "options": [
                {"text": "入睡困难或多梦易醒", "const": "阴虚质", "weight": 2},
                {"text": "睡眠差，难以深睡", "const": "气郁质", "weight": 2},
                {"text": "睡眠良好", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 4,
            "question": "你的体型和腹部特征？",
            "options": [
                {"text": "偏胖，腹部松软肥满", "const": "痰湿质", "weight": 3},
                {"text": "匀称或偏瘦", "const": "平和质", "weight": 1},
                {"text": "偏瘦但面色晦暗", "const": "血瘀质", "weight": 2}
            ]
        },
        {
            "id": 5,
            "question": "你的皮肤和面部状态？",
            "options": [
                {"text": "面部油光，易生痤疮", "const": "湿热质", "weight": 3},
                {"text": "面色晦暗，有瘀斑", "const": "血瘀质", "weight": 2},
                {"text": "皮肤干燥或有过敏史", "const": "特禀质", "weight": 2},
                {"text": "肤色红润，无明显异常", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 6,
            "question": "你的情绪状态？",
            "options": [
                {"text": "经常情绪低落、抑郁", "const": "气郁质", "weight": 3},
                {"text": "容易急躁、焦虑", "const": "阴虚质", "weight": 2},
                {"text": "心情平和稳定", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 7,
            "question": "你的出汗情况？",
            "options": [
                {"text": "轻微活动就大汗淋漓", "const": "气虚质", "weight": 2},
                {"text": "汗液黏腻或有异味", "const": "湿热质", "weight": 2},
                {"text": "出汗正常", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 8,
            "question": "你的食欲和消化情况？",
            "options": [
                {"text": "食欲不振，食后腹胀", "const": "气虚质", "weight": 2},
                {"text": "口苦口臭，大便黏滞", "const": "湿热质", "weight": 2},
                {"text": "食欲正常，消化良好", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 9,
            "question": "你是否容易过敏？",
            "options": [
                {"text": "经常过敏（鼻炎、皮疹等）", "const": "特禀质", "weight": 3},
                {"text": "偶尔过敏", "const": "特禀质", "weight": 2},
                {"text": "几乎不过敏", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 10,
            "question": "你的口腔和咽喉感觉？",
            "options": [
                {"text": "经常口干咽燥，喜冷饮", "const": "阴虚质", "weight": 3},
                {"text": "口苦口臭明显", "const": "湿热质", "weight": 2},
                {"text": "口中黏腻不爽", "const": "痰湿质", "weight": 2},
                {"text": "正常无不适", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 11,
            "question": "你的腰部和下肢感觉？",
            "options": [
                {"text": "经常腰膝酸软无力", "const": "阳虚质", "weight": 2},
                {"text": "腰部冷痛明显", "const": "阳虚质", "weight": 3},
                {"text": "无明显不适", "const": "平和质", "weight": 1}
            ]
        },
        {
            "id": 12,
            "question": "你的舌象特征（如了解）？",
            "options": [
                {"text": "舌淡胖有齿痕", "const": "气虚质", "weight": 3},
                {"text": "舌红少苔或无苔", "const": "阴虚质", "weight": 3},
                {"text": "舌苔黄腻", "const": "湿热质", "weight": 2},
                {"text": "舌紫暗或有瘀点", "const": "血瘀质", "weight": 2},
                {"text": "不清楚/正常", "const": "平和质", "weight": 1}
            ]
        }
    ]
    
    def __init__(self):
        self.user_answers = []
        self.constitution_scores = {}
        
    def add_answer(self, question_id, option_index):
        """
        记录用户答案
        :param question_id: 问题 ID
        :param option_index: 选项索引（0,1,2...）
        """
        # 找到对应问题和选项
        for q in self.QUESTIONS:
            if q["id"] == question_id:
                if option_index < len(q["options"]):
                    option = q["options"][option_index]
                    
                    # 累加该体质的分数
                    const_type = option["const"]
                    weight = option["weight"]
                    
                    if const_type not in self.constitution_scores:
                        self.constitution_scores[const_type] = 0
                    
                    self.constitution_scores[const_type] += weight
                    self.user_answers.append({
                        "question_id": question_id,
                        "option_index": option_index,
                        "option_text": option["text"],
                        "constitution": const_type,
                        "weight": weight
                    })
                break
    
    def get_result(self):
        """
        根据得分计算体质类型
        :return: dict containing result
        """
        if not self.constitution_scores:
            return {"error": "未回答问题，无法判断"}
        
        # 找出得分最高的前 3 种体质
        sorted_const = sorted(
            self.constitution_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        primary, score1 = sorted_const[0]
        secondary = sorted_const[1][0] if len(sorted_const) > 1 else None
        tertiary = sorted_const[2][0] if len(sorted_const) > 2 else None
        
        result = {
            "primary_constitution": primary,
            "secondary_constitution": secondary,
            "tertiary_constitution": tertiary,
            "score_breakdown": dict(sorted_const),
            "analysis": self._generate_analysis(primary, secondary, tertiary)
        }
        
        return result
    
    def _generate_analysis(self, primary, secondary, tertiary):
        """生成详细的体质分析报告"""
        primary_info = self.CONSTITUTIONS.get(primary, {})
        
        analysis = {
            "体质类型": f"{primary_info.get('name', primary)} - {primary_info.get('description', '待补充')}",
            "核心特征": primary_info.get("features", []),
            "内经依据": primary_info.get("neijing_basis", ""),
            "养生重点": primary_info.get("nurturing_focus", []),
        }
        
        if secondary:
            sec_info = self.CONSTITUTIONS.get(secondary, {})
            analysis["兼夹体质"] = {
                "类型": sec_info.get("name", secondary),
                "说明": f"同时具有{sec_info.get('description', '')}的特征"
            }
        
        return analysis

def main_interactive():
    """交互式自测模式"""
    print("=" * 60)
    print("🌿 《黄帝内经》体质自测系统".center(60))
    print("=" * 60)
    print()
    
    quiz = ConstitutionQuiz()
    
    for question in quiz.QUESTIONS:
        print(f"【问题{question['id']}】{question['question']}")
        print("-" * 40)
        
        # 显示选项
        for i, option in enumerate(question["options"]):
            print(f"  {i+1}. {option['text']}")
        
        # 获取用户输入
        while True:
            try:
                choice = int(input("请输入选项编号 (1-{}): ".format(len(question['options']))))
                if 1 <= choice <= len(question["options"]):
                    quiz.add_answer(question["id"], choice - 1)
                    break
                else:
                    print("❌ 请输入有效选项！")
            except ValueError:
                print("❌ 请输入数字！")
        
        print()
    
    # 显示结果
    result = quiz.get_result()
    
    if "error" in result:
        print(result["error"])
        return
    
    analysis = result["analysis"]
    
    print("=" * 60)
    print("📊 体质判断结果".center(60))
    print("=" * 60)
    print()
    print(f"主要体质：{analysis['体质类型']}")
    print()
    print("核心特征:")
    for feature in analysis["核心特征"]:
        print(f"  • {feature}")
    print()
    print(f"📜 《内经》依据：{analysis['内经依据']}")
    print()
    print("养生重点:")
    for focus in analysis["养生重点"]:
        print(f"  🌿 {focus}")
    
    if "兼夹体质" in analysis:
        print()
        print(f"次要体质：{analysis['兼夹体质']['类型']}")
        print(f"说明：{analysis['兼夹体质']['说明']}")
    
    print()
    print("⚠️ 注意：本结果仅供参考，具体诊断请咨询专业中医师。")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        main_interactive()
    else:
        # API 模式：输出使用说明
        print(json.dumps({
            "usage": "python constitution-quiz.py --interactive (启动交互模式)",
            "api_example": "导入 ConstitutionQuiz 类，调用 add_answer() 和 get_result()"
        }, ensure_ascii=False, indent=2))
