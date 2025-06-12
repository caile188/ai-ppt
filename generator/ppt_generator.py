#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/4/30 11:06

from pptx import Presentation


def create_ppt(powerpoint_data, template_path, output_path):
    """根据解析结果生成PPTX文件"""
    prs = Presentation(template_path)
    prs.core_properties.title = powerpoint_data.title  # 设置 PowerPoint 的核心标题

    for slide_data in powerpoint_data.slides:
        slide_layout = prs.slide_layouts[slide_data.layout_id]
        new_slide = prs.slides.add_slide(slide_layout)

        # 设置幻灯片标题
        if new_slide.shapes.title:
            if slide_data.content.title:
                new_slide.shapes.title.text = slide_data.content.title
            elif slide_data.content.closing:
                new_slide.shapes.title.text = slide_data.content.closing

        # 设置文本内容
        for shape in new_slide.shapes:
            if shape.has_text_frame and not shape == new_slide.shapes.title:
                tf = shape.text_frame
                tf.clear()
                first_paragraph = tf.paragraphs[0]
                if slide_data.content.presenter_name:  # 设置主讲人
                    first_paragraph.level = 0
                    format_text(first_paragraph, slide_data.content.presenter_name)

                for item in slide_data.content.agenda:  # 设置目录
                    # 第一个要点覆盖初始段落，其他要点添加新段落
                    p = first_paragraph if item == slide_data.content.agenda[0] else tf.add_paragraph()
                    p.level = 0
                    format_text(p, item)  # 调用 format_text 方法来处理加粗文本

                for item in slide_data.content.bullet_points:  # 设置要点及详细阐述
                    p = first_paragraph if item == slide_data.content.bullet_points[0] else tf.add_paragraph()
                    p.level = item["level"]
                    format_text(p, item["text"])  # 调用 format_text 方法来处理加粗文本

                break

    prs.save(output_path)


def format_text(paragraph, text):
    """
    格式化文本，处理加粗内容，** 包围的文本表示需要加粗。
    """
    while '**' in text:
        start = text.find('**')
        end = text.find('**', start + 2)

        if start != -1 and end != -1:
            # 添加加粗之前的普通文本
            if start > 0:
                run = paragraph.add_run()
                run.text = text[:start]

            # 添加加粗文本
            bold_run = paragraph.add_run()
            bold_run.text = text[start + 2:end]
            bold_run.font.bold = True  # 设置加粗

            # 处理剩余文本
            text = text[end + 2:]
        else:
            break

    # 添加剩余的普通文本
    if text:
        run = paragraph.add_run()
        run.text = text