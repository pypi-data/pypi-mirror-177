# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Micro Metrics Orchestrator """


from baseblock import FileIO
from baseblock import Enforcer
from baseblock import BaseObject

from micro_metrics.svc import FindFileMetrics
from micro_metrics.svc import ReadFileContent
from micro_metrics.svc import FindFolderMetrics
from micro_metrics.svc import ComputeComplexity


class Orchestrator(BaseObject):
    """ Micro Metrics Orchestrator """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _sum_file_metrics(results: list) -> dict:

        loc = 0
        tloc = 0
        ccs = 0
        fps = 0
        imports = 0

        for result in results:
            loc += result['LOC']
            tloc += result['TLOC']
            ccs += result['CC']
            fps += result['FP']
            imports += result['Imports']

        return {
            'LOC': loc,
            'TLOC': tloc,
            'CC': ccs,
            'FP': fps,
            'Imports': imports
        }

    def run(self,
            microservice_directory: str) -> dict:

        if self.isEnabledForDebug:
            Enforcer.is_str(microservice_directory)

        FileIO.exists_or_error(microservice_directory)

        project_files = FileIO.load_all_files(microservice_directory, exclude=[
            '.git', '.pytest_cache', '__pycache__'])

        d_py_files = ReadFileContent().process(project_files['py'])
        if self.isEnabledForDebug:
            Enforcer.is_dict(d_py_files)

        def notebooks() -> int:
            if 'ipynb' in d_py_files:
                return len(d_py_files['ipynb'])
            return 0

        results = FindFileMetrics().process(d_py_files)

        d_sum_file = self._sum_file_metrics(results)
        d_sum_folder = FindFolderMetrics().process(microservice_directory)

        d_sum_file.update(d_sum_folder)
        d_sum_file['IPYNB'] = notebooks()

        complexity_score = ComputeComplexity().process(d_sum_file)

        d_sum_file['Complexity'] = complexity_score

        return d_sum_file
