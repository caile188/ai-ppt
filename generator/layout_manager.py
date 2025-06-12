#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/6/6 18:52

import random
from typing import List, Tuple, Dict
from generator.ppt_data_structure import SlideContent

# 定义 content_type 对应的权重
CONTENT_TYPE_WEIGHTS = {
    'Title': 1,
    'Content': 2,
    'Photo': 4,
    'Agenda': 8,
    'Closing': 16

}


class LayoutManager:
    """
    布局管理器：
    根据
    """
    def __init__(self, layout_mapping: dict):
        self.layout_mapping = layout_mapping  # layout_name 与 layout_id 映射关系
        self.strategies: Dict[int, List[Tuple[int, str]]] = {}
        self._initialize_strategies()  # 初始化策略

    def _initialize_strategies(self):
        """
        根据 layout_mapping 动态初始化布局策略。
        将布局按其内容编码分组。
        :return:
        """
        layouts_by_encoding: Dict[int, List[Tuple[int, str]]] = {}

        for layout_name, layout_id in self.layout_mapping.items():
            encoding = self.calculate_layout_encoding(layout_name)
            if encoding not in layouts_by_encoding:
                layouts_by_encoding[encoding] = []
            layouts_by_encoding[encoding].append((layout_id, layout_name))

        # 为每个唯一编码创建 LayoutStrategy 实例
        for encoding, layout_group in layouts_by_encoding.items():
            self.strategies[encoding] = layout_group

    def assign_layout(self, slide_content: SlideContent) -> Tuple[int, str]:
        """
        根据 SlideContent 的成员情况计算编码，并从对应布局策略组中获取 layoyt
        :param slide_content:
        :return:
        """

        # 计算 SlideContent 的编码
        content_encoding = self.calculate_content_encoding(slide_content)

        # 根据编码获取对应的布局组
        layout_group = self.strategies.get(content_encoding)
        if not layout_group:
            raise ValueError(f"没有找到内容编码 {content_encoding} 的布局组。")

        # 从对应布局组中选择一个布局并返回
        return random.choice(layout_group)

    def calculate_layout_encoding(self, layout_name: str) -> int:
        """
        根据布局名称计算其编码值
        :param layout_name:
        :return:
        """
        weight_sum = 0

        # layout_name 示例：Title_Content 0
        type_list = layout_name.split(' ')[0].split('_')
        if 'Blank' in type_list:
            return weight_sum
        for type in type_list:
            weight_sum += CONTENT_TYPE_WEIGHTS[type]
        return weight_sum

    def calculate_content_encoding(self, slide_content: SlideContent) -> int:
        """
        根据 SlideContent 成员，计算该 slide 的编码
        :param slide_content:
        :return:
        """
        weight_sum = 0
        if slide_content.title:
            weight_sum += CONTENT_TYPE_WEIGHTS['Title']
        if slide_content.agenda:
            weight_sum += CONTENT_TYPE_WEIGHTS['Agenda']
        if slide_content.bullet_points:
            weight_sum += CONTENT_TYPE_WEIGHTS['Content']
        if slide_content.image_path:
            weight_sum += CONTENT_TYPE_WEIGHTS['Photo']
        if slide_content.closing:
            weight_sum += CONTENT_TYPE_WEIGHTS['Closing']

        return weight_sum

    def __str__(self):
        """
        打印 LayoutManager 的调试信息，包括所有布局策略及其对应的布局组。
        :return:
        """
        output = []
        output.append("LayoutManager 状态：")
        if not self.strategies:
            output.append(" 没有初始化任何策略")
            return "\n".join(output)

        for encoding, layout_group in self.strategies.items():
            output.append(f"  编码 {encoding}: {len(layout_group)} 个布局")
            for layout_id, layout_name in layout_group:
                output.append(f"    - 布局 ID: {layout_id}, 布局名称: {layout_name}")
        return "\n".join(output)

