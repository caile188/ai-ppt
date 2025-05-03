#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/4/30 11:06

from openai import OpenAI

# 固定Markdown生成模板
PROMPT_TEMPLATE = """请根据以下主题生成PPT内容，使用严格规范的Markdown格式：
# 主标题
## 目录
- 章节1
- 章节2 
- 章节3

## 章节1
- 要点1
- 要点2

## 章节2
- 要点1 
- 要点2

## 总结
- 总结要点1
- 总结要点2

当前主题：{topic}"""


def generate_markdown(topic):
    """调用LLM生成结构化Markdown"""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": PROMPT_TEMPLATE.format(topic=topic)
        }]
    )
    return response.choices[0].message.content

