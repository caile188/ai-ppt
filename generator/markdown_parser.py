#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author :le
# @Time : 2025/4/30 11:06
import re


def parse_markdown(md_text):
    """
    解析markdown,转为列表
    :param md_text:
    :return:
    """
    lines = md_text.split('\n')
    slides = []
    slide = {}
    bullet_pattern = re.compile(r'^(\s*)-\s+(.*)')

    for line in lines:
        # 主标题
        if line.startswith('# ') and not line.startswith('##'):
            first_slide = {'title': line.strip('# ').strip(), 'bullets': []}
            slides.append(first_slide)

        elif line.startswith('## '):
            if slide:
                slides.append(slide)
            slide = {'title': line.strip('## ').strip(), 'bullets': []}

        elif bullet_pattern.match(line) and slide:
            match = bullet_pattern.match(line)

            if match:
                indent_spaces, bullet = match.groups()  # 获取缩进空格和项目符号内容
                indent_level = len(indent_spaces) // 2  # 计算缩进层级，每 2 个空格为一级
                bullet_text = bullet.strip()  # 获取项目符号的文本内容

                # 根据层级添加要点
                slide['bullets'].append({"text": bullet_text, "level": indent_level})

    if slide:
        slides.append(slide)

    return slides