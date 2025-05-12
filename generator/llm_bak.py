#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/4/30 11:06

from openai import OpenAI


def generate_markdown(user_input):
    """调用LLM生成结构化Markdown"""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": load_prompt()

            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    return response.choices[0].message.content


def load_prompt():
    """
    从文件加载系统提示语。
    """
    with open("config/prompt.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


