#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易学习练习测验系统 v1.0
包含八卦识别、卦名记忆、爻辞理解、解卦练习等多种练习

版本：v1.0 (2026-03-25)
"""

import random
import json
from datetime import date

class ZhouyiExercise:
    """周易练习测验系统"""
    
    def __init__(self):
        self.score = 0
        self.total = 0
        self.results = []
        
        # 八卦数据
        self.bagua = {
            "乾": {"symbol": "☰", "element": "天", "binary": "111", "nature": "刚健"},
            "坤": {"symbol": "☷", "element": "地", "binary": "000", "nature": "柔顺"},
            "震": {"symbol": "☳", "element": "雷", "binary": "100", "nature": "动"},
            "巽": {"symbol": "☴", "element": "风", "binary": "110", "nature": "入"},
            "坎": {"symbol": "☵", "element": "水", "binary": "010", "nature": "陷"},
            "离": {"symbol": "☲", "element": "火", "binary": "101", "nature": "丽"},
            "艮": {"symbol": "☶", "element": "山", "binary": "001", "nature": "止"},
            "兑": {"symbol": "☱", "element": "泽", "binary": "011", "nature": "悦"},
        }
        
        # 六十四卦基础数据（部分）
        self.hexagrams = {
            "乾": {"symbol": "䷀", "phrase": "元亨利贞", "theme": "自强不息"},
            "坤": {"symbol": "䷁", "phrase": "厚德载物", "theme": "顺势而为"},
            "屯": {"symbol": "䷂", "phrase": "元亨利贞，勿用有攸往", "theme": "艰难创业"},
            "蒙": {"symbol": "䷃", "phrase": "亨，匪我求童蒙", "theme": "启蒙求知"},
            "需": {"symbol": "䷄", "phrase": "有孚，光亨贞吉", "theme": "耐心等待"},
            "讼": {"symbol": "䷅", "phrase": "有孚窒惕，中吉终凶", "theme": "慎始敬终"},
            "师": {"symbol": "䷆", "phrase": "贞，丈人吉无咎", "theme": "以正治国"},
            "比": {"symbol": "䷇", "phrase": "原筮元永贞", "theme": "亲附和睦"},
            "泰": {"symbol": "䷊", "phrase": "小往大来吉亨", "theme": "天地交泰"},
            "否": {"symbol": "䷋", "phrase": "否之匪人，不利君子贞", "theme": "小人道长"},
            "既济": {"symbol": "䷾", "phrase": "亨，小利贞", "theme": "事已成"},
            "未济": {"symbol": "䷿", "phrase": "亨，濡其尾", "theme": "事未成"},
        }
        
        # 爻辞练习题
        self.yao_questions = [
            {
                "gua": "乾",
                "yao": "初九",
                "phrase": "潜龙勿用",
                "options": [
                    "龙潜伏不要作为",
                    "龙在天上飞翔",
                    "龙在田野出现",
                    "龙过度亢奋"
                ],
                "answer": 0
            },
            {
                "gua": "乾",
                "yao": "九二",
                "phrase": "见龙在田",
                "options": [
                    "龙潜伏水中",
                    "龙现田野有利见贵人",
                    "龙飞上天",
                    "龙在深渊"
                ],
                "answer": 1
            },
            {
                "gua": "乾",
                "yao": "九五",
                "phrase": "飞龙在天",
                "options": [
                    "龙在地上",
                    "龙在水中",
                    "龙飞得高远的最佳状态",
                    "龙过头了"
                ],
                "answer": 2
            },
            {
                "gua": "乾",
                "yao": "上九",
                "phrase": "亢龙有悔",
                "options": [
                    "龙太亢奋会有悔恨",
                    "龙很高兴",
                    "龙在休息",
                    "龙刚开始"
                ],
                "answer": 0
            },
            {
                "gua": "坤",
                "yao": "初六",
                "phrase": "履霜坚冰至",
                "options": [
                    "走在雪地上",
                    "见微知著，从小处培养觉察力",
                    "冰很坚硬",
                    "冬天来了"
                ],
                "answer": 1
            }
        ]
        
        # 案例分析题
        self.case_questions = [
            {
                "scenario": "你在考虑是否接受一个新工作 Offer，起得乾卦，应该？",
                "options": [
                    "立即接受，乾卦代表大吉大利",
                    "分析自己处于乾卦的哪个阶段（潜龙/见龙/飞龙等）",
                    "不接受，乾卦太刚强不适合职场",
                    "再起一卦确认"
                ],
                "answer": 1,
                "explanation": "乾卦六爻各有不同含义，需要根据自身情况判断处于哪个阶段"
            },
            {
                "scenario": "感情遇到问题，起得坤卦，启示是？",
                "options": [
                    "应该主动强势处理",
                    "包容接纳，以柔克刚",
                    "立即分手",
                    "等待对方改变"
                ],
                "answer": 1,
                "explanation": "坤卦核心是包容承载，顺势而为，以柔顺的态度处理关系"
            },
            {
                "scenario": "创业初期起得屯卦，应该如何？",
                "options": [
                    "立即大规模扩张",
                    "艰难创业，稳扎稳打",
                    "放弃创业",
                    "寻求大量投资"
                ],
                "answer": 1,
                "explanation": "屯卦象征万物初生之难，需要谨慎积累，不宜冒进"
            }
        ]
        
    def display_menu(self):
        """显示主菜单"""
        print("\n" + "="*60)
        print("📚 周易学习练习测验系统".center(60))
        print("="*60)
        print("\n请选择练习类型：")
        print("1️⃣  八卦识别测验（8 题）")
        print("2️⃣  卦名记忆测验（12 题）")
        print("3️⃣  爻辞理解测验（5 题）")
        print("4️⃣  案例分析测验（3 题）")
        print("5️⃣  综合测验（全部 28 题）")
        print("6️⃣  查看学习进度")
        print("0️⃣  退出")
        
    def exercise_bagua(self):
        """八卦识别测验"""
        print("\n" + "="*60)
        print("🔮 八卦识别测验".center(60))
        print("="*60)
        print("\n规则：根据八卦的属性选择正确的卦名")
        print("共 8 题，每题 1 分\n")
        
        questions = []
        for name, data in self.bagua.items():
            questions.append({
                "question": f"八卦中，代表'{data['element']}'的是？",
                "options": list(self.bagua.keys()),
                "answer": name
            })
        
        random.shuffle(questions)
        return self.run_quiz(questions, "八卦识别")
        
    def exercise_hexagram(self):
        """卦名记忆测验"""
        print("\n" + "="*60)
        print("📜 卦名记忆测验".center(60))
        print("="*60)
        print("\n规则：根据卦的主题选择正确的卦名")
        print("共 12 题，每题 1 分\n")
        
        questions = []
        for name, data in self.hexagrams.items():
            questions.append({
                "question": f"主题为'{data['theme']}'的卦是？",
                "options": list(self.hexagrams.keys()),
                "answer": name
            })
        
        random.shuffle(questions)
        return self.run_quiz(questions, "卦名记忆")
        
    def exercise_yao(self):
        """爻辞理解测验"""
        print("\n" + "="*60)
        print("📖 爻辞理解测验".center(60))
        print("="*60)
        print("\n规则：选择爻辞的正确白话解读")
        print("共 5 题，每题 2 分\n")
        
        random.shuffle(self.yao_questions)
        return self.run_yao_quiz(self.yao_questions[:5], "爻辞理解")
        
    def exercise_case(self):
        """案例分析测验"""
        print("\n" + "="*60)
        print("🎯 案例分析测验".center(60))
        print("="*60)
        print("\n规则：根据场景选择正确的应用方式")
        print("共 3 题，每题 3 分\n")
        
        random.shuffle(self.case_questions)
        return self.run_case_quiz(self.case_questions[:3], "案例分析")
        
    def run_quiz(self, questions, quiz_name):
        """运行选择题测验"""
        self.score = 0
        self.total = len(questions)
        self.results = []
        
        for i, q in enumerate(questions, 1):
            print(f"\n第{i}/{self.total}题")
            print("-" * 40)
            print(f"Q: {q['question']}")
            
            # 打乱选项
            options = q['options']
            if isinstance(options, list):
                answer_index = options.index(q['answer'])
                options_with_idx = list(enumerate(options))
                random.shuffle(options_with_idx)
                
                for idx, opt in options_with_idx:
                    print(f"  {chr(65+idx)}. {opt}")
                
                while True:
                    choice = input("\n你的答案（A-D）：").strip().upper()
                    if choice in 'ABCD':
                        break
                    print("请输入 A、B、C 或 D")
                
                selected_idx = ord(choice) - 65
                correct_idx, _ = options_with_idx[selected_idx]
                
                if correct_idx == answer_index:
                    print("✅ 正确！")
                    self.score += 1
                else:
                    print(f"❌ 错误，正确答案是：{q['answer']}")
                    
                self.results.append({
                    "question": q['question'],
                    "correct": correct_idx == answer_index,
                    "answer": q['answer']
                })
                
            input("\n按 Enter 继续...")
            
        return self.show_result(quiz_name)
        
    def run_yao_quiz(self, questions, quiz_name):
        """运行爻辞测验"""
        self.score = 0
        self.total = len(questions)
        self.results = []
        
        for i, q in enumerate(questions, 1):
            print(f"\n第{i}/{self.total}题")
            print("-" * 40)
            print(f"卦：{q['gua']}卦 {q['yao']}")
            print(f"爻辞：「{q['phrase']}」")
            print("\n请选择正确的白话解读：")
            
            for idx, opt in enumerate(q['options']):
                print(f"  {chr(65+idx)}. {opt}")
                
            while True:
                choice = input("\n你的答案（A-D）：").strip().upper()
                if choice in 'ABCD':
                    break
                print("请输入 A、B、C 或 D")
            
            if int(choice) - 65 == q['answer']:
                print("✅ 正确！")
                self.score += 2  # 每题 2 分
            else:
                print(f"❌ 错误，正确答案是：{q['options'][q['answer']]}")
                
            self.results.append({
                "question": f"{q['gua']}卦 {q['yao']}: {q['phrase']}",
                "correct": int(choice) - 65 == q['answer'],
                "answer": q['options'][q['answer']]
            })
            
            input("\n按 Enter 继续...")
            
        return self.show_result(quiz_name)
        
    def run_case_quiz(self, questions, quiz_name):
        """运行案例测验"""
        self.score = 0
        self.total = len(questions)
        self.results = []
        
        for i, q in enumerate(questions, 1):
            print(f"\n第{i}/{self.total}题")
            print("-" * 40)
            print(f"场景：{q['scenario']}")
            print("\n请选择：")
            
            for idx, opt in enumerate(q['options']):
                print(f"  {chr(65+idx)}. {opt}")
                
            while True:
                choice = input("\n你的答案（A-D）：").strip().upper()
                if choice in 'ABCD':
                    break
                print("请输入 A、B、C 或 D")
            
            if int(choice) - 65 == q['answer']:
                print("✅ 正确！")
                self.score += 3  # 每题 3 分
            else:
                print(f"❌ 错误")
                print(f"💡 解析：{q['explanation']}")
                
            self.results.append({
                "question": q['scenario'],
                "correct": int(choice) - 65 == q['answer'],
                "answer": q['options'][q['answer']],
                "explanation": q['explanation']
            })
            
            input("\n按 Enter 继续...")
            
        return self.show_result(quiz_name)
        
    def show_result(self, quiz_name):
        """显示测验结果"""
        print("\n" + "="*60)
        print(f"📊 {quiz_name}测验结果".center(60))
        print("="*60)
        
        max_score = self.total * 2 if quiz_name == "爻辞理解" else (self.total * 3 if quiz_name == "案例分析" else self.total)
        percentage = (self.score / max_score * 100) if max_score > 0 else 0
        
        print(f"\n得分：{self.score} / {max_score}")
        print(f"正确率：{percentage:.1f}%")
        
        if percentage >= 90:
            print("\n🌟 优秀！你已经掌握了这个知识点")
        elif percentage >= 70:
            print("\n👍 良好！继续加油")
        elif percentage >= 60:
            print("\n📚 合格！需要加强练习")
        else:
            print("\n⚠️  需要重新学习这个知识点")
            
        # 显示错题
        wrong_count = sum(1 for r in self.results if not r['correct'])
        if wrong_count > 0:
            print(f"\n📝 错题回顾（{wrong_count}题）：")
            print("-" * 40)
            for i, r in enumerate(self.results, 1):
                if not r['correct']:
                    print(f"{i}. {r['question']}")
                    print(f"   正确答案：{r['answer']}")
                    if 'explanation' in r:
                        print(f"   解析：{r['explanation']}")
                        
        # 保存成绩
        self.save_result(quiz_name)
        
        return self.score, max_score
        
    def save_result(self, quiz_name):
        """保存测验结果"""
        filename = f"exercise_result_{date.today().strftime('%Y%m%d')}.json"
        
        result_data = {
            "date": str(date.today()),
            "quiz_name": quiz_name,
            "score": self.score,
            "total": self.total,
            "results": self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
            
        print(f"\n💾 成绩已保存到 {filename}")
        
    def show_progress(self):
        """显示学习进度"""
        print("\n" + "="*60)
        print("📈 学习进度".center(60))
        print("="*60)
        
        # 读取所有成绩文件
        import glob
        result_files = glob.glob("exercise_result_*.json")
        
        if not result_files:
            print("\n暂无练习记录")
            return
            
        print(f"\n共找到 {len(result_files)} 次练习记录")
        
        # 统计各类型练习
        progress = {}
        for filepath in result_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            quiz_name = data['quiz_name']
            if quiz_name not in progress:
                progress[quiz_name] = []
            progress[quiz_name].append(data)
            
        # 显示统计
        for quiz_name, records in progress.items():
            scores = [r['score'] for r in records]
            avg = sum(scores) / len(scores) if scores else 0
            print(f"\n{quiz_name}:")
            print(f"  练习次数：{len(records)}")
            print(f"  平均得分：{avg:.1f}")
            
    def run(self):
        """运行主程序"""
        while True:
            self.display_menu()
            
            choice = input("\n请选择（0-6）：").strip()
            
            if choice == "1":
                self.exercise_bagua()
            elif choice == "2":
                self.exercise_hexagram()
            elif choice == "3":
                self.exercise_yao()
            elif choice == "4":
                self.exercise_case()
            elif choice == "5":
                # 综合测验
                print("\n🚀 开始综合测验（全部 28 题）\n")
                self.exercise_bagua()
                self.exercise_hexagram()
                self.exercise_yao()
                self.exercise_case()
                print("\n🎉 综合测验完成！")
            elif choice == "6":
                self.show_progress()
            elif choice == "0":
                print("\n👋 感谢使用，再见！")
                break
            else:
                print("\n⚠️  无效选项，请重新选择")

if __name__ == "__main__":
    exercise = ZhouyiExercise()
    exercise.run()
