"""
 Copyright (C) 2022 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import re
from typing import Optional
from openvino.runtime import layout_helpers


class Layout:
    def __init__(self, layout = '') -> None:
        self.layout = layout

    @staticmethod
    def from_shape(shape):
        '''
        Create Layout from given shape
        '''
        if len(shape) == 2:
            return 'NC'
        if len(shape) == 3:
            return 'CHW' if shape[0] in range(1, 5) else 'HWC'
        if len(shape) == 4:
            return 'NCHW' if shape[1] in range(1, 5) else 'NHWC'

        raise RuntimeError("Get layout from shape method doesn't support {}D shape".format(len(shape)))


    @staticmethod
    def from_openvino(input):
        '''
        Create Layout from openvino input
        '''
        return layout_helpers.get_layout(input).to_string().strip('[]').replace(',', '')

    @staticmethod
    def from_user_layouts(input_names: set, user_layouts: dict):
        '''
        Create Layout for input based on user info
        '''
        for input_name in input_names:
            if input_name in user_layouts:
                return user_layouts[input_name]
        return user_layouts.get('', '')


    @staticmethod
    def parse_layouts(layout_regex: str) -> Optional[dict]:
        '''
        Parse layout parameter in format "input0[NCHW],input1[NC]" or "[NCHW]" (applied to all inputs)
        '''
        if not layout_regex:
            return None
        inputs_layouts = layout_regex.split(',')
        user_layouts = {}
        for layout in inputs_layouts:
            if not re.fullmatch(r"[^\[\]]*\[[A-Z]+\]", layout):
                raise ValueError("invalid --layout option format")
            layout_list = layout.split('[')
            input_name = layout_list[0]
            input_layout = layout_list[1].strip('[]')
            user_layouts[input_name] = input_layout
        return user_layouts
