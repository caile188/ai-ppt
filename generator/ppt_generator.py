#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/4/30 11:06

from pptx import Presentation


TEMPLATE_PATH = "templates/default.pptx"


def create_ppt(slides, output_path):
    """根据解析结果生成PPTX文件"""
    prs = Presentation(TEMPLATE_PATH)

    # 标题页
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = slides[0]['title']

    # 内容页
    for slide_data in slides[1:]:
        slide = prs.slides.add_slide(prs.slide_layouts[1])

        # 设置标题
        title_box = slide.shapes.title
        title_box.text = slide_data['title']

        # 设置内容
        for shape in slide.shapes:
            if shape.has_text_frame and not shape == title_box:
                tf = shape.text_frame
                tf.clear()

                for item in slide_data['bullets']:
                    p = tf.add_paragraph()
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