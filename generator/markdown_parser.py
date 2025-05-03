#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author :le
# @Time : 2025/4/30 11:06


def parse_markdown(md_text):
    """
    解析markdown,转为列表
    :param md_text:
    :return:
    """
    lines = md_text.strip().split('\n')
    slides = []
    slide = {}
    for line in lines:
        if line.startswith('#'):
            if slide:
                slides.append(slide)
            slide = {'title': line.strip('# ').strip(), 'bullets': []}
        elif line.startswith('-'):
            slide['bullets'].append(line.strip('- ').strip())
    if slide:
        slides.append(slide)
    return slides