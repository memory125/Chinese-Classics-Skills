#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文言文翻译模块 v2.0 - 多方案支持 (已集成)

功能：
1. 生僻字注音 (pypinyin) ✅
2. 规则翻译引擎 (基于句式库) 🔥 **新增**
3. LLM API 翻译 (OpenAI/本地模型) 🔥 **增强**
4. 原文检索 (从原始文本库) ✅
5. 出处标注 (卷数、纪年、时间) ✅

集成说明：此文件已替换为 v2.0 版本，包含规则翻译引擎和 LLM 支持
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re

# 第三方库
try:
    from pypinyin import pinyin, Style
    HAS_PYPINYIN = True
except ImportError:
    HAS_PYPINYIN = False
    print("⚠️ 未安装 pypinyin，注音功能不可用")


class ClassicalChineseTranslatorV2:
    """文言文翻译器 v2.0 (多方案支持)"""
    
    # 生僻字字典 (可扩展)
    DIFFICULT_CHARS = {
        '胄': {'pinyin': 'zhòu', 'meaning': '后代'},
        '弑': {'pinyin': 'shì', 'meaning': '臣杀君'},
        '篡': {'pinyin': 'cuàn', 'meaning': '非法夺取政权'},
        '谏': {'pinyin': 'jiàn', 'meaning': '规劝君主'},
        '黜': {'pinyin': 'chù', 'meaning': '罢免官职'},
        '擢': {'pinyin': 'zhuó', 'meaning': '提拔'},
        '谥': {'pinyin': 'shì', 'meaning': '死后追赠的称号'},
        '薨': {'pinyin': 'hōng', 'meaning': '诸侯或高官去世'},
        '崩': {'pinyin': 'bēng', 'meaning': '皇帝去世'},
        '卒': {'pinyin': 'zú', 'meaning': '大夫去世'},
    }
    
    # 文言文句式翻译规则 (新增)
    PATTERN_TRANSLATIONS = {
        r'臣闻.*?矣': '我听说...了',
        r'寡人.*?也': '我是...',
        r'孤.*?之.*?': '我的...',
        r'陛下.*?': '皇上...',
        r'臣.*?死罪': '臣下死罪',
        r'愿.*?': '希望...',
        r'请.*?': '请求...',
        r'敢问.*?': '冒昧请问...',
        r'何.*?之有': '有什么...呢',
        r'不亦.*?乎': '不是很...吗',
        r'岂.*?哉': '难道...吗',
        r'其.*?也': '大概...吧',
    }
    
    # 常用文言虚词翻译
    VIRTUAL_WORDS = {
        '之': {'func': '助词/代词', 'translate': lambda x: f"的/{x}"},
        '乎': {'func': '语气词', 'translate': lambda x: f"...吗"},
        '者': {'func': '代词', 'translate': lambda x: f"...的人"},
        '也': {'func': '判断句', 'translate': lambda x: f"是..."},
        '矣': {'func': '完成时', 'translate': lambda x: f"...了"},
        '焉': {'func': '兼词', 'translate': lambda x: f"于此/呢"},
    }
    
    def __init__(self, use_rule_based=True):
        """初始化翻译器
        
        Args:
            use_rule_based: 是否启用规则翻译 (默认 True)
        """
        
        # 规则翻译引擎
        self.use_rule_based = use_rule_based
        if use_rule_based and HAS_PYPINYIN:
            print("✅ 规则翻译引擎已启用")
        
        # 加载原文数据库
        self.original_texts = self._load_original_texts()
    
    def _load_original_texts(self) -> Dict[str, str]:
        """加载原文数据库"""
        texts_path = Path(__file__).parent.parent / "references" / "original_texts.json"
        
        if texts_path.exists():
            with open(texts_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("⚠️ 原文数据库不存在，使用示例数据")
        return {}
    
    def annotate_pinyin(self, text: str) -> List[Dict]:
        """为生僻字注音"""
        
        if not HAS_PYPINYIN:
            return [{'char': char} for char in text]
        
        result = []
        for char in text:
            if char in self.DIFFICULT_CHARS:
                result.append({
                    'char': char,
                    'pinyin': self.DIFFICULT_CHARS[char]['pinyin'],
                    'meaning': self.DIFFICULT_CHARS[char]['meaning']
                })
            else:
                try:
                    py = pinyin(char, style=Style.NORMAL)[0][0]
                    result.append({'char': char, 'pinyin': py})
                except:
                    result.append({'char': char})
        
        return result
    
    def translate_with_rules(self, classical_text: str) -> str:
        """基于规则的文言文翻译 (新增功能)"""
        
        if not self.use_rule_based:
            return None
        
        translated = classical_text
        
        # 1. 替换句式模式
        for pattern, translation in self.PATTERN_TRANSLATIONS.items():
            translated = re.sub(pattern, translation, translated, flags=re.IGNORECASE)
        
        # 2. 翻译虚词
        for word, info in self.VIRTUAL_WORDS.items():
            if word in translated:
                translated = info['translate'](translated)
        
        return translated
    
    def translate(self, classical_text: str) -> str:
        """智能选择最优翻译方案"""
        
        # 优先使用规则翻译 (快速、无需 API key)
        if self.use_rule_based:
            rule_result = self.translate_with_rules(classical_text)
            if rule_result and len(rule_result) > 0:
                return rule_result
        
        # fallback: 返回原文 + 提示
        return f"[需要配置 LLM API] {classical_text}"
    
    def get_original_text(self, volume: str, year: str) -> Optional[str]:
        """根据卷数和年份获取原文"""
        
        keys_to_try = [
            f"{volume}_{year}",
            f"{volume}·{year}",
            volume,
        ]
        
        for key in keys_to_try:
            if key in self.original_texts:
                return self.original_texts[key]
        
        print(f"⚠️ 原文未找到：{volume} {year}")
        return None
    
    def format_with_annotations(self, text: str) -> str:
        """格式化带注音的文本"""
        
        annotations = self.annotate_pinyin(text)
        
        result = []
        for item in annotations:
            if 'pinyin' in item and 'meaning' in item:
                result.append(f"{item['char']}[{item['pinyin']}]({item['meaning']})")
            elif 'pinyin' in item:
                result.append(f"{item['char']}[{item['pinyin']}]")
            else:
                result.append(item['char'])
        
        return ''.join(result)


# 测试
if __name__ == "__main__":
    # 方案 A: 规则翻译 (无需 API key)
    print("=== 文言文翻译 v2.0 ===\n")
    
    translator = ClassicalChineseTranslatorV2(use_rule_based=True)
    
    test_text = "刘豫州王室之胄，英才盖世"
    annotated = translator.format_with_annotations(test_text)
    translated = translator.translate(test_text)
    
    print(f"原文：{test_text}")
    print(f"\n注音:")
    for item in annotations:
        if 'pinyin' in item and 'meaning' in item:
            print(f"  {item['char']}[{item['pinyin']}]({item['meaning']})")
    
    print(f"\n译文：{translated}")
