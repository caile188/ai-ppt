# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from generator.markdown_parser import parse_markdown
from generator.ppt_generator import create_ppt
from generator.layout_manager import LayoutManager
from pptx import Presentation
import uuid
import os

from util.log_manager import log_manager
from config import setting

logger = log_manager.get_logger(__name__)
logger.info("log test")

OUTPUT_DIR = "static/output/pptx"
TEMPLATE_PATH = "templates/default.pptx"

def test():
    md_content = """
# 黑洞：宇宙的神秘深渊

## 目录
1. 黑洞的定义与基本概念
2. 黑洞的形成过程
3. 黑洞的类型与分类
4. 黑洞的观测与发现
5. 黑洞对宇宙的影响
6. 黑洞研究的未来展望

## 黑洞的定义与基本概念
![黑洞的定义与基本概念](static/output/images/黑洞的定义与基本概念_1.jpeg)
- **什么是黑洞？**
  - 黑洞是宇宙中一种极其致密的天体，其引力强大到连光都无法逃脱。根据爱因斯坦的广义相对论，黑洞是由质量极大的恒星在生命末期坍缩形成的。黑洞的核心被称为“奇点”，其密度无限大，体积无限小，周围被“事件视界”包围，任何进入事件视界的物质都无法返回。
- **黑洞的基本特性**
  - 黑洞具有三个基本特性：质量、电荷和角动量。质量决定了黑洞的引力大小，电荷和角动量则影响黑洞周围的时空结构。黑洞的行为可以通过“无毛定理”来描述，即黑洞的外部特性仅由这三个参数决定。

## 黑洞的形成过程
![黑洞的形成过程](static/output/images/黑洞的形成过程_1.jpeg)
- **恒星坍缩**
  - 黑洞通常由大质量恒星（质量超过太阳的20倍）在生命末期坍缩形成。当恒星耗尽核燃料时，引力压倒内部压力，导致恒星核心坍缩。如果核心质量足够大，它会继续坍缩，最终形成黑洞。
- **超新星爆发**
  - 在恒星坍缩过程中，外层物质会被剧烈抛射，形成超新星爆发。这一过程释放出巨大的能量，同时为黑洞的形成提供了条件。超新星爆发是宇宙中最壮观的现象之一。

## 黑洞的类型与分类
- **按质量分类**
  - 黑洞可分为三类：恒星质量黑洞（质量约为太阳的几倍到几十倍）、中等质量黑洞（质量约为太阳的几百到几千倍）和超大质量黑洞（质量可达太阳的百万甚至数十亿倍）。超大质量黑洞通常位于星系中心。
- **按旋转分类**
  - 黑洞还可以根据其旋转状态分为静态黑洞（不旋转）和旋转黑洞（具有角动量）。旋转黑洞的时空结构更为复杂，周围会形成“能层”。

## 黑洞的观测与发现
![黑洞的观测与发现](static/output/images/黑洞的观测与发现_1.jpeg)
- **间接观测方法**
  - 由于黑洞本身不发光，科学家通过观测黑洞对周围物质的影响来间接探测它们。例如，黑洞吸积盘中的物质在落入黑洞前会释放X射线，这些信号可以被望远镜捕捉。
- **直接成像**
  - 2019年，事件视界望远镜（EHT）成功拍摄到M87星系中心超大质量黑洞的“阴影”图像，这是人类首次直接“看到”黑洞，为黑洞研究提供了直接证据。

## 黑洞对宇宙的影响
- **星系演化**
  - 超大质量黑洞对宿主星系的演化具有重要影响。它们通过吸积物质释放巨大能量，调节星系中的恒星形成速率，甚至可能阻止星系的进一步增长。
- **引力波**
  - 黑洞合并是引力波的主要来源之一。2015年，LIGO首次探测到双黑洞合并产生的引力波，开启了引力波天文学的新时代。

## 黑洞研究的未来展望
- **更深入的观测**
  - 未来，随着望远镜技术的进步，科学家有望观测到更多黑洞的细节，例如黑洞的磁场结构以及更小质量的黑洞。
- **理论突破**
  - 黑洞研究可能为统一广义相对论和量子力学提供线索。黑洞信息悖论等未解之谜的解决，将推动物理学的前沿发展。
    """

    # 加载 PowerPoint 模板，并获取可用布局
    prs = Presentation(TEMPLATE_PATH)
    layout_mapping = {}
    for idx, layout in enumerate(prs.slide_layouts):
        layout_mapping[layout.name] = idx


    # 解析 markdown，获取 powerpoint 格式信息
    powerpoint_data = parse_markdown(md_content, LayoutManager(layout_mapping))
    print(powerpoint_data)

    # 生成PPT
    filename = f"{uuid.uuid4().hex[:6]}.pptx"
    output_path = os.path.join(OUTPUT_DIR, filename)
    create_ppt(powerpoint_data, TEMPLATE_PATH, output_path)

    print(output_path)


if __name__ == '__main__':

    test()





