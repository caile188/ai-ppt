# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from generator.markdown_parser import parse_markdown
from generator.ppt_generator import create_ppt
from generator.layout_manager import LayoutManager
from pptx import Presentation
import uuid
import os

OUTPUT_DIR = "static/output"
TEMPLATE_PATH = "templates/default.pptx"

def test():
    md_content = """
# AI大语言模型

## 目录
1. 什么是AI大语言模型
2. AI大语言模型的核心技术
3. 主要应用场景
4. 优势与挑战
5. 未来发展趋势
6. 总结与展望

## 什么是AI大语言模型
- 定义与背景
  - AI大语言模型是一种基于深度学习的自然语言处理技术，能够理解和生成人类语言。这类模型通常基于Transformer架构，通过海量文本数据的训练，具备强大的语言理解和生成能力。例如，GPT-3、BERT等模型在多个任务中表现出色，成为当前AI领域的热点。
- 发展历程
  - 从早期的统计语言模型到如今的深度学习模型，AI大语言模型经历了多次技术迭代。2017年Transformer架构的提出是关键转折点，随后GPT、BERT等模型的推出进一步推动了技术的发展，使得模型规模和数据量呈指数级增长。

## AI大语言模型的核心技术
- Transformer架构
  - Transformer是AI大语言模型的基础架构，其核心是自注意力机制（Self-Attention），能够高效捕捉文本中的长距离依赖关系。这种架构避免了传统RNN的序列处理限制，使得模型能够并行处理输入数据，大幅提升训练效率。
- 预训练与微调
  - 大语言模型通常采用两阶段训练：预训练和微调。预训练阶段通过无监督学习从海量文本中学习语言规律；微调阶段则针对特定任务进行有监督学习，使模型适应具体应用场景。

## 主要应用场景
- 自然语言生成
  - AI大语言模型能够生成高质量的自然语言文本，广泛应用于内容创作、对话系统、代码生成等领域。例如，ChatGPT可以用于客服机器人，帮助用户解决问题。
- 文本理解与分类
  - 模型能够理解文本的语义和情感，用于情感分析、文本摘要、信息检索等任务。BERT等模型在文本分类任务中表现出色，显著提升了准确率。

## 优势与挑战
- 优势
  - AI大语言模型具备强大的泛化能力，能够适应多种任务；同时，其生成能力为自动化内容创作提供了可能。此外，模型的开源和社区支持推动了技术的快速普及。
- 挑战
  - 模型训练需要巨大的计算资源和数据量，成本高昂；此外，模型可能生成偏见或错误内容，存在伦理和安全风险。如何平衡性能与资源消耗是当前的研究重点。

## 未来发展趋势
- 模型小型化
  - 未来研究将聚焦于如何在不损失性能的前提下减小模型规模，降低计算成本。例如，知识蒸馏和模型剪枝技术有望成为发展方向。
- 多模态融合
  - AI大语言模型将与其他模态（如图像、音频）结合，实现更复杂的多模态任务。例如，GPT-4已开始探索文本与图像的联合生成能力。

## 总结与展望
- 总结
  - AI大语言模型是当前自然语言处理领域的核心技术，其强大的语言理解和生成能力为多个行业带来了变革。然而，技术仍面临资源消耗和伦理问题等挑战。
- 展望
  - 随着技术的进步，AI大语言模型将更加高效和智能化，为人类社会带来更多创新应用。同时，行业需共同制定规范，确保技术的健康发展。
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
    # tt = "新能源汽车是指采用新型动力系统，完全或主要依靠电能或其他清洁能源驱动的汽车。随着全球对环境保护和能源安全的重视，新能源汽车逐渐成为汽车产业的重要发展方向。其核心目标是减少对传统化石燃料的依赖，降低碳排放，推动可持续发展。"
    # print(len(tt))





