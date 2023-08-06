# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Read File Content """


from baseblock import FileIO
from baseblock import Enforcer
from baseblock import BaseObject


class ReadFileContent(BaseObject):
    """ Read File Content """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_files: list) -> dict:

        if self.isEnabledForDebug:
            Enforcer.is_list_of_str(input_files)

        [FileIO.exists_or_error(input_file)
         for input_file in input_files]

        d = {}
        for input_file in input_files:
            d[input_file] = FileIO.read_lines(input_file)

        return d
