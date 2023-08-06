"""

"""

from abc import ABCMeta, abstractmethod
from enum import Enum
from pyspark.sql import DataFrame
from typing import Optional, List


class SamplingStrategyType(Enum):
    mean_downsampling = "MeanDownsampling"
    linear_upsampling = "LinearUpsampling"
    # fourier_method_sampling = "FourierMethodSampling"


class SamplingStrategy(metaclass=ABCMeta):
    """

    """
    @staticmethod
    @abstractmethod
    def sample(ts: DataFrame, time_col_name: str, data_col_name: str, period: int, sampling_period: int, by_freq: bool, count_flag_cols: List[str], **kwargs) -> DataFrame:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :param period:
        :param sampling_period:
        :param by_freq:
        :param count_flag_cols:
        :return:
        """
        pass
