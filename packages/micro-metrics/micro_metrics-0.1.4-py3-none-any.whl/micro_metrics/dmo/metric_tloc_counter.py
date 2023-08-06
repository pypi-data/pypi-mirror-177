# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Metrics to Find TLoC (Total-Lines-of-Code) metrics """


from baseblock import FileIO
from baseblock import Enforcer
from baseblock import BaseObject


class MetricTLocCounter(BaseObject):
    """ Metrics to Find TLoC (Total-Lines-of-Code) metrics """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_lines: list) -> dict:

        input_lines = [x for x in input_lines if x and len(x)]
        input_lines = [x for x in input_lines if not x.strip().startswith('#')]

        line_no = 0
        normalized = []
        
        flag_comment = False
        total_lines = len(input_lines)

        while line_no < total_lines:

            line = input_lines[line_no]

            if line.strip().startswith('"""'):
                flag_comment = not flag_comment

            if not flag_comment:
                normalized.append(line)

            line_no += 1

        return len(normalized)
