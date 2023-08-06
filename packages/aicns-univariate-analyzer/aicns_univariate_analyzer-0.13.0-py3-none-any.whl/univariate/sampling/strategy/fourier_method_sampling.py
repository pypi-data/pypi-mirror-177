"""

"""

from univariate.sampling.strategy import SamplingStrategy
from pyspark.sql import DataFrame
from typing import Optional, List
from univariate.sampling.utils import find_start_timestamp, construct_range_df
from scipy import signal


class FourierMethodSampling(SamplingStrategy):
    """
    Sampling strategy using fourier method
    """
    @staticmethod
    def sample(ts: DataFrame, time_col_name: str, data_col_name: str, period: int, sampling_period: int, by_freq: bool, count_flag_cols: Optional[List[str]] = None, agg_point: Optional[str] = "middle", display_point: Optional[str] = "first") -> DataFrame:
        """
        Sampling method using fourier method implemented by scipy
        Note: It is not Spark-native
        :param ts:
        :param time_col_name:
        :param data_col_name:
        :param period:
        :param sampling_period:
        :param by_freq:
        :param count_flag_cols:
        :param agg_point:
        :param display_point:
        :return:
        """
        # first range's start timestamp
        first_timestamp = ts.sort(time_col_name).first().asDict()[time_col_name]
        first_start = find_start_timestamp(first_timestamp, by_freq, sampling_period)

        # last range's start timestamp
        last_timestamp = ts.sort(time_col_name).tail(1)[0].asDict()[time_col_name]
        last_start = find_start_timestamp(last_timestamp, by_freq, sampling_period)

        # fit
        ts_pd = ts.sort(time_col_name).select(time_col_name, data_col_name).toPandas()
        # range df
        range_df = construct_range_df(sampling_period, first_start, last_start)

        # new point

        #
        # result