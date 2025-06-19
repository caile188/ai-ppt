#!/usr/bin/python3
# -*- coding: utf-8 -*-            
# @Author :le
# @Time : 2025/6/18 12:00

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHATBOT_PROMPT_PATH = "config/prompt.txt"
IMAGE_PROMPT_PATH = "config/image_prompt.txt"
PPTX_OUTPUT_DIR = "static/output/pptx"
IMAGE_OUTPUT_DIR = "static/output/images"
TEMPLATE_PATH = "templates/default.pptx"

MODEL_LIST = {
  "deepseek-v3": {
    "model_provider": "deepseek",
    "model_name": "deepseek-chat"
  }
}

LOGGING = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "standardFormatter": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    }
  },
  "handlers": {
    "consoleHandler": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "standardFormatter",
      "stream": "ext://sys.stdout"
    },
    "fileHandler": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "INFO",
      "formatter": "standardFormatter",
      "filename": "logs/application.log",
      "mode": "a",
      "maxBytes": 5 * 1024 * 1024,
      "backupCount": 3,
      "encoding": "utf-8"
    }
  },
  "loggers": {
    "main_app": {
      "level": "DEBUG",
      "handlers": ["consoleHandler", "fileHandler"],
      "propagate": False
    }
  },
  "root": {
    "level": "DEBUG",
    "handlers": ["consoleHandler", "fileHandler"]
  }
}
