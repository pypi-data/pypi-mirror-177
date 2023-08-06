# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Heuristic Computation of Complexity """


from baseblock import BaseObject


class ComputeComplexity(BaseObject):
    """ Heuristic Computation of Complexity """

    def __init__(self):
        """ Change Log

        Created:
            5-Sept-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                d_sum: dict) -> int:

        def loc() -> float:
            if 'LOC' in d_sum and d_sum['LOC']:
                return d_sum['LOC'] * 0.25
            return 0

        def tloc() -> float:
            if 'TLOC' in d_sum and d_sum['TLOC']:
                return d_sum['TLOC'] * 0.05
            return 0

        def ccs() -> float:
            if 'CC' in d_sum and d_sum['CC']:
                return d_sum['CC'] * 0.75
            return 0

        def fps() -> float:
            if 'FP' in d_sum and d_sum['FP']:
                return d_sum['FP'] * 0.50
            return 0

        def ipynb() -> float:
            if 'IPYNB' in d_sum and d_sum['IPYNB']:
                return d_sum['IPYNB'] * 2
            return 0

        def imports() -> float:
            if 'Imports' in d_sum and d_sum['Imports']:
                return d_sum['Imports'] * 0.15
            return 0

        def dmo() -> float:
            if 'DMO' in d_sum and d_sum['DMO']:
                return d_sum['DMO'] * 0.80
            return 0

        def svc() -> float:
            if 'SVC' in d_sum and d_sum['SVC']:
                return d_sum['SVC'] * 1.00
            return 0

        def bp() -> float:
            if 'BP' in d_sum and d_sum['BP']:
                return d_sum['BP'] * 1.10
            return 0

        def dto() -> float:
            if 'DTO' in d_sum and d_sum['DTO']:
                return d_sum['DTO'] * 0.60
            return 0

        def tests() -> float:
            if 'TESTS' in d_sum and d_sum['TESTS']:
                return d_sum['TESTS'] * 1.50
            return 0

        total = loc() + tloc() + ccs() + fps() + imports() + \
            dmo() + svc() + bp() + dto() + tests() + ipynb()

        return int(round(total, 0))
