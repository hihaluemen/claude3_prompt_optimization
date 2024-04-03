#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/3 11:28
# @Author  : hihaluemen
# @File    : config.py


ANTHROPIC_API_KEY = "sk-XXXXX" # Put your API key here!
MODEL_NAME = "claude-3-opus-20240229"

# Replace with your task!
TASK = "Draft an email responding to a customer complaint"

# Optional: specify the input variables you want Claude to use. If you want Claude to choose, you can set `variables` to an empty list!
VARIABLES = []

SAVE_PATH = './data'