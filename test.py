# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from generator.markdown_parser import parse_markdown
from generator.ppt_generator import create_ppt
import uuid
import os

OUTPUT_DIR = "static/output"

def test():
    md_content = """
# 黑洞

## 目录
- 章节1: 黑洞的定义与形成
- 章节2: 黑洞的性质与分类
- 章节3: 黑洞的研究现状与未来

## 章节1: 黑洞的定义与形成
- **要点1:** 黑洞是一个引力极强的天体，任何物质和光线都无法逃脱其引力。
- **要点2:** 黑洞的形成通常源于大质量恒星的引力坍缩，特别是在超新星爆炸后。

## 章节2: 黑洞的性质与分类
- **要点1:** 黑洞主要分为三种类型：恒星黑洞、超大质量黑洞和中等质量黑洞。
- **要点2:** 黑洞的事件视界是其边界，超出这一界限的物质无法返回。

## 章节3: 黑洞的研究现状与未来
- **要点1:** 当前，科学家通过引力波探测器和事件视界望远镜等技术研究黑洞。
- **要点2:** 未来的研究可能揭示黑洞与宇宙早期状态及暗物质的关系。

## 总结
- **总结要点1:** 黑洞是宇宙中极端的天体，具有独特的引力特性。
- **总结要点2:** 对黑洞的研究不仅有助于理解宇宙的演化，还可能解开许多物理学的未解之谜。
    """

    slides = parse_markdown(md_content)

    # 生成PPT
    filename = f"{uuid.uuid4().hex[:6]}.pptx"
    output_path = os.path.join(OUTPUT_DIR, filename)
    create_ppt(slides, output_path)

    print(md_content, output_path)

if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
