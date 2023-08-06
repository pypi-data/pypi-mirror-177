# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Metrics to Find LoC (Lines-of-Code) metrics """


from baseblock import BaseObject


class MetricLocCounter(BaseObject):
    """ Metrics to Find LoC (Lines-of-Code) metrics """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_lines: list) -> int:

        input_lines = [x for x in input_lines if x and len(x)]

        return len(input_lines)
