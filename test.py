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
# 新能源汽车

## 新能源汽车的定义与分类
- 新能源汽车定义: 对使用一种或多种新型动力系统为动力来源的汽车的概述
  - 主要类型: 电动汽车、混合动力汽车、氢燃料电池汽车
    - 电动汽车（EV）: 仅使用电池电力
  - 分类使用的标准: 能源来源与驱动方式的不同
    - 全球各国的不同标准与定义

## 新能源汽车的发展历程
- 初期研究与发展: 20世纪初的初步发展与技术探索
  - 主要公司与科研机构的贡献
    - 特斯拉、丰田等公司在推动市场的案例
  - 技术的演进与瓶颈突破
- 政府支持与政策推动: 推动市场发展的关键因素
  - 国际政策与法规的制定
    - 例如：欧盟2025年电动车计划

## 新能源汽车的优势
- 环境影响: 减少碳排放与环境保护
  - 与传统燃油车的对比
    - 碳足迹的显著减少
  - 在城市内减少污染
- 经济效应: 长期的成本效益分析
  - 燃料与维护成本的降低
    - 长期使用中的耗费比较

## 新能源汽车面临的挑战
- 技术挑战: 电池技术与续航能力的限制
  - 充电速度与电池寿命问题
    - 研究中的潜在解决方案
  - 冬季使用的能效问题
- 基础设施: 充电网络的覆盖与普及
  - 不同地区充电桩的分布不均
    - 城市与乡村的服务可及性差异

## 新能源汽车的市场趋势
- 市场增长预测: 全球与地区市场的发展趋势
  - 当前市场份额与增长率
    - 市场调查数据支持
  - 新兴市场的机遇与挑战
- 创新与新品: 技术创新带来的新机遇
  - 无人驾驶技术与智能网联汽车的融合
    - 主要厂商的最新发布

## 未来展望与发展方向
- 可持续发展: 在可再生能源市场中的融合
  - 依赖太阳能、风能等清洁能源的可能性
    - 具体案例与试点项目
- 政策发展: 政府与商界的合作伙伴关系
  - 各国政策的持续支持与调整
    - 理想的政策框架和其实施效果
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
