#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author :le
# @Time : 2025/4/30 11:06
import re
from typing import Optional
from generator.ppt_data_structure import PowerPoint
from generator.slide_builder import SlideBuilder
from generator.layout_manager import LayoutManager


def parse_markdown(md_text: str, layout_manager: LayoutManager):
    """
    解析markdown, 生成 PowerPoint 数据结构
    :param md_text:
    :param layout_manager:
    :return:
    """
    lines = md_text.split('\n')
    presentation_title = ""  # PowerPoint 的主标题
    slides = []
    slide_builder: Optional[SlideBuilder] = None  # 当前幻灯片的构建器
    bullet_pattern = re.compile(r'^(\s*)-\s+(.*)')
    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')


    for line in lines:

        if line.strip() == "":
            continue  # 跳过空行

        # 主标题
        if line.startswith('# ') and not line.startswith('##'):
            presentation_title = line.strip('# ').strip()
            first_slide_builder = SlideBuilder(layout_manager)
            first_slide_builder.set_title(presentation_title)
            first_slide_builder.set_presenter_name("主讲人：xxx")
            slides.append(first_slide_builder.finalize())

        elif line.startswith('## '):  # 插入标题
            if slide_builder:
                slides.append(slide_builder.finalize())

            # 创建新的 SlideBuilder
            slide_builder = SlideBuilder(layout_manager)
            slide_builder.set_title(line.strip('## ').strip())

        elif re.match(r'^\d\.', line) and slide_builder:  # 插入目录项
            slide_builder.add_agenda(line)

        elif bullet_pattern.match(line) and slide_builder:  # 插入文本内容
            match = bullet_pattern.match(line)

            if match:
                indent_spaces, bullet = match.groups()  # 获取缩进空格和项目符号内容
                indent_level = len(indent_spaces) // 2  # 计算缩进层级，每 2 个空格为一级
                bullet_text = bullet.strip()  # 获取项目符号的文本内容

                # 根据层级添加要点
                slide_builder.add_bullet_point(bullet_text, level=indent_level)

        elif line.startswith('![') and slide_builder:  # 插入图片
            match = image_pattern.match(line)
            if match:
                image_path = match.group(1).strip()
                slide_builder.set_image(image_path)

    if slide_builder:
        slides.append(slide_builder.finalize())

    # 插入结束页
    closing_slide_builder = SlideBuilder(layout_manager)
    closing_slide_builder.set_closing("Thank you")
    slides.append(closing_slide_builder.finalize())

    return PowerPoint(title=presentation_title, slides=slides)
