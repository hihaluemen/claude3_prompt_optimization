#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/3 11:27
# @Author  : hihaluemen
# @File    : unit.py
import anthropic, re
from config import SAVE_PATH
from prompt import claude_3_metaprompt
import time, os



def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return ext_list

def remove_empty_tags(text):
    return re.sub(r'<(\w+)></\1>$', '', text)

def extract_prompt(metaprompt_response):
    between_tags = extract_between_tags("Instructions", metaprompt_response)[0]
    return remove_empty_tags(remove_empty_tags(between_tags).strip()).strip()

def extract_variables(prompt):
    pattern = r'{([^}]+)}'
    variables = re.findall(pattern, prompt)
    return set(variables)

def pretty_print(message):
    print('\n\n'.join('\n'.join(line.strip() for line in re.findall(r'.{1,100}(?:\s+|$)', paragraph.strip('\n'))) for paragraph in re.split(r'\n\n+', message)))
    return '\n\n'.join('\n'.join(line.strip() for line in re.findall(r'.{1,100}(?:\s+|$)', paragraph.strip('\n'))) for paragraph in re.split(r'\n\n+', message))

def get_prompt_opti(TASK, VARIABLES, API_KEY, MODEL_NAME):
    prompt = claude_3_metaprompt.replace("{{TASK}}", TASK)
    assistant_partial = "<Inputs>"

    variable_string = ""
    for variable in VARIABLES:
        variable_string += "\n{" + variable.upper() + "}"

    if variable_string:
        assistant_partial += variable_string + "\n</Inputs><Instructions Structure>"

    # claude 3 model
    CLIENT = anthropic.Anthropic(api_key=API_KEY)
    message = CLIENT.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": assistant_partial
            }
        ],
        temperature=0
    ).content[0].text

    extracted_prompt_template = extract_prompt(message)
    variables = extract_variables(message)

    return pretty_print(extracted_prompt_template), str(variables)

def save_output(outputs, variables=None):
    now_time = time.strftime("%Y-%m-%d", time.localtime())
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    file_name = os.path.join(SAVE_PATH, now_time+'_prompt.txt')
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('Your Pompt is:\n')
        f.write(outputs.strip())
        f.write('\n\n')
        if variables:
            f.write('Your Variables is:\n')
            f.write(variables.strip())

    return file_name, 'save success!'




