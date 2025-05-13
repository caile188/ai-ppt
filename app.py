#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/4/30 11:05
from generator.llm import build_graph
from generator.markdown_parser import parse_markdown
from generator.ppt_generator import create_ppt
from langchain_core.messages import HumanMessage
import uuid
import os
import gradio as gr

OUTPUT_DIR = "static/output"

# 全局图对象（避免重复构建）
GRAPH = build_graph()


def process_flow(user_input, history, session_id: str):
    """完整处理流程"""

    # 生成Markdown
    result = GRAPH.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={
            "configurable": {
                "thread_id": f"thread_{session_id}"
            }
        }
    )
    # 提取最新生成的 AI 消息内容
    md_content = result["messages"][-1].content

    return md_content


def handle_generate(history):
    """
    生成ppt
    :param history:
    :return:
    """
    md_content = history[-1]["content"]
    slides = parse_markdown(md_content)
    # 生成PPT
    filename = f"{uuid.uuid4().hex[:6]}.pptx"
    output_path = os.path.join(OUTPUT_DIR, filename)
    create_ppt(slides, output_path)
    return output_path


def generator_session():
    return str(uuid.uuid4())


# Gradio界面
with gr.Blocks(title="AiPPT") as demo:

    session_id = gr.State(value=generator_session)  # 会话状态存储
    gr.Markdown("## AiPPT - PPT生成助手")

    with gr.Row():
        with gr.Column(scale=2):

            # 创建聊天机器人
            chatbot = gr.Chatbot(
                placeholder="AI 一键生成 PPT：请输入主题或详细描述",
                height=500,
                type="messages",
            )
            gr.ChatInterface(
                fn=process_flow,  # 处理用户输入的函数
                additional_inputs=[session_id],
                chatbot=chatbot,  # 绑定的聊天机器人
                type="messages"
            )

            # 创建生成 PowerPoint 的按钮
            generate_btn = gr.Button("一键生成 PowerPoint", variant="stop")

        with gr.Column(scale=1):
            # 监听生成按钮的点击事件
            generate_btn.click(
                fn=handle_generate,  # 点击时执行的函数
                inputs=chatbot,  # 输入为聊天记录
                outputs=gr.File(label="文件下载")  # 输出为文件下载链接
            )

    # 页面加载时刷新会话ID
    demo.load(
        fn=generator_session,
        outputs=[session_id],
        queue=False
    )


if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)


