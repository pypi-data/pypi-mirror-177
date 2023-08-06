# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Metrics to Find FPs (Function Point) metrics """


from baseblock import BaseObject


class MetricFpCounter(BaseObject):
    """ Metrics to Find FPs (Function Point) metrics """

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
        input_lines = [x for x in input_lines if x.startswith('def ')]

        return len(input_lines)
