#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/6/17 15:05

from util.log_manager import log_manager
from util.load_prompt import load_prompt
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from config import setting

from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import os
import json
import re


class ImageManager:

    def __init__(self, slide_content, chat_model):
        self.logger = log_manager.get_logger(__name__)
        self.slide_content = slide_content
        self.prompt_file_path = setting.IMAGE_PROMPT_PATH
        self.output_image_dir = setting.IMAGE_OUTPUT_DIR
        self.model_dict = setting.MODEL_LIST[chat_model]

    def get_slide_keywords(self):
        """
        调用大模型，根据 slideContent 获取随机幻灯片与其关键字映射关系
        使用结构化输出确保 JSON 格式。
        :return:
        """

        chat_model = init_chat_model(
            f"{self.model_dict['model_provider']}:{self.model_dict['model_name']}",
            temperature=0.5,
            max_tokens=4096
        )

        prompt = ChatPromptTemplate(
            [
                ("system", load_prompt(self.prompt_file_path)),
                ("human", "{input}")
            ]
        )


        # 使用openai代理api，暂不支持此解析方式，改为手动解析
        # chain = prompt | chat_model.with_structured_output(method="json_mode")

        chain = prompt | chat_model
        response = chain.invoke({"input": self.slide_content})
        final_response = self.parser_output(response.content)
        return final_response

    def configure_images(self):
        """
        智能配图
        获取图片并嵌入到 PowerPoint 内容中。
        :return:
        """

        slide_keyword_map = self.get_slide_keywords()
        self.logger.info(f"[建议配图]\n{slide_keyword_map}")

        image_pair = {}
        for slide_title, keyword in slide_keyword_map.items():
            images = self.get_bing_images(slide_title, keyword)
            if not images:
                self.logger.warning(f"No images found for {slide_title}.")
                continue
            else:
                for image in images:
                    self.logger.info(f"Name: {image['slide_title']}, Query: {image['query']} 分辨率：{image['width']}x{image['height']}")

            # 仅处理分辨率最高的图像，保存图像到本地
            img = images[0]
            os.makedirs(self.output_image_dir, exist_ok=True)
            save_path = os.path.join(self.output_image_dir, f"{img['slide_title']}_1")
            final_save_path = self.save_image(img["obj"], save_path)
            if final_save_path:
                image_pair[img["slide_title"]] = final_save_path

        content_with_images = self.insert_images_to_content(image_pair)
        return content_with_images

    def get_bing_images(self, slide_title, query, num_images=5, timeout=5, retries=3):
        """
        从 Bing 检索图像，最多重试3次。
        :param slide_title:
        :param query:
        :param num_images:
        :param timeout:
        :param retries:
        :return:
        """
        url = f"https://www.bing.com/images/search?q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

        # 发送请求，并设置重试逻辑
        for i in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                break  # 请求成功，跳出重试循环
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {i + 1}/{retries} failed for query '{query}': {e}")
                if i == retries - 1:
                    self.logger.error(f"Max retries reached for query '{query}'.")
                    return []

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 使用 CSS 选择器查找图像元素
        image_elements = soup.select("a.iusc")

        # 提取图像链接
        image_links = []
        for img in image_elements:
            m_data = img.get("m")
            if m_data:
                m_json = json.loads(m_data)
                if "murl" in m_json:
                    image_links.append(m_json["murl"])
            if len(image_links) >= num_images:
                break

        # 获取图像的分辨率并存储为字典
        image_data = []
        for link in image_links:
            try:
                img_data = requests.get(link, headers=headers)
                img = Image.open(BytesIO(img_data.content))
                image_info = {
                    "slide_title": slide_title,
                    "query": query,
                    "width": img.width,
                    "height": img.height,
                    "resolution": img.width * img.height,  # 宽度 x 高度
                    "obj": img,
                }
                image_data.append(image_info)

            except Exception as e:
                self.logger.error(f"获取图片失败 {link}: {e}")

        # 按分辨率从大到小排序
        sorted_images = sorted(image_data, key=lambda x: x["resolution"], reverse=True)
        return sorted_images

    def save_image(self, img_obj, save_path, format="JPEG", quality=85, max_size=1080):
        """
        调整图片分辨率，并将图片保存到本地
        :param img_obj:
        :param save_path:
        :param format:
        :param quality:
        :param max_size:
        :return:
        """

        final_save_path = ""

        try:
            # 调整分辨率，保持长宽比
            width, height = img_obj.size
            if max(width, height) > max_size:
                scaling_factor = max_size / max(width, height)
                new_width = int(width * scaling_factor)
                new_height = int(height * scaling_factor)
                img_obj = img_obj.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 默认后缀为 .jpeg
            file_extension = "jpeg"

            if img_obj.mode == "P":
                img_obj = img_obj.convert("RGB")
                format = "JPEG"  # 确保格式设置为JPEG，因为我们已经转换成RGB

            if img_obj.mode == "RGBA":
                format = "PNG"
                save_options = {
                    "optimize": True  # 启用优化以减小文件大小
                }
                file_extension = "png"
            else:
                save_options = {
                    "quality": quality,  # 设置图像质量
                    "optimize": True,
                    "progressive": True  # 使用渐进式加载
                }

            # 保存图像
            final_save_path = f"{save_path}.{file_extension}"
            img_obj.save(final_save_path, format=format, **save_options)
            self.logger.info(f"Image saved as {final_save_path} in {format} format with quality {quality}.")

        except Exception as e:
            self.logger.error(f"Failed to save image: {e}")

        return final_save_path

    def insert_images_to_content(self, image_pair):
        """
        将图像嵌入到 Markdown 内容中。
        :param slide_content:
        :param image_pair:
        :return:
        """
        lines = self.slide_content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            # 检查是否为幻灯片标题行（以 '## ' 开头）
            if line.startswith('## '):
                # 提取幻灯片标题
                slide_title = line[3:].strip()
                # 如果幻灯片标题在 image_pair 中，插入对应的图像
                if slide_title in image_pair:
                    image_path = image_pair[slide_title]
                    # 按照 Markdown 图像格式插入
                    image_markdown = f'![{slide_title}]({image_path})'
                    new_lines.append(image_markdown)
            i += 1
        # 将修改后的内容重新组合为字符串
        new_content = '\n'.join(new_lines)
        return new_content

    def parser_output(self, content):
        self.logger.info(f"[模型生成slide及其关键字为：] {content}")

        # --- START: 添加 JSON 提取和解析逻辑 ---
        json_string_match = re.search(r"```json\s*(\{.*\})\s*```", content, re.DOTALL)

        if json_string_match:
            extracted_json_content = json_string_match.group(1)
            final_response = json.loads(extracted_json_content)
        else:
            # 如果没有匹配到 ```json 块，尝试直接解析整个 content
            final_response = json.loads(content)

        return final_response
