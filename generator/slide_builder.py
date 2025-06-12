#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/6/6 18:54
from generator.ppt_data_structure import SlideContent, Slide
from generator.layout_manager import LayoutManager


class SlideBuilder:
    """
    构建单页幻灯片，并通过 LayoutManager 自动分配布局
    """
    def __init__(self, layout_manager: LayoutManager):
        self.layout_manager = layout_manager  # 布局管理器实例
        self.layout_id = None  # 布局id
        self.layout_name = None  # 布局名称
        self.title = ""  # 幻灯片标题
        self.presenter_name = "" # 主讲人
        self.agenda = []  # 目录项
        self.bullet_point = []  # 幻灯片内容列表，支持多级结构
        self.image_path = None  # 幻灯片中图片路径
        self.closing = ""  # 幻灯片结束语

    def set_title(self, title: str):
        self.title = title

    def set_presenter_name(self, presenter_name: str):
        self.presenter_name = presenter_name

    def add_agenda(self, point: str):
        self.agenda.append(point)

    def add_bullet_point(self, bullet: str, level: int = 0):
        self.bullet_point.append({
            "text": bullet,
            "level": level
        })

    def set_image(self, image_path: str):
        self.image_path = image_path

    def set_closing(self, closing: str):
        self.closing = closing

    def finalize(self) -> Slide:
        content = SlideContent(
            title=self.title,
            presenter_name=self.presenter_name,
            agenda=self.agenda,
            bullet_points=self.bullet_point,
            image_path=self.image_path,
            closing=self.closing
        )

        # 调用 LayoutManager 分配布局
        self.layout_id, self.layout_name = self.layout_manager.assign_layout(content)

        # 返回 Slide 对象
        return Slide(layout_id=self.layout_id, layout_name=self.layout_name, content=content)