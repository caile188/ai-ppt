#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/4/30 11:05
from generator.llm import generate_markdown
from generator.markdown_parser import parse_markdown
from generator.ppt_generator import create_ppt
import uuid
import os
import gradio as gr

OUTPUT_DIR = "static/output"


def process_flow(topic):
    """完整处理流程"""
    # 生成Markdown
    md_content = generate_markdown(topic)

    # 解析结构
    slides = parse_markdown(md_content)

    # 生成PPT
    filename = f"{uuid.uuid4().hex[:6]}.pptx"
    output_path = os.path.join(OUTPUT_DIR, filename)
    create_ppt(slides, output_path)

    return md_content, output_path


# Gradio界面
with gr.Blocks(title="ChatPPT MVP") as demo:
    gr.Markdown("## ChatPPT - AI PPT生成助手")

    with gr.Row():
        topic_input = gr.Textbox(label="输入主题", placeholder="请输入PPT主题...")
        with gr.Column():
            md_output = gr.Code(label="生成内容", language="markdown")
            file_output = gr.File(label="下载PPT")

    submit_btn = gr.Button("生成PPT", variant="primary")

    submit_btn.click(
        fn=process_flow,
        inputs=topic_input,
        outputs=[md_output, file_output]
    )

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)


