# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Metrics to Find TLoC (Total-Lines-of-Code) metrics """


from baseblock import BaseObject


class MetricImportCounter(BaseObject):
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

        def is_import(input_line: str) -> bool:
            if input_line.startswith('from ') and ' import ' in input_line:
                return True
            if input_line.startswith('input '):
                return True
            return False

        input_lines = [x.strip() for x in input_lines if x and len(x)]
        input_lines = [x for x in input_lines if is_import(x)]

        return len(input_lines)
