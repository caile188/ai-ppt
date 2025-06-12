#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/6/6 18:46

from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class SlideContent:
    """
    表示幻灯片内容
    """
    title: str  # 幻灯片的标题
    presenter_name: str  # 主讲人
    agenda: List[str]  # 目录项
    closing: str
    bullet_points: List[dict] = field(default_factory=list)  # 文本内容及层级信息
    image_path: Optional[str] = None  # 图片路径，默认为 None



@dataclass
class Slide:
    """
    单页幻灯片
    """
    layout_id: int  # 布局 ID，对应 PowerPoint 模板中的布局
    layout_name: str  # 布局名称
    content: SlideContent  # 幻灯片的内容，类型为 SlideContent


@dataclass
class PowerPoint:
    """
    表示整个 PowerPoint 演示文稿，包括标题和幻灯片列表
    """
    title: str  # PowerPoint 演示文稿的标题
    slides: List[Slide] = field(default_factory=list)  # 幻灯片列表，默认为空列表