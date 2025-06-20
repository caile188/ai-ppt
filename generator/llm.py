#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/5/12 10:59
from typing import Annotated, TypedDict, Sequence, Literal
from langgraph.graph import StateGraph, START, END
from operator import add
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chat_models import init_chat_model
from config import setting
from util.load_prompt import load_prompt


class AgentState(TypedDict):
    """
    定义状态结构
    """
    messages: Annotated[Sequence[BaseMessage], add]
    chat_model: str


class ToolManager:
    """
    tools 管理
    """

    @staticmethod
    def get_tools():
        """初始化并返回所有工具"""
        return [
            TavilySearchResults(max_results=2),
        ]


def llm_node(state: AgentState):
    """
    定义节点函数：调用大模型，生成markdown
    :param state:
    :return:
    """

    model_dict = setting.MODEL_LIST[state['chat_model']]
    model_obj = init_chat_model(
        f"{model_dict['model_provider']}:{model_dict['model_name']}",
        temperature=0.5,
        max_tokens=4096
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", load_prompt(setting.CHATBOT_PROMPT_PATH)),
            ("human", "{input}")
        ]
    )

    tools = ToolManager.get_tools()

    chain = prompt | model_obj.bind_tools(tools)
    response = chain.invoke(state["messages"])
    return {"messages": [response]}


def router(state: AgentState) -> Literal["tool_node", "__end__"]:
    """
    定义路由函数，检查工具调用
    使用条件边来检查最后一条消息中是否有工具调用。
    :param state: 状态字典或消息列表，用于存储当前对话的状态和消息
    :return:
    如果最后一条消息包含工具调用，返回 "tool_node" 节点，表示需要执行工具调用；
    否则返回 "__end__"，表示直接结束流程。
    """

    if isinstance(state, list):
        ai_message = state[-1]
    elif message := state.get("messages", []):
        ai_message = message[-1]
    else:
        raise ValueError(f"输入状态中未找到消息：{state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tool_node"
    return END


def build_graph():
    # 创建一个状态图对象，传入状态定义
    graph_builder = StateGraph(AgentState)

    tool_node = ToolNode(ToolManager.get_tools())

    # 添加节点
    graph_builder.add_node("llm_node", llm_node)
    graph_builder.add_node("tool_node", tool_node)

    # 添加边
    graph_builder.add_edge(START, "llm_node")
    graph_builder.add_conditional_edges("llm_node", router)
    graph_builder.add_edge("tool_node", "llm_node")

    graph = graph_builder.compile(checkpointer=MemorySaver())

    return graph



