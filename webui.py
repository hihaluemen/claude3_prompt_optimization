#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/3 11:39
# @Author  : hihaluemen
# @File    : webui.py
import gradio as gr
from config import VARIABLES, TASK, ANTHROPIC_API_KEY, MODEL_NAME
from unit import get_prompt_opti, save_output

def main():
    with gr.Blocks() as app:
        with gr.Row():
            with gr.Column():
                task = gr.Textbox(
                    label="Your TASK",
                    value=f"{TASK}",
                    lines=10,
                    interactive=True
                )
            with gr.Column():
                variables = gr.Textbox(
                    label="The VARIABLES Of Your TASK",
                    value=f"{VARIABLES}",
                    lines=2,
                    interactive=True
                )
                api_key = gr.Textbox(
                    label='api key',
                    value=f'{ANTHROPIC_API_KEY}',
                    interactive=True
                )
                model_name = gr.Dropdown(
                    choices=['claude-3-opus-20240229', 'claude-3-5-sonnet-20240620', 'claude-3-haiku-20240307'],
                    value='claude-3-5-sonnet-20240620',
                    label='model'
                )


        with gr.Row():
            prompt_output = gr.Textbox(
                label='Your Prompt',
                lines=15,
                interactive=True
            )
            var_outputs = gr.Textbox(
                label='Output VARIABLES',
                lines=3,
                interactive=True
            )
        with gr.Row():
            with gr.Column():
                btn = gr.Button('Create Prompt')
            with gr.Column():
                stn = gr.Button('Save the Prompt')
        with gr.Row():
            file = gr.components.File(label='Download The Prompt')
            status = gr.Markdown(
                value='not save'
            )
        btn.click(get_prompt_opti, [task, variables, api_key, model_name], [prompt_output, var_outputs])
        stn.click(save_output, [prompt_output, var_outputs], [file, status])
    app.launch(server_name='127.0.0.1', server_port=8970)

if __name__ == '__main__':
    main()