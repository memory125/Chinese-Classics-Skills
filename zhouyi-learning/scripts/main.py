#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易学习技能 - 主入口
快速访问所有功能
"""

import os
import sys

# 确保在工作目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def clear_screen():
    """清屏"""
    os.system('clear' if os.name == 'posix' else 'cls')

def show_welcome():
    """显示欢迎信息"""
    clear_screen()
    print("""
╔══════════════════════════════════════════╗
║                                          ║
║         📜 周易学习技能 v1.0 📜        ║
║                                          ║
║      第一性原理 · 修心智慧 · 实战应用    ║
║                                          ║
╚══════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    """)

def show_menu():
    """显示主菜单"""
    print("📚 核心功能")
    print("-" * 40)
    print("1️⃣  每日一卦          - 今日卦象推荐 (农历 + 节气)")
    print("2️⃣  交互起卦解卦     - 硬币/数字/时间法起卦")
    print("3️⃣  练习测验系统     - 八卦/卦名/爻辞/案例分析")
    print("4️⃣  查询农历干支     - 今日农历日期与干支")
    print("5️⃣  查询节气信息     - 24 节气与卦象对应")
    print()
    print("📖 学习资源")
    print("-" * 40)
    print("6️⃣  六十四卦查询     - 查看卦象完整解读")
    print("7️⃣  修心指南         - 18 个核心卦象心性修炼")
    print("8️⃣  案例库浏览       - 18+ 真实应用案例")
    print()
    print("🛠️  工具选项")
    print("-" * 40)
    print("9️⃣  查看文件结构     - 浏览技能目录")
    print("🔟  查看帮助         - 完整使用说明")
    print()
    print("0️⃣  退出")
    print()

def run_daily_gua():
    """运行每日一卦"""
    print("\n📅 正在加载每日一卦...\n")
    os.system(f"python3 {SCRIPT_DIR}/daily-gua.py")
    input("\n按回车键返回主菜单...")

def run_interactive_gua():
    """运行交互起卦"""
    print("\n🎲 正在启动交互起卦...\n")
    os.system(f"python3 {SCRIPT_DIR}/interactive-gua.py")
    input("\n按回车键返回主菜单...")

def run_exercise():
    """运行练习测验"""
    print("\n📝 正在启动练习测验...\n")
    os.system(f"python3 {SCRIPT_DIR}/exercise-system.py")
    input("\n按回车键返回主菜单...")

def run_lunar():
    """运行农历查询"""
    print("\n📆 正在查询农历干支...\n")
    os.system(f"python3 {SCRIPT_DIR}/get-lunar-ganzhi.py")
    input("\n按回车键返回主菜单...")

def run_solar_term():
    """运行节气查询"""
    print("\n☀️ 正在查询节气信息...\n")
    os.system(f"python3 {SCRIPT_DIR}/get-solar-term.py")
    input("\n按回车键返回主菜单...")

def view_gua_database():
    """查看六十四卦数据库"""
    gua_file = os.path.join(SCRIPT_DIR, '..', 'references', '六十四卦终极版_v10.md')
    if os.path.exists(gua_file):
        print(f"\n📖 正在打开卦象数据库：{gua_file}\n")
        # 尝试用 cat 显示前 100 行
        os.system(f"head -n 100 '{gua_file}'")
        print("\n👉 提示：完整内容请查看文件或使用 OpenClaw 对话查询")
    else:
        print(f"\n❌ 未找到卦象数据库：{gua_file}")
    input("\n按回车键返回主菜单...")

def view_xiuxin():
    """查看修心指南"""
    xiuxin_file = os.path.join(SCRIPT_DIR, '..', 'references', '修心指南_v3.md')
    if os.path.exists(xiuxin_file):
        print(f"\n🧘 正在打开修心指南：{xiuxin_file}\n")
        os.system(f"head -n 80 '{xiuxin_file}'")
        print("\n👉 提示：完整内容请查看文件")
    else:
        print(f"\n❌ 未找到修心指南：{xiuxin_file}")
    input("\n按回车键返回主菜单...")

def view_cases():
    """查看案例库"""
    cases_file = os.path.join(SCRIPT_DIR, '..', 'references', '案例库.md')
    if os.path.exists(cases_file):
        print(f"\n💼 正在打开案例库：{cases_file}\n")
        os.system(f"head -n 80 '{cases_file}'")
        print("\n👉 提示：完整内容请查看文件")
    else:
        print(f"\n❌ 未找到案例库：{cases_file}")
    input("\n按回车键返回主菜单...")

def view_structure():
    """查看文件结构"""
    print("\n📁 周易学习技能文件结构:\n")
    os.system(f"tree -L 2 '{SCRIPT_DIR}/..' 2>/dev/null || ls -la '{SCRIPT_DIR}/..'")
    input("\n按回车键返回主菜单...")

def show_help():
    """显示帮助"""
    print("""
