"""

"""

from univariate.analyzer import Analyzer
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame
import plotly.express as px
from univariate.sampling.utils import freq_to_period_map
from statsmodels.tsa.seasonal import STL
import pandas as pd


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

        report = AnalysisReport()
        report.parameters["observed"] = stl.observed
        report.parameters["trend"] = stl.trend
        report.parameters["seasonal"] = stl.seasonal
        report.parameters["resid"] = stl.resid

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
