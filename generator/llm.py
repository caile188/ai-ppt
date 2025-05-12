#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/5/12 10:59
from typing import Annotated, TypedDict, Sequence
from langgraph.graph import StateGraph, START, END
from operator import add
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver


class AgentState(TypedDict):
    """
    定义状态结构
    """
    messages: Annotated[Sequence[HumanMessage | AIMessage], add]


def llm_node(state: AgentState):
    """
    定义节点函数：调用大模型，生成markdown
    :param state:
    :return:
    """
    chat_model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.5,
        max_tokens=4096
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", load_prompt()),
            ("human", "{input}")
        ]
    )

    chain = prompt | chat_model
    response = chain.invoke(state["messages"])
    return {"messages": [AIMessage(content=response.content)]}


def build_graph():
    # 创建一个状态图对象，传入状态定义
    graph_builder = StateGraph(AgentState)

    # 添加节点
    graph_builder.add_node("llm_node", llm_node)

    # 添加边
    graph_builder.add_edge(START, "llm_node")
    graph_builder.add_edge("llm_node", END)

    graph = graph_builder.compile(checkpointer=MemorySaver())

    return graph


def load_prompt():
    """
    从文件加载系统提示语。
    """
    with open("config/prompt.txt", "r", encoding="utf-8") as file:
        return file.read().strip()



