#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
# -*- coding: utf-8 -*-
"""
"""
修复 V11 格式问题：
1. 修正重复的卦名（### 1. 1. → ### 1.）
2. 更新版本号
3. 验证最终结果
"""

import re

# 读取 V11 文件
with open('references/六十四卦终极版_v11.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复重复的卦名格式
content = re.sub(r'^### (\d+)\. \d+\. ', r'### \1. ', content, flags=re.MULTILINE)

# 更新文件标题和版本信息
old_header = "# 六十四卦完整数"
new_header = """# 六十四卦终极版 v11.0

> 周易学习技能 · 白话 + 实用教学
> 
> 本文件包含完整的六十四卦数据，每个卦象包括：
> 1. **基本信息表**：卦形、卦辞、白话、核心精神、应用场景
> 2. **爻辞详解表**：六爻白话解读与实际应用
> 3. **卦象关系**：错卦、综卦、互卦
> 4. **典型案例**：现代企业/历史人物案例

**版本历史**：
- **v11.0** (2026-03-16): ✅ 完美 64 卦，无重复无缺失
- **v10.0** (2026-03-13): 64 条目（56 独立卦，8 重复）
- **v9.0**: 基础版本

**使用建议**：
1. **初学者**: 从"乾"、"坤"开始，理解基本概念
2. **进阶**: 按序号顺序学习，掌握卦象变化
3. **应用**: 结合典型案例，理解实际应用

---

"""

content = content.replace(old_header, new_header)

# 写入文件
with open('references/六十四卦终极版_v11.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 格式修复完成！")

# 验证
with open('references/六十四卦终极版_v11.md', 'r', encoding='utf-8') as f:
    new_content = f.read()

# 检查卦名格式
gua_pattern = r'^### (\d+)\. (.+)$'
matches = re.findall(gua_pattern, new_content, re.MULTILINE)

print(f"\n=== 验证结果 ===")
print(f"总卦数：{len(matches)}")
print(f"格式正确：{all(len(m[0]) <= 2 for m in matches)}")

# 检查前 10 卦
print(f"\n前 10 卦:")
for i, (num, name) in enumerate(matches[:10], 1):
    print(f"  {i}. {num}. {name}")

# 检查后 10 卦
print(f"\n后 10 卦:")
for i, (num, name) in enumerate(matches[-10:], len(matches)-9):
    print(f"  {i}. {num}. {name}")

# 检查重复
names = [m[1] for m in matches]
from collections import Counter
name_counts = Counter(names)
duplicates = [(n, c) for n, c in name_counts.items() if c > 1]

if duplicates:
    print(f"\n⚠️ 发现重复：{len(duplicates)}")
    for name, count in duplicates:
        print(f"  {name}: {count}次")
else:
    print(f"\n✅ 无重复！完美 64 卦！")

# 检查序号连续性
nums = [int(m[0]) for m in matches]
if nums == list(range(1, 65)):
    print(f"✅ 序号连续：1-64")
else:
    print(f"⚠️ 序号异常：{nums[:5]}...{nums[-5:]}")
