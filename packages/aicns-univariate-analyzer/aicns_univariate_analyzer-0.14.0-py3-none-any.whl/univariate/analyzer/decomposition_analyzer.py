"""

"""

from univariate.analyzer import Analyzer
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame
import plotly.express as px
from univariate.sampling.utils import freq_to_period_map
from statsmodels.tsa.seasonal import STL
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


class DecompositionAnalyzer(Analyzer):
    """
    Decompose Time series
    """
    def __init__(self):
        """

        """
        # todo: decide decomposition strategy
        pass

    def analyze(self, ts: DataFrame, time_col_name: str, data_col_name: str, seasonal_freq: str, ts_period: int) -> AnalysisReport:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :param seasonal_freq:
        :param ts_period: milli seconds
        :return:
        """
        period = self.__calc_period(seasonal_freq, ts_period)
        ts_pd = ts.sort(time_col_name).select(time_col_name, data_col_name).toPandas()
        ts_pd[time_col_name] = pd.to_datetime(ts_pd[time_col_name], unit='ms')  # todo: ms constraint?
        stl = STL(ts_pd.set_index(time_col_name)[data_col_name], period=period).fit()  # todo: strategies for ts decompositions  #todo: multi seasonal

        decomposed_pd = pd.concat([stl.observed, stl.trend, stl.seasonal, stl.resid], axis=1).reset_index(drop=False)
        decomposed_df = SparkSession.getActiveSession().createDataFrame(decomposed_pd)
        decomposed_df = decomposed_df.withColumn(time_col_name, F.unix_timestamp(time_col_name) * 1000)
        decomposed_df = ts.join(decomposed_df, [time_col_name, data_col_name], "left").sort(time_col_name)

        report = AnalysisReport()
        report.parameters['decomposed_df'] = decomposed_df
        report.plots["decomposed"] = stl
        report.plots["observed"] = px.line(stl.observed)
        report.plots["seasonal"] = px.line(stl.seasonal)
        report.plots["trend"] = px.line(stl.trend)
        report.plots["resid"] = px.line(stl.resid)

        return report


    def __calc_period(self, seasonal_freq: str, ts_period: int):
        """

        :param seasonal_freq:
        :param ts_period:
        :return:
        """
        if seasonal_freq not in freq_to_period_map.keys():
            raise ValueError(f"seasonal_freq {seasonal_freq} is not supported")
        if (freq_to_period_map[seasonal_freq] / 2) < ts_period:
            raise ValueError(f"Seasonal component need at least 2 observed points. So ts_period should be less than half of seasonal period.")

        return int(round(freq_to_period_map[seasonal_freq] / ts_period))
