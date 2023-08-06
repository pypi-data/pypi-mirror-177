# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Metrics to Find Structural Metrics for the Microservice """


from baseblock import FileIO
from baseblock import BaseObject


class FindFolderMetrics(BaseObject):
    """ Metrics to Find Structural Metrics for the Microservice """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_directory: str) -> dict:

        d_results = {}

        d_folders = FileIO.load_all_folders(
            input_directory,
            exclude=['.git', '__pycache__', '.pytest_cache'])

        for folder_name in d_folders:
            if folder_name in ['bp', 'svc', 'dmo', 'dto', 'tests']:
                d_results[folder_name] = len(d_folders[folder_name])

        return {k.upper(): d_results[k] for k in d_results}
