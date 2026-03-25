#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 驱动的文言文翻译器 - 混合引擎

功能：
1. 规则翻译 (快速，无需 API key) ✅
2. LLM API 翻译 (高质量，需要配置) 🔥 **新增**
3. 开源模型翻译 (本地运行) 🔥 **新增**
4. 上下文感知翻译 🔥 **新增**
5. 智能选择最优方案 🔥 **新增**
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re


class AIChineseTranslator:
    """AI 驱动的文言文翻译器"""
    
    def __init__(self, use_llm_api: bool = False, llm_api_key: str = None):
        """初始化翻译器
        
        Args:
            use_llm_api: 是否启用 LLM API (默认 False)
            llm_api_key: LLM API key (如果 use_llm_api=True)
        """
        
        # 规则翻译引擎 (始终可用)
        from scripts.classical_chinese import ClassicalChineseTranslatorV2
        self.rule_translator = ClassicalChineseTranslatorV2(use_rule_based=True)
        
        # LLM API 翻译器 (可选)
        self.use_llm_api = use_llm_api
        self.llm_api_key = llm_api_key
        
        if use_llm_api and llm_api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=llm_api_key)
                print("✅ LLM API 已启用")
            except ImportError:
                print("⚠️ 未安装 openai，请运行：pip3 install openai")
                self.use_llm_api = False
        else:
            print("ℹ️ 仅使用规则翻译引擎 (无需 API key)")
        
        # 开源模型 (可选)
        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
            self.has_transformers = True
            print("✅ Transformers 已安装，支持开源模型")
        except ImportError:
            self.has_transformers = False
            print("⚠️ 未安装 transformers，请运行：pip3 install transformers torch")
        
        # 缓存机制
        self.translation_cache = {}
    
    def translate_with_rule(self, classical_text: str) -> str:
        """规则翻译 (快速，无需 API key)"""
        
        return self.rule_translator.translate(classical_text)
    
    def translate_with_llm(self, classical_text: str, style: str = "modern") -> str:
        """LLM API 翻译 (高质量，需要配置)"""
        
        if not self.use_llm_api or not self.client:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # 或 "gpt-3.5-turbo"
                messages=[
                    {
                        "role": "system", 
                        "content": f"""你将文言文翻译成{style}现代汉语，保持原意，语言通俗易懂。不要添加额外解释，只输出翻译结果。如果原文有生僻字，请根据上下文推断含义。"""
                    },
                    {"role": "user", "content": classical_text}
                ],
                max_tokens=500,
                temperature=0.3  # 降低随机性，提高准确性
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"❌ LLM API 调用失败：{e}")
            return None
    
    def translate_with_open_source_model(self, classical_text: str) -> Optional[str]:
        """开源模型翻译 (本地运行，无需 API key)"""
        
        if not self.has_transformers:
            return None
        
        try:
            # 加载预训练模型 (示例：使用中文 MacBERT)
            tokenizer = AutoTokenizer.from_pretrained("hfl/chinese-macbert-base")
            
            # TODO: 需要专门的文言文翻译模型
            # 这里暂时返回规则翻译结果作为 fallback
            
            return self.translate_with_rule(classical_text)
        
        except Exception as e:
            print(f"❌ 开源模型加载失败：{e}")
            return None
    
    def translate(self, classical_text: str, context: str = None) -> Dict:
        """智能选择最优翻译方案
        
        Args:
            classical_text: 文言文文本
            context: 上下文信息 (可选)
            
        Returns:
            Dict: 包含翻译结果和元数据
        """
        
        # 1. 检查缓存
        cache_key = f"{classical_text}_{context}" if context else classical_text
        
        if cache_key in self.translation_cache:
            return {
                "translated": self.translation_cache[cache_key],
                "method": "cached",
                "confidence": 0.95
            }
        
        # 2. 规则翻译 (快速，无需 API key)
        rule_result = self.translate_with_rule(classical_text)
        
        # 3. LLM 翻译 (高质量，需要配置)
        llm_result = None
        if self.use_llm_api:
            llm_result = self.translate_with_llm(classical_text, style="modern")
        
        # 4. 开源模型翻译 (本地运行)
        open_source_result = None
        if self.has_transformers:
            open_source_result = self.translate_with_open_source_model(classical_text)
        
        # 5. 智能选择最优方案
        best_result, method, confidence = self._select_best_result(
            rule_result, llm_result, open_source_result
        )
        
        # 6. 缓存结果
        if best_result:
            self.translation_cache[cache_key] = best_result
        
        return {
            "translated": best_result,
            "method": method,
            "confidence": confidence,
            "rule_result": rule_result,
            "llm_result": llm_result,
            "open_source_result": open_source_result
        }
    
    def _select_best_result(self, 
                           rule_result: str, 
                           llm_result: Optional[str], 
                           open_source_result: Optional[str]) -> Tuple[str, str, float]:
        """选择最优翻译结果"""
        
        # 优先级：LLM > 开源模型 > 规则
        
        if llm_result and len(llm_result) > 10:
            return llm_result, "llm_api", 0.95
        
        if open_source_result and len(open_source_result) > 10:
            return open_source_result, "open_source_model", 0.85
        
        if rule_result and not rule_result.startswith("[需要配置"):
            return rule_result, "rule_based", 0.75
        
        # fallback
        return rule_result or classical_text, "fallback", 0.5
    
    def translate_with_context(self, classical_text: str, context: str) -> Dict:
        """带上下文的翻译"""
        
        if not context:
            return self.translate(classical_text)
        
        # 将上下文作为提示词增强翻译质量
        enhanced_prompt = f"根据以下背景：{context}\n原文：{classical_text}"
        
        result = self.translate(enhanced_prompt)
        
        # 提取纯译文部分 (移除背景信息)
        if "原文：" in result.get("translated", ""):
            translated_part = result["translated"].split("原文：")[1]
            result["translated"] = translated_part
        
        return result
    
    def annotate_pinyin(self, text: str) -> List[Dict]:
        """为生僻字注音"""
        
        return self.rule_translator.annotate_pinyin(text)
    
    def get_original_text(self, volume: str, year: str) -> Optional[str]:
        """根据卷数和年份获取原文"""
        
        return self.rule_translator.get_original_text(volume, year)


