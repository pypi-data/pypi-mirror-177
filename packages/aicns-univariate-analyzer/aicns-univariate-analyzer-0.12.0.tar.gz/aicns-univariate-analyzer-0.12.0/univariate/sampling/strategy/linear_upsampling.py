"""

"""

from univariate.sampling.strategy import SamplingStrategy
from pyspark.sql import DataFrame
from typing import Optional, List


class LinearUpsampling(SamplingStrategy):
    """

    """
    @staticmethod
    def sample(ts: DataFrame, time_col_name: str, data_col_name: str, period: int, sampling_period: int, by_freq: bool, count_flag_cols: Optional[List[str]] = None) -> DataFrame:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :param period:
        :param sampling_period:
        :param by_freq:
        :return:
        """

