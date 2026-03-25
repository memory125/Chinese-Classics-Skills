#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式起卦解卦工具 - 周易学习技能 v1.0
引导用户提出问题，模拟起卦过程，生成卦象并解读

版本：v1.0 (2026-03-25)
"""

import random
import sys
from datetime import date

class InteractiveGua:
    """交互式起卦解卦系统"""
    
    # 八卦基础数据
    BAGUA = {
        0: {"name": "坤", "symbol": "☷", "element": "地", "binary": "000"},
        1: {"name": "乾", "symbol": "☰", "element": "天", "binary": "111"},
        2: {"name": "坎", "symbol": "☵", "element": "水", "binary": "010"},
        3: {"name": "离", "symbol": "☲", "element": "火", "binary": "101"},
        4: {"name": "艮", "symbol": "☶", "element": "山", "binary": "001"},
        5: {"name": "震", "symbol": "☳", "element": "雷", "binary": "100"},
        6: {"name": "巽", "symbol": "☴", "element": "风", "binary": "110"},
        7: {"name": "兑", "symbol": "☱", "element": "泽", "binary": "011"},
    }
    
    # 六十四卦名称（简化版）
    HEXAGRAM_NAMES = {
        (1, 1): "乾为天", (0, 0): "坤为地", (2, 2): "坎为水", (3, 3): "离为火",
        (4, 4): "艮为山", (5, 5): "震为雷", (6, 6): "巽为风", (7, 7): "兑为泽",
        (0, 1): "地天泰", (1, 0): "天地否", (3, 2): "火水未济", (2, 3): "水火既济",
        # 更多卦象可以补充
    }
    
    def __init__(self):
        self.question = ""
        self.context = ""
        self.hexagram_upper = None
        self.hexagram_lower = None
        self.moving_lines = []
        
    def greet(self):
        """问候用户"""
        print("\n" + "="*60)
        print("🔮 欢迎来到周易交互式起卦解卦系统".center(60))
        print("="*60)
        print("\n我将引导你完成以下步骤：")
        print("1️⃣ 明确你的问题")
        print("2️⃣ 选择起卦方式")
        print("3️⃣ 生成卦象")
        print("4️⃣ 解读卦象")
        print("\n开始之前，请深呼吸，静下心来。\n")
        
    def collect_question(self):
        """收集用户问题"""
        print("\n📝 第一步：明确你的问题")
        print("-" * 40)
        print("\n请思考你要问的事情，可以是：")
        print("• 事业决策（是否换工作、创业时机等）")
        print("• 人际关系（感情、家庭、朋友等）")
        print("• 投资理财（投资时机、买房等）")
        print("• 学习规划（考研、学习新技能等）")
        print("• 健康问题（养生、治疗方案等）")
        print("\n现在，请用一句话描述你的问题：")
        
        self.question = input("> ").strip()
        
        if not self.question:
            print("\n⚠️  问题不能为空，请重新输入")
            return self.collect_question()
            
        print(f"\n✅ 你的问题是：「{self.question}」")
        
        # 收集背景信息
        print("\n请简要描述相关背景（可选，按 Enter 跳过）：")
        self.context = input("> ").strip()
        
    def choose_method(self):
        """选择起卦方式"""
        print("\n🎲 第二步：选择起卦方式")
        print("-" * 40)
        print("\n请选择：")
        print("1️⃣  硬币法（最传统，模拟抛硬币 18 次）")
        print("2️⃣  数字法（输入 3 个数字快速起卦）")
        print("3️⃣  时间法（根据当前时间起卦）")
        
        choice = input("\n请输入选项编号（1-3）：").strip()
        
        if choice == "1":
            return self.coin_method()
        elif choice == "2":
            return self.number_method()
        elif choice == "3":
            return self.time_method()
        else:
            print("\n⚠️  无效选项，请重新选择")
            return self.choose_method()
            
    def coin_method(self):
        """硬币法起卦"""
        print("\n" + "="*60)
        print("🪙 硬币法起卦（模拟）".center(60))
        print("="*60)
        print("\n方法说明：")
        print("• 想象手中拿着 3 枚硬币")
        print("• 心中默念你的问题")
        print("• 抛掷 6 次，每次生成一爻（从下到上）")
        print("\n每爻可能有四种结果：")
        print("  老阴 (6) - 变爻 - 阴变阳")
        print("  少阳 (7) - 不变")
        print("  少阴 (8) - 不变")
        print("  老阳 (9) - 变爻 - 阳变阴")
        
        input("\n准备好了吗？按 Enter 开始抛硬币...")
        
        lines = []
        for i in range(6):
            print(f"\n第{i+1}爻：")
            input("  按 Enter 抛掷硬币...")
            
            # 模拟抛硬币结果
            result = random.choice([6, 7, 8, 9])
            lines.append(result)
            
            line_names = {6: "老阴 ⚋", 7: "少阳 ⚊", 8: "少阴 ⚋", 9: "老阳 ⚊"}
            print(f"  结果：{line_names[result]}")
            
            if result in [6, 9]:
                print("  ⚡ 这是变爻！")
                self.moving_lines.append(i + 1)
                
        return self.generate_hexagram(lines)
        
    def number_method(self):
        """数字法起卦"""
        print("\n" + "="*60)
        print("🔢 数字法起卦".center(60))
        print("="*60)
        print("\n请凭直觉输入 3 个数字（1-999 任意数字）：")
        
        try:
            num1 = int(input("第一个数字：").strip())
            num2 = int(input("第二个数字：").strip())
            num3 = int(input("第三个数字：").strip())
        except ValueError:
            print("\n⚠️  请输入有效的数字")
            return self.choose_method()
            
        # 计算卦象
        upper = num1 % 8
        lower = num2 % 8
        moving = num3 % 6
        
        # 生成六爻
        lines = []
        for i in range(6):
            base = random.choice([7, 8])  # 少阳或少阴
            if i == moving:
                base = random.choice([6, 9])  # 变爻
            lines.append(base)
            
        self.moving_lines = [moving + 1] if moving < 6 else []
        
        return self.generate_hexagram(lines)
        
    def time_method(self):
        """时间法起卦"""
        print("\n" + "="*60)
        print("🕐 时间法起卦".center(60))
        print("="*60)
        print(f"\n当前时间：{date.today()}")
        print("根据农历时间起卦...")
        
        # 简化版：用随机模拟
        lines = [random.choice([6, 7, 8, 9]) for _ in range(6)]
        
        # 标记变爻
        for i, line in enumerate(lines):
            if line in [6, 9]:
                self.moving_lines.append(i + 1)
                
        return self.generate_hexagram(lines)
        
    def generate_hexagram(self, lines):
        """根据六爻生成卦象"""
        print("\n" + "="*60)
        print("📊 第三步：生成卦象".center(60))
        print("="*60)
        
        # 计算上下卦
        upper_trigram = (lines[5] % 2) * 4 + (lines[4] % 2) * 2 + (lines[3] % 2)
        lower_trigram = (lines[2] % 2) * 4 + (lines[1] % 2) * 2 + (lines[0] % 2)
        
        self.hexagram_upper = upper_trigram
        self.hexagram_lower = lower_trigram
        
        # 显示卦形
        print("\n你的卦象：")
        print("-" * 40)
        
        line_symbols = {6: "⚏", 7: "⚊", 8: "⚋", 9: "⚐"}
        line_names = {6: "老阴", 7: "少阳", 8: "少阴", 9: "老阳"}
        
        for i in range(5, -1, -1):
            line = lines[i]
            symbol = line_symbols[line]
            name = line_names[line]
            moving_mark = " ⚡" if i + 1 in self.moving_lines else ""
            print(f"第{i+1}爻：{symbol} {name}{moving_mark}")
            
        upper_name = self.BAGUA[upper_trigram]["name"]
        lower_name = self.BAGUA[lower_trigram]["name"]
        
        print(f"\n上卦：{upper_name} {self.BAGUA[upper_trigram]['symbol']}")
        print(f"下卦：{lower_name} {self.BAGUA[lower_trigram]['symbol']}")
        
        # 尝试匹配卦名
        gua_name = self.HEXAGRAM_NAMES.get((upper_trigram, lower_trigram), "未知卦")
        print(f"\n卦名：{gua_name}")
        
        if self.moving_lines:
            print(f"\n变爻：第{self.moving_lines}爻")
            
        return lines
        
    def interpret(self, lines):
        """解读卦象"""
        print("\n" + "="*60)
        print("🔮 第四步：解读卦象".center(60))
        print("="*60)
        
        print(f"\n📝 问题：{self.question}")
        
        if self.context:
            print(f"📋 背景：{self.context}")
            
        print("\n💡 基本解读原则：")
        print("1. 先看本卦（当前状态）")
        print("2. 再看变爻（变化关键点）")
        print("3. 后看之卦（发展趋势）")
        
        print("\n🎯 给你的建议：")
        print("-" * 40)
        
        # 根据卦象给出通用建议
        upper_element = self.BAGUA[self.hexagram_upper]["element"]
        lower_element = self.BAGUA[self.hexagram_lower]["element"]
        
        print(f"• 上卦 {upper_element} 代表外部环境/趋势")
        print(f"• 下卦 {lower_element} 代表内在状态/基础")
        
        if self.moving_lines:
            print(f"\n⚡ 有变爻，说明情况会变化")
            print("• 重点关注变爻的启示")
            print("• 变化可能是契机也可能是挑战")
        else:
            print("\n🔄 无变爻，说明当前状态相对稳定")
            print("• 以卦辞为主要参考")
            print("• 保持现状或微调即可")
            
        print("\n📚 深度解读建议：")
        print("• 查看 'references/六十四卦终极版_v10.md' 获取完整解读")
        print("• 参考 'references/修心指南.md' 进行心性修炼")
        print("• 对比 'references/案例库.md' 中的相似案例")
        
        print("\n⚠️  重要提醒：")
        print("• 卦象是参考，不是绝对预测")
        print("• 最终决策需要结合理性分析")
        print("• 周易的核心是提升判断力和思考深度")
        
    def save_result(self):
        """保存结果"""
        print("\n💾 是否保存这次起卦记录？")
        choice = input("输入 y 保存，其他键跳过：").strip().lower()
        
        if choice == 'y':
            filename = f"gua_record_{date.today().strftime('%Y%m%d')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"问题：{self.question}\n")
                if self.context:
                    f.write(f"背景：{self.context}\n")
                f.write(f"日期：{date.today()}\n")
                f.write(f"上卦：{self.BAGUA[self.hexagram_upper]['name']}\n")
                f.write(f"下卦：{self.BAGUA[self.hexagram_lower]['name']}\n")
                if self.moving_lines:
                    f.write(f"变爻：{self.moving_lines}\n")
            print(f"✅ 已保存到 {filename}")
            
    def run(self):
        """运行完整流程"""
        self.greet()
        self.collect_question()
        self.choose_method()
        self.interpret([])
        self.save_result()
        
        print("\n" + "="*60)
        print("🙏 感谢使用，祝好！".center(60))
        print("="*60 + "\n")

if __name__ == "__main__":
    gua = InteractiveGua()
    gua.run()
