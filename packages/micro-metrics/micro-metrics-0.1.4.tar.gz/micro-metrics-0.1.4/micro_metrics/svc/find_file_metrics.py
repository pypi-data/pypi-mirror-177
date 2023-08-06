# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Metrics to Find LoC (Lines-of-Code) metrics """


from baseblock import Enforcer
from baseblock import BaseObject

from micro_metrics.dmo import MetricFpCounter
from micro_metrics.dmo import MetricImportCounter
from micro_metrics.dmo import MetricLocCounter
from micro_metrics.dmo import MetricTLocCounter
from micro_metrics.dmo import MetricCCCounter


class FindFileMetrics(BaseObject):
    """ Metrics to Find LoC (Lines-of-Code) metrics """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._loc = MetricLocCounter().process
        self._tloc = MetricTLocCounter().process
        self._fps = MetricFpCounter().process
        self._ccs = MetricCCCounter().process
        self._imports = MetricImportCounter().process

    def process(self,
                d_input_files: dict) -> dict:

        if self.isEnabledForDebug:
            Enforcer.is_dict(d_input_files)

        results = []
        for file_name in d_input_files:
            input_lines = d_input_files[file_name]

            results.append({
                "FileName": file_name,
                "LOC": self._loc(input_lines),
                "TLOC": self._tloc(input_lines),
                "FP": self._fps(input_lines),
                "CC": self._ccs(input_lines),
                "Imports": self._imports(input_lines)
            })

        return results
