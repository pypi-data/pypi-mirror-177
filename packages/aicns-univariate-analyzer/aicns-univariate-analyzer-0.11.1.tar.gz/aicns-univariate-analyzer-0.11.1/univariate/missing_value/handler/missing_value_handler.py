"""

"""

from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport
from univariate.missing_value.handler.strategy import MissingValueHandleStrategy, MissingValueHandleStrategyType
import importlib
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import plotly.express as px
from typing import Optional


class MissingValueHandler:
    """
    It can handle missing value with some strategies, such as imputation, deletion, filling constant, interpolation, and so on
    """
    def __init__(self, handler_type: MissingValueHandleStrategyType):
        concrete_cls = getattr(
            importlib.import_module("univariate.missing_value.handler.strategy"),
            handler_type.value
        )
        self.__handler_type: MissingValueHandleStrategyType = handler_type
        self.__handler: MissingValueHandleStrategy = concrete_cls()


    def handle_missing_value(self, missed_ts: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: Optional[str] = None, **kwargs) -> AnalysisReport:
        """

        :param missed_ts:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name: # todo: explain
        :param kwargs:
        :return:
        """
        # todo: decision logic decoupling, decision rule-engine?
        if handled_col_name is None:
            handled_col_name = data_col_name + "_mv_handled"
        filled_ts = self.__handler.handle(missed_ts, time_col_name, data_col_name, handled_col_name, **kwargs)
        report = self.__build_report(missed_ts, filled_ts, time_col_name, data_col_name, handled_col_name)
        return report


    def __build_report(self, missed_ts: DataFrame, filled_ts: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: str) -> AnalysisReport:
        """

        :param missed_ts:
        :param filled_ts:
        :param time_col_name:
        :param data_col_name:
        :return:
        """
        # todo: refactor report system
        report = AnalysisReport()
        report.parameters['strategy'] = self.__handler_type.value
        # report.parameters['mean'] = mean  # todo: build logic with specific strategy
        # report.parameters['ad-hoc'] = ad_hoc

        report.parameters['missed_ts'] = missed_ts
        report.parameters['filled_ts'] = filled_ts

        report.plots['disconnected_plot'] = self.__build_disconnected_plot(filled_ts, time_col_name, data_col_name)
        report.plots['connected_plot'] = self.__build_connected_plot(filled_ts, time_col_name, data_col_name, handled_col_name)

        return report


    def __build_disconnected_plot(self, filled_ts: DataFrame, time_col_name: str, data_col_name: str) -> Figure:
        """

        :param filled_ts:
        :param time_col_name:
        :param data_col_name:
        :return:
        """
        pd_df = filled_ts.select(time_col_name, data_col_name).sort(time_col_name).toPandas()
        fig = px.line(pd_df, x=time_col_name, y=data_col_name)
        return fig


    def __build_connected_plot(self, filled_ts: DataFrame, time_col_name: str, data_col_name: str, handled_col_name: str) -> Figure:
        """

        :param filled_ts:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name:
        :return:
        """
        pd_df = filled_ts.select(time_col_name, data_col_name, handled_col_name).sort(time_col_name).toPandas()
        fig = px.line(pd_df, x=time_col_name, y=handled_col_name)
        fig.add_trace(go.Scatter(x=pd_df[pd_df[data_col_name].isnull()][time_col_name],
                                 y=pd_df[pd_df[data_col_name].isnull()][handled_col_name],
                                 mode='markers',
                                 name='replaced value'))
        return fig