╔══════════════════════════════════════════╗
║         📖 周易学习技能 - 帮助            ║
╚══════════════════════════════════════════╝

🎯 核心功能说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ 每日一卦
   - 结合农历日期和 24 节气推荐今日卦象
   - 包含卦辞、白话解读、核心启发
   - 适用场景建议

2️⃣ 交互起卦解卦
   - 支持硬币法、数字法、时间法
   - 引导式问题梳理
   - 自动生成卦象并解读

3️⃣ 练习测验
   - 八卦识别测验 (8 题)
   - 卦名记忆测验 (12 题)
   - 爻辞理解测验 (5 题)
   - 案例分析测验 (3 题)
   - 综合测验 (28 题)
   - 成绩自动保存，支持进度追踪

4️⃣ 农历干支查询
   - 公历 ↔ 农历转换
   - 干支纪年日计算
   - 支持 2024-2030 年

5️⃣ 节气查询
   - 24 节气日期计算
   - 节气与卦象对应
   - 季节特征解读

📚 学习资源
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6️⃣ 六十四卦查询
   - 64 卦完整数据 (v10.1 终极版)
   - 卦形、卦辞、爻辞
   - 白话解读 + 多维启示

7️⃣ 修心指南
   - 18 个核心卦象心性修炼
   - 8 个经卦 + 10 个常用卦
   - 修心实践指导

8️⃣ 案例库
   - 18+ 真实应用案例
   - 涵盖工作、感情、健康等 6 大类
   - 完整案例链：背景→起卦→解卦→复盘

💡 使用建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 每日使用"每日一卦"培养感觉
• 遇到问题时"交互起卦"分析趋势
• 定期"练习测验"巩固知识
• 结合"修心指南"提升心性

⚠️ 重要原则
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 周易是古人观察世界的方法，不是玄学
• 卦象提供趋势参考，不决定最终结果
• 学习目的是提升判断力和思考深度
• 循序渐进：从基础概念开始，逐步深入

🔧 命令行工具
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd ~/.openclaw/workspace/skills/zhouyi-learning/scripts/

python3 main.py              # 本交互菜单
python3 daily-gua.py         # 每日一卦
python3 interactive-gua.py   # 交互起卦
python3 exercise-system.py   # 练习测验
python3 get-lunar-ganzhi.py  # 农历查询
python3 get-solar-term.py    # 节气查询

📖 完整文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SKILL.md      - 技能说明
README.md     - 详细文档
references/   - 知识库目录

    """)
    input("\n按回车键返回主菜单...")

def main():
    """主循环"""
    while True:
        show_welcome()
        show_menu()
        
        choice = input("🎯 请输入选项 (0-9): ").strip()
        
        try:
            if choice == '1':
                run_daily_gua()
            elif choice == '2':
                run_interactive_gua()
            elif choice == '3':
                run_exercise()
            elif choice == '4':
                run_lunar()
            elif choice == '5':
                run_solar_term()
            elif choice == '6':
                view_gua_database()
            elif choice == '7':
                view_xiuxin()
            elif choice == '8':
                view_cases()
            elif choice == '9':
                view_structure()
            elif choice == '10' or choice == '🔟':
                show_help()
            elif choice == '0':
                print("\n👋 感谢使用周易学习技能！")
                print("🌟 记住：周易不是占卜工具，而是修心智慧。\n")
                sys.exit(0)
            else:
                print(f"\n⚠️  无效选项：{choice}，请输入 0-10")
                input("按回车键继续...")
        except KeyboardInterrupt:
            print("\n\n👋 感谢使用周易学习技能！\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
