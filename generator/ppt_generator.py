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
                    p.text = item

                break

    prs.save(output_path)