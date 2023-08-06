"""

"""


from pyspark.sql import DataFrame
from univariate.sampling.strategy import SamplingStrategy, MeanDownsampling, LinearUpsampling
from univariate.sampling.utils import freq_to_period_map
from typing import List, Optional




class Sampler:
    """

    """

    @staticmethod
    def sample_by_freq_alias(ts: DataFrame, time_col_name: str, data_col_name: str, period: int, freq: str, count_flag_cols: Optional[List[str]] = []) -> DataFrame:
        """

        :return:
        """
        assert Sampler.__validate_freq_alias(freq)
        sampling_strategy = Sampler.__instantiate_sampling_strategy(period, freq_to_period_map[freq])
        return sampling_strategy.sample(ts, time_col_name, data_col_name, period, freq_to_period_map[freq], True, count_flag_cols)

    @staticmethod
    def __validate_freq_alias(freq: str) -> bool:
        """

        :param freq: frequency alias
        :return: if freq is valid return true, else exception will be raised

        Note: please see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
        (221117) Support alias: 'A', 'Q', 'M', 'W', 'D', 'H'
        """
        # todo: if you want more aliases issue a ticket
        supports = ['A', 'Q', 'M', 'W', 'D', 'H']
        if freq not in supports:
            raise ValueError(f"freq {freq} is not supported now, supports {supports} (if you want more aliases issue a ticket)")

        return True

    @staticmethod
    def __instantiate_sampling_strategy(period: int, sampling_period) -> SamplingStrategy:
        """

        :param period:
        :param sampling_period:
        :return:
        """
        # todo: parameterize or auto-decision instantiation
        if period <= sampling_period:
            strategy = MeanDownsampling()
        else:
            strategy = LinearUpsampling()

        return strategy
