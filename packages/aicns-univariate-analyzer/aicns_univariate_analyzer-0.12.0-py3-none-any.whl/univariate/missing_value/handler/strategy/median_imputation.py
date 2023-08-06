"""

"""

from univariate.missing_value.handler.strategy import MissingValueHandleStrategy, MissingValueHandleStrategyType
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from univariate.analyzer import AnalysisReport
from univariate.analyzer import DescriptiveStatAnalyzer
from typing import Optional


class MedianImputation(MissingValueHandleStrategy):
    """ """

    def handle(
        self, missed_ts: DataFrame, time_col_name: str, data_col_name, handled_col_name: str, median: Optional[float] = None, ad_hoc: bool=False
    ) -> DataFrame:
        """

        :param missed_ts:
        :param time_col_name:
        :param data_col_name:
        :param handled_col_name:
        :param median: It can only be None when ad_hoc is False. If ad_hoc is False and median is None, then throw exception
        :param ad_hoc:
        :return:
        """
        # validate: if non-ad-hoc (ad-hoc=False) run and median is None then it is invalid request
        if median is None and not ad_hoc:
            # todo: error log to spark logger
            raise TypeError("When Imputation is not ad-hoc, median value must be passed by argument")
        if ad_hoc:
            descriptive_stat_report = DescriptiveStatAnalyzer().analyze(missed_ts, time_col_name=time_col_name, data_col_name=data_col_name)  # todo: selective field
            median = descriptive_stat_report.parameters["median"]
        filled_ts = missed_ts.withColumn(handled_col_name, F.coalesce(data_col_name, F.lit(round(median, 3))))
        return filled_ts
