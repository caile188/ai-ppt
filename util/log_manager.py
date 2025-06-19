#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/6/18 11:13

import logging
import logging.config
from config import setting
import os


class LogManager:
    """
    统一日志管理类，采用单例模式，通过 JSON 配置文件进行配置。
    """
    _instance = None  # 用于存储单例实例

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化日志管理器，从 JSON 配置文件加载日志配置。
        """
        if hasattr(self, '_initialized') and self._initialized:
            return  # 避免重复初始化

        self._initialized = True
        self.config = setting.LOGGING
        self._setup_logging()

    def _setup_logging(self):
        """
        加载并应用日志配置
        """
        # try:


        # 额外处理：如果配置文件中指定了日志文件路径，确保其目录存在
        for handler_name, handler_config in self.config.get('handlers', {}).items():
            if 'filename' in handler_config:
                log_dir = os.path.dirname(handler_config['filename'])
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)

        logging.config.dictConfig(self.config)

        # except Exception as e:
        #     print(">>>>>>>>>>>>>error")
        #     print(str(e))
        #     logging.basicConfig(level=logging.INFO,
        #                         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self, name: str = __name__) -> logging.Logger:
        """
        获取一个具名 Logger 实例。
        """
        return logging.getLogger(name)


log_manager = LogManager()


