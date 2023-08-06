# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Metrics to Find CC (Cyclomatic Complexity) metrics """


from baseblock import BaseObject


class MetricCCCounter(BaseObject):
    """ Metrics to Find CC (Cyclomatic Complexity) metrics """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_lines: list) -> dict:

        input_lines = [x.strip() for x in input_lines if x and len(x)]
        total_definitions = len([x for x in input_lines
                                 if x.startswith('def ')])

        calls = 0
        for input_line in input_lines:
            if 'self.' in input_line or 'cls.' in input_line:
                calls += 1

        return calls + total_definitions
