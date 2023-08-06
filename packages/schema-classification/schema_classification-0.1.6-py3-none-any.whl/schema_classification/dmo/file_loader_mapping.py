#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
"""Load the Mapping File for a given Test Case"""


import os
from typing import Dict

from baseblock import FileIO
from baseblock import BaseObject


class FileLoaderMapping(BaseObject):
    """Load the Mapping File for a given Test Case"""

    def __init__(self):
        """
        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                test_case: Dict) -> dict:
        """ Load Mapping """

        # mapping defined within the test case
        if 'mappings' in test_case:
            return test_case['mappings']

        # test case references external mapping
        if 'mapping_file' in test_case:
            path = os.path.join(os.getcwd(),
                                'resources/mapping',
                                test_case['mapping_file'])
            return FileIO.file_to_yaml(path)

        raise ValueError
