"""

"""

from abc import ABCMeta
from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport
from typing import Optional

class AnomalyDetector(metaclass=ABCMeta):
    """

    """
    @staticmethod
    def detect(ts: DataFrame, data_col_name: str, q1: Optional[float], median: Optional[float], q3: Optional[float], ad_hoc: bool=False) -> AnalysisReport:
        """

        :param ts:
        :param data_col_name:
        :param q1:
        :param median:
        :param q3:
        :param ad_hoc:
        :return:
        """
        pass
