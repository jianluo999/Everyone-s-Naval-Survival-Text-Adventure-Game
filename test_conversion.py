#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试人称转换功能
"""

import re

def test_convert_text(text):
    """测试转换函数"""
    print(f"原文: {text}")
    
    # 保护引号内容
    protected_parts = []
    quote_pattern = r'"[^"]*"'
    quotes = re.findall(quote_pattern, text)
    converted_text = text
    
    for i, quote in enumerate(quotes):
        placeholder = f"__QUOTE_{i}__"
        converted_text = converted_text.replace(quote, placeholder, 1)
        protected_parts.append((placeholder, quote))
        print(f"保护引号: {quote} -> {placeholder}")
    
    print(f"保护后: {converted_text}")
    
    # 应用转换规则（中文环境下不使用\b边界）
    basic_rules = [
        (r'我(?![的们])', '你'),  # 匹配"我"但不是"我的"或"我们"
        (r'我的', '你的'),
        (r'我们', '你们'),
        (r'我们的', '你们的'),
    ]
    
    for pattern, replacement in basic_rules:
        old_text = converted_text
        converted_text = re.sub(pattern, replacement, converted_text)
        if old_text != converted_text:
            print(f"应用规则 {pattern} -> {replacement}: {old_text} -> {converted_text}")
    
    # 恢复引号内容
    for placeholder, original in protected_parts:
        converted_text = converted_text.replace(placeholder, original)
        print(f"恢复引号: {placeholder} -> {original}")
    
    print(f"最终结果: {converted_text}")
    print("-" * 50)
    return converted_text

# 测试用例
test_cases = [
    '我开始竟然站了，这简直是奇迹！',
    '海风轻抚着我的脸庞，带来咸腥的味道。',
    '"这声音说的....是真的！"我自语着说。',
    '环顾四周，我发现我在一处狭窄昏暗的破房子里。',
    '我看完属性界面，稍微安心。',
]

for test_case in test_cases:
    test_convert_text(test_case)