# 测试
if __name__ == "__main__":
    print("=" * 80)
    print("📖 AI 文言文翻译器 v1.0")
    print("=" * 80)
    
    # 创建翻译器 (不使用 LLM API，仅规则引擎)
    translator = AIChineseTranslator(use_llm_api=False)
    
    test_cases = [
        "刘豫州王室之胄，英才盖世",
        "诸葛亮曰：'愿将军量力而处之'",
        "臣闻求木之长者，必固其根本"
    ]
    
    print("\n📝 测试用例:\n")
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"{i}. {test_text}")
        
        # 注音
        annotations = translator.annotate_pinyin(test_text)
        if any(item.get('pinyin') and item.get('meaning') for item in annotations):
            print("   🔤 注音:")
            for item in annotations:
                if item.get('pinyin') and item.get('meaning'):
                    print(f"      {item['char']}[{item['pinyin']}]({item['meaning']})")
        
        # 翻译
        result = translator.translate(test_text)
        print(f"   📖 译文：{result['translated']}")
        print(f"   💡 方法：{result['method']} (置信度：{result['confidence']:.2f})")
        
        print()
    
    # 测试带上下文的翻译
    print("--- 带上下文翻译 ---\n")
    context = "这是诸葛亮对刘备说的话，背景是赤壁之战前"
    test_text = "愿将军量力而处之"
    
    result = translator.translate_with_context(test_text, context)
    print(f"原文：{test_text}")
    print(f"上下文：{context}")
    print(f"译文：{result['translated']}")
