#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/6/18 14:58

def load_prompt(prompt_path: str):
    """
    从文件加载系统提示语。
    """
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read().strip()